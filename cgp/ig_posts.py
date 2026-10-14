"""Prvih 12 objav za Instagram @hungrygoat (1080 × 1350) + profilna slika.

python cgp/ig_posts.py <mapa_s_pripravljenimi_fotografijami> <izhodna_mapa>
"""
import os, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PREP = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
TMP = PREP.parent / "html"
TMP.mkdir(exist_ok=True)

F = (ROOT / "cgp" / "fonts").as_uri()
BRAND = (ROOT / "img" / "brand").as_uri()
LOGO = (ROOT / "Logotipi").as_uri()
P = PREP.as_uri()

CSS = f"""
@font-face{{font-family:Anton;src:url({F}/Anton-Regular.ttf)}}
@font-face{{font-family:Inter;src:url({F}/Inter.ttf);font-weight:100 900}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:#0E0E0E}}
.post{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#0E0E0E;color:#F2EEE6;font-family:Inter,sans-serif}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.sb{{position:absolute;inset:0;background:linear-gradient(to top,rgba(8,8,8,.96) 0%,rgba(8,8,8,.82) 26%,rgba(8,8,8,0) 58%)}}
.st{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(8,8,8,.9) 0%,rgba(8,8,8,.55) 22%,rgba(8,8,8,0) 45%)}}
.grain{{position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}}
.pad{{position:absolute;left:84px;right:84px}}
.k{{font:700 24px/1.2 Inter;letter-spacing:.3em;text-transform:uppercase;color:#FF5A1F}}
.h{{font-family:Anton,Impact,sans-serif;text-transform:uppercase;line-height:.96;letter-spacing:.005em}}
.h em{{font-style:normal;color:#FF5A1F}}
.sub{{font:500 34px/1.35 Inter;color:#D8D2C7}}
.foot{{position:absolute;left:84px;right:84px;bottom:60px;display:flex;justify-content:space-between;align-items:center}}
.foot img{{height:46px}}
.foot span{{font:600 24px Inter;letter-spacing:.08em;color:#A39E95}}
.rule{{height:4px;width:120px;background:#FF5A1F}}
"""


def page(body, bg="#0E0E0E"):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='post' style='background:{bg}'>{body}<div class='grain'></div></div></body></html>"


def foot(dark=False, handle="@hungrygoat"):
    src = f"{LOGO}/metal-napis-ena-vrstica-crn.svg" if dark else f"{BRAND}/bm-line.svg"
    col = "#5b5750" if dark else "#A39E95"
    return f"<div class='foot'><img src='{src}'><span style='color:{col}'>{handle}</span></div>"


def photo(name, pos="center"):
    return f"<div class='bg' style=\"background-image:url('{P}/{name}.jpg');background-position:{pos}\"></div>"


POSTS = {}

# 01 · uvod (pripeto)
POSTS["01-uvod"] = page(photo("4073") + "<div class='sb'></div>" + f"""
<div class='pad' style='bottom:190px'>
  <div class='k'>Licenciran osebni trener · Maribor</div>
  <div class='h' style='font-size:138px;margin-top:26px'>Ostani lačen.<br><em>Postani GOAT.</em></div>
</div>""" + foot())

# 02 · storitve (karusel, naslovnica)
rows = [("01", "1 na 1", "Osebni treningi v TNT Gym"), ("02", "Online coaching", "Program, popravki in podpora od kjerkoli"),
        ("03", "Skupinske vadbe", "Energija ekipe, trener ob tebi")]
r = "".join(f"<div style='display:flex;gap:34px;align-items:baseline;padding:30px 0;border-top:2px solid #2A2826'>"
            f"<div class='h' style='font-size:64px;color:#FF5A1F;width:90px'>{n}</div><div><div class='h' style='font-size:66px'>{t}</div>"
            f"<div class='sub' style='font-size:28px;margin-top:8px'>{s}</div></div></div>" for n, t, s in rows)
POSTS["02-storitve"] = page(f"""
<div class='pad' style='top:110px'><div class='k'>Kako delam</div>
<div class='h' style='font-size:150px;margin-top:26px'>3 poti do<br><em>rezultata.</em></div></div>
<div class='pad' style='top:620px'>{r}<div style='border-top:2px solid #2A2826'></div>
<div class='k' style='margin-top:34px;color:#A39E95'>Povleci za podrobnosti →</div></div>""" + foot())

# 02a–c · strani karusela
slides = [("02a-1na1", "4005", "1 na 1", ["Ocena in meritve na prvem treningu", "Program po tvoji meri", "Tehnika pred težo, napredek vsak teden"], "od 30 € / trening"),
          ("02b-online", "4030", "Online coaching", ["Program v aplikaciji z video vajami", "Popravki tehnike po tvojem videu", "Tedenski pregled in sporočila"], "79 € / mesec"),
          ("02c-skupine", "4084", "Skupinske vadbe", ["Največ 10 ljudi v skupini", "Moč, kondicija in tehnika", "Skupnost Hungry Goat"], "45 € / mesec")]
