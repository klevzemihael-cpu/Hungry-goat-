# Hungry Goat — projekt Sadless Media

Uporabnik je Mihael Klevže (Sadless Media, Maribor), ki vodi Instagram, snemanje in spletno stran za stranko **Hungry Goat**. Z uporabnikom komuniciraj v slovenščini; dokumenti za stranko uporabljajo vikanje.

## Stranka
- Hungry Goat: licenciran osebni trener iz Maribora, trenira v **TNT Gym**. Ciljna skupina 25–50 let.
- Storitve: osebni treningi 1 na 1, online coaching, skupinske vadbe. Ločena znamka oblačil Hungry Goat Clothing (@hungrygoat.clothing).
- Gostovanje pri Neoservu (cPanel, uporabnik `hungrygoat`, SSL, Oranžni paket); coming soon stran je naložena v `public_html` (16. 10. 2026). Domena **hungrygoat.com** je od stranke, a je registrirana pri **Squarespace** (prej Google Domains, imenski strežniki ns-cloud-c1–c4.googledomains.com); v Moj NEOSERV je le dodana (gumb »Prenos k nam«), DNS na Neoserv še ne kaže (16. 10. 2026: A @ in www → 50.193.61.124, MX → Mailgun). Za prikaz strani je treba pri Squarespace A zapisa @ in www preusmeriti na IP gostovanja Neoserv (cPanel → Shared IP Address) ali domeno prenesti k Neoservu. Spletna trgovina pride kasneje (WooCommerce na Neoservu).
- Paketa Sadless Media: Začetek 290 €/mesec, Rast 490 €/mesec. Cena spletne strani (590 €, s paketom Rast 490 €) je predlog, ki ga uporabnik še ni potrdil.

## Znamka
- **Glavni logotip (od 14. 10. 2026):** okrogel znak s kozlom, monogramom HG in napisom HUNGRY GOAT (`Logotipi/glavni-logotip*.svg`, `img/logo/logo-*.png`). Stari logotip (kozel s prekrižanimi rokami) je samo še v `Logotipi/arhiv/` in `img/logo/arhiv/` – ne uporabljaj ga več. Na glavni logotip ne dodajaj rogov.
- Barve: črna `#0E0E0E`, kost-bela `#F2EEE6`, oranžna `#FF5A1F`. Pisavi Anton (naslovi) in Inter.
- Slogan: »Ostani lačen. Postani GOAT.« / »Stay hungry. Become a GOAT.«
- Prehrana v vsebinah **brez štetja kalorij** (porcije z dlanjo/pestjo).
- Pri fotografijah se mora videti obraz ali vaja, nikoli samo noge. Na nekaterih fotografijah je napis »KingsBox«.
- Izjave strank na spletni strani so primeri — pred objavo jih je treba zamenjati s pravimi ali odstraniti.

