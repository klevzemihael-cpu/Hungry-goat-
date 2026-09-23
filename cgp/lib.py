"""Vektorska orodja za CGP Hungry Goat.

Vse besedilo se pretvori v krivulje (brez odvisnosti od pisav v tiskarni),
rogovi, ročka in ostali elementi so zgrajeni kot čiste vektorske oblike.
"""
import math, os
import pathops
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- barve ----------
BLACK = "#0E0E0E"
BONE = "#F2EEE6"
ORANGE = "#FF5A1F"
EMBER = "#C23A0E"
ASH = "#8C877F"
IRON = "#2A2826"


# ---------- oblika (ovoj za pathops) ----------
class Shape:
    def __init__(self, p=None):
        self.p = p if p is not None else pathops.Path()

    @classmethod
    def from_d(cls, d):
        p = pathops.Path()
        parse_path(d, p.getPen())
        return cls(p)

    def d(self, prec=2):
        pen = SVGPathPen(None, ntos=lambda v: (f"{v:.{prec}f}").rstrip("0").rstrip("."))
        self.p.draw(pen)
        return pen.getCommands()

    @property
    def bounds(self):
        return self.p.bounds  # xmin, ymin, xmax, ymax

    @property
    def w(self):
        b = self.bounds; return b[2] - b[0]

    @property
    def h(self):
        b = self.bounds; return b[3] - b[1]

    def copy(self):
        return Shape(self.p.transform(1, 0, 0, 1, 0, 0))

    def t(self, a=1, b=0, c=0, d=1, e=0, f=0):
        return Shape(self.p.transform(a, b, c, d, e, f))

    def move(self, dx, dy):
        return self.t(1, 0, 0, 1, dx, dy)

    def scale(self, sx, sy=None, ox=0, oy=0):
        sy = sx if sy is None else sy
        return self.t(sx, 0, 0, sy, ox - ox * sx, oy - oy * sy)

    def rotate(self, deg, ox=0, oy=0):
        r = math.radians(deg); c, s = math.cos(r), math.sin(r)
        return self.t(c, s, -s, c, ox - c * ox + s * oy, oy - s * ox - c * oy)

    def mirror_x(self, ox=0):
        return self.t(-1, 0, 0, 1, 2 * ox, 0)

    def skew_x(self, deg, oy=0):
        k = math.tan(math.radians(deg))
        return self.t(1, 0, k, 1, -k * oy, 0)

    def __or__(self, o):
        return Shape(pathops.op(self.p, o.p, pathops.PathOp.UNION))

    def __sub__(self, o):
        return Shape(pathops.op(self.p, o.p, pathops.PathOp.DIFFERENCE))

    def __and__(self, o):
        return Shape(pathops.op(self.p, o.p, pathops.PathOp.INTERSECTION))

    def simplify(self):
        return Shape(pathops.simplify(self.p))

    def stroked(self, width, join="round", cap="round"):
        q = self.p.transform(1, 0, 0, 1, 0, 0)
        q.stroke(width, {"butt": pathops.LineCap.BUTT_CAP, "round": pathops.LineCap.ROUND_CAP,
                         "square": pathops.LineCap.SQUARE_CAP}[cap],
                 {"miter": pathops.LineJoin.MITER_JOIN, "round": pathops.LineJoin.ROUND_JOIN,
                  "bevel": pathops.LineJoin.BEVEL_JOIN}[join], 4)
        q.convertConicsToQuads()
        return Shape(pathops.simplify(q))

    def outline(self, gap, line):
        """Obroba na razdalji `gap` z debelino `line` (klasični 'metal' obris)."""
        outer = self.stroked(2 * (gap + line)) | self
        inner = self.stroked(2 * gap) | self
        return outer - inner

    def svg(self, fill, extra=""):
        return f'<path d="{self.d()}" fill="{fill}"{(" " + extra) if extra else ""}/>'


def union(*shapes):
    out = Shape()
    for s in shapes:
        if s is None:
            continue
        out = out | s
    return out


