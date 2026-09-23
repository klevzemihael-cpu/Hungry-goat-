"""Metal kolekcija: black metal napis, rogovi na kapuci, jopa in majice.

python metal.py  → svg/bm-*.svg (tisk) + mock/metal-*.svg (mockupi)
"""
import os, json, random
from lib import *
from bm import *
import mockups as M

SVG = os.path.join(HERE, "svg")
JOBS = []


def save_print(name, shape_items, pad=40, distress=None):
    """shape_items: [(Shape, barva)] → obrezan SVG."""
    xs = [s.bounds for s, _ in shape_items if len(s.p)]
    x0 = min(b[0] for b in xs); y0 = min(b[1] for b in xs)
    x1 = max(b[2] for b in xs); y1 = max(b[3] for b in xs)
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    body = "".join(s.move(pad - x0, pad - y0).svg(c) for s, c in shape_items if len(s.p))
    open(os.path.join(SVG, name + ".svg"), "w").write(svg_doc(round(w), round(h), body, distress=distress))
    return w, h


def place(name, cx, cy, width, w, h, rot=0):
    """<image> datoteke s tiskom, centrirane v (cx, cy) s širino width."""
    hh = width * h / w
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<image href="../svg/{name}.svg" x="{cx-width/2:.1f}" y="{cy-hh/2:.1f}" width="{width:.1f}" height="{hh:.1f}"{t}/>'


# ---------------- tiskovine ----------------
def build_prints():
    sizes = {}
    # glavni logotip z rogovi (majice) in brez rogov (jopa – rogovi so na kapuci)
    lg = bm_logo(seed=7, horns=True)
    sizes["bm-logo"] = save_print("bm-logo", [(lg, BONE)])
    txt, hr = bm_logo(seed=7, horns=True, parts=True)
    sizes["bm-logo-orange"] = save_print("bm-logo-orange", [(hr, ORANGE), (txt, BONE)])
    sizes["bm-logo-black"] = save_print("bm-logo-black", [(lg, BLACK)])
    nh = bm_logo(seed=7, horns=False)
    sizes["bm-logo-nohorns"] = save_print("bm-logo-nohorns", [(nh, BONE)])
    sizes["bm-line"] = save_print("bm-line", [(bm_one_line(), BONE)])
    # STAY HUNGRY – za hrbet
    rng = random.Random(11)
    W = 520
    stay, _, cap = metal_line("STAY", 300, 0, 0, rng, lambda x: .3 + 1.3 * min(1, abs(x) / W) ** 2, top_len=(.45, .95))
    hun, _, cap2 = metal_line("HUNGRY", 250, 0, cap + 120, rng, lambda x: .2, top_len=(.2, .4),
                              drip_len=(.15, .9), drip_prob=.85)
    stay = warp(stay, arch(0, .00035))
    sh = roughen(stay | hun, amp=2.0, seed=11)
    b = sh.bounds
    sub = INTER_TEXT("BECOME A GOAT  ·  MARIBOR  ·  EST. 2026", (b[2] - b[0]) * .78, (b[0] + b[2]) / 2, b[3] + 90)
    sizes["bm-stay"] = save_print("bm-stay", [(sh, BONE), (sub, ORANGE)])
    # navpični napis za rokav
    rng = random.Random(5)
    sv, _, _ = metal_line("STAY HUNGRY", 160, 0, 0, rng, lambda x: .5, top_len=(.25, .5), drip_len=(.08, .3),
                          drip_prob=.5, thorns_n=0)
    sizes["bm-sleeve"] = save_print("bm-sleeve", [(roughen(sv, amp=1.6, seed=5).rotate(-90), BONE)])
    return sizes


def INTER_TEXT(s, width, cx, y):
    return Font("Inter", wght=800).fit(s, width, cx, y, track=300)


# ---------------- rogovi na kapuci (v koordinatah kapuce) ----------------
def hood_horns_front():
    segs = [((452, 212), (440, 166), (410, 132), (376, 134)),
            ((376, 134), (346, 136), (332, 170), (340, 212))]
    h = engraved_horn(segs, 46, 5, rings=11, hatch=2, seed=3)
    return h | h.mirror_x(500)


def hood_horns_back():
    segs = [((446, 88), (402, 92), (372, 128), (368, 178)),
            ((368, 178), (364, 226), (380, 262), (404, 280))]
    h = engraved_horn(segs, 50, 5, rings=11, hatch=2, seed=4)
    return h | h.mirror_x(500)


# ---------------- stranski pogled kapuce ----------------
HOOD_SIDE = ("M338,600 C300,520 286,400 318,318 C352,232 452,180 570,188 C690,196 772,282 778,410 "
             "C784,520 742,610 672,662 L642,690 L360,690 Z")
