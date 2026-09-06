#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""San Joaquin intake packet for Matters 36–39.

CM-010, SUM-100, and FW-001 for each executed complaint. FW-001 copies the
financial answers that produced automatic grants on the July 15, 2026 UPS and
FedEx San Joaquin filings (same 5b / $0-income pattern as the Randstad
FW-001). First Advantage is not a named defendant.

    python3 internal/scripts/matter36-39-san-joaquin-intake.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pymupdf
from pypdf import PdfReader, PdfWriter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DOCS = ROOT / "internal/public/documents"
FORMS = DOCS / "_form-library"

EXEC_DATE = "September 8, 2026"
PLAINTIFF_PRINT = "Brendan Ngwa Nforbi"
PLAINTIFF_CAPS = "BRENDAN NGWA NFORBI"

STREET = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
ATTY_FOR = "Plaintiff, In Propria Persona"

COURT_COUNTY = "San Joaquin"
COURT_STREET = "180 E Weber Avenue"
COURT_MAIL = "180 E Weber Avenue"
COURT_CITYZIP = "Stockton, CA 95202"
COURT_BRANCH = "Stockton Courthouse"

PLAINTIFF_INFO_LINE = (
    f"{PLAINTIFF_CAPS}, In Propria Persona; "
    f"{STREET}, {CITY}, {STATE} {ZIP}; {PHONE}; {EMAIL}"
)

CASES = [
    {
        "number": 36,
        "dir": DOCS / "matter-36",
        "caption": "Brendan Ngwa Nforbi v. AT&T Mobility Services LLC",
        "defendants": (
            "AT&T MOBILITY SERVICES LLC, a Delaware limited liability "
            "company; and DOES 1 through 20, inclusive"
        ),
        "causes": "9",
        "stem": "Ngwa Nforbi v AT&T Mobility Services LLC",
    },
    {
        "number": 37,
        "dir": DOCS / "matter-37",
        "caption": "Brendan Ngwa Nforbi v. Home Depot U.S.A., Inc.",
        "defendants": (
            "HOME DEPOT U.S.A., INC., a Delaware corporation; and "
            "DOES 1 through 20, inclusive"
        ),
        "causes": "3",
        "stem": "Ngwa Nforbi v Home Depot USA Inc",
    },
    {
        "number": 38,
        "dir": DOCS / "matter-38",
        "caption": "Brendan Ngwa Nforbi v. Swift Transportation Co. of Arizona LLC",
        "defendants": (
            "SWIFT TRANSPORTATION CO. OF ARIZONA LLC, a limited liability "
            "company; and DOES 1 through 20, inclusive"
        ),
        "causes": "3",
        "stem": "Ngwa Nforbi v Swift Transportation Co of Arizona LLC",
    },
    {
        "number": 39,
        "dir": DOCS / "matter-39",
        "caption": "Brendan Ngwa Nforbi v. Best Buy Co., Inc.",
        "defendants": (
            "BEST BUY CO., INC., a Minnesota corporation; and "
            "DOES 1 through 20, inclusive"
        ),
        "causes": "3",
        "stem": "Ngwa Nforbi v Best Buy Co Inc",
    },
]


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


def _stamp_signature_on(doc: pymupdf.Document, page_index: int, x0: float, x1: float, y_line: float) -> None:
    page = doc[page_index]
    width = x1 - x0
    height = width * SIGNATURE_ASPECT
    rect = pymupdf.Rect(x0, y_line - height, x1, y_line)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)