def poly(pts, closed=True):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if closed:
        p.close()
    return Shape(p)


def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def circle(cx, cy, r):
    k = 0.5522847498 * r
    p = pathops.Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return Shape(p)


# ---------- pisave ----------
class Font:
    _cache = {}

    def __init__(self, name, wght=None, wdth=None):
        path = os.path.join(HERE, "fonts", name + ".ttf")
        self.tt = TTFont(path)
        self.upem = self.tt["head"].unitsPerEm
        loc = {}
        if wght is not None: loc["wght"] = wght
        if wdth is not None: loc["wdth"] = wdth
        self.gs = self.tt.getGlyphSet(location=loc or None)
        self.order = self.tt.getGlyphOrder()
        face = hb.Face(hb.Blob.from_file_path(path))
        self.hb = hb.Font(face)
        if loc:
            self.hb.set_variations(loc)
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or self.upem * 0.7

    def text(self, s, size, x=0, y=0, anchor="middle", track=0, features=None):
        """Besedilo kot oblika. y je osnovnica, track v tisočinkah em."""
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, features or {"kern": True, "liga": True})
        k = size / self.upem
        tr = track * self.upem / 1000
        pen = pathops.Path().getPen()
        out = pathops.Path()
        pen = out.getPen(glyphSet=self.gs)
        cx = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            g = self.order[info.codepoint]
            tp = TransformPen(pen, (k, 0, 0, -k, (cx + pos.x_offset) * k, -pos.y_offset * k))
            self.gs[g].draw(tp)
            cx += pos.x_advance + tr
        cx -= tr
        sh = Shape(pathops.simplify(out)) if len(out) else Shape(out)
        adv = cx * k
        dx = {"start": 0, "middle": -adv / 2, "end": -adv}[anchor]
        return sh.move(x + dx, y)

    def layout(self, s, size, x=0, y=0, track=0, features=None):
        """Posamezne črke kot oblike [(znak, oblika)], začetek v x (levo poravnano)."""
        buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
        hb.shape(self.hb, buf, features or {"kern": True, "liga": True})
        k = size / self.upem; tr = track * self.upem / 1000
        out, cx = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            p = pathops.Path()
            self.gs[self.order[info.codepoint]].draw(TransformPen(p.getPen(glyphSet=self.gs), (k, 0, 0, -k, x + (cx + pos.x_offset) * k, y - pos.y_offset * k)))
            out.append((s[info.cluster], Shape(pathops.simplify(p)) if len(p) else Shape(p)))
            cx += pos.x_advance + tr
        return out, (cx - tr) * k

    def fit(self, s, width, cx, y, track=0, features=None):
        """Besedilo, raztegnjeno na točno širino črnila, centrirano na cx."""
        t = self.text(s, 1000, 0, 0, "start", track, features)
        b = t.bounds
        k = width / (b[2] - b[0])
        return t.scale(k).move(cx - (b[0] + (b[2] - b[0]) / 2) * k, y)

    def cap_px(self, size):
        return self.cap * size / self.upem


# ---------- rog ----------
def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def _curve(segs, n):
    """Točke vzdolž zaporedja Bézierovih segmentov [(p0,p1,p2,p3), ...]."""
    pts = []
    for k, s in enumerate(segs):
        for i in range(n + 1):
            if k and i == 0:
                continue
            pts.append(_bez(*s, i / n))
    return pts


