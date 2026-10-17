#!/usr/bin/env python3
"""Render tracked Matter 29 discovery Markdown sources as review DOCX/PDF.

Every ``[[SIGNATURE]]`` paragraph in a source is replaced with Plaintiff's
portfolio signature image (internal/assets/signature/brendan-newanforbi-
signature.png, resolved and guarded through signature_stamp.py, the same
canonical path used by prior filings) sitting on a signature rule above the
typed name. The image is embedded in the DOCX, so the LibreOffice PDF render
carries it as well. Nothing is served; outputs are generated under
internal/docs/matter-29/discovery-set-one/generated/.
"""
from __future__ import annotations
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pypdf import PdfReader, PdfWriter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH, _resolve_stamp_path  # noqa: E402

SIGNATURE_MARKER = "[[SIGNATURE]]"
SIGNATURE_WIDTH_IN = 2.4

ROOT = Path(__file__).resolve().parents[1] / "docs" / "matter-29" / "discovery-set-one"
OUT = ROOT / "generated"
CORE = [p for p in sorted(ROOT.glob("[0-1][0-9]_*.md")) if p.name != "README.md"]


def signature(doc):
    """Signature image on a bottom-bordered line; the typed name follows."""
    path = _resolve_stamp_path(SIGNATURE_PATH)
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(
        path,
        width=Inches(SIGNATURE_WIDTH_IN),
        height=Inches(SIGNATURE_WIDTH_IN * SIGNATURE_ASPECT),
    )
    ppr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"), ("w:color", "000000")):
        bottom.set(qn(k), v)
    borders.append(bottom)
    ppr.append(borders)
    # Limit the rule to the signature width via a right indent.
    usable = doc.sections[0].page_width - doc.sections[0].left_margin - doc.sections[0].right_margin
    p.paragraph_format.right_indent = usable - Inches(SIGNATURE_WIDTH_IN + 0.3)


def paragraph(doc, source: str):
    text = source.strip()
    if not text:
        return
    if text == SIGNATURE_MARKER:
        signature(doc)
        return
    if text.startswith("# "):
        p = doc.add_paragraph(text[2:], style="Heading 1")
    elif text.startswith("## "):
        p = doc.add_paragraph(text[3:], style="Heading 2")
    else:
        p = doc.add_paragraph(style="Normal")
        chunks = re.split(r"(\*\*.*?\*\*)", text)
        for chunk in chunks:
            if chunk.startswith("**") and chunk.endswith("**"):
                r = p.add_run(chunk[2:-2])
                r.bold = True
            else:
                p.add_run(chunk)
        return
    p.paragraph_format.keep_with_next = True


def render_docx(source: Path, destination: Path):
    d = Document()
    sec = d.sections[0]
    sec.top_margin = Inches(0.79)
    sec.bottom_margin = Inches(0.7)
    sec.left_margin = Inches(0.94)
    sec.right_margin = Inches(0.94)
    styles = d.styles
    styles["Normal"].font.name = "Times New Roman"
    styles["Normal"].font.size = Pt(11)
    styles["Normal"].paragraph_format.space_after = Pt(5)
    styles["Normal"].paragraph_format.line_spacing = 1.12
    for hname in ("Heading 1", "Heading 2"):
        styles[hname].font.name = "Times New Roman"
        styles[hname].font.size = Pt(11)
        styles[hname].font.bold = True
        styles[hname].font.color.rgb = RGBColor(0, 0, 0)
    hdr = sec.header.paragraphs[0]
    hdr.text = "CASE NO. 4:26-cv-09249-ASK | DISCOVERY DRAFT — NOT FOR FILING"
    hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in hdr.runs:
        run.font.size = Pt(8)
    f = sec.footer.paragraphs[0]
    f.text = "Matter 29 — REVIEW DRAFT — NOT SERVED"
    f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in f.runs:
        run.font.size = Pt(8)
    for block in re.split(r"\n\s*\n", source.read_text(encoding="utf-8")):
        paragraph(d, block)
    d.save(destination)


def combine(paths: list[Path], destination: Path):
    writer = PdfWriter()
    for p in paths:
        for page in PdfReader(str(p)).pages:
            writer.add_page(page)
    with destination.open("wb") as f:
        writer.write(f)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing portfolio signature image: {SIGNATURE_PATH}")
    for source in CORE:
        render_docx(source, OUT / (source.stem + ".docx"))
    if not shutil.which("libreoffice") and not shutil.which("soffice"):
        raise SystemExit("LibreOffice is needed to render PDFs: install libreoffice-writer")
    cmd = shutil.which("libreoffice") or shutil.which("soffice")
    docx_files = [OUT / (p.stem + ".docx") for p in CORE]
    subprocess.run([cmd, "-env:UserInstallation=file:///tmp/m29-lo-profile", "--headless", "--convert-to", "pdf", "--outdir", str(OUT), *map(str, docx_files)], check=True, timeout=240)
    pdf_files = [OUT / (p.stem + ".pdf") for p in CORE]
    absent = [str(p) for p in pdf_files if not p.exists()]
    if absent:
        raise RuntimeError("Missing PDF renders: " + ", ".join(absent))
    combine(pdf_files, OUT / "Matter_29_Complete_Discovery_Packet.pdf")
    amazon = [OUT / (p + ".pdf") for p in ("01_Amazon_RFP_Set_One", "03_Amazon_Interrogatories_Set_One", "05_Amazon_RFA_Set_One")]
    accurate = [OUT / (p + ".pdf") for p in ("02_Accurate_RFP_Set_One", "04_Accurate_Interrogatories_Set_One", "06_Accurate_RFA_Set_One")]
    combine(amazon, OUT / "Matter_29_Amazon_Discovery_Combined.pdf")
    combine(accurate, OUT / "Matter_29_Accurate_Discovery_Combined.pdf")
    zip_path = OUT / "Matter_29_Complete_Discovery_Packet_DOCX_PDF.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.glob("*.docx")) + sorted(OUT.glob("*.pdf")):
            z.write(p, arcname=p.name)
        z.write(ROOT / "12_Cover_Email_Templates_NOT_SENT.txt", arcname="12_Cover_Email_Templates_NOT_SENT.txt")
        z.write(ROOT / "package_manifest.json", arcname="package_manifest.json")
    print(f"Built {len(docx_files)} DOCX, {len(pdf_files)} PDFs, and 3 combined PDFs; archive: {zip_path}")


if __name__ == "__main__":
    main()
