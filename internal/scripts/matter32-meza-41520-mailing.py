#!/usr/bin/env python3
"""Matter 32 — CCP § 415.20(b) mailing follow-up for Santiago Meza-Gonzalez.

Dkt. 16 / 16-1 (filed Sep. 14, 2026) is Fischer's substitute-service return:
leave with Kim S. - H.R. at CHP Modesto Area on Aug. 27 after two attempts.
Diligence only. No mail date. Workplace substitute service under
Fed. R. Civ. P. 4(e)(1) / Cal. Code Civ. Proc. § 415.20(b) is leave-plus-mail.
This packet is the missing mailing.

  python3 internal/scripts/matter32-meza-41520-mailing.py
  python3 internal/scripts/matter32-meza-41520-mailing.py \\
      --date "September 16, 2026" --mailed-from "San Jose, California"
      --declaration-only

Date the papers the day the envelope actually goes in the mail. POS is
valid only if mailed that day from the stated city. Do not treat
September 16 as a default date against Meza or Li.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pypdf import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import append_page, assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
OUT_DIR = ROOT / "public/documents/matter-32/ndcal"

DEFAULT_DATE = "September 16, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
SHORT_MAIL = "meza-41520-mail"
SHORT_FILING = "meza-41520-filing"

CASE_NO = "4:26-cv-08271-ASK"
JUDGE = "Hon. Ajay S. Krishnan"
RELATED = "4:26-cv-05953-ASK"

SUMMONS = OUT_DIR / "Dkt 03 - Summons Issued - Meza-Gonzalez and Melano (Aug 10 2026).pdf"
MEZA_SUMMONS_PAGE = 1  # Dkt. 3 p.2 — Meza @ 4030 Kiernan; p.1 is Melano
FAC = OUT_DIR / "Dkt 05 - First Amended Complaint (CONFORMED, Filed Aug 17 2026).pdf"
NOTICE = OUT_DIR / "Notice Identifying Operative First Amended Complaint (Meza) (Aug 24 2026).pdf"
CMC = OUT_DIR / (
    "Dkt 04 - Order Setting Initial Case Management Conference and ADR Deadlines "
    "(Aug 10 2026).pdf"
)

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("SANTIAGO MEZA-GONZALEZ", True, False),
    ("(CHP #023295); JOSE MELANO", True, False),
    ("(CHP #023054); and DOES 1-10,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

DECL_FOOTER = (
    "DECLARATION OF MAILING — CCP § 415.20(b) -- "
    "NFORBI v. MEZA-GONZALEZ ET AL."
)
NONPARTY_FOOTER = (
    "NON-PARTY DECLARATION OF MAILING — CCP § 415.20(b) -- "
    "NFORBI v. MEZA-GONZALEZ ET AL."
)

LI_BLOCK = [
    "Haiyang A. Li, Deputy Attorney General",
    "Office of the Attorney General",
    "300 South Spring Street, Suite 1702",
    "Los Angeles, CA 90013-1230",
    "Haiyang.Li@doj.ca.gov",
    "Counsel for Captain G. Serrato in the related action;",
    "prior counsel for Meza-Gonzalez and Melano on this incident",
]

MELANO_BLOCK = [
    "Jose Melano, CHP #023054",
    "California Highway Patrol, South Sacramento Area",
    "6 Massie Court",
    "Sacramento, CA 95823",
    "Defendant (summons served August 14, 2026)",
]

MEZA_BLOCK = [
    "Santiago Meza-Gonzalez, CHP #023295",
    "California Highway Patrol, Modesto Area",
    "4030 Kiernan Avenue",
    "Modesto, CA 95356",
    "Defendant (individual capacity; § 415.20(b) mailing)",
]

ENVELOPE_LINES = [
    "Santiago Meza-Gonzalez",
    "California Highway Patrol, Modesto Area",
    "4030 Kiernan Avenue",
    "Modesto, CA 95356",
]

PAPERS_LEFT = (
    "the issued summons as to Santiago Meza-Gonzalez individually (Dkt. 3), "
    "the operative First Amended Complaint (Dkt. 5), the Notice Identifying "
    "the Operative First Amended Complaint, and the Order Setting Initial "
    "Case Management Conference and ADR Deadlines (Dkt. 4)"
)


def _caption_right(title_lines: list[str]) -> list[tuple[str, bool, bool]]:
    rows: list[tuple[str, bool, bool]] = [
        (f"Case No. {CASE_NO}", True, False),
        ("", False, False),
    ]
    for line in title_lines:
        rows.append((line, True, False))
    rows.extend(
        [
            ("", False, False),
            ("Fed. R. Civ. P. 4(e)(1), 4(l);", False, False),
            ("Cal. Code Civ. Proc.", False, False),
            ("§ 415.20(b)", False, False),
            ("", False, False),
            (f"Judge: {JUDGE}", False, False),
            (f"Related: {RELATED}", False, False),
        ]
    )
    return rows


PLAINTIFF_CAPTION_RIGHT = _caption_right(
    [
        "DECLARATION OF MAILING",
        "(Cal. Code Civ. Proc.",
        "§ 415.20(b) Follow-Up",
        "to Documents 16 / 16-1)",
    ]
)

NONPARTY_CAPTION_RIGHT = _caption_right(
    [
        "DECLARATION OF MAILING",
        "(Non-Party Mailer —",
        "Cal. Code Civ. Proc.",
        "§ 415.20(b) Follow-Up",
        "to Documents 16 / 16-1)",
    ]
)


def _header_block(d: PleadingPaper, right_caption: list) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, right_caption, caption_size=9,
                         tight_lh=12, boxed=True)
    d.blank_line()


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=18, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")


def _plaintiff_decl_content(exec_date: str, mailed_from: str) -> list[tuple[str, str]]:
    city = mailed_from.removesuffix(", California").removesuffix(", CA")
    return [
        ("PARA", "I, BRENDAN NGWA NFORBI, declare as follows:"),
        (
            "LIST_ITEM",
            "1.  I am the Plaintiff in this action. I am over eighteen years of "
            "age. I make this declaration from my personal knowledge.",
        ),
        (
            "LIST_ITEM",
            "2.  On August 27, 2026, at 1:30 p.m., Daniel Fischer of Run With "
            "It, order 15645547, left copies of "
            + PAPERS_LEFT
            + " with Kim S. - H.R., a person apparently in charge at Defendant "
            "Santiago Meza-Gonzalez's usual place of business, California "
            "Highway Patrol, Modesto Area, 4030 Kiernan Avenue, Modesto, "
            "California 95356. Fischer had attempted personal delivery at that "
            "address on August 25, 2026, at 4:00 p.m., and on August 26, 2026, "
            "at 10:15 a.m. He signed a Declaration of Service and a Declaration "
            "of Reasonable Diligence on September 3, 2026. I filed those "
            "declarations on September 14, 2026, as Documents 16 and 16-1.",
        ),
        (
            "LIST_ITEM",
            "3.  Documents 16 and 16-1 recite the two attempts and the August 27 "
            "leaving. They do not recite a first-class mailing to "
            "Meza-Gonzalez at 4030 Kiernan Avenue. They do not recite postage "
            "or an envelope. The service form states that a declaration of "
            "diligence and/or mailing is attached if applicable. What I filed "
            "is diligence only.",
        ),
        (
            "LIST_ITEM",
            f"4.  On {exec_date}, I placed a true copy of the same papers listed "
            "in paragraph 2 in a sealed envelope addressed to:",
        ),
        (
            "LIST_ITEM",
            "     Santiago Meza-Gonzalez",
        ),
        (
            "LIST_ITEM",
            "     California Highway Patrol, Modesto Area",
        ),
        (
            "LIST_ITEM",
            "     4030 Kiernan Avenue",
        ),
        (
            "LIST_ITEM",
            "     Modesto, CA 95356",
        ),
        (
            "LIST_ITEM",
            f"5.  I mailed that envelope by first-class United States Mail, "
            f"postage prepaid, by depositing it in the United States Mail at "
            f"{city}, California. This is the mailing required by section "
            "415.20(b) to the person to be served at the place where the copies "
            "were left. Service in this manner is deemed complete on the tenth "
            "day after the mailing. Fed. R. Civ. P. 4(e)(1).",
        ),
        (
            "LIST_ITEM",
            "6.  The action is against Meza-Gonzalez in his individual capacity. "
            "The envelope did not include a copy of Document 16 itself and did "
            "not include a cover letter.",
        ),
        (
            "LIST_ITEM",
            "7.  A copy of the United States Postal Service receipt for this "
            "mailing is attached as Exhibit A, or will be attached when received.",
        ),
        (
            "PARA",
            "I declare under penalty of perjury under the laws of the United "
            "States of America that the foregoing is true and correct.",
        ),
    ]


def _nonparty_decl_content(exec_date: str, mailed_from: str) -> list[tuple[str, str]]:
    city = mailed_from.removesuffix(", California").removesuffix(", CA")
    return [
        ("PARA", "I, ______________________________________, declare as follows:"),
        (
            "LIST_ITEM",
            "1.  I am over eighteen years of age. I am not a party to this "
            "action. My address is "
            "______________________________________________________________.",
        ),
        (
            "LIST_ITEM",
            "2.  I have read, or have been shown, Documents 16 and 16-1 in "
            "this action. Those papers are the September 3, 2026 Declaration "
            "of Service and Declaration of Reasonable Diligence of Daniel "
            "Fischer, Run With It order 15645547, filed September 14, 2026. "
            "They recite that on August 27, 2026, at 1:30 p.m., Fischer left "
            + PAPERS_LEFT
            + " with Kim S. - H.R. at California Highway Patrol, Modesto Area, "
            "4030 Kiernan Avenue, Modesto, California 95356, after attempts "
            "at that address on August 25, 2026, at 4:00 p.m., and August 26, "
            "2026, at 10:15 a.m.",
        ),
        (
            "LIST_ITEM",
            "3.  Documents 16 and 16-1 do not recite a first-class mailing to "
            "Meza-Gonzalez at that address.",
        ),
        (
            "LIST_ITEM",
            f"4.  On {exec_date}, I placed a true copy of the same papers listed "
            "in paragraph 2 in a sealed envelope addressed to Santiago "
            "Meza-Gonzalez, California Highway Patrol, Modesto Area, 4030 "
            "Kiernan Avenue, Modesto, CA 95356. The envelope did not include "
            "a cover letter.",
        ),
        (
            "LIST_ITEM",
            f"5.  I mailed that envelope by first-class United States Mail, "
            f"postage prepaid, by depositing it in the United States Mail at "
            f"{city}, California. This is the mailing required by section "
            "415.20(b) to the person to be served at the place where the copies "
            "were left.",
        ),
        (
            "LIST_ITEM",
            "6.  A copy of the United States Postal Service receipt for this "
            "mailing is attached as Exhibit A, or will be attached when received.",
        ),
        (
            "PARA",
            "I declare under penalty of perjury under the laws of the United "
            "States of America that the foregoing is true and correct.",
        ),
    ]


def _plaintiff_signature(d: PleadingPaper, exec_date: str, place: str) -> None:
    d.ensure_space(10)
    d.write_line(f"Executed on {exec_date}, at {place}.")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
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
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _nonparty_signature(d: PleadingPaper, exec_date: str, place: str) -> None:
    d.ensure_space(8)
    d.write_line(f"Executed on {exec_date}, at {place}.")
    d.blank_line()
    d.write_line("________________________________________")
    d.write_line("Signature of person who mailed the envelope")
    d.write_line("Printed name: ____________________________")


def paths_for(exec_date: str) -> dict[str, Path]:
    tag = exec_date
    return {
        "cover_letter": OUT_DIR / (
            f"Cover Letter - CCP 415.20(b) Mailing to Meza-Gonzalez "
            f"(N.D. Cal. 4-26-cv-08271-ASK) ({tag}).pdf"
        ),
        "meza_summons": OUT_DIR / (
            f"Summons Issued - Santiago Meza-Gonzalez only "
            f"(N.D. Cal. Dkt. 3) (Aug 10 2026).pdf"
        ),
        "plaintiff_decl": OUT_DIR / (
            f"Declaration of Mailing - CCP 415.20(b) Follow-Up to Dkt 16 - "
            f"Meza-Gonzalez (N.D. Cal. 4-26-cv-08271-ASK) ({tag}).pdf"
        ),
        "nonparty_decl": OUT_DIR / (
            f"Declaration of Mailing - Non-Party - CCP 415.20(b) Follow-Up to "
            f"Dkt 16 - Meza-Gonzalez (N.D. Cal. 4-26-cv-08271-ASK) ({tag}).pdf"
        ),
        "exhibit_cover": OUT_DIR / (
            f"Exhibit A Cover - USPS Receipt - CCP 415.20(b) Mailing "
            f"Meza-Gonzalez ({tag}).pdf"
        ),
        "pos": OUT_DIR / (
            f"Proof of Service - Declaration of Mailing CCP 415.20(b) - "
            f"Meza-Gonzalez (N.D. Cal. 4-26-cv-08271-ASK) ({tag}).pdf"
        ),
        "instructions": OUT_DIR / (
            f"PLAINTIFF COPY - CCP 415.20(b) Mailing Instructions - "
            f"Meza-Gonzalez ({tag}).pdf"
        ),
        "label": OUT_DIR / (
            f"Envelope Address - Meza-Gonzalez 4030 Kiernan Ave ({tag}).pdf"
        ),
        "mail_bundle": OUT_DIR / (
            f"CCP 415.20(b) Mailing Bundle - Meza-Gonzalez "
            f"(N.D. Cal. 4-26-cv-08271-ASK) ({tag}).pdf"
        ),
        "filing_packet": OUT_DIR / (
            f"CCP 415.20(b) Mailing Filing Packet - Meza-Gonzalez "
            f"(N.D. Cal. 4-26-cv-08271-ASK) ({tag}).pdf"
        ),
        "email": OUT_DIR / "EMAIL_DRAFT_Li_CCP_41520_Mailing_Meza.txt",
        "how_to": OUT_DIR / "CCP_41520_MAILING_INSTRUCTIONS_Meza.txt",
    }


def write_cover_letter(path: Path, exec_date: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    y = h - 72

    def line(text: str, *, size: float = 11, bold: bool = False, dy: float = 14) -> None:
        nonlocal y
        c.setFont("Times-Bold" if bold else "Times-Roman", size)
        c.drawString(72, y, text)
        y -= dy

    def wrapped(text: str, *, size: float = 11, first_indent: float = 18) -> None:
        nonlocal y
        c.setFont("Times-Roman", size)
        words = text.split()
        x0 = 72
        max_w = w - 144
        current = ""
        indent = first_indent
        for word in words:
            trial = f"{current} {word}".strip()
            if c.stringWidth(trial, "Times-Roman", size) <= max_w - indent:
                current = trial
            else:
                c.drawString(x0 + indent, y, current)
                y -= 15
                current = word
                indent = 0
        if current:
            c.drawString(x0 + indent, y, current)
            y -= 15

    line("BRENDAN NGWA NFORBI", bold=True, size=12)
    line("Plaintiff, In Propria Persona")
    line("1455 Cat Tail Drive")
    line("Stockton, CA 95204")
    y -= 10
    line(exec_date)
    y -= 10
    for row in ENVELOPE_LINES:
        line(row)
    y -= 10
    line("Re:  Nforbi v. Meza-Gonzalez et al., No. 4:26-cv-08271-ASK", bold=True)
    line("     United States District Court, Northern District of California")
    line("     Follow-up copies — Cal. Code Civ. Proc. § 415.20(b)")
    y -= 8
    line("Officer Meza-Gonzalez:")
    y -= 6
    wrapped(
        "On August 27, 2026, at 1:30 p.m., process server Daniel Fischer left "
        "copies of the enclosed papers with Kim S., H.R., a person apparently "
        "in charge at your usual place of business, 4030 Kiernan Avenue, "
        "Modesto, California. Those papers are enclosed again:"
    )
    y -= 6
    line("     1.  Issued summons as to you individually (Dkt. 3);")
    line("     2.  First Amended Complaint (Dkt. 5);")
    line("     3.  Notice Identifying the Operative First Amended Complaint; and")
    line("     4.  Order Setting Initial Case Management Conference and")
    line("         ADR Deadlines (Dkt. 4).")
    y -= 6
    wrapped(
        "I am mailing these copies to you at that same address, by first-class "
        "mail, postage prepaid, as required by California Code of Civil "
        "Procedure section 415.20(b). This action is against you in your "
        "individual capacity."
    )
    y -= 16
    line("Very truly yours,")
    y -= 28
    try:
        sig_w = 180.0
        sig_h = sig_w * (SIGNATURE_NATIVE_PX[1] / SIGNATURE_NATIVE_PX[0]) * 1.15
        c.drawImage(
            SIGNATURE_PATH,
            72,
            y,
            width=sig_w,
            height=sig_h,
            mask="auto",
            preserveAspectRatio=False,
        )
        y -= 8
    except Exception as exc:  # noqa: BLE001
        print(f"warning: cover-letter signature: {exc}", file=sys.stderr)
    y -= 18
    line("Brendan Ngwa Nforbi", bold=True)
    line("Plaintiff, In Propria Persona")
    c.save()
    return path


def write_envelope_label(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    c.setFont("Times-Bold", 12)
    c.drawString(72, h - 72, "ENVELOPE FACE — tape or copy onto the large envelope")
    c.setFont("Times-Roman", 10)
    c.drawString(72, h - 90, "First-Class Mail  ·  postage prepaid  ·  do not use Certified unless you also keep first-class")
    c.setFont("Times-Roman", 11)
    c.drawString(72, h - 140, "FROM:")
    y = h - 158
    for row in [
        "Brendan Ngwa Nforbi",
        "1455 Cat Tail Drive",
        "Stockton, CA 95204",
    ]:
        c.drawString(90, y, row)
        y -= 16
    c.setFont("Times-Bold", 14)
    c.drawString(72, h - 240, "TO:")
    y = h - 262
    c.setFont("Times-Bold", 16)
    for row in ENVELOPE_LINES:
        c.drawString(90, y, row)
        y -= 22
    c.setFont("Times-Roman", 10)
    c.drawString(72, 120, "Nforbi v. Meza-Gonzalez et al., N.D. Cal. No. 4:26-cv-08271-ASK")
    c.drawString(72, 104, "Cal. Code Civ. Proc. § 415.20(b) follow-up copies — individual capacity")
    c.save()
    return path


def write_instructions_pdf(path: Path, exec_date: str, mailed_from: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    y = h - 56

    def line(text: str, size: float = 10.5, bold: bool = False, dy: float = 13) -> None:
        nonlocal y
        if y < 56:
            c.showPage()
            y = h - 56
        c.setFont("Times-Bold" if bold else "Times-Roman", size)
        c.drawString(54, y, text)
        y -= dy

    def wrapped(text: str, *, size: float = 10.5, bold: bool = False) -> None:
        nonlocal y
        font = "Times-Bold" if bold else "Times-Roman"
        words = text.split()
        current = ""
        max_w = w - 108
        for word in words:
            trial = f"{current} {word}".strip()
            if c.stringWidth(trial, font, size) <= max_w:
                current = trial
            else:
                line(current, size=size, bold=bold)
                current = word
        if current:
            line(current, size=size, bold=bold)

    line("PLAINTIFF COPY — DO NOT FILE — DO NOT PUT THIS SHEET IN THE MEZA ENVELOPE", 11, True)
    line(f"Nforbi v. Meza-Gonzalez et al., {CASE_NO}  ·  papers dated {exec_date}", 10, True, 16)

    line("What Dkt. 16 actually is", 12, True, 16)
    wrapped(
        "Keep Documents 16 / 16-1. They prove two attempts (Aug. 25, 4:00 p.m.; "
        "Aug. 26, 10:15 a.m.) and leaving the right stack with Kim S. - H.R. at "
        "4030 Kiernan Avenue on Aug. 27 at 1:30 p.m. They do not close Rule 4. "
        "The form says a declaration of diligence and/or mailing is attached if "
        "applicable. You filed diligence only. No mail date. No first-class "
        "recital. No postage. Workplace substitute service here is Rule 4(e)(1) "
        "using CCP § 415.20(b). That statute is leave-plus-mail. Service is "
        "complete on the 10th day after mailing."
    )
    y -= 6
    line("It is not Rule 4(e)(2): not personal delivery, not dwelling service,", 10.5)
    line("and Kim S. is not identified as an authorized agent. Melano's return", 10.5)
    line("said Officer Reed was designated to accept at that station. This one", 10.5)
    line("does not say that about Kim S.", 10.5, dy=16)

    line("Do not treat September 17 as a default date", 12, True, 16)
    wrapped(
        "Haiyang Li is not the defendant. These papers were not left with him. "
        "He has no Rule 12(a) duty in this action until he appears or the Court "
        "orders him to accept service (Dkt. 13 is that ask; it is already on "
        "file). Counting 21 days from August 27 lands on Thursday, September 17. "
        "That is the weak theory. Li will say exactly what the return shows: "
        "two attempts, papers left with HR, no mail follow-up, not an authorized "
        "agent. Until this mailing goes out — or the Court grants Dkt. 13 — "
        "there is no completed 415.20 service and no clean 12(a) date."
    )
    y -= 8

    line("What goes in the Meza envelope (first-class, postage prepaid)", 12, True, 16)
    line("Use the assembled mailing bundle, or print these in this order:", 10.5)
    line("  1. Cover letter (signed) — one page")
    line("  2. Issued Meza summons only (Dkt. 3, page 2 — 4030 Kiernan Ave.)")
    line("  3. First Amended Complaint, Dkt. 5 (21 pages)")
    line("  4. Notice Identifying the Operative FAC (2 pages)")
    line("  5. CMC / ADR order, Dkt. 4 (2 pages)")
    line("Address: Santiago Meza-Gonzalez / CHP Modesto Area /", 10.5)
    line("4030 Kiernan Avenue / Modesto, CA 95356", 10.5)
    line("That is the place where Fischer left the copies. The statute requires", 10.5)
    line("mailing to that place. Individual capacity. Do not put Dkt. 16 in", 10.5)
    line("this envelope. Do not put this instruction sheet in it. Do not put a", 10.5)
    line("GitHub or document-store link in it.", 10.5, dy=16)

    line("Who drops it in the mail", 12, True, 16)
    wrapped(
        "CCP § 414.10 says a summons may be served by a person who is at least "
        "18 and not a party. Fischer already left the papers. The safer mailing "
        "is by any adult who is not you — a friend, a roommate, another server. "
        "That person signs the non-party declaration. If you mail it yourself, "
        "use the Plaintiff-signed declaration. Mail either way rather than skip. "
        "Date the declaration the day the envelope actually goes in. City of "
        f"mailing on these papers: {mailed_from}. Match the USPS receipt."
    )
    y -= 8

    line("After the envelope is in the mail — same day if you can", 12, True, 16)
    line("  1. Keep the USPS receipt. Tape it behind the Exhibit A cover.")
    line("  2. Sign the matching declaration (you, or the non-party mailer).")
    line("  3. File with the N.D. Cal. San Jose clerk: declaration + Exhibit A")
    line("     + proof of service. Same path Dkt. 13 and Dkt. 16 used.")
    line("  4. Serve that filing by first-class on Li, Melano, and Meza")
    line("     (the POS already lists them).")
    line("  5. Send Li the covering email (EMAIL_DRAFT_Li_CCP_41520_Mailing_Meza.txt).")
    line("     Attach the signed declaration from your computer. No GitHub URL.", dy=16)

    line("The clock once the mail goes out", 12, True, 16)
    wrapped(
        f"If mailed {exec_date}: service is complete on the 10th day after "
        "mailing, then Rule 12(a) adds 21 days, and Rule 6 skips a weekend "
        "or holiday last day. For a September 16 or September 17 mailing that "
        "is Monday, October 19, 2026. Do not write that date on anything Li "
        "or Meza will see. Do not start a default clock until the mailing is "
        "done and the tenth day has run. Dkt. 13 stays on file. Completing "
        "this mailing does not withdraw it."
    )
    c.save()
    return path


def write_how_to_txt(path: Path, exec_date: str, mailed_from: str) -> Path:
    path.write_text(
        f"""PLAINTIFF COPY — DO NOT FILE — DO NOT MAIL THIS SHEET TO MEZA