def horn(segs, w0, w1=2, ridges=9, ridge=True, n=160, groove=1.25, taper=.8):
    """Kozji rog vzdolž Bézierovih segmentov: debel pri korenu, koničast na koncu,
    z vrezanimi obroči (utori od zunanjega roba proti notranjemu)."""
    if isinstance(segs[0][0], (int, float)):
        segs = [segs]
    pts = _curve(segs, n)
    N = len(pts) - 1
    # dolžina loka za enakomerne obroče
    acc = [0]
    for i in range(1, N + 1):
        acc.append(acc[-1] + math.dist(pts[i], pts[i - 1]))
    total = acc[-1]
    L, R, nrm, W = [], [], [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, N)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        t = acc[i] / total
        w = (w0 + (w1 - w0) * t ** taper) / 2
        nrm.append((nx, ny)); W.append(w)
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
    body = poly(L + R[::-1])
    if not ridge:
        return body
    cuts = []
    for j in range(1, ridges + 1):
        t = j / (ridges + 1) * .92
        i = min(range(N + 1), key=lambda q: abs(acc[q] / total - t))
        x, y = pts[i]; nx, ny = nrm[i]; w = W[i]
        tx, ty = ny, -nx   # smer proti konici
        g = w * .15 * groove
        up, dn = [], []
        for q in range(13):
            s = -.66 + 1.46 * q / 12            # čez rog: od notranjega do zunanjega roba
            bow = w * .22 * (1 - (s / .8) ** 2)  # obroč je rahlo usločen proti konici
            th = g * max(0.0, 1 - abs((s - .06) / .72) ** 2.2)
            px, py = x + nx * w * s + tx * bow, y + ny * w * s + ty * bow
            up.append((px + tx * th / 2, py + ty * th / 2))
            dn.append((px - tx * th / 2, py - ty * th / 2))
        cuts.append(poly(up + dn[::-1]))
    return body - union(*cuts)


HORN_STYLES = {
    # levi rog, koren v (0,0); enote ~ px pri scale=1
    "curl": ([((0, 0), (-4, -110), (-50, -205), (-140, -222)),
              ((-140, -222), (-215, -234), (-262, -180), (-240, -118))], 64),
    "sweep": ([((0, 0), (-10, -120), (-90, -215), (-210, -225)),
               ((-210, -225), (-280, -230), (-330, -200), (-350, -160))], 60),
    "ram": ([((0, 0), (-30, -120), (-170, -150), (-200, -60)),
             ((-200, -60), (-222, 0), (-170, 40), (-130, 5))], 66),
    "up": ([((0, 0), (0, -80), (-40, -150), (-100, -170))], 52),
}


def horn_pair(cx, base_y, spread, scale=1.0, ridges=9, ridge=True, style="curl", w0=None):
    segs, w = HORN_STYLES[style]
    s = scale
    ox = cx - spread / 2
    segs = [tuple((ox + x * s, base_y + y * s) for x, y in seg) for seg in segs]
    left = horn(segs, (w0 or w) * s, 2.2 * s, ridges=ridges, ridge=ridge)
    return left | left.mirror_x(cx)


# ---------- ikone ----------
def kettlebell(cx, cy, r, horns=True, window=True):
    """Ročka (kettlebell) s kozjimi rogovi – sekundarni znak."""
    body = circle(cx, cy, r)
    flat = rect(cx - r * 1.2, cy + r * .86, r * 2.4, r)
    body = body - flat
    # ročaj
    hw, ht = r * .78, r * 1.02
    top = cy - r * .55 - ht
    handle = Shape.from_d(
        f"M{cx-hw},{cy-r*.35} C{cx-hw},{top-r*.05} {cx-hw*.8},{top} {cx},{top} "
        f"C{cx+hw*.8},{top} {cx+hw},{top-r*.05} {cx+hw},{cy-r*.35}").stroked(r * .30, cap="butt")
    kb = body | handle
    if window:
        win_w, win_h = hw * .64, ht * .5
        wy = cy - r * .62
        win = Shape.from_d(
            f"M{cx-win_w},{wy} C{cx-win_w},{wy-win_h*1.2} {cx-win_w*.6},{wy-win_h*1.3} {cx},{wy-win_h*1.3} "
            f"C{cx+win_w*.6},{wy-win_h*1.3} {cx+win_w},{wy-win_h*1.2} {cx+win_w},{wy} Z")
        kb = kb - win
    if horns:
        hp = horn_pair(cx, top + r * .28, hw * 2.05, scale=r / 170, ridges=6, style="curl")
        kb = kb | hp
    return kb


