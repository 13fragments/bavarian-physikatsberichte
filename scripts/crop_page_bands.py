#!/usr/bin/env python3
"""Split a page scan into overlapping horizontal bands for close reading.

Full IIIF page images are about 2200 x 3800 pixels, and a whole page shrunk to
one view is not legible. Each band extends 8% of a band height past each of its
edges, so neighboring bands overlap by 16% and no line is cut in every crop.

Usage: python3 crop_page_bands.py <image.jpg> <out_dir> [bands=4] [x0_frac=0] [x1_frac=1]
Use x0_frac of about 0.45 for pages that carry the text only in the right half.
"""

from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image


def main() -> int:
    if not 3 <= len(sys.argv) <= 6:
        print(__doc__)
        return 2
    image_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    try:
        bands = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        x0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
        x1 = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    except ValueError:
        bands, x0, x1 = 0, 0.0, 0.0
    if bands < 1 or not 0.0 <= x0 < x1 <= 1.0:
        print("error: bands must be at least 1, and 0 <= x0_frac < x1_frac <= 1", file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(image_path)
    width, height = img.size
    band, pad = height / bands, height / bands * 0.08
    for i in range(bands):
        top, bottom = max(0, int(i * band - pad)), min(height, int((i + 1) * band + pad))
        dest = out_dir / f"{image_path.stem}_b{i + 1}of{bands}.jpg"
        img.crop((int(width * x0), top, int(width * x1), bottom)).save(dest, quality=90)
        print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
