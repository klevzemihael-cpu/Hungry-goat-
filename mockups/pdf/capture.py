"""Posnetki spletne strani in trgovine za PDF predstavitev (zahteva strežnik na :8080)."""
import subprocess
from pathlib import Path
from PIL import Image
import numpy as np

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = Path(__file__).parent / "shots"
OUT.mkdir(exist_ok=True)
BASE = "http://localhost:8080"


def shot(url, w, h, name):
    png = OUT / f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", "--virtual-time-budget=9000",
                    f"--screenshot={png}", url], capture_output=True)
    return png


def trim(png, crop_w=None, bg=(14, 14, 14)):
    im = Image.open(png).convert("RGB")
    if crop_w:
        im = im.crop((0, 0, crop_w, im.height))
    a = np.asarray(im).astype(int)
    diff = np.abs(a - np.array(bg)).max(axis=2).max(axis=1)
    rows = np.where(diff > 6)[0]
    im = im.crop((0, 0, im.width, int(rows.max()) + 24))
    return im


jobs = [
    ("web-desktop", f"{BASE}/index.html?static", 1440, 9000, None),
    ("web-mobile", f"{BASE}/mockups/pdf/frame.html?src=/index.html%3Fstatic&w=390&h=14000", 600, 14000, 390),
    ("shop-desktop", f"{BASE}/shop.html", 1440, 5000, None),
    ("shop-mobile", f"{BASE}/mockups/pdf/frame.html?src=/shop.html&w=390&h=9000", 600, 9000, 390),
]
for name, url, w, h, cw in jobs:
    png = shot(url, w, h, name)
    im = trim(png, cw)
    im.save(OUT / f"{name}.jpg", quality=88, optimize=True, progressive=True)
    png.unlink()
    print("OK", name, im.size)

# zgornji del trgovine za dokument o obleki
top = Image.open(OUT / "shop-desktop.jpg")
top.crop((0, 0, 1440, min(top.height, 2300))).save(OUT / "shop-desktop-top.jpg", quality=86)
