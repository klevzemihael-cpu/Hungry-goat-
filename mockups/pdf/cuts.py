"""Izračuna reze dolgih posnetkov na mestih, kjer je vrstica enobarvna (med razdelki)."""
import json
from pathlib import Path
from PIL import Image
import numpy as np

SH = Path(__file__).parent / "shots"

def cuts(name, max_h, min_h):
    a = np.asarray(Image.open(SH / f"{name}.jpg").convert("L")).astype(int)
    flat = a.max(axis=1) - a.min(axis=1) < 10          # enobarvne vrstice
    H, out, y = a.shape[0], [0], 0
    while H - y > max_h:
        win = [r for r in range(y + min_h, y + max_h) if flat[r]]
        y = win[-1] if win else y + max_h
        out.append(y)
    out.append(H)
    return out

res = {
    "web-desktop": cuts("web-desktop", 1940, 1300),
    "shop-desktop": cuts("shop-desktop", 1940, 1300),
    "web-mobile": cuts("web-mobile", 1730, 1100),
    "shop-mobile": cuts("shop-mobile", 1730, 1100),
}
(SH / "cuts.json").write_text(json.dumps(res))
print(res)
