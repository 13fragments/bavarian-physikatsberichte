#!/usr/bin/env python3
"""Compile image-verified shards into final CSVs, GeoJSON, passage table, summary stats, and QA viewer.

Outputs under `data/dataset/`:
1. `verified_bavaria_1860_infant_feeding.csv` (separated birth-cohort vs all-deaths columns + flags)
2. `verified_bavaria_1860_folk_medicine.csv`
3. `verified_passages.csv` (normalized passage-level evidence table for every published quotation)
4. `map_bavaria_1860_infant_feeding.geojson` (separated mortality properties; never pools denominators)
5. `epidemiology_summary_stats.json` (includes strict live-births sensitivity & Mann-Whitney AUC)
6. `verification_viewer.html`
"""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path
import re
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "data" / "dataset"
DISTRICTS_INDEX_JSON = DATASET_DIR / "districts_index.json"
DISTRICT_SHARDS_DIR = DATASET_DIR / "verified_shards"
FOLK_SHARDS_DIR = DATASET_DIR / "verified_folk_shards"

VALID_BREASTFEEDING = {
    "predominantly_breastfed",
    "mixed_or_short_duration",
    "rarely_or_not_breastfed",
    "not_documented",
}
VALID_MEHLBREI = {
    "predominant_early_diet",
    "supplemental",
    "explicitly_rare_or_absent",
    "not_documented",
}
# Shared by goiter_status and cretinism_status; each column describes one condition only.
CONDITION_STATUSES = (
    "endemic_or_frequent",
    "sporadic_or_localized",
    "explicitly_absent",
    "not_documented",
)
CONDITION_COLUMNS = ("goiter_status", "cretinism_status")
VALID_DENOMINATORS = {"live_births", "total_births_incl_stillborn", "all_deaths", "not_applicable", ""}
VALID_VERIFICATION = {"Agent-checked", "No-relevant-section", "Seen"}

# Explicit mortality flags audited against primary scan details
STILLBIRTH_IN_NUMERATOR_IDS = {"landstuhl", "regensburg_land"}
APPROXIMATE_MORTALITY_IDS = {"eggenfelden"}
SPECIAL_AGE_WINDOWS = {"ebermannstadt": "before_smallpox_vaccination"}