def barbell(cx, cy, length, plate_h, bar=None):
    bar = bar or plate_h * .07
    parts = [rect(cx - length / 2, cy - bar / 2, length, bar)]
    ws = [(plate_h, plate_h * .16), (plate_h * .82, plate_h * .13), (plate_h * .6, plate_h * .1)]
    for side in (-1, 1):
        x = cx + side * length * .30
        for h, w in ws:
            px = x if side > 0 else x - w
            parts.append(rect(px, cy - h / 2, w, h).simplify())
            x += side * (w + plate_h * .02)
        # objemka
        cxl = cx + side * length * .27
        parts.append(rect(cxl - plate_h * .03, cy - plate_h * .12, plate_h * .06, plate_h * .24))
    return union(*parts)


def diamond(cx, cy, r):
    return poly([(cx, cy - r), (cx + r * .62, cy), (cx, cy + r), (cx - r * .62, cy)])


def star4(cx, cy, r, k=.22):
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * k
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts)


def blade(x1, x2, y, h, notch=True):
    """Metal ločnica: dvojno koničasto rezilo z rombom na sredini."""
    cx = (x1 + x2) / 2
    left = poly([(x1, y), (cx - h * 2.2, y - h / 2), (cx - h * 2.2, y + h / 2)])
    right = poly([(x2, y), (cx + h * 2.2, y - h / 2), (cx + h * 2.2, y + h / 2)])
    return left | right | diamond(cx, y, h * 2.4)


def spike(x, y, length, width, angle=-90):
    a = math.radians(angle)
    tx, ty = x + math.cos(a) * length, y + math.sin(a) * length
    nx, ny = -math.sin(a) * width / 2, math.cos(a) * width / 2
    return poly([(x + nx, y + ny), (tx, ty), (x - nx, y - ny)])


# ---------- SVG ----------
DISTRESS = """<filter id="distress" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse">
  <feTurbulence type="fractalNoise" baseFrequency="{f}" numOctaves="4" seed="{seed}" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -{k} {o}" result="m"/>
  <feComposite in="SourceGraphic" in2="m" operator="in"/>
</filter>"""


def svg_doc(w, h, body, bg=None, distress=None, seed=7):
    defs = ""
    if distress:
        f, k, o = {"light": (.9, 9, 7.6), "mid": (.75, 8, 6.2), "heavy": (.6, 7, 4.9)}[distress]
        defs = "<defs>" + DISTRESS.replace("{f}", str(f)).replace("{k}", str(k)).replace("{o}", str(o)).replace("{seed}", str(seed)) \
            .replace('x="0" y="0" width="100%" height="100%"', f'x="0" y="0" width="{w}" height="{h}"') + "</defs>"
        body = f'<g filter="url(#distress)">{body}</g>'
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">{defs}{b}{body}</svg>')


def arc_text(font, s, size, cx, cy, r, center=-90, track=0, bottom=False):
    """Besedilo po krožnici. Zgoraj bere v smeri urinega kazalca, spodaj (bottom=True) v obratni."""
    glyphs, adv = font.layout(s, size, 0, 0, track)
    out = Shape()
    for ch, g in glyphs:
        if not len(g.p):
            continue
        b = g.bounds
        xc = (b[0] + b[2]) / 2
        off = (xc - adv / 2) / r
        if not bottom:
            th = math.radians(center) + off
            rot = math.degrees(th) + 90
        else:
            th = math.radians(center) - off
            rot = math.degrees(th) - 90
        gg = g.move(-xc, 0).rotate(rot).move(cx + r * math.cos(th), cy + r * math.sin(th))
        out = out | gg
    return out


def ring(cx, cy, r, w):
    return circle(cx, cy, r + w / 2) - circle(cx, cy, r - w / 2)


def caron(cx, y, w, h, t):
    """Strešica (za č/š/ž pri pisavah, ki je nimajo)."""
    return poly([(cx - w / 2, y - h), (cx, y - h * .25), (cx + w / 2, y - h), (cx + w / 2 - t * .3, y - h - t * .1),
                 (cx, y - h * .25 - t), (cx - w / 2 + t * .3, y - h - t * .1)]).move(0, 0)
