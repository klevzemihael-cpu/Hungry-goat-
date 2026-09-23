"""Black metal napis HUNGRY GOAT: gotska osnova + konice, kaplje, trni in hrapav rob.

Vse je vektor (pathops). Naključnost je vezana na seme, zato je rezultat ponovljiv.
"""
import math, random
import pathops
from fontTools.pens.basePen import BasePen
from lib import *


# ---------- poligoni ----------
class FlatPen(BasePen):
    """Pretvori krivulje v poligone (seznam kontur s točkami)."""

    def __init__(self, step=3.0):
        super().__init__(None)
        self.step = step
        self.contours = []
        self.cur = None

    def _moveTo(self, p):
        self.cur = [p]
        self.contours.append(self.cur)

    def _lineTo(self, p):
        a = self.cur[-1]
        n = max(1, int(math.dist(a, p) / self.step))
        for i in range(1, n + 1):
            t = i / n
            self.cur.append((a[0] + (p[0] - a[0]) * t, a[1] + (p[1] - a[1]) * t))

    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        ln = math.dist(p0, p1) + math.dist(p1, p2) + math.dist(p2, p3)
        n = max(2, int(ln / self.step))
        for i in range(1, n + 1):
            self.cur.append(lib_bez(p0, p1, p2, p3, i / n))

    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        n = max(2, int((math.dist(p0, p1) + math.dist(p1, p2)) / self.step))
        for i in range(1, n + 1):
            t = i / n; u = 1 - t
            self.cur.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                             u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))

    def _closePath(self):
        if self.cur and len(self.cur) > 1 and math.dist(self.cur[0], self.cur[-1]) < 1e-6:
            self.cur.pop()


def lib_bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def flatten(shape, step=3.0):
    pen = FlatPen(step)
    shape.p.draw(pen)
    return [c for c in pen.contours if len(c) > 2]


def from_contours(contours):
    p = pathops.Path()
    for c in contours:
        p.moveTo(*c[0])
        for q in c[1:]:
            p.lineTo(*q)
        p.close()
    return Shape(pathops.simplify(p))


# ---------- hrapav rob ----------
class Noise1D:
    def __init__(self, rng, n=4096):
        self.v = [rng.uniform(-1, 1) for _ in range(n)]
        self.n = n

    def __call__(self, x):
        i = int(math.floor(x)); f = x - i
        a = self.v[i % self.n]; b = self.v[(i + 1) % self.n]
        f = f * f * (3 - 2 * f)
        return a + (b - a) * f

    def fbm(self, x, oct=4):
        s, amp, fr = 0, 1, 1
        for _ in range(oct):
            s += amp * self(x * fr); amp *= .5; fr *= 2.03
        return s


def roughen(shape, amp=2.4, freq=.09, nick=.05, seed=1, step=2.2):
    """Razbrazda robove: fraktalni šum vzdolž normale + občasne zareze."""
    rng = random.Random(seed)
    nz = Noise1D(rng)
    out = []
    s = 0.0
    for c in flatten(shape, step):
        n = len(c)
        pts = []
        for i, (x, y) in enumerate(c):
            a = c[i - 1]; b = c[(i + 1) % n]
            tx, ty = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(tx, ty) or 1
            nx, ny = ty / ln, -tx / ln
            s += 1
            d = nz.fbm(s * freq) * amp
            if rng.random() < nick:
                d -= rng.uniform(.8, 2.2) * amp
            pts.append((x + nx * d, y + ny * d))
        out.append(pts)
    return from_contours(out)


# ---------- konice in kaplje ----------
def spike_shape(x0, x1, yb, h, lean=0.0, curve=.18, up=True):
    """Koničast trn iz osnove [x0,x1] na višini yb, dolžine h (navzgor ali navzdol)."""
    sgn = -1 if up else 1
    xm = (x0 + x1) / 2
    tip = (xm + lean, yb + sgn * h)
    w = x1 - x0
    p = pathops.Path()
    p.moveTo(x0, yb - sgn * w * .35)
    p.lineTo(x0, yb)
    p.quadTo(x0 + w * curve + lean * .35, yb + sgn * h * .55, *tip)
    p.quadTo(x1 - w * curve + lean * .35, yb + sgn * h * .55, x1, yb)
    p.lineTo(x1, yb - sgn * w * .35)
    p.close()
    return Shape(p)


