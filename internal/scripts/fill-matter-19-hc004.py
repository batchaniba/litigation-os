#!/usr/bin/env python3
"""Fill Matter 19 HC-004 Notice and Request for Ruling; assemble filing packet.

Packet order:
  1. HC-004 (filled, signed)
  2. Exhibit A cover (Matter-12 default-packet style)
  3. Unstamped Petition for Writ of Habeas Corpus (67 pp)

Execution / notice date: August 7, 2026.
Petition filing date: April 3, 2026 (Case No. C2604791).
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "internal/public/documents/_form-library/hc004-blank-template.pdf"
OUT_DIR = ROOT / "internal/public/documents/matter-19"
PETITION = OUT_DIR / "Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf"

HC004_OUT = OUT_DIR / (
    "HC-004 Notice and Request for Ruling "
    "(Habeas Corpus, Executed Aug 7 2026).pdf"
)
COVER_OUT = OUT_DIR / (
    "Exhibit A Cover — Petition for Writ of Habeas Corpus "
    "(HC-004 Attachment).pdf"
)
PACKET_OUT = OUT_DIR / (
    "HC-004 Notice and Request for Ruling Packet "
    "(with Exhibit A — Unstamped Petition) (Ready to File Aug 7 2026).pdf"
)

# Party / caption
NAME = "Brendan Ngehsi Newanforbi"
NAME_CAPS = "BRENDAN NGEHSI NEWANFORBI"
STREET = "1090 S Milpitas Blvd, Unit #304"
CITY = "Milpitas"
STATE = "CA"
ZIP = "95035"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
ATTY_FOR = "Petitioner in pro per"
COUNTY = "SANTA CLARA"
COUNTY_SHORT = "Santa Clara"
CASE_NUMBER = "C2604791"
DOB = "09/16/1996"
CDC_NO = "BF3571"
PETITION_FILE_DATE = "April 3, 2026"
SIG_DATE = "August 7, 2026"

# pypdf field names (XFA-style hierarchy on Judicial Council HC-004)
F = {
    "case": (
        "HC-004[0].Page1[0].p1Caption[0].captionSub[0]"
        ".CaseNumber[0].CaseNumber[0]"
    ),
    "name": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].AttyName[0]",
    "street": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].AttyStreet[0]",
    "city": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].AttyCity[0]",
    "state": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].AttyState[0]",
    "zip": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].AttyZip[0]",
    "phone": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].Phone[0]",
    "email": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].Email[0]",
    "atty_for": "HC-004[0].Page1[0].p1Caption[0].AttyInfo[0].AttyFor[0]",
    "county": "HC-004[0].Page1[0].p1Caption[0].CourtInfo[0].CrtCounty[0]",
    "in_re": "HC-004[0].Page1[0].p1Caption[0].TitlePartyName[0].fl100129[0]",
    "def_name": "HC-004[0].Page1[0].p1Caption[0].TitlePartyName[0].defName[0]",
    "dob": "HC-004[0].Page1[0].p1Caption[0].TitlePartyName[0].defDOB[0]",
    "cdc": "HC-004[0].Page1[0].p1Caption[0].TitlePartyName[0].CDCNo[0]",
    "pet_name": "HC-004[0].Page1[0].petName[0]",
    "pet_county": "HC-004[0].Page1[0].petCounty[0]",
    "pet_file": "HC-004[0].Page1[0].petFIleDate[0]",
    "sig_date": "HC-004[0].Page1[0].sigDate[0]",
    "sig_name": "HC-004[0].Page1[0].sigName[0]",
}

# Signature line on HC-004 (PyMuPDF top-origin coords).
SIG_X0 = 360.0
SIG_X1 = 540.0
SIG_Y_LINE = 556.3

GRAY = Color(0.5, 0.5, 0.5)


def fields() -> dict[str, str]:
    return {
        F["case"]: CASE_NUMBER,
        F["name"]: NAME_CAPS,
        F["street"]: STREET,
        F["city"]: CITY,
        F["state"]: STATE,
        F["zip"]: ZIP,
        F["phone"]: PHONE,
        F["email"]: EMAIL,
        F["atty_for"]: ATTY_FOR,
        F["county"]: COUNTY,
        F["in_re"]: NAME_CAPS,
        F["def_name"]: NAME_CAPS,
        F["dob"]: DOB,
        F["cdc"]: CDC_NO,
        F["pet_name"]: NAME,
        F["pet_county"]: COUNTY_SHORT,
        F["pet_file"]: PETITION_FILE_DATE,
        F["sig_date"]: SIG_DATE,
        F["sig_name"]: NAME,
    }


def fill_hc004(out: Path) -> None:
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, fields())
    try:
        writer.set_need_appearances_writer(True)
    except Exception:
        pass
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)

    # Stamp pen signature, drop Print/Save/Clear chrome, bake field appearances.
    doc = fitz.open(str(out))
    page = doc[0]
    width = SIG_X1 - SIG_X0
    height = width * SIGNATURE_ASPECT
    rect = fitz.Rect(SIG_X0, SIG_Y_LINE - height, SIG_X1, SIG_Y_LINE)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)
    for widget in list(page.widgets() or []):
        name = widget.field_name or ""
        if name.endswith(".Print[0]") or name.endswith(".Save[0]") or name.endswith(
            ".Reset[0]"
        ):
            page.delete_widget(widget)
    doc.bake()
    tmp = out.with_suffix(".baked.pdf")
    doc.save(str(tmp), deflate=True, garbage=4)
    doc.close()
    tmp.replace(out)


def _center(c: canvas.Canvas, text: str, y: float, font: str, size: float, color=black) -> None:
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(306, y, text)


def build_exhibit_cover(out: Path) -> None:
    """Matter-12 default-packet exhibit cover style (black header bar, giant letter)."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(612, 792))

    # Outer border (1 pt) and black header band — match Matter 12 geometry.
    c.setStrokeColor(black)
    c.setLineWidth(1.0)
    c.rect(36, 36, 540, 720, stroke=1, fill=0)

    c.setFillColor(black)
    c.rect(36, 692, 540, 64, stroke=0, fill=1)  # y=792-100=692 … 792-36=756 → height 64
    # Matter 12: header band Rect(36, 36, 576, 100) in top-origin → bottom-origin:
    # top 36 → y=756; bottom 100 → y=692; height=64. Yes.

    _center(c, "SANTA CLARA COUNTY SUPERIOR COURT", 738, "Helvetica-Bold", 9, white)
    _center(
        c,
        "IN RE NEWANFORBI (CDC BF3571) v. DODD ET AL.",
        723,
        "Helvetica",
        8,
        white,
    )
    _center(c, f"Case No. {CASE_NUMBER}", 710, "Helvetica", 8, white)

    # EXHIBIT above giant letter — keep number clear of the description rule.
    _center(c, "EXHIBIT", 530, "Helvetica", 18, black)
    _center(c, "A", 370, "Helvetica-Bold", 130, black)

    # Rule above description (Matter 12: y_top 452 → bottom-origin 340)
    c.setStrokeColor(black)
    c.setLineWidth(0.75)
    c.line(108, 340, 504, 340)

    _center(c, "Petition for Writ of Habeas Corpus", 318, "Helvetica-Bold", 13, black)
    _center(
        c,
        "Filed April 3, 2026 | Santa Clara Superior Court",
        298,
        "Helvetica",
        10,
        black,
    )
    _center(c, "Immediate Discharge from Parole Requested", 283, "Helvetica", 10, black)
    _center(c, "(Cal. Penal Code § 1473 et seq.)", 268, "Helvetica", 10, black)

    _center(
        c,
        "Notice and Request for Ruling (HC-004) — Case No. C2604791",
        52,
        "Helvetica",
        7.5,
        GRAY,
    )

    c.save()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(buf.getvalue())


def assemble_packet(hc004: Path, cover: Path, petition: Path, out: Path) -> int:
    writer = PdfWriter()
    for path in (hc004, cover, petition):
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    return len(writer.pages)


def main() -> None:
    for required in (TEMPLATE, PETITION, Path(SIGNATURE_PATH)):
        if not required.exists():
            raise SystemExit(f"Missing required file: {required}")

    fill_hc004(HC004_OUT)
    print(f"HC-004 → {HC004_OUT.name}")

    build_exhibit_cover(COVER_OUT)
    print(f"Exhibit cover → {COVER_OUT.name}")

    total = assemble_packet(HC004_OUT, COVER_OUT, PETITION, PACKET_OUT)
    print(f"Packet → {PACKET_OUT.name} ({total} pages)")


if __name__ == "__main__":
    main()