Nforbi v. Meza-Gonzalez et al., {CASE_NO}
Papers dated {exec_date}. City of mailing: {mailed_from}.

AGREE with the assessment. Dkt. 16 / 16-1 is diligence and delivery to the
Modesto office. It is not completed CCP § 415.20(b) service. It is not
Rule 4(e)(2). It does not start a clean September 17 clock against Li
(he is not the defendant). It is a weak default clock against Meza.

ENVELOPE TO MEZA (first-class, postage prepaid)
  Santiago Meza-Gonzalez
  California Highway Patrol, Modesto Area
  4030 Kiernan Avenue
  Modesto, CA 95356

  1. Cover letter
  2. Meza summons only (Dkt. 3 page 2)
  3. FAC Dkt. 5
  4. Notice identifying the operative FAC
  5. CMC/ADR order Dkt. 4

Do not enclose Dkt. 16, this sheet, the declaration, or any URL.

WHO MAILS
  Preferred: any adult who is not a party, then use the non-party declaration.
  If you mail it: use the Plaintiff-signed declaration. CCP § 414.10 is why
  a non-party is cleaner. Mail either way rather than wait.

SAME DAY AFTER MAILING
  Keep the USPS receipt. File declaration + Exhibit A + POS with the San Jose
  clerk. Serve Li, Melano, and Meza. Send Li the covering email. No GitHub.

