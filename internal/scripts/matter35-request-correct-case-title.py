#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 35 — Request to Correct Case Title (clerical party-order error).

The Verified Complaint and issued SUM-100 name Ross Stores, Inc. first.
One Legal Order #29111713 transmitted the defendants in the wrong order
(Does 2 through 20 first). Odyssey / the public portal therefore short-
title the case "Brendan Ngwa Nforbi vs Does 2 through 20 et al."

Do not amend the complaint. Do not reissue the summons unless the clerk
requires it. Send the One Legal email first; file this request if they
cannot correct Odyssey after acceptance.

  python3 internal/scripts/matter35-request-correct-case-title.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import append_pdf  # noqa: E402
from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
MATTER = ROOT / "internal/public/documents/matter-35"

EXEC_DATE = "September 9, 2026"
CASE_NO = "26CV501995"
CORRECT_TITLE = "Brendan Ngwa Nforbi vs. Ross Stores, Inc., et al."
WRONG_TITLE = "Brendan Ngwa Nforbi vs Does 2 through 20 et al"
FOOTER = (
    "REQUEST TO CORRECT CASE TITLE -- NGWA NFORBI v. ROSS STORES, INC., ET AL."
)

OUT_REQUEST = MATTER / (
    "Request to Correct Case Title - Clerical Party-Order Error (Sep 9 2026).pdf"
)
OUT_ORDER = MATTER / (
    "[Proposed] Order Correcting Case Title - 26CV501995 (Sep 9 2026).pdf"
)
OUT_COVER_A = MATTER / "Exhibit A Cover - Complaint Caption Page (26CV501995).pdf"
OUT_COVER_B = MATTER / "Exhibit B Cover - Public Portal Wrong Title (26CV501995).pdf"
OUT_COVER_C = MATTER / "Exhibit C Cover - One Legal Order 29111713 Title (26CV501995).pdf"
OUT_EX_A = MATTER / "Exhibit A - Complaint Caption Page (26CV501995).pdf"
OUT_PACKET = MATTER / (
    "Request to Correct Case Title Packet (Request, Proposed Order, Exs A-C) "
    "(Sep 9 2026).pdf"
)

COMPLAINT = MATTER / (
    "Verified Complaint (CONFORMED, Filed Aug 26 2026) - 26CV501995.pdf"
)
PORTAL = MATTER / (
    "Santa Clara Public Portal - 26CV501995 Caption Does 2 through 20 "
    "(Sep 8 2026).pdf"
)
ONELEGAL = MATTER / (
    "One Legal Order 29111713 Status - Wrong Case Title Does 2 through 20 "
    "(Sep 8 2026).pdf"
)

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("ROSS STORES, INC., a Delaware", True, False),
    ("corporation; ROSS DRESS FOR LESS,", True, False),
    ("INC., a Virginia corporation;", True, False),
    ("DOE 1; and DOES 2 through 20,", True, False),
    ("inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    (f"Case No. {CASE_NO}", False, False),
    ("", False, False),
    ("REQUEST TO CORRECT CASE", True, False),
    ("TITLE (Clerical Party-Order", True, False),
    ("Error on E-Filing)", True, False),
    ("", False, False),
    ("[No hearing requested]", False, False),
    ("", False, False),
    ("Assigned: Hon. Vince Parrett", False, False),
    ("Dept. 16", False, False),
    ("Action Filed: August 26, 2026", False, False),
    ("CMC: February 11, 2027", False, False),
]

ORDER_RIGHT = [
    (f"Case No. {CASE_NO}", False, False),
    ("", False, False),
    ("[PROPOSED] ORDER", True, False),
    ("CORRECTING CASE TITLE", True, False),
    ("", False, False),
    ("[No hearing requested]", False, False),
    ("", False, False),
    ("Assigned: Hon. Vince Parrett", False, False),
    ("Dept. 16", False, False),
]


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line("COUNTY OF SANTA CLARA", bold=True, center=True)
    d.blank_line()