FRONT_RIM = "M338,600 C300,520 286,400 318,318 C330,288 348,262 372,240"
BODY_SIDE = ("M300,690 C330,672 420,664 520,664 C640,664 740,676 800,700 C860,724 900,800 910,1000 "
             "L230,1000 C236,860 250,740 300,690 Z")
SLEEVE_SIDE = "M520,700 C600,690 690,700 740,760 C790,830 800,920 800,1000 L520,1000 C510,900 505,790 520,700 Z"


def hood_side_horn():
    segs = [((352, 312), (360, 238), (430, 196), (520, 196)),
            ((520, 196), (640, 196), (724, 268), (728, 380)),
            ((728, 380), (732, 460), (694, 520), (640, 536))]
    return engraved_horn(segs, 92, 6, rings=22, hatch=5, seed=9)


def hood_side(col="black", horn_ink=BONE):
    c = M.C[col]
    cid, bid = M.uid("hs"), M.uid("bs")
    s = f'<path d="{BODY_SIDE}" fill="#000" opacity=".3" filter="url(#b28)" transform="translate(0,20)"/>'
    s += f'<path d="{BODY_SIDE}" fill="{c["base"]}"/>'
    s += (f'<defs><clipPath id="{bid}"><path d="{BODY_SIDE}"/></clipPath></defs><g clip-path="url(#{bid})">'
          f'<path d="M300,700 C420,690 620,690 800,720" stroke="#000" stroke-width="60" opacity=".45" fill="none" filter="url(#b28)"/>'
          f'<path d="M330,760 C340,860 330,940 320,1000" stroke="#fff" stroke-width="60" opacity="{c["hi"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:screen"/>'
          f'<rect width="1000" height="1000" filter="url(#fleece)" opacity=".16" style="mix-blend-mode:screen"/></g>')
    s += f'<path d="{SLEEVE_SIDE}" fill="#000" opacity=".35" filter="url(#b10)" transform="translate(-6,0)"/>'
    s += f'<path d="{SLEEVE_SIDE}" fill="{c["base"]}"/>'
    s += f'<path d="M530,720 C560,800 560,900 548,1000" stroke="#fff" stroke-width="36" opacity="{c["hi"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:screen"/>'
    s += f'<path d="M760,780 C780,860 786,940 786,1000" stroke="#000" stroke-width="40" opacity=".5" fill="none" filter="url(#b28)"/>'
    s += f'<path d="M520,700 C600,690 690,700 740,760" stroke="{c["seam"]}" stroke-width="3" fill="none"/>'
    # kapuca
    s += f'<path d="{HOOD_SIDE}" fill="#000" opacity=".35" filter="url(#b28)" transform="translate(10,14)"/>'
    s += f'<path d="{HOOD_SIDE}" fill="{c["base"]}"/>'
    s += (f'<defs><clipPath id="{cid}"><path d="{HOOD_SIDE}"/></clipPath></defs><g clip-path="url(#{cid})">'
          f'<g filter="url(#warp)">{hood_side_horn().svg(horn_ink)}</g>'
          f'<path d="M420,250 C380,330 380,470 420,600" stroke="#fff" stroke-width="80" opacity="{c["hi"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:screen"/>'
          f'<path d="M760,330 C780,440 760,560 690,650" stroke="#000" stroke-width="90" opacity="{c["lo"]}" fill="none" filter="url(#b28)" style="mix-blend-mode:multiply"/>'
          f'<path d="M560,190 C640,200 700,240 740,300" stroke="#000" stroke-width="40" opacity="{c["lo"]*.6}" fill="none" filter="url(#b28)" style="mix-blend-mode:multiply"/>'
          f'<path d="M430,640 C520,610 600,620 660,660" stroke="#000" stroke-width="30" opacity=".45" fill="none" filter="url(#b10)"/>'
          f'<rect width="1000" height="1000" filter="url(#fleece)" opacity=".16" style="mix-blend-mode:screen"/></g>')
    # rob kapuce, šiv po sredini in vrvica
    s += f'<path d="{FRONT_RIM}" stroke="{c["rib"]}" stroke-width="22" fill="none" stroke-linecap="round"/>'
    s += f'<path d="{FRONT_RIM}" stroke="#000" stroke-opacity=".5" stroke-width="6" fill="none" transform="translate(-9,0)"/>'
    s += f'<path d="M372,240 C420,206 490,186 570,188 C690,196 772,282 778,410" stroke="{c["seam"]}" stroke-width="2.4" fill="none" stroke-dasharray="7 6" transform="translate(0,14)"/>'
    s += f'<circle cx="332" cy="584" r="7" fill="#777" stroke="#444" stroke-width="2"/>'
    s += f'<path d="M332,584 C318,640 312,700 318,770" stroke="{c["rib"]}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    s += f'<rect x="312" y="764" width="12" height="30" rx="3" fill="#8a8a8a"/>'
    return s