CLOCK
  Mail date + 10 days = service complete. Then + 21 days (Rule 6 if the last
  day is a weekend). September 16 or 17 mailing → Monday, October 19, 2026.
  Do not treat tomorrow as a default date. Leave Dkt. 13 on file.
"""
    )
    return path


def write_email(path: Path, exec_date: str) -> Path:
    body = f"""To: Haiyang.Li@doj.ca.gov
Subject: Nforbi v. Meza-Gonzalez, 4:26-cv-08271-ASK — Documents 16 / 16-1 and section 415.20(b) mailing

Counsel:

I filed the Fischer / Run With It Declaration of Service and Declaration of Reasonable Diligence on September 14, 2026, as Documents 16 and 16-1. That return shows substituted delivery to Kim S., H.R., at CHP Modesto Area, 4030 Kiernan Avenue, on August 27, 2026, after attempts on August 25 and August 26. It does not recite a mailing.

On {exec_date} I mailed first-class, postage prepaid, copies of the issued summons, the Dkt. 5 First Amended Complaint, the notice identifying that First Amended Complaint, and the Dkt. 4 CMC/ADR order to Officer Santiago Meza-Gonzalez at 4030 Kiernan Avenue, Modesto, California 95356, the place where the copies were left. The declaration of that mailing is attached and is being filed.