def thorn(x, y, length, width, angle):
    a = math.radians(angle)
    tx, ty = x + math.cos(a) * length, y + math.sin(a) * length
    nx, ny = -math.sin(a) * width / 2, math.cos(a) * width / 2
    return poly([(x + nx - math.cos(a) * width, y + ny - math.sin(a) * width), (tx, ty),
                 (x - nx - math.cos(a) * width, y - ny - math.sin(a) * width)])


def drip(x, y, w, length, rng):
    """Kaplja: rahlo valovit curek z odebeljenim koncem."""
    pts_l, pts_r = [], []
    n = 16
    wob = rng.uniform(-.25, .25) * w
    for i in range(n + 1):
        t = i / n
        ww = w * (1 - .55 * t ** .7) / 2
        cx = x + wob * math.sin(t * math.pi)
        yy = y + length * t
        pts_l.append((cx - ww, yy)); pts_r.append((cx + ww, yy))
    body = poly([(x - w / 2, y - w * .6)] + pts_l + pts_r[::-1] + [(x + w / 2, y - w * .6)])
    end = circle(x + wob * 0, y + length, w * rng.uniform(.34, .46))
    return body | end


def clusters(points, key, band, gap):
    """Skupine točk ob robu (npr. vrh ali dno črke) → [(x0, x1, y)]."""
    sel = sorted([p for p in points if key(p) <= band], key=lambda p: p[0])
    out = []
    for p in sel:
        if out and p[0] - out[-1][1] <= gap:
            out[-1][1] = p[0]
            out[-1][2].append(p[1])
        else:
            out.append([p[0], p[0], [p[1]]])
    return [(a, b, ys) for a, b, ys in out]


def metalize(glyph, cap, rng, top=True, bottom=True, top_len=(.25, .9), drip_len=(.15, .75),
             drip_prob=.6, thorns=True, profile=None, maxw=.075, bottom_len=(.2, .6)):
    """Doda tanke konice na vrhove debel in kaplje/konice na dno.
    profile(x) → množitelj dolžine konice (za simetrično silhueto)."""
    b = glyph.bounds
    pts = [p for c in flatten(glyph, 2.0) for p in c]
    parts = [glyph]
    prof = profile or (lambda x: 1.0)
    if top:
        for x0, x1, ys in clusters(pts, lambda p: p[1] - b[1], cap * .06, cap * .04):
            w = x1 - x0
            if w < cap * .015:
                continue
            xm = (x0 + x1) / 2
            bw = min(max(w * .8, cap * .035), cap * maxw)
            h = cap * rng.uniform(*top_len) * prof(xm)
            if h < cap * .06:
                continue
            lean = rng.uniform(-.08, .08) * h
            yb = min(ys)
            parts.append(spike_shape(xm - bw / 2, xm + bw / 2, yb + 3, h, lean, curve=.3))
            if thorns and h > cap * .5 and rng.random() < .8:
                f = rng.uniform(.3, .55)
                side = rng.choice((-1, 1))
                parts.append(thorn(xm + lean * f, yb - h * f, h * rng.uniform(.2, .3), bw * .45, -90 + side * rng.uniform(38, 58)))
    if bottom:
        for x0, x1, ys in clusters(pts, lambda p: b[3] - p[1], cap * .05, cap * .04):
            w = x1 - x0
            if w < cap * .015:
                continue
            yb = max(ys)
            xm = (x0 + x1) / 2
            if rng.random() < drip_prob:
                nd = 1 if w < cap * .16 else 2
                for k in range(nd):
                    xx = x0 + w * (k + 1) / (nd + 1) + rng.uniform(-.1, .1) * w
                    parts.append(drip(xx, yb - 2, min(max(w * .5, cap * .03), cap * .065) * rng.uniform(.7, 1), cap * rng.uniform(*drip_len), rng))
            else:
                bw = min(max(w * .8, cap * .035), cap * maxw)
                parts.append(spike_shape(xm - bw / 2, xm + bw / 2, yb - 3, cap * rng.uniform(*bottom_len), rng.uniform(-.08, .08) * cap, curve=.3, up=False))
    return union(*parts)


# ---------- napis ----------
def word(font, text, size, x, y, track, rng, sy=1.25, profile=None, **kw):
    """Beseda z metal obdelavo, raztegnjena v višino (sy). profile dobi x v koordinatah platna."""
    glyphs, adv = font.layout(text, size, 0, 0, track)
    out = []
    cap = font.cap_px(size) * sy
    dx = x - adv / 2
    for ch, g in glyphs:
        if not len(g.p):
            continue
        g = g.scale(1, sy).move(dx, y)
        out.append(metalize(g, cap, rng, profile=profile, **kw))
    return union(*out), cap


