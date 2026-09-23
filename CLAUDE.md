# Hungry Goat — projekt Sadless Media

Uporabnik je Mihael Klevže (Sadless Media, Maribor), ki vodi Instagram, snemanje in spletno stran za stranko **Hungry Goat**. Z uporabnikom komuniciraj v slovenščini; dokumenti za stranko uporabljajo vikanje.

## Stranka
- Hungry Goat: licenciran osebni trener iz Maribora, trenira v **TNT Gym**. Ciljna skupina 25–50 let.
- Storitve: osebni treningi 1 na 1, online coaching, skupinske vadbe. Ločena znamka oblačil Hungry Goat Clothing (@hungrygoat.clothing).
- Domena **hungrygoat.com** (Neoserv, SSL, Oranžni paket). Spletna trgovina pride kasneje (WooCommerce na Neoservu).
- Paketa Sadless Media: Začetek 290 €/mesec, Rast 490 €/mesec. Cena spletne strani (590 €, s paketom Rast 490 €) je predlog, ki ga uporabnik še ni potrdil.

## Znamka
- Barve: črna `#0E0E0E`, kost-bela `#F2EEE6`, oranžna `#FF5A1F`. Pisavi Anton (naslovi) in Inter.
- Slogan: »Ostani lačen. Postani GOAT.« / »Stay hungry. Become a GOAT.«
- Prehrana v vsebinah **brez štetja kalorij** (porcije z dlanjo/pestjo).
- Pri fotografijah se mora videti obraz ali vaja, nikoli samo noge. Na nekaterih fotografijah je napis »KingsBox«.
- Izjave strank na spletni strani so primeri — pred objavo jih je treba zamenjati s pravimi ali odstraniti.

## Struktura
- `index.html` — spletna stran (SL/EN), `?static` za posnetke zaslona.
- `shop.html` — mockup trgovine.
- `img/` — obdelane fotografije, `img/logo/` prosojni logotipi, `img/products/` mockupi izdelkov.
- `slike 2048px/` — originalne fotografije s fotografiranja.
- `mockups/studio.html` + `render.ps1` — izris mockupov oblačil (`?p=<ključ>`, `?print=<ključ>`).
- `mockups/pdf/` — izdelava PDF predstavitev: `src/*.md` (izvoz iz dokumentov na claude.ai), `doc.html`, `build.py`, `capture.py`, `cuts.py`, `covers.py`.
- `Predstavitev/` — končni PDF-ji za stranko.
- `cgp/` — celostna grafična podoba in Drop 02 (fitnes × metal): `designs.py` (napisni logotipi, znaki, motivi za majice; vse v vektorju, besedilo v krivuljah), `mockups.py` (majice, jopa s kozjimi rogovi na kapuci), `lib.py` (pisave → krivulje, generator rogov, ročka), `export.py` (PNG za tisk 3600 px v `tisk/`, mockupi JPG v `mockupi/`), `predstavitev/` (stran za claude.ai). Zahteva `pip install fonttools uharfbuzz skia-pathops pillow playwright`. Pisave v `cgp/fonts/` (OFL). Barve za tisk: `WAYS=black,bone,orange python designs.py`.

Lokalni strežnik: `python -m http.server 8080` v korenu projekta (glej `.claude/launch.json`). Skripte za PDF in mockupe zahtevajo Chrome in tečejo na računalniku uporabnika.

## Dokumenti na claude.ai
- Predlog sodelovanja + Vsebinski brief: https://claude.ai/code/artifact/027e7200-019c-4e59-9fd3-210c475b55a7
- Scenariji za reelse in fotografije: https://claude.ai/code/artifact/1c145fe9-e52a-40df-a2bb-4749e5722b12
- Hungry Goat Clothing – ponudba in trgovina: https://claude.ai/code/artifact/d7a0d4b2-afe8-48d2-89f8-5276c95fb387
- Hungry Goat CGP (napisni logotip, znaki, majice, jopa Horns): https://claude.ai/artifact/LyWJiju6krzeDG4DE49HwY
