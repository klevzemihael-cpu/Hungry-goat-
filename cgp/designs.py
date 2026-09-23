"""CGP Hungry Goat – napisni logotipi, znaki in tiskovine za majice/jope.

python designs.py [ime ...]   → svg/<ime>-<barva>.svg (+ seznam za izris)
"""
import sys, os, json, math
from lib import *

OUT = os.path.join(HERE, "svg")
os.makedirs(OUT, exist_ok=True)

ANTON = Font("Anton-Regular")
FRAK = Font("UnifrakturCook-Bold")
PIRATA = Font("PirataOne-Regular")
GRENZE = Font("GrenzeGotisch", wght=900)
INTER = Font("Inter", wght=800)
INTER_M = Font("Inter", wght=600)
STAAT = Font("Staatliches-Regular")
OSW = Font("Oswald", wght=700)

REG = {}


def design(name, kind):
    def deco(fn):
        REG[name] = (fn, kind)
        return fn
    return deco


# barvne kombinacije: (ozadje oblačila, primarna, poudarek)
WAYS = {
    "black": (BLACK, BONE, ORANGE),
    "bone": (BONE, BLACK, ORANGE),
    "orange": (ORANGE, BLACK, BONE),
}


def fitted(items, pad=40):
    """Samodejno obreže platno okoli oblik. items: [(Shape, barva)]."""
    xs = [s.bounds for s, _ in items if len(s.p)]
    x0 = min(b[0] for b in xs); y0 = min(b[1] for b in xs)
    x1 = max(b[2] for b in xs); y1 = max(b[3] for b in xs)
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    body = "".join(s.move(pad - x0, pad - y0).svg(c) for s, c in items)
    return round(w), round(h), body


def placed(items):
    return "".join(s if isinstance(s, str) else s.svg(c) for s, c in items if isinstance(s, str) or len(s.p))


_LOGO = {}


def logo_img(cx, cy, size, ink):
    """Originalni okrogli logotip (ostane nespremenjen) – vdelan v SVG."""
    import base64
    col = {BONE: "white", BLACK: "black", ORANGE: "orange"}[ink]
    if col not in _LOGO:
        _LOGO[col] = base64.b64encode(open(os.path.join(HERE, "..", "img", "logo", f"logo-{col}.png"), "rb").read()).decode()
    w, h = size, size * 1606 / 1586
    return f'<image x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" href="data:image/png;base64,{_LOGO[col]}"/>'


# ======================================================================
#  NAPISNI LOGOTIPI
# ======================================================================
def goat_word(size, x, y, anchor="middle", track=8, horns=True, font=None, style="sweep", k=1.0):
    """'GOAT' z rogovi, ki zrastejo iz črke O. Vrne (črke, rogovi)."""
    f = font or ANTON
    glyphs, adv = f.layout("GOAT", size, 0, y, track)
    dx = {"start": 0, "middle": -adv / 2, "end": -adv}[anchor] + x
    letters = union(*[g.move(dx, 0) for _, g in glyphs])
    hp = Shape()
    if horns:
        o = glyphs[1][1].move(dx, 0).bounds
        ocx, top, ow = (o[0] + o[2]) / 2, o[1], o[2] - o[0]
        hp = horn_pair(ocx, top + ow * .22, ow * .80, scale=ow / 200 * .58 * k, style=style, ridges=7, w0=74)
        letters = letters - hp.stroked(ow * .075)
    return letters, hp


def wordmark_line(size=200, track=8, horns=True):
    hungry = ANTON.text("HUNGRY", size, 0, 0, "start", track)
    gap = size * .22
    gl, gh = goat_word(size, hungry.bounds[2] + gap, 0, "start", track, horns)
    return hungry, gl, gh


@design("wordmark", "logo")
def d_wordmark(bg, ink, acc):
    h, g, horns = wordmark_line()
    return fitted([(h, ink), (g, ink), (horns, acc)], pad=60)