def _save_clean(doc: pymupdf.Document, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()
    tmp.replace(path)


def _set_on(widget) -> None:
    on = widget.on_state()
    if on:
        widget.field_value = on
        widget.update()


def build_cm010(case: dict, out: Path) -> None:
    src = FORMS / "cm010-blank-template.pdf"
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
        f"{P}.P1Caption[0].TitlePartyName[0].Party1[0]": case["caption"],
        f"{P}.P1Caption[0].FormTitle[0].Civil[0].limited1[0]": "/1",
        f"{P}.P1Caption[0].FormTitle[0].Civil[0].limited1[1]": "/Off",
        f"{P}.List1[0].Item1Check[14]": "/15",
        f"{P2}.List2[0].is1[0]": "/Off",
        f"{P2}.List2[0].is1[1]": "/2",
        f"{P2}.List3[0].Item3[0].Lia[0].Ch1[0]": "/1",
        f"{P2}.List3[0].Item3[0].Lib[0].Ch2[0]": "/1",
        f"{P2}.List5[0].is[0]": "/Off",
        f"{P2}.List5[0].is[1]": "/2",
        f"{P2}.List4[0].FillText1[0]": case["causes"],
        f"{P2}.SigDate[0]": EXEC_DATE,
        f"{P2}.SigName[0]": PLAINTIFF_PRINT,
    }
    _fill_pypdf(src, out, fields)

    doc = pymupdf.open(str(out))
    page0 = doc[0]
    page1 = doc[1]
    for w in page0.widgets() or []:
        name = w.field_name or ""
        if name.endswith("limited1[0]"):
            _set_on(w)
        elif name.endswith("Item1Check[14]"):
            # Other employment (15)
            _set_on(w)
    for w in page1.widgets() or []:
        name = w.field_name or ""
        if name.endswith("is1[1]") or name.endswith("is[1]"):
            _set_on(w)
        elif name.endswith("Ch1[0]") or name.endswith("Ch2[0]"):
            _set_on(w)
    _stamp_signature_on(doc, 1, 300, 530, 318)
    _save_clean(doc, out)
    print(f"Wrote {out}")


def build_sum100(case: dict, out: Path) -> None:
    src = FORMS / "sum100-blank-template.pdf"
    P = "SUM-100[0].Page1[0]"
    defendants_rect = pymupdf.Rect(168.0, 90.5, 428.0, 141.0)
    court_line1 = "Superior Court of California,"
    court_line2 = "County of San Joaquin -- Stockton"
    court_line3 = "180 E Weber Avenue, Stockton, CA 95202"
    court_x = 192.8
    fields = {
        f"{P}.Notice[0].FillText25[0]": "",
        f"{P}.Notice[0].FillText180[0]": PLAINTIFF_CAPS,
        f"{P}.Info[0].FillText3[0]": court_line1,
        f"{P}.Info[0].FillText2[0]": "",
        f"{P}.Info[0].CaseNumber[0].FillText26[0]": "",
        f"{P}.Info[0].FillText30[0]": PLAINTIFF_INFO_LINE,
        f"{P}.Info[0].Sign1[0].FillText34[0]": "",
    }
    _fill_pypdf(src, out, fields)

    doc = pymupdf.open(str(out))
    page = doc[0]
    for w in page.widgets() or []:
        name = w.field_name or ""
        if name.endswith("FillText25[0]") or name.endswith("FillText2[0]"):
            w.field_value = ""
            w.update()
        elif name.endswith("FillText180[0]"):
            w.field_value = PLAINTIFF_CAPS
            w.update()
        elif name.endswith("FillText3[0]"):
            w.text_fontsize = 8
            w.field_value = court_line1
            w.update()
        elif name.endswith("FillText30[0]"):
            w.text_fontsize = 7
            w.field_value = PLAINTIFF_INFO_LINE
            w.update()

    fontsize = 8.0
    for trial in (8.0, 7.5, 7.0, 6.5):
        probe = pymupdf.open()
        pp = probe.new_page(width=page.rect.width, height=page.rect.height)
        rem = pp.insert_textbox(
            defendants_rect,
            case["defendants"],
            fontsize=trial,
            fontname="helv",
            align=pymupdf.TEXT_ALIGN_LEFT,
        )
        probe.close()
        if rem >= 0:
            fontsize = trial
            break
    page.insert_textbox(
        defendants_rect,
        case["defendants"],
        fontsize=fontsize,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_LEFT,
        color=(0, 0, 0),
    )
    page.insert_text((court_x, 506.0), court_line2, fontsize=8.0, fontname="helv")
    page.insert_text((court_x, 516.0), court_line3, fontsize=8.0, fontname="helv")
    for w in list(page.widgets() or []):
        name = w.field_name or ""
        if "Footer" in name or "CourtLink" in name:
            page.delete_widget(w)
    page.draw_rect(
        pymupdf.Rect(36.0, 762.0, 576.0, 792.0),
        color=(1, 1, 1),
        fill=(1, 1, 1),
        width=0,
    )
    _save_clean(doc, out)
    print(f"Wrote {out}")


