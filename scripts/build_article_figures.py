#!/usr/bin/env python3
"""Generate publication-ready archival Kurrent crops for Article 1, Article 2, and report.

Crops exact verified passage strips from local IIIF scans in `data/verification_scans/`,
saves them under `publication/figures/`, and copies them into the conversation artifact
directory for direct Markdown embedding.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCANS_DIR = ROOT / "data" / "verification_scans"
FIG_DIR = ROOT / "publication" / "figures"
ARTIFACT_DIR = Path(os.environ["ARTIFACT_DIR"]) if os.environ.get("ARTIFACT_DIR") else None

# Fractional crop boxes `(x0, y0, x1, y1)` verified visually on each 1400px scan
CROPS = {
    # Roggenburg (bsb00007355 scan 15): Schnuller dipped in Schnaps + Mehlbrei / Schnullerbrod
    "fig_roggenburg_schnaps_pacifier.jpg": ("bsb00007355_p015.jpg", (0.45, 0.09, 0.99, 0.52)),
    # Roggenburg (bsb00007355 scan 27): Maid with throat chancres moistening newborn's Schnuller
    "fig_roggenburg_syphilis_pacifier.jpg": ("bsb00007355_p027.jpg", (0.01, 0.24, 0.51, 0.50)),
    # Landstuhl, Pfalz (bsb00145118 scan 58): Poppy-head decoction (Mohnköpfen) -> severe intoxication
    "fig_landstuhl_poppy_decoction.jpg": ("bsb00145118_p058.jpg", (0.34, 0.58, 0.95, 0.77)),
    # Bischofsheim v. d. Rhön (bsb00140582 scan 146): City wet-nurses use opium; mothers here put Schnaps under pacifier
    "fig_bischofsheim_schnaps_opium.jpg": ("bsb00140582_p146.jpg", (0.44, 0.50, 0.96, 0.79)),
    # Landshut Land (bsb00111891 scan 33): Stiff Mieder bodices flatten nipples -> unsuitable for nursing
    "fig_landshut_mieder_nipples.jpg": ("bsb00111891_p033.jpg", (0.03, 0.21, 0.74, 0.39)),
    # Greding (bsb00141175 scan 131): Within-district natural experiment on stiff Mieder vs Franconian Leibchen
    "fig_greding_mieder_natural_experiment.jpg": ("bsb00141175_p131.jpg", (0.20, 0.35, 0.91, 0.72)),
    # Lauingen (bsb00009733 scan 253): Boiled dog meat for TB, dog/hare/badger fat for wasting
    "fig_lauingen_folk_remedies.jpg": ("bsb00009733_p253.jpg", (0.01, 0.10, 0.98, 0.46)),
    # Amberg Land (bsb00026307 scan 252): Flaming schnapps glass cupped over infant navel + walnut shell of lard
    "fig_amberg_navel_cupping.jpg": ("bsb00026307_p252.jpg", (0.12, 0.22, 0.97, 0.44)),
}


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for out_name, (src_name, (fx0, fy0, fx1, fy1)) in CROPS.items():
        src_path = SCANS_DIR / src_name
        img = Image.open(src_path).convert("RGB")
        w, h = img.size
        box = (int(w * fx0), int(h * fy0), int(w * fx1), int(h * fy1))
        cropped = img.crop(box)
        dest = FIG_DIR / out_name
        cropped.save(dest, format="JPEG", quality=90, optimize=True)
        if ARTIFACT_DIR is not None and ARTIFACT_DIR.exists():
            shutil.copy2(dest, ARTIFACT_DIR / out_name)
        print(f"Saved {out_name}: {cropped.size[0]}x{cropped.size[1]}px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
