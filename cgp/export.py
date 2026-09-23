"""Izvoz: tiskovine (PNG 3600 px, prosojno), logotipi (PNG 3000 px), mockupi (JPG 2000 px).

python export.py            → vse
python export.py mock       → samo mockupi
"""
import os, sys, json, glob
from PIL import Image
from render import render

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tisk")
MOCK_OUT = os.path.join(HERE, "mockupi")
os.makedirs(OUT, exist_ok=True)
os.makedirs(MOCK_OUT, exist_ok=True)

sys.path.insert(0, HERE)
from designs import REG  # noqa: E402


def svg_size(p):
    import re
    head = open(p).read(400)
    w = float(re.search(r'width="([\d.]+)"', head).group(1))
    h = float(re.search(r'height="([\d.]+)"', head).group(1))
    return int(w), int(h)


def export_prints():
    jobs = []
    for p in sorted(glob.glob(os.path.join(HERE, "svg", "*.svg"))):
        name = os.path.basename(p)[:-4]
        base = name.rsplit("-", 1)[0]
        kind = REG[base][1] if base in REG else "logo"
        w, h = svg_size(p)
        target = 3600 if kind == "back" else 3000
        jobs.append((p, os.path.join(OUT, name + ".png"), w, h, target / w, True))
    render(jobs)


def export_mock():
    jobs = []
    tmp = []
    for p in sorted(glob.glob(os.path.join(HERE, "mock", "*.svg"))):
        name = os.path.basename(p)[:-4]
        png = os.path.join(MOCK_OUT, name + ".png")
        jobs.append((p, png, 1000, 1000, 2, False))
        tmp.append(png)
    render(jobs)
    for png in tmp:
        Image.open(png).convert("RGB").save(png[:-4] + ".jpg", quality=90, optimize=True, progressive=True)
        os.remove(png)


if __name__ == "__main__":
    what = sys.argv[1:] or ["prints", "mock"]
    if "prints" in what:
        export_prints()
    if "mock" in what:
        export_mock()
