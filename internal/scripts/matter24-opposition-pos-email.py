#!/usr/bin/env python3
"""Matter 24 - Declaration of Service by E-mail for the Serrato Opp.

Modeled on Defendant's Aug. 26, 2026 Declaration of Service by E-mail
(Diana Montufar / Haiyang A. Li), adapted for Plaintiff serving the
Opposition by email to counsel of record.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
OUT_MATTER = (
    ROOT
    / "public/documents/matter-24"
    / "Proof of Service by Email - Opposition to Serrato MTD (Aug 27 2026).pdf"
)
OUT_ROOT = ROOT.parent / "Proof of Service by Email - Opposition to Serrato MTD (Aug 27 2026).pdf"
OUT_ARTIFACT = Path(
    "/opt/cursor/artifacts/serrato_opp_pos_email_20260827.pdf"
)

PAGE_W, PAGE_H = letter
LEFT = 72.0
RIGHT = PAGE_W - 72.0
WIDTH = RIGHT - LEFT
TOP = PAGE_H - 72.0
FS = 11.0
LH = 15.0

CASE_NAME = "Brendan N. Newanforbi v. Captain G. Serrato, et al."
CASE_NUMBER = "4:26-cv-05953-ASK"
SERVICE_DATE = "August 27, 2026"
EXECUTION_PLACE = "San Jose, California"

DOC_LINES = [
    "a. PLAINTIFF'S OPPOSITION TO DEFENDANT CAPTAIN G.",
    "   SERRATO'S NOTICE OF MOTION TO DISMISS PLAINTIFF'S",
    "   FIRST AMENDED COMPLAINT AND/OR MOTION TO STRIKE",
    "   PORTIONS OF THE FIRST AMENDED COMPLAINT;",
    "   MEMORANDUM OF POINTS AND AUTHORITIES",
]

RECIPIENT_LINES = [
    "Haiyang A. Li",
    "Deputy Attorney General",
    "Office of the Attorney General",
    "300 South Spring Street, Suite 1702",
    "Los Angeles, CA 90013-1230",
    "E-mail Address: Haiyang.Li@doj.ca.gov",
    "Attorneys for Defendant Captain G. Serrato",
]


def _wrap(c: canvas.Canvas, text: str, x: float, y: float, max_w: float, font="Times-Roman", size=FS) -> float:
    c.setFont(font, size)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            line = trial
        else:
            c.drawString(x, y, line)
            y -= LH
            line = w
    if line:
        c.drawString(x, y, line)
        y -= LH
    return y


def build(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    y = TOP

    c.setFont("Times-Bold", 13)
    c.drawCentredString(PAGE_W / 2, y, "DECLARATION OF SERVICE BY E-MAIL")
    y -= LH * 2.0

    # Case header block (mirror AG POS layout)
    c.setFont("Times-Bold", FS)
    c.drawString(LEFT, y, "Case Name:")
    c.setFont("Times-Roman", FS)
    c.drawString(LEFT + 95, y, CASE_NAME)
    y -= LH * 1.2

    c.setFont("Times-Bold", FS)
    c.drawString(LEFT, y, "Case Number:")
    c.setFont("Times-Roman", FS)
    c.drawString(LEFT + 95, y, CASE_NUMBER)
    y -= LH * 1.2

    c.setFont("Times-Bold", FS)
    c.drawString(LEFT, y, "Party Represented:")
    c.setFont("Times-Roman", FS)
    c.drawString(LEFT + 115, y, "Plaintiff Brendan Ngehsi Newanforbi, In Pro Per")
    y -= LH * 1.8

    c.setFont("Times-Bold", 12)
    c.drawString(LEFT, y, "Declaration of Electronic Service")
    y -= LH * 1.6

    paras = [
        "1. I am over the age of eighteen years. I am the Plaintiff in this action, "
        "appearing in propria persona.",
        "2. My mailing address is 1455 Cat Tail Drive, Stockton, CA 95204, County of "
        "San Joaquin. My telephone number is (209) 801-4442.",
        "3. My electronic service address is bnn.cdl@gmail.com.",
        f"4. On {SERVICE_DATE}, I electronically served the following document[s]:",
    ]
    for p in paras:
        y = _wrap(c, p, LEFT, y, WIDTH)
        y -= LH * 0.35

    y -= LH * 0.3
    for line in DOC_LINES:
        c.setFont("Times-Roman", FS)
        c.drawString(LEFT + 24, y, line)
        y -= LH
    y -= LH * 0.5

    y = _wrap(
        c,
        "5. I electronically served the aforementioned document[s] by emailing them to "
        "the following individual[s]:",
        LEFT,
        y,
        WIDTH,
    )
    y -= LH * 0.6

    for line in RECIPIENT_LINES:
        c.setFont("Times-Roman", FS)
        c.drawString(LEFT + 12, y, line)
        y -= LH

    y -= LH * 1.2
    y = _wrap(
        c,
        "I declare under penalty of perjury under the laws of the State of California "
        "and the United States of America that the foregoing is true and correct, and "
        f"that this declaration was executed on {SERVICE_DATE}, at {EXECUTION_PLACE}.",
        LEFT,
        y,
        WIDTH,
    )

    y -= LH * 2.0

    # Signature block - stamp over a signature line
    sig_w = 160.0
    sig_h = sig_w * SIGNATURE_ASPECT
    line_w = 220.0
    sig_x = RIGHT - line_w
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

    c.setFont("Times-Bold", FS)
    c.drawString(LEFT, line_y - 4, "Brendan Ngehsi Newanforbi")
    c.setFont("Times-Roman", FS)
    c.drawString(LEFT, line_y - 4 - LH, "Declarant / Plaintiff, In Pro Per")

    c.setFont("Times-Roman", 8)
    c.drawString(LEFT, 42, "Matter 24 - N.D. Cal. 4:26-cv-05953-ASK")
    c.drawRightString(RIGHT, 42, "Proof of Service by E-mail - Opposition to MTD")

    c.save()
    print(f"Wrote {path} ({path.stat().st_size} bytes)")


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    for out in (OUT_MATTER, OUT_ROOT, OUT_ARTIFACT):
        build(out)


if __name__ == "__main__":
    main()
