"""Premium serija: glavni okrogli logotip + metal elementi.  python premium.py → svg/pr-*.svg + tisk/premium/*.png"""
import os, random, base64
from lib import *
from bm import *
from render import render

OUT = os.path.join(HERE, "svg"); PNG = os.path.join(HERE, "tisk", "premium"); os.makedirs(PNG, exist_ok=True)
INTER = Font("Inter", wght=800); INTER6 = Font("Inter", wght=600)
_L = {}


def logo(cx, cy, size, col="white"):
    if col not in _L:
        _L[col] = base64.b64encode(open(os.path.join(HERE, "..", "img", "logo", f"logo-{col}.png"), "rb").read()).decode()
    w, h = size, size * 1606 / 1586
    return f'<image x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" href="data:image/png;base64,{_L[col]}"/>'


def txt(s, width, cx, y, font=INTER, track=380):
    return font.fit(s, width, cx, y, track=track)


def centered(shape, cx, top, maxw=None):
    if maxw and shape.w > maxw:
        shape = shape.scale(maxw / shape.w)
    b = shape.bounds
    return shape.move(cx - (b[0] + b[2]) / 2, top - b[1])


def save(name, w, h, body, dist=None):
    p = os.path.join(OUT, name + ".svg")
    open(p, "w").write(svg_doc(w, h, body, distress=dist))
    return (p, os.path.join(PNG, name + ".png"), w, h, 3600 / w, True)


jobs = []
W = 1000

# 1) SEAL – glavni logotip v dvojnem krogu z metal napisom po obodu
cx, cy, R = 500, 520, 330
rings = ring(cx, cy, R, 10) | ring(cx, cy, R - 26, 3) | ring(cx, cy, R + 70, 3)
top = arc_text(INTER, "STAY HUNGRY  ·  BECOME A GOAT", 34, cx, cy, R + 24, -90, 420)
bot = arc_text(INTER, "TNT GYM  ·  MARIBOR  ·  EST. 2026", 34, cx, cy, R + 50, 90, 420, bottom=True)
stars = star4(cx - R - 38, cy, 16) | star4(cx + R + 38, cy, 16)
line = centered(bm_one_line("HUNGRY GOAT", seed=90, size=150), cx, 960, 760)
body = rings.svg(BONE) + (top | bot).svg(BONE) + stars.svg(ORANGE) + logo(cx, cy, 520) + line.svg(BONE)
jobs.append(save("pr-seal", W, 1200, body))

# 2) OVERSIZED BACK – ogromen logotip, pod njim BECOME A GOAT s kapljami
rng = random.Random(91)
b1, _, _ = metal_line("BECOME A GOAT", 170, 0, 0, rng, lambda x: .5, top_len=(.2, .45), drip_len=(.2, .9), drip_prob=.85)
b1 = centered(roughen(b1, amp=1.8, seed=91), 500, 830, 880)
sub = txt("EST. 2026  ·  MARIBOR  ·  SLOVENIJA", 560, 500, b1.bounds[3] + 80)
body = logo(500, 400, 760) + b1.svg(BONE) + sub.svg(ORANGE)
jobs.append(save("pr-oversized", W, 1250, body))

# 3) NO DAYS OFF – metal napis, majhen pečat zgoraj, drog spodaj
rng = random.Random(92)
n1, _, c = metal_line("NO DAYS", 250, 0, 0, rng, lambda x: .3 + 1.2 * min(1, abs(x) / 480) ** 2, top_len=(.4, .95))
n1 = warp(n1, arch(0, .0003))
n2, _, _ = metal_line("OFF", 330, 0, c + 150, rng, lambda x: .2, top_len=(.2, .4), drip_len=(.15, .5), drip_prob=.9)
nd = centered(roughen(n1 | n2, amp=2, seed=92), 500, 320, 860)
bar = centered(roughen(barbell(0, 0, 820, 120, 12), amp=1.4, seed=93), 500, nd.bounds[3] + 60)
body = logo(500, 160, 230) + nd.svg(BONE) + bar.svg(ORANGE) + txt("365 DAYS A YEAR  ·  HUNGRY GOAT", 560, 500, bar.bounds[3] + 80).svg(BONE)
jobs.append(save("pr-nodays", W, 1400, body))

# 4) PRSNI ZNAK – logotip + tanek napis (spredaj levo)
body = logo(160, 160, 280) + txt("HUNGRY GOAT", 300, 520, 150, INTER, 420).svg(BONE) + txt("STAY HUNGRY · EST. 2026", 300, 520, 200, INTER6, 300).svg(ORANGE)
jobs.append(save("pr-chest", 700, 320, body))

# 5) GOAT GARAGE – logotip na sredini, metal napis v loku zgoraj, rogovi na straneh
rng = random.Random(95)
arc_t, _, _ = metal_line("HUNGRY GOAT", 190, 500, 0, rng, lambda x: .35 + 1.3 * min(1, abs(x - 500) / 520) ** 2, top_len=(.4, 1.0), drip_len=(.05, .25), drip_prob=.3)
arc_t = roughen(warp(arc_t, arch(500, .0006)), amp=1.8, seed=95)
arc_t = centered(arc_t, 500, 60, 900)
lh = engraved_horn([((-20, 0), (-60, -120), (-200, -170), (-280, -80)), ((-280, -80), (-320, -30), (-300, 60), (-240, 90))], 80, 6, rings=18, hatch=4, seed=96)
horns = lh.move(330, 700) | lh.move(330, 700).mirror_x(500)
foot = txt("IRON  ·  SWEAT  ·  DISCIPLINE", 620, 500, 1080)
body = arc_t.svg(BONE) + logo(500, 690, 520) + foot.svg(ORANGE)
jobs.append(save("pr-horns", W, 1200, body))

render(jobs)
print("ok")
