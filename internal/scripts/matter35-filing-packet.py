#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 35 -- Santa Clara filing packet (CM-010, SUM-100, blank CV-5012).

Generates the companion Judicial Council / local forms for e-filing the
Verified Complaint (v9) in Santa Clara Superior Court (Downtown).

    python3 internal/scripts/matter35-filing-packet.py

Outputs (matter-35/):
  - CM-010 Civil Case Cover Sheet - Ngwa Nforbi v Ross Stores (Aug 26 2026).pdf
  - SUM-100 Summons - Ngwa Nforbi v Ross Stores (Aug 26 2026).pdf
  - CV-5012 Civil Lawsuit Notice (blank for clerk) - Aug 26 2026.pdf
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal/public/documents/matter-35"
FORMS = ROOT / "internal/public/documents/_form-library"

# Prefer the official Judicial Council download when present; fall back to the
# fillable CM-010 already in the portfolio (Matter 29).
CM010_SRC_CANDIDATES = [
    Path("/tmp/forms/cm010.pdf"),
    FORMS / "cm010-blank-template.pdf",
    ROOT
    / "internal/public/documents/matter-29/CM010 Newanforbi v Amazon.pdf",
]
SUM100_SRC = FORMS / "sum100-blank-template.pdf"
CV5012_SRC_CANDIDATES = [
    Path("/tmp/forms/cv-5012.pdf"),
    FORMS / "cv-5012-blank-template.pdf",
]

EXEC_DATE = "August 26, 2026"

PLAINTIFF_PRINT = "Brendan Ngwa Nforbi"
PLAINTIFF_CAPS = "BRENDAN NGWA NFORBI"
CASE_NAME = "Ngwa Nforbi v. Ross Stores, Inc., et al."

DEFENDANTS_NOTICE = (
    "ROSS STORES, INC., a Delaware corporation; "
    "ROSS DRESS FOR LESS, INC., a Virginia corporation; "
    "DOE 1; and DOES 2 through 20, inclusive"
)

COURT_COUNTY = "Santa Clara"
COURT_STREET = "191 North First Street"
COURT_MAIL = "191 North First Street"
COURT_CITYZIP = "San Jose, CA 95113"
COURT_BRANCH = "Downtown Superior Court"
COURT_BLOCK = (
    "Superior Court of California, County of Santa Clara\n"
    "Downtown Superior Court\n"
    "191 North First Street\n"
    "San Jose, CA 95113"
)

STREET = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
ATTY_FOR = "Plaintiff, In Propria Persona"

PLAINTIFF_INFO_LINE = (
    f"{PLAINTIFF_CAPS}, In Propria Persona; "
    f"{STREET}, {CITY}, {STATE} {ZIP}; {PHONE}; {EMAIL}"
)


def _first_existing(paths: list[Path]) -> Path:
    for p in paths:
        if p.is_file():
            return p
    raise FileNotFoundError(
        "None of these sources exist:\n  " + "\n  ".join(str(p) for p in paths)
    )


def _fill_pypdf(src: Path, out: Path, fields: dict[str, str]) -> None:
    reader = PdfReader(str(src))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, fields)
    try:
        writer.set_need_appearances_writer(True)
    except Exception:
        pass
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)


def _stamp_signature(path: Path, page_index: int, x0: float, x1: float, y_line: float) -> None:
    doc = fitz.open(str(path))
    page = doc[page_index]
    width = x1 - x0
    height = width * SIGNATURE_ASPECT
    rect = fitz.Rect(x0, y_line - height, x1, y_line)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)
    doc.saveIncr()
    doc.close()


