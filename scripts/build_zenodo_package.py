#!/usr/bin/env python3
"""Assemble a reproducible local Zenodo / Hugging Face companion dataset bundle.

Does NOT upload anything externally. Builds into a clean staging directory from a strict
required allowlist (failing if any artifact is missing), writes deterministic archives
(`mtime=0`), atomically replaces `dist/zenodo_package/`, and writes `SHA256SUMS`.
"""

from __future__ import annotations

from difflib import SequenceMatcher
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "data" / "catalog" / "volumes.jsonl"
CATALOG_CSV = ROOT / "data" / "catalog" / "volumes.csv"
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
DATASET_DIR = ROOT / "data" / "dataset"
EVAL_DIR = ROOT / "data" / "eval_sample"
DIST_DIR = ROOT / "dist" / "zenodo_package"
STAGING_DIR = ROOT / "dist" / ".zenodo_package_staging"

REQUIRED_DATASET_FILES = (
    "corpus_audit.json",
    "districts_index.csv",
    "epidemiology_summary_stats.json",
    "in_corpus_accuracy_eval.csv",
    "in_corpus_accuracy_eval.json",
    "map_bavaria_1860_infant_feeding.geojson",
    "verified_bavaria_1860_folk_medicine.csv",
    "verified_bavaria_1860_infant_feeding.csv",
    "verified_passages.csv",
)

REQUIRED_ROOT_FILES = (
    "DATACARD.md",
    "LICENSE-CODE.txt",
    "LICENSE-DATA.txt",
    "CITATION.cff",
)


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


def write_deterministic_eval_tarball(dest_path: Path) -> None:
    """Bundle 30-page eval references, blind keyings, and manifest with deterministic mtime=0."""
    files_to_pack: list[tuple[Path, str]] = []
    for name in ("sample_manifest.json", "sample_blind_manifest.json"):
        p = EVAL_DIR / name
        if not p.exists():
            raise FileNotFoundError(f"Missing required eval manifest: {p}")
        files_to_pack.append((p, f"eval_sample/{name}"))
    for subdir in ("blind_keying", "references"):
        d = EVAL_DIR / subdir
        txts = sorted(d.glob("*.txt"))
        if len(txts) != 30:
            raise FileNotFoundError(f"Expected 30 eval texts in {d}, found {len(txts)}")
        for p in txts:
            files_to_pack.append((p, f"eval_sample/{subdir}/{p.name}"))

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        for src, arcname in files_to_pack:
            data = src.read_bytes()
            ti = tarfile.TarInfo(name=arcname)
            ti.size = len(data)
            ti.mtime = 0
            ti.mode = 0o644
            ti.uid = 0
            ti.gid = 0
            ti.uname = ""
            ti.gname = ""
            tf.addfile(ti, io.BytesIO(data))
    with dest_path.open("wb") as raw_out:
        with gzip.GzipFile(filename="eval_sample_references.tar", mode="wb", fileobj=raw_out, mtime=0) as gz:
            gz.write(buf.getvalue())


def main() -> int:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    catalog = [
        json.loads(ln)
        for ln in CATALOG_FILE.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    admitted = sorted([r for r in catalog if r.get("admitted")], key=sort_key)

    shutil.copy2(CATALOG_CSV, STAGING_DIR / "cgm6874_volumes.csv")

    for name in REQUIRED_DATASET_FILES:
        src = DATASET_DIR / name
        if not src.exists():
            raise FileNotFoundError(f"Missing required dataset artifact: {src}")
        shutil.copy2(src, STAGING_DIR / name)

    for name in REQUIRED_ROOT_FILES:
        src = ROOT / name
        if not src.exists():
            raise FileNotFoundError(f"Missing required root metadata artifact: {src}")
        shutil.copy2(src, STAGING_DIR / name)

    write_deterministic_eval_tarball(STAGING_DIR / "eval_sample_references.tar.gz")

    pages_out = STAGING_DIR / "cgm6874_pages.jsonl.gz"
    total_pages = 0
    with pages_out.open("wb") as raw_out:
        with gzip.GzipFile(filename="cgm6874_pages.jsonl", mode="wb", fileobj=raw_out, mtime=0) as gz_bin:
            with io.TextIOWrapper(gz_bin, encoding="utf-8", newline="\n") as out_txt:
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
                        same_img_hash = False
                        if prev_page is not None and int(p["canvas_number"]) == int(prev_page["canvas_number"]) + 1:
                            if is_duplicate_pair(prev_page.get("text", ""), p.get("text", "")):
                                dup_of = int(prev_page["canvas_number"])
                                prev_sha = (prev_page.get("image_step") or {}).get("sent_sha256", "")
                                curr_sha = (p.get("image_step") or {}).get("sent_sha256", "")
                                same_img_hash = bool(prev_sha and curr_sha and prev_sha == curr_sha)
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
                            "duplicate_same_image_sha256": same_img_hash if dup_of is not None else None,
                            "incomplete": p.get("incomplete"),
                            "loop_rule": p.get("loop_rule"),
                            "runs_removed": p.get("runs_removed", False),
                            "completion_tokens": p.get("completion_tokens", 0),
                            "sent_sha256": (p.get("image_step") or {}).get("sent_sha256", ""),
                            "painted_share": (p.get("image_step") or {}).get("painted_share", 0.0),
                        }
                        out_txt.write(json.dumps(row, ensure_ascii=False) + "\n")
                        total_pages += 1
                        prev_page = p

    sums_lines = [
        f"{sha256_file(artifact)}  {artifact.name}"
        for artifact in sorted(STAGING_DIR.iterdir())
        if artifact.is_file() and artifact.name != "SHA256SUMS"
    ]
    (STAGING_DIR / "SHA256SUMS").write_text("\n".join(sums_lines) + "\n", encoding="utf-8")

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    STAGING_DIR.rename(DIST_DIR)
    print(f"Packaged {len(admitted)} volumes ({total_pages} pages, {len(sums_lines)} files) into {DIST_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
