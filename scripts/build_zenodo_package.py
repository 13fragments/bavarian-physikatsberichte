#!/usr/bin/env python3
"""Assemble the local Zenodo / Hugging Face companion dataset bundle under `dist/zenodo_package/`.

Does NOT upload anything externally. Stages:
1. `cgm6874_volumes.csv` — 212-volume catalog with page counts and `PDM 1.0` IIIF links.
2. `cgm6874_pages.jsonl.gz` — all 26,325 transcribed pages in deterministic volume/canvas order.
3. Copies verified district `CSV` tables and `DATACARD.md` if present, then computes `SHA256SUMS`.
"""

from __future__ import annotations

import csv
from difflib import SequenceMatcher
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "data" / "catalog" / "volumes.jsonl"
CATALOG_CSV = ROOT / "data" / "catalog" / "volumes.csv"
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
DATASET_DIR = ROOT / "data" / "dataset"
DIST_DIR = ROOT / "dist" / "zenodo_package"


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def is_duplicate_pair(prev_text: str, curr_text: str) -> bool:
    a = compact_text(prev_text)
    b = compact_text(curr_text)
    if len(a) < 200 or len(b) < 200:
        return False
    if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.25:
        return False
    return SequenceMatcher(None, a[:1500], b[:1500]).ratio() >= 0.88


def sort_key(rec: dict) -> tuple[int, str, str]:
    m = re.match(r"(\d+)", rec.get("volume_number") or "")
    return (int(m.group(1)) if m else 9999, rec.get("volume_number") or "", rec["bsb_id"])


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    catalog = [
        json.loads(ln)
        for ln in CATALOG_FILE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    admitted = sorted([r for r in catalog if r.get("admitted")], key=sort_key)

    shutil.copy2(CATALOG_CSV, DIST_DIR / "cgm6874_volumes.csv")

    pages_out = DIST_DIR / "cgm6874_pages.jsonl.gz"
    total_pages = 0
    with gzip.open(pages_out, "wt", encoding="utf-8") as out_gz:
        for vol in admitted:
            bid = vol["bsb_id"]
            src = TRANSCRIPTS_DIR / f"{bid}.jsonl.gz"
            if not src.exists():
                raise FileNotFoundError(f"Missing volume transcript: {src}")
            with gzip.open(src, "rt", encoding="utf-8") as in_gz:
                pages = [json.loads(ln) for ln in in_gz if ln.strip()]
            pages.sort(key=lambda p: int(p["canvas_number"]))
            prev_page = None
            for p in pages:
                dup_of = None
                if prev_page is not None and int(p["canvas_number"]) == int(prev_page["canvas_number"]) + 1:
                    if is_duplicate_pair(prev_page.get("text", ""), p.get("text", "")):
                        dup_of = int(prev_page["canvas_number"])
                row = {
                    "bsb_id": bid,
                    "volume_number": vol["volume_number"],
                    "district": vol["district"],
                    "canvas_number": p["canvas_number"],
                    "canvas_label": p.get("canvas_label", ""),
                    "iiif_image_url": p["iiif_image_url"],
                    "mdz_page_url": f"https://www.digitale-sammlungen.de/de/view/{bid}?page={p['canvas_number']}",
                    "width": p.get("width", 0),
                    "height": p.get("height", 0),
                    "text": p.get("text", ""),
                    "raw_text": p.get("raw_text", ""),
                    "duplicate_of_canvas": dup_of,
                    "incomplete": p.get("incomplete"),
                    "loop_rule": p.get("loop_rule"),
                    "runs_removed": p.get("runs_removed", False),
                    "completion_tokens": p.get("completion_tokens", 0),
                    "sent_sha256": (p.get("image_step") or {}).get("sent_sha256", ""),
                    "painted_share": (p.get("image_step") or {}).get("painted_share", 0.0),
                }
                out_gz.write(json.dumps(row, ensure_ascii=False) + "\n")
                total_pages += 1
                prev_page = p

    for extra_csv in sorted(DATASET_DIR.glob("verified_*.csv")):
        shutil.copy2(extra_csv, DIST_DIR / extra_csv.name)
    for extra_name in (
        "districts_index.csv",
        "in_corpus_accuracy_eval.csv",
        "map_bavaria_1860_infant_feeding.geojson",
    ):
        extra_path = DATASET_DIR / extra_name
        if extra_path.exists():
            shutil.copy2(extra_path, DIST_DIR / extra_name)

    sums_lines = []
    for artifact in sorted(DIST_DIR.iterdir()):
        if artifact.is_file() and artifact.name != "SHA256SUMS":
            sums_lines.append(f"{sha256_file(artifact)}  {artifact.name}")
    (DIST_DIR / "SHA256SUMS").write_text("\n".join(sums_lines) + "\n", encoding="utf-8")

    print(f"Packaged {len(admitted)} volumes ({total_pages} pages) into {DIST_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
