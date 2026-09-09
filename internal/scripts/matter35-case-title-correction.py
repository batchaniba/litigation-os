#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 35 -- correct the case title in the Santa Clara register of actions.

Ngwa Nforbi v. Ross Stores, Inc., et al., Santa Clara Sup. Ct. No. 26CV501995.

The Verified Complaint, the issued SUM-100, and the CM-010 all name the
defendants in this order:

    ROSS STORES, INC., a Delaware corporation; ROSS DRESS FOR LESS, INC.,
    a Virginia corporation; DOE 1; and DOES 2 through 20, inclusive.

The Court's public portal (printed Sept. 8, 2026) instead titles the case
"Brendan Ngwa Nforbi vs Does 2 through 20 et al" and lists the defendant party
records Does-first. The case management system builds the short title from the
first-listed defendant record, so the party-entry step of the Aug. 26, 2026
One Legal submission -- not the pleadings -- is what produced the wrong title.

Two documents, in escalation order:

  1. Letter to the Civil Division Clerk asking for the correction as a
     records/clerical fix (no fee, no hearing, nothing filed). Try this first.
  2. Notice of Errata on pleading paper, for filing if the Clerk wants
     something in the case file before touching the register of actions.

    python3 internal/scripts/matter35-case-title-correction.py [--date "September 9, 2026"]

Outputs (matter-35/):
  - Letter to Civil Division Clerk - Request to Correct Case Title in Register
    of Actions (Sept 9 2026).pdf
  - Notice of Errata and Request to Correct Case Title (26CV501995)
    (Sept 9 2026).pdf
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import (  # noqa: E402
    SIGNATURE_ASPECT,
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
)

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal/public/documents/matter-35"

DEFAULT_EXEC_DATE = "September 9, 2026"

LETTER_OUT = (
    "Letter to Civil Division Clerk - Request to Correct Case Title in Register "
    "of Actions (Sept 9 2026).pdf"
)
NOTICE_OUT = (
    "Notice of Errata and Request to Correct Case Title (26CV501995) "
    "(Sept 9 2026).pdf"
)

PLAINTIFF_PRINT = "Brendan Ngwa Nforbi"
PLAINTIFF_CAPS = "BRENDAN NGWA NFORBI"
CASE_NO = "26CV501995"
CASE_NAME_CORRECT = "Ngwa Nforbi v. Ross Stores, Inc., et al."
PORTAL_TITLE_WRONG = "Brendan Ngwa Nforbi vs Does 2 through 20 et al"

# Party order as it appears on the operative Verified Complaint, the issued
# SUM-100, and the CM-010 -- the order the register of actions should track.
COMPLAINT_PARTY_ORDER = [
    "Ross Stores, Inc., a Delaware corporation;",
    "Ross Dress for Less, Inc., a Virginia corporation;",
    "Doe 1; and",
    "Does 2 through 20, inclusive.",
]

# Defendant party records as the portal listed them on Sept. 8, 2026.
PORTAL_PARTY_ORDER = [
    "Does 2 through 20",
    "Doe 1",
    "Ross Dress for Less, Inc., a Virginia corporation",
    "Ross Stores, Inc., a Delaware corporation",
]

SIG_LINE = "___________________________________"


