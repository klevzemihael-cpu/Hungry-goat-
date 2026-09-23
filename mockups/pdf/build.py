"""Sestavi PDF-je za predstavitev v mapo Predstavitev (zahteva strežnik na :8080)."""
import subprocess, sys
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = Path(__file__).resolve().parents[2] / "Predstavitev"
OUT.mkdir(exist_ok=True)

FILES = {
    "01 Predlog sodelovanja in vsebinski brief": "predlog,brief",
    "02 Scenariji za reelse in fotografije": "scenariji",
    "03 Hungry Goat Clothing – ponudba in trgovina": "trgovina",
    "04 Spletna stran in trgovina – predogled": "web",
    "05 Kolekcija Drop 01 – lookbook": "look",
    "00 Hungry Goat – celotna predstavitev": "predlog,brief,scenariji,trgovina,web,look",
}
only = sys.argv[1:]
for name, docs in FILES.items():
    if only and not any(o in name for o in only):
        continue
    pdf = OUT / f"{name}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw",
                    f"--print-to-pdf={pdf}", f"http://localhost:8080/mockups/pdf/doc.html?docs={docs}"],
                   capture_output=True)
    print("OK" if pdf.exists() else "NAPAKA", pdf.name, f"{pdf.stat().st_size // 1024} KB" if pdf.exists() else "")