for key, ph, title, items, price in slides:
    li = "".join(f"<div class='sub' style='padding:14px 0 14px 40px;position:relative'><span style='position:absolute;left:0;top:34px;width:22px;height:4px;background:#FF5A1F'></span>{x}</div>" for x in items)
    POSTS[key] = page(photo(ph) + "<div class='sb' style='background:linear-gradient(to top,rgba(8,8,8,.97) 0%,rgba(8,8,8,.9) 40%,rgba(8,8,8,0) 70%)'></div>" + f"""
<div class='pad' style='bottom:170px'><div class='h' style='font-size:118px'>{title}</div>
<div style='margin-top:26px'>{li}</div>
<div class='h' style='font-size:56px;color:#FF5A1F;margin-top:30px'>{price}</div></div>""" + foot())

# 03 · ponudba (pripeto)
POSTS["03-prvi-trening"] = page(photo("4081", "center 20%") + "<div class='sb'></div>" + f"""
<div class='pad' style='top:84px'><div style='display:inline-block;background:#FF5A1F;color:#0E0E0E;font:800 26px Inter;letter-spacing:.22em;padding:14px 22px'>BREZPLAČNO</div></div>
<div class='pad' style='bottom:190px'>
  <div class='h' style='font-size:150px'>Prvi trening<br>je <em>na meni.</em></div>
  <div class='sub' style='margin-top:30px'>Napiši <b style='color:#F2EEE6'>GOAT</b> v sporočilo in se dogovoriva.</div>
</div>""" + foot())

# 04 · citat
POSTS["04-citat"] = page(f"""
<div class='pad' style='top:120px;text-align:center'><img src='{BRAND}/bm-logo-orange.svg' style='width:420px'></div>
<div class='pad' style='top:560px;text-align:center'>
  <div class='h' style='font-size:156px'>Razlika je<br>v zadnji<br><em>ponovitvi.</em></div>
</div>""" + foot())

# 05 · čista fotografija
POSTS["05-portret"] = page(photo("4011") + f"""
<div class='st' style='background:linear-gradient(to bottom,rgba(8,8,8,.7) 0%,rgba(8,8,8,0) 20%)'></div>
<div class='pad' style='top:70px'><div class='k' style='color:#F2EEE6'>TNT Gym · Maribor</div></div>
<img src='{LOGO}/glavni-logotip.svg' style='position:absolute;right:66px;bottom:66px;width:170px'>""")

# 06 · prehrana (svetla)
por = [("1 dlan", "Beljakovine", "meso, ribe, jajca, skuta"), ("1 pest", "Ogljikovi hidrati", "riž, krompir, kosmiči, kruh"),
       ("2 pesti", "Zelenjava", "karkoli, čim bolj pisano"), ("1 palec", "Maščobe", "olje, oreščki, avokado")]
pr = "".join(f"<div style='display:flex;align-items:center;gap:36px;padding:26px 0;border-top:3px solid #0E0E0E'>"
             f"<div class='h' style='font-size:88px;width:330px;color:#0E0E0E'>{a}</div><div><div style='font:800 34px Inter;color:#0E0E0E'>{b}</div>"
             f"<div style='font:500 28px Inter;color:#5b5750;margin-top:4px'>{c}</div></div></div>" for a, b, c in por)
POSTS["06-prehrana"] = page(f"""
<div class='pad' style='top:100px'><div class='k' style='color:#C23A0E'>Prehrana brez štetja kalorij</div>
<div class='h' style='font-size:140px;margin-top:24px;color:#0E0E0E'>Roka je tvoja<br><em style='color:#FF5A1F'>tehtnica.</em></div></div>
<div class='pad' style='top:560px'>{pr}<div style='border-top:3px solid #0E0E0E'></div>
<div style='font:600 26px Inter;color:#5b5750;margin-top:26px'>Izhodišče za en obrok. Natančno ti ga prilagodim na treningu.</div></div>""", bg="#F2EEE6").replace(
    "<div class='grain'></div>", "<div class='grain' style='mix-blend-mode:multiply;opacity:.12'></div>" + foot(dark=True))

# 07 · no days off (oranžna)
POSTS["07-no-days-off"] = page(photo("4137") + "<div class='st'></div>" + f"""
<div class='pad' style='top:96px;text-align:right'>
  <div class='h' style='font-size:190px'>No days<br><em>off.</em></div>
</div>""" + "<div class='sb' style='background:linear-gradient(to top,rgba(8,8,8,.85) 0%,rgba(8,8,8,0) 22%)'></div>" + foot())

# 08 · drop teaser
POSTS["08-drop-teaser"] = page(photo("jopa", "center 30%") + "<div class='sb'></div>" + f"""
<div class='pad' style='bottom:190px'>
  <div class='k'>Hungry Goat Clothing</div>
  <div class='h' style='font-size:170px;margin-top:22px'>Drop 02.<br><em>Kmalu.</em></div>
</div>""" + foot(handle="@hungrygoat.clothing"))

