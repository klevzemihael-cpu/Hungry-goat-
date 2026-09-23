"""Mockupi oblačil (majica spredaj/zadaj, jopa s kozjimi rogovi na kapuci).

python mockups.py  → mock/<ime>.svg + mock/_jobs.json (izris: python render_all.py)
"""
import os, json
from lib import *

MOCK = os.path.join(HERE, "mock")
os.makedirs(MOCK, exist_ok=True)

C = {
    "black":  dict(base="#1b1b1b", inner="#0a0a0a", rib="#222", seam="#2d2d2d", hi=.13, lo=.55, bg=("#F3EFE8", "#D3CCC0"), dark=True),
    "bone":   dict(base="#ECE6DA", inner="#BDB5A6", rib="#E3DCCE", seam="#CEC5B5", hi=.32, lo=.22, bg=("#5E5850", "#262320"), dark=False),
    "orange": dict(base="#F0561E", inner="#A8360C", rib="#E24E18", seam="#C9460F", hi=.22, lo=.32, bg=("#2B2724", "#121110"), dark=False),
    "ash":    dict(base="#6F6A63", inner="#3D3935", rib="#67625B", seam="#5A554F", hi=.2, lo=.38, bg=("#F3EFE8", "#D3CCC0"), dark=True),
}

# ---------- oblike ----------
TEE = "M400,160 C415,205 460,222 500,222 C540,222 585,205 600,160 C650,172 710,186 765,205 C810,280 850,350 885,418 L778,466 C765,440 750,410 738,388 C742,540 746,720 742,888 C600,902 400,902 258,888 C254,720 258,540 262,388 C250,410 235,440 222,466 L115,418 C150,350 190,280 235,205 C290,186 350,172 400,160 Z"
TEE_BACK = "M400,160 C440,176 560,176 600,160 C650,172 710,186 765,205 C810,280 850,350 885,418 L778,466 C765,440 750,410 738,388 C742,540 746,720 742,888 C600,902 400,902 258,888 C254,720 258,540 262,388 C250,410 235,440 222,466 L115,418 C150,350 190,280 235,205 C290,186 350,172 400,160 Z"
TEE_INNER = "M400,160 C440,142 560,142 600,160 C585,205 540,222 500,222 C460,222 415,205 400,160 Z"


def mirror_path(left):
    """Levo polovico (od vrha na sredini do dna na sredini) zrcali v celo obliko."""
    import re
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", left)]
    return nums


# pulover s kapuco – polovica in zrcaljenje z lib.Shape
HOODIE_L = ("M500,296 L402,290 C352,296 302,302 262,322 C222,344 198,404 188,484 "
            "C178,584 168,704 160,812 L152,884 L234,888 L238,814 C246,704 262,584 278,478 "
            "C272,604 268,744 272,852 L270,908 L500,908 Z")


def hoodie_body():
    left = Shape.from_d(HOODIE_L)
    return (left | left.mirror_x(500)).d()


HOOD_FRONT = "M384,306 C346,226 368,112 500,94 C632,112 654,226 616,306 C590,326 410,326 384,306 Z"
HOOD_OPEN = "M424,306 C406,232 432,160 500,150 C568,160 594,232 576,306 C560,330 530,356 500,366 C470,356 440,330 424,306 Z"
HOOD_BACK = "M362,336 C328,236 364,92 500,82 C636,92 672,236 638,336 C590,352 410,352 362,336 Z"

FOLDS = {
    "tee": [
        ("hi", "M440,260 C425,480 445,700 425,870", 70, 34), ("hi", "M600,300 C610,520 590,700 610,860", 50, 30),
        ("hi", "M300,215 C350,232 385,236 425,226", 26, 12), ("hi", "M575,226 C615,236 650,232 700,215", 26, 12),
        ("lo", "M268,395 C315,425 350,468 372,528", 16, 9), ("lo", "M732,395 C685,425 650,468 628,528", 16, 9),
        ("lo", "M205,300 C230,338 248,378 256,412", 14, 9), ("lo", "M795,300 C770,338 752,378 744,412", 14, 9),
        ("lo", "M292,845 C372,822 420,862 482,846", 12, 8), ("lo", "M530,852 C592,830 652,864 712,842", 12, 8),
        ("lo", "M500,560 C492,640 505,720 496,800", 30, 26),
        ("edge", "M262,388 C258,540 254,720 258,888", 46, 26), ("edge", "M738,388 C742,540 746,720 742,888", 46, 26),
    ],
    "hoodie": [
        ("hi", "M430,380 C418,560 440,720 424,860", 70, 34), ("hi", "M590,400 C604,560 584,720 604,850", 56, 30),
        ("hi", "M215,420 C205,560 200,700 190,800", 26, 16), ("hi", "M785,420 C795,560 800,700 810,800", 26, 16),
        ("lo", "M262,330 C252,400 252,440 262,480", 18, 12), ("lo", "M738,330 C748,400 748,440 738,480", 18, 12),
        ("lo", "M300,835 C380,815 430,852 490,838", 14, 9), ("lo", "M520,842 C590,822 650,856 710,836", 14, 9),
        ("lo", "M200,640 C215,660 230,668 246,664", 10, 8), ("lo", "M800,640 C785,660 770,668 754,664", 10, 8),
        ("lo", "M190,760 C205,778 222,784 240,780", 10, 8), ("lo", "M810,760 C795,778 778,784 760,780", 10, 8),
        ("edge", "M278,478 C272,604 268,744 272,852", 40, 24), ("edge", "M722,478 C728,604 732,744 728,852", 40, 24),
    ],
}


