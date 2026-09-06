#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""San Joaquin intake packet for Matters 36–39.

CM-010, SUM-100, and FW-001 for each executed complaint. Text is drawn onto
the printed lines (not left to AcroForm appearance streams) so captions stack
inside the case-name boxes and the signature sits on the signature line.
FW-001 still copies the 5b / $0 answers that produced automatic grants on the
July 15, 2026 UPS and FedEx filings. First Advantage is not a named defendant.

    python3 internal/scripts/matter36-39-san-joaquin-intake.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pymupdf

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

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
COURT_CITYZIP = "Stockton, CA 95202"
COURT_BRANCH = "Stockton Courthouse"

CASES = [
    {
        "number": 36,
        "dir": DOCS / "matter-36",
        "caption": "Brendan Ngwa Nforbi v. AT&T Mobility Services LLC",
        "defendants": (
            "AT&T MOBILITY SERVICES LLC, a Delaware limited liability "
            "company; and DOES 1 through 20, inclusive"
        ),
        "defendant_lines": [
            "AT&T MOBILITY SERVICES LLC, a Delaware",
            "limited liability company; and DOES 1–20, inclusive",
        ],
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
        "defendant_lines": [
            "HOME DEPOT U.S.A., INC., a Delaware corporation;",
            "and DOES 1 through 20, inclusive",
        ],
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
        "defendant_lines": [
            "SWIFT TRANSPORTATION CO. OF ARIZONA LLC,",
            "a limited liability company; and DOES 1–20, inclusive",
        ],
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
        "defendant_lines": [
            "BEST BUY CO., INC., a Minnesota corporation;",
            "and DOES 1 through 20, inclusive",
        ],
        "causes": "3",
        "stem": "Ngwa Nforbi v Best Buy Co Inc",
    },
]


def _caption_lines(caption: str) -> list[str]:
    if " v. " in caption:
        left, right = caption.split(" v. ", 1)
        return [left.strip(), f"v. {right.strip()}"]
    return [caption]


def _whiteout(page: pymupdf.Page, rect: pymupdf.Rect) -> None:
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)


def _write_at(
    page: pymupdf.Page, x: float, baseline: float, text: str, fontsize: float
) -> None:
    page.insert_text(
        (x, baseline),
        text,
        fontsize=fontsize,
        fontname="helv",
        color=(0, 0, 0),
    )


def _write_on_line(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    text: str,
    fontsize: float = 8.0,
    *,
    wipe: bool = False,
    baseline_inset: float = 1.5,
    x_inset: float = 0.8,
) -> None:
    """Sit text on the widget's bottom edge (the printed rule)."""
    if not text:
        return
    if wipe:
        _whiteout(page, rect)
    width = pymupdf.get_text_length(text, fontname="helv", fontsize=fontsize)
    max_w = max(rect.width - x_inset - 1.0, 8)
    if width > max_w:
        fontsize = max(6.0, fontsize * (max_w / width))
    baseline = rect.y1 - baseline_inset
    if baseline - fontsize < rect.y0 - 0.4:
        baseline = rect.y0 + fontsize * 0.9
    _write_at(page, rect.x0 + x_inset, baseline, text, fontsize)


def _stamp_on_rule(
    page: pymupdf.Page,
    x0: float,
    y_rule: float,
    width: float = 128.0,
    sink: float = 5.4,
) -> None:
    """Park the visible ink mass on the rule.

    The PNG's lowest 10% is a hairline; the loops start ~15% up. `sink` is
    how far the stamp bottom goes through the rule. Keep it small on CM-010
    so the mark does not collide with the printed label under the line.
    """
    sw, sh = SIGNATURE_NATIVE_PX
    height = width * (sh / sw)
    bottom = y_rule + sink
    rect = pymupdf.Rect(x0, bottom - height, x0 + width, bottom)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=False)