## Struktura
- `index.html` — spletna stran (SL/EN), `?static` za posnetke zaslona.
- `shop.html` — mockup trgovine.
- `coming-soon/` — začasna stran za hungrygoat.com: samo napis COMING SOON na črnem in majhen glavni logotip spodaj, nič drugega (uporabnik želi popolnoma minimalistično, da se ne ve, kaj bo – brez imena, fotografij in podatkov). En sam `index.html` z vdelano pisavo in logotipom (SVG); naloži se v `public_html` na Neoservu. Predogled: https://klevzemihael-cpu.github.io/Hungry-goat-/coming-soon/
- `img/` — obdelane fotografije, `img/logo/` glavni logotip v PNG (`logo-badge` original, `logo-white`/`logo-orange` za temne podlage, `logo-black` za svetle), `img/products/` mockupi izdelkov.
- `slike 2048px/` — originalne fotografije s fotografiranja.
- `mockups/studio.html` + `render.ps1` — izris mockupov oblačil (`?p=<ključ>`, `?print=<ključ>`).
- `mockups/pdf/` — izdelava PDF predstavitev: `src/*.md` (izvoz iz dokumentov na claude.ai), `doc.html`, `build.py`, `capture.py`, `cuts.py`, `covers.py`.
- `Predstavitev/` — končni PDF-ji za stranko.
- `Dizajni PNG/` — vsi dizajni za tisk kot prosojni PNG (3000–3600 px) po mapah + Instagram in fotografije izdelkov.
- `Logotipi/` — vsi logotipi v SVG z jasnimi imeni. Glavni logotip (vir `img/logo/glavni-logotip-vir.png`, poslal uporabnik) vektorizira `cgp/vectorize_logo.py` (potrace, prosojno ozadje) in izdela tudi PNG v `img/logo/`. Po spremembi logotipa ponovno zaženi `premium.py`, `women.py`, `designs.py stay-hungry-metal ostani-lacen goat-acronym`, `mockups.py` + `export.py mock` in mockupe izdelkov iz `mockups/studio.html`. `img/brand/` — metal napisi (SVG) za spletno stran; `cgp/instagram/` — naslovnice izpostavljenih zgodb in predloga objave.
- `cgp/` — celostna grafična podoba in Drop 02 (fitnes × metal): `designs.py` (napisni logotipi, znaki, motivi za majice; vse v vektorju, besedilo v krivuljah), `mockups.py` (majice, jopa s kozjimi rogovi na kapuci), `lib.py` (pisave → krivulje, generator rogov, ročka), `export.py` (PNG za tisk 3600 px v `tisk/`, mockupi JPG v `mockupi/`), `predstavitev/` (stran za claude.ai). Zahteva `pip install fonttools uharfbuzz skia-pathops pillow playwright`. Pisave v `cgp/fonts/` (OFL). Barve za tisk: `WAYS=black,bone,orange python designs.py`. Metal smer (aktualna, po primerih uporabnika: black metal/deathcore merch): `bm.py` (napis s konicami, kapljami, trni, graviran rog) in `metal.py` (tiskovine `svg/bm-*.svg`, mockupi `mock/metal-*`). Brez pentagramov in obrnjenih križev, razen če uporabnik izrecno želi.

- `Instagram objave/` — prvih 12 objav za @hungrygoat (16 slik 1080×1350, profilna slika z logotipom HG, `izpostavljene/`). Izdelava: `python cgp/ig_prep.py <mapa>` (obrez 4:5, zabris napisa KingsBox, barvna obdelava fotografij iz `slike 2048px/`), nato `python cgp/ig_posts.py <mapa> "Instagram objave"`. Stran z načrtom: `cgp/predstavitev-instagram/`.

Lokalni strežnik: `python -m http.server 8080` v korenu projekta (glej `.claude/launch.json`). Skripte za PDF in mockupe zahtevajo Chrome in tečejo na računalniku uporabnika.

## Dokumenti na claude.ai
- Predlog sodelovanja + Vsebinski brief: https://claude.ai/code/artifact/027e7200-019c-4e59-9fd3-210c475b55a7
- Scenariji za reelse in fotografije: https://claude.ai/code/artifact/1c145fe9-e52a-40df-a2bb-4749e5722b12
- Hungry Goat Clothing – ponudba in trgovina: https://claude.ai/code/artifact/d7a0d4b2-afe8-48d2-89f8-5276c95fb387
- Hungry Goat CGP (prva, čista smer – uporabnik jo je zavrnil kot preveč šablonsko): https://claude.ai/artifact/LyWJiju6krzeDG4DE49HwY
- Hungry Goat Metal (black metal napis, jopa z rogovi na kapuci – aktualna smer): https://claude.ai/artifact/Cs2jRhmu8mNRHbbus79JfP
- Scenariji snemanja – metal smer (reelsi za stranke, cinematic, prehrana, lansiranje obleke, oglasi, urnik): https://claude.ai/code/artifact/be9fe914-5563-417d-8c1a-990f375c743c
- Instagram @hungrygoat (predogled profila, 12 objav z opisi, načrt zagona iz nule): https://claude.ai/artifact/1hLRLUQVTABzQrZU6W3M2D
- Predogled spletne strani (veja gh-pages): https://klevzemihael-cpu.github.io/Hungry-goat-/
- Canva (račun uporabnika), fotorealistični mockupi: jopa spredaj MAHWU2dR0t4, jopa zadaj MAHWU3ITocQ, Barbell Club MAHWU7TgAcY, Feed the Beast MAHWU6meJcM, Earn Your Horns MAHWU7fly2c, majica metal napis MAHWU7DmSKM, kapa s šiltom MAHWUwpJyoE, zimska kapa MAHWU2Nutvw; ilustracija kozla MAHWB6D0GX8, jopa studio MAHWCPwljG0, jopa na modelu MAHWCF5kFQE, majica s kozlom MAHWCOimzx8. media.canva.com je v okolju blokiran.