# Secondary verified passages cited in Articles 1 and 2 beyond each district/page primary quote
SECONDARY_VERIFIED_PASSAGES = [
    {
        "passage_id": "roggenburg_p15_schnaps",
        "source_table": "secondary_verified_passage",
        "district_id": "roggenburg",
        "district_name": "Roggenburg",
        "regierungsbezirk": "Schwaben und Neuburg",
        "bsb_id": "bsb00007355",
        "volume_number": "153",
        "canvas_number": 15,
        "topic": "infant_alcohol_pacifier",
        "mdz_page_url": "https://www.digitale-sammlungen.de/de/view/bsb00007355?page=15",
        "iiif_image_url": "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00007355_00015/full/full/0/default.jpg",
        "verified_german_quote": "Allein das Aller Empörendste ist, daß in solchen versoffenen Familien schon die Säuglinge an dieses gefährliche Getränk gewöhnt, u ihre Schnuller in Schnaps eingetaucht werden, damit sie schneller u länger schlafen sollen!!! Was Wunder, wenn solche unglückliche Geschöpfe dem Hydrocephalus oder dem habituellen Blödsinne verfallen.",
        "english_translation": "Yet the most outrageous thing of all is that in such heavy-drinking families even nursing infants are accustomed to this dangerous drink, and their pacifiers are dipped in schnapps so that they should sleep faster and longer!!! What wonder if such unfortunate creatures fall prey to hydrocephalus or habitual idiocy.",
        "ocr_corrections_noted": "Fixed OCR 'Emperor este' -> 'Empörendste', 'vorhöffenen' -> 'versoffenen', 'Schmack' -> 'Schnaps', and 'Blodseine' -> 'Blödsinne' on scan 15.",
        "verification_status": "Agent-checked",
    },
    {
        "passage_id": "roggenburg_p27_syphilis",
        "source_table": "secondary_verified_passage",
        "district_id": "roggenburg",
        "district_name": "Roggenburg",
        "regierungsbezirk": "Schwaben und Neuburg",
        "bsb_id": "bsb00007355",
        "volume_number": "153",
        "canvas_number": 27,
        "topic": "pacifier_syphilis_transmission",
        "mdz_page_url": "https://www.digitale-sammlungen.de/de/view/bsb00007355?page=27",
        "iiif_image_url": "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00007355_00027/full/full/0/default.jpg",
        "verified_german_quote": "Vor einigen Jahren steckte eine solche Magd mit Chancres im Halse, die dem neugeborenen Kinde ihrer Dienstherrschaft den Schnuller annezte, dieses an, indem es Chancres in beiden Mundwinkeln u an der Zungenspitze bekam, u das Kind, welches an der Mutter trank, inficirte die mütterlichen Brustwarzen, die mit tief fressenden Chancres bedeckt wurden.",
        "english_translation": "Some years ago such a housemaid with chancres in her throat, who moistened the pacifier of her employers' newborn child, infected the child so that it developed chancres at both corners of the mouth and on the tip of the tongue, and the child, nursing at its mother, infected the mother's nipples, which became covered with deep-eating chancres.",
        "ocr_corrections_noted": "Fixed OCR 'anmugte' -> 'annezte' and 'leuen' -> 'beiden' on margin note *2 of scan 27.",
        "verification_status": "Agent-checked",
    },
    {
        "passage_id": "greding_p131_mieder",
        "source_table": "secondary_verified_passage",
        "district_id": "greding",
        "district_name": "Greding",
        "regierungsbezirk": "Mittelfranken",
        "bsb_id": "bsb00141175",
        "volume_number": "57,1",
        "canvas_number": 131,
        "topic": "mieder_bodice_within_district_contrast",
        "mdz_page_url": "https://www.digitale-sammlungen.de/de/view/bsb00141175?page=131",
        "iiif_image_url": "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00141175_00131/full/full/0/default.jpg",
        "verified_german_quote": "In der Gruppe Greding kommt dazu noch eine sehr beachtenswerthe Schädlichkeit durch die Mieder. Diese schnüren nicht blos den Brustkasten zusammen u hemmen die ganze Ausbildung desselben, sie drücken auch noch speciell die Brüste, hindern deren Entwicklung u pressen die Warzen so hinein, daß sie zum Säugen untauglich werden oder das Säugen für die Mutter so schmerzhaft machen, daß sie es unterlassen muß. In der Gruppe Stauf fällt dieser Mißstand durch die Form der Leibchen weg.",
        "english_translation": "In the Greding group there is an additional very noteworthy harm from the Mieder [bodices]. These not only lace the ribcage tight and impede its entire development; they also press specifically upon the breasts, hinder their development, and press the nipples so far inward that they become unfit for nursing or make nursing so painful for the mother that she must give it up. In the Stauf group this defect disappears because of the shape of the Leibchen [bodices].",
        "ocr_corrections_noted": "Verified letter-for-letter against scan 131 (manuscript page 129).",
        "verification_status": "Agent-checked",
    },
    {
        "passage_id": "landshut_land_p33_mieder",
        "source_table": "secondary_verified_passage",
        "district_id": "landshut_land",
        "district_name": "Landshut (Land)",
        "regierungsbezirk": "Niederbayern",
        "bsb_id": "bsb00111891",
        "volume_number": "97",
        "canvas_number": 33,
        "topic": "mieder_bodice_nipples",
        "mdz_page_url": "https://www.digitale-sammlungen.de/de/view/bsb00111891?page=33",
        "iiif_image_url": "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00111891_00033/full/full/0/default.jpg",
        "verified_german_quote": "Die steifen Mieder üben übrigens auf die Brust eine sehr nachtheilige Wirkung, die Warze wird eingedrückt und zum Stillen nicht mehr geeignet; während in späteren Jahren die heruntergedrängte weibliche Brust häßlich hängt.",
        "english_translation": "The stiff bodices moreover exert a very harmful effect on the breast: the nipple is pressed inward and made no longer suitable for nursing, while in later years the downward-forced female breast hangs unattractively.",
        "ocr_corrections_noted": "Verified letter-for-letter against scan 33.",
        "verification_status": "Agent-checked",
    },
    {
        "passage_id": "amberg_land_p174_beer",
        "source_table": "secondary_verified_passage",
        "district_id": "amberg_land",
        "district_name": "Amberg (Land)",
        "regierungsbezirk": "Oberpfalz und Regensburg",
        "bsb_id": "bsb00026307",
        "volume_number": "5",
        "canvas_number": 174,
        "topic": "infant_child_beer",
        "mdz_page_url": "https://www.digitale-sammlungen.de/de/view/bsb00026307?page=174",
        "iiif_image_url": "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00026307_00174/full/full/0/default.jpg",
        "verified_german_quote": "Hier trinken schon die kleinen Kinder Bier und nach dem Abgewöhnen von der Brust geben viele Mütter ihren Kleinen gewässertes Bier oder Nachbier zum trinken. ... Schon deren Kinder gewöhnen sich ans Biertrinken und man sieht oft schon am Vormittage solche Kleine vollkommen berauscht.",
        "english_translation": "Here even small children drink beer, and after weaning from the breast many mothers give their little ones watered beer or small beer to drink. ... Even their children grow accustomed to beer drinking, and one often sees such little ones completely intoxicated already in the forenoon.",
        "ocr_corrections_noted": "Verified against scan 174 (manuscript page 145); fixed OCR 'trincken' -> 'trinken'.",
        "verification_status": "Agent-checked",
    },
    {
        "passage_id": "markt_erlbach_p124_poppy_schnaps",
        "source_table": "secondary_verified_passage",
        "district_id": "markt_erlbach",
        "district_name": "Markt Erlbach",
        "regierungsbezirk": "Mittelfranken",
        "bsb_id": "bsb00143123",
        "volume_number": "109",
        "canvas_number": 124,
        "topic": "infant_poppy_and_schnaps",
        "mdz_page_url": "https://www.digitale-sammlungen.de/de/view/bsb00143123?page=124",
        "iiif_image_url": "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00143123_00124/full/full/0/default.jpg",
        "verified_german_quote": "Daß stillende Mütter zur Beruhigung ihrer Kinder Branntwein trinken, oder ihn den Kindern selbst, namentlich beim Abgewöhnen zur Beförderung des Schlafes zu trinken geben, so wie daß Bauersweiber, zu gleichem Zwecke, ihren Kindern die Saamen von Papaver somnifer., gewöhnlich auf Brod, oder auch gekocht darreichen, sind weiter zu beobachtende Mißbräuche.",
        "english_translation": "That nursing mothers drink schnapps to quiet their children, or give it to the children themselves to drink, especially at weaning to promote sleep, as well as that peasant women for the same purpose give their children the seeds of Papaver somniferum, usually on bread or boiled, are further abuses to be observed.",
        "ocr_corrections_noted": "Fixed OCR 'Beamtwein' -> 'Branntwein', 'Schleifes' -> 'Schlafes', 'Bauersväter' -> 'Bauersweiber', 'Seemen' -> 'Saamen', 'baxd' -> 'Brod', 'gekraft' -> 'gekocht', and 'Mißkrieche' -> 'Mißbräuche' on scan 124 (ms p. 61).",
        "verification_status": "Agent-checked",
    },
    {
        "passage_id": "parsberg_p134_night_watchman",
        "source_table": "secondary_verified_passage",
        "district_id": "parsberg",
        "district_name": "Parsberg",
        "regierungsbezirk": "Oberpfalz und Regensburg",
        "bsb_id": "bsb00003359",
        "volume_number": "137",
        "canvas_number": 134,
        "topic": "folk_medicine_witchcraft_anecdote",
        "mdz_page_url": "https://www.digitale-sammlungen.de/de/view/bsb00003359?page=134",
        "iiif_image_url": "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00003359_00134/full/full/0/default.jpg",
        "verified_german_quote": "Davon erzählte ein Nachtwächter einem vertrauten Freunde: = Als ich einmal zwischen 11 u. 12 Uhr in einem Ecke saß, um auszuruhen, kamen nach und nach mehrere Weibspersonen bei dunklem Mondenschein mit Besen und Ofengabeln daher, kehrten und tanzten im Kreise herum, und als sie ihn erblickten, schlich sich Eine von diesen zu ihm hin, um zu sehen, ob er schläft, od. nicht /: es war sein eigenes Weib :/. Ich stellte mich, als schlafe ich fest. Da ging sie wieder zu ihrer Gesellschaft zurück und sagte: er schläft fest und hört nichts. Und nun machten selbe ihren Tanz noch einige Zeit fort, und auf Einmal waren sie meinen Augen verschwunden.",
        "english_translation": "A night watchman told a trusted friend about this: 'Once, as I sat in a corner between 11 and 12 o'clock to rest, several women came along one after another in dim moonlight with brooms and oven-forks, swept, and danced around in a circle; and when they caught sight of him, one of them crept over to see whether he was asleep or not (it was his own wife). I pretended to be fast asleep. Then she went back to her company and said: he is fast asleep and hears nothing. And so they continued their dance for some time, and all at once they vanished from my eyes.'",
        "ocr_corrections_noted": "Verified directly on scan 134: fixed 'Vorlauten' -> 'vertrauten', 'mehrern' -> 'mehrere', 'Ofenzabeln' -> 'Ofengabeln', 'Tanzten in' -> 'tanzten im', 'hm ... d.' -> 'hin ... od.', 'fast' -> 'fest', and 'Eumiae' -> 'Einmal'.",
        "verification_status": "Agent-checked",
    },
]


