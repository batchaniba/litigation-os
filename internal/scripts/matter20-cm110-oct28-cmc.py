#!/usr/bin/env python3
"""Matter 20 — Case Management Statement (CM-110) for the October 28, 2026 CMC.

Newanforbi v. California Highway Patrol, et al., Alameda Sup. Ct. No. 26CV191136,
Dept. 25 (Hon. Jenna M. Whitman). Executed October 5, 2026.

The official CM-110 is not downloadable from this environment, so the blank is
derived from the June 30, 2026 filed CM-110: the filled-in values (embedded
subset font and Helvetica header values), the old X marks, the e-filing stamp,
the old signature, and the print-button bar are removed; the printed form text
(Arial) is kept. Then this script draws the new values.

Rule 3.725: file and serve no later than 15 calendar days before the CMC
(October 13, 2026). Rule 3.724 meet and confer: Sept. 30 email; Oct. 1 Teams call
with DAG Vanessa K. Ing; Ing's Oct. 1 memorialization; Petitioner's Oct. 1 reply.

  python3 internal/scripts/matter20-cm110-oct28-cmc.py

FILED_STATUS: False until filed through One Legal and served on DAG Ing.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))

import pymupdf  # noqa: E402
from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402
from signature_stamp import (  # noqa: E402
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
    stamp_on_pdf_line,
)

FILED_STATUS = False

EXEC_DATE = "October 5, 2026"
EXEC_PLACE = "Stockton, California"

REPO_ROOT = Path(SCRIPT_DIR).parents[1]
DOCS = REPO_ROOT / "internal" / "public" / "documents"
SOURCE_JUNE30 = DOCS / "matter-32" / "from-20" / (
    "Case Management Statement (CM-110) (filed June 30, 2026).pdf"
)
BLANK = DOCS / "_form-library" / "cm110-blank-template-derived.pdf"
OUT_DIR = DOCS / "matter-20"
CM110_OUT = OUT_DIR / "Case Management Statement CM-110 (Oct 28 2026 CMC) (Executed Oct 5 2026).pdf"
POS_OUT = OUT_DIR / "Proof of Electronic Service - CM-110 (Oct 5 2026).pdf"
PACKET_OUT = OUT_DIR / "Case Management Statement CM-110 with POS (Executed Oct 5 2026).pdf"
EMAIL_OUT = OUT_DIR / "EMAIL_DRAFT_Ing_CM-110_Oct_5_2026.txt"

PETITIONER = "Brendan Ngehsi Newanforbi"
RESPONDENT = "California Highway Patrol; G. Serrato, et al."
CASE_NO = "26CV191136"

FONT = "helv"
FONT_B = "hebo"
BLUE_BLACK = (0, 0, 0)


# ---------------------------------------------------------------- blank form

def build_blank(src: Path, dst: Path) -> Path:
    if not src.is_file():
        raise SystemExit(
            f"Missing source CM-110: {src}\n"
            "Fetch it first: npm run docs:fetch "
            "4a8158830d687b1c7c3c0dba1a5ef578a262da82f204249e7842275563ae9571"
        )
    d = pymupdf.open(src)
    d.delete_page(5)
    for p in d:
        for bl in p.get_text("dict")["blocks"]:
            for ln in bl.get("lines", []):
                for s in ln["spans"]:
                    if s["font"].startswith("font0000") or s["font"] == "Helvetica":
                        p.add_redact_annot(pymupdf.Rect(s["bbox"]), fill=None)
        p.apply_redactions(
            images=pymupdf.PDF_REDACT_IMAGE_NONE,
            graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
        )
        # Old X marks: small line drawings inside checkboxes. Cover the inside
        # of each box only, so the box border stays.
        for dr in p.get_drawings():
            r = dr["rect"]
            if r.width < 12 and r.height < 12 and len(dr["items"]) >= 2 and all(
                it[0] == "l" for it in dr["items"]
            ):
                p.draw_rect(pymupdf.Rect(r.x0 + 0.6, r.y0 + 0.6, r.x1 - 0.6, r.y1 - 0.6),
                            color=None, fill=(1, 1, 1), width=0)
    # Old X marks by position (from the June 30 drawing scan), in case any
    # were drawn with curve segments and missed above.
    old_marks = {
        0: [(70, 394), (70, 481), (141, 668)],
        1: [(55, 157), (255, 183), (70, 253), (70, 376), (462, 407), (273, 586), (84, 694)],
        2: [(206, 237), (206, 304)],
        3: [(55, 466), (70, 646)],
        4: [(56, 240), (71, 334), (71, 414)],
    }
    for pn, marks in old_marks.items():
        for x, y in marks:
            d[pn].draw_rect(pymupdf.Rect(x + 0.7, y + 0.5, x + 9.3, y + 8.7),
                            color=None, fill=(1, 1, 1), width=0)
    # 10a(1) "has": the old X there is a filled glyph; clear the whole box interior.
    d[1].draw_rect(pymupdf.Rect(268.8, 586.4, 285.6, 594.2), color=None, fill=(1, 1, 1), width=0)
    p0 = d[0]
    p0.draw_rect(pymupdf.Rect(418, 96, 568, 196), color=None, fill=(1, 1, 1), width=0)
    p4 = d[4]
    p4.draw_rect(pymupdf.Rect(345, 572, 470, 595), color=None, fill=(1, 1, 1), width=0)
    p4.draw_rect(pymupdf.Rect(30, 756, 590, 790), color=None, fill=(1, 1, 1), width=0)
    # The "19. Meet and confer" heading was clipped by an overlapping value span.
    p4.draw_rect(pymupdf.Rect(50, 317, 125, 328), color=None, fill=(1, 1, 1), width=0)
    p4.insert_text((50.7, 325.6), "Meet and confer", fontname=FONT_B, fontsize=9)
    dst.parent.mkdir(parents=True, exist_ok=True)
    d.save(dst, garbage=3, deflate=True)
    return dst


# ---------------------------------------------------------------- helpers

def t(p, x, y, s, size=9, bold=False):
    p.insert_text((x, y), s, fontname=FONT_B if bold else FONT, fontsize=size, color=BLUE_BLACK)


def box(p, rect, s, size=8.5):
    r = pymupdf.Rect(*rect)
    while size >= 7.5:
        shape = p.new_shape()
        if shape.insert_textbox(r, s, fontname=FONT, fontsize=size, color=BLUE_BLACK, lineheight=1.15) >= 0:
            shape.commit()
            return
        size -= 0.2
    raise SystemExit(f"Text overflow on page {p.number + 1} in {rect}: {s[:60]}...")


def x_mark(p, label_x, label_top):
    """Draw an X in the checkbox that sits just left of a printed label."""
    x0, y0 = label_x - 18.4, label_top + 0.8
    x1, y1 = x0 + 8.4, y0 + 7.6
    p.draw_line((x0, y0), (x1, y1), color=BLUE_BLACK, width=1.1)
    p.draw_line((x0, y1), (x1, y0), color=BLUE_BLACK, width=1.1)


def header(p):
    t(p, 155.4, 57.0, PETITIONER)
    t(p, 155.8, 70.9, RESPONDENT)
    t(p, 453.0, 56.5, CASE_NO)


# ---------------------------------------------------------------- form pages

ITEM_4A = (
    "Verified Petition for Writ of Mandate (Code Civ. Proc. § 1085; Pen. Code § 679.10) challenging Respondent "
    "CHP's April 20, 2026 denial of Petitioner's request for U nonimmigrant status certification (Form I-918, "
    "Supplement B). Under the August 29, 2026 order, the First Cause of Action (abuse of discretion in refusing "
    "certification) proceeds; the Second and Third were sustained without leave; the Fourth (declaratory relief) "
    "was sustained with leave to amend, and no amended petition has been filed."
)

ITEM_4B = (
    "Petitioner seeks a peremptory writ of mandate directing CHP to set aside its April 20, 2026 denial of his "
    "April 9, 2026 certification request and to reconsider the request under the correct legal standard. The "
    "request arises from Petitioner's November 1, 2024 detention and arrest by CHP officers on Interstate 580; no "
    "criminal complaint was filed. Relief sought is equitable only. No damages are sought. See Attachment 4b."
)


def fill_form(blank: Path, dst: Path, attachment_pages: int) -> Path:
    d = pymupdf.open(blank)

    # Page 1
    p = d[0]
    t(p, 59.0, 68.6, "BRENDAN NGEHSI NEWANFORBI", 7.5)
    t(p, 97.0, 91.8, "1455 Cat Tail Drive", 7.5)
    t(p, 56.0, 103.4, "Stockton", 7.5)
    t(p, 265.0, 103.4, "CA", 7.5)
    t(p, 328.3, 103.4, "95204", 7.5)
    t(p, 90.0, 115.0, "(209) 801-4442", 7.5)
    t(p, 92.6, 126.5, "bnn.cdl@gmail.com", 7.5)
    t(p, 109.0, 138.2, "Petitioner, In Pro Per", 7.5)
    t(p, 229.2, 152.7, "ALAMEDA", 7.5, bold=True)
    t(p, 98.5, 163.6, "1225 Fallon Street", 7.0)
    t(p, 98.5, 174.4, "1225 Fallon Street", 7.0)
    t(p, 98.5, 185.4, "Oakland, CA 94612", 7.0)
    t(p, 98.5, 196.8, "Rene C. Davidson Courthouse", 7.0)
    t(p, 152.0, 212.0, PETITIONER, 7.5)
    t(p, 152.0, 225.5, RESPONDENT, 7.5)
    t(p, 401.5, 256.0, CASE_NO, 9)
    x_mark(p, 126.5, 251.4)  # unlimited
    t(p, 63.0, 315.0, "October 28, 2026", 9)
    t(p, 217.0, 315.0, "4:00 p.m.", 9)
    t(p, 310.0, 315.0, "25", 9)
    x_mark(p, 88.9, 394.3)  # 1a
    t(p, 270.7, 402.3, f"{PETITIONER} (Petitioner)", 9)
    t(p, 204.0, 447.5, "May 29, 2026", 9)
    x_mark(p, 89.2, 481.0)  # 3a
    x_mark(p, 159.7, 668.0)  # 4a complaint (petition)
    box(p, (66, 680, 576, 730), ITEM_4A, 8.2)

    # Page 2
    p = d[1]
    header(p)
    box(p, (66, 114, 576, 157), ITEM_4B, 8.2)
    x_mark(p, 74.6, 157.6)  # attachment 4b
    x_mark(p, 274.3, 183.0)  # nonjury
    x_mark(p, 88.9, 252.8)  # 6b
    box(p, (142, 264, 576, 288),
        "Writ proceeding; no trial. Hearing on Petitioner's motion for peremptory writ of mandate (First Cause of "
        "Action) is reserved for January 8, 2027, at 9:00 a.m., Dept. 25 (Reservation ID 958052306492).", 8.5)
    x_mark(p, 89.3, 375.7)  # 7b hours
    t(p, 213.0, 384.0, "2 hours (hearing on the writ)", 9)
    x_mark(p, 480.8, 407.2)  # 8 by the following
    t(p, 104.0, 428.6, f"{PETITIONER} (self-represented)", 9)
    t(p, 89.0, 442.4, "None", 9)
    t(p, 103.0, 456.5, "1455 Cat Tail Drive, Stockton, CA 95204", 9)
    t(p, 146.0, 470.4, "(209) 801-4442", 9)
    t(p, 393.0, 470.5, "None", 9)
    t(p, 127.0, 485.5, "bnn.cdl@gmail.com", 9)
    t(p, 417.0, 485.8, "Petitioner", 9)
    x_mark(p, 249.0, 610.5)  # 10a(2) has reviewed
    x_mark(p, 100.3, 694.0)  # 10b(3) exempt
    box(p, (104, 715, 576, 740),
        "Petition for writ of mandate seeking only equitable relief; no money damages are claimed "
        "(Code Civ. Proc., § 1141.11; Cal. Rules of Court, rule 3.811).", 8.5)

    # Page 3 (ADR table)
    p = d[2]
    header(p)
    x_mark(p, 206.0 + 18.4 - 0.4, 237.0 - 0.3)  # mediation willing
    x_mark(p, 206.0 + 18.4 - 0.4, 304.0 - 0.3)  # settlement conference willing

    # Page 4
    p = d[3]
    header(p)
    x_mark(p, 90.1, 257.5)  # 13a related cases
    t(p, 146.0, 280.8, "Newanforbi v. Serrato", 9)
    t(p, 146.0, 294.6, "U.S. District Court, Northern District of California (San Francisco)", 9)
    t(p, 146.0, 308.8, "3:26-cv-05953-CRB", 9)
    t(p, 146.0, 322.6, "Pending; motion to dismiss set for November 20, 2026 (Breyer, J.)", 9)
    x_mark(p, 89.5, 330.6)  # additional cases in attachment 13a
    x_mark(p, 74.2, 466.4)  # 15 other motions
    box(p, (74, 478, 576, 508),
        "Petitioner: motion for peremptory writ of mandate on the First Cause of Action (Code Civ. Proc., § 1085), "
        "hearing reserved January 8, 2027, 9:00 a.m., Dept. 25; to be filed and served in early November 2026 with "
        "briefing under Code Civ. Proc., § 1005(b). See Attachment 18.", 8.5)
    x_mark(p, 89.8, 543.2)  # 16b
    rows = [
        ("Respondents", "Written responses to Petitioner's Request for Production, Set One (served Sept. 16, 2026)",
         "Oct. 20, 2026"),
        ("Respondents", "Production of non-privileged responsive records (denial letter, arrest-investigation report,",
         "Shortly after"),
        ("", "Pen. Code § 851.6 certificate, Nov. 1, 2024 dashcam), as stated at the Oct. 1 meet and confer",
         "Oct. 20, 2026"),
        ("Respondents", "No affirmative discovery intended (Oct. 1, 2026 meet and confer)", "None"),
    ]
    y = 582.0
    for party, desc, date in rows:
        t(p, 52.0, y, party, 8.2)
        t(p, 112.0, y, desc, 8.2)
        t(p, 496.0, y, date, 8.2)
        y += 12.5
    x_mark(p, 88.4, 646.1)  # 16c
    box(p, (74, 668, 576, 724),
        "Respondents reserved privilege and redaction objections. Petitioner will review any privilege or redaction "
        "log and meet and confer before any motion to compel. Electronically stored information: the November 1, "
        "2024 CHP dashcam audio-video recording, lodged September 8, 2026, and provided to Respondents' counsel "
        "through the Department of Justice file-exchange link on October 1, 2026.", 8.5)

    # Page 5
    p = d[4]
    header(p)
    x_mark(p, 74.8, 240.2)  # 18
    box(p, (74, 262, 576, 314),
        "See Attachment 18: (1) confirm the January 8, 2027 hearing on the First Cause of Action and set briefing "
        "under Code Civ. Proc., § 1005(b) (Respondents proposed a continuance to February 4, 2027; Petitioner does "
        "not agree); (2) Respondents' answer, due by October 12, 2026; (3) status of the Fourth Cause of Action; "
        "(4) authenticity of CHP's own records for the hearing.", 8.5)
    x_mark(p, 89.8, 334.3)  # 19a
    box(p, (89, 356, 576, 410),
        "Petitioner wrote to Respondents' counsel, Deputy Attorney General Vanessa K. Ing, on September 30, 2026. "
        "The parties met and conferred by video conference on October 1, 2026, on all rule 3.724 subjects. "
        "Counsel memorialized the discussion in writing on October 1, and Petitioner confirmed it, with "
        "clarifications, the same day. See Attachment 19.", 8.5)
    x_mark(p, 89.4, 414.0)  # 19b
    box(p, (89, 436, 576, 500),
        "(1) The remaining Respondents will file their answer by October 12, 2026. (2) Respondents will serve "
        "written responses to Request for Production, Set One, by October 20, 2026, with production of "
        "non-privileged records to follow shortly. (3) Respondents do not intend to serve affirmative discovery. "
        "(4) Authenticity of CHP records will be revisited closer to the hearing. Not agreed: the hearing date "
        "and briefing schedule (Attachment 18, item 1).", 8.5)
    t(p, 214.0, 512.0, str(attachment_pages), 9)
    t(p, 62.0, 570.0, EXEC_DATE, 9)
    t(p, 60.0, 596.0, "BRENDAN NGEHSI NEWANFORBI", 9)
    stamp_on_pdf_line(p, 372.0, 492.0, 597.5, whiteout=False)

    dst.parent.mkdir(parents=True, exist_ok=True)
    d.save(dst, garbage=3, deflate=True)
    return dst


# ---------------------------------------------------------------- attachments

ATTACHMENTS = [
    ("ATTACHMENT 4b", "Brief Statement of the Case (Continued)", [
        "On April 9, 2026, Petitioner submitted a request to Respondent California Highway Patrol (CHP) for "
        "certification on Form I-918, Supplement B, under 8 U.S.C. § 1101(a)(15)(U) and Penal Code section "
        "679.10. The request arises from Petitioner's November 1, 2024 detention and arrest by CHP officers on "
        "Interstate 580 in Livermore. CHP later issued a Penal Code section 851.6 certificate describing the "
        "event as a detention only, and no criminal complaint was filed.",
        "On April 20, 2026, Respondent G. Serrato, Captain and Commander of the CHP Dublin Area, denied the "
        "request on the ground that the incident did not involve qualifying criminal activity.",
        "Petitioner filed his Verified Petition for Writ of Mandate on May 29, 2026. By order dated August 29, "
        "2026 (notice of entry August 31, 2026), the Court overruled the demurrer to the First Cause of Action, "
        "sustained it without leave to amend as to the Second and Third Causes of Action, and sustained it with "
        "leave to amend as to the Fourth Cause of Action. Respondents Dutra and Paul were dismissed by "
        "stipulation. The remaining Respondents are CHP and G. Serrato. No amended petition has been filed.",
        "Relief sought on the First Cause of Action: a peremptory writ of mandate directing CHP to set aside the "
        "April 20, 2026 denial and to reconsider the certification request under the correct legal standard. "
        "No money damages are sought in this action.",
    ]),
    ("ATTACHMENT 13a", "Related Cases (Continued)", [
        "(1) Nforbi v. Meza-Gonzalez, et al., U.S. District Court, Northern District of California (Oakland), "
        "No. 4:26-cv-08271-ASK. Civil rights action under 42 U.S.C. § 1983 arising from the same November 1, 2024 "
        "detention and arrest. Status: pending, pleading stage.",
        "(2) Newanforbi v. Meza-Gonzalez, et al., Superior Court of California, County of Alameda, "
        "No. 26CV168913. State-law claims arising from the same November 1, 2024 events. Status: dismissed "
        "without prejudice on August 15, 2026. Listed for completeness.",
        "None of these cases seeks the relief at issue here, which is limited to CHP's certification decision. "
        "Petitioner does not intend to move to consolidate or coordinate.",
    ]),
    ("ATTACHMENT 18", "Other Issues for the Case Management Conference", [
        "1. Hearing date and briefing on the First Cause of Action. Petitioner reserved January 8, 2027, at "
        "9:00 a.m. in Department 25 (Reservation ID 958052306492) for his motion for a peremptory writ of mandate "
        "on the First Cause of Action. He will file and serve the motion in early November 2026. He proposes the "
        "opposition and reply deadlines set by Code of Civil Procedure section 1005(b). At the October 1, 2026 meet "
        "and confer, Respondents proposed two alternatives: (a) continuing the hearing to February 4, 2027, with "
        "the opening brief due December 21, 2026, the opposition January 11, 2027, and the reply January 20, 2027; "
        "or (b) keeping January 8, 2027, with the opening brief due November 4, 2026, the opposition December 2, "
        "2026, and the reply December 14, 2026. Petitioner does not agree to a continuance. The petition has been "
        "pending since May 29, 2026, and the certification is a prerequisite to the immigration benefit it "
        "supports, so delay is itself prejudicial. Petitioner asks the Court to confirm the January 8, 2027 hearing "
        "and to set briefing under section 1005(b), or as the Court directs.",
        "2. Respondents' answer. Respondents' counsel confirmed that the remaining Respondents will file their "
        "answer to the Petition by October 12, 2026. Petitioner asks that the answer date be confirmed so the "
        "First Cause of Action is at issue well before the hearing.",
        "3. Fourth Cause of Action. The August 29, 2026 order sustained the demurrer to the Fourth Cause of "
        "Action with leave to amend within 20 days of notice of entry. No amended petition has been filed. The "
        "First Cause of Action is the only claim set for hearing.",
        "4. Authenticity of CHP's own records. To narrow the hearing, Petitioner asked Respondents to stipulate to "
        "the authenticity of CHP's own records attached to the Petition: the April 20, 2026 denial letter (Ex. 1), "
        "the arrest-investigation report (Ex. 6), the Penal Code section 851.6 certificate (Ex. 7), and the "
        "November 1, 2024 dashcam recording lodged on September 8, 2026. Respondents consider the issue premature "
        "and will reassess closer to the hearing; they intend to produce true and correct copies of those records. "
        "Petitioner asks the Court to set a date before Respondents' opposition is due by which the parties will "
        "meet and confer and file any stipulation on authenticity.",
        "5. Resolution. Respondents have stated that CHP will not reconsider the April 9, 2026 certification "
        "request. Petitioner remains willing to resolve the First Cause of Action by reconsideration at any time.",
    ]),
    ("ATTACHMENT 19", "Meet and Confer (Continued)", [
        "On September 30, 2026, Petitioner emailed Respondents' counsel, Deputy Attorney General Vanessa K. Ing "
        "(copying Mark Beckington), requesting a rule 3.724 meet and confer and listing the hearing date, the "
        "status of the pleadings, discovery, authenticity of CHP records, and possible resolution.",
        "Counsel and Petitioner met and conferred by Microsoft Teams video conference on October 1, 2026, at "
        "3:30 p.m. Ms. Ing memorialized the discussion by email at 3:55 p.m. that day. Petitioner replied at "
        "5:49 p.m. confirming the summary with these clarifications: Petitioner does not agree to continue the "
        "hearing; he will review any privilege or redaction log when produced; he reserves the authenticity issue; "
        "and he acknowledges CHP's position on reconsideration.",
        "At counsel's request, Petitioner uploaded the November 1, 2024 dashcam recording lodged with the Court "
        "through the Department of Justice file-exchange link on October 1, 2026.",
    ]),
]


def build_attachments(dst: Path) -> int:
    d = pymupdf.open()
    W, H = 612, 792
    for label, subtitle, paras in ATTACHMENTS:
        remaining = list(paras)
        cont = False
        while remaining:
            p = d.new_page(width=W, height=H)
            t(p, 540.4, 45.0, "CM-110", 10, bold=True)
            p.draw_rect(pymupdf.Rect(36, 48, 576, 76), color=(0, 0, 0), width=0.8)
            p.draw_line((396, 48), (396, 76), color=(0, 0, 0), width=0.8)
            t(p, 40, 58, "PLAINTIFF/PETITIONER:", 8)
            t(p, 40, 71, "DEFENDANT/RESPONDENT:", 8)
            t(p, 152, 58, PETITIONER, 9)
            t(p, 152, 71, RESPONDENT, 9)
            t(p, 400, 58, "CASE NUMBER:", 6)
            t(p, 453, 66, CASE_NO, 9)
            heading = label + (" (continued)" if cont else "")
            w = pymupdf.get_text_length(heading, fontname=FONT_B, fontsize=11)
            t(p, (W - w) / 2, 104, heading, 11, bold=True)
            sub = f"to Case Management Statement (CM-110): {subtitle}"
            w = pymupdf.get_text_length(sub, fontname=FONT, fontsize=9.5)
            t(p, (W - w) / 2, 119, sub, 9.5)
            y = 140.0
            while remaining:
                para = remaining[0]
                r = pymupdf.Rect(54, y, 558, 730)
                need = p.insert_textbox(r, para, fontname=FONT, fontsize=10, lineheight=1.35, color=BLUE_BLACK)
                if need < 0:
                    # Does not fit: undo by redrawing on a fresh page.
                    p.draw_rect(r, color=None, fill=(1, 1, 1), width=0)
                    if y == 140.0:
                        raise SystemExit(f"Paragraph too long for one page in {label}")
                    break
                used = (730 - y) - need
                y += used + 12
                remaining.pop(0)
            cont = True
    n = len(d)
    for i, p in enumerate(d):
        s = f"CM-110 Attachments, page {i + 1} of {n}"
        t(p, 36, 760, s, 7)
    d.save(dst, garbage=3, deflate=True)
    return n


# ---------------------------------------------------------------- proof of service

def build_pos(dst: Path) -> Path:
    """Party-signed proof of electronic service (CCP § 1013b). POS-050 recites the
    server is not a party, so it is not used; see matter20-rfp-set-one-chp.py."""
    d = PleadingPaper(str(dst), doc_title_footer=(
        "PROOF OF ELECTRONIC SERVICE — CM-110 — NEWANFORBI v. CHP, ET AL., 26CV191136"
    ))
    c = d.c
    y0 = d._line_y(0)
    for i, (txt, fn) in enumerate([
        ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold"),
        ("Petitioner In Pro Per", "Times-Roman"),
        ("1455 Cat Tail Drive", "Times-Roman"),
        ("Stockton, CA 95204", "Times-Roman"),
        ("Telephone: (209) 801-4442", "Times-Roman"),
        ("E-mail: bnn.cdl@gmail.com", "Times-Roman"),
    ]):
        c.setFont(fn, 12)
        c.drawString(CONTENT_LEFT, y0 - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
    d.blank_line()
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Petitioner,", False, False),
        ("       v.", False, False),
        ("CALIFORNIA HIGHWAY PATROL;", True, False),
        ("G. SERRATO, in his official capacity", True, False),
        ("as Captain and Commander of the CHP", True, False),
        ("Dublin Area; and DOES 1 through 10,", True, False),
        ("inclusive,", True, False),
        ("                          Respondents.", False, False),
    ]
    right = [
        (f"Case No. {CASE_NO}", False, False),
        ("", False, False),
        ("PROOF OF ELECTRONIC SERVICE", True, False),
        ("[Code Civ. Proc. § 1013b]", False, False),
        ("", False, False),
        ("CMC:  October 28, 2026, 4:00 p.m.", False, False),
        ("Dept. 25 — Hon. Jenna M. Whitman", False, False),
        ("Action Filed: May 29, 2026", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    for para in [
        "I, Brendan Ngehsi Newanforbi, declare:",
        "1.  I am over the age of 18 years and am the Petitioner in this action. My electronic service address is "
        "bnn.cdl@gmail.com. My mailing address is 1455 Cat Tail Drive, Stockton, California 95204.",
        f"2.  On {EXEC_DATE}, I electronically served the following document: Case Management Statement "
        "(Judicial Council form CM-110), with Attachments 4b, 13a, 18, and 19, by transmitting a true copy by "
        "electronic mail from bnn.cdl@gmail.com to Vanessa K. Ing, Deputy Attorney General, counsel of record "
        "for Respondents California Highway Patrol and G. Serrato, at Vanessa.Ing@doj.ca.gov.",
        "3.  I transmitted a courtesy copy to Mark.Beckington@doj.ca.gov.",
        "4.  I did not receive, within a reasonable time after the transmission, any electronic message or other "
        "indication that the transmission was unsuccessful.",
        "I declare under penalty of perjury under the laws of the State of California that the foregoing is true "
        f"and correct. Executed on {EXEC_DATE}, at {EXEC_PLACE}.",
    ]:
        d.write_wrapped(para)
        d.blank_line()
    sig_line = "___________________________________"
    w_px, h_px = SIGNATURE_NATIVE_PX
    d.draw_signature_image(SIGNATURE_PATH, w_px, h_px, sig_line, width=165, x_offset=15)
    d.write_line(sig_line, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Petitioner, In Pro Per", right=True, right_margin_offset=20)
    d.save()
    return dst


EMAIL = f"""To: Vanessa.Ing@doj.ca.gov
Cc: Mark.Beckington@doj.ca.gov
Subject: Newanforbi v. California Highway Patrol, No. 26CV191136 — Petitioner's Case Management Statement (Oct. 28 CMC)

