"""Vektorizacija okroglih logotipov v Logotipi/*.svg (prosojno ozadje).

- glavni-logotip-*.svg  ← img/logo/logo-white.png (alfa kanal)
- logotip-hg-*.svg      ← img/logo/logo-hg-vir.png (okrogli logotip z monogramom HG, ki ga je poslal uporabnik)
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import potrace

ROOT = Path(__file__).resolve().parent.parent
BONE, BLACK, ORANGE = "#F2EEE6", "#0E0E0E", "#FF5A1F"


def trace(mask, k=1.0):
    # potrace.Bitmap podatke obrne, zato mu podamo negativ maske
    path = potrace.Bitmap(~mask).trace(turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.2)
    f = lambda p: f"{p.x * k:.2f},{p.y * k:.2f}"
    out = []
    for curve in path:
        d = ["M" + f(curve.start_point)]
        for seg in curve.segments:
            d.append(f"L{f(seg.c)}L{f(seg.end_point)}" if seg.is_corner else f"C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}")
        out.append("".join(d) + "Z")
    return "".join(out), len(path)


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>\n'


def main_logo():
    im = Image.open(ROOT / "img/logo/logo-white.png")
    w, h = im.size
    d, n = trace(np.array(im.getchannel("A")) > 127)
    for name, col in [("bela", BONE), ("crna", BLACK), ("oranzna", ORANGE)]:
        (ROOT / f"Logotipi/glavni-logotip-{name}.svg").write_text(
            svg(w, h, f'<path fill-rule="evenodd" fill="{col}" d="{d}"/>'), encoding="utf-8")
    print("✓ glavni logotip", n, "krivulj")


def hg_logo():
    src = Image.open(ROOT / "img/logo/logo-hg-vir.png").convert("L")
    a = np.array(src)
    ys, xs = np.where(a > 128)
    cx, cy = (xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2
    r = max(xs.max() + 1 - xs.min(), ys.max() + 1 - ys.min()) / 2
    pad = 6
    box = (int(cx - r - pad), int(cy - r - pad), int(cx + r + pad), int(cy + r + pad))
    crop = src.crop(box)
    up = 8
    S = crop.width * up
    big = crop.resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(up * .45))
    m = np.array(big) > 128
    yy, xx = np.mgrid[:S, :S]
    m &= (xx - S / 2) ** 2 + (yy - S / 2) ** 2 <= (r * up) ** 2
    OUT = 2000
    k = OUT / S
    d, n = trace(m, k)
    R = (r + 2.2) * up * k  # tanek črn rob okoli belega obroča
    c = OUT / 2
    for name, ring, ink in [("crn", BLACK, BONE), ("negativ", BONE, BLACK), ("oranzen", BLACK, ORANGE)]:
        (ROOT / f"Logotipi/logotip-hg-{name}.svg").write_text(
            svg(OUT, OUT, f'<circle cx="{c}" cy="{c}" r="{R:.1f}" fill="{ring}"/><path fill-rule="evenodd" fill="{ink}" d="{d}"/>'),
            encoding="utf-8")
    print("✓ logotip HG", n, "krivulj")


if __name__ == "__main__":
    main_logo()
    hg_logo()