def defs(bg):
    return f"""<defs>
  <radialGradient id="bg" cx=".5" cy=".42" r=".78"><stop offset="0" stop-color="{bg[0]}"/><stop offset="1" stop-color="{bg[1]}"/></radialGradient>
  <filter id="b10" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1400" height="1400"><feGaussianBlur stdDeviation="10"/></filter>
  <filter id="b28" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1400" height="1400"><feGaussianBlur stdDeviation="26"/></filter>
  <filter id="b4" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1400" height="1400"><feGaussianBlur stdDeviation="3.5"/></filter>
  <filter id="fabric" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="1.5" numOctaves="2" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 1.4 -.35"/>
  </filter>
  <filter id="fleece" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="11" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 1.6 -.45"/>
  </filter>
  <filter id="warp" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="2" seed="9" result="w"/>
    <feDisplacementMap in="SourceGraphic" in2="w" scale="8" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <linearGradient id="hornshade" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity=".45"/>
  </linearGradient>
  <linearGradient id="interior" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#1a1a1a"/>
  </linearGradient>
</defs>"""


_uid = [0]


def uid(p):
    _uid[0] += 1
    return f"{p}{_uid[0]}"


def shading(kind, c, shape_d):
    clip, lg, vg = uid("clip"), uid("lg"), uid("vg")
    dark = c["dark"]
    s = f"""<defs><clipPath id="{clip}"><path d="{shape_d}"/></clipPath>
    <linearGradient id="{lg}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity="{.55 if dark else .3}"/>
      <stop offset=".22" stop-color="#000" stop-opacity="0"/><stop offset=".78" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity="{.6 if dark else .34}"/></linearGradient>
    <linearGradient id="{vg}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="{.07 if dark else .16}"/>
      <stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="{.25 if dark else .16}"/></linearGradient></defs>"""
    g = f'<g clip-path="url(#{clip})">'
    for t, d, w, b in FOLDS[kind]:
        blur = "b28" if b > 20 else "b10"
        if t == "hi":
            g += f'<path d="{d}" stroke="#fff" stroke-width="{w}" fill="none" stroke-linecap="round" opacity="{c["hi"]}" filter="url(#{blur})" style="mix-blend-mode:screen"/>'
        else:
            op = c["lo"] if t == "lo" else c["lo"] * .9
            g += f'<path d="{d}" stroke="#000" stroke-width="{w}" fill="none" stroke-linecap="round" opacity="{op}" filter="url(#{blur})" style="mix-blend-mode:multiply"/>'
    g += f'<rect width="1000" height="1000" fill="url(#{lg})" style="mix-blend-mode:multiply"/>'
    g += f'<rect width="1000" height="1000" fill="url(#{vg})"/>'
    tex = "fleece" if kind == "hoodie" else "fabric"
    g += f'<rect width="1000" height="1000" filter="url(#{tex})" opacity="{.16 if dark else .2}" style="mix-blend-mode:{"screen" if dark else "multiply"}"/>'
    return s, clip, g


def img(href, x, y, w, h):
    return f'<image href="{href}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>'


