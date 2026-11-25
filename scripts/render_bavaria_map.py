#!/usr/bin/env python3
"""Render Figure 2: infant feeding at the 1860 district seats of BSB Cgm 6874.

Reads `data/dataset/verified_bavaria_1860_infant_feeding.csv` and writes
`publication/figures/fig_bavaria_1860_feeding_map.svg`. With Google Chrome
available, it also writes a 2x PNG next to it.

The map makes no claim about district boundaries. Each point is the seat of one
of the 239 canonical districts. No open data set of the 1860 Bavarian district
boundaries was used, so the figure draws none. River courses are schematic
polylines through towns on their banks, for orientation only. The Palatinate
appears as an inset at the same scale.
"""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "dataset" / "verified_bavaria_1860_infant_feeding.csv"
SVG_PATH = ROOT / "publication" / "figures" / "fig_bavaria_1860_feeding_map.svg"
PNG_PATH = SVG_PATH.with_suffix(".png")
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

WIDTH, HEIGHT = 560, 560
FONT = '"IBM Plex Mono", ui-monospace, Menlo, monospace'
INK, MUTED, BG, FRAME, RIVER = "#111", "#666", "#fdfdfc", "#cfcfcf", "#9db3c4"

STATUS = {
    "predominantly_breastfed": ("#2b5c8a", "Predominantly breastfed"),
    "mixed_or_short_duration": ("#d08c1a", "Mixed or short breastfeeding"),
    "rarely_or_not_breastfed": ("#a3292b", "Rarely or not breastfed"),
    "not_documented": ("none", "Feeding not documented"),
}
DRAW_ORDER = ["not_documented", "predominantly_breastfed", "mixed_or_short_duration", "rarely_or_not_breastfed"]

# Main map frame, in degrees. The scale is equal in x and y at latitude 49.
LON0, LON1, LAT0, LAT1 = 8.95, 13.95, 47.38, 50.72
COS = math.cos(math.radians(49.0))
PAD = 10
SCALE = (WIDTH - 2 * PAD) / ((LON1 - LON0) * COS)

# Palatinate inset: top-right corner of the main map, same scale.
INSET_LON0, INSET_LAT1 = 7.13, 49.80
INSET_X, INSET_Y, INSET_W, INSET_H = 390, 10, 164, 158

# Schematic river courses (lon, lat) through towns on their banks.
DANUBE = [
    (10.01, 48.40), (10.22, 48.45), (10.27, 48.45), (10.43, 48.57), (10.49, 48.58),
    (10.57, 48.61), (10.78, 48.72), (10.94, 48.74), (11.18, 48.73), (11.43, 48.76),
    (11.62, 48.77), (11.77, 48.80), (11.89, 48.92), (12.04, 48.94), (12.10, 49.02),
    (12.21, 49.03), (12.40, 49.00), (12.57, 48.88), (12.69, 48.91), (12.96, 48.84),
    (13.03, 48.77), (13.18, 48.63), (13.46, 48.57), (13.72, 48.52),
]
MAIN = [
    (11.58, 49.94), (11.45, 50.10), (11.25, 50.14), (11.06, 50.15), (10.99, 50.10),
    (10.88, 49.93), (10.51, 50.03), (10.23, 50.04), (10.23, 49.86), (10.16, 49.80),
    (10.16, 49.74), (10.15, 49.67), (10.07, 49.66), (9.93, 49.79), (9.77, 49.96),
    (9.70, 50.05), (9.58, 50.00), (9.60, 49.85), (9.52, 49.76), (9.26, 49.70),
    (9.15, 49.84), (9.15, 49.97), (9.00, 50.07),
]
LECH = [(10.70, 47.57), (10.90, 47.81), (10.88, 48.05), (10.93, 48.37), (10.95, 48.74)]
RHINE = [(8.18, 48.97), (8.37, 49.22), (8.44, 49.32), (8.44, 49.48), (8.37, 49.63), (8.40, 49.80)]

# Region names at hand-placed anchor points (lon, lat), clear of the points.
REGIONS = [
    ("Lower Franconia", 9.45, 50.62, "middle"),
    ("Upper Franconia", 11.62, 50.62, "middle"),
    ("Middle Franconia", 10.05, 49.28, "end"),
    ("Upper Palatinate", 12.75, 49.55, "middle"),
    ("Lower Bavaria", 13.35, 49.30, "middle"),
    ("Swabia", 9.55, 47.95, "middle"),
]

