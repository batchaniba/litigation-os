#!/usr/bin/env python3
"""Matter 29 — Plaintiff-executed counterpart of the Amazon response extension.

Andrew P. Frederick (Morgan Lewis) emailed a draft stipulation on August 31,
2026, and asked for permission to apply Plaintiff's e-signature and file.
This script does not stamp counsel's .docx (that file was not in the Gmail
print). It renders a Civil L.R. 6-1(a) counterpart from the terms already
agreed on the email record: Amazon.com Services, LLC only, through and
including September 22, 2026. Plaintiff signs his own paper.

  python3 internal/scripts/matter29-amazon-extension-stipulation.py
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import (  # noqa: E402
    SIGNATURE_ASPECT,
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
)

ROOT = SCRIPT_DIR.parent
MATTER29 = ROOT / "public/documents/matter-29"
OUT_STIP = MATTER29 / (
    "Stipulation to Extend Time for Amazon to Respond "
    "(Plaintiff Counterpart, Aug 31 2026).pdf"
)
OUT_DOCX = MATTER29 / (
    "Stipulation to Extend Time for Amazon to Respond "
    "(Plaintiff Counterpart, Aug 31 2026).docx"
)

EXEC_DATE = "August 31, 2026"
CASE_NO = "3:26-cv-09249-ASK"
FOOTER = "STIPULATION TO EXTEND TIME -- NEWANFORBI v. AMAZON.COM SERVICES, LLC"

ATTY = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()


SIG_LINE = "___________________________________"


def _plaintiff_sign_block(d: PleadingPaper) -> None:
    """Date on the left, loops mark on the right-hand line.

    House stamp: 220-pt width, default height scale. Blank lines keep
    the mark off the date.
    """
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.blank_line()
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=220,
        x_offset=15,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)


def build_stipulation(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=FOOTER)
    _header(d)
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("AMAZON.COM SERVICES, LLC;", True, False),
        ("ACCURATE BACKGROUND LLC; and", True, False),
        ("DOES 1–10, inclusive,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        (f"Case No. {CASE_NO}", False, False),
        ("", False, False),
        ("STIPULATION TO EXTEND TIME", True, False),
        ("FOR AMAZON.COM SERVICES, LLC", True, False),
        ("TO RESPOND TO THE COMPLAINT", True, False),
        ("[Civil L.R. 6-1(a);", True, False),
        ("Fed. R. Civ. P. 6(b)(1)(A), 81(c)]", True, False),
        ("", False, False),
        ("Judge: Hon. Ajay S. Krishnan", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("STIPULATION TO EXTEND TIME", bold=True, center=True)
    d.write_line("(Amazon.com Services, LLC Only)", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendant Amazon.com Services, LLC, through its counsel of record, "
        "stipulate as follows:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "1. Amazon.com Services, LLC removed this action on August 31, 2026. "
        "Under Fed. R. Civ. P. 81(c)(2), its time to answer or otherwise respond "
        "to the Complaint is September 8, 2026.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2. The parties agree to extend that deadline, as to Amazon.com "
        "Services, LLC only, through and including September 22, 2026.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3. This extension does not apply to Defendant Accurate Background LLC "
        "or to any other party. Accurate Background LLC’s deadline is unchanged.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "4. This is a single extension. It does not alter any date set by Court "
        "order. No further extension is implied. It does not waive any defense, "
        "objection, or right of any party, including Plaintiff’s right to seek "
        "default if no timely response is filed.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "5. This stipulation is made under Civil L.R. 6-1(a) and shall be "
        "promptly filed pursuant to Civil L.R. 5. No Court order is required.",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("IT IS SO STIPULATED.", bold=True, center=True)
    d.blank_line()
    _plaintiff_sign_block(d)
    d.blank_line()
    d.ensure_space(7)
    d.write_line("Dated: ________________")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("ANDREW P. FREDERICK (SBN 284832)", bold=True, right=True, right_margin_offset=20)
    d.write_line("Morgan, Lewis & Bockius LLP", right=True, right_margin_offset=20)
    d.write_line("Attorneys for Defendant", right=True, right_margin_offset=20)
    d.write_line("Amazon.com Services, LLC", right=True, right_margin_offset=20)
    d.save()


def build_docx(path: Path) -> None:
    """Word counterpart for counsel's e-filing workflow. Same terms, same
    date, same house-scale signature. No 5-1(i) attestation."""
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt
    except ImportError:
        import os

        os.system(f"{sys.executable} -m pip install -q python-docx")
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt

    font_name = "Times New Roman"
    size = Pt(12)
    sig_width = Inches(220 / 72)
    sig_height = Inches((220 / 72) * SIGNATURE_ASPECT)

    def set_run(run, *, bold=False, italic=False, run_size=size):
        run.font.name = font_name
        run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
        run.font.size = run_size
        run.bold = bold
        run.italic = italic

    def add_para(
        document,
        text="",
        *,
        bold=False,
        center=False,
        right=False,
        double=False,
        run_size=size,
    ):
        p = document.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        if double:
            pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        else:
            pf.line_spacing = 1.0
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif right:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if text:
            run = p.add_run(text)
            set_run(run, bold=bold, run_size=run_size)
        return p

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run(
        f"Case No. {CASE_NO}  —  STIPULATION TO EXTEND TIME (Amazon only)"
    )
    set_run(run, run_size=Pt(9))

    for line, fn, _sz in ATTY:
        add_para(doc, line, bold=("Bold" in fn))
    add_para(doc, "")
    add_para(doc, "UNITED STATES DISTRICT COURT", bold=True, center=True)
    add_para(doc, "NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    add_para(doc, "")

    table = doc.add_table(rows=1, cols=2)
    left, right = table.rows[0].cells
    left_lines = [
        ("BRENDAN NGEHSI NEWANFORBI,", True),
        ("          Plaintiff,", False),
        ("", False),
        ("     v.", False),
        ("", False),
        ("AMAZON.COM SERVICES, LLC;", True),
        ("ACCURATE BACKGROUND LLC; and", True),
        ("DOES 1–10, inclusive,", True),
        ("          Defendants.", False),
    ]
    right_lines = [
        (f"Case No. {CASE_NO}", False),
        ("", False),
        ("STIPULATION TO EXTEND TIME", True),
        ("FOR AMAZON.COM SERVICES, LLC", True),
        ("TO RESPOND TO THE COMPLAINT", True),
        ("[Civil L.R. 6-1(a);", True),
        ("Fed. R. Civ. P. 6(b)(1)(A), 81(c)]", True),
        ("", False),
        ("Judge: Hon. Ajay S. Krishnan", False),
    ]
    for cell, lines in ((left, left_lines), (right, right_lines)):
        cell.text = ""
        for i, (text, bold) in enumerate(lines):
            p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(text)
            set_run(run, bold=bold, run_size=Pt(11))

    add_para(doc, "")
    add_para(doc, "STIPULATION TO EXTEND TIME", bold=True, center=True)
    add_para(doc, "(Amazon.com Services, LLC Only)", bold=True, center=True)
    add_para(doc, "")
    add_para(
        doc,
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendant Amazon.com Services, LLC, through its counsel of record, "
        "stipulate as follows:",
        double=True,
    )
    for text in (
        "1. Amazon.com Services, LLC removed this action on August 31, 2026. "
        "Under Fed. R. Civ. P. 81(c)(2), its time to answer or otherwise respond "
        "to the Complaint is September 8, 2026.",
        "2. The parties agree to extend that deadline, as to Amazon.com "
        "Services, LLC only, through and including September 22, 2026.",
        "3. This extension does not apply to Defendant Accurate Background LLC "
        "or to any other party. Accurate Background LLC’s deadline is unchanged.",
        "4. This is a single extension. It does not alter any date set by Court "
        "order. No further extension is implied. It does not waive any defense, "
        "objection, or right of any party, including Plaintiff’s right to seek "
        "default if no timely response is filed.",
        "5. This stipulation is made under Civil L.R. 6-1(a) and shall be "
        "promptly filed pursuant to Civil L.R. 5. No Court order is required.",
    ):
        add_para(doc, text, double=True)
    add_para(doc, "")
    add_para(doc, "IT IS SO STIPULATED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, f"Dated: {EXEC_DATE}")
    add_para(doc, "")
    add_para(doc, "")
    sig_p = add_para(doc, "", right=True)
    run = sig_p.add_run()
    run.add_picture(SIGNATURE_PATH, width=sig_width, height=sig_height)
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, "BRENDAN NGEHSI NEWANFORBI", bold=True, right=True)
    add_para(doc, "Plaintiff, In Pro Per", right=True)
    add_para(doc, "")
    add_para(doc, "Dated: ________________")
    add_para(doc, "")
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, "ANDREW P. FREDERICK (SBN 284832)", bold=True, right=True)
    add_para(doc, "Morgan, Lewis & Bockius LLP", right=True)
    add_para(doc, "Attorneys for Defendant", right=True)
    add_para(doc, "Amazon.com Services, LLC", right=True)
    doc.save(str(path))


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    build_stipulation(OUT_STIP)
    print(f"Wrote {OUT_STIP}")
    build_docx(OUT_DOCX)
    print(f"Wrote {OUT_DOCX}")


if __name__ == "__main__":
    main()
