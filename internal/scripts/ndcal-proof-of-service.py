#!/usr/bin/env python3
"""N.D. Cal. Proof of Service form (adapted from E.D. Cal. clerk sample).

Visual model: last page of Barocio Dkt. 5-2 sample Proof of Service
(Case 2:26-cv-00191-DJC-CSK), with:

  - no CM/ECF blue case stamp
  - the Local Rule 135 instructional paragraph removed
  - outer border beginning where that paragraph began
  - court line changed to NORTHERN DISTRICT OF CALIFORNIA

Generates:
  - blank template in _form-library/
  - filled Meza (Dkt. 5 ? Melano) and Candelaria (Dkt. 6 ? both) POS PDFs
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
FORM_LIB = ROOT / "public/documents/_form-library"
OUT_BLANK = FORM_LIB / "ndcal-proof-of-service-blank-template.pdf"
OUT_MEZA = (
    ROOT
    / "public/documents/matter-32/ndcal"
    / "Proof of Service - FAC Dkt 05 Mailed to Melano (Aug 21 2026).pdf"
)
OUT_CAND = (
    ROOT
    / "public/documents/matter-33/ndcal"
    / "Proof of Service - FAC Dkt 06 Mailed to Candelaria and Gordon (Aug 21 2026).pdf"
)

# Legacy pleading-paper certificates this form replaces.
LEGACY_MEZA = (
    ROOT
    / "public/documents/matter-32/ndcal"
    / "Certificate of Service - FAC Dkt 05 Mailed to Melano (Aug 21 2026).pdf"
)
LEGACY_CAND = (
    ROOT
    / "public/documents/matter-33/ndcal"
    / "Certificate of Service - FAC Dkt 06 Mailed to Candelaria and Gordon (Aug 21 2026).pdf"
)

PAGE_W, PAGE_H = letter  # 612 x 792

# Border begins where the deleted "The following is a sample..." line sat
# on the E.D. Cal. sample (~y 48-124 above the old inner box).
BORDER_L = 44.0
BORDER_R = 568.0
BORDER_T = 48.0
BORDER_B = 720.0

FS = 10.0
LEADING = 14.0
INNER_L = 60.0
INNER_R = 552.0
CAPTION_RIGHT_X = 330.0


@dataclass
class ProofOfServiceFields:
    """Blank placeholders when a field is None / empty list."""

    plaintiff_line: str = "(Case Title)"
    plaintiff_role: str = "Plaintiff or Petitioner"
    defendant_lines: list[str] = field(default_factory=list)
    defendant_role: str = "Defendant or Respondent"
    case_number: str = ""
    case_number_hint: str = "(case number)"
    title: str = "PROOF OF SERVICE"
    service_date: str = ""
    document_title: str = ""
    mailing_location: str = ""
    recipients: list[str] = field(default_factory=list)
    server_name: str = ""
    stamp_signature: bool = False


def _hline(c: canvas.Canvas, x0: float, x1: float, y: float, width: float = 0.7) -> None:
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(width)
    c.line(x0, y, x1, y)


def _draw_border(c: canvas.Canvas) -> None:
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.9)
    c.rect(BORDER_L, PAGE_H - BORDER_B, BORDER_R - BORDER_L, BORDER_B - BORDER_T, stroke=1, fill=0)


def _center(c: canvas.Canvas, text: str, y: float, font: str = "Times-Roman", size: float = FS) -> None:
    c.setFont(font, size)
    c.drawCentredString((BORDER_L + BORDER_R) / 2.0, y, text)


def _fill_or_blank_line(
    c: canvas.Canvas,
    y: float,
    prefix: str,
    value: str,
    italic_hint: str,
    suffix: str,
    x0: float = INNER_L,
    x1: float = INNER_R,
) -> None:
    """Draw 'prefix ____hint____ suffix' or 'prefix value suffix' with underline."""
    c.setFont("Times-Roman", FS)
    c.drawString(x0, y, prefix)
    pref_w = c.stringWidth(prefix, "Times-Roman", FS)
    suf_w = c.stringWidth(suffix, "Times-Roman", FS) if suffix else 0.0

    if value:
        val_w = c.stringWidth(value, "Times-Roman", FS)
        c.drawString(x0 + pref_w, y, value)
        _hline(c, x0 + pref_w - 1, x0 + pref_w + val_w + 1, y - 2)
        if suffix:
            c.drawString(x0 + pref_w + val_w, y, suffix)
    else:
        avail = max(80.0, x1 - x0 - pref_w - suf_w - 4)
        _hline(c, x0 + pref_w, x0 + pref_w + avail, y - 2)
        if italic_hint:
            c.setFont("Times-Italic", FS)
            hw = c.stringWidth(italic_hint, "Times-Italic", FS)
            c.drawString(x0 + pref_w + max(0.0, (avail - hw) / 2.0), y, italic_hint)
        if suffix:
            c.setFont("Times-Roman", FS)
            c.drawString(x0 + pref_w + avail + 2, y, suffix)


def build_proof_of_service(path: Path, fields: ProofOfServiceFields) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    _draw_border(c)

    # PDF y increases upward; work in top-down coordinates.
    y = PAGE_H - BORDER_T - 28

    _center(c, "UNITED STATES DISTRICT COURT", y, "Times-Roman", FS)
    y -= LEADING
    _center(c, "NORTHERN DISTRICT OF CALIFORNIA", y, "Times-Roman", FS)
    y -= LEADING * 2.2

    # Caption: left party block + right case number / title
    caption_top = y
    left_x = INNER_L
    left_w = CAPTION_RIGHT_X - left_x - 12

    # Plaintiff line + underline
    c.setFont("Times-Roman", FS)
    plaintiff = fields.plaintiff_line or "(Case Title)"
    c.drawString(left_x, y, plaintiff)
    _hline(c, left_x, left_x + left_w, y - 2)
    y -= LEADING + 2
    c.setFont("Times-Roman", FS)
    role_w = c.stringWidth(fields.plaintiff_role, "Times-Roman", FS)
    c.drawString(left_x + (left_w - role_w) / 2.0, y, fields.plaintiff_role)
    y -= LEADING + 4

    # V. on left; case number on right (aligned to caption top band)
    c.setFont("Times-Roman", FS)
    c.drawString(left_x, y, "V.")

    right_y = caption_top
    c.setFont("Times-Roman", FS)
    if fields.case_number:
        c.drawString(CAPTION_RIGHT_X, right_y, f"Case Number: {fields.case_number}")
    else:
        c.drawString(CAPTION_RIGHT_X, right_y, "Case Number: ____________________")
        if fields.case_number_hint:
            c.setFont("Times-Italic", 8.5)
            c.drawString(CAPTION_RIGHT_X, right_y - 11, fields.case_number_hint)

    y -= LEADING * 2.0

    # Defendant lines
    def_lines = fields.defendant_lines or [""]
    for i, line in enumerate(def_lines):
        c.setFont("Times-Roman", FS)
        if line:
            c.drawString(left_x, y, line)
        _hline(c, left_x, left_x + left_w, y - 2)
        y -= LEADING + 1

    c.setFont("Times-Roman", FS)
    role_w = c.stringWidth(fields.defendant_role, "Times-Roman", FS)
    c.drawString(left_x + (left_w - role_w) / 2.0, y, fields.defendant_role)

    # Document title on the right, opposite defendant block
    c.setFont("Times-Bold", FS)
    c.drawString(CAPTION_RIGHT_X, y + LEADING, fields.title)

    y -= LEADING + 6
    # Closing slash / rule under caption (ED Cal sample convention)
    c.setFont("Times-Roman", FS)
    mid = (BORDER_L + BORDER_R) / 2.0
    c.drawCentredString(mid - 40, y, "/")
    _hline(c, left_x, left_x + 40, y - 1)
    y -= LEADING * 2.4

    # Body
    _fill_or_blank_line(
        c,
        y,
        "    I hereby certify that on ",
        fields.service_date,
        "(Date)",
        ", I served a copy of the attached",
    )
    y -= LEADING * 1.8

    _fill_or_blank_line(
        c,
        y,
        "",
        fields.document_title,
        "(Title of Document Served and Filed)",
        ",",
    )
    y -= LEADING * 1.8

    c.setFont("Times-Roman", FS)
    c.drawString(
        INNER_L,
        y,
        "by placing a copy in a postage paid envelope addressed to the person(s) hereinafter listed, by depositing said",
    )
    y -= LEADING * 1.8

    _fill_or_blank_line(
        c,
        y,
        "envelope in the United States Mail at ",
        fields.mailing_location,
        "(Location of Mailing)",
        ":",
    )
    y -= LEADING * 1.8

    c.setFont("Times-Bold", FS)
    c.drawString(
        INNER_L,
        y,
        "(List Name and Address of Each Defendant or Attorney Served)",
    )
    y -= LEADING * 1.4

    if fields.recipients:
        c.setFont("Times-Roman", FS)
        for line in fields.recipients:
            if not line:
                y -= LEADING * 0.7
                continue
            c.drawString(INNER_L + 12, y, line)
            y -= LEADING
    else:
        # Blank address lines for the template
        for _ in range(6):
            _hline(c, INNER_L + 12, INNER_R - 12, y)
            y -= LEADING * 1.35

    # Push declaration toward bottom of the box
    decl_y = PAGE_H - BORDER_B + 78
    if y < decl_y + 40:
        decl_y = y - 36

    c.setFont("Times-Roman", FS)
    c.drawString(
        INNER_L,
        decl_y,
        "I declare under penalty of perjury that the foregoing is true and correct.",
    )

    sig_y = decl_y - 36
    sig_x0 = INNER_L + 160
    sig_x1 = INNER_R - 40
    _hline(c, sig_x0, sig_x1, sig_y)

    name = fields.server_name or "(Name of Person Completing Service)"
    c.setFont("Times-Roman" if fields.server_name else "Times-Italic", FS)
    nw = c.stringWidth(name, c._fontname, FS)
    c.drawString(sig_x0 + (sig_x1 - sig_x0 - nw) / 2.0, sig_y - 14, name)

    if fields.stamp_signature and fields.server_name:
        # Affix signature just above the signature line.
        try:
            width = 150
            height = width * SIGNATURE_ASPECT
            c.drawImage(
                SIGNATURE_PATH,
                sig_x0 + 10,
                sig_y + 2,
                width=width,
                height=height,
                mask="auto",
                preserveAspectRatio=True,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"warning: could not stamp signature: {exc}", file=sys.stderr)

    c.save()
    print(f"Wrote {path}")


def blank_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="(Case Title)",
        defendant_lines=[""],
        case_number="",
        title="PROOF OF SERVICE",
        service_date="",
        document_title="",
        mailing_location="",
        recipients=[],
        server_name="",
        stamp_signature=False,
    )


def meza_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGWA NFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "SANTIAGO MEZA-GONZALEZ;",
            "JOSE MELANO; and DOES 1-10",
        ],
        defendant_role="Defendants",
        case_number="3:26-cv-08271-PHK",
        title="PROOF OF SERVICE",
        service_date="August 21, 2026",
        document_title="First Amended Complaint for Damages (Dkt. 5)",
        mailing_location="San Jose, California",
        recipients=[
            "Officer Jose Melano (CHP Badge #023054)",
            "California Highway Patrol, South Sacramento Area",
            "6 Massie Court",
            "Sacramento, CA 95823",
            "",
            "(No Rule 5 mailing to Defendant Santiago Meza-Gonzalez --",
            "process under Fed. R. Civ. P. 4 has not been completed.)",
        ],
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
    )


def candelaria_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGWA NFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "DIANA CANDELARIA, individually;",
            "STEVE GORDON, officially; and DOES 1-10",
        ],
        defendant_role="Defendants",
        case_number="3:26-cv-08272-LJC",
        title="PROOF OF SERVICE",
        service_date="August 21, 2026",
        document_title="First Amended Complaint for Damages and Injunctive Relief (Dkt. 6)",
        mailing_location="San Jose, California",
        recipients=[
            "Diana Candelaria, Driver Safety Hearing Officer",
            "California Department of Motor Vehicles",
            "Legal Affairs Division, Mail Station C128",
            "2415 First Avenue",
            "Sacramento, CA 95818",
            "",
            "Steve Gordon, Director",
            "California Department of Motor Vehicles",
            "Legal Affairs Division, Mail Station C128",
            "2415 First Avenue",
            "Sacramento, CA 95818",
        ],
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
    )


def main() -> None:
    build_proof_of_service(OUT_BLANK, blank_fields())
    build_proof_of_service(OUT_MEZA, meza_fields())
    build_proof_of_service(OUT_CAND, candelaria_fields())
    for legacy in (LEGACY_MEZA, LEGACY_CAND):
        if legacy.exists():
            legacy.unlink()
            print(f"Removed legacy {legacy.name}")


if __name__ == "__main__":
    main()
