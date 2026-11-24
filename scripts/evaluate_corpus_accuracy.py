#!/usr/bin/env python3
"""Stratified 30-page in-corpus accuracy evaluation sampler and scorer.

Implements the pre-registered Kurrent Pages Benchmark normalization and alignment
metrics (`cer_dipl`, `cer_norm`, `cer_norm_lc`, `wer_norm`, `nls_norm`) with
10,000-draw nonparametric bootstrap 95% confidence intervals.

Subcommands:
  sample — deterministically select 30 prose pages across 30 distinct volumes
           (seed=18580421) once corpus transcription is complete.
  score  — score verified reference transcriptions in `data/eval_sample/references/`
           against the `re-v1` model outputs and write
           `data/dataset/in_corpus_accuracy_eval.json` and `.csv`.
"""

from __future__ import annotations

import argparse
import csv
from difflib import SequenceMatcher
import gzip
import json
from pathlib import Path
import random
import re
import statistics
import sys
from typing import Sequence
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "data" / "catalog" / "volumes.jsonl"
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
EVAL_DIR = ROOT / "data" / "eval_sample"
REF_DIR = EVAL_DIR / "references"
DATASET_DIR = ROOT / "data" / "dataset"

SEED = 18580421  # Royal Bavarian ministerial rescript date: 21 April 1858

_LIGATURES = {
    "ſ": "s",
    "ꝛ": "r",
    "ﬀ": "ff",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬅ": "st",
    "ﬆ": "st",
}
_LIGATURE_TABLE = str.maketrans(_LIGATURES)
_MARKER_KEYED = re.compile(r"⟪(?P<tag>[MSD]):[ \t]?(?P<body>[^\n⟫]*)⟫")
_MARKER_PREFIX = re.compile(r"⟪(?P<tag>[MSD])⟫[ \t]?")
_PRINT_REGION = re.compile(r"⟪P:[ \t]?(?P<body>.*?)⟫", re.DOTALL)
_MARKER_UNSCORED = re.compile(r"⟪[GZ]⟫")
_CLOSING_MARK = re.compile(r"⟪Z⟫")
_UNCERTAIN = re.compile(r"⟦(?P<body>[^\n⟧]*)⟧")
_HYPHEN_BREAK = re.compile(r"(?:(?<=[^\W\d_])|(?<=[\u0300-\u036f]))[-=⸗]\n")
_STROKE_BREAK = re.compile(r"[-=⸗]\n")


def _collapse_spaces(text: str) -> str:
    return re.sub(r"[ \t\u00a0]+", " ", text).strip()


def strip_markers(text: str) -> str:
    text = _PRINT_REGION.sub("", text)
    text = _MARKER_UNSCORED.sub("", text)
    text = _MARKER_KEYED.sub(lambda m: m.group("body"), text)
    text = _MARKER_PREFIX.sub("", text)
    text = _UNCERTAIN.sub(lambda m: m.group("body"), text)
    lines = [_collapse_spaces(line) for line in text.split("\n")]
    return "\n".join(line for line in lines if line)


def strip_hyp_markers(text: str) -> str:
    text = _PRINT_REGION.sub(lambda m: m.group("body"), text)
    text = _CLOSING_MARK.sub("", text)
    text = _MARKER_KEYED.sub(lambda m: m.group("body"), text)
    text = _MARKER_PREFIX.sub("", text)
    text = _UNCERTAIN.sub(lambda m: m.group("body"), text)
    lines = [_collapse_spaces(line) for line in text.split("\n")]
    return "\n".join(line for line in lines if line and line != "⟪G⟫")


def diplomatic(text: str) -> str:
    return unicodedata.normalize("NFC", strip_markers(text))


def normalize(text: str, lowercase: bool = False) -> str:
    text = strip_markers(text)
    text = text.translate(_LIGATURE_TABLE)
    text = _HYPHEN_BREAK.sub("", text)
    text = _STROKE_BREAK.sub("\n", text)
    text = text.replace("\n", " ")
    text = unicodedata.normalize("NFC", text)
    text = _collapse_spaces(text)
    return text.lower() if lowercase else text


def levenshtein(ref: Sequence, hyp: Sequence) -> int:
    if len(ref) < len(hyp):
        ref, hyp = hyp, ref
    previous = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, start=1):
        current = [i]
        for j, h in enumerate(hyp, start=1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (r != h)))
        previous = current
    return previous[-1]