@design("wordmark-stacked", "logo")
def d_wordmark_stacked(bg, ink, acc):
    W = 900
    hungry = ANTON.fit("HUNGRY", W, 0, 0, track=30)
    gl, gh = goat_word(100, 0, 0, "middle", 6)
    k = W / gl.w
    gl2, gh2 = goat_word(100 * k, 0, 0, "middle", 6, k=.9)
    gy = hungry.bounds[3] + 36 + (gl2.bounds[1] - gh2.bounds[1]) - gl2.bounds[1]
    gl2, gh2 = gl2.move(0, gy), gh2.move(0, gy)
    ty = gl2.bounds[3] + 58
    tag = INTER.fit("STAY HUNGRY. BECOME A GOAT.", W * .74, 0, ty, track=260)
    mid = tag.bounds[1] + tag.h / 2
    left = poly([(-W / 2, mid), (-W * .40, mid - 5), (-W * .40, mid + 5)])
    return fitted([(hungry, ink), (gl2, ink), (gh2, acc), (tag, acc), (left, acc), (left.mirror_x(0), acc)], pad=70)


@design("wordmark-metal", "logo")
def d_wordmark_metal(bg, ink, acc):
    size = 300
    t = FRAK.text("Hungry Goat", size, 0, 0, "middle", 4)
    b = t.bounds
    ol = t.outline(12, 9)
    y = b[3] + size * .16
    L = (b[2] - b[0]) / 2 + size * .15
    bl = union(poly([(-L, y), (-size * .30, y - 8), (-size * .30, y + 8)]),
               poly([(L, y), (size * .30, y - 8), (size * .30, y + 8)]),
               diamond(0, y, 34))
    est = INTER.fit("EST. 2026", size * .62, 0, 0, track=500)
    est = est.move(0, y + 44 - est.bounds[1])
    mb = INTER.fit("MARIBOR · SLOVENIJA", size * .62 * 1.5, 0, 0, track=500)
    return fitted([(ol, acc), (t, ink), (bl, acc), (est, ink)], pad=70)


@design("monogram", "logo")
def d_monogram(bg, ink, acc):
    s = 420
    hg = FRAK.text("HG", s, 0, 0, "middle", -20)
    b = hg.bounds
    cy = (b[1] + b[3]) / 2
    R = s * .78
    hp = horn_pair(0, b[1] + s * .02, s * .46, scale=s / 300, style="ram", ridges=8, w0=58)
    rings = ring(0, cy, R, 16) | ring(0, cy, R + 30, 7)
    top = arc_text(INTER, "HUNGRY GOAT", 34, 0, cy, R - 62, -90, 420)
    bot = arc_text(INTER, "EST. 2026", 34, 0, cy, R - 62 + 26, 90, 420, bottom=True)
    return fitted([(rings - hp.stroked(34), ink), (hp, acc), (hg - hp.stroked(14), ink)], pad=60)


def kb_shape(r):
    body = circle(0, 0, r) - rect(-r * 1.2, r * .84, r * 2.4, r)
    outer = Shape.from_d(f"M{-r*.80},{-r*.25} L{-r*.80},{-r*1.05} C{-r*.80},{-r*1.52} {-r*.52},{-r*1.62} 0,{-r*1.62} "
                         f"C{r*.52},{-r*1.62} {r*.80},{-r*1.52} {r*.80},{-r*1.05} L{r*.80},{-r*.25} Z")
    inner = Shape.from_d(f"M{-r*.53},{-r*.25} L{-r*.53},{-r*1.02} C{-r*.53},{-r*1.30} {-r*.34},{-r*1.36} 0,{-r*1.36} "
                         f"C{r*.34},{-r*1.36} {r*.53},{-r*1.30} {r*.53},{-r*1.02} L{r*.53},{-r*.25} Z")
    return (outer - inner) | body


@design("icon-kettlebell", "logo")
def d_kb(bg, ink, acc):
    r = 220
    kb = kb_shape(r)
    hp = horn_pair(0, -r * 1.12, r * 1.62, scale=r / 205, style="ram", ridges=8, w0=62)
    hg = ANTON.fit("HG", r * .78, 0, r * .46, track=30)
    return fitted([(kb - hp.stroked(r * .08) - hg, ink), (hp, acc)], pad=60)


# ======================================================================
#  TISKOVINE (1000 × 1200, hrbet; 1000 × 600 prsi)
# ======================================================================
W, H = 1000, 1200


def back(items, dist="mid"):
    return W, H, placed(items), dist


def hline(x1, x2, y, t):
    return rect(x1, y - t / 2, x2 - x1, t)


