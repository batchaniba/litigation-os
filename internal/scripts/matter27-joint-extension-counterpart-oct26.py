#!/usr/bin/env python3
"""Matter 27 — Plaintiff counterpart: joint extension to October 26, 2026.

LOCKED stipulation posture: .claude/skills/stipulation-defense/TEMPLATE.md
and SKILL.md. Plaintiff signs his own paper. Single shot. Default reserved.

Supersedes the Sep. 24 Randstad-only / October 14 counterpart
(matter27-joint-extension-counterpart-sep24.py). On September 24, 2026,
Chadwick L. Williams (Kabat Chapman & Ozmer LLP) accepted the settlement
revisions except three: no § 664.6 retention request, payment 14 days after
signing, and his original October 26, 2026 response date for both Randstad
US, LLC and The RK Logistics Group, Inc. Plaintiff agreed to that number, so
the counterpart extends both defendants to October 26 — no later.

Filing is conditioned on Randstad executing the settlement agreement; filing
is Randstad's representation that it has. Neither defendant may take an
automatic extension (§ 430.41(a)(2) / § 435.5(a)(2)). Tod C. Gurney signs
for RK Logistics.

Rendered UNSIGNED unless STIP_SIGNED=1, set only after Plaintiff says it goes.

  python3 internal/scripts/matter27-joint-extension-counterpart-oct26.py
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
TAG = ", Signed" if os.environ.get("STIP_SIGNED") == "1" else ""
OUT_STIP = MATTER27 / (
    "Stipulation to Extend Time for Defendants to Respond "
    f"(Plaintiff Counterpart{TAG}, Oct 26 Joint, Sep 24 2026).pdf"
)
OUT_STIP_DOCX = MATTER27 / (
    "Stipulation to Extend Time for Defendants to Respond "
    f"(Plaintiff Counterpart{TAG}, Oct 26 Joint, Sep 24 2026).docx"
)
OUT_ORDER = MATTER27 / (
    "[Proposed] Order Extending Time for Defendants to Respond "
    f"(Plaintiff Counterpart{TAG}, Oct 26 Joint, Sep 24 2026).pdf"
)
OUT_ORDER_DOCX = MATTER27 / (
    "[Proposed] Order Extending Time for Defendants to Respond "
    f"(Plaintiff Counterpart{TAG}, Oct 26 Joint, Sep 24 2026).docx"
)
OUT_COMBINED = MATTER27 / (
    "Stipulation and Proposed Order Extending Time for Defendants to Respond "
    f"(Plaintiff Counterpart{TAG}, Oct 26 Joint, Sep 24 2026).pdf"
)
OUT_COMBINED_DOCX = MATTER27 / (
    "Stipulation and Proposed Order Extending Time for Defendants to Respond "
    f"(Plaintiff Counterpart{TAG}, Oct 26 Joint, Sep 24 2026).docx"
)

# Unsigned until Plaintiff approves; STIP_SIGNED=1 renders his /s/ copy.
SIGNED = os.environ.get("STIP_SIGNED") == "1"
EXEC_DATE = "September 24, 2026" if SIGNED else "September ___, 2026"
CASE_NO = "26CV199902"
STIP_FOOTER = (
    "JOINT STIPULATION TO EXTEND TIME -- NEWANFORBI v. RANDSTAD US, LLC "
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
    "1. Plaintiff filed the Complaint on July 20, 2026. Default was entered "
    "against Defendant Randstad US, LLC on September 16, 2026. By the "
    "Stipulation and Order to Set Aside and Vacate Entry of Default entered "
    "September 17, 2026, the default was vacated and Randstad was ordered to "
    "file and serve its response to the Complaint on or before September 25, "
    "2026.",
    "2. On September 14, 2026, Defendant The RK Logistics Group, Inc. filed a "
    "declaration under Code of Civil Procedure section 430.41, subdivision "
    "(a)(2) (Judicial Council Form CIV-141). RK Logistics' time to respond is "
    "October 14, 2026. RK Logistics has used the automatic extension that "
    "section allows; any further extension requires a court order.",
    "3. Plaintiff and Randstad have reached a settlement that is being "
    "documented and paid. This stipulation is made only to allow that to "
    "occur. It is not a settlement, a release, or a dismissal, and it does not "
    "alter any term of the settlement.",
    "4. The parties agree to extend the time for Randstad US, LLC and The RK "
    "Logistics Group, Inc. to answer, demur, or otherwise respond to the "
    "Complaint through and including October 26, 2026.",
    "5. This is a single extension. It does not alter any other date set by "
    "Court order, including the January 12, 2027 initial case management "
    "conference. No further extension is implied. Neither Defendant shall file "
    "a declaration under Code of Civil Procedure section 430.41, subdivision "
    "(a)(2), or section 435.5, subdivision (a)(2), to obtain an automatic "
    "extension of the October 26, 2026 date, and neither shall seek any "
    "further extension except by order of the Court. It does not waive any "
    "defense, objection, or right of any party, including Plaintiff's right to "
    "seek default if no timely response is filed. It is not a stay of "
    "discovery.",
    "6. Defendants shall file this stipulation and the proposed order lodged "
    "with it on or before September 25, 2026, and only after Randstad has "
    "executed the parties' written settlement agreement. Defendants' filing of "
    "this stipulation constitutes their representation that Randstad has done "
    "so.",
    "7. This stipulation is made under California Rules of Court, rule "
    "3.110(d), and Code of Civil Procedure sections 430.41, subdivision (a)(2), "
    "and 1054. Because Randstad's current deadline was set by the Court's "
    "September 17, 2026 order and RK Logistics has used its automatic "
    "extension, a proposed order is lodged. The proposed order is no broader "
    "than these terms. This stipulation is not an operative deadline until it "
    "is signed, filed, and the Court enters an order.",
)

ORDER_PARAS = (
    "The Court has considered the Joint Stipulation of Plaintiff Brendan "
    "Ngehsi Newanforbi and Defendants Randstad US, LLC and The RK Logistics "
    "Group, Inc. to extend Defendants' time to respond to the Complaint. IT IS "
    "ORDERED:",
    "1. The time for Defendants Randstad US, LLC and The RK Logistics Group, "
    "Inc. to answer, demur, or otherwise respond to the Complaint is extended "
    "through and including October 26, 2026.",
    "2. This is a single extension. It does not alter any other date set by "
    "Court order, including the January 12, 2027 initial case management "
    "conference. No further extension is implied. Neither Defendant shall "
    "obtain any further extension, including by declaration under Code of "
    "Civil Procedure section 430.41, subdivision (a)(2), or section 435.5, "
    "subdivision (a)(2), except by further order of the Court.",
    "3. Nothing in the stipulation or this Order waives any defense, "
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
    d.write_line("/s/ Brendan Ngehsi Newanforbi" if SIGNED else SIG_LINE, bold=SIGNED)
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
    d.blank_line()
    d.ensure_space(7)
    d.write_line("Dated: ________________")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("TOD C. GURNEY (SBN 199813)", bold=True, right=True, right_margin_offset=20)
    d.write_line("Garcia & Gurney, ALC", right=True, right_margin_offset=20)
    d.write_line("Attorneys for Defendant", right=True, right_margin_offset=20)
    d.write_line("The RK Logistics Group, Inc.", right=True, right_margin_offset=20)


def build_stipulation(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=STIP_FOOTER)
    _header(d)
    _caption(
        d,
        [
            (f"Case No. {CASE_NO}", False, False),
            ("", False, False),
            ("JOINT STIPULATION TO EXTEND", True, False),
            ("TIME FOR DEFENDANTS", True, False),
            ("TO RESPOND TO THE COMPLAINT", True, False),
            ("[Cal. Rules of Court, rule 3.110(d);", True, False),
            ("Code Civ. Proc., § 1054]", True, False),
            ("", False, False),
            ("Judge: Hon. Thomas Weathers", False, False),
            ("Dept. 20", False, False),
            ("[Proposed] Order lodged concurrently", False, False),
        ],
    )
    d.write_line("JOINT STIPULATION TO EXTEND TIME", bold=True, center=True)
    d.write_line("(Randstad US, LLC and The RK Logistics Group, Inc.)", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendants Randstad US, LLC and The RK Logistics Group, Inc., through "
        "their respective counsel of record, stipulate as follows:",
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
            ("TIME FOR DEFENDANTS", True, False),
            ("TO RESPOND TO THE COMPLAINT", True, False),
            ("", False, False),
            ("Judge: Hon. Thomas Weathers", False, False),
            ("Dept. 20", False, False),
            ("Complaint filed: July 20, 2026", False, False),
        ],
    )
    d.write_line("[PROPOSED] ORDER", bold=True, center=True)
    d.write_line("(Randstad US, LLC and The RK Logistics Group, Inc.)", bold=True, center=True)
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
        path, f"Case No. {CASE_NO}  —  JOINT STIPULATION TO EXTEND TIME (Defendants)"
    )
    _docx_caption(
        doc,
        add_para,
        set_run,
        Pt,
        [
            (f"Case No. {CASE_NO}", False),
            ("", False),
            ("JOINT STIPULATION TO EXTEND", True),
            ("TIME FOR DEFENDANTS", True),
            ("TO RESPOND TO THE COMPLAINT", True),
            ("[Cal. Rules of Court, rule 3.110(d);", True),
            ("Code Civ. Proc., § 1054]", True),
            ("", False),
            ("Judge: Hon. Thomas Weathers", False),
            ("Dept. 20", False),
        ],
    )
    add_para(doc, "JOINT STIPULATION TO EXTEND TIME", bold=True, center=True)
    add_para(doc, "(Randstad US, LLC and The RK Logistics Group, Inc.)", bold=True, center=True)
    add_para(doc, "")
    add_para(
        doc,
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, and "
        "Defendants Randstad US, LLC and The RK Logistics Group, Inc., through "
        "their respective counsel of record, stipulate as follows:",
        double=True,
    )
    for text in STIP_PARAS:
        add_para(doc, text, double=True)
    add_para(doc, "")
    add_para(doc, "IT IS SO STIPULATED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, f"Dated: {EXEC_DATE}")
    add_para(doc, "")
    add_para(doc, "/s/ Brendan Ngehsi Newanforbi" if SIGNED else SIG_LINE, bold=SIGNED)
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
    add_para(doc, "")
    add_para(doc, "Dated: ________________")
    add_para(doc, "")
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, "TOD C. GURNEY (SBN 199813)", bold=True, right=True)
    add_para(doc, "Garcia & Gurney, ALC", right=True)
    add_para(doc, "Attorneys for Defendant", right=True)
    add_para(doc, "The RK Logistics Group, Inc.", right=True)
    doc.save(str(path))


def build_order_docx(path: Path) -> None:
    doc, add_para, set_run, _Inches, Pt, _align = _docx_common(
        path, f"Case No. {CASE_NO}  —  [PROPOSED] ORDER EXTENDING TIME (Defendants)"
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
            ("TIME FOR DEFENDANTS", True),
            ("TO RESPOND TO THE COMPLAINT", True),
            ("", False),
            ("Judge: Hon. Thomas Weathers", False),
            ("Dept. 20", False),
            ("Complaint filed: July 20, 2026", False),
        ],
    )
    add_para(doc, "[PROPOSED] ORDER", bold=True, center=True)
    add_para(doc, "(Randstad US, LLC and The RK Logistics Group, Inc.)", bold=True, center=True)
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


def merge_pdfs(out: Path, *inputs: Path) -> None:
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    dst = pymupdf.open()
    for src_path in inputs:
        src = pymupdf.open(src_path)
        dst.insert_pdf(src)
        src.close()
    out.parent.mkdir(parents=True, exist_ok=True)
    dst.save(str(out))
    dst.close()


def merge_docx(out: Path, first: Path, second: Path) -> None:
    from copy import deepcopy

    Document, _align, _spacing, qn, _Inches, _Pt = _docx_helpers()
    doc = Document(str(first))
    doc.add_page_break()
    other = Document(str(second))
    body = doc.element.body
    for child in list(other.element.body):
        if child.tag == qn("w:sectPr"):
            continue
        body.append(deepcopy(child))
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))


def main() -> None:
    build_stipulation(OUT_STIP)
    print(f"Wrote {OUT_STIP}")
    build_order(OUT_ORDER)
    print(f"Wrote {OUT_ORDER}")
    build_stip_docx(OUT_STIP_DOCX)
    print(f"Wrote {OUT_STIP_DOCX}")
    build_order_docx(OUT_ORDER_DOCX)
    print(f"Wrote {OUT_ORDER_DOCX}")
    merge_pdfs(OUT_COMBINED, OUT_STIP, OUT_ORDER)
    print(f"Wrote {OUT_COMBINED}")
    merge_docx(OUT_COMBINED_DOCX, OUT_STIP_DOCX, OUT_ORDER_DOCX)
    print(f"Wrote {OUT_COMBINED_DOCX}")


if __name__ == "__main__":
    main()