# 09 · mit
POSTS["09-mit"] = page(f"""
<div class='pad' style='top:150px'><div style='display:inline-block;border:8px solid #FF5A1F;color:#FF5A1F;transform:rotate(-6deg);padding:6px 40px 0'><span class='h' style='font-size:170px'>Mit</span></div></div>
<div class='pad' style='top:520px'>
  <div class='h' style='font-size:128px'>»Za rezultate<br>moraš <em>stradati.</em>«</div>
  <div class='k' style='margin-top:60px;color:#A39E95'>Resnica v naslednji sliki →</div>
</div>""" + foot())

# 09b · resnica
facts = [("Stradanje", "ti vzame mišice, energijo in voljo. Kilogrami se vrnejo."),
         ("Beljakovine", "v vsakem obroku – ena dlan. Sitost in mišice."),
         ("Trening moči", "3× na teden. Mišice so tvoj motor."),
         ("Spanec", "7 ur ali več. Brez tega ni napredka.")]
fx = "".join(f"<div style='padding:26px 0;border-top:2px solid #2A2826'><div class='h' style='font-size:64px'>{a}</div>"
             f"<div class='sub' style='font-size:30px;margin-top:8px'>{b}</div></div>" for a, b in facts)
POSTS["09b-resnica"] = page(f"""
<div class='pad' style='top:110px'><div class='k'>Resnica</div>
<div class='h' style='font-size:128px;margin-top:22px'>Jej <em>dovolj.</em><br>Treniraj <em>težko.</em></div></div>
<div class='pad' style='top:520px'>{fx}<div style='border-top:2px solid #2A2826'></div></div>""" + foot())

# 10 · earn your horns
POSTS["10-earn-your-horns"] = page(photo("4055", "center 30%") + "<div class='sb'></div>" + f"""
<div class='pad' style='bottom:190px'>
  <div class='h' style='font-size:176px'>Earn your<br><em>horns.</em></div>
  <div class='sub' style='margin-top:24px'>Nihče ti jih ne podari. Zrastejo ti s treningom.</div>
</div>""" + foot())

# 11 · skupinske
POSTS["11-skupinske"] = page(photo("4152", "center 40%") + "<div class='sb' style='background:linear-gradient(to top,rgba(8,8,8,.97) 0%,rgba(8,8,8,.9) 34%,rgba(8,8,8,0) 62%)'></div>" + f"""
<div class='pad' style='bottom:190px'>
  <div class='k'>Skupinske vadbe</div>
  <div class='h' style='font-size:156px;margin-top:22px'>Treniraj<br>s <em>čredo.</em></div>
  <div class='sub' style='margin-top:24px'>Torek in četrtek · 19:00 · TNT Gym Maribor</div>
</div>""" + foot())

# 12 · ustanovni člani (oranžna)
boxes = "".join("<div style='aspect-ratio:1;border:5px solid #0E0E0E'></div>" for _ in range(10))
POSTS["12-prvih-10"] = page(f"""
<div class='pad' style='top:100px'><div class='k' style='color:#0E0E0E'>Ustanovni člani</div>
<div class='h' style='font-size:176px;margin-top:22px;color:#0E0E0E'>Prvih 10<br>dobi −30 %</div></div>
<div class='pad' style='top:640px;display:grid;grid-template-columns:repeat(5,1fr);gap:18px'>{boxes}</div>
<div class='pad' style='top:1020px'><div style='font:700 32px/1.4 Inter;color:#0E0E0E'>3 mesece −30 % · majica Hungry Goat gratis<br>Cena ostane zaklenjena, dokler treniraš.</div></div>""",
    bg="#FF5A1F").replace("<div class='grain'></div>", "<div class='grain' style='mix-blend-mode:multiply;opacity:.14'></div>" + foot(dark=True))

# profilna slika
PROFILE = f"<!doctype html><html><head><style>html,body{{margin:0;width:1080px;height:1080px;background:#0E0E0E;display:grid;place-items:center}}</style></head><body><img src='{LOGO}/glavni-logotip.svg' style='width:940px'></body></html>"

with sync_playwright() as pw:
    exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    b = pw.chromium.launch(executable_path=exe) if os.path.exists(exe) else pw.chromium.launch()
    for name, html in list(POSTS.items()) + [("00-profilna-slika", PROFILE)]:
        f = TMP / f"{name}.html"
        f.write_text(html, encoding="utf-8")
        h = 1080 if name.startswith("00") else 1350
        pg = b.new_page(viewport={"width": 1080, "height": h})
        pg.goto(f.as_uri())
        pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(200)
        png = TMP / f"{name}.png"
        pg.screenshot(path=str(png))
        pg.close()
        Image.open(png).convert("RGB").save(OUT / f"{name}.jpg", quality=95)
        print("✓", name)
    b.close()