# ---------- majica ----------
def tee(col, prints="", back=False):
    c = C[col]
    shape = TEE_BACK if back else TEE
    s = f'<path d="{shape}" fill="#000" opacity="{.28 if c["dark"] else .4}" filter="url(#b28)" transform="translate(0,22)"/>'
    if not back:
        s += f'<path d="{TEE_INNER}" fill="{c["inner"]}"/><rect x="484" y="150" width="32" height="14" rx="2" fill="{ORANGE}"/>'
    s += f'<path d="{shape}" fill="{c["base"]}"/>'
    d, clip, g = shading("tee", c, shape)
    s += d + f'<g clip-path="url(#{clip})"><g filter="url(#warp)">{prints}</g>' + g[g.index(">") + 1:] + "</g>"
    for p in ["M600,160 C650,172 710,186 765,205", "M400,160 C350,172 290,186 235,205",
              "M765,205 C745,260 735,330 738,388", "M235,205 C255,260 265,330 262,388"]:
        s += f'<path d="{p}" stroke="{c["seam"]}" stroke-width="2.4" fill="none" opacity=".9"/>'
    for p in ["M870,398 L766,444", "M130,398 L234,444", "M262,864 C400,877 600,877 738,864"]:
        s += f'<path d="{p}" stroke="{c["seam"]}" stroke-width="2" stroke-dasharray="7 6" fill="none"/>'
    if back:
        s += f'<path d="M400,160 C440,176 560,176 600,160" stroke="{c["rib"]}" stroke-width="16" fill="none"/>'
    else:
        s += (f'<path d="M400,160 C415,205 460,222 500,222 C540,222 585,205 600,160" stroke="{c["rib"]}" stroke-width="20" fill="none"/>'
              f'<path d="M405,172 C420,212 462,230 500,230 C538,230 580,212 595,172" stroke="{c["seam"]}" stroke-width="2" stroke-dasharray="6 5" fill="none"/>')
    return s


# ---------- rogovi na kapuci ----------
HORN_COL = {"bone": ("#E9E1D0", "#8F8471"), "black": ("#262422", "#070707"), "orange": ("#FF6A2E", "#9E330A")}


def hood_horns(col, back=False, cx=500, base_y=150, spread=176, style="curl", k=.60, w0=92):
    """3D rogova iz filca/umetnega usnja, prišita na vrh kapuce."""
    light, dark = HORN_COL[col]
    segs, w = HORN_STYLES[style]
    ox = cx - spread / 2
    segs = [tuple((ox + x * k, base_y + y * k) for x, y in seg) for seg in segs]
    body = horn(segs, w0 * k, 5 * k, ridge=False)
    cut = horn(segs, w0 * k, 5 * k, ridges=10, groove=1.5)
    pair_body = body | body.mirror_x(cx)
    pair_cut = cut | cut.mirror_x(cx)
    hid = uid("horn")
    s = f'<defs><clipPath id="{hid}"><path d="{pair_body.d()}"/></clipPath></defs>'
    # senca na kapuci
    s += f'<path d="{pair_body.d()}" fill="#000" opacity=".35" filter="url(#b10)" transform="translate(6,14)"/>'
    s += pair_body.svg(dark)
    s += pair_cut.svg(light)
    s += f'<g clip-path="url(#{hid})"><rect x="0" y="0" width="1000" height="400" fill="url(#hornshade)" opacity=".9"/>'
    # šiv ob korenu
    s += f'<rect x="0" y="{base_y - 14}" width="1000" height="40" fill="#000" opacity=".25" filter="url(#b4)"/></g>'
    # obroba koren/kapuca
    s += f'<ellipse cx="{ox}" cy="{base_y + 4}" rx="{32*k}" ry="8" fill="#000" opacity=".35" filter="url(#b4)"/>'
    s += f'<ellipse cx="{2*cx-ox}" cy="{base_y + 4}" rx="{32*k}" ry="8" fill="#000" opacity=".35" filter="url(#b4)"/>'
    return s