def has_logged_ocr_correction(row: dict) -> bool:
    if row.get("verification_status") != "Agent-checked":
        return False
    note = (row.get("ocr_corrections_noted") or "").strip()
    if not note:
        return False
    low = note.lower()
    if "->" in note or "→" in note or re.search(r"\b(fixed|corrected|restored|recovered|omitted)\b", low):
        return True
    if low.startswith("exact match") or low.startswith("no ocr") or low.startswith("verified"):
        return False
    return True


def mann_whitney_auc(group_low: list[float], group_high: list[float]) -> dict[str, float | int | None]:
    if not group_low or not group_high:
        return {"u": None, "max_u": 0, "auc": None}
    u = sum(
        (1.0 if hi > lo else 0.5 if hi == lo else 0.0)
        for lo in group_low
        for hi in group_high
    )
    max_u = len(group_low) * len(group_high)
    return {"u": round(u, 2), "max_u": max_u, "auc": round(u / max_u, 4)}


def group_summary(vals: list[float]) -> dict[str, float | int | None]:
    if not vals:
        return {"n": 0, "median_pct": None, "mean_pct": None, "min_pct": None, "max_pct": None}
    return {
        "n": len(vals),
        "median_pct": round(statistics.median(vals), 2),
        "mean_pct": round(statistics.mean(vals), 2),
        "min_pct": round(min(vals), 2),
        "max_pct": round(max(vals), 2),
    }