def build_fw001(case: dict, out: Path) -> None:
    """Same 5b / $0 answers that produced automatic UPS/FedEx/Randstad grants."""
    src = (
        DOCS
        / "matter-27"
        / "FW-001 Request to Waive Court Fees - Randstad US LLC.pdf"
    )
    shutil.copy2(src, out)
    doc = pymupdf.open(str(out))
    page0 = doc[0]
    page1 = doc[1]
    text_map = {
        "CourtInfo[0]": f"{COURT_COUNTY}\n{COURT_STREET}\n{COURT_CITYZIP}",
        "CaseName[0]": case["caption"],
        "PetitionerName1[0]": PLAINTIFF_PRINT,
        "PetitionerStrAddress[0]": STREET,
        "PetitionerCity[0]": CITY,
        "PetitionerState[0]": STATE,
        "PetitionerZip[0]": ZIP,
        "PetitionerTel[0]": PHONE,
        "SigDate[0]": EXEC_DATE,
        "PetitionerName[0]": PLAINTIFF_PRINT,
        "IncomeSource1[0]": "N/A",
        "IncomeAmount1[0]": "0",
        "IncomeSource2[0]": "N/A",
        "IncomeAmount2[0]": "0",
        "IncomeSource3[0]": "N/A",
        "IncomeAmount3[0]": "0",
        "IncomeSource4[0]": "N/A",
        "IncomeAmount4[0]": "0",
        "TotalIncome[0]": "0",
        "HouseholdIncomeName1[0]": "N/A",
        "HouseholdIncomeAge1[0]": "N/A",
        "HouseholdIncomeRel1[0]": "N/A",
        "HouseholdIncomeAmount1[0]": "0",
        "HouseholdTotalncome[0]": "0",
        "TotalAllIncome[0]": "0",
    }
    for page in (page0, page1):
        for w in page.widgets() or []:
            short = (w.field_name or "").split(".")[-1]
            if short in text_map and w.field_type_string == "Text":
                w.field_value = text_map[short]
                w.update()
            elif short == "WaiveSuperiorCrtFee[0]":
                _set_on(w)
            elif short == "GrossMonthIncomeLess[0]":
                _set_on(w)
    # The Randstad source left a typed "/s/ Brendan Ngehsi Newanforbi"
    # appearance to the right of the printed-name widget. Redact it before
    # stamping the universal signature.
    for page in (page0, page1):
        redacted = False
        for needle in ("/s/ Brendan Ngehsi Newanforbi", "Newanforbi", "Ngehsi"):
            for rect in page.search_for(needle):
                page.add_redact_annot(rect + (-2, -1, 2, 1), fill=(1, 1, 1))
                redacted = True
        if redacted:
            page.apply_redactions()
    _stamp_signature_on(doc, 0, 340, 560, 694)
    _save_clean(doc, out)
    print(f"Wrote {out}")


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    for case in CASES:
        case["dir"].mkdir(parents=True, exist_ok=True)
        stem = case["stem"]
        build_cm010(
            case,
            case["dir"] / f"CM-010 Civil Case Cover Sheet - {stem} (Sep 8 2026).pdf",
        )
        build_sum100(
            case,
            case["dir"] / f"SUM-100 Summons - {stem} (Sep 8 2026).pdf",
        )
        build_fw001(
            case,
            case["dir"] / f"FW-001 Request to Waive Court Fees - {stem} (Sep 8 2026).pdf",
        )


if __name__ == "__main__":
    main()