# Labelled districts with their first-year death rate where the article cites one.
CALLOUTS = [
    ("roggenburg", "Roggenburg"),
    ("ottobeuren", "Ottobeuren 40.7%"),
    ("oettingen", "Öttingen 35.9%"),
    ("noerdlingen", "Nördlingen"),
    ("uffenheim", "Uffenheim 17.6%"),
    ("fuerth", "Fürth"),
    ("roth_mittelfranken", "Roth 40.0%"),
    ("greding", "Greding"),
    ("woerth_a_d_donau", "Wörth 47.4%"),
    ("eggenfelden", "Eggenfelden ~50%"),
    ("landstuhl", "Landstuhl"),
]
CALLOUT_SIZE = 9.5
CHAR_WIDTH = 0.6  # IBM Plex Mono advance width, in em

# Legend box, bottom-right corner (Salzburg and Austria, no districts).
LEGEND_X, LEGEND_Y, LEGEND_W, LEGEND_H = 372, 462, 182, 88


def project(lon: float, lat: float) -> tuple[float, float]:
    return PAD + (lon - LON0) * COS * SCALE, PAD + (LAT1 - lat) * SCALE


def project_inset(lon: float, lat: float) -> tuple[float, float]:
    return INSET_X + 8 + (lon - INSET_LON0) * COS * SCALE, INSET_Y + 22 + (INSET_LAT1 - lat) * SCALE


def polyline(points: list[tuple[float, float]], proj, width: float) -> str:
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in (proj(lon, lat) for lon, lat in points))
    return f'<polyline points="{path}" fill="none" stroke="{RIVER}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'


def text(x: float, y: float, body: str, size: float = 10, fill: str = INK, anchor: str = "start", extra: str = "") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
        f'stroke="{BG}" stroke-width="3" paint-order="stroke" stroke-linejoin="round"{extra}>{escape(body)}</text>'
    )


def label_box(x: float, y: float, label: str, anchor: str) -> tuple[float, float, float, float]:
    width = CHAR_WIDTH * CALLOUT_SIZE * len(label)
    left = {"start": x, "end": x - width, "middle": x - width / 2}[anchor]
    return left - 1, y - CALLOUT_SIZE * 0.8, left + width + 1, y + CALLOUT_SIZE * 0.25


def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def place_label(x, y, label, points, obstacles):
    """Score label positions around a point; return text position, anchor, and leader start or None.

    Candidates sit at four distances in eight directions. The score counts the
    points and earlier labels or frames that the text box would cover, with a
    small penalty for distance. Labels away from their point get a leader line.
    """
    best = None
    for distance in (8, 16, 24, 34):
        for step in range(8):
            angle = math.radians(step * 45)
            dx, dy = math.cos(angle), -math.sin(angle)
            ax, ay = x + distance * dx, y + distance * dy
            anchor = "start" if dx > 0.3 else "end" if dx < -0.3 else "middle"
            baseline = ay + 3.5 if abs(dy) < 0.3 else ay - 1 if dy < 0 else ay + 8.5
            box = label_box(ax, baseline, label, anchor)
            if box[0] < 2 or box[2] > WIDTH - 2 or box[1] < 2 or box[3] > HEIGHT - 2:
                continue
            hits = sum(1 for px, py, r in points if overlaps(box, (px - r, py - r, px + r, py + r)))
            hits += sum(1 for other in obstacles if overlaps(box, other))
            score = hits * 10 + distance * 0.15 + (0 if abs(dy) < 0.3 else 0.6)
            if best is None or score < best[0]:
                start = 8.5 if (x, y, 7.0) in points else 5.5
                leader = (x + start * dx, y + start * dy, ax - 1.5 * dx, ay - 1.5 * dy) if distance > 8 else None
                best = (score, ax, baseline, anchor, box, leader)
    _, lx, ly, anchor, box, leader = best
    obstacles.append(box)
    return lx, ly, anchor, leader


