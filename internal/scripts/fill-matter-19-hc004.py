#!/usr/bin/env python3
"""Fill Matter 19 HC-004 Notice and Request for Ruling; assemble filing packet.

Packet order:
  1. HC-004 (filled, signed)
  2. Exhibit A cover (Matter-12 default-packet style)
  3. Unstamped Petition for Writ of Habeas Corpus (67 pp)

Execution / notice date: August 17, 2026.
Petition filing date: April 3, 2026 (Case No. C2604791).
Address of record on this form: 1455 Cat Tail Drive, Stockton, CA 95204.
"""

from __future__ import annotations

import sys
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from exhibit_cover import write_exhibit_cover  # noqa: E402
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "internal/public/documents/_form-library/hc004-blank-template.pdf"
OUT_DIR = ROOT / "internal/public/documents/matter-19"
PETITION = OUT_DIR / "Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf"

HC004_OUT = OUT_DIR / (
    "HC-004 Notice and Request for Ruling "
    "(Habeas Corpus, Executed Aug 17 2026).pdf"
)
COVER_OUT = OUT_DIR / (
    "Exhibit A Cover — Petition for Writ of Habeas Corpus "
    "(HC-004 Attachment).pdf"
)
PACKET_OUT = OUT_DIR / (
    "HC-004 Notice and Request for Ruling Packet "
    "(with Exhibit A — Unstamped Petition) (Ready to File Aug 17 2026).pdf"
)

# Party / caption
NAME = "Brendan Ngehsi Newanforbi"
STREET = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
ATTY_FOR = "Petitioner in pro per"
COUNTY = "SANTA CLARA"
COUNTY_SHORT = "Santa Clara"
CASE_NUMBER = "C2604791"
DOB = "09/16/1996"
CDC_NO = "BF3571"
PETITION_FILE_DATE = "April 3, 2026"
SIG_DATE = "August 17, 2026"

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


# Every caption-block field is drawn directly as static page content instead
# of going through the AcroForm fill pipeline. pypdf's default appearance
# stream for a filled text field clips descenders (g/j/p/q/y) at the box's
# bottom edge once flattened -- neither calling widget.update() (regenerates
# through PyMuPDF's own layout engine) nor a smaller font size closed that out
# reliably. Drawing the text ourselves sidesteps the appearance-stream
# pipeline for these fields entirely, the same way the exhibit cover's text
# -- never routed through a form field -- never had this problem.
HARDCODED_VALUES = {
    "name": NAME,
    "street": STREET,
    "city": CITY,
    "state": STATE,
    "zip": ZIP,
    "phone": PHONE,
    "email": EMAIL,
    "atty_for": ATTY_FOR,
    "county": COUNTY,
    "in_re": NAME,
    "def_name": NAME,
    "dob": DOB,
}
HARDCODED_FIELD_NAMES = {F[key]: value for key, value in HARDCODED_VALUES.items()}

# Helvetica AFM metrics (nearly identical to the template's ArialMT at this
# scale) -- used to hand-place the baseline so a full ascender-to-descender
# line fits inside the field's own box with margin on both sides, verified
# against rendered pixels rather than assumed.
HC_FONT = "helv"
HC_FONT_SIZE = 8.67
_ASCENT_RATIO = 0.718
_DESCENT_RATIO = 0.207
_LEFT_PAD = 2.0
# Bias the slack toward the bottom margin: descenders were the actual
# clipping failure mode observed, ascenders/cap-height never clipped.
_TOP_BIAS = 0.35


def fields() -> dict[str, str]:
    return {
        F["case"]: CASE_NUMBER,
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
            continue
        if name in HARDCODED_FIELD_NAMES:
            rect = widget.rect
            page.delete_widget(widget)
            slack = rect.height - (_ASCENT_RATIO + _DESCENT_RATIO) * HC_FONT_SIZE
            top_margin = slack * _TOP_BIAS
            baseline_y = rect.y0 + top_margin + _ASCENT_RATIO * HC_FONT_SIZE
            page.insert_text(
                (rect.x0 + _LEFT_PAD, baseline_y),
                HARDCODED_FIELD_NAMES[name],
                fontname=HC_FONT,
                fontsize=HC_FONT_SIZE,
                color=(0, 0, 0),
            )
            continue
        # The remaining text fields (CaseNumber, CDCNo, petName/petCounty/
        # petFileDate, sigDate, sigName) sit in taller boxes and were never
        # part of the descender-clipping bug; still route them through
        # widget.update() (PyMuPDF's own layout engine) rather than trusting
        # pypdf's default appearance stream, for consistency.
        if widget.field_type_string == "Text":
            widget.update()
    doc.bake()
    tmp = out.with_suffix(".baked.pdf")
    doc.save(str(tmp), deflate=True, garbage=4)
    doc.close()
    tmp.replace(out)


def build_exhibit_cover(out: Path) -> None:
    """Diamond default-packet exhibit cover (portfolio house style)."""
    write_exhibit_cover(
        out,
        court="SANTA CLARA COUNTY SUPERIOR COURT",
        caption="IN RE NEWANFORBI (CDC BF3571) v. DODD ET AL.",
        case_no=f"Case No. {CASE_NUMBER}",
        exhibit="A",
        title="Petition for Writ of Habeas Corpus",
        details=[
            "Filed April 3, 2026 | Santa Clara Superior Court",
            "Immediate Discharge from Parole Requested",
            "(Cal. Penal Code § 1473 et seq.)",
        ],
        footer=(
            "Notice and Request for Ruling (HC-004) — "
            f"Case No. {CASE_NUMBER}"
        ),
    )


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