def condition_breakdown(rows: list[dict], column: str) -> dict[str, int]:
    return {status: sum(1 for r in rows if r[column] == status) for status in CONDITION_STATUSES}


def validate_district_rows(district_rows: list[dict]) -> None:
    expected_index = json.loads(DISTRICTS_INDEX_JSON.read_text(encoding="utf-8"))
    expected_ids = {d["district_id"] for d in expected_index}
    row_ids = [r["district_id"] for r in district_rows]
    if len(row_ids) != len(set(row_ids)):
        raise ValueError("Duplicate district_id entries detected across verified shards.")
    if set(row_ids) != expected_ids:
        missing = sorted(expected_ids - set(row_ids))
        extra = sorted(set(row_ids) - expected_ids)
        raise ValueError(f"District ID mismatch vs districts_index.json: missing={missing}, extra={extra}")
    for r in district_rows:
        if not isinstance(r.get("infant_feeding_documented"), bool):
            raise TypeError(f"{r['district_id']}: infant_feeding_documented must be bool")
        if r.get("breastfeeding_status") not in VALID_BREASTFEEDING:
            raise ValueError(f"{r['district_id']}: invalid breastfeeding_status={r.get('breastfeeding_status')}")
        if r.get("mehlbrei_gruel_status") not in VALID_MEHLBREI:
            raise ValueError(f"{r['district_id']}: invalid mehlbrei_gruel_status={r.get('mehlbrei_gruel_status')}")
        for col in CONDITION_COLUMNS:
            if r.get(col) not in CONDITION_STATUSES:
                raise ValueError(f"{r['district_id']}: invalid {col}={r.get(col)}")
        if (r.get("infant_mortality_denominator") or "") not in VALID_DENOMINATORS:
            raise ValueError(f"{r['district_id']}: invalid denominator={r.get('infant_mortality_denominator')}")
        if r.get("verification_status") not in VALID_VERIFICATION:
            raise ValueError(f"{r['district_id']}: invalid verification_status={r.get('verification_status')}")


def enrich_mortality_fields(row: dict) -> dict:
    r = dict(row)
    denom = r.get("infant_mortality_denominator") or ""
    pct = r.get("infant_mortality_pct")
    did = r["district_id"]
    if pct is not None and denom in ("live_births", "total_births_incl_stillborn"):
        r["imr_pct_of_births"] = float(pct)
        r["infant_share_of_all_deaths_pct"] = None
        r["numerator_includes_stillbirths"] = did in STILLBIRTH_IN_NUMERATOR_IDS
        r["is_approximate"] = did in APPROXIMATE_MORTALITY_IDS
        r["age_window"] = SPECIAL_AGE_WINDOWS.get(did, "0_to_12_months")
    elif pct is not None and denom == "all_deaths":
        r["imr_pct_of_births"] = None
        r["infant_share_of_all_deaths_pct"] = float(pct)
        r["numerator_includes_stillbirths"] = False
        r["is_approximate"] = False
        r["age_window"] = "0_to_12_months"
    else:
        r["imr_pct_of_births"] = None
        r["infant_share_of_all_deaths_pct"] = None
        r["numerator_includes_stillbirths"] = ""
        r["is_approximate"] = ""
        r["age_window"] = ""
    return r