def legend() -> list[str]:
    x, y = LEGEND_X, LEGEND_Y
    out = [f'<rect x="{x}" y="{y}" width="{LEGEND_W}" height="{LEGEND_H}" fill="{BG}" stroke="{FRAME}"/>']
    row = y + 16
    for status in ("predominantly_breastfed", "mixed_or_short_duration", "rarely_or_not_breastfed", "not_documented"):
        color, label = STATUS[status]
        if status == "not_documented":
            out.append(f'<circle cx="{x + 12}" cy="{row - 3}" r="3" fill="{BG}" stroke="#8a8a8a" stroke-width="1.1"/>')
        else:
            out.append(f'<circle cx="{x + 12}" cy="{row - 3}" r="3.6" fill="{color}"/>')
        out.append(text(x + 22, row, label, 8.5, INK))
        row += 14
    out.append(f'<circle cx="{x + 12}" cy="{row - 3}" r="6" fill="none" stroke="{INK}" stroke-width="1.1"/>')
    out.append(text(x + 22, row, "First-year death rate given", 8.5, INK))
    return out


def district_title(row: dict[str, str]) -> str:
    parts = [row["district_name"], STATUS[row["breastfeeding_status"]][1].lower()]
    if row.get("imr_pct_of_births"):
        basis = "live births" if row["infant_mortality_denominator"] == "live_births" else "all births"
        parts.append(f"first-year deaths {float(row['imr_pct_of_births']):.1f}% of {basis}")
    return ", ".join(parts)


