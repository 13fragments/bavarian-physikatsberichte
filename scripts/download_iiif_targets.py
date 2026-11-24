#!/usr/bin/env python3
"""Concurrent IIIF scan downloader for evaluation and visual verification.

Reads a JSON list of `{"url": "...", "dest": "..."}` entries and downloads all
missing JPEGs from `api.digitale-sammlungen.de` with polite concurrency and retries.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import sys
import time
import urllib.request

USER_AGENT = "13fragments-physikatsberichte-verifier/1.0 (https://13fragments.com)"


def fetch_one(item: dict) -> tuple[str, str]:
    url = item["url"]
    dest = Path(item["dest"])
    if dest.exists() and dest.stat().st_size > 1000:
        return "cached", str(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".jpg.part")
    last_err = ""
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
            if len(data) < 1000:
                raise RuntimeError(f"short response ({len(data)} bytes)")
            tmp.write_bytes(data)
            tmp.replace(dest)
            return "downloaded", str(dest)
        except Exception as exc:
            last_err = str(exc)
            time.sleep(1.5 * (attempt + 1))
    tmp.unlink(missing_ok=True)
    return f"error: {last_err}", str(dest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=10)
    args = parser.parse_args()

    items = json.loads(args.manifest.read_text(encoding="utf-8"))
    counts = {"cached": 0, "downloaded": 0, "errors": 0}
    errors = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(fetch_one, item) for item in items]
        for idx, fut in enumerate(as_completed(futs), start=1):
            status, dest = fut.result()
            if status in ("cached", "downloaded"):
                counts[status] += 1
            else:
                counts["errors"] += 1
                errors.append({"dest": dest, "status": status})
            if idx % 50 == 0 or idx == len(items):
                print(
                    f"[iiif] {idx}/{len(items)} processed "
                    f"(downloaded={counts['downloaded']}, cached={counts['cached']}, errors={counts['errors']})",
                    flush=True,
                )

    if errors:
        print(json.dumps(errors[:10], indent=2), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