def hood_print_svg(shape, col):
    return shape.svg(col)


# ---------------- jopa ----------------
M.AGLET = "#9a9a9a"


def metal_hoodie(sizes, col="black", ink=BONE, horn_ink=BONE, front_logo="bm-logo-nohorns", back_print="bm-stay"):
    w, h = sizes[front_logo]
    front = place(front_logo, 500, 520, 330, w, h)
    # rokav (desno na sliki = levi rokav nosilca): ponavljajoči se mali logotipi
    sw, sh = sizes["bm-logo-nohorns"]
    for i in range(5):
        y = 505 + i * 66
        x = 787 + (y - 480) * .06
        front += place("bm-logo-nohorns", x, y, 60, sw, sh, rot=-3)
    # drugi rokav: navpični STAY HUNGRY
    vw, vh = sizes["bm-sleeve"]
    front += place("bm-sleeve", 212, 640, 58, vw, vh, rot=3)
    hf = M.hoodie(col, None, front, back=False, hood_print=hood_horns_front().svg(horn_ink))
    bw, bh = sizes[back_print]
    back = place(back_print, 500, 560, 340, bw, bh)
    hb = M.hoodie(col, None, back, back=True, hood_print=hood_horns_back().svg(horn_ink))
    return hf, hb


def save_mock(name, svg, col):
    p = os.path.join(M.MOCK, name + ".svg")
    open(p, "w").write(svg)
    JOBS.append((p, 1000, 1000, col))


def metal_tees(sizes):
    w, h = sizes["bm-logo"]
    t1 = M.tee("black", place("bm-logo", 500, 445, 360, w, h))
    save_mock("metal-tee-logo-black", M.scene(t1, "black"), "black")
    w, h = sizes["bm-logo-orange"]
    t2 = M.tee("black", place("bm-logo-orange", 500, 445, 360, w, h))
    save_mock("metal-tee-logo-orange-black", M.scene(t2, "black"), "black")
    w, h = sizes["bm-stay"]
    t3 = M.tee("black", place("bm-stay", 500, 470, 360, w, h), back=True)
    save_mock("metal-tee-stay-back", M.scene(t3, "black"), "black")
    w, h = sizes["bm-logo-black"]
    t4 = M.tee("bone", place("bm-logo-black", 500, 445, 360, w, h))
    save_mock("metal-tee-logo-bone", M.scene(t4, "bone"), "bone")