def cer(ref: str, hyp: str) -> float:
    if not ref:
        return 0.0 if not hyp else 1.0
    return levenshtein(ref, hyp) / len(ref)


def wer(ref_tokens: Sequence[str], hyp_tokens: Sequence[str]) -> float:
    if not ref_tokens:
        return 0.0 if not hyp_tokens else 1.0
    return levenshtein(ref_tokens, hyp_tokens) / len(ref_tokens)


def nls(ref: str, hyp: str) -> float:
    longest = max(len(ref), len(hyp))
    if longest == 0:
        return 1.0
    return 1.0 - levenshtein(ref, hyp) / longest


def bootstrap_ci(values: list[float], stat_fn, draws: int = 10000, seed: int = SEED) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(values)
    stats = sorted(stat_fn([values[rng.randrange(n)] for _ in range(n)]) for _ in range(draws))
    return round(stats[int(0.025 * draws)], 5), round(stats[int(0.975 * draws)], 5)


def is_duplicate_pair(prev_text: str, curr_text: str) -> bool:
    a = re.sub(r"\s+", " ", (prev_text or "").strip().lower())
    b = re.sub(r"\s+", " ", (curr_text or "").strip().lower())
    if len(a) < 200 or len(b) < 200:
        return False
    return SequenceMatcher(None, a[:1500], b[:1500]).ratio() >= 0.88


