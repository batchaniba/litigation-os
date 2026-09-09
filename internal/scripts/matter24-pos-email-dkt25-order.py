#!/usr/bin/env python3
"""Matter 24 - Declaration of Service by E-mail for the Dkt. 25 signed order.

Same house form as matter24-opposition-pos-email.py: Plaintiff serving by
e-mail on counsel of record. Documents served are Plaintiff's transmittal
correspondence and the Order entered September 9, 2026 (Dkt. 25).
"""
from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
MATTER24 = ROOT / "public/documents/matter-24"
OUT_MATTER = MATTER24 / "Proof of Service by Email - Dkt 25 Order Continuing Initial CMC (Sep 9 2026).pdf"

PAGE_W, PAGE_H = letter
LEFT = 72.0
RIGHT = PAGE_W - 72.0
WIDTH = RIGHT - LEFT
TOP = PAGE_H - 72.0
FS = 11.0
LH = 15.0

CASE_NAME = "Brendan N. Newanforbi v. Captain G. Serrato, et al."
CASE_NUMBER = "4:26-cv-05953-ASK"
SERVICE_DATE = "September 9, 2026"
EXECUTION_PLACE = "San Jose, California"
STAMP_SIGNATURE = True

DOC_LINES = [
    "a. PLAINTIFF'S CORRESPONDENCE TO DEPUTY ATTORNEY",
    "   GENERAL HAIYANG A. LI REGARDING THE ORDER",
    "   ENTERED SEPTEMBER 9, 2026 (DKT. 25) CONTINUING",
    "   THE INITIAL CASE MANAGEMENT CONFERENCE; and",
    "",
    "b. JOINT STIPULATION TO CONTINUE INITIAL CASE",
    "   MANAGEMENT CONFERENCE BASED UPON DELAY IN",
    "   SERVICE OF DEFENDANT AND PENDING MOTION TO",
    "   DISMISS, AND ORDER (Dkt. 25, signed and entered",
    "   September 9, 2026)",
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
    line = ""
    for w in text.split():
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

    for label, value, off in (
        ("Case Name:", CASE_NAME, 95),
        ("Case Number:", CASE_NUMBER, 95),
        ("Party Represented:", "Plaintiff Brendan Ngehsi Newanforbi, In Pro Per", 115),
    ):
        c.setFont("Times-Bold", FS)
        c.drawString(LEFT, y, label)
        c.setFont("Times-Roman", FS)
        c.drawString(LEFT + off, y, value)
        y -= LH * 1.2
    y -= LH * 0.6

    c.setFont("Times-Bold", 12)
    c.drawString(LEFT, y, "Declaration of Electronic Service")
    y -= LH * 1.6

    for p in [
        "1. I am over the age of eighteen years. I am the Plaintiff in this action, "
        "appearing in propria persona.",
        "2. My mailing address is 1455 Cat Tail Drive, Stockton, CA 95204, County of "
        "San Joaquin. My telephone number is (209) 801-4442.",
        "3. My electronic service address is bnn.cdl@gmail.com.",
        f"4. On {SERVICE_DATE}, I electronically served the following document[s]:",
    ]:
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
        LEFT, y, WIDTH,
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
        LEFT, y, WIDTH,
    )
    y -= LH * 2.0

    sig_w = 160.0
    sig_h = sig_w * SIGNATURE_ASPECT
    line_w = 220.0
    sig_x = RIGHT - line_w
    line_y = y - 8

    if STAMP_SIGNATURE and Path(SIGNATURE_PATH).is_file():
        c.drawImage(SIGNATURE_PATH, sig_x + (line_w - sig_w) / 2.0, line_y + 4,
                    width=sig_w, height=sig_h, mask="auto", preserveAspectRatio=True)

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
    c.drawRightString(RIGHT, 42, "Proof of Service by E-mail - Dkt. 25 Order")

    c.save()
    print(f"Wrote {path} ({path.stat().st_size} bytes)")


def main() -> None:
    if STAMP_SIGNATURE and not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    build(OUT_MATTER)


if __name__ == "__main__":
    main()
