#!/usr/bin/env python3
"""Extract standardized 1858 questionnaire topics from completed Cgm 6874 transcripts.

Builds:
1. `data/dataset/district_excerpts.jsonl` — candidate paragraphs per district for
   infant care / feeding / poppy pacifiers, diet, endemic goiter/cretinism, and folk superstitions.
2. `data/dataset/verification_viewer.html` — self-contained side-by-side verification page linking
   every extracted excerpt directly to its original BSB IIIF image scan.
"""

from __future__ import annotations

import gzip
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = ROOT / "data" / "transcripts"
DATASET_DIR = ROOT / "data" / "dataset"

TOPIC_PATTERNS = {
    "infant_care": re.compile(
        r"(säugling|ersten\s+lebensjahr|kinderpflege|mutterbrust|stillen|gestillt|"
        r"mehlbrei|schlafmohn|mohnköpf|schnuller|zulp|kindersterblichkeit)",
        re.IGNORECASE,
    ),
    "goiter_cretinism": re.compile(
        r"(kropf|struma|cretin|kretin|blödsinn|schilddrüse)",
        re.IGNORECASE,
    ),
    "folk_medicine_superstition": re.compile(
        r"(aberglaub|sympathie|pfusch|quacksalb|geheimmittel|amulett|segen|"
        r"hexen|schinder|hundsschmalz|volksarznei|volksheilmittel)",
        re.IGNORECASE,
    ),
    "nutrition_beverages": re.compile(
        r"(nahrungsweise|ernährung|branntwein|brantwein|bierpreis|mandelrüben|"
        r"kartoffel|schmalz|fleischgenuß)",
        re.IGNORECASE,
    ),
}


def parse_district(volume_label: str, bsb_id: str) -> tuple[str, str]:
    match = re.search(r"Bd\.\s*([^:]+):\s*(.+?)\s*-\s*BSB\s*Cgm\s*6874", volume_label)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", volume_label or bsb_id


def main() -> int:
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(TRANSCRIPTS_DIR.glob("bsb*.jsonl.gz"))
    rows = []

    for path in files:
        bsb_id = path.name.split(".")[0]
        with gzip.open(path, "rt", encoding="utf-8") as gz:
            pages = [json.loads(line) for line in gz if line.strip()]
        if not pages:
            continue
        vol_no, district = parse_district(pages[0].get("volume_label", ""), bsb_id)
        for page in pages:
            text = page.get("text") or ""
            for topic, pattern in TOPIC_PATTERNS.items():
                matches = list(pattern.finditer(text))
                if not matches:
                    continue
                terms = sorted({m.group(0).lower() for m in matches})
                rows.append(
                    {
                        "bsb_id": bsb_id,
                        "volume_number": vol_no,
                        "district": district,
                        "canvas_number": page["canvas_number"],
                        "topic": topic,
                        "matched_terms": terms,
                        "iiif_image_url": page["iiif_image_url"],
                        "mdz_viewer_url": f"https://www.digitale-sammlungen.de/de/view/{bsb_id}?page={page['canvas_number']}",
                        "incomplete": page.get("incomplete"),
                        "text": text,
                    }
                )

    jsonl_path = DATASET_DIR / "district_excerpts.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    cards = []
    for row in rows[:300]:
        preview_url = row["iiif_image_url"].replace("/full/full/", "/full/900,/")
        cards.append(
            f"""
            <article class="card" data-topic="{html.escape(row['topic'])}">
              <header>
                <strong>{html.escape(row['district'])}</strong>
                <span>Bd. {html.escape(row['volume_number'])} · {html.escape(row['bsb_id'])} · scan {row['canvas_number']}</span>
                <span class="tag">{html.escape(row['topic'])}</span>
                <span>hits: {html.escape(', '.join(row['matched_terms']))}</span>
                <a href="{html.escape(row['mdz_viewer_url'])}" target="_blank" rel="noopener">Open MDZ scan</a>
              </header>
              <div class="pair">
                <a href="{html.escape(row['iiif_image_url'])}" target="_blank" rel="noopener">
                  <img loading="lazy" src="{html.escape(preview_url)}" alt="Scan {row['canvas_number']}">
                </a>
                <pre>{html.escape(row['text'])}</pre>
              </div>
            </article>
            """
        )

    viewer_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BSB Cgm 6874 Verification Viewer</title>
<style>
  body {{ font-family: Georgia, serif; margin: 2rem; background: #f6f4ef; color: #1b1b1b; }}
  .card {{ background: #fff; border: 1px solid #d4cfc4; margin-bottom: 1.5rem; padding: 1rem; }}
  header {{ display: flex; gap: 1rem; flex-wrap: wrap; align-items: baseline; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; margin-bottom: 0.8rem; }}
  .tag {{ background: #1f3a52; color: #fff; padding: 0.15rem 0.5rem; font-size: 0.85rem; }}
  .pair {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; align-items: start; }}
  img {{ width: 100%; height: auto; border: 1px solid #ccc; }}
  pre {{ white-space: pre-wrap; font-family: ui-monospace, Menlo, monospace; font-size: 0.88rem; line-height: 1.45; margin: 0; }}
</style>
</head>
<body>
<h1>BSB Cgm 6874 — Side-by-side scan verification ({len(rows)} total topic hits across {len(files)} volumes)</h1>
<p>Rule: verify every figure and quotation against the scan before inclusion in the final dataset or article.</p>
{''.join(cards)}
</body>
</html>
"""
    (DATASET_DIR / "verification_viewer.html").write_text(viewer_html, encoding="utf-8")
    print(f"Wrote {len(rows)} topic hits from {len(files)} volumes to {jsonl_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
