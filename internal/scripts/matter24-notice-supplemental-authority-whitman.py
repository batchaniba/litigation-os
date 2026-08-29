#!/usr/bin/env python3
"""Matter 24 — Notice of Supplemental Authority on the Whitman tentative.

The Serrato opposition was original-filed August 27, 2026, the day before
the Alameda demurrer hearing. This notice lodges Judge Whitman's written
tentative (August 27, for the August 28 hearing) with Magistrate Judge
Krishnan. It does not treat the tentative as the minute order.

Dkt. 21 (Aug. 28) reset the MTD hearing to September 30, 2026, 1:30 p.m.
Execution date for this packet: August 31, 2026.

  python3 internal/scripts/matter24-notice-supplemental-authority-whitman.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
EXEC_DATE = "August 31, 2026"
HEARING_DATE = "September 30, 2026"
SERVICE_PLACE = "San Jose, California"

MATTER24 = ROOT / "public/documents/matter-24"
TENTATIVE = (
    ROOT
    / "public/documents/matter-32/from-20"
    / "Tentative Ruling - CHP Demurrer (Dept 25 Whitman, Aug 27 2026 for Aug 28 hearing).pdf"
)
OUT_NOTICE = MATTER24 / (
    "Notice of Supplemental Authority - Whitman Tentative - Serrato MTD (Aug 31 2026).pdf"
)
OUT_COVER = MATTER24 / (
    "Exhibit A Cover - Whitman Tentative Ruling (Aug 27 2026).pdf"
)
OUT_POS = MATTER24 / (
    "Proof of Service by Email - Notice of Supplemental Authority Whitman (Aug 31 2026).pdf"
)
OUT_PACKET = MATTER24 / (
    "Notice of Supplemental Authority - Whitman Tentative with POS (Aug 31 2026).pdf"
)

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


def _sign_block(d: PleadingPaper) -> None:
    d.ensure_space(7)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.blank_line()
    d.write_line("___________________________________")
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")


def _stamp_sig(path: Path) -> None:
    doc = fitz.open(str(path))
    line = None
    page = None
    for candidate in doc:
        hits = candidate.search_for("_______________________________")
        if hits:
            page = candidate
            line = hits[-1]
            break
    if page is None or line is None:
        doc.close()
        raise RuntimeError(f"No signature line found in {path}")
    width = 135.0
    height = width * SIGNATURE_ASPECT
    y1 = line.y1 - 2.0
    y0 = y1 - height
    rect = fitz.Rect(line.x0, y0, line.x0 + width, y1)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)
    tmp = path.with_name(path.stem + ".signed.pdf")
    doc.save(tmp, garbage=4, deflate=True, incremental=False)
    doc.close()
    tmp.replace(path)


def build_notice(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(
        str(path),
        doc_title_footer="NOTICE OF SUPPLEMENTAL AUTHORITY -- NEWANFORBI v. SERRATO",
    )
    _header(d)
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("CAPTAIN G. SERRATO, in his", True, False),
        ("individual and official capacities", True, False),
        ("as Commander, Dublin Area,", True, False),
        ("California Highway Patrol,", True, False),
        ("", False, False),
        ("                          Defendant.", False, False),
    ]
    right = [
        ("Case No. 4:26-cv-05953-ASK", False, False),
        ("", False, False),
        ("NOTICE OF SUPPLEMENTAL", True, False),
        ("AUTHORITY", True, False),
        ("[Civil L.R. 7-3]", True, False),
        ("", False, False),
        (f"Date: {HEARING_DATE}", False, False),
        ("Time: 1:30 p.m.", False, False),
        ("Ctrm: Oakland 4, 3rd Floor", False, False),
        ("Judge: Hon. Ajay S. Krishnan", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("NOTICE OF SUPPLEMENTAL AUTHORITY", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "TO THE COURT AND TO DEFENDANT AND HIS ATTORNEY OF RECORD:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngehsi Newanforbi, appearing in propria persona, "
        "submits this Notice of Supplemental Authority in connection with "
        "Defendant's Motion to Dismiss the First Amended Complaint and/or "
        f"Motion to Strike (hearing reset by Clerk's Notice, Dkt. 21, to "
        f"{HEARING_DATE}, 1:30 p.m., Oakland Courtroom 4). Plaintiff's "
        "opposition was original-filed August 27, 2026, the day before the "
        "state-court hearing described below.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "On August 27, 2026, the Honorable Jenna M. Whitman, Department 25 of "
        "the Alameda County Superior Court, issued a written tentative ruling "
        "on Respondents' demurrer to the Petition for Writ of Mandate in "
        "Newanforbi v. California Highway Patrol et al., No. 26CV191136 — the "
        "state-law mandate proceeding on the same April 20, 2026 U-visa "
        "certification denial that is the subject of this action. The demurrer "
        "was heard August 28, 2026. A copy of the written tentative is attached "
        "as Exhibit A.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "The tentative overrules the demurrer as to the first cause of action "
        "(ministerial duty under Penal Code section 679.10; the qualifying-crime "
        "/ probable-cause dispute is factual and cannot be resolved on demurrer) "
        "and the fourth cause of action (declaratory relief). It sustains "
        "without leave the second and third causes of action.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "The minute order has not yet entered. Plaintiff does not ask this Court "
        "to treat the attached tentative as a final state-court judgment. "
        "Plaintiff files this notice so the Court has the written ruling that "
        "was before the parties at the August 28 hearing, and will lodge the "
        "minute order when it is in hand.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "This Notice does not amend the opposition and contains no further "
        "argument. See Civil L.R. 7-3.",
        first_indent=0,
    )
    _sign_block(d)
    d.save()
    _stamp_sig(path)


def build_exhibit_cover(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    page_w, page_h = letter
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Times-Bold", 14)
    c.drawCentredString(page_w / 2, page_h / 2 + 40, "EXHIBIT A")
    c.setFont("Times-Roman", 12)
    lines = [
        "Tentative Ruling",
        "Hon. Jenna M. Whitman, Department 25",
        "Alameda County Superior Court",
        "Newanforbi v. California Highway Patrol et al.",
        "No. 26CV191136",
        "Issued August 27, 2026, for the August 28, 2026 demurrer hearing",
        "Minute order not yet entered — do not treat as the final order",
    ]
    y = page_h / 2 + 10
    for line in lines:
        c.drawCentredString(page_w / 2, y, line)
        y -= 18
    c.save()


def build_email_pos(path: Path) -> None:
    """Match the August 27 opposition email POS (Li / Montufar layout)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    page_w, page_h = letter
    left = 72.0
    width = page_w - 144.0
    fs = 11.0
    lh = 15.0
    c = canvas.Canvas(str(path), pagesize=letter)
    y = page_h - 72.0

    def wrap(text: str) -> None:
        nonlocal y
        c.setFont("Times-Roman", fs)
        words = text.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if c.stringWidth(trial, "Times-Roman", fs) <= width:
                line = trial
            else:
                c.drawString(left, y, line)
                y -= lh
                line = word
        if line:
            c.drawString(left, y, line)
            y -= lh

    c.setFont("Times-Bold", 13)
    c.drawCentredString(page_w / 2, y, "DECLARATION OF SERVICE BY E-MAIL")
    y -= lh * 2.0

    c.setFont("Times-Bold", fs)
    c.drawString(left, y, "Case Name:")
    c.setFont("Times-Roman", fs)
    c.drawString(left + 95, y, "Brendan N. Newanforbi v. Captain G. Serrato, et al.")
    y -= lh * 1.2

    c.setFont("Times-Bold", fs)
    c.drawString(left, y, "Case Number:")
    c.setFont("Times-Roman", fs)
    c.drawString(left + 95, y, "4:26-cv-05953-ASK")
    y -= lh * 1.2

    c.setFont("Times-Bold", fs)
    c.drawString(left, y, "Party Represented:")
    c.setFont("Times-Roman", fs)
    c.drawString(left + 115, y, "Plaintiff Brendan Ngehsi Newanforbi, In Pro Per")
    y -= lh * 1.8

    c.setFont("Times-Bold", 12)
    c.drawString(left, y, "Declaration of Electronic Service")
    y -= lh * 1.6

    for para in (
        "1. I am over the age of eighteen years. I am the Plaintiff in this action, "
        "appearing in propria persona.",
        "2. My mailing address is 1455 Cat Tail Drive, Stockton, CA 95204, County of "
        "San Joaquin. My telephone number is (209) 801-4442.",
        "3. My electronic service address is bnn.cdl@gmail.com.",
        f"4. On {EXEC_DATE}, I electronically served the following document[s]:",
    ):
        wrap(para)
        y -= lh * 0.35

    y -= lh * 0.3
    for line in (
        "a. NOTICE OF SUPPLEMENTAL AUTHORITY, with Exhibit A",
        "   (Tentative Ruling of Hon. Jenna M. Whitman, Dept. 25,",
        "   Alameda Superior Court, issued August 27, 2026, for the",
        "   August 28, 2026 demurrer hearing in No. 26CV191136);",
    ):
        c.setFont("Times-Roman", fs)
        c.drawString(left + 24, y, line)
        y -= lh
    y -= lh * 0.5

    wrap(
        "5. I electronically served the aforementioned document[s] by emailing them to "
        "the following individual[s]:",
    )
    y -= lh * 0.6
    for line in (
        "Haiyang A. Li",
        "Deputy Attorney General",
        "Office of the Attorney General",
        "300 South Spring Street, Suite 1702",
        "Los Angeles, CA 90013-1230",
        "E-mail Address: Haiyang.Li@doj.ca.gov",
        "Attorneys for Defendant Captain G. Serrato",
    ):
        c.setFont("Times-Roman", fs)
        c.drawString(left + 12, y, line)
        y -= lh

    y -= lh * 1.2
    wrap(
        "I declare under penalty of perjury under the laws of the State of California "
        "and the United States of America that the foregoing is true and correct, and "
        f"that this declaration was executed on {EXEC_DATE}, at {SERVICE_PLACE}."
    )

    y -= lh * 2.0
    sig_w = 160.0
    sig_h = sig_w * SIGNATURE_ASPECT
    line_w = 220.0
    right = page_w - 72.0
    sig_x = right - line_w
    line_y = y - 8
    if Path(SIGNATURE_PATH).is_file():
        img_x = sig_x + (line_w - sig_w) / 2.0
        c.drawImage(
            SIGNATURE_PATH,
            img_x,
            line_y + 4,
            width=sig_w,
            height=sig_h,
            mask="auto",
            preserveAspectRatio=True,
        )
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.8)
    c.line(sig_x, line_y, sig_x + line_w, line_y)
    c.setFont("Times-Roman", 9)
    c.drawCentredString(sig_x + line_w / 2, line_y - 14, "Signature")
    c.setFont("Times-Bold", fs)
    c.drawString(left, line_y - 4, "Brendan Ngehsi Newanforbi")
    c.setFont("Times-Roman", fs)
    c.drawString(left, line_y - 4 - lh, "Declarant / Plaintiff, In Pro Per")
    c.save()


def main() -> None:
    if not TENTATIVE.is_file():
        raise SystemExit(f"Missing tentative: {TENTATIVE}")
    build_notice(OUT_NOTICE)
    build_exhibit_cover(OUT_COVER)
    build_email_pos(OUT_POS)
    pages = assemble([OUT_NOTICE, OUT_COVER, TENTATIVE, OUT_POS], OUT_PACKET)
    print(f"Wrote {OUT_NOTICE}")
    print(f"Wrote {OUT_COVER}")
    print(f"Wrote {OUT_POS}")
    print(f"Wrote {OUT_PACKET} ({pages} pages)")


if __name__ == "__main__":
    main()