def build_svg(rows: list[dict[str, str]]) -> str:
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" '
        f'font-family=\'{FONT}\' role="img" aria-labelledby="map-title map-desc">',
        '<title id="map-title">Infant feeding at the seats of 239 Bavarian districts, 1858 to 1861</title>',
        '<desc id="map-desc">Each point is a district seat, colored by how the district physician described infant feeding. '
        "Blue points, predominantly breastfed, fill Franconia and the Palatinate. Red and amber points, rarely or briefly "
        "breastfed, fill Swabia and parts of Lower Bavaria. Upper Bavaria is blank because its reports are not in this "
        "collection.</desc>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BG}"/>',
    ]
    for lon in (9, 10, 11, 12, 13):
        x, _ = project(lon, 49)
        out.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{HEIGHT}" stroke="#eeeeec" stroke-width="1"/>')
    for lat in (48, 49, 50):
        _, y = project(11, lat)
        out.append(f'<line x1="0" y1="{y:.1f}" x2="{WIDTH}" y2="{y:.1f}" stroke="#eeeeec" stroke-width="1"/>')

    for course, width in ((DANUBE, 2.4), (MAIN, 1.8), (LECH, 1.4)):
        out.append(polyline(course, project, width))
    for name, lon, lat, rot in (("Danube", 11.98, 48.87, -8), ("Main", 10.62, 50.06, 0), ("Lech", 10.98, 47.85, 80)):
        x, y = project(lon, lat)
        out.append(text(x, y, name, 9, "#6f8799", extra=f' font-style="italic" transform="rotate({rot} {x:.1f} {y:.1f})"'))

    region_boxes = []
    for name, lon, lat, anchor in REGIONS:
        x, y = project(lon, lat)
        out.append(text(x, y, name.upper(), 8.5, "#888", anchor, ' letter-spacing="0.08em"'))
        width = len(name) * 8.5 * (CHAR_WIDTH + 0.08)
        left = {"start": x, "end": x - width, "middle": x - width / 2}[anchor]
        region_boxes.append((left, y - 8, left + width, y + 2))
    x, y = project(11.70, 48.08)
    out.append(text(x, y, "UPPER BAVARIA", 8.5, "#888", "middle", ' letter-spacing="0.08em"'))
    out.append(text(x, y + 12, "reports not in this collection", 8.5, "#888", "middle"))
    region_boxes.append((x - 80, y - 8, x + 80, y + 14))

    # Palatinate inset
    out.append(f'<rect x="{INSET_X}" y="{INSET_Y}" width="{INSET_W}" height="{INSET_H}" fill="{BG}" stroke="{FRAME}"/>')
    out.append(text(INSET_X + 8, INSET_Y + 14, "PALATINATE", 8.5, "#888", extra=' letter-spacing="0.08em"'))
    out.append(text(INSET_X + 8 + 72, INSET_Y + 14, "same scale", 8.5, "#aaa"))
    out.append(polyline(RHINE, project_inset, 1.8))
    rx, ry = project_inset(8.52, 49.12)
    out.append(text(rx, ry, "Rhine", 9, "#6f8799", extra=f' font-style="italic" transform="rotate(-80 {rx:.1f} {ry:.1f})"'))

    positions: dict[str, tuple[float, float]] = {}
    ringed: set[str] = set()
    for status in DRAW_ORDER:
        for row in rows:
            if row["breastfeeding_status"] != status:
                continue
            lon, lat = float(row["longitude"]), float(row["latitude"])
            x, y = project_inset(lon, lat) if row["regierungsbezirk"] == "Pfalz" else project(lon, lat)
            positions[row["district_id"]] = (x, y)
            color = STATUS[status][0]
            ring = ""
            if row.get("imr_pct_of_births"):
                ringed.add(row["district_id"])
                ring = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="none" stroke="{INK}" stroke-width="1.1"/>'
            if status == "not_documented":
                dot = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{BG}" stroke="#8a8a8a" stroke-width="1.1"/>'
            else:
                dot = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{color}" stroke="{BG}" stroke-width="0.8"/>'
            out.append(f"<g><title>{escape(district_title(row))}</title>{ring}{dot}</g>")

    obstacles = [
        (INSET_X, INSET_Y, INSET_X + INSET_W, INSET_Y + 18),
        (LEGEND_X - 2, LEGEND_Y - 2, LEGEND_X + LEGEND_W + 2, LEGEND_Y + LEGEND_H + 2),
        *region_boxes,
    ]
    points = [(x, y, 7.0 if district_id in ringed else 4.4) for district_id, (x, y) in positions.items()]
    for district_id, label in CALLOUTS:
        x, y = positions[district_id]
        lx, ly, anchor, leader = place_label(x, y, label, points, obstacles)
        if leader:
            out.append(f'<line x1="{leader[0]:.1f}" y1="{leader[1]:.1f}" x2="{leader[2]:.1f}" y2="{leader[3]:.1f}" '
                       f'stroke="{INK}" stroke-width="0.8"/>')
        out.append(text(lx, ly, label, CALLOUT_SIZE, INK, anchor, ' font-weight="500"'))

    out.extend(legend())

    # Scale bar: 50 km along a meridian.
    bar = 50 / 111.2 * SCALE
    sx, sy = PAD + 6, HEIGHT - 16
    out.append(f'<line x1="{sx:.1f}" y1="{sy}" x2="{sx + bar:.1f}" y2="{sy}" stroke="{INK}" stroke-width="1"/>')
    for tick in (sx, sx + bar):
        out.append(f'<line x1="{tick:.1f}" y1="{sy - 3}" x2="{tick:.1f}" y2="{sy + 3}" stroke="{INK}" stroke-width="1"/>')
    out.append(text(sx + bar + 6, sy + 3, "50 km", 9, MUTED))
    out.append("</svg>")
    return "\n".join(out) + "\n"


def render_png(svg_path: Path, png_path: Path) -> bool:
    if not Path(CHROME).exists():
        return False
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "map.html"
        page.write_text(
            f'<!DOCTYPE html><html><body style="margin:0;background:{BG}">{svg_path.read_text()}</body></html>',
            encoding="utf-8",
        )
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
             f"--window-size={WIDTH},{HEIGHT}", f"--screenshot={png_path}", page.as_uri()],
            check=True, capture_output=True,
        )
    return True


def main() -> int:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(build_svg(rows), encoding="utf-8")
    print(f"Rendered {SVG_PATH.relative_to(ROOT)} ({len(rows)} districts)")
    if render_png(SVG_PATH, PNG_PATH):
        print(f"Rendered {PNG_PATH.relative_to(ROOT)}")
    artifact_dir = os.environ.get("ARTIFACT_DIR")
    if artifact_dir and Path(artifact_dir).exists():
        for path in (SVG_PATH, PNG_PATH):
            if path.exists():
                shutil.copy2(path, Path(artifact_dir) / path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