def _write_stack(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    lines: list[str],
    max_fs: float = 8.0,
    min_fs: float = 6.0,
    leading: float | None = None,
    valign: str = "center",
) -> None:
    usable = [ln for ln in lines if ln]
    if not usable:
        return
    fontsize = max_fs
    for trial in (max_fs, 7.5, 7.0, 6.5, min_fs):
        widths = [
            pymupdf.get_text_length(ln, fontname="helv", fontsize=trial)
            for ln in usable
        ]
        if max(widths) <= rect.width - 2.0:
            fontsize = trial
            break
        fontsize = trial
    lead = leading if leading is not None else fontsize + 1.1
    total_h = lead * (len(usable) - 1) + fontsize
    if valign == "top":
        y = rect.y0 + fontsize + 0.3
    else:
        y = rect.y0 + max((rect.height - total_h) / 2, 0.3) + fontsize
    for ln in usable:
        _write_at(page, rect.x0 + 1.0, y, ln, fontsize)
        y += lead


def _widget_map(page: pymupdf.Page) -> dict[str, pymupdf.Rect]:
    found: dict[str, pymupdf.Rect] = {}
    for w in page.widgets() or []:
        name = w.field_name or ""
        found[name.split(".")[-1]] = pymupdf.Rect(w.rect)
    return found


def _drop_text_widgets(page: pymupdf.Page) -> None:
    for w in list(page.widgets() or []):
        if w.field_type_string == "Text":
            page.delete_widget(w)


def _set_on(widget) -> None:
    on = widget.on_state()
    if on:
        widget.field_value = on
        widget.update()