# ----------------------------------------------------------------------
# 1. Letter to the Civil Division Clerk
# ----------------------------------------------------------------------
def build_letter(out: Path, exec_date: str) -> Path:
    body = ParagraphStyle(
        "body", fontName="Times-Roman", fontSize=12, leading=16.5,
        alignment=TA_JUSTIFY, spaceAfter=12,
    )
    plain = ParagraphStyle(
        "plain", fontName="Times-Roman", fontSize=12, leading=16.5, alignment=TA_LEFT,
    )
    bold = ParagraphStyle(
        "bold", fontName="Times-Bold", fontSize=12, leading=16.5, alignment=TA_LEFT,
    )
    indented = ParagraphStyle(
        "indented", fontName="Times-Roman", fontSize=12, leading=16.5,
        alignment=TA_LEFT, leftIndent=36,
    )

    story = []
    story.append(Paragraph(PLAINTIFF_CAPS, bold))
    story.append(Paragraph("Plaintiff, In Propria Persona", plain))
    story.append(Paragraph("1455 Cat Tail Drive", plain))
    story.append(Paragraph("Stockton, CA 95204", plain))
    story.append(Paragraph("Telephone: (209) 801-4442", plain))
    story.append(Paragraph("E-mail: bnn.cdl@gmail.com", plain))
    story.append(Spacer(1, 28))

    story.append(Paragraph(exec_date, plain))
    story.append(Spacer(1, 18))

    story.append(Paragraph("Clerk of the Court &mdash; Civil Division", plain))
    story.append(Paragraph("Superior Court of California, County of Santa Clara", plain))
    story.append(Paragraph("Downtown Superior Court", plain))
    story.append(Paragraph("191 North First Street", plain))
    story.append(Paragraph("San Jos&eacute;, CA 95113", plain))
    story.append(Spacer(1, 18))

    story.append(Paragraph(
        f"Re:&nbsp;&nbsp;<b>{CASE_NAME_CORRECT}</b> &mdash; Case No. {CASE_NO}<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Request to Correct the Case Title and Defendant "
        "Party Order in the Register of Actions<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hon. Vince Parrett, Department 16 &mdash; "
        "Complaint filed August 26, 2026; first CMC February 11, 2027",
        body,
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Dear Clerk of the Court:", plain))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "I am the Plaintiff in the above-referenced action, appearing in propria persona. "
        "I write to ask the Court to correct the title of this case in the register of "
        "actions and on the public case portal. The title now shown does not match the "
        "caption of the Complaint the Court accepted for filing, and the mismatch came "
        "from the party-entry step of my electronic submission rather than from the "
        "pleadings themselves.",
        body,
    ))

    story.append(Paragraph(
        "I filed this action on August 26, 2026 through One Legal (Filing Order "
        "#29111713; Confirmation #35442871; Court Transaction #24948831). The Court "
        "accepted the filing the same day, assigned Case No. 26CV501995, issued the "
        "Summons, and returned the conformed Verified Complaint, Civil Case Cover Sheet, "
        "and clerk-stamped Civil Lawsuit Notice.",
        body,
    ))

    story.append(Paragraph(
        "<b>The caption on file.</b> The conformed Verified Complaint names the defendants "
        "in this order, and the issued SUM-100 Summons and the CM-010 Civil Case Cover "
        "Sheet name them in the same order:",
        body,
    ))
    for i, line in enumerate(COMPLAINT_PARTY_ORDER, start=1):
        story.append(Paragraph(f"({i})&nbsp;&nbsp;{line}", indented))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "<b>The title on the portal.</b> The public case portal, printed September 8, 2026, "
        f"shows the case title as &ldquo;{PORTAL_TITLE_WRONG},&rdquo; and lists the "
        "defendant party records in this order: &ldquo;Does 2 through 20&rdquo;; "
        "&ldquo;Doe 1&rdquo;; &ldquo;Ross Dress for Less, Inc., a Virginia "
        "corporation&rdquo;; &ldquo;Ross Stores, Inc., a Delaware corporation.&rdquo; "
        "Because the short title is generated from the first-listed defendant record, the "
        "Doe defendants &mdash; who are unidentified, unnamed, and unserved &mdash; now "
        "appear in the title of the case ahead of the two corporate defendants actually "
        "sued by name.",
        body,
    ))

    story.append(Paragraph(
        "<b>What I am asking for.</b> I respectfully request that the Court (1) correct the "
        f"case title in the register of actions and on the portal to &ldquo;{PLAINTIFF_PRINT} "
        "v. Ross Stores, Inc., et al.,&rdquo; and (2) re-sequence the defendant party "
        "records to track the Complaint: Ross Stores, Inc. first, then Ross Dress for Less, "
        "Inc., then Doe 1, then Does 2 through 20. In a complaint, &ldquo;the title of the "
        "action shall include the names of all the parties&rdquo; (Code Civ. Proc., "
        "&sect; 422.40), and California Rules of Court, rule 2.111(4) permits a short title "
        "on later papers stating &ldquo;the name of the first party on each side, with "
        "appropriate indication of other parties.&rdquo; The Complaint on file complies; I "
        "am asking only that the Court's record of it follow the same order.",
        body,
    ))

    story.append(Paragraph(
        "This is a records correction, not a request for substantive relief. I am not "
        "adding, dropping, substituting, or renaming any party, and the correction does "
        "not change the Complaint, the Summons, or any date on the Court's calendar. As of "
        "today no defendant has been served and none has appeared, so no party is "
        "prejudiced by the correction.",
        body,
    ))

    story.append(Paragraph(
        "I would like this fixed before I serve Ross Stores, Inc. and Ross Dress for Less, "
        "Inc. through their agent for service of process, which I must do by approximately "
        "October 25, 2026. Papers that go out under a title naming the Doe defendants first "
        "invite confusion about who has actually been sued, and the same title would carry "
        "forward onto the proof of service, the case management statement, and every order "
        "in the case.",
        body,
    ))

    story.append(Paragraph(
        "If the Court needs something filed in the case before it will correct the register "
        "of actions, I have a Notice of Errata prepared and will submit it the same day, in "
        "whatever form the Court prefers &mdash; e-filed notice, ex parte application, "
        "noticed motion, or a local form. Please let me know which. I would also appreciate "
        "written or electronic confirmation once the correction is made, so that I can serve "
        "papers bearing a title that matches the Court's record.",
        body,
    ))

    story.append(Paragraph(
        "Thank you for your attention to this matter.",
        body,
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Respectfully submitted,", plain))
    story.append(Spacer(1, 6))
    if os.path.isfile(SIGNATURE_PATH):
        img = Image(
            SIGNATURE_PATH, width=2.5 * inch, height=2.5 * inch * SIGNATURE_ASPECT
        )
        img.hAlign = "LEFT"
        story.append(img)
    story.append(Paragraph(PLAINTIFF_PRINT, plain))
    story.append(Paragraph("Plaintiff, In Propria Persona", plain))
    story.append(Spacer(1, 18))

    story.append(Paragraph("Enclosures:", plain))
    story.append(Paragraph(
        "1.&nbsp;&nbsp;Public case portal printout, Case No. 26CV501995 "
        "(printed September 8, 2026)", indented))
    story.append(Paragraph(
        "2.&nbsp;&nbsp;Conformed Verified Complaint, caption page (filed August 26, 2026)",
        indented))
    story.append(Paragraph(
        "3.&nbsp;&nbsp;Issued SUM-100 Summons (filed August 26, 2026)", indented))
    story.append(Paragraph(
        "4.&nbsp;&nbsp;One Legal Order #29111713 status page (Confirmation #35442871)",
        indented))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"cc: File ({CASE_NAME_CORRECT}, {CASE_NO})", plain))

    out.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(out),
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch,
        title="Letter to Civil Division Clerk - Correct Case Title (26CV501995)",
    )
    doc.build(story)
    return out