# ---------- jopa ----------
def hoodie(col, horn_col, prints="", back=False):
    c = C[col]
    body = hoodie_body()
    s = f'<path d="{body}" fill="#000" opacity="{.28 if c["dark"] else .4}" filter="url(#b28)" transform="translate(0,22)"/>'
    hood = HOOD_BACK if back else HOOD_FRONT
    s += f'<path d="{hood}" fill="#000" opacity=".3" filter="url(#b28)" transform="translate(0,16)"/>'
    s += f'<path d="{body}" fill="{c["base"]}"/>'
    d, clip, g = shading("hoodie", c, body)
    s += d + f'<g clip-path="url(#{clip})"><g filter="url(#warp)">{prints if back else ""}</g>' + g[g.index(">") + 1:] + "</g>"
    # rebra: manšete in pas
    for x0, x1 in ((152, 234), (766, 848)):
        s += f'<path d="M{x0+4},{818} L{x1},{820} L{x1-2},{886} L{x0},{882} Z" fill="{c["rib"]}"/>'
        for i in range(1, 9):
            xx = x0 + (x1 - x0) * i / 9
            s += f'<path d="M{xx+2},{820} L{xx},{884}" stroke="#000" stroke-opacity=".18" stroke-width="1.6"/>'
        s += f'<path d="M{x0+4},{818} L{x1},{820}" stroke="{c["seam"]}" stroke-width="3"/>'
    s += f'<path d="M272,852 C400,862 600,862 728,852 L730,908 L270,908 Z" fill="{c["rib"]}"/>'
    for i in range(1, 46):
        xx = 272 + 456 * i / 46
        s += f'<path d="M{xx},857 L{xx},906" stroke="#000" stroke-opacity=".16" stroke-width="1.6"/>'
    s += f'<path d="M272,852 C400,862 600,862 728,852" stroke="{c["seam"]}" stroke-width="3" fill="none"/>'
    s += f'<path d="M272,908 L728,908" stroke="#000" stroke-opacity=".25" stroke-width="3"/>'
    # rokavi – šiv ob ramenu
    s += f'<path d="M262,322 C250,380 262,440 278,478" stroke="{c["seam"]}" stroke-width="2.4" fill="none"/>'
    s += f'<path d="M738,322 C750,380 738,440 722,478" stroke="{c["seam"]}" stroke-width="2.4" fill="none"/>'
    if not back:
        # žep kenguru
        s += (f'<path d="M360,640 L640,640 L694,752 L700,846 M360,640 L306,752 L300,846" stroke="{c["seam"]}" stroke-width="3" fill="none"/>'
              f'<path d="M362,646 L308,756 L304,846" stroke="#000" stroke-opacity=".35" stroke-width="10" fill="none" filter="url(#b4)"/>'
              f'<path d="M638,646 L692,756 L696,846" stroke="#000" stroke-opacity=".35" stroke-width="10" fill="none" filter="url(#b4)"/>'
              f'<path d="M366,650 L634,650" stroke="{c["seam"]}" stroke-width="2" stroke-dasharray="6 5" fill="none"/>')
        s += f'<g filter="url(#warp)">{prints}</g>'
    # kapuca
    s += f'<g transform="translate(500,312) scale(1.13) translate(-500,-312)">{hood_part(c, back)}{hood_horns(horn_col, back)}</g>'
    if not back:
        # vrvici
        for x0, x1, x2 in ((466, 452, 446), (534, 548, 556)):
            s += f'<circle cx="{x0}" cy="344" r="6" fill="#8a8a8a" stroke="#555" stroke-width="2"/>'
            s += f'<path d="M{x0},344 C{x0-2},400 {x1},460 {x2},540" stroke="{c["rib"] if c["dark"] else "#fff"}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            s += f'<path d="M{x0},344 C{x0-2},400 {x1},460 {x2},540" stroke="#000" stroke-opacity=".25" stroke-width="9" fill="none" stroke-linecap="round" transform="translate(2,3)" filter="url(#b4)"/>'
            s += f'<rect x="{x2-5}" y="536" width="10" height="26" rx="3" fill="{ORANGE}"/>'
    return s


def hood_part(c, back):
    if back:
        hid = uid("hb")
        s = f'<path d="{HOOD_BACK}" fill="{c["base"]}"/>'
        s += (f'<defs><clipPath id="{hid}"><path d="{HOOD_BACK}"/></clipPath></defs><g clip-path="url(#{hid})">'
              f'<path d="M420,120 C400,200 404,280 420,330" stroke="#fff" stroke-width="50" opacity="{c["hi"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:screen"/>'
              f'<path d="M640,140 C660,220 660,300 640,340" stroke="#000" stroke-width="50" opacity="{c["lo"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:multiply"/>'
              f'<path d="M362,336 C328,236 364,92 500,82" stroke="#000" stroke-width="40" opacity="{c["lo"]*.8}" fill="none" filter="url(#b28)"/>'
              f'<rect width="1000" height="400" filter="url(#fleece)" opacity="{.16 if c["dark"] else .2}" style="mix-blend-mode:{"screen" if c["dark"] else "multiply"}"/></g>')
        s += f'<path d="M500,84 L500,344" stroke="{c["seam"]}" stroke-width="3"/>'
        s += f'<path d="M506,90 L506,342" stroke="{c["seam"]}" stroke-width="1.6" stroke-dasharray="6 5"/>'
        return s
    hid = uid("hf")
    s = f'<path d="{HOOD_FRONT}" fill="{c["base"]}"/>'
    s += (f'<defs><clipPath id="{hid}"><path d="{HOOD_FRONT}"/></clipPath></defs><g clip-path="url(#{hid})">'
          f'<path d="M395,300 C370,220 390,140 470,108" stroke="#fff" stroke-width="40" opacity="{c["hi"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:screen"/>'
          f'<path d="M610,300 C634,220 614,150 560,110" stroke="#000" stroke-width="40" opacity="{c["lo"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:multiply"/>'
          f'<rect width="1000" height="400" filter="url(#fleece)" opacity="{.16 if c["dark"] else .2}" style="mix-blend-mode:{"screen" if c["dark"] else "multiply"}"/></g>')
    # notranjost kapuce
    s += f'<path d="{HOOD_OPEN}" fill="{c["inner"]}"/>'
    s += f'<path d="M438,300 C424,236 446,176 500,168 C554,176 576,236 562,300 C548,322 526,340 500,348 C474,340 452,322 438,300 Z" fill="url(#interior)" opacity=".92"/>'
    # rob kapuce (dvojni šiv) in prekrivanje na vratu
    s += f'<path d="{HOOD_OPEN}" fill="none" stroke="{c["rib"]}" stroke-width="12"/>'
    s += f'<path d="M430,308 C414,236 438,166 500,158 C562,166 586,236 570,308" fill="none" stroke="{c["seam"]}" stroke-width="1.8" stroke-dasharray="6 5"/>'
    s += f'<path d="M424,306 C446,330 470,350 512,370" stroke="{c["seam"]}" stroke-width="3" fill="none"/>'
    return s


