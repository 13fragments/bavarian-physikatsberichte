#!/usr/bin/env python3
"""Build the canonical 1860 Bavarian district index and extract topic candidates.

Outputs under `data/dataset/`:
1. `districts_index.json` & `districts_index.csv` — 239 canonical Bavarian medical
   districts across 7 Regierungsbezirke, with exact volume/canvas slices and WGS84 coords.
2. `district_epidemiology_candidates.json` — per-district top candidate canvases for:
   - `infant_feeding` (first-year nutrition, breastfeeding, Mehlbrei, pacifiers, poppy/alcohol)
   - `goiter_cretinism` (Kropf / Struma / Kretinismus)
   - `mortality_table` (vital-statistics birth & infant-mortality tables)
   - `folk_medicine` (Aberglauben, Sympathie, Geheimmittel, quackery)
"""

from __future__ import annotations

import csv
from difflib import SequenceMatcher
import gzip
import json
from pathlib import Path
import re
import sys

from district_gazetteer_data import (
    COLLECTIVE_VOLUME_SLICES,
    DISTRICT_COORDINATES,
    SINGLE_VOLUME_CANONICAL_NAME,
)

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "data" / "catalog" / "volumes.jsonl"
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
DATASET_DIR = ROOT / "data" / "dataset"

# OCR- and dialect-tolerant patterns tailored to 1860 Bavarian Kurrent & Kurrent 1B errors
PAT_INFANT_CORE = re.compile(
    r"(ersten\s+lebensjahr|erste[ns]?\s+jahr|säugling|neugebor|kinderpflege|ernährung\s+der\s+kinder|"
    r"kinderernährung|kindersterblichkeit|mutterbrust|mutterkunst|brust\s+gereicht|selbststill|gestillt|"
    r"stillen\s+der|säugen|gesäugt|säugung|[mw]ehlbrei|kindsmu[sß]|kindsbrei|schnuller|"
    r"saugschlo[tz]er|schlo[tz]er|zulp|zulze|zuzel|luller|sauglappen|"
    r"mohn|schlafmohn|opium|theriak|branntwein|schnaps|schmack)",
    re.IGNORECASE,
)
PAT_INFANT_HIGH = re.compile(
    r"(ersten\s+lebensjahr|[mw]ehlbrei|mutterbrust|selbststill|gestillt|säugen|gesäugt|"
    r"schnuller|saugschlo[tz]er|schlo[tz]er|zulp|zulze|zuzel|luller|"
    r"mohnk[öo]pf|schlafmohn|mohnabsud|kindersterblichkeit)",
    re.IGNORECASE,
)
PAT_GOITER = re.compile(
    r"(kropf|kröpfe|struma|cretin|kretin|blödsinn|halblödsinn|schilddrüse)",
    re.IGNORECASE,
)
PAT_MORTALITY_TABLE = re.compile(
    r"(sterb[ef]?f[äa]lle|stertf[äa]lle|gestorben|geburten|lebensjahr|0\s*[–-]\s*1|unter\s+1\s+jahr)",
    re.IGNORECASE,
)
PAT_FOLK = re.compile(
    r"(aberglaub|sympathie|pfusch|quacksalb|geheimmittel|amulett|segen|besprech|hexen|verhex|"
    r"schinder|hundsschmalz|dachsschmalz|volksarznei|volksheilmittel|volksmittel|arsenik)",
    re.IGNORECASE,
)


def slugify(name: str) -> str:
    s = name.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def is_duplicate_pair(prev_text: str, curr_text: str) -> bool:
    a = re.sub(r"\s+", " ", (prev_text or "").strip().lower())
    b = re.sub(r"\s+", " ", (curr_text or "").strip().lower())
    if len(a) < 200 or len(b) < 200:
        return False
    if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.25:
        return False
    return SequenceMatcher(None, a[:1500], b[:1500]).ratio() >= 0.88


def score_infant_page(text: str) -> tuple[int, list[str]]:
    core = [m.group(0).lower() for m in PAT_INFANT_CORE.finditer(text)]
    if not core:
        return 0, []
    high = [m.group(0).lower() for m in PAT_INFANT_HIGH.finditer(text)]
    distinct = sorted(set(core))
    score = len(distinct) * 3 + len(set(high)) * 5 + min(len(core), 10)
    # Penalize short table-of-contents lines so actual narrative pages rank highest
    if "inhalts" in text.lower()[:120] or text.count("...") > 3:
        score = max(1, score - 8)
    return score, distinct


def score_folk_page(text: str) -> tuple[int, list[str]]:
    hits = [m.group(0).lower() for m in PAT_FOLK.finditer(text)]
    if not hits:
        return 0, []
    distinct = sorted(set(hits))
    score = len(distinct) * 4 + min(len(hits), 10)
    if "inhalts" in text.lower()[:120] or text.count("...") > 3:
        score = max(1, score - 8)
    return score, distinct


