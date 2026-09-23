"""Izris HTML/SVG strani v PNG s Chromiumom.

Uporaba:
  python render.py <datoteka.html>[?param] <izhod.png> <širina> <višina> [skala] [--transparent]
"""
import sys, pathlib, os
from playwright.sync_api import sync_playwright

EXE = next((p for p in ["/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                        os.environ.get("CHROME_PATH", "")] if p and os.path.exists(p)), None)


def render(jobs):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=EXE) if EXE else p.chromium.launch(channel="chrome")
        for src, out, w, h, scale, transparent in jobs:
            page = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            path, _, q = src.partition("?")
            url = pathlib.Path(path).resolve().as_uri() + (("?" + q) if q else "")
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(250)
            page.screenshot(path=out, omit_background=transparent, full_page=False)
            page.close()
            print("✓", out)
        b.close()


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    render([(a[0], a[1], int(a[2]), int(a[3]), float(a[4]) if len(a) > 4 else 1, "--transparent" in sys.argv)])
