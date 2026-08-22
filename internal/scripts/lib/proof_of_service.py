"""Portfolio-wide federal Proof of Service PDF generator.

Canonical blank: ``internal/public/documents/_form-library/proof-of-service-blank-template.pdf``

Adapted from the E.D. Cal. clerk sample (Barocio Dkt. 5-2 last page) with the
CM/ECF stamp and Local Rule 135 intro removed and the border raised to where
that intro began. Default court line is Northern District of California;
override ``district_line`` for E.D. Cal. or other districts.

This is the de facto Rule 5 Proof of Service form for all federal matters in
the portfolio going forward. Import ``build_proof_of_service`` /
``ProofOfServiceFields`` from matter scripts rather than hand-rolling
pleading-paper certificates.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

REPO_INTERNAL = Path(__file__).resolve().parents[2]
FORM_LIBRARY = REPO_INTERNAL / "public/documents/_form-library"
BLANK_TEMPLATE_PATH = FORM_LIBRARY / "proof-of-service-blank-template.pdf"
# Kept as a same-content alias during transition from the ndcal-prefixed name.
BLANK_TEMPLATE_ALIAS_PATH = FORM_LIBRARY / "ndcal-proof-of-service-blank-template.pdf"

PAGE_W, PAGE_H = letter  # 612 x 792

BORDER_L = 44.0
BORDER_R = 568.0
# Top edge sits below the page head; bottom edge sits near the page foot.
BORDER_T = 80.0
BORDER_B = 770.0

FS = 10.0
LEADING = 14.0
INNER_L = 60.0
INNER_R = 552.0
CAPTION_RIGHT_X = 330.0

DISTRICT_NDCAL = "NORTHERN DISTRICT OF CALIFORNIA"
DISTRICT_EDCAL = "EASTERN DISTRICT OF CALIFORNIA"


@dataclass
class ProofOfServiceFields:
    """Fillable fields. Leave strings empty for blank-template underlines."""

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
    district_line: str = DISTRICT_NDCAL


def _hline(c: canvas.Canvas, x0: float, x1: float, y: float, width: float = 0.7) -> None:
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(width)
    c.line(x0, y, x1, y)


def _draw_border(c: canvas.Canvas) -> None:
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.9)
    c.rect(
        BORDER_L,
        PAGE_H - BORDER_B,
        BORDER_R - BORDER_L,
        BORDER_B - BORDER_T,
        stroke=1,
        fill=0,
    )


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


def build_proof_of_service(path: Path | str, fields: ProofOfServiceFields) -> Path:
    """Write one Proof of Service PDF. Returns the output path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    _draw_border(c)

    y = PAGE_H - BORDER_T - 44

    _center(c, "UNITED STATES DISTRICT COURT", y, "Times-Roman", FS)
    y -= LEADING
    _center(c, fields.district_line or DISTRICT_NDCAL, y, "Times-Roman", FS)
    y -= LEADING * 2.2

    caption_top = y
    left_x = INNER_L
    left_w = CAPTION_RIGHT_X - left_x - 12

    c.setFont("Times-Roman", FS)
    plaintiff = fields.plaintiff_line or "(Case Title)"
    c.drawString(left_x, y, plaintiff)
    _hline(c, left_x, left_x + left_w, y - 2)
    y -= LEADING + 2
    c.setFont("Times-Roman", FS)
    role_w = c.stringWidth(fields.plaintiff_role, "Times-Roman", FS)
    c.drawString(left_x + (left_w - role_w) / 2.0, y, fields.plaintiff_role)
    y -= LEADING + 4

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

    def_lines = fields.defendant_lines or [""]
    for line in def_lines:
        c.setFont("Times-Roman", FS)
        if line:
            c.drawString(left_x, y, line)
        _hline(c, left_x, left_x + left_w, y - 2)
        y -= LEADING + 1

    c.setFont("Times-Roman", FS)
    role_w = c.stringWidth(fields.defendant_role, "Times-Roman", FS)
    c.drawString(left_x + (left_w - role_w) / 2.0, y, fields.defendant_role)

    c.setFont("Times-Bold", FS)
    c.drawString(CAPTION_RIGHT_X, y + LEADING, fields.title)

    y -= LEADING + 6
    c.setFont("Times-Roman", FS)
    mid = (BORDER_L + BORDER_R) / 2.0
    c.drawCentredString(mid - 40, y, "/")
    _hline(c, left_x, left_x + 40, y - 1)
    y -= LEADING * 2.4

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
        for _ in range(6):
            _hline(c, INNER_L + 12, INNER_R - 12, y)
            y -= LEADING * 1.35

    # Footer: declaration, then clear air for the signature stamp, then the line.
    sig_width = 140.0
    sig_height = sig_width * SIGNATURE_ASPECT  # ~35 pt
    gap_decl_to_sig = 40.0  # keep cursive loops clear of the declaration line
    name_below = 16.0
    footer_pad = 32.0  # clearance from typed name down to the bottom border
    footer_block = (
        FS  # declaration
        + gap_decl_to_sig
        + sig_height
        + 4.0  # line sits just under the stamp
        + name_below
        + footer_pad
    )
    border_bottom_y = PAGE_H - BORDER_B
    decl_y = border_bottom_y + footer_block - FS
    # If body content ran low, keep a gap under the last body line.
    min_decl_from_body = y - 32
    if min_decl_from_body < decl_y:
        decl_y = min_decl_from_body

    c.setFont("Times-Roman", FS)
    c.drawString(
        INNER_L,
        decl_y,
        "I declare under penalty of perjury that the foregoing is true and correct.",
    )

    # Signature image sits fully below the declaration; the line is under the image.
    sig_line_y = decl_y - gap_decl_to_sig - sig_height
    sig_x0 = INNER_L + 160
    sig_x1 = INNER_R - 40
    _hline(c, sig_x0, sig_x1, sig_line_y)

    name = fields.server_name or "(Name of Person Completing Service)"
    c.setFont("Times-Roman" if fields.server_name else "Times-Italic", FS)
    nw = c.stringWidth(name, c._fontname, FS)
    c.drawString(sig_x0 + (sig_x1 - sig_x0 - nw) / 2.0, sig_line_y - name_below, name)

    if fields.stamp_signature and fields.server_name:
        try:
            c.drawImage(
                SIGNATURE_PATH,
                sig_x0 + 10,
                sig_line_y,  # baseline of stamp = signature line
                width=sig_width,
                height=sig_height,
                mask="auto",
                preserveAspectRatio=True,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"warning: could not stamp signature: {exc}", file=sys.stderr)

    c.save()
    return path


def blank_fields(*, district_line: str = DISTRICT_NDCAL) -> ProofOfServiceFields:
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
        district_line=district_line,
    )


def write_blank_template(path: Path | str | None = None) -> Path:
    """Regenerate the portfolio blank Proof of Service template."""
    out = Path(path) if path else BLANK_TEMPLATE_PATH
    build_proof_of_service(out, blank_fields())
    # Keep the older ndcal-prefixed filename in sync as an alias.
    if out.resolve() == BLANK_TEMPLATE_PATH.resolve():
        build_proof_of_service(BLANK_TEMPLATE_ALIAS_PATH, blank_fields())
    return out