def main() -> int:
    raw_rows: list[dict] = []
    for spath in sorted(DISTRICT_SHARDS_DIR.glob("shard_*.json")):
        raw_rows.extend(json.loads(spath.read_text(encoding="utf-8")))
    raw_rows.sort(key=lambda r: r["district_id"])
    validate_district_rows(raw_rows)
    district_rows = [enrich_mortality_fields(r) for r in raw_rows]

    folk_rows: list[dict] = []
    seen_folk: set[tuple[str, int]] = set()
    for fpath in sorted(FOLK_SHARDS_DIR.glob("folk_*.json")):
        for item in json.loads(fpath.read_text(encoding="utf-8")):
            key = (str(item.get("bsb_id", "")), int(item.get("canvas_number") or 0))
            if key not in seen_folk:
                seen_folk.add(key)
                folk_rows.append(item)
    folk_substantive = [r for r in folk_rows if r.get("is_substantive_folk_practice")]
    folk_substantive.sort(key=lambda r: (-int(r.get("vividness_score") or 0), r["district_id"]))

    # 1. Write verified_bavaria_1860_infant_feeding.csv
    infant_fields = [
        "district_id",
        "district_name",
        "regierungsbezirk",
        "jurisdiction_type",
        "latitude",
        "longitude",
        "bsb_ids",
        "volume_numbers",
        "infant_feeding_documented",
        "breastfeeding_status",
        "mehlbrei_gruel_status",
        "pacifier_status",
        "poppy_opiate_sedative",
        "alcohol_to_infants",
        "imr_pct_of_births",
        "infant_share_of_all_deaths_pct",
        "infant_mortality_denominator",
        "numerator_includes_stillbirths",
        "is_approximate",
        "age_window",
        "infant_mortality_detail",
        "goiter_status",
        "cretinism_status",
        "primary_bsb_id",
        "primary_canvas",
        "mdz_page_url",
        "iiif_image_url",
        "verified_german_quote",
        "english_translation",
        "ocr_corrections_noted",
        "verification_status",
    ]
    out_inf_csv = DATASET_DIR / "verified_bavaria_1860_infant_feeding.csv"
    with out_inf_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=infant_fields, extrasaction="ignore")
        w.writeheader()
        for r in district_rows:
            w.writerow(r)

    # 2. Write verified_bavaria_1860_folk_medicine.csv
    folk_fields = [
        "district_id",
        "district_name",
        "regierungsbezirk",
        "latitude",
        "longitude",
        "bsb_id",
        "volume_number",
        "canvas_number",
        "primary_category",
        "vividness_score",
        "practices_summary",
        "verified_german_quote",
        "english_translation",
        "ocr_corrections_noted",
        "mdz_page_url",
        "iiif_image_url",
        "verification_status",
    ]
    out_folk_csv = DATASET_DIR / "verified_bavaria_1860_folk_medicine.csv"
    with out_folk_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=folk_fields, extrasaction="ignore")
        w.writeheader()
        for r in folk_substantive:
            w.writerow(r)

    # 3. Write normalized verified_passages.csv (all primary + secondary article quotes)
    passage_fields = [
        "passage_id",
        "source_table",
        "district_id",
        "district_name",
        "regierungsbezirk",
        "bsb_id",
        "volume_number",
        "canvas_number",
        "topic",
        "mdz_page_url",
        "iiif_image_url",
        "verified_german_quote",
        "english_translation",
        "ocr_corrections_noted",
        "verification_status",
    ]
    passages: list[dict] = []
    for r in district_rows:
        if r.get("verified_german_quote"):
            passages.append(
                {
                    "passage_id": f"inf_{r['district_id']}_p{r['primary_canvas']}",
                    "source_table": "infant_feeding",
                    "district_id": r["district_id"],
                    "district_name": r["district_name"],
                    "regierungsbezirk": r["regierungsbezirk"],
                    "bsb_id": r["primary_bsb_id"],
                    "volume_number": r["volume_numbers"],
                    "canvas_number": r["primary_canvas"],
                    "topic": "infant_feeding_and_mortality",
                    "mdz_page_url": r["mdz_page_url"],
                    "iiif_image_url": r["iiif_image_url"],
                    "verified_german_quote": r["verified_german_quote"],
                    "english_translation": r["english_translation"],
                    "ocr_corrections_noted": r["ocr_corrections_noted"],
                    "verification_status": r["verification_status"],
                }
            )
    for r in folk_substantive:
        passages.append(
            {
                "passage_id": f"folk_{r['district_id']}_p{r['canvas_number']}",
                "source_table": "folk_medicine",
                "district_id": r["district_id"],
                "district_name": r["district_name"],
                "regierungsbezirk": r["regierungsbezirk"],
                "bsb_id": r["bsb_id"],
                "volume_number": r["volume_number"],
                "canvas_number": r["canvas_number"],
                "topic": r["primary_category"],
                "mdz_page_url": r["mdz_page_url"],
                "iiif_image_url": r["iiif_image_url"],
                "verified_german_quote": r["verified_german_quote"],
                "english_translation": r["english_translation"],
                "ocr_corrections_noted": r["ocr_corrections_noted"],
                "verification_status": r["verification_status"],
            }
        )
    passages.extend(SECONDARY_VERIFIED_PASSAGES)
    with (DATASET_DIR / "verified_passages.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=passage_fields)
        w.writeheader()
        w.writerows(passages)

    # 4. Write GeoJSON (strictly separated mortality properties)
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(r["longitude"]), float(r["latitude"])],
            },
            "properties": {k: r.get(k) for k in infant_fields if k not in ("latitude", "longitude")},
        }
        for r in district_rows
    ]
    (DATASET_DIR / "map_bavaria_1860_infant_feeding.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # 5. Compute aggregate, regional, and sensitivity statistics
    documented = [r for r in district_rows if r["infant_feeding_documented"]]
    by_region: dict[str, dict] = {}
    for reg in sorted({r["regierungsbezirk"] for r in district_rows}):
        sub_all = [r for r in district_rows if r["regierungsbezirk"] == reg]
        sub_doc = [r for r in sub_all if r["infant_feeding_documented"]]
        all_bc = [float(r["imr_pct_of_births"]) for r in sub_all if r["imr_pct_of_births"] is not None]
        live_only = [
            float(r["imr_pct_of_births"])
            for r in sub_all
            if r["imr_pct_of_births"] is not None and r["infant_mortality_denominator"] == "live_births"
        ]
        by_region[reg] = {
            "total_districts": len(sub_all),
            "infant_documented_districts": len(sub_doc),
            "predominantly_breastfed": sum(1 for r in sub_doc if r["breastfeeding_status"] == "predominantly_breastfed"),
            "mixed_or_short_breastfed": sum(1 for r in sub_doc if r["breastfeeding_status"] == "mixed_or_short_duration"),
            "rarely_or_not_breastfed": sum(1 for r in sub_doc if r["breastfeeding_status"] == "rarely_or_not_breastfed"),
            "mehlbrei_predominant": sum(1 for r in sub_doc if r["mehlbrei_gruel_status"] == "predominant_early_diet"),
            "mehlbrei_any": sum(
                1 for r in sub_doc if r["mehlbrei_gruel_status"] in ("predominant_early_diet", "supplemental")
            ),
            "pacifier_used": sum(1 for r in sub_doc if r["pacifier_status"] == "used"),
            "poppy_opiate_used": sum(1 for r in sub_doc if r["poppy_opiate_sedative"] == "documented_used"),
            "alcohol_to_infants_used": sum(1 for r in sub_doc if r["alcohol_to_infants"] == "documented_used"),
            "endemic_goiter": sum(1 for r in sub_all if r["goiter_status"] == "endemic_or_frequent"),
            "endemic_cretinism": sum(1 for r in sub_all if r["cretinism_status"] == "endemic_or_frequent"),
            "n_all_birth_cohort": len(all_bc),
            "median_imr_pct_all_birth_cohort": round(statistics.median(all_bc), 2) if all_bc else None,
            "mean_imr_pct_all_birth_cohort": round(statistics.mean(all_bc), 2) if all_bc else None,
            "n_live_births_only": len(live_only),
            "median_imr_pct_live_births_only": round(statistics.median(live_only), 2) if live_only else None,
        }

    def slice_comparison(rows_subset: list[dict]) -> dict:
        bf = [float(r["imr_pct_of_births"]) for r in rows_subset if r["breastfeeding_status"] == "predominantly_breastfed"]
        non_bf = [
            float(r["imr_pct_of_births"])
            for r in rows_subset
            if r["breastfeeding_status"] in ("mixed_or_short_duration", "rarely_or_not_breastfed")
        ]
        gap = round(statistics.median(non_bf) - statistics.median(bf), 2) if bf and non_bf else None
        return {
            "predominantly_breastfed": group_summary(bf),
            "mixed_or_rarely_breastfed": group_summary(non_bf),
            "median_gap_pp": gap,
            "mann_whitney": mann_whitney_auc(bf, non_bf),
        }

    bc_rows = [r for r in district_rows if r["imr_pct_of_births"] is not None]
    live_rows = [r for r in bc_rows if r["infant_mortality_denominator"] == "live_births"]
    live_exact_rows = [r for r in live_rows if not r["is_approximate"]]
    mf_rows = [r for r in live_rows if r["regierungsbezirk"] == "Mittelfranken"]

    all_bc_vals = [float(r["imr_pct_of_births"]) for r in bc_rows]
    live_vals = [float(r["imr_pct_of_births"]) for r in live_rows]
    stats = {
        "total_canonical_districts": len(district_rows),
        "agent_checked_districts": sum(1 for r in district_rows if r["verification_status"] == "Agent-checked"),
        "no_candidate_section_districts": sum(1 for r in district_rows if r["verification_status"] != "Agent-checked"),
        "infant_feeding_documented_districts": len(documented),
        "breastfeeding_breakdown": {
            "predominantly_breastfed": sum(1 for r in documented if r["breastfeeding_status"] == "predominantly_breastfed"),
            "mixed_or_short_duration": sum(1 for r in documented if r["breastfeeding_status"] == "mixed_or_short_duration"),
            "rarely_or_not_breastfed": sum(1 for r in documented if r["breastfeeding_status"] == "rarely_or_not_breastfed"),
            "feeding_documented_breastfeeding_unstated": sum(
                1 for r in documented if r["breastfeeding_status"] == "not_documented"
            ),
        },
        "mehlbrei_breakdown": {
            "predominant_early_diet": sum(1 for r in documented if r["mehlbrei_gruel_status"] == "predominant_early_diet"),
            "supplemental": sum(1 for r in documented if r["mehlbrei_gruel_status"] == "supplemental"),
            "explicitly_rare_or_absent": sum(
                1 for r in documented if r["mehlbrei_gruel_status"] == "explicitly_rare_or_absent"
            ),
            "not_documented": sum(1 for r in documented if r["mehlbrei_gruel_status"] == "not_documented"),
        },
        "pacifier_used_districts": sum(1 for r in documented if r["pacifier_status"] == "used"),
        "poppy_opiate_used_districts": sum(1 for r in documented if r["poppy_opiate_sedative"] == "documented_used"),
        "alcohol_to_infants_used_districts": sum(1 for r in documented if r["alcohol_to_infants"] == "documented_used"),
        "alcohol_to_children_all_districts": sum(1 for r in district_rows if r["alcohol_to_infants"] == "documented_used"),
        "goiter_breakdown": condition_breakdown(district_rows, "goiter_status"),
        "cretinism_breakdown": condition_breakdown(district_rows, "cretinism_status"),
        "birth_cohort_mortality_districts_all": len(all_bc_vals),
        "birth_cohort_mortality_districts_live_births_only": len(live_vals),
        "all_deaths_share_only_districts": sum(
            1 for r in district_rows if r["infant_share_of_all_deaths_pct"] is not None
        ),
        "median_imr_pct_all_birth_cohort": round(statistics.median(all_bc_vals), 2),
        "median_imr_pct_live_births_only": round(statistics.median(live_vals), 2),
        "mortality_sensitivity": {
            "all_birth_cohort_rates": slice_comparison(bc_rows),
            "strict_live_births_only": slice_comparison(live_rows),
            "strict_live_births_excl_approximate": slice_comparison(live_exact_rows),
            "within_mittelfranken_live_births": slice_comparison(mf_rows),
        },
        "agent_checked_rows_with_logged_ocr_corrections": sum(
            1 for r in district_rows if has_logged_ocr_correction(r)
        ),
        "verified_folk_medicine_passages": len(folk_substantive),
        "verified_passages_total_rows": len(passages),
        "by_regierungsbezirk": by_region,
    }
    (DATASET_DIR / "epidemiology_summary_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 6. Build side-by-side HTML verification viewer
    cards = []
    for r in district_rows:
        if not r.get("verified_german_quote"):
            continue
        preview = (r.get("iiif_image_url") or "").replace("/full/full/", "/full/900,/")
        mort_str = "none"
        if r["imr_pct_of_births"] is not None:
            mort_str = f"{r['imr_pct_of_births']}% ({r['infant_mortality_denominator']})"
        elif r["infant_share_of_all_deaths_pct"] is not None:
            mort_str = f"{r['infant_share_of_all_deaths_pct']}% of all deaths"
        cards.append(
            f"""<article class="card">
  <header>
    <strong>{html.escape(r['district_name'])}</strong>
    <span>{html.escape(r['regierungsbezirk'])} · Bd. {html.escape(str(r['volume_numbers']))} · {html.escape(r['primary_bsb_id'])} scan {r['primary_canvas']}</span>
    <span class="tag">{html.escape(r['breastfeeding_status'])}</span>
    <span class="tag2">Mehlbrei: {html.escape(r['mehlbrei_gruel_status'])}</span>
    <a href="{html.escape(r['mdz_page_url'])}" target="_blank" rel="noopener">MDZ scan</a>
  </header>
  <div class="pair">
    <a href="{html.escape(r['iiif_image_url'])}" target="_blank" rel="noopener">
      <img loading="lazy" src="{html.escape(preview)}" alt="{html.escape(r['district_name'])} scan {r['primary_canvas']}">
    </a>
    <div>
      <blockquote>"{html.escape(r['verified_german_quote'])}"</blockquote>
      <p class="en">{html.escape(r['english_translation'])}</p>
      <p class="meta"><strong>Mortality:</strong> {html.escape(mort_str)} — {html.escape(str(r.get('infant_mortality_detail') or ''))}<br>
      <strong>Poppy/opiate:</strong> {html.escape(r['poppy_opiate_sedative'])} · <strong>Alcohol:</strong> {html.escape(r['alcohol_to_infants'])} · <strong>Goiter:</strong> {html.escape(r['goiter_status'])} · <strong>Cretinism:</strong> {html.escape(r['cretinism_status'])}<br>
      <strong>Verification:</strong> {html.escape(r['verification_status'])} ({html.escape(r.get('ocr_corrections_noted') or '')})</p>
    </div>
  </div>
</article>"""
        )

    viewer_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BSB Cgm 6874 — Agent-Checked District Evidence ({len(cards)} Quoted Pages)</title>
<style>
  body {{ font-family: Charter, Georgia, serif; margin: 2rem auto; max-width: 1280px; padding: 0 1rem; background: #f7f4ee; color: #191919; }}
  h1 {{ font-size: 1.65rem; margin-bottom: 0.4rem; }}
  .card {{ background: #fff; border: 1px solid #d6d0c4; margin-bottom: 1.5rem; padding: 1.1rem; }}
  header {{ display: flex; gap: 0.8rem; flex-wrap: wrap; align-items: baseline; border-bottom: 1px solid #ece8df; padding-bottom: 0.5rem; margin-bottom: 0.9rem; }}
  .tag {{ background: #1d3557; color: #fff; padding: 0.15rem 0.55rem; font-size: 0.82rem; }}
  .tag2 {{ background: #7f4f24; color: #fff; padding: 0.15rem 0.55rem; font-size: 0.82rem; }}
  .pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; align-items: start; }}
  img {{ width: 100%; height: auto; border: 1px solid #ccc; }}
  blockquote {{ margin: 0 0 0.75rem 0; font-style: italic; line-height: 1.5; color: #111; }}
  .en {{ line-height: 1.5; color: #2b2b2b; }}
  .meta {{ font-family: ui-monospace, Menlo, monospace; font-size: 0.82rem; color: #444; background: #f4f1ea; padding: 0.6rem; }}
</style>
</head>
<body>
<h1>BSB Cgm 6874 (1858–1861) — Agent-Checked District Evidence ({len(cards)} districts with verified quotes)</h1>
<p>Every quotation and coded field below was checked by an LLM agent against Bayerische Staatsbibliothek IIIF page images; independent review by a professional historical paleographer is open before publication.</p>
{''.join(cards)}
</body>
</html>
"""
    (DATASET_DIR / "verification_viewer.html").write_text(viewer_html, encoding="utf-8")
    print(json.dumps({k: v for k, v in stats.items() if k != "by_regierungsbezirk"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