def blade_rule(cx, y, half, t=7, gem=20):
    l = poly([(cx - half, y), (cx - gem * 1.2, y - t), (cx - gem * 1.2, y + t)])
    return l | l.mirror_x(cx) | diamond(cx, y, gem)


def frak_c_caron(text, size, x, y, anchor="middle", track=0):
    """UnifrakturCook nima č – dodamo strešico nad c (znak '^' v besedilu pomeni č)."""
    plain = text.replace("^", "c")
    glyphs, adv = FRAK.layout(plain, size, 0, y, track)
    dx = {"start": 0, "middle": -adv / 2, "end": -adv}[anchor] + x
    out = union(*[g.move(dx, 0) for _, g in glyphs])
    for i, ch in enumerate(text):
        if ch == "^":
            b = glyphs[i][1].move(dx, 0).bounds
            cx = (b[0] + b[2]) / 2 + size * .02
            out = out | caron(cx, b[1] - size * .03, size * .20, size * .12, size * .06)
    return out


# ---- 1. STAY HUNGRY (metal) ----
@design("stay-hungry-metal", "back")
def p_stay(bg, ink, acc):
    top = INTER.fit("HUNGRY GOAT  ·  DROP 02  ·  MARIBOR", 640, W / 2, 150, track=300)
    r1 = blade_rule(W / 2, 205, 330, 5, 14)
    stay = FRAK.fit("Stay", 520, W / 2, 470)
    hungry = FRAK.fit("Hungry", 860, W / 2, 745)
    words = stay | hungry
    ol = words.outline(12, 10)
    bag = ANTON.fit("BECOME A GOAT.", 820, W / 2, 925, track=40)
    bar = rect(90, 950, 820, 14)
    sub = INTER.fit("OSTANI LAČEN  ·  POSTANI GOAT", 600, W / 2, 1030, track=320)
    return back([(top, ink), (r1, acc), (ol, acc), (words, ink), (bag, acc), (bar, ink), (sub, ink),
                 (logo_img(W / 2, 1115, 105, ink), None)])


# ---- 2. EARN YOUR HORNS ----
@design("earn-your-horns", "back")
def p_earn(bg, ink, acc):
    hp = horn_pair(W / 2, 330, 250, scale=1.42, style="ram", ridges=10, w0=74)
    earn = ANTON.fit("EARN", 330, W / 2, 400, track=20)
    your = ANTON.fit("YOUR", 330, W / 2, 470 + 20 + earn.h * 0.52, track=20)
    your = your.move(0, earn.bounds[3] + 22 - your.bounds[1])
    horns = ANTON.fit("HORNS", 700, W / 2, 0, track=10)
    horns = horns.move(0, your.bounds[3] + 26 - horns.bounds[1])
    txt = earn | your | horns
    tag = FRAK.fit("Hungry Goat", 420, W / 2, 0)
    tag = tag.move(0, horns.bounds[3] + 60 - tag.bounds[1])
    rule = blade_rule(W / 2, tag.bounds[3] + 48, 300, 5, 13)
    loc = INTER.fit("TRAINING CLUB  ·  MARIBOR  ·  EST. 2026", 620, W / 2, 0, track=300)
    loc = loc.move(0, rule.bounds[3] + 34 - loc.bounds[1])
    return back([(hp - txt.stroked(26), acc), (txt, ink), (tag, acc), (rule, ink), (loc, ink)])


# ---- 3. HEAVY METAL CLUB ----
@design("heavy-metal", "back")
def p_heavy(bg, ink, acc):
    cx, cy = W / 2, 560
    R = 420
    rings = ring(cx, cy, R, 14) | ring(cx, cy, R - 30, 5)
    heavy = FRAK.fit("Heavy", 440, cx, 0)
    heavy = heavy.move(0, cy - 62 - heavy.bounds[3])
    metal = FRAK.fit("Metal", 440, cx, 0)
    metal = metal.move(0, cy + 70 - metal.bounds[1])
    bb = barbell(cx, cy, 880, 190, 16)
    words = heavy | metal
    top = arc_text(INTER, "HUNGRY GOAT BARBELL CLUB", 40, cx, cy, R - 76, -90, 330)
    bot = arc_text(INTER, "EST. 2026  ·  MARIBOR", 40, cx, cy, R - 76 + 30, 90, 330, bottom=True)
    s1 = star4(cx - 300, cy + 190, 18); s2 = star4(cx + 300, cy + 190, 18)
    knock = bb.stroked(22)
    return back([(rings - knock, ink), (words - knock, ink), (bb, acc), (top | bot, ink), (s1 | s2, acc)], "mid")


