#!/usr/bin/env python3
"""N.D. Cal. name-correction stipulations — Serrato and Meza only.

DAG Haiyang A. Li wrote September 10, 2026, 8:55 a.m., asking for a draft
after Plaintiff's Civil L.R. 7-11(a) email. Plaintiff drafts. One paper
per action. Name correction only. No deadline moves.

Plaintiff's /s/ is applied because he directed that exact form on this
draft. Li's block is left blank.

  python3 internal/scripts/ndcal-name-correction-stipulations.py
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent

EXEC_DATE = "September 10, 2026"
TARGET_NAME = "BRENDAN NGWA NFORBI"
TARGET_NAME_TC = "Brendan Ngwa Nforbi"
PACER_LOGIN = "bngwanforbi"
HELPDESK_DATE = "September 1, 2026"
LI_SBN = "288063"

ADDRESS = [
    "1455 Cat Tail Drive",
    "Stockton, CA 95204",
    "Telephone: (209) 801-4442",
    "E-mail: bnn.cdl@gmail.com",
]


@dataclass(frozen=True)
class StipCase:
    matter: int
    outdir: Path
    case_no: str
    short: str
    docket_name: str
    left_caption: list[tuple[str, bool]]
    defendant_intro: str
    preserve_clauses: list[str]
    order_preserve: str
    li_for: list[str]
    footer: str
    filename: str


SERRATO = StipCase(
    matter=24,
    outdir=ROOT / "public/documents/matter-24",
    case_no="4:26-cv-05953-ASK",
    short="NFORBI v. SERRATO",
    docket_name="Brendan Ngehsi Newanforbi",
    left_caption=[
        ("BRENDAN NGWA NFORBI,", True),
        ("          Plaintiff,", False),
        ("", False),
        ("     v.", False),
        ("", False),
        ("CAPTAIN G. SERRATO, in his", True),
        ("individual and official capacities", True),
        ("as Commander, Dublin Area,", True),
        ("California Highway Patrol,", True),
        ("          Defendant.", False),
    ],
    defendant_intro=(
        "Defendant Captain G. Serrato, in his individual and official "
        "capacities, by and through his counsel of record Haiyang A. Li, "
        "Deputy Attorney General,"
    ),
    preserve_clauses=[
        "the initial Case Management Conference set for September 15, 2026, "
        "at 1:30 p.m., via Zoom",
        "the hearing on Defendant's Motion to Dismiss (Dkt. 18) set for "
        "September 30, 2026, at 1:30 p.m.",
        "the briefing already filed on that motion",
        "all disclosure and discovery obligations, including those already "
        "performed",
    ],
    order_preserve=(
        "including the September 15, 2026 initial Case Management Conference "
        "and the September 30, 2026 hearing on Defendant's Motion to Dismiss "
        "(Dkt. 18)"
    ),
    li_for=[
        "Attorneys for Defendant",
        "Captain G. Serrato",
    ],
    footer="STIPULATION TO CORRECT DOCKET NAME -- NFORBI v. SERRATO",
    filename=(
        "Stipulation and Proposed Order to Correct Plaintiff's Name "
        "on the Docket (4-26-cv-05953-ASK) (Sep 10 2026).docx"
    ),
)

MEZA = StipCase(
    matter=32,
    outdir=ROOT / "public/documents/matter-32/ndcal",
    case_no="4:26-cv-08271-ASK",
    short="NFORBI v. MEZA-GONZALEZ",
    docket_name="Nforbi",
    left_caption=[
        ("BRENDAN NGWA NFORBI,", True),
        ("          Plaintiff,", False),
        ("", False),
        ("     v.", False),
        ("", False),
        ("SANTIAGO MEZA-GONZALEZ,", True),
        ("individually; JOSE MELANO,", True),
        ("individually; and DOES 1–10,", True),
        ("          Defendants.", False),
    ],
    defendant_intro=(
        "Defendants Santiago Meza-Gonzalez and Jose Melano, by and through "
        "Haiyang A. Li, Deputy Attorney General,"
    ),
    preserve_clauses=[
        "the service, Rule 4, and Rule 12 posture of every defendant, "
        "including any pending request that Mr. Li accept service (Dkt. 13)",
        "any Case Management Conference, ADR, or disclosure date the Court "
        "has set or will set",
        "all disclosure and discovery obligations",
    ],
    order_preserve=(
        "including the service, Rule 4, and Rule 12 posture of every "
        "defendant and the pending administrative motion at Dkt. 13"
    ),
    li_for=[
        "Attorneys for Defendants",
        "Santiago Meza-Gonzalez and Jose Melano",
    ],
    footer="STIPULATION TO CORRECT DOCKET NAME -- NFORBI v. MEZA-GONZALEZ",
    filename=(
        "Stipulation and Proposed Order to Correct Plaintiff's Name "
        "on the Docket (4-26-cv-08271-ASK) (Sep 10 2026).docx"
    ),
)


def _docx_helpers():
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt, Twips
    except ImportError:
        os.system(f"{sys.executable} -m pip install -q python-docx")
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt, Twips
    return Document, WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, qn, Inches, Pt, Twips


def _set_run(run, qn, *, bold=False, italic=False, size, font_name="Times New Roman"):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    run.font.size = size
    run.bold = bold
    run.italic = italic


def build_docx(case: StipCase) -> Path:
    Document, WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, qn, Inches, Pt, _Twips = (
        _docx_helpers()
    )
    font_name = "Times New Roman"
    size = Pt(12)

    def add_para(
        document,
        text="",
        *,
        bold=False,
        italic=False,
        center=False,
        right=False,
        double=False,
        first_line=None,
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
        if first_line is not None:
            pf.first_line_indent = Inches(first_line)
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif right:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if text:
            run = p.add_run(text)
            _set_run(run, qn, bold=bold, italic=italic, size=run_size)
        return p

    path = case.outdir / case.filename
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
    run = fp.add_run(f"Case No. {case.case_no}  —  {case.footer}")
    _set_run(run, qn, size=Pt(9))

    add_para(doc, TARGET_NAME, bold=True)
    add_para(doc, f"(docketed as {case.docket_name})", italic=True, run_size=Pt(11))
    add_para(doc, "Plaintiff, In Pro Per")
    for line in ADDRESS:
        add_para(doc, line)
    add_para(doc, "")
    add_para(doc, "UNITED STATES DISTRICT COURT", bold=True, center=True)
    add_para(doc, "NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    add_para(doc, "OAKLAND DIVISION", bold=True, center=True)
    add_para(doc, "")

    table = doc.add_table(rows=1, cols=2)
    left, right = table.rows[0].cells
    right_lines = [
        (f"Case No. {case.case_no}", False),
        ("", False),
        ("STIPULATION AND [PROPOSED] ORDER", True),
        ("TO CORRECT PLAINTIFF'S NAME", True),
        ("ON THE DOCKET", True),
        ("[Civil L.R. 7-11, 7-12]", True),
        ("", False),
        ("Judge: Hon. Ajay S. Krishnan", False),
    ]
    for cell, lines in ((left, case.left_caption), (right, right_lines)):
        cell.text = ""
        for i, (text, bold) in enumerate(lines):
            p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(text)
            _set_run(run, qn, bold=bold, size=Pt(11))

    add_para(doc, "")
    add_para(doc, "STIPULATION TO CORRECT PLAINTIFF'S", bold=True, center=True)
    add_para(doc, "NAME ON THE DOCKET", bold=True, center=True)
    add_para(doc, "")

    add_para(
        doc,
        f"Plaintiff {TARGET_NAME_TC}, who appears on this docket as "
        f"\"{case.docket_name},\" appearing in propria persona, and "
        f"{case.defendant_intro} stipulate as follows:",
        double=True,
    )
    add_para(doc, "")

    numbered = [
        (
            f"Plaintiff is one natural person. He maintains a single PACER "
            f"account under the login {PACER_LOGIN}, in which his first name "
            f"is recorded as \"Brendan\" and his last name as \"Ngwa Nforbi.\""
        ),
        (
            f"This docket currently identifies Plaintiff as "
            f"\"{case.docket_name}.\" That identification and "
            f"\"{TARGET_NAME_TC}\" refer to the same person."
        ),
        (
            f"On {HELPDESK_DATE}, the Court's ECF Help Desk advised Plaintiff "
            f"that it cannot link this action to that PACER account until the "
            f"docket reflects the name recorded on the account, and that "
            f"Plaintiff may request that the Court correct the name on the "
            f"docket first. Because of the mismatch, Plaintiff cannot "
            f"electronically file in this action."
        ),
        (
            f"The parties stipulate, and respectfully request that the Court "
            f"order, that the Clerk correct the docket and the CM/ECF party "
            f"record in this action to identify Plaintiff as "
            f"\"{TARGET_NAME}.\""
        ),
        (
            "This stipulation corrects the form of Plaintiff's name only. It "
            "does not add, drop, or substitute any party. Federal Rule of "
            "Civil Procedure 25 is not implicated. It does not amend any "
            "claim, allegation, or operative pleading. It does not authorize "
            "any additional relief."
        ),
        (
            "Except for the name correction stated in paragraph 4, no "
            "deadline, hearing, conference, briefing schedule, discovery "
            "obligation, or trial date is modified. Without limitation, the "
            "following remain as previously set: "
            + "; ".join(case.preserve_clauses)
            + "."
        ),
        (
            "Nothing in this stipulation is a waiver of any claim, defense, "
            "objection, or right. No party concedes any disputed issue of "
            "fact or law by entering into it. This stipulation is not a stay "
            "of discovery and does not affect any pending motion except as "
            "to the form of Plaintiff's name on the docket."
        ),
        (
            "The parties request that the Court enter the [Proposed] Order "
            "below pursuant to Civil Local Rules 7-11 and 7-12."
        ),
    ]
    if case.matter == 32:
        numbered.insert(
            6,
            "This stipulation does not accept service on any defendant, "
            "does not waive any defect or completeness of service, and does "
            "not start, stop, or extend any time to answer or otherwise "
            "respond.",
        )
        # Renumber is implicit — we print by enumerate after the insert.
    for i, text in enumerate(numbered, 1):
        add_para(doc, f"{i}.  {text}", double=True)
        add_para(doc, "")

    add_para(doc, "IT IS SO STIPULATED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, f"Dated: {EXEC_DATE}")
    add_para(doc, "")
    add_para(doc, f"/s/ {TARGET_NAME_TC}")
    add_para(doc, TARGET_NAME, bold=True)
    add_para(doc, f"(docketed as {case.docket_name})", italic=True, run_size=Pt(11))
    add_para(doc, "Plaintiff, In Pro Per")
    add_para(doc, "")
    add_para(doc, "Dated: ________________")
    add_para(doc, "")
    add_para(doc, "___________________________________")
    add_para(doc, f"HAIYANG A. LI (SBN {LI_SBN})", bold=True)
    add_para(doc, "Deputy Attorney General")
    for line in case.li_for:
        add_para(doc, line)
    add_para(doc, "")
    add_para(doc, "FILER'S ATTESTATION", bold=True, center=True)
    add_para(doc, "")
    add_para(
        doc,
        "Pursuant to Civil L.R. 5-1(i)(3), I attest that concurrence in the "
        "filing of this document has been obtained from each of the other "
        "signatories. This attestation applies only to this document as "
        "signed and does not authorize any revised version.",
        double=True,
    )
    add_para(doc, "")
    add_para(doc, "Dated: ________________")
    add_para(doc, "")
    add_para(doc, "___________________________________")
    add_para(doc, f"HAIYANG A. LI (SBN {LI_SBN})", bold=True)
    add_para(doc, "Deputy Attorney General")
    doc.add_page_break()
    add_para(doc, "UNITED STATES DISTRICT COURT", bold=True, center=True)
    add_para(doc, "NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    add_para(doc, "OAKLAND DIVISION", bold=True, center=True)
    add_para(doc, "")
    order_table = doc.add_table(rows=1, cols=2)
    order_left, order_right = order_table.rows[0].cells
    order_right_lines = [
        (f"Case No. {case.case_no}", False),
        ("", False),
        ("[PROPOSED] ORDER CORRECTING", True),
        ("PLAINTIFF'S NAME ON THE", True),
        ("DOCKET", True),
        ("[Civil L.R. 7-11, 7-12]", True),
        ("", False),
        ("Judge: Hon. Ajay S. Krishnan", False),
    ]
    for cell, lines in ((order_left, case.left_caption), (order_right, order_right_lines)):
        cell.text = ""
        for i, (text, bold) in enumerate(lines):
            p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(text)
            _set_run(run, qn, bold=bold, size=Pt(11))
    add_para(doc, "")
    add_para(doc, "[PROPOSED] ORDER", bold=True, center=True)
    add_para(doc, "")
    add_para(
        doc,
        "The parties having stipulated under Civil Local Rules 7-11 and 7-12, "
        "the Court ORDERS:",
        double=True,
    )
    add_para(doc, "")
    order_paras = [
        f"1.  The Clerk shall correct the docket and the CM/ECF party record "
        f"in this action to identify Plaintiff as \"{TARGET_NAME}.\"",
        "2.  This Order corrects the form of Plaintiff's name only. It "
        "effects no substitution of parties, no amendment of any claim or "
        "allegation, and no change to any deadline, hearing, conference, "
        f"briefing schedule, discovery obligation, or trial date previously "
        f"set in this action, {case.order_preserve}.",
        "3.  No other relief is granted.",
    ]
    for text in order_paras:
        add_para(doc, text, double=True)
        add_para(doc, "")
    add_para(doc, "PURSUANT TO STIPULATION, IT IS SO ORDERED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, "Dated: ______________________")
    add_para(doc, "")
    add_para(doc, "___________________________________")
    add_para(doc, "HON. AJAY S. KRISHNAN")
    add_para(doc, "United States Magistrate Judge")

    doc.save(str(path))
    return path


def main() -> None:
    for case in (SERRATO, MEZA):
        path = build_docx(case)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
