# utils/generate_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import json
import textwrap

INPUT = "../data/competences.json"
OUTPUT = "../competences_catalogue.pdf"

def draw_wrapped_text(c, text, x, y, max_width, leading=12):
    lines = []
    for paragraph in text.split("\n"):
        wrapped = textwrap.wrap(paragraph, width=80)
        if not wrapped:
            lines.append("")
        else:
            lines.extend(wrapped)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y

def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    c = canvas.Canvas(OUTPUT, pagesize=A4)
    width, height = A4
    margin = 18*mm
    y = height - margin

    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, y, "Catalogue des compétences — Book d'apprentissage")
    y -= 14*mm

    c.setFont("Helvetica", 10)
    # grouper par categorie -> semestre
    cats = {}
    for comp in data.get("competences", []):
        cat = comp.get("categorie","Autre")
        cats.setdefault(cat, []).append(comp)

    for cat, comps in cats.items():
        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin, y, f"{cat}")
        y -= 8*mm
        # trier par semestre
        comps_sorted = sorted(comps, key=lambda x: x.get("semestre", 0))
        for comp in comps_sorted:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin+6*mm, y, f"- {comp.get('titre')} (S{comp.get('semestre','-')})")
            y -= 6*mm
            c.setFont("Helvetica", 9)
            y = draw_wrapped_text(c, "Description: " + comp.get("description_popup","-"), margin+10*mm, y, width - 2*margin, leading=12)
            y -= 2*mm
            proofs = comp.get("preuve","-")
            y = draw_wrapped_text(c, "Preuves / exemples: " + proofs, margin+10*mm, y, width - 2*margin, leading=12)
            y -= 6*mm
            if y < margin+40*mm:
                c.showPage()
                y = height - margin

        y -= 6*mm

    c.save()
    print("PDF généré:", OUTPUT)

if __name__ == "__main__":
    main()