def drips_under(shape, cap, rng, n=10, lo=.2, hi=.9, wmin=.03, wmax=.07):
    """Dodatne kaplje s spodnjih robov (za 'taljenje')."""
    b = shape.bounds
    pts = [p for c in flatten(shape, 3.0) for p in c]
    out = []
    for _ in range(n):
        x = rng.uniform(b[0] + (b[2] - b[0]) * .05, b[2] - (b[2] - b[0]) * .05)
        cand = [p for p in pts if abs(p[0] - x) < 3]
        if not cand:
            continue
        # najnižja točka na tem x, ki je spodnji rob (zunaj pod njo ni oblike)
        yb = max(p[1] for p in cand)
        out.append(drip(x, yb - 3, cap * rng.uniform(wmin, wmax), cap * rng.uniform(lo, hi), rng))
    return union(*out)


def side_thorns(glyph, cap, rng, n=2, length=(.15, .35), up=True):
    """Trni iz levega/desnega roba črke, usmerjeni navzven in navzgor."""
    b = glyph.bounds
    pts = [p for c in flatten(glyph, 3.0) for p in c]
    out = []
    for side in (-1, 1):
        edge = [p for p in pts if (p[0] - b[0] < cap * .04 if side < 0 else b[2] - p[0] < cap * .04)
                and b[1] + (b[3] - b[1]) * .2 < p[1] < b[3] - (b[3] - b[1]) * .15]
        for _ in range(n):
            if not edge or rng.random() < .35:
                continue
            x, y = rng.choice(edge)
            ang = (180 if side < 0 else 0) + (-1 if up else 1) * side * -rng.uniform(25, 50)
            ang = -180 + rng.uniform(25, 50) if side < 0 else -rng.uniform(25, 50)
            out.append(thorn(x - side * 2, y, cap * rng.uniform(*length), cap * .035, ang))
    return union(*out)


def warp(shape, fn, step=2.5):
    """Deformacija: fn(x, y) → (x', y') na vseh točkah (npr. lok)."""
    return from_contours([[fn(x, y) for x, y in c] for c in flatten(shape, step)])


def arch(cx, k):
    return lambda x, y: (x, y + k * (x - cx) ** 2)


# ======================================================================
#  LOGOTIP
# ======================================================================
GOTH = None


def goth():
    global GOTH
    if GOTH is None:
        GOTH = Font("GrenzeGotisch", wght=800)
    return GOTH


def metal_line(text, size, cx, y, rng, prof=None, sy=1.3, track=-12, top_len=(.5, 1.0), drip_len=(.08, .35),
               drip_prob=.45, thorns_n=1, maxw=.05):
    F = goth()
    glyphs, adv = F.layout(text, size, 0, 0, track)
    cap = F.cap_px(size) * sy
    dx = cx - adv / 2
    parts, gl = [], []
    for ch, g in glyphs:
        if not len(g.p):
            continue
        g = g.scale(1, sy).move(dx, y)
        gl.append(g)
        parts.append(metalize(g, cap, rng, profile=prof, top_len=top_len, drip_len=drip_len, drip_prob=drip_prob, maxw=maxw))
        if thorns_n:
            parts.append(side_thorns(g, cap, rng, n=thorns_n))
    return union(*parts), gl, cap


def bm_logo(seed=7, horns=True, cx=0, y0=0, arch_k=.00032, parts=False):
    """Glavni black metal logotip: HUNGRY v loku, GOAT spodaj s kapljami, rogova iz H in Y."""
    rng = random.Random(seed)
    W = 560
    prof = lambda x: .45 + 1.5 * min(1, abs(x - cx) / W) ** 2
    hungry, gl, cap = metal_line("HUNGRY", 240, cx, y0, rng, prof)
    hungry = warp(hungry, arch(cx, arch_k))
    F = goth()
    cap2 = F.cap_px(330) * 1.3
    y1 = y0 + cap2 * 1.02 + 60
    goat, _, _ = metal_line("GOAT", 330, cx, y1, rng, lambda x: .2, top_len=(.25, .45), drip_len=(.15, .95),
                            drip_prob=.85)
    hl = Shape()
    if horns:
        hb = gl[0].bounds
        hx = hb[0] + (hb[2] - hb[0]) * .18
        hy = hb[1] + cap * .05 + arch_k * (hx - cx) ** 2
        k = cap / 300 * 1.25
        segs = [((hx, hy), (hx - 8 * k, hy - 130 * k), (hx - 70 * k, hy - 215 * k), (hx - 165 * k, hy - 222 * k)),
                ((hx - 165 * k, hy - 222 * k), (hx - 250 * k, hy - 228 * k), (hx - 300 * k, hy - 150 * k), (hx - 282 * k, hy - 62 * k))]
        h1 = horn(segs, (hb[2] - hb[0]) * .42, 3, ridges=11, groove=1.4)
        hl = h1 | h1.mirror_x(cx)
    if parts:
        return roughen(hungry | goat, amp=2.0, seed=seed), roughen(hl, amp=1.6, seed=seed + 1) if horns else Shape()
    return roughen(hungry | goat | hl, amp=2.0, seed=seed)