Attach:
- {CM110_OUT.name}
- {POS_OUT.name}

---

Ms. Ing:

Attached is Petitioner's Case Management Statement for the October 28, 2026 case management conference, with proof of electronic service. It reflects our October 1 meet and confer.

Thank you,

Brendan Ngwa Nforbi
Plaintiff, In Propria Persona

---
Note to self (do not send this footer):
- File the CM-110 (with attachments) through One Legal first, then send this email the same day so the proof date matches.
- If filing or service slips past {EXEC_DATE}, change EXEC_DATE in the script and regenerate; the form date, signature date, and proof date must match the actual day.
- Hard deadline: October 13, 2026 (rule 3.725, 15 calendar days before the CMC).
- Do not attach the combined "with POS" packet in place of the two files.
- Confirm before filing: no amended petition on the Fourth Cause of Action was filed (Attachment 18, item 3; Item 4a).
"""


def main() -> None:
    if not BLANK.is_file():
        build_blank(SOURCE_JUNE30, BLANK)
    att = OUT_DIR / "_cm110_attachments_tmp.pdf"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_att = build_attachments(att)
    form = OUT_DIR / "_cm110_form_tmp.pdf"
    fill_form(BLANK, form, n_att)
    out = pymupdf.open(form)
    out.insert_pdf(pymupdf.open(att))
    out.save(CM110_OUT, garbage=3, deflate=True)
    build_pos(POS_OUT)
    pk = pymupdf.open(CM110_OUT)
    pk.insert_pdf(pymupdf.open(POS_OUT))
    pk.save(PACKET_OUT, garbage=3, deflate=True)
    EMAIL_OUT.write_text(EMAIL)
    att.unlink()
    form.unlink()
    print(f"Wrote {CM110_OUT.relative_to(REPO_ROOT)} ({5 + n_att} pp)")
    print(f"Wrote {POS_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote {PACKET_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote {EMAIL_OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
