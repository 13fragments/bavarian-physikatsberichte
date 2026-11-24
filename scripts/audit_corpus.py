#!/usr/bin/env python3
"""Audit completeness and quality flags across all 212 BSB Cgm 6874 volume transcripts.

Verifies:
1. Every admitted volume in `data/catalog/volumes.jsonl` has a non-empty `.jsonl.gz` transcript.
2. Every volume's transcribed page count matches its IIIF manifest `canvas_count`.
3. Tallies `incomplete == "repetition"` pages, `runs_removed` pages, empty pages, and token/speed stats.
4. Writes `data/dataset/corpus_audit.json` and exits non-zero if any volume or page is missing.
"""

from __future__ import annotations

from difflib import SequenceMatcher
import gzip
import json
from pathlib import Path
import re
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "data" / "catalog" / "volumes.jsonl"
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
OUT_FILE = ROOT / "data" / "dataset" / "corpus_audit.json"


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def is_duplicate_pair(prev_text: str, curr_text: str) -> tuple[bool, float]:
    a = compact_text(prev_text)
    b = compact_text(curr_text)
    if len(a) < 200 or len(b) < 200:
        return False, 0.0
    if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.25:
        return False, 0.0
    ratio = SequenceMatcher(None, a[:1500], b[:1500]).ratio()
    return ratio >= 0.88, round(ratio, 4)


def main() -> int:
    catalog = [
        json.loads(ln)
        for ln in CATALOG_FILE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    admitted = [r for r in catalog if r.get("admitted")]

    missing_volumes = []
    page_mismatches = []
    incomplete_pages = []
    duplicate_frames = []
    runs_removed_count = 0
    empty_pages = 0
    total_pages = 0
    total_tokens = 0
    durations = []

    for vol in admitted:
        bid = vol["bsb_id"]
        expected = int(vol["canvas_count"])
        path = TRANSCRIPTS_DIR / f"{bid}.jsonl.gz"
        if not path.exists() or path.stat().st_size == 0:
            missing_volumes.append(bid)
            continue
        with gzip.open(path, "rt", encoding="utf-8") as gz:
            pages = [json.loads(ln) for ln in gz if ln.strip()]
        pages.sort(key=lambda x: int(x["canvas_number"]))
        canvas_nums = [int(p["canvas_number"]) for p in pages]
        expected_seq = list(range(1, expected + 1))
        if canvas_nums != expected_seq:
            page_mismatches.append(
                {
                    "bsb_id": bid,
                    "expected": expected,
                    "actual": len(pages),
                    "missing_canvases": sorted(set(expected_seq) - set(canvas_nums))[:20],
                    "duplicate_canvases": len(canvas_nums) - len(set(canvas_nums)),
                }
            )
        prev_page = None
        for p in pages:
            total_pages += 1
            total_tokens += int(p.get("completion_tokens") or 0)
            if p.get("duration_s") is not None:
                durations.append(float(p["duration_s"]))
            if p.get("incomplete"):
                incomplete_pages.append(
                    {
                        "bsb_id": bid,
                        "district": vol["district"],
                        "canvas_number": p["canvas_number"],
                        "incomplete": p["incomplete"],
                        "loop_rule": p.get("loop_rule"),
                    }
                )
            if p.get("runs_removed"):
                runs_removed_count += 1
            if not (p.get("text") or "").strip():
                empty_pages += 1
            if prev_page is not None and int(p["canvas_number"]) == int(prev_page["canvas_number"]) + 1:
                dup, sim = is_duplicate_pair(prev_page.get("text", ""), p.get("text", ""))
                if dup:
                    prev_sha = (prev_page.get("image_step") or {}).get("sent_sha256", "")
                    curr_sha = (p.get("image_step") or {}).get("sent_sha256", "")
                    same_img_hash = bool(prev_sha and curr_sha and prev_sha == curr_sha)
                    duplicate_frames.append(
                        {
                            "bsb_id": bid,
                            "district": vol["district"],
                            "canvas_number": int(p["canvas_number"]),
                            "duplicate_of_canvas": int(prev_page["canvas_number"]),
                            "similarity": sim,
                            "same_image_sha256": same_img_hash,
                            "duplicate_method": "exact_image_hash_and_text" if same_img_hash else "text_near_duplicate",
                        }
                    )
            prev_page = p

    exact_hash_dups = sum(1 for d in duplicate_frames if d["same_image_sha256"])
    text_near_dups = len(duplicate_frames) - exact_hash_dups
    summary = {
        "admitted_volumes": len(admitted),
        "completed_volumes": len(admitted) - len(missing_volumes),
        "missing_volumes": missing_volumes,
        "page_mismatches": page_mismatches,
        "total_pages_transcribed": total_pages,
        "unique_non_duplicate_pages": total_pages - len(duplicate_frames),
        "expected_total_pages": sum(int(v["canvas_count"]) for v in admitted),
        "duplicate_consecutive_frames_count": len(duplicate_frames),
        "duplicate_exact_image_hash_count": exact_hash_dups,
        "duplicate_text_near_match_count": text_near_dups,
        "incomplete_repetition_pages_count": len(incomplete_pages),
        "incomplete_repetition_share": round(len(incomplete_pages) / max(total_pages, 1), 5),
        "runs_removed_pages_count": runs_removed_count,
        "empty_pages_count": empty_pages,
        "total_completion_tokens": total_tokens,
        "median_page_duration_s": round(statistics.median(durations), 3) if durations else None,
        "duplicate_consecutive_frames": duplicate_frames,
        "incomplete_pages": incomplete_pages,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in summary.items() if k not in ("incomplete_pages", "duplicate_consecutive_frames")},
            indent=2,
        )
    )
    return 0 if not missing_volumes and not page_mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