def score_goiter_page(text: str) -> tuple[int, list[str]]:
    hits = [m.group(0).lower() for m in PAT_GOITER.finditer(text)]
    if not hits:
        return 0, []
    distinct = sorted(set(hits))
    return len(distinct) * 4 + min(len(hits), 8), distinct


def score_table_page(text: str) -> tuple[int, list[str]]:
    hits = [m.group(0).lower() for m in PAT_MORTALITY_TABLE.finditer(text)]
    digits = sum(ch.isdigit() for ch in text)
    if len(set(hits)) < 2 or digits < 25:
        return 0, []
    distinct = sorted(set(hits))
    bonus = 8 if "<table>" in text.lower() else 0
    return len(distinct) * 3 + min(digits // 20, 10) + bonus, distinct


def main() -> int:
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    catalog = [
        json.loads(ln)
        for ln in CATALOG_FILE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    admitted = [r for r in catalog if r.get("admitted")]

    # Build district -> list of slices `{bsb_id, volume_number, start_canvas, end_canvas}`
    district_slices: dict[str, list[dict]] = {}
    for vol in admitted:
        bid = vol["bsb_id"]
        vno = vol["volume_number"]
        ccount = int(vol["canvas_count"])
        if bid in COLLECTIVE_VOLUME_SLICES:
            for dname, start_c, end_c in COLLECTIVE_VOLUME_SLICES[bid]:
                district_slices.setdefault(dname, []).append(
                    {
                        "bsb_id": bid,
                        "volume_number": vno,
                        "start_canvas": start_c,
                        "end_canvas": min(end_c, ccount),
                    }
                )
        else:
            dname = SINGLE_VOLUME_CANONICAL_NAME.get(bid, vol["district"])
            district_slices.setdefault(dname, []).append(
                {
                    "bsb_id": bid,
                    "volume_number": vno,
                    "start_canvas": 1,
                    "end_canvas": ccount,
                }
            )

    missing_coords = sorted(set(district_slices) - set(DISTRICT_COORDINATES))
    if missing_coords:
        raise KeyError(f"Districts missing from DISTRICT_COORDINATES: {missing_coords}")

    # Cache loaded transcripts once
    vol_pages_cache: dict[str, list[dict]] = {}
    missing_transcripts: list[str] = []
    for vol in admitted:
        bid = vol["bsb_id"]
        tpath = TRANSCRIPTS_DIR / f"{bid}.jsonl.gz"
        if not tpath.exists():
            missing_transcripts.append(bid)
            continue
        with gzip.open(tpath, "rt", encoding="utf-8") as gz:
            pages = sorted([json.loads(ln) for ln in gz if ln.strip()], key=lambda p: int(p["canvas_number"]))
        # Mark consecutive duplicate microfilm frames
        prev_txt = ""
        prev_cno = -10
        for p in pages:
            cno = int(p["canvas_number"])
            txt = p.get("text") or ""
            p["_is_dup"] = cno == prev_cno + 1 and is_duplicate_pair(prev_txt, txt)
            prev_txt = txt
            prev_cno = cno
        vol_pages_cache[bid] = pages

    districts_index = []
    candidates_out = []

    for dname in sorted(district_slices):
        regbez, lat, lon = DISTRICT_COORDINATES[dname]
        jtype = (
            "Stadt"
            if "(Stadt)" in dname or dname in ("Augsburg", "Nürnberg", "Fürth", "Hof", "Speyer")
            else ("Kanton" if regbez == "Pfalz" else "Landgericht")
        )
        slices = sorted(district_slices[dname], key=lambda s: (s["bsb_id"], s["start_canvas"]))
        total_slice_pages = sum(s["end_canvas"] - s["start_canvas"] + 1 for s in slices)
        did = slugify(dname)

        d_meta = {
            "district_id": did,
            "district_name": dname,
            "regierungsbezirk": regbez,
            "jurisdiction_type": jtype,
            "latitude": lat,
            "longitude": lon,
            "total_canvases": total_slice_pages,
            "bsb_ids": ";".join(dict.fromkeys(s["bsb_id"] for s in slices)),
            "volume_numbers": ";".join(dict.fromkeys(s["volume_number"] for s in slices)),
            "slices": slices,
        }
        districts_index.append(d_meta)

        infant_hits = []
        goiter_hits = []
        table_hits = []
        folk_hits = []

        for sl in slices:
            bid = sl["bsb_id"]
            pages = vol_pages_cache.get(bid, [])
            page_map = {int(p["canvas_number"]): p for p in pages}
            for cno in range(sl["start_canvas"], sl["end_canvas"] + 1):
                p = page_map.get(cno)
                if not p or p.get("_is_dup"):
                    continue
                txt = p.get("text") or ""
                if not txt.strip():
                    continue

                sc_inf, terms_inf = score_infant_page(txt)
                if sc_inf > 0:
                    # Include +/- 1 page text context in case sentence crosses a page break!
                    prev_p = page_map.get(cno - 1) if cno - 1 >= sl["start_canvas"] else None
                    next_p = page_map.get(cno + 1) if cno + 1 <= sl["end_canvas"] else None
                    infant_hits.append(
                        {
                            "bsb_id": bid,
                            "volume_number": sl["volume_number"],
                            "canvas_number": cno,
                            "score": sc_inf,
                            "terms": terms_inf,
                            "iiif_image_url": p["iiif_image_url"],
                            "mdz_page_url": f"https://www.digitale-sammlungen.de/de/view/{bid}?page={cno}",
                            "text": txt,
                            "prev_canvas_tail": (prev_p.get("text") or "")[-350:] if prev_p else "",
                            "next_canvas_head": (next_p.get("text") or "")[:350] if next_p else "",
                        }
                    )

                sc_goi, terms_goi = score_goiter_page(txt)
                if sc_goi > 0:
                    goiter_hits.append(
                        {
                            "bsb_id": bid,
                            "volume_number": sl["volume_number"],
                            "canvas_number": cno,
                            "score": sc_goi,
                            "terms": terms_goi,
                            "iiif_image_url": p["iiif_image_url"],
                            "mdz_page_url": f"https://www.digitale-sammlungen.de/de/view/{bid}?page={cno}",
                            "text": txt,
                        }
                    )

                sc_tbl, terms_tbl = score_table_page(txt)
                if sc_tbl > 0:
                    table_hits.append(
                        {
                            "bsb_id": bid,
                            "volume_number": sl["volume_number"],
                            "canvas_number": cno,
                            "score": sc_tbl,
                            "terms": terms_tbl,
                            "iiif_image_url": p["iiif_image_url"],
                            "mdz_page_url": f"https://www.digitale-sammlungen.de/de/view/{bid}?page={cno}",
                            "text": txt,
                        }
                    )

                sc_flk, terms_flk = score_folk_page(txt)
                if sc_flk > 0:
                    folk_hits.append(
                        {
                            "bsb_id": bid,
                            "volume_number": sl["volume_number"],
                            "canvas_number": cno,
                            "score": sc_flk,
                            "terms": terms_flk,
                            "iiif_image_url": p["iiif_image_url"],
                            "mdz_page_url": f"https://www.digitale-sammlungen.de/de/view/{bid}?page={cno}",
                            "text": txt,
                        }
                    )

        infant_hits.sort(key=lambda x: (-x["score"], x["canvas_number"]))
        goiter_hits.sort(key=lambda x: (-x["score"], x["canvas_number"]))
        table_hits.sort(key=lambda x: (-x["score"], x["canvas_number"]))
        folk_hits.sort(key=lambda x: (-x["score"], x["canvas_number"]))

        candidates_out.append(
            {
                **d_meta,
                "infant_feeding_candidates": infant_hits[:4],
                "goiter_cretinism_candidates": goiter_hits[:3],
                "mortality_table_candidates": table_hits[:3],
                "folk_medicine_candidates": folk_hits[:4],
            }
        )

    (DATASET_DIR / "districts_index.json").write_text(
        json.dumps(districts_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (DATASET_DIR / "districts_index.csv").open("w", encoding="utf-8", newline="") as f:
        fields = [
            "district_id",
            "district_name",
            "regierungsbezirk",
            "jurisdiction_type",
            "latitude",
            "longitude",
            "total_canvases",
            "bsb_ids",
            "volume_numbers",
            "slices_json",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for d in districts_index:
            row = {k: d[k] for k in fields if k != "slices_json"}
            row["slices_json"] = json.dumps(d["slices"], ensure_ascii=False)
            w.writerow(row)

    (DATASET_DIR / "district_epidemiology_candidates.json").write_text(
        json.dumps(candidates_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with_inf = sum(1 for c in candidates_out if c["infant_feeding_candidates"])
    with_goi = sum(1 for c in candidates_out if c["goiter_cretinism_candidates"])
    with_tbl = sum(1 for c in candidates_out if c["mortality_table_candidates"])
    with_flk = sum(1 for c in candidates_out if c["folk_medicine_candidates"])
    print(
        json.dumps(
            {
                "canonical_districts": len(districts_index),
                "missing_transcripts": len(missing_transcripts),
                "districts_with_infant_hits": with_inf,
                "districts_with_goiter_hits": with_goi,
                "districts_with_table_hits": with_tbl,
                "districts_with_folk_hits": with_flk,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
