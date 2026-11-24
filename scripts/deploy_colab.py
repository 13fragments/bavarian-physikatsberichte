#!/usr/bin/env python3
"""Local autonomous Google Colab orchestrator for BSB Cgm 6874 transcription.

Features:
1. Provisions `A100` (falling back to `L4`) or attaches to an existing warm session (`--reuse-session`).
2. Harvests the BSB Cgm 6874 catalog if not yet cached locally.
3. Dispatches pending volumes in chunks, downloading each completed `<bsb_id>.jsonl.gz`
   immediately to `data/transcripts/`.
4. Self-heals up to `--max-recoveries` times if Google Colab preempts or recycles the VM mid-run.
5. Releases the Colab VM (`colab stop`) in `finally:` unless `--keep-session` is set.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "data" / "catalog"
CATALOG_FILE = CATALOG_DIR / "volumes.jsonl"
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
HARVEST_SCRIPT = ROOT / "scripts" / "harvest_catalog.py"
WORKER_SCRIPT = ROOT / "scripts" / "colab_worker.py"
COLAB_BIN = shutil.which("colab") or str(Path.home() / ".local" / "bin" / "colab")
COLAB_GLOBAL_ARGS: list[str] = []


def run_colab(
    args: list[str],
    check: bool = True,
    timeout: int = 7200,
    stdin_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    cmd = [COLAB_BIN, *COLAB_GLOBAL_ARGS, *args]
    print(f"[deploy] $ {' '.join(cmd)}", flush=True)
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE if stdin_text is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if stdin_text is not None and proc.stdin is not None:
        try:
            proc.stdin.write(stdin_text)
        except BrokenPipeError:
            pass
        proc.stdin.close()

    deadline = time.monotonic() + timeout
    saw_lost_conn = False
    assert proc.stdout is not None
    while True:
        if time.monotonic() > deadline:
            proc.kill()
            proc.wait()
            raise subprocess.TimeoutExpired(cmd, timeout)
        line = proc.stdout.readline()
        if not line:
            if proc.poll() is not None:
                break
            time.sleep(0.05)
            continue
        print(line, end="", flush=True)
        if "RuntimeError: Connection was lost." in line:
            saw_lost_conn = True
            time.sleep(1.0)
            if proc.poll() is None:
                proc.kill()
            break

    rc = proc.wait(timeout=10)
    if saw_lost_conn and rc == 0:
        rc = 1
    if check and rc != 0:
        raise RuntimeError(f"colab command failed ({rc}): {' '.join(cmd)}")
    return subprocess.CompletedProcess(cmd, rc)


def run_remote_argv(session: str, argv: list[str], timeout: int = 7200) -> None:
    code = (
        "import subprocess\n"
        f"p = subprocess.Popen({argv!r}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)\n"
        "for ln in p.stdout:\n"
        "    print(ln, end='', flush=True)\n"
        "rc = p.wait()\n"
        "if rc != 0:\n"
        "    raise RuntimeError(f'remote command exited with {rc}')\n"
    )
    run_colab(["exec", "-s", session, "--timeout", "0"], check=True, timeout=timeout, stdin_text=code)


def load_pending_volumes(
    limit: int | None = None,
    allowed_ids: set[str] | None = None,
) -> list[dict]:
    if not CATALOG_FILE.exists():
        raise FileNotFoundError(f"Catalog missing: {CATALOG_FILE}")
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    done = {p.name.split(".")[0] for p in TRANSCRIPTS_DIR.glob("bsb*.jsonl.gz") if p.stat().st_size > 0}
    pending = []
    for line in CATALOG_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if not rec.get("admitted") or rec["bsb_id"] in done:
            continue
        if allowed_ids is not None and rec["bsb_id"] not in allowed_ids:
            continue
        pending.append(rec)
    if limit is not None:
        pending = pending[:limit]
    return pending


def provision_gpu(session: str, preferred_gpu: str) -> str:
    run_colab(["sessions"], check=False, timeout=60)
    run_colab(["stop", "-s", session], check=False, timeout=60)
    gpus = [preferred_gpu] + [g for g in ("A100", "L4") if g != preferred_gpu]
    for gpu in gpus:
        res = run_colab(["new", "-s", session, "--gpu", gpu], check=False, timeout=300)
        if res.returncode == 0:
            print(f"[deploy] provisioned Colab session '{session}' with GPU={gpu}", flush=True)
            return gpu
        print(f"[deploy] GPU={gpu} unavailable, trying fallback...", file=sys.stderr, flush=True)
    raise RuntimeError("Could not allocate A100 or L4 GPU on this Colab account.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", default="cgm6874")
    parser.add_argument("--gpu", choices=("A100", "L4", "H100"), default="A100")
    parser.add_argument("--scope", choices=("full", "ethnography"), default="full")
    parser.add_argument("--chunk-size", type=int, default=2)
    parser.add_argument("--limit-volumes", type=int, default=None)
    parser.add_argument("--infer-workers", type=int, default=14)
    parser.add_argument("--max-recoveries", type=int, default=12)
    parser.add_argument("--colab-config", type=Path, default=None)
    parser.add_argument("--volumes-file", type=Path, default=None, help="Newline-delimited BSB IDs for this shard")
    parser.add_argument("--reuse-session", action="store_true")
    parser.add_argument("--keep-session", action="store_true")
    args = parser.parse_args()

    if args.colab_config is not None:
        args.colab_config.parent.mkdir(parents=True, exist_ok=True)
        COLAB_GLOBAL_ARGS[:] = ["--config", str(args.colab_config)]

    allowed_ids: set[str] | None = None
    if args.volumes_file is not None:
        allowed_ids = {
            ln.strip()
            for ln in args.volumes_file.read_text(encoding="utf-8").splitlines()
            if ln.strip()
        }

    run_colab(["usage"], check=True, timeout=60)
    if args.reuse_session:
        run_colab(["sessions"], check=False, timeout=60)
        allocated_gpu = args.gpu
        print(f"[deploy] reusing existing Colab session '{args.session}'", flush=True)
    else:
        allocated_gpu = provision_gpu(args.session, args.gpu)

    recoveries = 0
    t_start = time.monotonic()

    try:
        if not CATALOG_FILE.exists():
            print("[deploy] harvesting Cgm 6874 catalog on Colab VM...", flush=True)
            CATALOG_DIR.mkdir(parents=True, exist_ok=True)
            run_colab(["upload", "-s", args.session, str(HARVEST_SCRIPT), "/content/harvest_catalog.py"], timeout=120)
            run_remote_argv(
                args.session,
                ["python3", "/content/harvest_catalog.py", "--out-dir", "/content/catalog"],
                timeout=600,
            )
            run_colab(["download", "-s", args.session, "/content/catalog/volumes.jsonl", str(CATALOG_FILE)], timeout=120)
            run_colab(
                ["download", "-s", args.session, "/content/catalog/volumes.csv", str(CATALOG_DIR / "volumes.csv")],
                timeout=120,
            )

        run_colab(["upload", "-s", args.session, str(WORKER_SCRIPT), "/content/colab_worker.py"], timeout=120)
        failed_ids: set[str] = set()

        while True:
            pending = [
                r
                for r in load_pending_volumes(args.limit_volumes, allowed_ids=allowed_ids)
                if r["bsb_id"] not in failed_ids
            ]
            if not pending:
                break

            total_pages = sum(
                rec["ethnography_pages"] if args.scope == "ethnography" else rec["canvas_count"]
                for rec in pending
            )
            print(
                f"[deploy] {len(pending)} pending volumes ({total_pages} pages remaining, scope={args.scope})",
                flush=True,
            )

            chunk = pending[: args.chunk_size]
            bsb_ids = [rec["bsb_id"] for rec in chunk]
            infer_workers = args.infer_workers if allocated_gpu != "L4" else min(args.infer_workers, 14)

            try:
                run_remote_argv(
                    args.session,
                    [
                        "python3",
                        "/content/colab_worker.py",
                        "--scope",
                        args.scope,
                        "--download-workers",
                        "10",
                        "--infer-workers",
                        str(infer_workers),
                        "--volumes",
                        *bsb_ids,
                    ],
                    timeout=1200,
                )
            except Exception as exc:
                print(
                    f"[deploy] chunk exec interrupted ({exc}); syncing session token and retrying on warm VM...",
                    file=sys.stderr,
                    flush=True,
                )
                time.sleep(5)
                run_colab(["sessions"], check=False, timeout=60)
                try:
                    run_remote_argv(
                        args.session,
                        [
                            "python3",
                            "/content/colab_worker.py",
                            "--scope",
                            args.scope,
                            "--download-workers",
                            "10",
                            "--infer-workers",
                            str(infer_workers),
                            "--volumes",
                            *bsb_ids,
                        ],
                        timeout=1200,
                    )
                except Exception as exc2:
                    recoveries += 1
                    print(
                        f"[deploy] warm retry failed ({exc2}); reprovisioning VM ({recoveries}/{args.max_recoveries})...",
                        file=sys.stderr,
                        flush=True,
                    )
                    if recoveries > args.max_recoveries:
                        raise
                    time.sleep(15)
                    allocated_gpu = provision_gpu(args.session, args.gpu)
                    run_colab(["upload", "-s", args.session, str(WORKER_SCRIPT), "/content/colab_worker.py"], timeout=120)
                    continue

            for bsb_id in bsb_ids:
                local_dest = TRANSCRIPTS_DIR / f"{bsb_id}.jsonl.gz"
                tmp_dest = TRANSCRIPTS_DIR / f".{bsb_id}.jsonl.gz.part"
                dl = run_colab(
                    ["download", "-s", args.session, f"/content/transcripts/{bsb_id}.jsonl.gz", str(tmp_dest)],
                    check=False,
                    timeout=300,
                )
                if dl.returncode == 0 and tmp_dest.exists() and tmp_dest.stat().st_size > 0:
                    tmp_dest.replace(local_dest)
                else:
                    tmp_dest.unlink(missing_ok=True)
                    failed_ids.add(bsb_id)
                    print(f"[deploy] warning: {bsb_id} produced no transcript; marked skipped", file=sys.stderr, flush=True)

            done_count = len(list(TRANSCRIPTS_DIR.glob("bsb*.jsonl.gz")))
            elapsed_min = (time.monotonic() - t_start) / 60.0
            print(
                f"[deploy] local checkpoints: {done_count} volumes saved ({elapsed_min:.1f} min elapsed)",
                flush=True,
            )

        if failed_ids:
            print(f"[deploy] finished with {len(failed_ids)} skipped volumes: {sorted(failed_ids)}", file=sys.stderr)
            return 1
        print("[deploy] ALL VOLUMES COMPLETED SUCCESSFULLY.", flush=True)
        return 0
    finally:
        if args.keep_session:
            print(f"[deploy] keeping Colab session '{args.session}' warm (--keep-session).", flush=True)
        else:
            print(f"[deploy] stopping Colab session '{args.session}' to preserve compute units...", flush=True)
            run_colab(["stop", "-s", args.session], check=False, timeout=120)


if __name__ == "__main__":
    sys.exit(main())
