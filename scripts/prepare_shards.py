#!/usr/bin/env python3
"""Rescue any uncheckpointed remote transcripts on cgm6874, allocate parallel GPU sessions,
and create page-balanced volume shard files for concurrent Colab execution.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT / "data" / "catalog" / "volumes.jsonl"
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
SHARDS_DIR = ROOT / "data" / "shards"
COLAB_BIN = shutil.which("colab") or str(Path.home() / ".local" / "bin" / "colab")


def run_colab(args: list[str], timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run([COLAB_BIN, *args], text=True, capture_output=True, timeout=timeout)


def rescue_remote_files(session: str) -> int:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    local_done = {p.name for p in TRANSCRIPTS_DIR.glob("bsb*.jsonl.gz") if p.stat().st_size > 0}
    ls_res = run_colab(["ls", "-s", session, "/content/transcripts"])
    if ls_res.returncode != 0:
        return 0
    rescued = 0
    for line in ls_res.stdout.splitlines():
        fname = line.strip()
        if not re.fullmatch(r"bsb\d{8}\.jsonl\.gz", fname) or fname in local_done:
            continue
        tmp = TRANSCRIPTS_DIR / f".{fname}.part"
        dest = TRANSCRIPTS_DIR / fname
        dl = run_colab(["download", "-s", session, f"/content/transcripts/{fname}", str(tmp)], timeout=300)
        if dl.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.replace(dest)
            rescued += 1
            print(f"[shards] rescued {fname} from {session}", flush=True)
        else:
            tmp.unlink(missing_ok=True)
    return rescued


def parse_active_sessions() -> dict[str, str]:
    res = run_colab(["sessions"])
    active: dict[str, str] = {}
    for line in (res.stdout + "\n" + res.stderr).splitlines():
        m = re.search(r"\[([^\]]+)\].*Hardware:\s*(\S+)", line)
        if m and m.group(1) != "?":
            active[m.group(1)] = m.group(2)
    return active


def try_allocate(session: str) -> str | None:
    for gpu in ("A100", "L4"):
        res = run_colab(["new", "-s", session, "--gpu", gpu], timeout=300)
        if res.returncode == 0:
            print(f"[shards] allocated {session} -> {gpu}", flush=True)
            return gpu
        combined = (res.stdout + "\n" + res.stderr).lower()
        if "precondition failed" in combined or "too many active sessions" in combined:
            print(f"[shards] reached Colab concurrent session limit on {session} ({gpu})", flush=True)
            if gpu == "L4":
                return None
    return None


def main() -> int:
    active = parse_active_sessions()
    print(f"[shards] existing active sessions: {active}", flush=True)

    if "cgm6874" in active:
        rescued = rescue_remote_files("cgm6874")
        print(f"[shards] rescued {rescued} completed transcripts from cgm6874", flush=True)

    target_sessions = ["cgm6874", "cgm6874-s1", "cgm6874-s2", "cgm6874-s3"]
    allocated: list[tuple[str, str]] = []
    for name in target_sessions:
        if name in active and active[name] in ("A100", "L4", "H100"):
            allocated.append((name, active[name]))
            continue
        gpu = try_allocate(name)
        if gpu is not None:
            allocated.append((name, gpu))
        else:
            break

    if not allocated:
        raise RuntimeError("No GPU sessions available.")

    done = {p.name.split(".")[0] for p in TRANSCRIPTS_DIR.glob("bsb*.jsonl.gz") if p.stat().st_size > 0}
    pending = []
    for line in CATALOG_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("admitted") and rec["bsb_id"] not in done:
            pending.append(rec)

    # Greedy weighted load balancing by page count (largest volumes assigned first)
    weights = {"H100": 3.0, "A100": 2.4, "L4": 1.0}
    buckets: list[list[dict]] = [[] for _ in allocated]
    virtual_load = [0.0 for _ in allocated]

    for rec in sorted(pending, key=lambda r: int(r["canvas_count"]), reverse=True):
        best_i = min(range(len(allocated)), key=lambda i: virtual_load[i])
        buckets[best_i].append(rec)
        w = weights.get(allocated[best_i][1], 1.0)
        virtual_load[best_i] += int(rec["canvas_count"]) / w

    SHARDS_DIR.mkdir(parents=True, exist_ok=True)
    plan = []
    for i, ((sess, gpu), vols) in enumerate(zip(allocated, buckets)):
        # Sort each shard's volumes smallest-first so early checkpoints arrive fast
        vols.sort(key=lambda r: int(r["canvas_count"]))
        shard_file = SHARDS_DIR / f"{sess}.txt"
        shard_file.write_text("\n".join(r["bsb_id"] for r in vols) + "\n", encoding="utf-8")
        pages = sum(int(r["canvas_count"]) for r in vols)
        plan.append({"session": sess, "gpu": gpu, "volumes": len(vols), "pages": pages, "file": str(shard_file)})

    (SHARDS_DIR / "plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"done_volumes": len(done), "remaining_volumes": len(pending), "shards": plan}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