# ----------------------------------------------------------------------
# 2. Notice of Errata (pleading paper) -- filed only if the Clerk asks
# ----------------------------------------------------------------------
FOOTER = (
    "PLAINTIFF'S NOTICE OF ERRATA AND REQUEST TO CORRECT THE CASE TITLE "
    "-- NGWA NFORBI v. ROSS STORES, INC., ET AL."
)

PLAINTIFF_BLOCK = [
    (PLAINTIFF_CAPS, "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    (PLAINTIFF_CAPS + ",", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("ROSS STORES, INC., a Delaware", True, False),
    ("corporation; ROSS DRESS FOR LESS,", True, False),
    ("INC., a Virginia corporation; DOE 1;", True, False),
    ("and DOES 2 through 20, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    (f"Case No. {CASE_NO}", False, False),
    ("", False, False),
    ("PLAINTIFF'S NOTICE OF ERRATA", True, False),
    ("AND REQUEST TO CORRECT THE", True, False),
    ("CASE TITLE IN THE REGISTER OF", True, False),
    ("ACTIONS", True, False),
    ("", False, False),
    ("(Code Civ. Proc., sec. 422.40;", False, False),
    ("Cal. Rules of Court, rule 2.111(4))", False, False),
    ("", False, False),
    ("Judge: Hon. Vince Parrett", False, False),
    ("Dept.: 16", False, False),
    ("Complaint Filed: August 26, 2026", False, False),
    ("First CMC: February 11, 2027", False, False),
    ("", False, False),
    ("[No hearing requested]", False, True),
]

CONTENT = [
    ("PARA", "TO THE CLERK OF THE COURT AND TO THE HONORABLE VINCE PARRETT:"),
    ("PARA",
     f"Plaintiff {PLAINTIFF_CAPS}, appearing in propria persona, submits this notice for "
     "one limited purpose: to correct the title of this action as it appears in the "
     "Court's register of actions and on the Court's public case portal, which does not "
     "match the caption of the Verified Complaint the Court accepted for filing. The "
     "correction is clerical. It seeks no substantive relief, affects no party's rights, "
     "and requires no hearing."),

    ("HEADER", "I.\nTHE CAPTION ON FILE"),
    ("PARA",
     "1. Plaintiff filed this action on August 26, 2026 by electronic submission through "
     "One Legal (Filing Order #29111713; Confirmation #35442871; Court Transaction "
     "#24948831). The Court accepted the filing the same day, assigned Case No. "
     "26CV501995, issued the Summons, and returned the conformed Verified Complaint, "
     "Civil Case Cover Sheet, and clerk-stamped Civil Lawsuit Notice."),
    ("PARA",
     "2. The conformed Verified Complaint names the defendants in the following order: "
     "ROSS STORES, INC., a Delaware corporation; ROSS DRESS FOR LESS, INC., a Virginia "
     "corporation; DOE 1; and DOES 2 through 20, inclusive. The issued SUM-100 Summons "
     "and the CM-010 Civil Case Cover Sheet name the same defendants in the same order. "
     "Ross Stores, Inc. is, and has been since filing, the first-named defendant."),

    ("HEADER", "II.\nTHE TITLE IN THE REGISTER OF ACTIONS"),
    ("PARA",
     "3. The Court's public case portal, printed September 8, 2026, states the title of "
     f"this action as \"{PORTAL_TITLE_WRONG}.\" The portal lists the defendant party "
     "records in this order: \"Does 2 through 20\"; \"Doe 1\"; \"Ross Dress for Less, "
     "Inc., a Virginia corporation\"; \"Ross Stores, Inc., a Delaware corporation.\""),
    ("PARA",
     "4. The order of those party records is the source of the error. The case title is "
     "generated from the first-listed defendant record, and the defendant records were "
     "transmitted to the Court in the party-entry step of Plaintiff's August 26, 2026 "
     "electronic submission in an order that does not track the Complaint. The result is "
     "a case title in which the fictitiously named defendants -- who are unidentified, "
     "unnamed in the caption, and unserved -- stand ahead of the two corporate defendants "
     "actually sued by name. The pleadings themselves are correct; only the Court's "
     "record of the party order is not."),

    ("HEADER", "III.\nTHE CORRECTION SOUGHT"),
    ("PARA",
     "5. In a complaint, \"the title of the action shall include the names of all the "
     "parties.\" (Code Civ. Proc., sec. 422.40.) California Rules of Court, rule 2.111(4) "
     "requires that the name of each party begin on a separate line in the title of an "
     "initial complaint, and permits later papers to carry a short title \"stating the "
     "name of the first party on each side, with appropriate indication of other "
     "parties.\" The Complaint on file complies with both. Plaintiff asks only that the "
     "Court's record of the case follow the caption it already has."),
    ("PARA",
     "6. Plaintiff respectfully requests that the Clerk:"),
    ("LIST_ITEM",
     "(a) correct the title of this action in the register of actions and on the public "
     f"case portal to \"{PLAINTIFF_PRINT} v. Ross Stores, Inc., et al.\";"),
    ("LIST_ITEM",
     "(b) re-sequence the defendant party records to track the Verified Complaint: "
     "(1) Ross Stores, Inc., a Delaware corporation; (2) Ross Dress for Less, Inc., a "
     "Virginia corporation; (3) Doe 1; and (4) Does 2 through 20, inclusive; and"),
    ("LIST_ITEM",
     "(c) confirm the correction, so that Plaintiff may serve papers bearing a title that "
     "matches the Court's record."),
    ("PARA",
     "7. No party is prejudiced. As of the date of this notice, no defendant has been "
     "served and no defendant has appeared. Plaintiff does not seek to add, drop, "
     "substitute, or rename any party; the Doe defendants remain unidentified and will be "
     "substituted, if at all, by amendment under Code of Civil Procedure section 474. "
     "Nothing in this notice changes the Complaint, the Summons, the deadline to serve, "
     "or the February 11, 2027 case management conference."),
    ("PARA",
     "8. If the Court prefers that this request be presented by ex parte application, by "
     "noticed motion, or on a local form, Plaintiff will promptly submit it in that form."),
]


def _signature(d, exec_date: str) -> None:
    d.ensure_space(9)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(PLAINTIFF_CAPS, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=20)


def build_notice(out: Path, exec_date: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    c = d.c

    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()

    d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    d.write_line("COUNTY OF SANTA CLARA", bold=True, center=True)
    d.blank_line()

    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10,
                         tight_lh=13, boxed=True)
    d.blank_line()

    for kind, text in CONTENT:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")

    _signature(d, exec_date)
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=DEFAULT_EXEC_DATE,
                    help="Date printed on the letter and the notice")
    args = ap.parse_args()
    letter_path = build_letter(OUT_DIR / LETTER_OUT, args.date)
    print(f"Generated: {letter_path}")
    notice_path = build_notice(OUT_DIR / NOTICE_OUT, args.date)
    print(f"Generated: {notice_path}")


if __name__ == "__main__":
    main()