# ---- 4. THE GRIND TOUR ----
@design("grind-tour", "back")
def p_tour(bg, ink, acc):
    head = FRAK.fit("Hungry Goat", 800, W / 2, 200)
    ol = head.outline(9, 7)
    t1 = ANTON.fit("THE GRIND TOUR", 800, W / 2, 350, track=30)
    yr = ANTON.fit("2026", 260, W / 2, 0, track=60)
    yr = yr.move(0, t1.bounds[3] + 26 - yr.bounds[1])
    rows = [("MON", "CHEST DAY", "TNT GYM"), ("TUE", "BACK DAY", "TNT GYM"), ("WED", "LEG DAY", "TNT GYM"),
            ("THU", "SHOULDERS", "TNT GYM"), ("FRI", "ARMS", "TNT GYM"), ("SAT", "LEG DAY AGAIN", "TNT GYM"),
            ("SUN", "REST DAY", "SOLD OUT")]
    items = []
    y = yr.bounds[3] + 80
    for i, (d, what, where) in enumerate(rows):
        c = acc if i == 6 else ink
        items.append((OSW.text(d, 48, 110, y, "start", 60), acc))
        items.append((OSW.text(what, 48, 270, y, "start", 40), c))
        items.append((OSW.text(where, 48, 890, y, "end", 40), c))
        if i < 6:
            items.append((rect(110, y + 24, 780, 2.5), ink))
        y += 74
    foot = INTER.fit("NO CANCELLED SHOWS  ·  NO DAYS OFF", 700, W / 2, y + 16, track=300)
    return back([(ol, acc), (head, ink), (t1, ink), (yr, acc)] + items + [(foot, ink)], "light")


# ---- 5. FEED THE BEAST ----
@design("feed-the-beast", "back")
def p_feed(bg, ink, acc):
    r = 215
    ky = 690
    kb = kb_shape(r).move(W / 2, ky)
    hp = horn_pair(0, -r * 1.12, r * 1.62, scale=r / 205, style="ram", ridges=9, w0=62).move(W / 2, ky)
    hg = ANTON.fit("HG", r * .78, W / 2, ky + r * .46, track=30)
    feed = FRAK.fit("Feed the Beast", 860, W / 2, 230)
    ol = feed.outline(10, 8)
    sub = ANTON.fit("HUNGRY GOAT  —  NEVER FULL", 700, W / 2, 1040, track=60)
    rule = blade_rule(W / 2, 1090, 340, 5, 13)
    loc = INTER.fit("MARIBOR  ·  SLOVENIJA", 440, W / 2, 1150, track=360)
    return back([(ol, acc), (feed, ink), (kb - hp.stroked(r * .08) - hg, ink), (hp, acc), (sub, ink), (rule, acc), (loc, ink)])


# ---- 6. NEVER FULL (plasti) ----
@design("never-full", "back")
def p_never(bg, ink, acc):
    never = ANTON.fit("NEVER", 900, W / 2, 560, track=10)
    full = ANTON.fit("FULL.", 900, W / 2, 0, track=10)
    full = full.move(0, never.bounds[3] + 28 - full.bounds[1])
    script = FRAK.fit("Hungry Goat", 800, 0, 0).rotate(-9)
    b = script.bounds
    script = script.move(W / 2 - (b[0] + b[2]) / 2, (never.bounds[3] + full.bounds[1]) / 2 - (b[1] + b[3]) / 2 + 10)
    knock = script.stroked(34)
    top = INTER.fit("HUNGRY GOAT ATHLETICS", 560, W / 2, 130, track=380)
    num = ANTON.fit("No. 02", 150, W / 2, 0)
    foot = INTER.fit("STAY HUNGRY. BECOME A GOAT.", 640, W / 2, full.bounds[3] + 90, track=320)
    return back([(top, ink), ((never | full) - knock, ink), (script, acc), (foot, ink)], "heavy")


