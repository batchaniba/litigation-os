#!/usr/bin/env python3
"""Matter 27 — Plaintiff counterpart of the Randstad response extension.

LOCKED stipulation posture: .claude/skills/stipulation-defense/TEMPLATE.md
and SKILL.md. Portfolio-wide. Do not stamp counsel's Word. Plaintiff signs
his own paper. Named party only. Single shot. Default reserved.

Chadwick L. Williams (Kabat Chapman & Ozmer LLP) emailed a draft stipulation
and proposed order on September 14, 2026, 2:03 p.m., and asked permission to
add Plaintiff's e-signature and file. Counsel's caption still names Hon.
Karin Schwartz. Operative assignment is Hon. Thomas Weathers, Dept. 20.

This script does not edit counsel's .docx (labeled DO NOT SIGN in the
document store). It renders a CRC 3.110(d) / CCP § 1054 counterpart from
the number Plaintiff already put in writing on September 12: Randstad US,
LLC only, through and including September 18, 2026. A second extension
needs a court order. The proposed order is no broader than the stipulation.

Plaintiff e-signs both the PDF and the Word file as
"/s/ Brendan Ngehsi Newanforbi". Do not embed the loops stamp — Word was
cropping it.

  python3 internal/scripts/matter27-randstad-extension-stipulation.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402

ROOT = SCRIPT_DIR.parent
MATTER27 = ROOT / "public/documents/matter-27"
OUT_STIP = MATTER27 / (
    "Stipulation to Extend Time for Randstad to Respond "
    "(Plaintiff Counterpart, Sep 14 2026).pdf"
)
OUT_STIP_DOCX = MATTER27 / (
    "Stipulation to Extend Time for Randstad to Respond "
    "(Plaintiff Counterpart, Sep 14 2026).docx"
)
OUT_ORDER = MATTER27 / (
    "[Proposed] Order Extending Time for Randstad to Respond "
    "(Plaintiff Counterpart, Sep 14 2026).pdf"
)
OUT_ORDER_DOCX = MATTER27 / (
    "[Proposed] Order Extending Time for Randstad to Respond "
    "(Plaintiff Counterpart, Sep 14 2026).docx"
)

EXEC_DATE = "September 14, 2026"
CASE_NO = "26CV199902"
STIP_FOOTER = (
    "STIPULATION TO EXTEND TIME -- NEWANFORBI v. RANDSTAD US, LLC "
    f"(Alameda {CASE_NO})"
)
ORDER_FOOTER = (
    "[PROPOSED] ORDER EXTENDING TIME -- NEWANFORBI v. RANDSTAD US, LLC "
    f"(Alameda {CASE_NO})"
)

ATTY = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

SIG_LINE = "___________________________________"

STIP_PARAS = (
    "1. Defendant Randstad US, LLC was served with the Summons and Complaint "
    "on July 30, 2026. By written party agreement dated August 18, 2026, "
    "Plaintiff and Randstad stipulated without leave of court to one 15-day "
    "extension of Randstad's time to respond, through and including September "
    "15, 2026. That was the single 15-day extension California Rules of Court, "
    "rule 3.110(d), allows without leave of court. Randstad's time to answer, "
    "demur, or otherwise respond is therefore September 15, 2026, unless this "
    "Court orders a further extension.",
    "2. The parties agree to extend that deadline, as to Randstad US, LLC "
    "only, through and including September 18, 2026.",
    "3. This extension does not apply to Defendant The RK Logistics Group, "
    "Inc. or to any other party. The RK Logistics Group, Inc.'s deadline is "
    "unchanged by this stipulation.",
    "4. This is a single extension. It does not alter any date set by Court "
    "order, including the December 17, 2026 case management conference. No "
    "further extension is implied. Any additional extension would need to be "
    "agreed separately, in writing, and presented to the Court. It does not "
    "waive any defense, objection, or right of any party, including "
    "Plaintiff's right to seek default if no timely response is filed. This "
    "stipulation continues the response deadline only. It is not a stay of "
    "discovery, not a settlement, not a release, and not an acceptance of any "
    "settlement demand.",
    "5. As consideration for this single extension, Randstad shall promptly "
    "file this stipulation and the proposed order lodged with it, and shall "
    "not seek any further extension of its time to respond except by order of "
    "the Court.",
    "6. This stipulation is made under California Rules of Court, rule "
    "3.110(d), and Code of Civil Procedure section 1054. Because the August "
    "18, 2026 extension already used the one 15-day enlargement rule 3.110(d) "
    "allows without leave, a proposed order is lodged. The proposed order is "
    "no broader than these terms. Court approval is required. This "
    "stipulation is not an operative deadline until it is signed, filed, and "
    "the Court enters an order.",
)

ORDER_PARAS = (
    "The Court has considered the Stipulation of Plaintiff Brendan Ngehsi "
    "Newanforbi and Defendant Randstad US, LLC to extend Randstad's time to "
    "respond to the Complaint. IT IS ORDERED:",
    "1. Defendant Randstad US, LLC's time to answer, demur, or otherwise "
    "respond to the Complaint is extended through and including September 18, "
    "2026.",
    "2. This Order applies to Randstad US, LLC only. It does not apply to "
    "Defendant The RK Logistics Group, Inc. or to any other party. The RK "
    "Logistics Group, Inc.'s deadline is unchanged by this Order.",
    "3. This is a single extension. It does not alter any other date set by "
    "Court order, including the December 17, 2026 case management conference. "
    "No further extension is implied.",
    "4. Nothing in the stipulation or this Order waives any defense, "
    "objection, or right of any party, including Plaintiff's right to seek "
    "default if no timely response is filed.",
)


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    d.write_line(
        "COUNTY OF ALAMEDA — RENE C. DAVIDSON COURTHOUSE",
        bold=True,
        center=True,
    )
    d.blank_line()


def _caption(d: PleadingPaper, right_title: list[tuple[str, bool, bool]]) -> None:
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("RANDSTAD US, LLC;", True, False),
        ("THE RK LOGISTICS GROUP, INC.; and", True, False),
        ("DOES 1–20, inclusive,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    d.draw_caption_block(left, right_title, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()


def _plaintiff_sign_block(d: PleadingPaper) -> None:
    d.ensure_space(6)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.blank_line()
    d.write_line("/s/ Brendan Ngehsi Newanforbi", bold=True)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")


def _counsel_sign_block(d: PleadingPaper) -> None:
    d.blank_line()
    d.ensure_space(7)
    d.write_line("Dated: ________________")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("NATHAN D. CHAPMAN (SBN 338735)", bold=True, right=True, right_margin_offset=20)
    d.write_line("Kabat Chapman & Ozmer LLP", right=True, right_margin_offset=20)
    d.write_line("Attorneys for Defendant", right=True, right_margin_offset=20)
    d.write_line("Randstad US, LLC", right=True, right_margin_offset=20)


def build_stipulation(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=STIP_FOOTER)
    _header(d)
    _caption(
        d,
        [
            (f"Case No. {CASE_NO}", False, False),
            ("", False, False),
            ("STIPULATION TO EXTEND TIME", True, False),
            ("FOR RANDSTAD US, LLC", True, False),
            ("TO RESPOND TO THE COMPLAINT", True, False),
            ("[Cal. Rules of Court, rule 3.110(d);", True, False),
            ("Code Civ. Proc., § 1054]", True, False),
            ("", False, False),
            ("Judge: Hon. Thomas Weathers", False, False),
            ("Dept. 20", False, False),
            ("[Proposed] Order lodged concurrently", False, False),
        ],
    )
    d.write_line("STIPULATION TO EXTEND TIME", bold=True, center=True)
    d.write_line("(Randstad US, LLC Only)", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendant Randstad US, LLC, through its counsel of record, stipulate "
        "as follows:",
        first_indent=0,
    )
    d.blank_line()
    for para in STIP_PARAS:
        d.write_wrapped(para, first_indent=0)
        d.blank_line()
    d.write_line("IT IS SO STIPULATED.", bold=True, center=True)
    d.blank_line()
    _plaintiff_sign_block(d)
    _counsel_sign_block(d)
    d.save()


def build_order(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=ORDER_FOOTER)
    _header(d)
    _caption(
        d,
        [
            (f"Case No. {CASE_NO}", False, False),
            ("", False, False),
            ("[PROPOSED] ORDER EXTENDING", True, False),
            ("TIME FOR RANDSTAD US, LLC", True, False),
            ("TO RESPOND TO THE COMPLAINT", True, False),
            ("", False, False),
            ("Judge: Hon. Thomas Weathers", False, False),
            ("Dept. 20", False, False),
            ("Complaint filed: July 20, 2026", False, False),
        ],
    )
    d.write_line("[PROPOSED] ORDER", bold=True, center=True)
    d.write_line("(Randstad US, LLC Only)", bold=True, center=True)
    d.blank_line()
    for para in ORDER_PARAS:
        d.write_wrapped(para, first_indent=0)
        d.blank_line()
    d.write_line("IT IS SO ORDERED.", bold=True, center=True)
    d.blank_line()
    d.ensure_space(6)
    d.write_line("Dated: ________________")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("HON. THOMAS WEATHERS", bold=True, right=True, right_margin_offset=20)
    d.write_line("Judge of the Superior Court", right=True, right_margin_offset=20)
    d.save()


def _docx_helpers():
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt
    except ImportError:
        os.system(f"{sys.executable} -m pip install -q python-docx")
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt
    return Document, WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, qn, Inches, Pt


def _docx_common(path: Path, footer_text: str):
    Document, WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, qn, Inches, Pt = _docx_helpers()
    font_name = "Times New Roman"
    size = Pt(12)

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
    run = fp.add_run(footer_text)
    set_run(run, run_size=Pt(9))
    return doc, add_para, set_run, Inches, Pt, WD_ALIGN_PARAGRAPH


def _docx_caption(doc, add_para, set_run, Pt, right_lines):
    for line, fn, _sz in ATTY:
        add_para(doc, line, bold=("Bold" in fn))
    add_para(doc, "")
    add_para(doc, "SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    add_para(
        doc,
        "COUNTY OF ALAMEDA — RENE C. DAVIDSON COURTHOUSE",
        bold=True,
        center=True,
    )
    add_para(doc, "")
    table = doc.add_table(rows=1, cols=2)
    left, right = table.rows[0].cells
    left_lines = [
        ("BRENDAN NGEHSI NEWANFORBI,", True),
        ("          Plaintiff,", False),
        ("", False),
        ("     v.", False),
        ("", False),
        ("RANDSTAD US, LLC;", True),
        ("THE RK LOGISTICS GROUP, INC.; and", True),
        ("DOES 1–20, inclusive,", True),
        ("          Defendants.", False),
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


def build_stip_docx(path: Path) -> None:
    doc, add_para, set_run, Inches, Pt, _align = _docx_common(
        path, f"Case No. {CASE_NO}  —  STIPULATION TO EXTEND TIME (Randstad only)"
    )
    _docx_caption(
        doc,
        add_para,
        set_run,
        Pt,
        [
            (f"Case No. {CASE_NO}", False),
            ("", False),
            ("STIPULATION TO EXTEND TIME", True),
            ("FOR RANDSTAD US, LLC", True),
            ("TO RESPOND TO THE COMPLAINT", True),
            ("[Cal. Rules of Court, rule 3.110(d);", True),
            ("Code Civ. Proc., § 1054]", True),
            ("", False),
            ("Judge: Hon. Thomas Weathers", False),
            ("Dept. 20", False),
        ],
    )
    add_para(doc, "STIPULATION TO EXTEND TIME", bold=True, center=True)
    add_para(doc, "(Randstad US, LLC Only)", bold=True, center=True)
    add_para(doc, "")
    add_para(
        doc,
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendant Randstad US, LLC, through its counsel of record, stipulate "
        "as follows:",
        double=True,
    )
    for text in STIP_PARAS:
        add_para(doc, text, double=True)
    add_para(doc, "")
    add_para(doc, "IT IS SO STIPULATED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, f"Dated: {EXEC_DATE}")
    add_para(doc, "")
    add_para(doc, "/s/ Brendan Ngehsi Newanforbi", bold=True)
    add_para(doc, "BRENDAN NGEHSI NEWANFORBI", bold=True)
    add_para(doc, "Plaintiff, In Pro Per")
    add_para(doc, "")
    add_para(doc, "Dated: ________________")
    add_para(doc, "")
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, "NATHAN D. CHAPMAN (SBN 338735)", bold=True, right=True)
    add_para(doc, "Kabat Chapman & Ozmer LLP", right=True)
    add_para(doc, "Attorneys for Defendant", right=True)
    add_para(doc, "Randstad US, LLC", right=True)
    doc.save(str(path))


def build_order_docx(path: Path) -> None:
    doc, add_para, set_run, _Inches, Pt, _align = _docx_common(
        path, f"Case No. {CASE_NO}  —  [PROPOSED] ORDER EXTENDING TIME (Randstad only)"
    )
    _docx_caption(
        doc,
        add_para,
        set_run,
        Pt,
        [
            (f"Case No. {CASE_NO}", False),
            ("", False),
            ("[PROPOSED] ORDER EXTENDING", True),
            ("TIME FOR RANDSTAD US, LLC", True),
            ("TO RESPOND TO THE COMPLAINT", True),
            ("", False),
            ("Judge: Hon. Thomas Weathers", False),
            ("Dept. 20", False),
            ("Complaint filed: July 20, 2026", False),
        ],
    )
    add_para(doc, "[PROPOSED] ORDER", bold=True, center=True)
    add_para(doc, "(Randstad US, LLC Only)", bold=True, center=True)
    add_para(doc, "")
    for text in ORDER_PARAS:
        add_para(doc, text, double=True)
    add_para(doc, "")
    add_para(doc, "IT IS SO ORDERED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, "Dated: ________________")
    add_para(doc, "")
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, "HON. THOMAS WEATHERS", bold=True, right=True)
    add_para(doc, "Judge of the Superior Court", right=True)
    doc.save(str(path))


def main() -> None:
    build_stipulation(OUT_STIP)
    print(f"Wrote {OUT_STIP}")
    build_order(OUT_ORDER)
    print(f"Wrote {OUT_ORDER}")
    build_stip_docx(OUT_STIP_DOCX)
    print(f"Wrote {OUT_STIP_DOCX}")
    build_order_docx(OUT_ORDER_DOCX)
    print(f"Wrote {OUT_ORDER_DOCX}")


if __name__ == "__main__":
    main()