def _sign(d: PleadingPaper, closer: str) -> None:
    sig_line = "___________________________________"
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}", bold=False)
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    if os.path.isfile(SIGNATURE_PATH):
        d.draw_signature_image(
            SIGNATURE_PATH,
            SIGNATURE_NATIVE_PX[0],
            SIGNATURE_NATIVE_PX[1],
            sig_line,
        )
    d.write_line(sig_line, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGWA NFORBI", right=True, right_margin_offset=20)
    d.write_line(closer, right=True, right_margin_offset=20)


def build_request() -> Path:
    d = PleadingPaper(str(OUT_REQUEST), doc_title_footer=FOOTER)
    _header(d)
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("REQUEST TO CORRECT CASE TITLE", bold=True, center=True)
    d.write_line("(CLERICAL PARTY-ORDER ERROR ON E-FILING)", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "TO THE HONORABLE COURT AND THE CLERK OF THE COURT:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngwa Nforbi, appearing in propria persona, "
        "respectfully requests that the Clerk correct the case title in "
        f"this action to <<b:{CORRECT_TITLE}>> so that it matches the "
        "caption of the Verified Complaint and the issued Summons.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "<<b:1. The complaint and the issued summons are correct.>> The "
        "Verified Complaint filed August 26, 2026, names the defendants in "
        "this order: (1) Ross Stores, Inc., a Delaware corporation; "
        "(2) Ross Dress for Less, Inc., a Virginia corporation; (3) DOE 1; "
        "and (4) DOES 2 through 20, inclusive. The issued SUM-100 (NOTICE "
        "TO DEFENDANT) recites the same order, beginning with Ross Stores, "
        "Inc. Exhibit A is the caption page of the conformed Complaint.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "<<b:2. The register short title is not.>> The Court's public "
        f"portal and One Legal Order #29111713 currently title the case "
        f"<<b:\"{WRONG_TITLE}\">>. The named Ross entities are already on "
        "the party list. The short title picked DOES 2 through 20 as the "
        "lead defendant because the One Legal e-filing party grid was "
        "entered in the wrong order. Exhibits B and C.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "<<b:3. This is a clerical correction, not an amendment.>> "
        "Plaintiff is not adding parties, dropping parties, or changing "
        "any allegation. He does not seek leave to amend. He asks only "
        "that the register, public portal, and One Legal case title be "
        "conformed to the complaint caption, with Ross Stores, Inc. listed "
        "first among the defendants.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "<<b:4. Relief requested.>> Plaintiff respectfully requests that "
        "the Clerk (or the Court, if an order is required) correct the "
        f"case title to <<b:{CORRECT_TITLE}>>; reorder the defendant "
        "entries to match paragraph 1; and leave the issued Summons in "
        "place unless the Clerk determines a reissued summons is necessary "
        "after the title is corrected.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "<<b:5. No hearing; no service yet.>> No defendant has appeared. "
        "No proof of service accompanies this request. Plaintiff will serve "
        "the corporate defendants with the issued Summons after, or if "
        "needed notwithstanding, this correction. The service deadline "
        "under the Civil Lawsuit Notice remains about October 25, 2026.",
        first_indent=36,
    )
    d.blank_line()
    _sign(d, "Plaintiff, In Propria Persona")

    d.start_new_page()
    d.write_line("DECLARATION OF BRENDAN NGWA NFORBI", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, Brendan Ngwa Nforbi, declare:", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "1. I am the Plaintiff in this action. I have personal knowledge "
        "of the facts below and could testify to them if called.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "2. On August 26, 2026, I e-filed the Verified Complaint through "
        "One Legal (Order #29111713; Confirmation #35442871). When I "
        "entered the defendants into One Legal's party list, I entered "
        "them in the wrong order, with DOES 2 through 20 first. The "
        "complaint PDF and the SUM-100 I submitted named Ross Stores, "
        "Inc. first.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        f"3. On September 8, 2026, I printed the public portal for Case "
        f"No. {CASE_NO}. The case title reads \"{WRONG_TITLE}.\" The party "
        "list still includes Ross Stores, Inc. and Ross Dress for Less, "
        "Inc. One Legal's order-status page shows the same wrong title.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "4. I am not asking to amend the complaint or to add or drop any "
        "party. I want the Court's case title to match the complaint.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        f"I declare under penalty of perjury under the laws of the State "
        f"of California that the foregoing is true and correct. Executed "
        f"on {EXEC_DATE}, at Stockton, California.",
        first_indent=36,
    )
    d.blank_line()
    _sign(d, "Declarant")
    d.save()
    print(f"Wrote {OUT_REQUEST}")
    return OUT_REQUEST


def build_proposed_order() -> Path:
    d = PleadingPaper(str(OUT_ORDER), doc_title_footer=FOOTER)
    _header(d)
    d.draw_caption_block(CAPTION_LEFT, ORDER_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("[PROPOSED] ORDER CORRECTING CASE TITLE", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "The Court having considered Plaintiff's Request to Correct Case "
        "Title, and good cause appearing,",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped("IT IS ORDERED that:", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        f"1. The Clerk shall correct the case title in this action to "
        f"<<b:{CORRECT_TITLE}>>.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "2. The Clerk shall list the defendants in the register in the "
        "order named in the Verified Complaint: Ross Stores, Inc.; Ross "
        "Dress for Less, Inc.; DOE 1; and DOES 2 through 20, inclusive.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "3. This order does not amend the Verified Complaint, add or drop "
        "any party, or vacate the issued Summons.",
        first_indent=36,
    )
    d.blank_line()
    d.blank_line()
    d.write_line("IT IS SO ORDERED.", bold=False)
    d.blank_line()
    d.blank_line()
    d.write_line(f"Dated: _______________     ________________________________")
    d.write_line("                            Hon. Vince Parrett")
    d.write_line("                            Judge of the Superior Court")
    d.save()
    print(f"Wrote {OUT_ORDER}")
    return OUT_ORDER


def build_exhibits() -> None:
    writer = PdfWriter()
    writer.add_page(PdfReader(str(COMPLAINT)).pages[0])
    with OUT_EX_A.open("wb") as fh:
        writer.write(fh)

    write_exhibit_cover(
        OUT_COVER_A,
        court="SUPERIOR COURT OF CALIFORNIA",
        court_line2="COUNTY OF SANTA CLARA",
        caption="NGWA NFORBI v. ROSS STORES, INC., et al.",
        case_no=f"Case No. {CASE_NO}",
        exhibit="A",
        title="Verified Complaint \u2014 caption page",
        details=[
            "Conformed filed August 26, 2026",
            "Ross Stores, Inc. named first",
        ],
        footer=FOOTER,
    )
    write_exhibit_cover(
        OUT_COVER_B,
        court="SUPERIOR COURT OF CALIFORNIA",
        court_line2="COUNTY OF SANTA CLARA",
        caption="NGWA NFORBI v. ROSS STORES, INC., et al.",
        case_no=f"Case No. {CASE_NO}",
        exhibit="B",
        title="Public portal print \u2014 wrong short title",
        details=[
            "Printed September 8, 2026, 10:28 p.m.",
            f'Title: "{WRONG_TITLE}"',
        ],
        footer=FOOTER,
    )
    write_exhibit_cover(
        OUT_COVER_C,
        court="SUPERIOR COURT OF CALIFORNIA",
        court_line2="COUNTY OF SANTA CLARA",
        caption="NGWA NFORBI v. ROSS STORES, INC., et al.",
        case_no=f"Case No. {CASE_NO}",
        exhibit="C",
        title="One Legal Order #29111713 status",
        details=[
            "Printed September 8, 2026, 10:29 p.m.",
            "Same wrong title on the completed e-filing order",
        ],
        footer=FOOTER,
    )


def assemble_packet() -> Path:
    writer = PdfWriter()
    append_pdf(writer, OUT_REQUEST)
    append_pdf(writer, OUT_ORDER)
    append_pdf(writer, OUT_COVER_A)
    append_pdf(writer, OUT_EX_A)
    append_pdf(writer, OUT_COVER_B)
    append_pdf(writer, PORTAL)
    append_pdf(writer, OUT_COVER_C)
    append_pdf(writer, ONELEGAL)
    with OUT_PACKET.open("wb") as fh:
        writer.write(fh)
    print(f"Wrote {OUT_PACKET}")
    return OUT_PACKET


def main() -> None:
    for path in (COMPLAINT, PORTAL, ONELEGAL):
        if not path.is_file():
            raise SystemExit(f"Missing {path}")
    build_request()
    build_proposed_order()
    build_exhibits()
    assemble_packet()
    print("Do not file until One Legal says they cannot correct Odyssey.")
    print("Do not amend the complaint. Do not reissue the summons unless asked.")


if __name__ == "__main__":
    main()
