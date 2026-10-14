"""Vektorizacija logotipov (potrace, prosojno ozadje).

Glavni logotip (okrogli, kozel z monogramom HG; od 14. 10. 2026) ← img/logo/glavni-logotip-vir.png
  Logotipi/glavni-logotip.svg          original: črn krog, kost-bela risba
  Logotipi/glavni-logotip-bela.svg     ena barva, za temne podlage (črni deli so prosojni)
  Logotipi/glavni-logotip-oranzna.svg  ena barva, oranžna, za temne podlage
  Logotipi/glavni-logotip-crna.svg     ena barva, za svetle podlage (beli deli so prosojni)
  Logotipi/glavni-logotip-negativ.svg  kost-bel krog, črna risba
  img/logo/logo-{white,orange,black}.png, img/logo/logo-badge.png (1600 px) za skripte in spletno stran

Stari logotip (kozel s prekrižanimi rokami) ← img/logo/arhiv/stari-logo-white.png → Logotipi/arhiv/
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import potrace

ROOT = Path(__file__).resolve().parent.parent
BONE, BLACK, ORANGE = "#F2EEE6", "#0E0E0E", "#FF5A1F"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


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


def old_logo():
    im = Image.open(ROOT / "img/logo/arhiv/stari-logo-white.png")
    w, h = im.size
    d, n = trace(np.array(im.getchannel("A")) > 127)
    for name, col in [("bela", BONE), ("crna", BLACK), ("oranzna", ORANGE)]:
        (ROOT / f"Logotipi/arhiv/stari-logotip-{name}.svg").write_text(
            svg(w, h, f'<path fill-rule="evenodd" fill="{col}" d="{d}"/>'), encoding="utf-8")
    print("✓ stari logotip", n, "krivulj")


def main_logo():
    src = Image.open(ROOT / "img/logo/glavni-logotip-vir.png").convert("L")
    a = np.array(src)
    ys, xs = np.where(a > 128)
    cx, cy = (xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2
    r = max(xs.max() + 1 - xs.min(), ys.max() + 1 - ys.min()) / 2
    pad = 6
    crop = src.crop((int(cx - r - pad), int(cy - r - pad), int(cx + r + pad), int(cy + r + pad)))
    up = 8
    S = crop.width * up
    big = crop.resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(up * .45))
    m = np.array(big) > 128
    yy, xx = np.mgrid[:S, :S]
    m &= (xx - S / 2) ** 2 + (yy - S / 2) ** 2 <= (r * up) ** 2
    OUT = 1600
    k = OUT / S
    ink, n = trace(m, k)
    c, R = OUT / 2, (r + 2.2) * up * k  # tanek črn rob okoli belega obroča
    disc = f"M{c - R:.1f},{c}A{R:.1f},{R:.1f} 0 1 0 {c + R:.1f},{c}A{R:.1f},{R:.1f} 0 1 0 {c - R:.1f},{c}Z"
    files = {
        "glavni-logotip": f'<path fill="{BLACK}" d="{disc}"/><path fill-rule="evenodd" fill="{BONE}" d="{ink}"/>',
        "glavni-logotip-negativ": f'<path fill="{BONE}" d="{disc}"/><path fill-rule="evenodd" fill="{BLACK}" d="{ink}"/>',
        "glavni-logotip-bela": f'<path fill-rule="evenodd" fill="{BONE}" d="{ink}"/>',
        "glavni-logotip-oranzna": f'<path fill-rule="evenodd" fill="{ORANGE}" d="{ink}"/>',
        "glavni-logotip-crna": f'<path fill-rule="evenodd" fill="{BLACK}" d="{disc}{ink}"/>',
    }
    for name, body in files.items():
        (ROOT / f"Logotipi/{name}.svg").write_text(svg(OUT, OUT, body), encoding="utf-8")
    print("✓ glavni logotip", n, "krivulj")
    return {"logo-badge": "glavni-logotip", "logo-white": "glavni-logotip-bela",
            "logo-orange": "glavni-logotip-oranzna", "logo-black": "glavni-logotip-crna"}


def render_png(pairs, size=1600):
    from playwright.sync_api import sync_playwright
    import os, tempfile
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME) if os.path.exists(CHROME) else p.chromium.launch()
        pg = b.new_page(viewport={"width": size, "height": size})
        for out, name in pairs.items():
            src = ROOT / f"Logotipi/{name}.svg"
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
                t.write(f"<html><body style='margin:0;background:transparent'><img src='{src.as_uri()}' style='width:{size}px;height:{size}px;display:block'></body></html>")
            pg.goto(Path(t.name).as_uri()); pg.wait_for_load_state("networkidle")
            pg.screenshot(path=str(ROOT / f"img/logo/{out}.png"), omit_background=True)
            os.unlink(t.name)
        b.close()
    print("✓ PNG", ", ".join(pairs))


if __name__ == "__main__":
    old_logo()
    render_png(main_logo())