# ---------- sestavljanje ----------
def scene(garment_svg, col, w=1000, h=1000, fit=None):
    bg = C[col]["bg"]
    g = f'<g transform="{fit}">{garment_svg}</g>' if fit else garment_svg
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{defs(bg)}'
            f'<rect width="{w}" height="{h}" fill="url(#bg)"/>'
            f'<ellipse cx="500" cy="950" rx="300" ry="24" fill="#000" opacity=".2" filter="url(#b28)"/>'
            f'{g}</svg>')


HOODIE_FIT = "translate(95,158) scale(.81)"


def P(name, way):
    return f"../svg/{name}-{way}.svg"


JOBS = []


def save(name, svg, col):
    p = os.path.join(MOCK, name + ".svg")
    open(p, "w").write(svg)
    JOBS.append((p, 1000, 1000, col))


# motiv za hrbet: 1000×1200 → 400 široko na hrbtu majice
def back_print(name, way, x=300, y=240, w=400):
    return img(P(name, way), x, y, w, w * 1.2)


def chest(name, way, cx=632, cy=300, w=120):
    return f'<g>{img(P(name, way), cx - w / 2, cy - w / 2, w, w)}</g>'


def logo_on(col_ink, cx, cy, size):
    c = {"bone": "white", "black": "black", "orange": "orange"}[col_ink]
    return img(f"../../img/logo/logo-{c}.png", cx - size / 2, cy - size / 2 * 1.013, size, size * 1.013)


if __name__ == "__main__":
    TEES = [
        ("stay-hungry-metal", "black"), ("earn-your-horns", "black"), ("heavy-metal", "bone"),
        ("grind-tour", "black"), ("feed-the-beast", "bone"), ("never-full", "black"),
        ("ostani-lacen", "bone"), ("goat-acronym", "orange"),
    ]
    for name, col in TEES:
        save(f"tee-{name}-{col}-back", scene(tee(col, back_print(name, col), back=True), col), col)
    # sprednje strani
    save("tee-front-metal-black", scene(tee("black", chest("chest-metal", "black", 600, 300, 150)), "black"), "black")
    save("tee-front-kb-bone", scene(tee("bone", chest("icon-kettlebell", "bone", 630, 300, 110)), "bone"), "bone")
    save("tee-front-wordmark-orange", scene(tee("orange", chest("wordmark", "orange", 500, 330, 330)), "orange"), "orange")
    # jope
    H = [("black", "bone", "earn-your-horns", "black", "logo"), ("bone", "black", "stay-hungry-metal", "bone", "kb"),
         ("orange", "black", "heavy-metal", "orange", "logo"), ("ash", "orange", "never-full", "black", "kb")]
    for col, hc, name, way, front in H:
        ink = "bone" if C[col]["dark"] else "black"
        fr = logo_on(ink, 612, 430, 92) if front == "logo" else chest("icon-kettlebell", "black" if C[col]["dark"] else "bone", 612, 430, 92)
        save(f"hoodie-{col}-front", scene(hoodie(col, hc, fr), col, fit=HOODIE_FIT), col)
        save(f"hoodie-{col}-back", scene(hoodie(col, hc, back_print(name, way, 320, 390, 360), back=True), col, fit=HOODIE_FIT), col)
    json.dump(JOBS, open(os.path.join(MOCK, "_jobs.json"), "w"))
    print(len(JOBS), "mockupov")