# ---- 7. OSTANI LAČEN ----
@design("ostani-lacen", "back")
def p_ostani(bg, ink, acc):
    o = frak_c_caron("Ostani la^en.", 250, 0, 0)
    k = 860 / o.w
    o = frak_c_caron("Ostani la^en.", 250 * k, W / 2, 0)
    o = o.move(0, 560 - o.bounds[3])
    ol = o.outline(10, 8)
    p2 = ANTON.fit("POSTANI GOAT.", 860, W / 2, 0, track=30)
    p2 = p2.move(0, o.bounds[3] + 60 - p2.bounds[1])
    rule = blade_rule(W / 2, p2.bounds[3] + 60, 380, 6, 15)
    loc = INTER.fit("MARIBOR  ·  SLOVENIJA  ·  2026", 620, W / 2, rule.bounds[3] + 60, track=320)
    return back([(logo_img(W / 2, o.bounds[1] - 150, 220, ink), None), (ol, acc), (o, ink), (p2, ink), (rule, acc), (loc, ink)])


# ---- 8. G.O.A.T. ----
@design("goat-acronym", "back")
def p_goat(bg, ink, acc):
    glyphs, adv = ANTON.layout("G.O.A.T.", 100, 0, 0, 10)
    k = 880 / union(*[s for _, s in glyphs]).w
    glyphs, adv = ANTON.layout("G.O.A.T.", 100 * k, 0, 660, 10)
    g = union(*[s for _, s in glyphs])
    g = g.move(W / 2 - (g.bounds[0] + g.bounds[2]) / 2, 0)
    ob = glyphs[2][1].move(W / 2 - (union(*[s for _, s in glyphs]).bounds[0] + union(*[s for _, s in glyphs]).bounds[2]) / 2, 0).bounds
    ow = ob[2] - ob[0]
    hpo = horn_pair((ob[0] + ob[2]) / 2, ob[1] + ow * .30, ow * .60, scale=ow / 200 * .9, style="curl", ridges=7, w0=70)
    hpo = Shape()
    ol = g.outline(10, 8)
    rows = ["GREATEST", "OF ALL", "TIME"]
    items = []
    y = g.bounds[3] + 80
    words = INTER.fit("GREATEST  OF  ALL  TIME", 880, W / 2, y, track=300)
    tag = FRAK.fit("Hungry Goat", 560, W / 2, 0)
    tag = tag.move(0, g.bounds[1] - 70 - tag.bounds[3])
    lg = logo_img(W / 2, tag.bounds[1] - 150, 200, ink)
    foot = blade_rule(W / 2, words.bounds[3] + 60, 400, 6, 15)
    return back([(lg, None), (tag, ink), (g, ink), (ol, acc), (words, acc), (foot, ink)])


# ---- prsni motivi (1000 × 1000) ----
def chest(items, dist=None):
    w, h, body = fitted(items, pad=30)
    return w, h, body, dist


@design("chest-metal", "chest")
def c_metal(bg, ink, acc):
    t = FRAK.text("Hungry Goat", 300, 0, 0)
    return chest([(t.outline(10, 8), acc), (t, ink)])


@design("chest-stay", "chest")
def c_stay(bg, ink, acc):
    t = FRAK.fit("Stay Hungry", 900, 0, 0)
    s = INTER.fit("BECOME A GOAT.", 560, 0, 0, track=460)
    s = s.move(0, t.bounds[3] + 50 - s.bounds[1])
    return chest([(t, ink), (s, acc)])


def render_named(name, way):
    fn, kind = REG[name]
    bg, ink, acc = WAYS[way]
    r = fn(bg, ink, acc)
    if len(r) == 3:
        w, h, body = r; dist = None
    else:
        w, h, body, dist = r
    if os.environ.get("CLEAN"):
        dist = None
    svg = svg_doc(w, h, body, distress=dist, seed=sum(map(ord, name)) % 97)
    p = os.path.join(OUT, f"{name}-{way}.svg")
    open(p, "w").write(svg)
    return p, w, h, kind


if __name__ == "__main__":
    names = sys.argv[1:] or list(REG)
    jobs = []
    ways = [w for w in ("black", "bone", "orange") if os.environ.get("WAYS", "black,bone").find(w) >= 0]
    for n in names:
        for way in ways:
            p, w, h, kind = render_named(n, way)
            jobs.append((p, w, h, way))
            print(n, way, w, h)
    json.dump(jobs, open(os.path.join(OUT, "_jobs.json"), "w"))
