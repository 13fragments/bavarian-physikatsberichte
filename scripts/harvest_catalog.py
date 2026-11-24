#!/usr/bin/env python3
"""Harvest all digitized BSB Cgm 6874 volumes and verify PDM-1.0 IIIF manifests.

Queries the Bayerische Staatsbibliothek ExLibris Alma SRU endpoint
(`https://bvb.alma.exlibrisgroup.com/view/sru/49BVB_BSB`) for all MARC21 records
in `Cgm 6874`, extracts `bsb...` digital object IDs from MARC fields `990$c` / `856$u` / `776$o`,
fetches each IIIF Presentation v2 manifest in parallel, verifies `PDM 1.0` licensing,
counts total canvases and `Ethnographie` start offsets, and writes:
  - `data/catalog/volumes.jsonl`
  - `data/catalog/volumes.csv`
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import json
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SRU_URL = "http://bvbr.bib-bvb.de:5661/bvb01sru"
USER_AGENT = "13fragments-htr/1.0 (historical public-health corpus research; catalog harvest)"
NS = {
    "srw": "http://www.loc.gov/zing/srw/",
    "marc": "http://www.loc.gov/MARC21/slim",
}


def fetch_bytes(url: str, timeout: int = 90, attempts: int = 4) -> bytes:
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
        time.sleep(2 * attempt)
    raise AssertionError("unreachable")


def query_sru_bsb_ids() -> dict[str, dict]:
    """Return {bsb_id: {'sru_title': ..., 'shelfmark': ...}} across all B3Kat SRU pages."""
    found: dict[str, dict] = {}
    start = 1
    page_size = 50
    while True:
        params = urllib.parse.urlencode(
            {
                "version": "1.1",
                "operation": "searchRetrieve",
                "recordSchema": "marcxml",
                "maximumRecords": str(page_size),
                "startRecord": str(start),
                "query": "dc.title=Physikatsbezirke",
            }
        )
        xml_bytes = fetch_bytes(f"{SRU_URL}?{params}")
        root = ET.fromstring(xml_bytes)
        total_el = root.find("srw:numberOfRecords", NS)
        total = int(total_el.text) if total_el is not None and total_el.text else 0
        records = root.findall(".//marc:record", NS)
        for rec in records:
            title = ""
            for sf in rec.findall("marc:datafield[@tag='245']/marc:subfield[@code='a']", NS):
                if sf.text:
                    title = sf.text.strip()
            shelfmarks = [
                sf.text.strip()
                for tag in ("024", "990", "AVA", "856")
                for sf in rec.findall(f"marc:datafield[@tag='{tag}']/marc:subfield", NS)
                if sf.text and "6874" in sf.text
            ]
            if "6874" not in title and not shelfmarks:
                continue
            blob = ET.tostring(rec, encoding="unicode")
            for bsb_id in set(re.findall(r"\bbsb\d{8}\b", blob)):
                found[bsb_id] = {
                    "sru_title": title,
                    "shelfmark": shelfmarks[0] if shelfmarks else "",
                }
        if not records or start + len(records) > total:
            break
        start += len(records)
    return found


def inspect_manifest(bsb_id: str, meta: dict) -> dict:
    url = f"https://api.digitale-sammlungen.de/iiif/presentation/v2/{bsb_id}/manifest"
    try:
        manifest = json.loads(fetch_bytes(url).decode("utf-8"))
    except Exception as exc:
        return {
            "bsb_id": bsb_id,
            "admitted": False,
            "reject_reason": f"manifest_fetch_failed: {exc}",
            "volume_number": "",
            "district": "",
            "label": meta.get("sru_title", ""),
            "license": "",
            "canvas_count": 0,
            "ethnography_start_canvas": 1,
            "ethnography_pages": 0,
        }

    label = str(manifest.get("label") or meta.get("sru_title") or "")
    lic = str(manifest.get("license") or "")
    blob = json.dumps(
        [manifest.get("license"), manifest.get("rights"), manifest.get("attribution")],
        ensure_ascii=False,
    ).lower()

    admitted = (
        "6874" in label
        and "creativecommons.org/publicdomain/mark/1.0" in lic.lower()
        and not any(r in blob for r in ("by-nc", "by-nd", "rightsstatements.org", "in copyright"))
    )
    reason = "" if admitted else f"license_or_title_check_failed ({lic})"

    canvases = manifest.get("sequences", [{}])[0].get("canvases", [])
    id_to_idx = {c.get("@id"): idx for idx, c in enumerate(canvases)}
    ethno_idx = 0
    for struct in manifest.get("structures", []):
        slabel = json.dumps(struct.get("label", ""), ensure_ascii=False).lower()
        if "ethnograph" in slabel:
            sc = struct.get("canvases") or []
            if sc and sc[0] in id_to_idx:
                ethno_idx = id_to_idx[sc[0]]
                break

    match = re.search(r"Bd\.\s*([^:]+):\s*(.+?)\s*-\s*BSB\s*Cgm\s*6874", label)
    vol_no = match.group(1).strip() if match else ""
    district = match.group(2).strip() if match else label

    return {
        "bsb_id": bsb_id,
        "admitted": admitted,
        "reject_reason": reason,
        "volume_number": vol_no,
        "district": district,
        "label": label,
        "license": lic,
        "canvas_count": len(canvases),
        "ethnography_start_canvas": ethno_idx + 1,
        "ethnography_pages": max(0, len(canvases) - ethno_idx),
    }


def sort_key(rec: dict) -> tuple[int, str, str]:
    m = re.match(r"(\d+)", rec.get("volume_number") or "")
    return (int(m.group(1)) if m else 9999, rec.get("volume_number") or "", rec["bsb_id"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "catalog",
    )
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()

    print("[harvest] querying BSB Alma SRU for Cgm 6874 volumes...", flush=True)
    candidates = query_sru_bsb_ids()
    print(f"[harvest] discovered {len(candidates)} candidate BSB IDs; checking IIIF manifests...", flush=True)

    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(inspect_manifest, bid, meta): bid for bid, meta in candidates.items()}
        for fut in as_completed(futures):
            rows.append(fut.result())
    rows.sort(key=sort_key)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.out_dir / "volumes.jsonl"
    csv_path = args.out_dir / "volumes.csv"

    with jsonl_path.open("w", encoding="utf-8") as jf:
        for row in rows:
            jf.write(json.dumps(row, ensure_ascii=False) + "\n")

    fields = [
        "bsb_id",
        "admitted",
        "volume_number",
        "district",
        "canvas_count",
        "ethnography_start_canvas",
        "ethnography_pages",
        "license",
        "reject_reason",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    admitted = [r for r in rows if r["admitted"]]
    total_pages = sum(r["canvas_count"] for r in admitted)
    ethno_pages = sum(r["ethnography_pages"] for r in admitted)
    print(
        f"[harvest] admitted {len(admitted)}/{len(rows)} PDM-1.0 volumes: "
        f"{total_pages} total pages ({ethno_pages} ethnography-scoped pages).",
        flush=True,
    )
    return 0 if admitted else 1


if __name__ == "__main__":
    sys.exit(main())
