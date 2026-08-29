"""Portfolio exhibit cover page — Diamond default-packet style.

Canonical house style for every Exhibit A/B/1/… separator sheet. Geometry
copied from Matter 12 Diamond / Alpine default-judgment packets
(black header band, outer border, giant exhibit mark, rule, gray footer).

Usage::

    from exhibit_cover import write_exhibit_cover

    write_exhibit_cover(
        path,
        court="UNITED STATES DISTRICT COURT",
        caption="NEWANFORBI v. SERRATO",
        case_no="Case No. 4:26-cv-05953-ASK",
        exhibit="A",
        title="Tentative Ruling",
        details=[
            "Hon. Jenna M. Whitman, Department 25",
            "Alameda County Superior Court — No. 26CV191136",
        ],
        footer="Notice of Supplemental Authority — Newanforbi v. Serrato",
    )

Optional second court line (e.g. \"NORTHERN DISTRICT OF CALIFORNIA\") goes in
``court_line2``. Prefer this helper over hand-rolled centered Times covers.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas

GRAY = Color(0.5, 0.5, 0.5)

# Letter page, Matter-12 geometry (reportlab bottom-origin).
PAGE_W = 612.0
PAGE_H = 792.0
MARGIN = 36.0
CONTENT_W = PAGE_W - 2 * MARGIN  # 540
BORDER_H = PAGE_H - 2 * MARGIN  # 720
HEADER_BOTTOM = 692.0  # top-origin y=100 → 792-100
HEADER_H = 64.0  # top-origin band y=36..100
RULE_Y = 340.0  # top-origin y=452
RULE_X0 = 108.0
RULE_X1 = 504.0


def _center(
    c: canvas.Canvas,
    text: str,
    y: float,
    font: str,
    size: float,
    color=black,
) -> None:
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(PAGE_W / 2.0, y, text)


def write_exhibit_cover(
    path: Path | str,
    *,
    court: str,
    caption: str,
    case_no: str,
    exhibit: str,
    title: str,
    details: list[str] | None = None,
    footer: str | None = None,
    court_line2: str | None = None,
) -> Path:
    """Write a one-page exhibit cover PDF. Returns ``path``."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    details = list(details or [])
    mark = str(exhibit).strip() or "A"

    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))

    # Outer border (1 pt) and black header band.
    c.setStrokeColor(black)
    c.setLineWidth(1.0)
    c.rect(MARGIN, MARGIN, CONTENT_W, BORDER_H, stroke=1, fill=0)

    c.setFillColor(black)
    c.rect(MARGIN, HEADER_BOTTOM, CONTENT_W, HEADER_H, stroke=0, fill=1)

    # Header text — white, centered. One or two court lines + caption + case.
    if court_line2:
        _center(c, court, 742, "Helvetica-Bold", 8, white)
        _center(c, court_line2, 730, "Helvetica-Bold", 8, white)
        _center(c, caption, 716, "Helvetica", 8, white)
        _center(c, case_no, 704, "Helvetica", 8, white)
    else:
        _center(c, court, 738, "Helvetica-Bold", 9, white)
        _center(c, caption, 723, "Helvetica", 8, white)
        _center(c, case_no, 710, "Helvetica", 8, white)

    # EXHIBIT above giant mark — Diamond uses 18 pt label + 160 pt mark.
    _center(c, "EXHIBIT", 530, "Helvetica", 18, black)
    _center(c, mark, 370, "Helvetica-Bold", 160, black)

    # Rule above description.
    c.setStrokeColor(black)
    c.setLineWidth(0.75)
    c.line(RULE_X0, RULE_Y, RULE_X1, RULE_Y)

    _center(c, title, 318, "Helvetica-Bold", 13, black)
    y = 298.0
    for line in details:
        _center(c, line, y, "Helvetica", 10, black)
        y -= 15.0

    if footer:
        _center(c, footer, 52, "Helvetica", 7.5, GRAY)

    c.save()
    return path
