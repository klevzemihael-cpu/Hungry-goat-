"""Pripravi fotografije naslovnic v formatu A4 z že vpečenim temnim prelivom (brez prosojnosti v PDF)."""
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent / "covers"
OUT.mkdir(exist_ok=True)
W, H = 1240, 1754  # A4 pri 150 dpi

COVERS = {  # ključ: (slika, vodoravni fokus 0-1, navpični fokus 0-1)
    "predlog":   ("img/founding.jpg", .30, .40),
    "brief":     ("img/g3.jpg", .45, .35),
    "scenariji": ("img/g4.jpg", .50, .30),
    "trgovina":  ("img/products/stay-outline-black.jpg", .50, .30),
    "web":       ("img/hero.jpg", .55, .30),
    "look":      ("img/products/stay-stack-black.jpg", .50, .25),
}
BG = np.array([14, 14, 14], dtype=np.float32)

for key, (src, fx, fy) in COVERS.items():
    im = Image.open(ROOT / src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - W) * fx); y = round((im.height - H) * fy)
    a = np.asarray(im.crop((x, y, x + W, y + H)), dtype=np.float32)
    t = np.linspace(0, 1, H)[:, None]
    # temnjenje: zgoraj 35 %, do 40 % višine 55 %, od 72 % naprej skoraj polno
    k = np.interp(t, [0, .40, .72, 1], [.35, .55, .97, 1.0])
    a = a * (1 - k[..., None]) + BG * k[..., None]
    Image.fromarray(a.astype(np.uint8)).save(OUT / f"{key}.jpg", quality=86, optimize=True, progressive=True)
    print("OK", key)