def bm_one_line(text="HUNGRY GOAT", seed=3, size=200):
    rng = random.Random(seed)
    W = 900
    s, gl, cap = metal_line(text, size, 0, 0, rng, lambda x: .35 + .9 * min(1, abs(x) / W) ** 2,
                            top_len=(.4, .9), drip_len=(.1, .5), drip_prob=.6)
    return roughen(s, amp=1.8, seed=seed)


# ======================================================================
#  GRAVIRAN ROG (za tisk na kapuco)
# ======================================================================
def engraved_horn(segs, w0, w1=3, rings=20, hatch=5, seed=5, n=140, shade_side=-1):
    """Rog v slogu bakroreza: telo minus vrezani obroči in črte senčenja na temni strani.
    Vrne enobarvno obliko (bela na črni podlagi)."""
    rng = random.Random(seed)
    if isinstance(segs[0][0], (int, float)):
        segs = [segs]
    from lib import _curve
    pts = _curve(segs, n)
    N = len(pts) - 1
    acc = [0]
    for i in range(1, N + 1):
        acc.append(acc[-1] + math.dist(pts[i], pts[i - 1]))
    total = acc[-1]
    nrm, W = [], []
    L, R = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, N)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        t = acc[i] / total
        w = (w0 + (w1 - w0) * t ** .8) / 2
        nrm.append((nx, ny)); W.append(w)
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
    body = poly(L + R[::-1])

    def at(t):
        i = min(range(N + 1), key=lambda q: abs(acc[q] / total - t))
        return i

    def P(i, s, along=0.0):
        x, y = pts[i]; nx, ny = nrm[i]; w = W[i]
        tx, ty = ny, -nx
        return (x + nx * w * s * shade_side * -1 + tx * along, y + ny * w * s * shade_side * -1 + ty * along)

    cuts = []
    # obroči: debelejši na senčni strani, izginejo na osvetljeni
    for j in range(1, rings + 1):
        t = j / (rings + 1) * .95
        i = at(t)
        w = W[i]
        g = w * .16 * (1 - t * .5)
        up, dn = [], []
        for q in range(15):
            s = -1.1 + 1.9 * q / 14          # od senčne (-1) proti svetli (+0.8)
            bow = w * .28 * (1 - (s / 1.1) ** 2)
            th = g * max(0, (0.75 - s) / 1.85) ** .9
            cx_, cy_ = P(i, s, bow)
            x, y = pts[i]; nx, ny = nrm[i]; tx, ty = ny, -nx
            up.append((cx_ + tx * th / 2, cy_ + ty * th / 2)); dn.append((cx_ - tx * th / 2, cy_ - ty * th / 2))
        cuts.append(poly(up + dn[::-1]))
    # vzdolžne črte senčenja med obroči
    for h in range(hatch):
        s = -.92 + h * .17
        for j in range(rings + 1):
            t0 = j / (rings + 1) * .95 + .012
            t1 = (j + 1) / (rings + 1) * .95 - .012
            if t1 <= t0 or rng.random() < .15:
                continue
            i0, i1 = at(t0), at(t1)
            if i1 - i0 < 3:
                continue
            th = W[i0] * .07 * (1 - h / hatch)
            side_a = [P(i, s) for i in range(i0, i1 + 1)]
            ln = len(side_a)
            up = [(x + nrm[i0 + k][0] * th * (1 - abs(2 * k / (ln - 1) - 1)), y + nrm[i0 + k][1] * th * (1 - abs(2 * k / (ln - 1) - 1)))
                  for k, (x, y) in enumerate(side_a)]
            cuts.append(poly(side_a + up[::-1]))
    out = body - union(*cuts)
    return roughen(out, amp=1.2, freq=.12, nick=.02, seed=seed)
