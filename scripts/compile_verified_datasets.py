#!/usr/bin/env python3
"""Compile scan-verified shards into final CSVs, GeoJSON, summary stats, and HTML viewer.

Outputs under `data/dataset/`:
1. `verified_bavaria_1860_infant_feeding.csv`
2. `verified_bavaria_1860_folk_medicine.csv`
3. `map_bavaria_1860_infant_feeding.geojson`
4. `epidemiology_summary_stats.json`
5. `verification_viewer.html`
"""

from __future__ import annotations

import csv
import html
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "data" / "dataset"
DISTRICT_SHARDS_DIR = DATASET_DIR / "verified_shards"
FOLK_SHARDS_DIR = DATASET_DIR / "verified_folk_shards"


def main() -> int:
    district_rows: list[dict] = []
    for spath in sorted(DISTRICT_SHARDS_DIR.glob("shard_*.json")):
        district_rows.extend(json.loads(spath.read_text(encoding="utf-8")))
    district_rows.sort(key=lambda r: r["district_id"])

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
        "infant_mortality_pct",
        "infant_mortality_denominator",
        "infant_mortality_detail",
        "goiter_cretinism_status",
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

    # 3. Write GeoJSON for interactive mapping
    features = []
    for r in district_rows:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(r["longitude"]), float(r["latitude"])],
                },
                "properties": {k: r.get(k) for k in infant_fields if k not in ("latitude", "longitude")},
            }
        )
    geojson = {"type": "FeatureCollection", "features": features}
    (DATASET_DIR / "map_bavaria_1860_infant_feeding.geojson").write_text(
        json.dumps(geojson, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 4. Compute exact aggregate and regional statistics
    documented = [r for r in district_rows if r.get("infant_feeding_documented")]
    by_region: dict[str, dict] = {}
    regions = sorted({r["regierungsbezirk"] for r in district_rows})
    for reg in regions:
        sub_all = [r for r in district_rows if r["regierungsbezirk"] == reg]
        sub_doc = [r for r in sub_all if r.get("infant_feeding_documented")]
        mort_vals = [
            float(r["infant_mortality_pct"])
            for r in sub_all
            if r.get("infant_mortality_pct") is not None
            and r.get("infant_mortality_denominator") in ("live_births", "total_births_incl_stillborn")
            and 5.0 <= float(r["infant_mortality_pct"]) <= 85.0
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
            "endemic_goiter_or_cretinism": sum(
                1 for r in sub_all if r["goiter_cretinism_status"] == "endemic_or_frequent"
            ),
            "explicit_mortality_pct_count": len(mort_vals),
            "median_infant_mortality_pct": round(statistics.median(mort_vals), 1) if mort_vals else None,
            "mean_infant_mortality_pct": round(statistics.mean(mort_vals), 1) if mort_vals else None,
        }

    all_mort = [
        float(r["infant_mortality_pct"])
        for r in district_rows
        if r.get("infant_mortality_pct") is not None
        and r.get("infant_mortality_denominator") in ("live_births", "total_births_incl_stillborn")
        and 5.0 <= float(r["infant_mortality_pct"]) <= 85.0
    ]
    bf_mort_groups = {
        "predominantly_breastfed": [
            float(r["infant_mortality_pct"])
            for r in district_rows
            if r.get("breastfeeding_status") == "predominantly_breastfed"
            and r.get("infant_mortality_pct") is not None
            and r.get("infant_mortality_denominator") in ("live_births", "total_births_incl_stillborn")
            and 5.0 <= float(r["infant_mortality_pct"]) <= 85.0
        ],
        "mixed_or_rarely_breastfed": [
            float(r["infant_mortality_pct"])
            for r in district_rows
            if r.get("breastfeeding_status") in ("mixed_or_short_duration", "rarely_or_not_breastfed")
            and r.get("infant_mortality_pct") is not None
            and r.get("infant_mortality_denominator") in ("live_births", "total_births_incl_stillborn")
            and 5.0 <= float(r["infant_mortality_pct"]) <= 85.0
        ],
    }
    mortality_by_breastfeeding = {
        k: {
            "n": len(v),
            "median_pct": round(statistics.median(v), 1) if v else None,
            "mean_pct": round(statistics.mean(v), 1) if v else None,
            "min_pct": round(min(v), 1) if v else None,
            "max_pct": round(max(v), 1) if v else None,
        }
        for k, v in bf_mort_groups.items()
    }
    stats = {
        "total_canonical_districts": len(district_rows),
        "agent_checked_districts": sum(1 for r in district_rows if r.get("verification_status") == "Agent-checked"),
        "infant_feeding_documented_districts": len(documented),
        "breastfeeding_breakdown": {
            "predominantly_breastfed": sum(1 for r in documented if r["breastfeeding_status"] == "predominantly_breastfed"),
            "mixed_or_short_duration": sum(1 for r in documented if r["breastfeeding_status"] == "mixed_or_short_duration"),
            "rarely_or_not_breastfed": sum(1 for r in documented if r["breastfeeding_status"] == "rarely_or_not_breastfed"),
            "not_documented": sum(1 for r in documented if r["breastfeeding_status"] == "not_documented"),
        },
        "mehlbrei_breakdown": {
            "predominant_early_diet": sum(1 for r in documented if r["mehlbrei_gruel_status"] == "predominant_early_diet"),
            "supplemental": sum(1 for r in documented if r["mehlbrei_gruel_status"] == "supplemental"),
            "explicitly_rare_or_absent": sum(
                1 for r in documented if r["mehlbrei_gruel_status"] == "explicitly_rare_or_absent"
            ),
        },
        "pacifier_used_districts": sum(1 for r in documented if r["pacifier_status"] == "used"),
        "poppy_opiate_used_districts": sum(1 for r in documented if r["poppy_opiate_sedative"] == "documented_used"),
        "poppy_opiate_explicitly_denied_districts": sum(
            1 for r in documented if r["poppy_opiate_sedative"] == "explicitly_denied"
        ),
        "alcohol_to_infants_used_districts": sum(1 for r in documented if r["alcohol_to_infants"] == "documented_used"),
        "endemic_goiter_districts": sum(
            1 for r in district_rows if r["goiter_cretinism_status"] == "endemic_or_frequent"
        ),
        "sporadic_goiter_districts": sum(
            1 for r in district_rows if r["goiter_cretinism_status"] == "sporadic_or_localized"
        ),
        "explicit_mortality_rate_districts": len(all_mort),
        "median_infant_mortality_pct": round(statistics.median(all_mort), 1) if all_mort else None,
        "min_infant_mortality_pct": round(min(all_mort), 1) if all_mort else None,
        "max_infant_mortality_pct": round(max(all_mort), 1) if all_mort else None,
        "mortality_by_breastfeeding_status": mortality_by_breastfeeding,
        "ocr_corrections_made_count": sum(
            1
            for r in district_rows
            if r.get("ocr_corrections_noted")
            and "exact match" not in r["ocr_corrections_noted"].lower()
        ),
        "verified_folk_medicine_passages": len(folk_substantive),
        "by_regierungsbezirk": by_region,
    }
    (DATASET_DIR / "epidemiology_summary_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 5. Build interactive side-by-side HTML verification viewer
    cards = []
    for r in district_rows:
        if not r.get("verified_german_quote"):
            continue
        preview = (r.get("iiif_image_url") or "").replace("/full/full/", "/full/900,/")
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
      <blockquote>“{html.escape(r['verified_german_quote'])}”</blockquote>
      <p class="en">{html.escape(r['english_translation'])}</p>
      <p class="meta"><strong>Mortality:</strong> {html.escape(str(r.get('infant_mortality_detail') or '—'))}<br>
      <strong>Poppy/opiate:</strong> {html.escape(r['poppy_opiate_sedative'])} · <strong>Alcohol:</strong> {html.escape(r['alcohol_to_infants'])} · <strong>Goiter:</strong> {html.escape(r['goiter_cretinism_status'])}<br>
      <strong>Scan check:</strong> {html.escape(r['verification_status'])} ({html.escape(r.get('ocr_corrections_noted') or '')})</p>
    </div>
  </div>
</article>"""
        )

    viewer_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BSB Cgm 6874 — Verified District Dataset ({len(cards)} Quoted Scans)</title>
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
<h1>BSB Cgm 6874 (1858–1861) — Scan-Verified District Evidence ({len(cards)} districts with verified quotes)</h1>
<p>Every quotation and coded field below was checked directly against its IIIF archival scan.</p>
{''.join(cards)}
</body>
</html>
"""
    (DATASET_DIR / "verification_viewer.html").write_text(viewer_html, encoding="utf-8")
    print(json.dumps({k: v for k, v in stats.items() if k != "by_regierungsbezirk"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