def _save_clean(doc: pymupdf.Document, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()
    tmp.replace(path)


def build_cm010(case: dict, out: Path) -> None:
    src = FORMS / "cm010-blank-template.pdf"
    shutil.copy2(src, out)
    doc = pymupdf.open(str(out))
    page0, page1, page2 = doc[0], doc[1], doc[2]
    fields0 = _widget_map(page0)
    fields1 = _widget_map(page1)

    for w in page0.widgets() or []:
        name = w.field_name or ""
        if name.endswith("limited1[0]") or name.endswith("Item1Check[14]"):
            _set_on(w)
    for w in page1.widgets() or []:
        name = w.field_name or ""
        if name.endswith("is1[1]") or name.endswith("is[1]"):
            _set_on(w)
        elif name.endswith("Ch1[0]") or name.endswith("Ch2[0]"):
            _set_on(w)

    _drop_text_widgets(page0)
    _drop_text_widgets(page1)

    header = {
        "Name[0]": (PLAINTIFF_PRINT, 8.0),
        "Street[0]": (STREET, 8.0),
        "City[0]": (CITY, 8.0),
        "State[0]": (STATE, 8.0),
        "Zip[0]": (ZIP, 8.0),
        "Phone[0]": (PHONE, 8.0),
        "Email[0]": (EMAIL, 8.0),
        "AttyFor[0]": (ATTY_FOR, 8.0),
        "CrtCounty[0]": (COURT_COUNTY, 8.0),
        "CrtStreet[0]": (COURT_STREET, 8.0),
        "CrtMailingAdd[0]": (COURT_STREET, 8.0),
        "CrtCityZip[0]": (COURT_CITYZIP, 8.0),
        "CrtBranch[0]": (COURT_BRANCH, 8.0),
    }
    for key, (text, fs) in header.items():
        if key in fields0:
            _write_on_line(
                page0, fields0[key], text, fontsize=fs, baseline_inset=2.8, x_inset=2.6
            )

    # CASE NAME cell is y≈201–226. Stack to the right of the label, centered
    # in the box so both lines sit cleanly with padding above and below.
    caption = _caption_lines(case["caption"])
    case_rect = pymupdf.Rect(90.0, 202.6, 393.0, 224.6)
    _whiteout(page0, case_rect)
    _write_stack(
        page0,
        case_rect,
        caption,
        max_fs=7.0,
        min_fs=6.2,
        leading=8.0,
        valign="center",
    )

    if "FillText1[0]" in fields1:
        _write_on_line(page1, fields1["FillText1[0]"], case["causes"], fontsize=9.0)
    if "SigDate[0]" in fields1:
        _write_on_line(page1, fields1["SigDate[0]"], EXEC_DATE, fontsize=8.0, baseline_inset=2.0)
    if "SigName[0]" in fields1:
        # Keep the typed name left of "Type or print name" (starts ~x=118).
        name_rect = pymupdf.Rect(
            fields1["SigName[0]"].x0,
            fields1["SigName[0]"].y0,
            min(fields1["SigName[0]"].x1, 116.0),
            fields1["SigName[0]"].y1,
        )
        _write_on_line(page1, name_rect, PLAINTIFF_PRINT, fontsize=7.5, baseline_inset=3.4)

    # Cover the printed sign-here pointer; it reads as a black triangle.
    _whiteout(page1, pymupdf.Rect(328.8, 305.2, 340.0, 324.2))
    # Signature rule is y=320.4.
    _stamp_on_rule(page1, 358.0, 320.4, 128.0, sink=5.4)

    # Adobe Print/Save/Clear chrome on page 3 is not part of the filed form.
    _whiteout(page2, pymupdf.Rect(0.0, 756.0, 612.0, 792.0))

    _save_clean(doc, out)
    print(f"Wrote {out}")


def build_sum100(case: dict, out: Path) -> None:
    src = FORMS / "sum100-blank-template.pdf"
    shutil.copy2(src, out)
    doc = pymupdf.open(str(out))
    page = doc[0]
    fields = _widget_map(page)

    _drop_text_widgets(page)
    for w in list(page.widgets() or []):
        name = w.field_name or ""
        if "Footer" in name or "CourtLink" in name:
            page.delete_widget(w)

    # Official FillText25 is y=118.4–140.3; NOTICE Spanish ends at 116.9.
    # Inset from the top so the stack does not kiss the header.
    defendant_rect = pymupdf.Rect(36.0, 126.8, 431.3, 139.8)
    _whiteout(page, fields.get("FillText25[0]", pymupdf.Rect(36.0, 118.4, 431.3, 140.3)))
    _write_stack(page, defendant_rect, case["defendant_lines"], max_fs=8.0, min_fs=6.5)

    plaintiff_rect = fields.get("FillText180[0]", pymupdf.Rect(36.0, 170.4, 431.3, 191.9))
    _write_on_line(page, plaintiff_rect, PLAINTIFF_CAPS, fontsize=10.0, baseline_inset=3.2)

    court_rect = pymupdf.Rect(192.0, 487.4, 360.0, 518.6)
    _whiteout(page, court_rect)
    _write_stack(
        page,
        court_rect,
        [
            "Superior Court of California",
            "County of San Joaquin",
            "180 E Weber Avenue, Stockton, CA 95202",
        ],
        max_fs=7.5,
        min_fs=6.5,
    )

    # Official FillText30 is only y=546.4–557.4. DATE: (Fecha) starts at 559.3.
    info_rect = pymupdf.Rect(36.0, 546.4, 575.4, 557.4)
    _whiteout(page, info_rect)
    _write_on_line(
        page,
        info_rect,
        (
            f"{PLAINTIFF_CAPS}, {STREET}, {CITY}, {STATE} {ZIP}   "
            f"{PHONE}   {EMAIL}"
        ),
        fontsize=6.6,
        baseline_inset=4.0,
    )

    _whiteout(page, pymupdf.Rect(36.0, 762.0, 576.0, 792.0))
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
    page0, page1 = doc[0], doc[1]
    fields0 = _widget_map(page0)
    fields1 = _widget_map(page1)

    # Randstad source burned /s/ Brendan Ngehsi Newanforbi into the content
    # stream. Redact those runs (a white rect left them visible under the
    # stamp). Clip above the printed italic labels, then restore Sign here
    # and the declaration line if a redact nicks them.
    for rect in page0.search_for("/s/ Brendan Ngehsi Newanforbi"):
        page0.add_redact_annot(
            pymupdf.Rect(rect.x0 - 1.0, rect.y0 - 0.4, rect.x1 + 1.0, min(rect.y1, 704.5)),
            fill=(1, 1, 1),
        )
    page0.add_redact_annot(pymupdf.Rect(379.0, 694.8, 470.0, 708.0), fill=(1, 1, 1))
    page0.add_redact_annot(pymupdf.Rect(36.0, 693.0, 132.5, 708.0), fill=(1, 1, 1))
    page0.add_redact_annot(pymupdf.Rect(66.4, 682.8, 200.0, 693.8), fill=(1, 1, 1))
    # Old Name: value sits under item 1. Do not start the wipe at y=219 —
    # that ate "nformation" from "Your Information" (bbox y1=220.7, x1=154.7).
    page0.add_redact_annot(pymupdf.Rect(154.7, 219.0, 392.5, 234.0), fill=(1, 1, 1))
    page0.add_redact_annot(pymupdf.Rect(97.3, 221.2, 154.7, 234.0), fill=(1, 1, 1))
    page1.add_redact_annot(pymupdf.Rect(97.0, 47.5, 250.0, 64.0), fill=(1, 1, 1))
    page0.apply_redactions()
    page1.apply_redactions()
    if "Your Information" not in (page0.get_text() or ""):
        page0.insert_text(
            (63.0, 216.6),
            "Your Information ",
            fontsize=11,
            fontname="hebo",
            color=(0, 0, 0),
        )
    # Cover leftover date tops that overlap the declaration, then restore
    # the official second line of the perjury block.
    _whiteout(page0, pymupdf.Rect(36.0, 667.0, 285.0, 682.5))
    page0.insert_text(
        (36.0, 678.7),
        "on this form and all attachments is true and correct.",
        fontsize=11,
        fontname="tibo",
        color=(0, 0, 0),
    )
    if not page0.search_for("Sign here"):
        page0.insert_text(
            (336.9, 715.9),
            "Sign here",
            fontsize=11,
            fontname="titi",
            color=(0, 0, 0),
        )
    # Cover the printed sign-here pointer; it reads as a black triangle.
    _whiteout(page0, pymupdf.Rect(335.8, 688.0, 344.8, 704.4))

    for page in (page0, page1):
        for w in page.widgets() or []:
            short = (w.field_name or "").split(".")[-1]
            if short == "WaiveSuperiorCrtFee[0]" or short == "GrossMonthIncomeLess[0]":
                _set_on(w)

    money = {
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
    for short, text in money.items():
        if short in fields1:
            _write_on_line(page1, fields1[short], text, fontsize=7.0)
        elif short in fields0:
            _write_on_line(page0, fields0[short], text, fontsize=7.0)

    _drop_text_widgets(page0)
    _drop_text_widgets(page1)

    court_rect = fields0.get("CourtInfo[0]", pymupdf.Rect(398.9, 169.0, 573.1, 236.3))
    _whiteout(page0, court_rect)
    _write_stack(
        page0,
        court_rect,
        [COURT_COUNTY, COURT_STREET, COURT_CITYZIP],
        max_fs=8.5,
        min_fs=7.0,
    )

    # "Case Name:" label sits at y≈287–300. Stack in the widget under it.
    # Extra wipe just above the B kills the leftover tick from the Randstad fill.
    _whiteout(page0, pymupdf.Rect(399.0, 298.8, 420.0, 301.2))
    case_rect = pymupdf.Rect(399.5, 300.4, 572.0, 316.2)
    _whiteout(page0, case_rect)
    _write_stack(
        page0,
        case_rect,
        _caption_lines(case["caption"]),
        max_fs=6.6,
        min_fs=6.0,
        leading=7.2,
        valign="center",
    )

    if "PetitionerName1[0]" in fields0:
        _write_on_line(page0, fields0["PetitionerName1[0]"], PLAINTIFF_PRINT, fontsize=8.0)
    if "PetitionerStrAddress[0]" in fields0:
        _write_on_line(page0, fields0["PetitionerStrAddress[0]"], STREET, fontsize=8.0)
    if "PetitionerCity[0]" in fields0:
        _write_on_line(page0, fields0["PetitionerCity[0]"], CITY, fontsize=8.0)
    if "PetitionerState[0]" in fields0:
        _write_on_line(page0, fields0["PetitionerState[0]"], STATE, fontsize=8.0)
    if "PetitionerZip[0]" in fields0:
        _write_on_line(page0, fields0["PetitionerZip[0]"], ZIP, fontsize=8.0)
    if "PetitionerTel[0]" in fields0:
        _write_on_line(page0, fields0["PetitionerTel[0]"], PHONE, fontsize=8.0)
    if "SigDate[0]" in fields0:
        _write_on_line(page0, fields0["SigDate[0]"], EXEC_DATE, fontsize=8.0)
    # Print name sits on the rule at y=707.3, left of "Print your name here" (x≈133).
    _write_at(page0, 37.0, 706.6, PLAINTIFF_PRINT, 8.0)
    if "PetitionerName1[0]" in fields1:
        _write_on_line(page1, fields1["PetitionerName1[0]"], PLAINTIFF_PRINT, fontsize=8.0)

    # Signature rule is y=707.3.
    _stamp_on_rule(page0, 368.0, 707.3, 128.0, sink=6.6)

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
