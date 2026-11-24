#!/usr/bin/env python3
"""Render an archival-atlas static map of 1860 Bavarian infant feeding and mortality.

Reads `data/dataset/verified_bavaria_1860_infant_feeding.csv` and renders a 2x-supersampled
editorial PNG (`publication/figures/fig_bavaria_1860_feeding_map.png`) showing all 239
canonical districts across Right-Rhine Bavaria + Bavarian Palatinate inset, the Danube and
Main rivers, the unrepresented Upper Bavaria region (held in Stadtarchiv München), and
key birth-cohort infant mortality callouts.
"""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "dataset" / "verified_bavaria_1860_infant_feeding.csv"
OUT_PATH = ROOT / "publication" / "figures" / "fig_bavaria_1860_feeding_map.png"
ARTIFACT_DIR = Path(os.environ["ARTIFACT_DIR"]) if os.environ.get("ARTIFACT_DIR") else None

# High-contrast archival palette (parchment ground, Prussian blue / amber / vermilion ink)
BG = (246, 242, 232)
PANEL_BG = (241, 236, 223)
BORDER = (165, 155, 138)
INK = (26, 24, 22)
MUTED = (98, 92, 83)
RIVER = (118, 155, 178)
OBERBAYERN_FILL = (231, 224, 208)
OBERBAYERN_STROKE = (168, 156, 136)

STATUS_COLORS = {
    "predominantly_breastfed": (27, 73, 101),    # Prussian blue
    "mixed_or_short_duration": (204, 122, 16),   # Ochre / amber
    "rarely_or_not_breastfed": (166, 38, 42),    # Vermilion crimson
    "not_documented": (168, 162, 152),           # Warm stone
}

# Simplified WGS84 polylines (lon, lat) for Danube, Main, and approximate Upper Bavaria region
DANUBE = [
    (9.99, 48.40), (10.30, 48.46), (10.50, 48.57), (10.78, 48.72), (11.18, 48.74),
    (11.42, 48.76), (11.76, 48.81), (11.87, 48.92), (12.10, 49.02), (12.57, 48.88),
    (12.96, 48.83), (13.19, 48.63), (13.46, 48.57), (13.72, 48.53),
]
MAIN = [
    (11.58, 50.09), (11.45, 50.11), (11.07, 50.14), (10.89, 49.90), (10.51, 50.03),
    (10.23, 50.04), (10.17, 49.74), (9.93, 49.79), (9.65, 49.99), (9.58, 49.76),
    (9.26, 49.70), (9.15, 49.97), (9.00, 50.06),
]
OBERBAYERN_POLY = [
    (10.88, 48.68), (11.42, 48.76), (11.78, 48.79), (12.05, 48.45), (12.68, 48.26),
    (12.88, 48.10), (13.02, 47.65), (12.60, 47.60), (11.80, 47.55), (11.05, 47.45),
    (10.82, 47.65), (10.84, 48.20),
]

CALLOUTS = {
    "uffenheim": ("Uffenheim 17.6%", (-228, -16)),
    "fuerth": ("Fürth (urban)", (20, -24)),
    "roth_mittelfranken": ("Roth 40% / Spalt 50%", (22, -10)),
    "greding": ("Greding (Mieder)", (22, -10)),
    "noerdlingen": ("Nördlingen (Ries, N of Danube)", (-395, -10)),
    "oettingen": ("Öttingen 35.9%", (22, -16)),
    "roggenburg": ("Roggenburg", (-162, 14)),
    "goeggingen": ("Göggingen 47.2%", (22, 12)),
    "ottobeuren": ("Ottobeuren 40.7%", (22, 14)),
    "woerth_a_d_donau": ("Wörth a.d.D. 47.4%", (22, -22)),
    "eggenfelden": ("Eggenfelden ~50%", (22, 10)),
    "landstuhl": ("Landstuhl 14.4%*", (-18, 28)),
    "otterberg": ("Otterberg 18.8%", (20, -34)),
}


def load_font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if bold:
        candidates += [
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
            "/System/Library/Fonts/Charter.ttc",
        ]
    elif italic:
        candidates += [
            "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
            "/System/Library/Fonts/Charter.ttc",
        ]
    else:
        candidates += [
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/System/Library/Fonts/Charter.ttc",
        ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def proj_main(lon: float, lat: float, box: tuple[int, int, int, int]) -> tuple[float, float]:
    # Mercator-aspect scaling centered at 49.0N (cos(49) ~= 0.656)
    lon0, lon1 = 8.85, 13.95
    lat0, lat1 = 47.25, 50.65
    x0, y0, x1, y1 = box
    x = x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0)
    y = y1 - (lat - lat0) / (lat1 - lat0) * (y1 - y0)
    return x, y


