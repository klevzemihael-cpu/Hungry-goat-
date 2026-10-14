"""Priprava fotografij za Instagram: obrez 4:5, zameglitev napisov, barvna obdelava."""
import sys, os
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw

SRC = "slike 2048px/REF_{} - 2048px.JPG"
OUT = sys.argv[1]

# ime: (foto, središče x (0-1), zgornji rob y (0-1), zameglitve [(x0,y0,x1,y1)], topel ton)
JOBS = {
    "4073": ("4073", .50, 0, [], 0),
    "4081": ("4081", .5, .05, [], 0),
    "4011": ("4011", .64, 0, [], 0),
    "4137": ("4137", .32, 0, [(.08, .02, .33, .15)], 1),
    "4055": ("4055", .5, .08, [], 0),
    "4152": ("4152", .5, .08, [(.05, .27, .27, .35)], 1),
    "4005": ("4005", .62, 0, [], 0),
    "4030": ("4030", .62, 0, [], 0),
    "4084": ("4084", .5, .06, [], 0),
    "4077": ("4077", .5, .08, [], 0),
}


def prep(key, foto, cx, y0, blurs, warm):
    im = ImageOps.exif_transpose(Image.open(SRC.format(foto))).convert("RGB")
    W, H = im.size
    for x0, yy0, x1, y1 in blurs:
        box = (int(x0 * W), int(yy0 * H), int(x1 * W), int(y1 * H))
        reg = im.crop(box).filter(ImageFilter.GaussianBlur(28))
        im.paste(reg, box)
    # obrez 4:5
    if W / H > .8:
        cw, ch = int(H * .8), H
        x = int(min(max(cx * W - cw / 2, 0), W - cw)); y = 0
    else:
        cw, ch = W, int(W * 1.25)
        x = 0; y = int(min(max(y0 * H, 0), H - ch))
    im = im.crop((x, y, x + cw, y + ch)).resize((1080, 1350), Image.LANCZOS)
    # obdelava: manj nasičenosti, več kontrasta, rahlo temneje
    im = ImageEnhance.Color(im).enhance(.78 if not warm else .9)
    im = ImageEnhance.Contrast(im).enhance(1.14)
    im = ImageEnhance.Brightness(im).enhance(.93)
    # vinjeta
    v = Image.new("L", (1080, 1350), 0)
    d = ImageDraw.Draw(v)
    for i in range(60):
        t = i / 60
        d.ellipse((-300 + i * 9, -260 + i * 9, 1380 - i * 9, 1610 - i * 9), fill=int(255 * t))
    v = v.filter(ImageFilter.GaussianBlur(80))
    dark = Image.new("RGB", (1080, 1350), (8, 8, 8))
    im = Image.composite(im, dark, v.point(lambda p: 90 + p * 165 // 255))
    im.save(os.path.join(OUT, key + ".jpg"), quality=94)


os.makedirs(OUT, exist_ok=True)
for k, v in JOBS.items():
    prep(k, *v)
# fotografija jope iz Canve (objava 08) je že obdelana
Image.open("img/foto/jopa-model.jpg").convert("RGB").save(os.path.join(OUT, "jopa.jpg"), quality=94)
print("ok", len(JOBS) + 1)