This is the California Code of Civil Procedure section 415.20(b) mailing. It does not ask you to accept service and does not withdraw Document 13.

Thank you,
Brendan Ngwa Nforbi
Plaintiff, In Propria Persona
"""
    path.write_text(body)
    return path


def build_declaration(
    out: Path,
    *,
    caption_right: list,
    footer: str,
    content: list[tuple[str, str]],
    exec_date: str,
    mailed_from: str,
    plaintiff: bool,
) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=footer)
    _header_block(d, caption_right)
    _render_body(d, content)
    if plaintiff:
        _plaintiff_signature(d, exec_date, mailed_from)
    else:
        _nonparty_signature(d, exec_date, mailed_from)
    d.save()
    return out


def build_pos(out: Path, exec_date: str, mailed_from: str) -> Path:
    recipients: list[str] = []
    recipients.extend(LI_BLOCK)
    recipients.append("")
    recipients.extend(MELANO_BLOCK)
    recipients.append("")
    recipients.extend(MEZA_BLOCK)
    return build_proof_of_service(
        out,
        ProofOfServiceFields(
            plaintiff_line="BRENDAN NGWA NFORBI",
            plaintiff_role="Plaintiff",
            defendant_lines=[
                "SANTIAGO MEZA-GONZALEZ; JOSE MELANO;",
                "and DOES 1-10",
            ],
            defendant_role="Defendants",
            case_number=CASE_NO,
            district_line=DISTRICT_NDCAL,
            title="PROOF OF SERVICE",
            service_date=exec_date,
            document_title=(
                "Declaration of Mailing (Cal. Code Civ. Proc. § 415.20(b) "
                "Follow-Up to Documents 16 / 16-1); Exhibit A"
            ),
            mailing_location=mailed_from,
            recipients=recipients,
            server_name="Brendan Ngwa Nforbi",
            stamp_signature=True,
            signature_on_second_page=True,
        ),
    )


def extract_meza_summons(dest: Path) -> Path:
    if not SUMMONS.is_file():
        raise SystemExit(f"Missing issued summons: {SUMMONS}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    append_page(writer, SUMMONS, MEZA_SUMMONS_PAGE)
    with dest.open("wb") as fh:
        writer.write(fh)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=DEFAULT_DATE)
    parser.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM)
    parser.add_argument(
        "--declaration-only",
        action="store_true",
        help="Write only the mailing declarations; skip the Meza envelope bundle.",
    )
    args = parser.parse_args()

    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    if not args.declaration_only:
        for src in (SUMMONS, FAC, NOTICE, CMC):
            if not src.is_file():
                raise SystemExit(f"Missing source filing: {src}")

    outs = paths_for(args.date)
    if args.declaration_only:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        build_declaration(
            outs["plaintiff_decl"],
            caption_right=PLAINTIFF_CAPTION_RIGHT,
            footer=DECL_FOOTER,
            content=_plaintiff_decl_content(args.date, args.mailed_from),
            exec_date=args.date,
            mailed_from=args.mailed_from,
            plaintiff=True,
        )
        print(f"plaintiff decl: {outs['plaintiff_decl']}")
        print(
            f"FILED_STATUS=False; execution date={args.date}; "
            f"mailed from={args.mailed_from}; declaration-only"
        )
        return

    write_cover_letter(outs["cover_letter"], args.date)
    extract_meza_summons(outs["meza_summons"])
    build_declaration(
        outs["plaintiff_decl"],
        caption_right=PLAINTIFF_CAPTION_RIGHT,
        footer=DECL_FOOTER,
        content=_plaintiff_decl_content(args.date, args.mailed_from),
        exec_date=args.date,
        mailed_from=args.mailed_from,
        plaintiff=True,
    )
    build_declaration(
        outs["nonparty_decl"],
        caption_right=NONPARTY_CAPTION_RIGHT,
        footer=NONPARTY_FOOTER,
        content=_nonparty_decl_content(args.date, args.mailed_from),
        exec_date=args.date,
        mailed_from=args.mailed_from,
        plaintiff=False,
    )
    write_exhibit_cover(
        outs["exhibit_cover"],
        court="UNITED STATES DISTRICT COURT",
        court_line2="NORTHERN DISTRICT OF CALIFORNIA",
        caption="NFORBI v. MEZA-GONZALEZ ET AL.",
        case_no=f"Case No. {CASE_NO}",
        exhibit="A",
        title="USPS receipt — CCP § 415.20(b) mailing to Meza-Gonzalez",
        details=[
            "First-Class Mail to Modesto, CA 95356",
            "4030 Kiernan Avenue — CHP Modesto Area",
            f"{args.date}  ·  {args.mailed_from}",
            "Attach the receipt behind this cover",
        ],
        footer=(
            "Declaration of Mailing — CCP § 415.20(b) — "
            "Nforbi v. Meza-Gonzalez et al. — Exhibit A"
        ),
    )
    build_pos(outs["pos"], args.date, args.mailed_from)
    write_instructions_pdf(outs["instructions"], args.date, args.mailed_from)
    write_envelope_label(outs["label"])
    write_email(outs["email"], args.date)
    write_how_to_txt(outs["how_to"], args.date, args.mailed_from)

    n_mail = assemble(
        [
            outs["cover_letter"],
            outs["meza_summons"],
            FAC,
            NOTICE,
            CMC,
        ],
        outs["mail_bundle"],
    )
    n_file = assemble(
        [
            outs["plaintiff_decl"],
            outs["exhibit_cover"],
            outs["pos"],
        ],
        outs["filing_packet"],
    )
    publish_short_link(outs["mail_bundle"], SHORT_MAIL)
    publish_short_link(outs["filing_packet"], SHORT_FILING)

    print(f"cover letter:   {outs['cover_letter']}")
    print(f"meza summons:   {outs['meza_summons']}")
    print(f"plaintiff decl: {outs['plaintiff_decl']}")
    print(f"nonparty decl:  {outs['nonparty_decl']}")
    print(f"exhibit cover:  {outs['exhibit_cover']}")
    print(f"pos:            {outs['pos']}")
    print(f"instructions:   {outs['instructions']}")
    print(f"label:          {outs['label']}")
    print(f"mail bundle:    {outs['mail_bundle']} ({n_mail} pp.)")
    print(f"filing packet:  {outs['filing_packet']} ({n_file} pp.)")
    print(f"email:          {outs['email']}")
    print(f"how-to:         {outs['how_to']}")
    print(f"short links:    /{SHORT_MAIL}  /{SHORT_FILING}")
    print(
        f"FILED_STATUS=False; execution date={args.date}; "
        f"mailed from={args.mailed_from}"
    )


if __name__ == "__main__":
    main()