def proj_pfalz(lon: float, lat: float, box: tuple[int, int, int, int]) -> tuple[float, float]:
    lon0, lon1 = 7.05, 8.60
    lat0, lat1 = 48.95, 49.85
    x0, y0, x1, y1 = box
    x = x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0)
    y = y1 - (lat - lat0) / (lat1 - lat0) * (y1 - y0)
    return x, y


def main() -> int:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    W, H = 2800, 1960
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title = load_font(56, bold=True)
    f_sub = load_font(30, italic=True)
    f_h = load_font(28, bold=True)
    f_body = load_font(24)
    f_small = load_font(22)
    f_callout = load_font(23, bold=True)
    f_region = load_font(26, italic=True)

    # Header
    draw.text((88, 52), "Infant feeding across 239 Bavarian districts (BSB Cgm 6874, 1858–1861)", fill=INK, font=f_title)
    draw.text(
        (88, 122),
        "Franconia and the Palatinate breastfed (86%); Swabia and Old Bavaria relied on flour gruel (Mehlbrei), extending north of the Danube into the Ries",
        fill=MUTED,
        font=f_sub,
    )
    draw.line([(88, 174), (W - 88, 174)], fill=BORDER, width=3)

    # Map frames
    main_box = (88, 206, 2020, 1820)
    pfalz_box = (2068, 206, 2712, 730)
    legend_box = (2068, 774, 2712, 1820)

    for b in (main_box, pfalz_box, legend_box):
        draw.rectangle(b, fill=PANEL_BG, outline=BORDER, width=3)

    # Subtle graticule on main map
    for lon in (9, 10, 11, 12, 13):
        x, _ = proj_main(lon, 49.0, main_box)
        draw.line([(x, main_box[1]), (x, main_box[3])], fill=(228, 222, 208), width=2)
    for lat in (48, 49, 50):
        _, y = proj_main(11.0, lat, main_box)
        draw.line([(main_box[0], y), (main_box[2], y)], fill=(228, 222, 208), width=2)

    # Shaded Oberbayern archival gap region
    ob_pts = [proj_main(lo, la, main_box) for lo, la in OBERBAYERN_POLY]
    draw.polygon(ob_pts, fill=OBERBAYERN_FILL, outline=OBERBAYERN_STROKE)
    ox, oy = proj_main(11.68, 48.08, main_box)
    draw.text((ox - 125, oy - 36), "OBERBAYERN", fill=(120, 110, 96), font=f_h)
    draw.text((ox - 165, oy + 2), "(not in BSB Cgm 6874;", fill=(120, 110, 96), font=f_small)
    draw.text((ox - 155, oy + 30), "Stadtarchiv München)", fill=(120, 110, 96), font=f_small)

    # Rivers
    danube_pts = [proj_main(lo, la, main_box) for lo, la in DANUBE]
    draw.line(danube_pts, fill=RIVER, width=7, joint="curve")
    main_pts = [proj_main(lo, la, main_box) for lo, la in MAIN]
    draw.line(main_pts, fill=RIVER, width=5, joint="curve")

    dx, dy = proj_main(11.55, 48.72, main_box)
    draw.text((dx - 45, dy - 38), "Danube", fill=(68, 108, 132), font=f_small)
    mx, my = proj_main(10.35, 50.07, main_box)
    draw.text((mx - 10, my - 34), "Main", fill=(68, 108, 132), font=f_small)

    # Regional watermarks
    region_labels = [
        ("UNTERFRANKEN", 9.65, 50.28),
        ("OBERFRANKEN", 11.45, 50.32),
        ("MITTELFRANKEN", 10.65, 49.42),
        ("OBERPFALZ", 12.18, 49.58),
        ("NIEDERBAYERN", 12.78, 48.62),
        ("SCHWABEN", 9.65, 47.72),
    ]
    for label, lo, la in region_labels:
        rx, ry = proj_main(lo, la, main_box)
        draw.text((rx - 95, ry), label, fill=(138, 130, 116), font=f_region)

    # Pfalz inset header
    draw.text((pfalz_box[0] + 24, pfalz_box[1] + 18), "Pfalz (Palatinate inset)", fill=INK, font=f_h)
    draw.text((pfalz_box[0] + 24, pfalz_box[1] + 54), "25 districts · 85% breastfed", fill=MUTED, font=f_small)

    # Draw district markers (undocumented first, then documented so signal pops)
    order = {
        "not_documented": 0,
        "predominantly_breastfed": 1,
        "mixed_or_short_duration": 2,
        "rarely_or_not_breastfed": 3,
    }
    rows.sort(key=lambda r: order.get(r["breastfeeding_status"], 0))

    coords_cache: dict[str, tuple[float, float]] = {}
    for r in rows:
        lon, lat = float(r["longitude"]), float(r["latitude"])
        is_pfalz = r["regierungsbezirk"] == "Pfalz"
        px, py = proj_pfalz(lon, lat, pfalz_box) if is_pfalz else proj_main(lon, lat, main_box)
        coords_cache[r["district_id"]] = (px, py)
        col = STATUS_COLORS.get(r["breastfeeding_status"], STATUS_COLORS["not_documented"])
        has_imr = bool(r.get("imr_pct_of_births"))
        rad = 15 if has_imr else 11
        if has_imr:
            draw.ellipse([px - rad - 5, py - rad - 5, px + rad + 5, py + rad + 5], outline=INK, width=3)
        draw.ellipse([px - rad, py - rad, px + rad, py + rad], fill=col, outline=(250, 248, 242), width=2)

    # Callout labels with crisp leader lines
    for did, (text, (ox, oy)) in CALLOUTS.items():
        if did not in coords_cache:
            continue
        px, py = coords_cache[did]
        tx, ty = px + ox, py + oy
        bbox = draw.textbbox((tx, ty), text, font=f_callout)
        pad = 6
        draw.line([(px, py), (tx + (4 if ox > 0 else (bbox[2] - bbox[0] - 4)), ty + 12)], fill=(90, 84, 76), width=2)
        draw.rectangle([bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad], fill=(252, 249, 242), outline=(185, 178, 166), width=2)
        draw.text((tx, ty), text, fill=INK, font=f_callout)

    # Legend & summary panel
    lx, ly = legend_box[0] + 32, legend_box[1] + 28
    draw.text((lx, ly), "Breastfeeding status (n = 239)", fill=INK, font=f_h)
    ly += 54
    legend_items = [
        ("Predominantly breastfed (122)", STATUS_COLORS["predominantly_breastfed"]),
        ("Mixed or short duration (36)", STATUS_COLORS["mixed_or_short_duration"]),
        ("Rarely or not breastfed (23)", STATUS_COLORS["rarely_or_not_breastfed"]),
        ("Undocumented / unstated (58)", STATUS_COLORS["not_documented"]),
    ]
    for label, col in legend_items:
        draw.ellipse([lx + 4, ly + 4, lx + 30, ly + 30], fill=col, outline=(250, 248, 242), width=2)
        draw.text((lx + 46, ly + 3), label, fill=INK, font=f_body)
        ly += 46

    ly += 10
    draw.ellipse([lx + 2, ly + 2, lx + 32, ly + 32], outline=INK, width=3)
    draw.text((lx + 46, ly + 3), "Black ring = birth-cohort IMR (37)", fill=INK, font=f_body)
    ly += 58

    draw.line([(lx, ly), (legend_box[2] - 32, ly)], fill=BORDER, width=2)
    ly += 26
    draw.text((lx, ly), "Birth-cohort infant mortality", fill=INK, font=f_h)
    ly += 44
    summary_lines = [
        "All birth-cohort rates (n = 26):",
        "  Breastfed (17):   23.0% median",
        "  Mixed / rare (9): 40.0% median",
        "  Gap: +17.0 pp (AUC = 0.922)",
        "",
        "Strict live-births only (n = 22):",
        "  Breastfed (15):   24.1% median",
        "  Mixed / rare (7): 40.0% median",
        "  Excl. approx (6): 39.5% median",
        "",
        "Within Mittelfranken (n = 8):",
        "  Breastfed (6):    24.9% median",
        "  Roth / Weißenburg: 40.0% / 38.9%",
    ]
    for line in summary_lines:
        if not line:
            ly += 14
            continue
        draw.text((lx, ly), line, fill=INK if not line.startswith("  ") else MUTED, font=f_small)
        ly += 34

    ly += 18
    draw.line([(lx, ly), (legend_box[2] - 32, ly)], fill=BORDER, width=2)
    ly += 22
    draw.text((lx, ly), "*Landstuhl: 14.4% live-birth IMR", fill=MUTED, font=f_small)
    ly += 30
    draw.text((lx, ly), "  (16.3% incl. stillbirths).", fill=MUTED, font=f_small)
    ly += 36
    draw.text((lx, ly), "Source: BSB Cgm 6874 (PDM 1.0);", fill=MUTED, font=f_small)
    ly += 30
    draw.text((lx, ly), "13fragments (agent-checked; human", fill=MUTED, font=f_small)
    ly += 30
    draw.text((lx, ly), "paleographer review open).", fill=MUTED, font=f_small)

    # Footer
    draw.text(
        (88, 1858),
        "Positions show 1860 district seats (WGS84). Notice Nördlingen, Wemding, Öttingen, and Wallerstein (Ries) lie north of the Danube yet follow the Swabian non-breastfeeding regime.",
        fill=MUTED,
        font=f_small,
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    final_img = img.resize((1400, 980), Image.Resampling.LANCZOS)
    final_img.save(OUT_PATH, format="PNG", optimize=True)
    if ARTIFACT_DIR is not None and ARTIFACT_DIR.exists():
        shutil.copy2(OUT_PATH, ARTIFACT_DIR / OUT_PATH.name)
    print(f"Rendered {OUT_PATH} ({final_img.size[0]}x{final_img.size[1]}px)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
