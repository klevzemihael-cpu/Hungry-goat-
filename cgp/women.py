"""Ženska linija: napisi za pas pajkic, nogo, crop top in modrček.  python women.py"""
import os, random
from lib import *
from bm import *
from render import render
from premium import logo, txt, centered, save, INTER, INTER6
jobs = []
# 1) pas pajkic – dolg trak
line = centered(bm_one_line("HUNGRY GOAT", seed=110, size=120), 0, 0)
parts = []
x = 0
body = ""
for i in range(3):
    s = line.move(x - line.bounds[0], 40 - line.bounds[1])
    body += s.svg(BONE)
    x = s.bounds[2] + 60
    body += star4(x, 40 + line.h / 2, 14).svg(ORANGE)
    x += 60
jobs.append(save("w-band", round(x), round(line.h + 80), body))
# 2) SHE IS THE GOAT – crop top / hrbet
rng = random.Random(111)
a, _, c = metal_line("SHE IS THE", 150, 0, 0, rng, lambda x: .3 + 1.1 * min(1, abs(x) / 420) ** 2, top_len=(.3, .8), drip_prob=.3)
b, _, _ = metal_line("GOAT", 330, 0, c + 250, rng, lambda x: .12, top_len=(.2, .35), drip_len=(.15, .7), drip_prob=.9)
g = centered(roughen(warp(a, arch(0, .0005)) | b, amp=1.8, seed=111), 500, 60, 860)
body = g.svg(BONE) + txt("STRONG  ·  FED  ·  UNSTOPPABLE", 520, 500, g.bounds[3] + 80).svg(ORANGE)
jobs.append(save("w-shegoat", 1000, round(g.bounds[3] + 140), body))
# 3) modrček / crop top spredaj – mali logotip + tanek napis
body = logo(200, 200, 300) + txt("HUNGRY GOAT", 360, 200, 420, INTER, 420).svg(BONE) + txt("EST. 2026", 200, 200, 470, INTER6, 400).svg(ORANGE)
jobs.append(save("w-badge", 400, 500, body))
render(jobs)
