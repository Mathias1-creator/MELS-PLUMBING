#!/usr/bin/env python3
"""
Generate the 10 on-brand placeholder plates in images/.

These stand in for stock/client photography. Each plate is a technical
line drawing in the MELS PLUMBING palette, rendered by headless Chromium
and saved as a real JPEG at the same dimensions the final photo should be.

Replacing a placeholder with a real photo is a straight file swap — keep the
filename, keep roughly the aspect ratio, and nothing else has to change.

Usage:  python3 tools/generate-placeholder-images.py
Needs:  Pillow, and a Chromium/Chrome binary (set CHROME= to override).
"""

import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "images")

GREEN_DEEP = "#12291C"
GREEN = "#1E4632"
GREEN_SOFT = "#2E6147"
SILVER = "#B9C2C6"

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("google-chrome") or "",
]


def find_chrome():
    for path in CHROME_CANDIDATES:
        if path and os.path.exists(path):
            return path
    sys.exit("No Chromium binary found. Set CHROME=/path/to/chrome and retry.")


# ---------------------------------------------------------------------------
# Drawing helpers — every scene is built from pipe runs and fittings
# ---------------------------------------------------------------------------

def pipe(d, width=20, opacity=0.82):
    """A pipe run: solid body plus a thin inner highlight for roundness."""
    return (
        f'<path d="{d}" fill="none" stroke="{SILVER}" stroke-opacity="{opacity}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" '
        f'stroke-width="{max(2, width * 0.22):.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def collar(x, y, r=17, opacity=0.75):
    """A coupling/collar at a joint."""
    return (
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{SILVER}" '
        f'stroke-opacity="{opacity}" stroke-width="7"/>'
    )


def valve(x, y, r=34):
    """A gate valve: wheel plus spokes."""
    return (
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{SILVER}" stroke-opacity="0.85" stroke-width="8"/>'
        f'<circle cx="{x}" cy="{y}" r="{r * 0.32:.0f}" fill="none" stroke="{SILVER}" stroke-opacity="0.85" stroke-width="7"/>'
        f'<path d="M{x - r} {y} H{x + r} M{x} {y - r} V{y + r}" stroke="{SILVER}" '
        f'stroke-opacity="0.6" stroke-width="6" stroke-linecap="round"/>'
    )


def outline(d, width=7, opacity=0.7):
    return (
        f'<path d="{d}" fill="none" stroke="{SILVER}" stroke-opacity="{opacity}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------

def scene_hero():
    """Rough-in: a run of supply lines, elbows, a gate valve and a gauge."""
    return "".join([
        pipe("M120 980 V620 Q120 560 180 560 H820", 30),
        collar(120, 800, 24), collar(520, 560, 24),
        pipe("M820 560 Q880 560 880 500 V180", 30),
        collar(880, 340, 24),
        pipe("M300 1050 V820 Q300 760 360 760 H1180 Q1240 760 1240 700 V300", 26),
        collar(720, 760, 21), collar(1240, 480, 21),
        pipe("M1480 1080 V420 Q1480 360 1540 360 H1900", 26),
        collar(1480, 760, 21),
        valve(880, 180, 46),
        # pressure gauge
        f'<circle cx="1240" cy="240" r="62" fill="none" stroke="{SILVER}" stroke-opacity="0.8" stroke-width="9"/>',
        f'<circle cx="1240" cy="240" r="46" fill="none" stroke="{SILVER}" stroke-opacity="0.4" stroke-width="4"/>',
        outline("M1240 240 L1276 206", 8, 0.9),
        f'<circle cx="1240" cy="240" r="8" fill="{SILVER}" fill-opacity="0.9"/>',
        # wall studs behind
        outline("M640 0 V1250 M1720 0 V1250", 3, 0.13),
    ])


def scene_remodel():
    """Bathroom vanity elevation: mirror, basin, faucet, P-trap."""
    return "".join([
        outline("M300 120 H900 V440 H300 Z", 7, 0.35),          # mirror
        outline("M330 150 L560 150", 4, 0.18),
        outline("M240 540 H960 V585 H240 Z", 7, 0.75),          # counter
        outline("M420 585 H780 Q800 585 795 610 L760 690 Q752 712 730 712 H470 "
                "Q448 712 440 690 L405 610 Q400 585 420 585 Z", 7, 0.8),  # basin
        pipe("M600 400 V470 Q600 440 640 440 H700", 16),        # faucet
        collar(600, 470, 13),
        outline("M540 500 V540 M660 500 V540", 6, 0.6),         # handles
        pipe("M600 712 V800 Q600 850 650 850 Q700 850 700 800 V740 "
             "Q700 700 740 700 H960", 18),                       # P-trap
        collar(600, 780, 15),
        outline("M240 900 H960", 3, 0.2),
    ])


def scene_repair():
    """Leak repair: pipe with a union, a wrench on it, and drips below."""
    return "".join([
        pipe("M80 420 H1120", 34),
        collar(560, 420, 30, 0.9),
        outline("M520 380 H600 V460 H520 Z", 7, 0.85),
        # wrench
        outline("M700 300 Q640 300 640 360 Q640 420 700 420 L700 380 "
                "Q680 380 680 360 Q680 340 700 340 Z", 8, 0.85),
        pipe("M700 360 L1000 660", 22, 0.7),
        # drips
        f'<path d="M560 500 q-22 40 0 58 q22 -18 0 -58 Z" fill="{SILVER}" fill-opacity="0.65"/>',
        f'<path d="M540 640 q-16 30 0 43 q16 -13 0 -43 Z" fill="{SILVER}" fill-opacity="0.4"/>',
        f'<path d="M588 700 q-12 22 0 32 q12 -10 0 -32 Z" fill="{SILVER}" fill-opacity="0.28"/>',
        outline("M120 820 H1080", 3, 0.18),
    ])


def scene_maintenance():
    """Water heater: tank, T&P valve, seismic straps, drain hose."""
    return "".join([
        outline("M380 200 H820 V760 H380 Z", 8, 0.8),
        outline("M380 200 q220 -45 440 0", 8, 0.8),
        outline("M380 760 q220 45 440 0", 8, 0.5),
        pipe("M470 200 V90", 20), pipe("M730 200 V90", 20),
        collar(470, 150, 15), collar(730, 150, 15),
        outline("M380 340 H820 M380 560 H820", 8, 0.6),        # straps
        pipe("M820 300 H960 Q1000 300 1000 340 V420", 16),     # T&P
        valve(1000, 470, 32),
        pipe("M380 700 H300 Q260 700 260 740 V860", 16),       # drain
        collar(260, 800, 13),
        outline("M300 900 H1000", 3, 0.18),
        outline("M560 430 H700 M560 480 H660", 5, 0.3),        # label plate
        outline("M540 400 H720 V510 H540 Z", 4, 0.35),
    ])


def scene_bath_finished():
    """Finished bathroom: vanity, mirror, tile field."""
    tiles = "".join(
        f'<path d="M{x} 60 V520" stroke="{SILVER}" stroke-opacity="0.10" stroke-width="3"/>'
        for x in range(120, 1140, 120)
    ) + "".join(
        f'<path d="M60 {y} H1140" stroke="{SILVER}" stroke-opacity="0.10" stroke-width="3"/>'
        for y in range(120, 540, 120)
    )
    return tiles + "".join([
        outline("M380 130 H820 V430 H380 Z", 8, 0.45),
        outline("M180 560 H1020 V610 H180 Z", 8, 0.8),
        outline("M480 610 H720 L690 760 H510 Z", 7, 0.8),
        pipe("M600 430 V500 Q600 470 636 470 H690", 15),
        outline("M520 520 V560 M680 520 V560", 6, 0.55),
        pipe("M600 760 V820 Q600 860 640 860 Q680 860 680 820 V790", 16),
        outline("M180 880 H1020", 3, 0.2),
    ])


def scene_water_heater_2():
    """Water heater install, wider view with expansion tank."""
    return "".join([
        outline("M300 240 H700 V780 H300 Z", 8, 0.8),
        outline("M300 240 q200 -42 400 0", 8, 0.8),
        pipe("M390 240 V120 H620", 20),
        pipe("M620 120 Q680 120 680 180 V240", 20),
        collar(390, 180, 15), collar(680, 200, 15),
        outline("M300 380 H700 M300 600 H700", 8, 0.6),
        f'<ellipse cx="900" cy="300" rx="90" ry="70" fill="none" stroke="{SILVER}" '
        f'stroke-opacity="0.75" stroke-width="8"/>',
        pipe("M900 370 V470 H700", 16),
        collar(820, 470, 13),
        pipe("M300 720 H200 V800", 16),
        valve(200, 838, 28),
        outline("M120 890 H1080", 3, 0.18),
    ])


def scene_copper_run():
    """Copper supply lines running through studs."""
    studs = "".join(
        f'<path d="M{x} 40 V860" stroke="{SILVER}" stroke-opacity="0.22" stroke-width="10"/>'
        for x in (200, 520, 840, 1160)
    )
    return studs + "".join([
        pipe("M60 300 H1140", 22),
        pipe("M60 520 H900 Q960 520 960 460 V240", 22),
        collar(200, 300, 17), collar(520, 300, 17), collar(840, 300, 17),
        collar(200, 520, 17), collar(520, 520, 17),
        collar(960, 340, 17),
        outline("M180 270 H220 V330 H180 Z", 5, 0.5),
        outline("M500 490 H540 V550 H500 Z", 5, 0.5),
        pipe("M300 700 H1140", 18, 0.55),
        collar(520, 700, 14), collar(840, 700, 14),
    ])


def scene_faucet():
    """Modern gooseneck kitchen faucet."""
    return "".join([
        pipe("M600 720 V420 Q600 250 760 250 Q900 250 900 400 V470", 26),
        collar(600, 600, 21),
        outline("M540 720 H660 V760 H540 Z", 7, 0.8),
        pipe("M480 640 Q420 640 420 700 V730", 16),
        outline("M380 730 H460", 8, 0.7),
        outline("M240 800 H1000 L960 900 H280 Z", 8, 0.75),
        outline("M300 850 H940", 4, 0.25),
        f'<circle cx="900" cy="500" r="9" fill="{SILVER}" fill-opacity="0.55"/>',
        f'<circle cx="900" cy="545" r="7" fill="{SILVER}" fill-opacity="0.35"/>',
        f'<circle cx="900" cy="585" r="5" fill="{SILVER}" fill-opacity="0.22"/>',
    ])


def scene_shower_valve():
    """Bathroom remodel: shower riser, valve body and tub spout on a tiled wall."""
    tiles = "".join(
        f'<path d="M{x} 60 V840" stroke="{SILVER}" stroke-opacity="0.09" stroke-width="3"/>'
        for x in range(120, 1140, 120)
    ) + "".join(
        f'<path d="M60 {y} H1140" stroke="{SILVER}" stroke-opacity="0.09" stroke-width="3"/>'
        for y in range(140, 860, 120)
    )
    return tiles + "".join([
        pipe("M600 600 V300 Q600 250 650 250 H780", 22),      # riser up to the shower arm
        collar(600, 440, 18),
        outline("M770 218 H880 V282 H770 Z", 8, 0.85),        # shower head
        outline("M790 282 V322 M825 282 V332 M860 282 V322", 5, 0.4),
        outline("M510 590 H690 V730 H510 Z", 8, 0.8),         # valve trim plate
        f'<circle cx="600" cy="660" r="44" fill="none" stroke="{SILVER}" '
        f'stroke-opacity="0.85" stroke-width="8"/>',
        outline("M600 660 L634 632", 7, 0.9),                 # handle
        pipe("M600 730 V800 Q600 830 640 830 H690", 20),      # drop to the tub spout
        collar(600, 780, 15),
        outline("M690 810 H780 L768 852 H690 Z", 7, 0.8),     # spout
        outline("M260 880 H1060", 4, 0.22),                   # tub rim
    ])


def scene_kitchen():
    """Finished kitchen sink from above: double basin, faucet, supply lines."""
    return "".join([
        outline("M180 240 H1020 V700 H180 Z", 8, 0.75),
        outline("M240 300 H570 V640 H240 Z", 7, 0.6),
        outline("M630 300 H960 V640 H630 Z", 7, 0.6),
        f'<circle cx="405" cy="470" r="26" fill="none" stroke="{SILVER}" stroke-opacity="0.7" stroke-width="7"/>',
        f'<circle cx="795" cy="470" r="26" fill="none" stroke="{SILVER}" stroke-opacity="0.7" stroke-width="7"/>',
        pipe("M600 240 V150 Q600 100 540 100 H420", 20),
        collar(600, 190, 16),
        pipe("M405 700 V800 Q405 850 460 850 H700 Q760 850 760 800 V740", 18),
        collar(405, 770, 14),
        pipe("M795 700 V790", 16),
        outline("M120 160 H1080", 3, 0.16),
    ])


# ---------------------------------------------------------------------------
# Image manifest
# ---------------------------------------------------------------------------

# ONLY the slots that still hold placeholders.
#
# Do NOT add hero.jpg or the three service-*.jpg entries back. The hero is a
# solid green gradient with no photo at all, and the service images hold real
# client photos — regenerating them would overwrite the client's work with
# placeholder art. The scene_hero/remodel/repair/maintenance functions are kept
# below only so the earlier plates can be rebuilt by hand if ever needed.
IMAGES = [
    ("gallery-1.jpg", 1200, 900, "Bathroom remodel", scene_bath_finished),
    ("gallery-2.jpg", 1200, 900, "Water heater install", scene_water_heater_2),
    ("gallery-3.jpg", 1200, 900, "Copper pipe run", scene_copper_run),
    ("gallery-4.jpg", 1200, 900, "Kitchen faucet", scene_faucet),
    ("gallery-5.jpg", 1200, 900, "Shower valve set", scene_shower_valve),
    ("gallery-6.jpg", 1200, 900, "Finished kitchen", scene_kitchen),
]


def build_html(width, height, label, scene_svg, tone="dark"):
    """Wrap a scene in the shared plate: gradient, grid, pipe motif, grain, label.

    tone="light" is for the hero, which sits under a deep-green scrim on the
    site — a dark plate would vanish under it.
    """
    vb_w, vb_h = (2000, 1250) if width > 1400 else (1200, 900)
    label_size = round(vb_w / 55)
    if tone == "light":
        stops = (GREEN_SOFT, GREEN, GREEN_DEEP)
        vignette = "0.28"
    else:
        stops = (GREEN, GREEN_DEEP, GREEN_DEEP)
        vignette = "0.45"

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  html,body {{ margin:0; padding:0; width:{width}px; height:{height}px; overflow:hidden; background:{GREEN_DEEP}; }}
  svg {{ display:block; width:{width}px; height:{height}px; }}
  text {{ font-family: "DejaVu Sans", "Liberation Sans", Arial, Helvetica, sans-serif; }}
</style></head><body>
<svg viewBox="0 0 {vb_w} {vb_h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{stops[0]}"/>
      <stop offset="55%" stop-color="{stops[1]}"/>
      <stop offset="100%" stop-color="{stops[2]}"/>
    </linearGradient>
    <radialGradient id="glow" cx="28%" cy="24%" r="78%">
      <stop offset="0%" stop-color="#2E6147" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#2E6147" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="{vb_w / 24:.2f}" height="{vb_w / 24:.2f}" patternUnits="userSpaceOnUse">
      <path d="M {vb_w / 24:.2f} 0 L 0 0 0 {vb_w / 24:.2f}" fill="none"
            stroke="{SILVER}" stroke-opacity="0.055" stroke-width="1.5"/>
    </pattern>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
    <radialGradient id="vig" cx="50%" cy="50%" r="72%">
      <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="{vignette}"/>
    </radialGradient>
  </defs>

  <rect width="100%" height="100%" fill="url(#bg)"/>
  <rect width="100%" height="100%" fill="url(#glow)"/>
  <rect width="100%" height="100%" fill="url(#grid)"/>

  <g>{scene_svg}</g>

  <rect width="100%" height="100%" fill="url(#vig)"/>
  <rect width="100%" height="100%" filter="url(#grain)" opacity="0.11"/>

  <g opacity="0.62">
    <path d="M{vb_w * 0.045:.0f} {vb_h - 84} h{vb_w * 0.09:.0f}" stroke="{SILVER}" stroke-width="3"/>
    <circle cx="{vb_w * 0.045:.0f}" cy="{vb_h - 84}" r="7" fill="none" stroke="{SILVER}" stroke-width="3"/>
  </g>
  <text x="{vb_w * 0.045:.0f}" y="{vb_h - 40}" fill="{SILVER}" fill-opacity="0.85"
        font-size="{label_size}" letter-spacing="{label_size * 0.18:.1f}"
        font-weight="600">PLACEHOLDER &#183; {label.upper()}</text>
</svg>
</body></html>
"""


def main():
    chrome = find_chrome()
    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="mels-img-")
    failures = []

    for name, width, height, label, scene in IMAGES:
        html_path = os.path.join(tmp, name.replace(".jpg", ".html"))
        png_path = os.path.join(tmp, name.replace(".jpg", ".png"))
        jpg_path = os.path.join(OUT_DIR, name)

        tone = "light" if name == "hero.jpg" else "dark"
        with open(html_path, "w") as fh:
            fh.write(build_html(width, height, label, scene(), tone))

        # Headless reserves some window height for chrome, which would clip the
        # bottom of the plate. Render taller than needed, then crop off the slack:
        # the SVG is pinned to the top-left at an exact pixel size.
        cmd = [
            chrome, "--headless", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={width},{height + 240}",
            f"--screenshot={png_path}",
            "file://" + html_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if not os.path.exists(png_path):
            failures.append(f"{name}: chromium produced no PNG\n{result.stderr[-400:]}")
            continue

        with Image.open(png_path) as im:
            im.convert("RGB").crop((0, 0, width, height)).save(
                jpg_path, "JPEG", quality=88, optimize=True, progressive=True
            )

        size_kb = os.path.getsize(jpg_path) / 1024
        with Image.open(jpg_path) as check:
            dims = check.size
        status = "ok" if size_kb > 30 and dims == (width, height) else "CHECK"
        if status == "CHECK":
            failures.append(f"{name}: {dims[0]}x{dims[1]}, {size_kb:.0f}KB")
        print(f"  {status:5} {name:26} {dims[0]}x{dims[1]}  {size_kb:6.1f} KB")

    shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("\nProblems:")
        for line in failures:
            print("  - " + line)
        sys.exit(1)
    print(f"\nAll {len(IMAGES)} placeholder images generated.")


if __name__ == "__main__":
    main()