def build_cm010(out: Path) -> None:
    src = _first_existing(CM010_SRC_CANDIDATES)
    # Cache a blank into the form library for future runs.
    lib = FORMS / "cm010-blank-template.pdf"
    if not lib.exists() and src.name == "cm010.pdf":
        shutil.copy2(src, lib)

    P = "CM-010[0].Page1[0]"
    P2 = "CM-010[0].Page2[0]"
    fields = {
        f"{P}.P1Caption[0].AttyPartyInfo[0].Name[0]": PLAINTIFF_PRINT,
        f"{P}.P1Caption[0].AttyPartyInfo[0].Street[0]": STREET,
        f"{P}.P1Caption[0].AttyPartyInfo[0].City[0]": CITY,
        f"{P}.P1Caption[0].AttyPartyInfo[0].State[0]": STATE,
        f"{P}.P1Caption[0].AttyPartyInfo[0].Zip[0]": ZIP,
        f"{P}.P1Caption[0].AttyPartyInfo[0].Phone[0]": PHONE,
        f"{P}.P1Caption[0].AttyPartyInfo[0].Email[0]": EMAIL,
        f"{P}.P1Caption[0].AttyPartyInfo[0].AttyFor[0]": ATTY_FOR,
        f"{P}.P1Caption[0].CourtInfo[0].CrtCounty[0]": COURT_COUNTY,
        f"{P}.P1Caption[0].CourtInfo[0].CrtStreet[0]": COURT_STREET,
        f"{P}.P1Caption[0].CourtInfo[0].CrtMailingAdd[0]": COURT_MAIL,
        f"{P}.P1Caption[0].CourtInfo[0].CrtCityZip[0]": COURT_CITYZIP,
        f"{P}.P1Caption[0].CourtInfo[0].CrtBranch[0]": COURT_BRANCH,
        f"{P}.P1Caption[0].TitlePartyName[0].Party1[0]": CASE_NAME,
        # Unlimited (amount demanded exceeds $35,000)
        f"{P}.P1Caption[0].FormTitle[0].Civil[0].limited1[0]": "/1",
        f"{P}.P1Caption[0].FormTitle[0].Civil[0].limited1[1]": "/Off",
        # Case type: Civil rights (08) -- Item1Check[7]
        f"{P}.List1[0].Item1Check[7]": "/8",
        # Item 2 -- not complex
        f"{P2}.List2[0].is1[0]": "/Off",
        f"{P2}.List2[0].is1[1]": "/2",
        # Item 3 -- monetary, injunctive, punitive (DOE 1)
        f"{P2}.List3[0].Item3[0].Lia[0].Ch1[0]": "/1",
        f"{P2}.List3[0].Item3[0].Lib[0].Ch2[0]": "/1",
        f"{P2}.List3[0].Item3[0].Lic[0].Ch3[0]": "/1",
        # Item 4 -- three causes of action
        f"{P2}.List4[0].FillText1[0]": "3",
        # Item 5 -- not a class action
        f"{P2}.List5[0].is[0]": "/Off",
        f"{P2}.List5[0].is[1]": "/2",
        f"{P2}.SigDate[0]": EXEC_DATE,
        f"{P2}.SigName[0]": PLAINTIFF_PRINT,
    }
    _fill_pypdf(src, out, fields)
    # Force widget appearances (XFA checkboxes sometimes need an explicit update).
    doc = fitz.open(str(out))
    page = doc[1]
    for w in page.widgets() or []:
        name = w.field_name or ""
        if name.endswith("Ch1[0]") or name.endswith("Ch2[0]") or name.endswith("Ch3[0]"):
            w.field_value = w.on_state()
            w.update()
        elif name.endswith("is1[1]") or name.endswith("is[1]"):
            w.field_value = w.on_state()
            w.update()
    doc.saveIncr()
    doc.close()
    # Signature sits on the "Signature of party..." line (page 2 ~ y 318).
    _stamp_signature(out, 1, 300, 530, 318)
    print(f"Wrote {out}")