def cmd_sample(count: int) -> int:
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    REF_DIR.mkdir(parents=True, exist_ok=True)
    catalog = [
        json.loads(ln)
        for ln in CATALOG_FILE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    admitted = sorted([r for r in catalog if r.get("admitted")], key=lambda r: r["bsb_id"])
    rng = random.Random(SEED)

    eligible_per_vol: list[dict] = []
    for vol in admitted:
        bid = vol["bsb_id"]
        tpath = TRANSCRIPTS_DIR / f"{bid}.jsonl.gz"
        if not tpath.exists():
            raise FileNotFoundError(f"Transcript missing for {bid}; complete all 212 volumes before sampling.")
        with gzip.open(tpath, "rt", encoding="utf-8") as gz:
            pages = sorted([json.loads(ln) for ln in gz if ln.strip()], key=lambda p: int(p["canvas_number"]))
        candidates = []
        prev_text = ""
        for p in pages:
            txt = (p.get("text") or "").strip()
            cno = int(p["canvas_number"])
            # Require interior manuscript pages (>= 80 words, <= 450 words, non-duplicate, non-table-heavy)
            words = txt.split()
            digit_share = sum(ch.isdigit() for ch in txt) / max(len(txt), 1)
            if cno > 2 and 80 <= len(words) <= 450 and digit_share < 0.12 and not is_duplicate_pair(prev_text, txt):
                candidates.append(p)
            prev_text = txt
        if candidates:
            chosen = rng.choice(candidates)
            eligible_per_vol.append({"vol": vol, "page": chosen})

    rng.shuffle(eligible_per_vol)
    # Stratified across the volume list by uniform stride after deterministic shuffle
    stride = len(eligible_per_vol) / count
    picked = [eligible_per_vol[int(i * stride)] for i in range(count)]
    picked.sort(key=lambda x: x["vol"]["bsb_id"])

    manifest = []
    for idx, item in enumerate(picked, start=1):
        vol = item["vol"]
        page = item["page"]
        sample_id = f"eval_{idx:02d}_{vol['bsb_id']}_p{int(page['canvas_number']):03d}"
        manifest.append(
            {
                "sample_id": sample_id,
                "bsb_id": vol["bsb_id"],
                "volume_number": vol["volume_number"],
                "district": vol["district"],
                "canvas_number": int(page["canvas_number"]),
                "iiif_image_url": page["iiif_image_url"],
                "mdz_page_url": f"https://www.digitale-sammlungen.de/de/view/{vol['bsb_id']}?page={page['canvas_number']}",
                "image_path": str(EVAL_DIR / "images" / f"{sample_id}.jpg"),
                "reference_path": str(REF_DIR / f"{sample_id}.txt"),
                "model_text": page.get("text", ""),
                "model_raw_text": page.get("raw_text", ""),
                "incomplete": page.get("incomplete"),
            }
        )

    out_path = EVAL_DIR / "sample_manifest.json"
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Also write a blind manifest without model_text for independent image-only reading
    blind = [{k: v for k, v in m.items() if not k.startswith("model_")} for m in manifest]
    (EVAL_DIR / "sample_blind_manifest.json").write_text(
        json.dumps(blind, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Selected {len(manifest)} stratified pages across {len(eligible_per_vol)} eligible volumes -> {out_path}")
    return 0


def cmd_score() -> int:
    manifest_path = EVAL_DIR / "sample_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = []
    total_ref_chars = 0
    total_char_edits = 0
    total_ref_words = 0
    total_word_edits = 0

    for item in manifest:
        ref_path = Path(item["reference_path"])
        if not ref_path.is_absolute():
            ref_path = ROOT / ref_path
        if not ref_path.exists():
            raise FileNotFoundError(f"Missing reference transcription: {ref_path}")
        gold_raw = ref_path.read_text(encoding="utf-8").strip()
        hyp_raw = item["model_text"]

        gold_scored = strip_markers(gold_raw)
        hyp_scored = strip_hyp_markers(hyp_raw)
        gold_norm = normalize(gold_scored)
        hyp_norm = normalize(hyp_scored)

        c_dipl = cer(diplomatic(gold_scored), diplomatic(hyp_scored))
        c_norm = cer(gold_norm, hyp_norm)
        c_norm_lc = cer(gold_norm.lower(), hyp_norm.lower())
        w_norm = wer(gold_norm.split(), hyp_norm.split())
        n_norm = nls(gold_norm, hyp_norm)

        char_edits = levenshtein(gold_norm, hyp_norm)
        word_edits = levenshtein(gold_norm.split(), hyp_norm.split())
        total_ref_chars += len(gold_norm)
        total_char_edits += char_edits
        total_ref_words += len(gold_norm.split())
        total_word_edits += word_edits

        rows.append(
            {
                "sample_id": item["sample_id"],
                "bsb_id": item["bsb_id"],
                "volume_number": item["volume_number"],
                "district": item["district"],
                "canvas_number": item["canvas_number"],
                "ref_chars": len(gold_norm),
                "hyp_chars": len(hyp_norm),
                "ref_words": len(gold_norm.split()),
                "cer_dipl": round(c_dipl, 5),
                "cer_norm": round(c_norm, 5),
                "cer_norm_lc": round(c_norm_lc, 5),
                "wer_norm": round(w_norm, 5),
                "nls_norm": round(n_norm, 5),
                "incomplete": item.get("incomplete"),
                "mdz_page_url": item["mdz_page_url"],
            }
        )

    cer_vals = [r["cer_norm"] for r in rows]
    wer_vals = [r["wer_norm"] for r in rows]
    cer_dipl_vals = [r["cer_dipl"] for r in rows]
    nls_vals = [r["nls_norm"] for r in rows]

    summary = {
        "protocol": "Kurrent Pages Benchmark §4-§5 normalization & alignment",
        "seed": SEED,
        "pages_evaluated": len(rows),
        "distinct_volumes": len({r["bsb_id"] for r in rows}),
        "verifier_note": "Independent agent image transcription checked word-for-word against IIIF scans; human paleographer check open.",
        "total_reference_chars": total_ref_chars,
        "total_reference_words": total_ref_words,
        "median_cer_norm": round(statistics.median(cer_vals), 5),
        "median_cer_norm_ci95": bootstrap_ci(cer_vals, statistics.median),
        "mean_cer_norm": round(statistics.mean(cer_vals), 5),
        "mean_cer_norm_ci95": bootstrap_ci(cer_vals, statistics.mean),
        "micro_cer_norm": round(total_char_edits / max(total_ref_chars, 1), 5),
        "median_cer_dipl": round(statistics.median(cer_dipl_vals), 5),
        "median_wer_norm": round(statistics.median(wer_vals), 5),
        "median_wer_norm_ci95": bootstrap_ci(wer_vals, statistics.median),
        "mean_wer_norm": round(statistics.mean(wer_vals), 5),
        "micro_wer_norm": round(total_word_edits / max(total_ref_words, 1), 5),
        "mean_nls_norm": round(statistics.mean(nls_vals), 5),
        "per_page": rows,
    }

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    out_json = DATASET_DIR / "in_corpus_accuracy_eval.json"
    out_csv = DATASET_DIR / "in_corpus_accuracy_eval.csv"
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({k: v for k, v in summary.items() if k != "per_page"}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_sample = sub.add_parser("sample")
    p_sample.add_argument("--count", type=int, default=30)
    sub.add_parser("score")
    args = parser.parse_args()
    if args.cmd == "sample":
        return cmd_sample(args.count)
    return cmd_score()


if __name__ == "__main__":
    sys.exit(main())
