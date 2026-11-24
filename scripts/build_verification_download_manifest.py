#!/usr/bin/env python3
"""Build a deduplicated IIIF download manifest for Stage 2 & Stage 3 scan checks.

Collects:
1. All 30 stratified evaluation pages (`full/full` native resolution JPEGs).
2. Top 2 infant-feeding candidate scans + top 1 goiter scan + top 1 mortality-table
   scan for every canonical Bavarian district (`full/1400,` high-legibility JPEGs).
3. Top 60 highest-scoring folk-medicine / superstition scans across distinct districts
   (`full/1400,` JPEGs) so the folk-medicine verification pool has wide regional coverage.

Writes:
- `data/dataset/iiif_download_manifest.json`
- `data/dataset/folk_medicine_top_candidates.json`
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EVAL_MANIFEST = ROOT / "data" / "eval_sample" / "sample_manifest.json"
CANDIDATES_FILE = ROOT / "data" / "dataset" / "district_epidemiology_candidates.json"
SCANS_DIR = ROOT / "data" / "verification_scans"
DATASET_DIR = ROOT / "data" / "dataset"


def scaled_iiif(url: str, width: int = 1400) -> str:
    return url.replace("/full/full/", f"/full/{width},/")


def scan_dest(bsb_id: str, canvas_number: int) -> Path:
    return SCANS_DIR / f"{bsb_id}_p{int(canvas_number):03d}.jpg"


def main() -> int:
    SCANS_DIR.mkdir(parents=True, exist_ok=True)
    downloads: dict[str, dict] = {}

    if EVAL_MANIFEST.exists():
        eval_items = json.loads(EVAL_MANIFEST.read_text(encoding="utf-8"))
        for item in eval_items:
            dest = item["image_path"]
            downloads[dest] = {"url": item["iiif_image_url"], "dest": dest}

    districts = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))
    folk_pool = []

    for d in districts:
        for hit in d["infant_feeding_candidates"][:2]:
            dest = str(scan_dest(hit["bsb_id"], hit["canvas_number"]))
            hit["local_scan_path"] = dest
            downloads[dest] = {"url": scaled_iiif(hit["iiif_image_url"], 1400), "dest": dest}

        for hit in d["goiter_cretinism_candidates"][:1]:
            dest = str(scan_dest(hit["bsb_id"], hit["canvas_number"]))
            hit["local_scan_path"] = dest
            downloads[dest] = {"url": scaled_iiif(hit["iiif_image_url"], 1400), "dest": dest}

        for hit in d["mortality_table_candidates"][:1]:
            dest = str(scan_dest(hit["bsb_id"], hit["canvas_number"]))
            hit["local_scan_path"] = dest
            downloads[dest] = {"url": scaled_iiif(hit["iiif_image_url"], 1400), "dest": dest}

        if d["folk_medicine_candidates"]:
            best_folk = dict(d["folk_medicine_candidates"][0])
            best_folk["district_id"] = d["district_id"]
            best_folk["district_name"] = d["district_name"]
            best_folk["regierungsbezirk"] = d["regierungsbezirk"]
            best_folk["latitude"] = d["latitude"]
            best_folk["longitude"] = d["longitude"]
            folk_pool.append(best_folk)

    # Also ensure Regen arsenic scan (bsb00146473 p.70) and Roggenburg (bsb00007355 p.15, p.27) are included
    folk_pool.sort(key=lambda x: (-x["score"], x["district_id"]))
    top_folk = folk_pool[:60]
    for fhit in top_folk:
        dest = str(scan_dest(fhit["bsb_id"], fhit["canvas_number"]))
        fhit["local_scan_path"] = dest
        downloads[dest] = {"url": scaled_iiif(fhit["iiif_image_url"], 1400), "dest": dest}

    # Save enriched candidates with `local_scan_path`
    CANDIDATES_FILE.write_text(json.dumps(districts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATASET_DIR / "folk_medicine_top_candidates.json").write_text(
        json.dumps(top_folk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    manifest_list = sorted(downloads.values(), key=lambda x: x["dest"])
    out_manifest = DATASET_DIR / "iiif_download_manifest.json"
    out_manifest.write_text(json.dumps(manifest_list, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(manifest_list)} unique IIIF scan targets -> {out_manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