# ---------------- fitnes × metal ----------------
def brutal_prints(sizes):
    from designs import kb_shape, OSW
    # 1) GRB: dva velika gravirana rogova, drog čez sredino, metal napis zgoraj
    left = engraved_horn([((-50, 30), (-80, -230), (-280, -430), (-440, -300)),
                          ((-440, -300), (-540, -210), (-500, -20), (-360, 0))], 140, 8, rings=28, hatch=5, seed=21)
    horns = left | left.mirror_x(0)
    bar = roughen(barbell(0, 20, 1040, 230, 22), amp=1.6, seed=22)
    horns = horns - bar.stroked(26)
    name = bm_one_line("HUNGRY GOAT", seed=4, size=190)
    nb = name.bounds
    name = name.move(-(nb[0] + nb[2]) / 2, -490 - nb[3])
    sub = INTER_TEXT("IRON  ·  SWEAT  ·  DISCIPLINE", 760, 0, 250)
    loc = INTER_TEXT("BARBELL CLUB  ·  MARIBOR  ·  2026", 560, 0, 320)
    sizes["bm-crest"] = save_print("bm-crest", [(name, BONE), (horns, BONE), (bar, ORANGE), (sub, BONE), (loc, ORANGE)])

    # 2) FEED THE BEAST: ročka, ki se topi, pod metal napisom
    rng = random.Random(31)
    kb = kb_shape(300)
    kb = kb | drips_under(kb, 600, rng, n=9, lo=.12, hi=.5, wmin=.03, wmax=.055)
    kb = roughen(kb, amp=2.2, seed=31)
    hg = Font("Anton-Regular").fit("HG", 230, 0, 128, track=30)
    kb = kb - hg
    t, _, cap = metal_line("FEED THE BEAST", 170, 0, -560, rng, lambda x: .35 + 1.2 * min(1, abs(x) / 620) ** 2,
                           top_len=(.4, .9), drip_len=(.08, .3), drip_prob=.4)
    t = roughen(warp(t, arch(0, .00025)), amp=1.8, seed=32)
    sub = INTER_TEXT("NO CALORIE COUNTING  ·  JUST EAT  ·  JUST LIFT", 700, 0, 760)
    sizes["bm-feed"] = save_print("bm-feed", [(t, BONE), (kb, BONE), (sub, ORANGE)])

    # 3) EARN YOUR HORNS – samo napis
    rng = random.Random(41)
    l1, _, c1 = metal_line("EARN YOUR", 190, 0, 0, rng, lambda x: .3 + 1.2 * min(1, abs(x) / 520) ** 2, top_len=(.4, .95),
                           drip_prob=.3)
    l1 = warp(l1, arch(0, .0003))
    l2, _, c2 = metal_line("HORNS", 330, 0, c1 + 190, rng, lambda x: .2, top_len=(.2, .4), drip_len=(.2, 1.0), drip_prob=.9)
    e = roughen(l1 | l2, amp=2.1, seed=41)
    b = e.bounds
    sub = INTER_TEXT("NOBODY GIVES YOU HORNS. YOU GROW THEM.", (b[2] - b[0]) * .82, 0, b[3] + 80)
    sizes["bm-earn"] = save_print("bm-earn", [(e, BONE), (sub, ORANGE)])

    # 4) THE GRIND TOUR – metal glava, fitnes urnik
    rng = random.Random(51)
    head = roughen(bm_one_line("HUNGRY GOAT", seed=51, size=200), amp=1.6, seed=52)
    hb = head.bounds
    head = head.move(-(hb[0] + hb[2]) / 2, 0)
    W = head.w
    t1 = Font("Anton-Regular").fit("THE GRIND WORLD TOUR 2026", W * .92, 0, hb[3] + 150, track=40)
    items = [(head, BONE), (t1, ORANGE)]
    rows = [("MON", "CHEST", "TNT GYM"), ("TUE", "BACK", "TNT GYM"), ("WED", "LEGS", "TNT GYM"),
            ("THU", "SHOULDERS", "TNT GYM"), ("FRI", "ARMS", "TNT GYM"), ("SAT", "LEGS AGAIN", "TNT GYM"),
            ("SUN", "REST DAY", "CANCELLED")]
    y = t1.bounds[3] + 110
    x0, x1 = -W * .46, W * .46
    for i, (d, what, where) in enumerate(rows):
        c = ORANGE if i == 6 else BONE
        items += [(OSW.text(d, 58, x0, y, "start", 60), ORANGE), (OSW.text(what, 58, x0 + 170, y, "start", 40), c),
                  (OSW.text(where, 58, x1, y, "end", 40), c)]
        if i < 6:
            items.append((rect(x0, y + 28, x1 - x0, 3), BONE))
        y += 92
    items.append((INTER_TEXT("NO REFUNDS  ·  NO EXCUSES  ·  NO DAYS OFF", W * .7, 0, y + 30), BONE))
    sizes["bm-tour"] = save_print("bm-tour", items)
    return sizes


def brutal_mocks(sizes):
    hf, hb = metal_hoodie(sizes, back_print="bm-tour")
    save_mock("metal-hoodie-black-front", M.scene(hf, "black", fit=M.HOODIE_FIT), "black")
    save_mock("metal-hoodie-black-back", M.scene(hb, "black", fit=M.HOODIE_FIT), "black")
    metal_tees(sizes)
    for key, col, back, cy, wd in [("bm-crest", "black", True, 470, 380), ("bm-feed", "black", True, 480, 360),
                                   ("bm-earn", "black", True, 440, 380), ("bm-crest", "bone", False, 430, 300)]:
        w, h = sizes[key]
        name = key if col != "bone" else key + "-svetla"
        prn = place(key if col == "black" else key + "-dark", 500, cy, wd, w, h)
        save_mock(f"metal-tee-{name.replace('bm-', '')}", M.scene(M.tee(col, prn, back=back), col), col)


if __name__ == "__main__":
    sizes = build_prints()
    sizes = brutal_prints(sizes)
    # temne različice za svetle majice
    import re
    for k in ("bm-crest",):
        src = open(os.path.join(SVG, k + ".svg")).read().replace(BONE, BLACK)
        open(os.path.join(SVG, k + "-dark.svg"), "w").write(src)
    json.dump({k: list(v) for k, v in sizes.items()}, open(os.path.join(SVG, "_bm_sizes.json"), "w"))
    brutal_mocks(sizes)
    json.dump(JOBS, open(os.path.join(M.MOCK, "_metal_jobs.json"), "w"))
    print("ok", {k: (round(v[0]), round(v[1])) for k, v in sizes.items()})
