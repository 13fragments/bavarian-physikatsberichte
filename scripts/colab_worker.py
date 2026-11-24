#!/usr/bin/env python3
"""Remote Google Colab GPU worker for BSB Cgm 6874 transcription.

Bootstraps isolated Python 3.11 `serve` and `client` virtual environments via `uv`
to match the exact tested `13fragments/kurrent-transcriber-1b` release stack
(`vllm==0.23.0`, `transformers==5.13.0`, `pillow==12.3.0`, `numpy==2.4.6`), even when
the host Colab runtime uses Python 3.13.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
import gzip
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

MODEL_REPO = "13fragments/kurrent-transcriber-1b"
MODEL_DIR = Path("/content/kurrent-transcriber-1b")
SERVE_VENV = Path("/content/serve")
CLIENT_VENV = Path("/content/client")
OUT_DIR = Path("/content/transcripts")
SCRATCH_ROOT = Path("/tmp/cgm6874_scans")
SERVER_URL = "http://127.0.0.1:8000/v1"
HEALTH_URL = "http://127.0.0.1:8000/health"
SERVED_MODEL_NAME = "kurrent-transcriber-1b"
USER_AGENT = "13fragments-htr/1.0 (historical public-health corpus research; IIIF fetch)"


def run_checked(cmd: list[str]) -> None:
    print(f"[worker] $ {' '.join(cmd)}", flush=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        print(line, end="", flush=True)
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"command failed ({rc}): {' '.join(cmd)}")


def bootstrap_envs_and_reexec() -> None:
    """If not running inside `/content/client/bin/python`, create Python 3.11 venvs via `uv` and re-exec."""
    client_py = CLIENT_VENV / "bin" / "python"
    serve_py = SERVE_VENV / "bin" / "python"
    if Path(sys.executable).resolve() == client_py.resolve() if client_py.exists() else False:
        return

    uv_bin = shutil.which("uv") or "/usr/local/bin/uv"
    if not (MODEL_DIR / "model.safetensors").exists():
        run_checked([uv_bin, "pip", "install", "--system", "-q", "huggingface_hub"])
        run_checked(
            [
                sys.executable,
                "-c",
                f"from huggingface_hub import snapshot_download; snapshot_download({MODEL_REPO!r}, local_dir={str(MODEL_DIR)!r})",
            ]
        )

    if not (SERVE_VENV / "bin" / "vllm").exists():
        run_checked([uv_bin, "venv", "--python", "3.11", str(SERVE_VENV)])
        run_checked(
            [
                uv_bin,
                "pip",
                "install",
                "--python",
                str(serve_py),
                "-r",
                str(MODEL_DIR / "inference" / "server" / "requirements.txt"),
            ]
        )

    if not (CLIENT_VENV / "bin" / "kurrent-transcribe").exists():
        run_checked([uv_bin, "venv", "--python", "3.11", str(CLIENT_VENV)])
        run_checked(
            [
                uv_bin,
                "pip",
                "install",
                "--python",
                str(client_py),
                str(MODEL_DIR / "inference"),
            ]
        )

    run_checked([str(client_py), str(Path(__file__).resolve()), *sys.argv[1:]])
    sys.exit(0)


def fetch_bytes(url: str, timeout: int = 120, attempts: int = 5) -> bytes:
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code in (400, 401, 403, 404, 410) or attempt == attempts:
                raise RuntimeError(f"{url}: HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            if attempt == attempts:
                raise RuntimeError(f"{url}: {exc}") from exc
        time.sleep(3 * attempt)
    raise AssertionError("unreachable")


def verify_pdm_manifest(manifest: dict, bsb_id: str) -> None:
    lic = json.dumps(manifest.get("license", ""), ensure_ascii=False).lower()
    if "creativecommons.org/publicdomain/mark/1.0" not in lic:
        raise ValueError(f"{bsb_id}: rejected non-PDM license field: {lic}")
    restricted = ("by-nc", "by-nd", "rightsstatements.org", "in copyright", "all rights reserved")
    blob = json.dumps(
        [manifest.get("license"), manifest.get("rights"), manifest.get("attribution")],
        ensure_ascii=False,
    ).lower()
    for term in restricted:
        if term in blob:
            raise ValueError(f"{bsb_id}: rejected restricted rights term '{term}'")


def server_healthy() -> bool:
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


def ensure_server() -> None:
    if server_healthy():
        print("[worker] vLLM server already healthy on :8000", flush=True)
        return

    log_path = Path("/content/vllm_server.log")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(MODEL_DIR / "inference" / "server")
    env["VLLM_USE_FLASHINFER_SAMPLER"] = "0"
    cmd = [
        str(SERVE_VENV / "bin" / "vllm"),
        "serve",
        str(MODEL_DIR),
        "--served-model-name",
        SERVED_MODEL_NAME,
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--max-model-len",
        "16384",
        "--dtype",
        "bfloat16",
        "--limit-mm-per-prompt",
        '{"image":1}',
        "--logits-processors",
        "windowed_repetition_penalty:WindowedRepetitionPenalty",
    ]
    print("[worker] starting vLLM server (Python 3.11 serve venv)...", flush=True)
    log_file = log_path.open("wb")
    proc = subprocess.Popen(
        cmd,
        cwd=str(MODEL_DIR),
        env=env,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    deadline = time.monotonic() + 480.0
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
            raise RuntimeError(f"vLLM exited early ({proc.returncode}):\n{tail}")
        if server_healthy():
            print("[worker] vLLM server ready on :8000.", flush=True)
            return
        time.sleep(2.0)
    proc.kill()
    tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
    raise RuntimeError(f"vLLM timed out after 480s:\n{tail}")


def ethnography_start_index(manifest: dict) -> int:
    canvases = manifest.get("sequences", [{}])[0].get("canvases", [])
    id_to_idx = {c.get("@id"): idx for idx, c in enumerate(canvases)}
    for struct in manifest.get("structures", []):
        label = json.dumps(struct.get("label", ""), ensure_ascii=False).lower()
        if "ethnograph" in label:
            sc = struct.get("canvases") or []
            if sc and sc[0] in id_to_idx:
                return id_to_idx[sc[0]]
    return 0


def process_volume(
    bsb_id: str,
    scope: str,
    download_workers: int,
    infer_workers: int,
    transcribe_fn,
) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / f"{bsb_id}.jsonl.gz"
    if out_file.exists() and out_file.stat().st_size > 0:
        return {"bsb_id": bsb_id, "status": "cached", "path": str(out_file)}

    manifest_url = f"https://api.digitale-sammlungen.de/iiif/presentation/v2/{bsb_id}/manifest"
    manifest = json.loads(fetch_bytes(manifest_url).decode("utf-8"))
    verify_pdm_manifest(manifest, bsb_id)

    canvases = manifest.get("sequences", [{}])[0].get("canvases", [])
    start_idx = ethnography_start_index(manifest) if scope == "ethnography" else 0
    selected = list(enumerate(canvases))[start_idx:]

    vol_dir = SCRATCH_ROOT / bsb_id
    if vol_dir.exists():
        shutil.rmtree(vol_dir)
    vol_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.monotonic()
    try:
        def dl_one(item: tuple[int, dict]) -> tuple[int, Path, str, str, int, int]:
            idx, canvas = item
            seq = idx + 1
            res = canvas["images"][0]["resource"]
            svc = (res.get("service") or {}).get("@id")
            img_url = f"{svc}/full/full/0/default.jpg" if svc else res["@id"]
            dest = vol_dir / f"{bsb_id}_{seq:04d}.jpg"
            dest.write_bytes(fetch_bytes(img_url))
            return (
                seq,
                dest,
                str(canvas.get("label") or ""),
                img_url,
                int(canvas.get("width") or 0),
                int(canvas.get("height") or 0),
            )

        def infer_one(entry: tuple[int, Path, str, str, int, int]) -> dict:
            seq, img_path, clabel, img_url, width, height = entry
            res = transcribe_fn(img_path, SERVER_URL, SERVED_MODEL_NAME, timeout=600.0)
            rec = asdict(res)
            rec["bsb_id"] = bsb_id
            rec["canvas_number"] = seq
            rec["canvas_label"] = clabel
            rec["iiif_image_url"] = img_url
            rec["width"] = width
            rec["height"] = height
            rec["volume_label"] = manifest.get("label", "")
            return rec

        records = []
        with (
            ThreadPoolExecutor(max_workers=download_workers) as dl_pool,
            ThreadPoolExecutor(max_workers=infer_workers) as infer_pool,
        ):
            dl_futures = [dl_pool.submit(dl_one, item) for item in selected]
            infer_futures = [infer_pool.submit(infer_one, fut.result()) for fut in as_completed(dl_futures)]
            for ifut in as_completed(infer_futures):
                records.append(ifut.result())
        records.sort(key=lambda r: r["canvas_number"])

        tmp_file = OUT_DIR / f".{bsb_id}.jsonl.gz.tmp"
        with gzip.open(tmp_file, "wt", encoding="utf-8") as gz:
            for rec in records:
                gz.write(json.dumps(rec, ensure_ascii=False) + "\n")
        os.replace(tmp_file, out_file)

        elapsed = round(time.monotonic() - t0, 2)
        incomplete_count = sum(1 for r in records if r.get("incomplete"))
        return {
            "bsb_id": bsb_id,
            "status": "done",
            "pages": len(records),
            "incomplete_pages": incomplete_count,
            "seconds": elapsed,
            "pages_per_min": round(len(records) * 60.0 / max(elapsed, 0.01), 1),
            "path": str(out_file),
        }
    finally:
        shutil.rmtree(vol_dir, ignore_errors=True)


def main() -> int:
    bootstrap_envs_and_reexec()

    parser = argparse.ArgumentParser()
    parser.add_argument("--volumes", nargs="+", required=True, help="BSB IDs to process")
    parser.add_argument("--scope", choices=("full", "ethnography"), default="full")
    parser.add_argument("--download-workers", type=int, default=8)
    parser.add_argument("--infer-workers", type=int, default=8)
    args = parser.parse_args()
    from kurrent_transcribe.pipeline import transcribe

    for bsb_id in args.volumes:
        if not re.fullmatch(r"bsb\d{8}", bsb_id):
            raise ValueError(f"invalid bsb_id: {bsb_id}")
        try:
            ensure_server()
            summary = process_volume(
                bsb_id=bsb_id,
                scope=args.scope,
                download_workers=args.download_workers,
                infer_workers=args.infer_workers,
                transcribe_fn=transcribe,
            )
            print(json.dumps(summary, ensure_ascii=False), flush=True)
        except Exception as exc:
            err_rec = {"bsb_id": bsb_id, "status": "error", "error": str(exc)}
            print(json.dumps(err_rec, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