def build_sum100(out: Path) -> None:
    """Fill SUM-100 cleanly: native fields; no content-area whiteouts."""
    src = SUM100_SRC
    if not src.is_file():
        src = _first_existing([Path("/tmp/forms/sum100.pdf"), SUM100_SRC])

    P = "SUM-100[0].Page1[0]"
    defendants_lines = (
        "ROSS STORES, INC., a Delaware corporation; ROSS DRESS FOR LESS, INC.,\n"
        "a Virginia corporation; DOE 1; and DOES 2 through 20, inclusive"
    )
    court_line1 = "Superior Court of California,"
    court_lines_2_3 = (
        "County of Santa Clara -- Downtown\n"
        "191 North First Street, San Jose, CA 95113"
    )
    # Slightly taller than the native field so County + 191 each get a full line,
    # still above the attorney-info label (~ y 524). No whiteout.
    court_addr_rect = fitz.Rect(36.1, 502.5, 362.0, 523.0)

    fields = {
        f"{P}.Notice[0].FillText25[0]": defendants_lines,
        f"{P}.Notice[0].FillText180[0]": PLAINTIFF_CAPS,
        f"{P}.Info[0].FillText3[0]": court_line1,
        # Drawn into the native address rect below (empty field avoids double ink).
        f"{P}.Info[0].FillText2[0]": "",
        f"{P}.Info[0].CaseNumber[0].FillText26[0]": "",
        f"{P}.Info[0].FillText30[0]": PLAINTIFF_INFO_LINE,
        f"{P}.Info[0].Sign1[0].FillText34[0]": "",
    }
    _fill_pypdf(src, out, fields)

    doc = fitz.open(str(out))
    page = doc[0]

    for w in page.widgets() or []:
        name = w.field_name or ""
        if name.endswith("FillText25[0]"):
            w.field_flags = int(w.field_flags) | (1 << 12)
            w.text_fontsize = 7.5
            w.field_value = defendants_lines
            w.update()
        elif name.endswith("FillText180[0]"):
            w.field_value = PLAINTIFF_CAPS
            w.update()
        elif name.endswith("FillText3[0]"):
            w.text_fontsize = 8
            w.field_value = court_line1
            w.update()
        elif name.endswith("FillText2[0]"):
            w.field_value = ""
            w.update()
        elif name.endswith("FillText30[0]"):
            w.text_fontsize = 7
            w.field_value = PLAINTIFF_INFO_LINE
            w.update()

    # Two compact lines inside the native address field only (no whiteout).
    page.insert_textbox(
        court_addr_rect,
        court_lines_2_3,
        fontsize=6.5,
        fontname="times-roman",
        align=fitz.TEXT_ALIGN_LEFT,
        color=(0, 0, 0),
    )

    for w in list(page.widgets() or []):
        name = w.field_name or ""
        if "Footer" in name or "CourtLink" in name:
            page.delete_widget(w)
    # Mask Print/Save/Clear chrome only (below form content).
    page.draw_rect(
        fitz.Rect(36.0, 762.0, 576.0, 792.0),
        color=(1, 1, 1),
        fill=(1, 1, 1),
        width=0,
    )

    doc.saveIncr()
    doc.close()
    print(f"Wrote {out}")


def build_cv5012(out: Path) -> None:
    """Copy the blank Santa Clara CV-5012 for the clerk to issue (local rule)."""
    src = _first_existing(CV5012_SRC_CANDIDATES)
    lib = FORMS / "cv-5012-blank-template.pdf"
    if not lib.exists():
        shutil.copy2(src, lib)
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, out)
    print(f"Wrote {out} (blank for clerk issuance)")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_cm010(
        OUT_DIR
        / "CM-010 Civil Case Cover Sheet - Ngwa Nforbi v Ross Stores (Aug 26 2026).pdf"
    )
    build_sum100(
        OUT_DIR / "SUM-100 Summons - Ngwa Nforbi v Ross Stores (Aug 26 2026).pdf"
    )
    build_cv5012(
        OUT_DIR
        / "CV-5012 Civil Lawsuit Notice (blank for clerk) - Aug 26 2026.pdf"
    )


if __name__ == "__main__":
    main()
