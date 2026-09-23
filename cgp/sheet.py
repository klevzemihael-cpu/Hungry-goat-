"""Pregledna pola: python sheet.py <izhod.png> [stolpci] – prikaže svg/_jobs.json."""
import json, os, sys
from render import render

HERE = os.path.dirname(os.path.abspath(__file__))
BG = {"black": "#0E0E0E", "bone": "#F2EEE6", "orange": "#FF5A1F", "ash": "#6F6A63"}

jobs = json.load(open(os.path.join(HERE, os.environ.get("JOBS", "svg/_jobs.json"))))
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 2
cells = "".join(
    f'<div style="background:{BG[way]}"><img src="{os.path.relpath(p, HERE)}"><span>{os.path.basename(p)}</span></div>'
    for p, w, h, way in jobs)
html = f"""<style>body{{margin:0;display:grid;grid-template-columns:repeat({cols},1fr);gap:4px;background:#555}}
div{{height:520px;display:flex;align-items:center;justify-content:center;position:relative}}
img{{max-width:86%;max-height:84%}}span{{position:absolute;left:8px;bottom:6px;font:12px sans-serif;color:#888}}</style>{cells}"""
open(os.path.join(HERE, "_sheet.html"), "w").write(html)
rows = -(-len(jobs) // cols)
render([(os.path.join(HERE, "_sheet.html"), sys.argv[1], 1400, rows * 524, 1, False)])
