"""Hiter predogled: python quick.py izhod.png svg1 svg2 ... (izris kot dokument, z vgnezdenimi slikami)."""
import sys, os
from PIL import Image
from render import render
out, files = sys.argv[1], sys.argv[2:]
tmp = [out + f".{i}.png" for i in range(len(files))]
render([(f, t, 1000, 1000, .6, False) for f, t in zip(files, tmp)])
ims = [Image.open(t) for t in tmp]
cols = min(4, len(ims)); rows = -(-len(ims) // cols)
w, h = ims[0].size
sheet = Image.new("RGB", (w * cols, h * rows), "#555")
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out)
for t in tmp: os.remove(t)
