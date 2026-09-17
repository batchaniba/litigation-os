#!/usr/bin/env python3
"""Matter 27 — Randstad default-judgment prove-up packet.

Alameda Super. Ct. No. 26CV199902, Dept. 20 (Hon. Thomas Weathers).

Court judgment after default already ENTERED September 16, 2026 (Pesko).
Randstad US, LLC only. Do not CIV-100 RK. Do not restamp the entered default.

Amounts are a Kim v. Westmoore prove-up, not the Greenup/425.115 ceiling.
Ask: ICRAA $10,000 + Penal Code additional $10,000 (1× ICRAA as the
actuals stand-in) + $25,000 civil penalty + $543.70 interest = $45,543.70.
The served 425.115 $500,000 notice is recited as the preserved cap; $0
punitive is requested on this packet. No 425.11; no emotional-distress
or lost-wage line. Fees $0. Costs waived.

  python3 internal/scripts/matter27-randstad-prove-up-packet.py

Packet order:
  1. CIV-100 (court judgment; default previously entered 09/16/2026)
  2. JUD-100 proposed judgment
  3. CIV-110 dismissal of Does 1-20 without prejudice
  4. Declaration ISO default judgment
  5. Exhibits A-I
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_PATH, stamp_on_pdf_line  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "internal" / "public" / "documents" / "matter-27"
DOCS = OUT_DIR
FORMS_DIR = REPO / "internal" / "public" / "documents" / "_form-library"
BUILD_DIR = Path("/tmp/m27build")
TMP_FORMS = Path("/tmp/m27forms")

BLANK_CIV100 = FORMS_DIR / "civ100-blank-template.pdf"
BLANK_JUD100 = FORMS_DIR / "jud100-blank-template.pdf"
BLANK_CIV110 = FORMS_DIR / "civ110-blank-template.pdf"

PLAINTIFF = "Brendan Ngehsi Newanforbi"
PLAINTIFF_CAPS = "BRENDAN NGEHSI NEWANFORBI"
CASE_NO = "26CV199902"
COMPLAINT_FILED = "07/20/2026"
DEFAULT_ENTERED = "09/16/2026"
DATE_SHORT = "09/16/2026"
DATE_LONG = "September 16, 2026"
CAPTION_DEFENDANTS = "Randstad US, LLC, et al."
RANDSTAD_AS_SUED = "RANDSTAD US, LLC, a Delaware limited liability company"
RANDSTAD_SHORT = "Randstad US, LLC"

# Conservative itemized ask. See declaration. Not the $500,000 cap.
ICRAA = "10,000.00"
PC_ADD = "10,000.00"  # 1x ICRAA as Penal Code actuals stand-in
PC_PENALTY = "25,000.00"
STATUTORY = "45,000.00"  # 10,000 + 10,000 + 25,000
PUNITIVE = "0.00"
DEMAND = "45,000.00"  # CIV-100 2a = itemized statutory only
INTEREST = "543.70"  # 7% x 63/365 from July 15, 2026 on $45,000
COSTS = "0.00"
FEES = "0.00"
TOTAL = "45,543.70"
ZERO = "0.00"
RATE = "7"
ASK_PUNITIVE = False

PARTY = {
    "name": PLAINTIFF,
    "street": "1455 Cat Tail Drive",
    "city": "Stockton",
    "state": "CA",
    "zip": "95204",
    "phone": "(209) 801-4442",
    "email": "bnn.cdl@gmail.com",
    "atty_for": "Plaintiff, In Pro Per",
}
COURT = {
    "county": "ALAMEDA",
    "street": "1225 Fallon Street",
    "mailing": "1225 Fallon Street",
    "cityzip": "Oakland, CA 94612",
    "branch": "Rene C. Davidson Courthouse",
}

MAIL_BLOCK = (
    "Chadwick L. Williams, Esq., Kabat Chapman & Ozmer LLP\n"
    "1150 Spring Street NW, Suite 800, Atlanta, GA 30309\n"
    "Randstad US, LLC, c/o CSC - Lawyers Incorporating Service\n"
    "2710 Gateway Oaks Drive, Suite 150N, Sacramento, CA 95833"
)

JUD100_OTHER = (
    "Several judgment (CCP 579) as to Randstad US, LLC only. "
    "RK Logistics remains. Does 1-20 dismissed without prejudice. "
    "Default entered 09/16/2026. Punitive damages noticed under "
    "CCP 425.115; none requested on this judgment. Costs waived "
    "(FW-003)."
)
PUNITIVE_LABEL = ""

CIV100_OUT = (
    "CIV-100 Request for Court Judgment - Randstad US LLC "
    "(Default Previously Entered, Sep 16 2026).pdf"
)
JUD100_OUT = (
    "[Proposed] Judgment (JUD-100) - Randstad US LLC "
    "(Default Prove-Up, Sep 16 2026).pdf"
)
CIV110_OUT = (
    "CIV-110 Request for Dismissal of Does 1-20 "
    "(Without Prejudice, Executed Sep 16 2026).pdf"
)
DECL_OUT = (
    "Declaration of Brendan Ngehsi Newanforbi ISO Default Judgment "
    "by Court - Randstad US LLC (Sep 16 2026).pdf"
)
PACKET_OUT = (
    "Default Judgment Prove-Up Packet - Randstad US LLC "
    "(Court Judgment, Sep 16 2026).pdf"
)

EXHIBITS: list[tuple[str, str, Path]] = [
    (
        "A",
        "Verified Complaint for Damages (filed July 20, 2026)",
        DOCS / "Complaint for Damages - Newanforbi v Randstad US LLC et al (Jul 20 2026).pdf",
    ),
    (
        "B",
        "POS-010 Proof of Service of Summons — Randstad US, LLC (served July 30, 2026)",
        DOCS
        / (
            "POS-010 Proof of Service of Summons - Randstad US LLC "
            "(Served Jul 30 2026, Levying Officer 2026026857).pdf"
        ),
    ),
    (
        "C",
        "CIV-100 — default ENTERED as to Randstad US, LLC (September 16, 2026)",
        DOCS
        / (
            "CIV-100 Request for Entry of Default - Randstad US LLC "
            "(Default Entered, Filed Sep 16 2026).pdf"
        ),
    ),
    (
        "D",
        "Amended CCP §425.115 Notice — Randstad US, LLC ($500,000.00)",
        DOCS
        / (
            "Amended Notice of Amount of Punitive Damages Sought (CCP 425.115) "
            "- Randstad US LLC (Aug 7 2026).pdf"
        ),
    ),
    (
        "E",
        "POS-040 — Amended §425.115 Notice (served August 21, 2026; filed September 9, 2026)",
        DOCS
        / (
            "POS-040 Proof of Service - Amended CCP 425.115 Notice - Randstad US LLC "
            "(Served Aug 21 2026, Filed Sep 9 2026, Levying Officer 2026028894).pdf"
        ),
    ),
    (
        "F",
        "InfoMart background-check report, Order No. 15780719",
        DOCS / "15780719Final_Profile.PDF",
    ),
    (
        "G",
        "InfoMart Notice to Consumer for Employment Purposes (July 13, 2026)",
        DOCS / "Notice to Consumer for Employment Purposes.pdf",
    ),
    (
        "H",
        "Randstad rehire notification (July 7, 2026)",
        DOCS / "Welcome to Randstad.pdf",
    ),
    (
        "I",
        "FW-003 Order on Court Fee Waiver (granted July 20, 2026)",
        DOCS / "FW-003 Order on Court Fee Waiver - GRANTED (One Legal download, Jul 20 2026).pdf",
    ),
]


def _endswith(name: str, *suffixes: str) -> bool:
    return any(name.endswith(s) for s in suffixes)


def set_text(doc: fitz.Document, suffix: str, value: str) -> int:
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string == "Text" and _endswith(w.field_name or "", suffix):
                w.field_value = value
                w.update()
                n += 1
    return n


def set_text_exact(doc: fitz.Document, full_suffix: str, value: str) -> int:
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string == "Text" and (w.field_name or "").endswith(full_suffix):
                w.field_value = value
                w.update()
                n += 1
    return n


def check_by_label(
    doc: fitz.Document,
    label_substr: str,
    on: bool = True,
    *,
    exact: bool = False,
) -> int:
    n = 0
    target = label_substr.lower()
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            lab = (w.field_label or "").strip()
            lab_l = lab.lower()
            match = lab_l == target if exact else target in lab_l
            if match:
                w.field_value = w.on_state() if on else "Off"
                w.update()
                n += 1
    return n


def check_radio_choice(doc: fitz.Document, name_contains: str, on_value) -> int:
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if name_contains not in name:
                continue
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            if w.on_state() == on_value or str(w.on_state()) == str(on_value):
                w.field_value = w.on_state()
                w.update()
                n += 1
    return n


def force_off(doc: fitz.Document, pred) -> int:
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            if pred(w):
                w.field_value = "Off"
                w.update()
                n += 1
    return n


def ensure_blank(path: Path, url: str, fallback: Path | None = None) -> Path:
    if path.is_file() and path.stat().st_size > 10_000:
        return path
    if fallback is not None and fallback.is_file() and fallback.stat().st_size > 10_000:
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fallback, path)
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        ["curl", "-fsSL", "-A", "Mozilla/5.0", "-L", url, "-o", str(path)]
    )
    return path


def ensure_forms() -> None:
    ensure_blank(
        BLANK_CIV100,
        "https://www.courts.ca.gov/documents/civ100.pdf",
        TMP_FORMS / "civ100.pdf",
    )
    ensure_blank(
        BLANK_JUD100,
        "https://www.courts.ca.gov/documents/jud100.pdf",
        TMP_FORMS / "jud100.pdf",
    )
    ensure_blank(
        BLANK_CIV110,
        "https://www.courts.ca.gov/documents/civ110.pdf",
        TMP_FORMS / "civ110.pdf",
    )


def fill_caption(doc: fitz.Document, defendant_caption: str) -> None:
    set_text(doc, "AttyName[0]", PARTY["name"])
    set_text(doc, "Name[0]", PARTY["name"])
    set_text(doc, "AttyStreet[0]", PARTY["street"])
    set_text(doc, "Street[0]", PARTY["street"])
    set_text(doc, "AttyCity[0]", PARTY["city"])
    set_text(doc, "City[0]", PARTY["city"])
    set_text(doc, "AttyState[0]", PARTY["state"])
    set_text(doc, "State[0]", PARTY["state"])
    set_text(doc, "AttyZip[0]", PARTY["zip"])
    set_text(doc, "Zip[0]", PARTY["zip"])
    set_text(doc, "Phone[0]", PARTY["phone"])
    set_text(doc, "Email[0]", PARTY["email"])
    set_text(doc, "AttyFor[0]", PARTY["atty_for"])
    set_text(doc, "CrtCounty[0]", COURT["county"])
    set_text_exact(doc, "CourtInfo[0].Street[0]", COURT["street"])
    set_text_exact(doc, "CourtInfo[0].CrtStreet[0]", COURT["street"])
    set_text_exact(doc, "CourtInfo[0].MailingAdd[0]", COURT["mailing"])
    set_text_exact(doc, "CourtInfo[0].CrtMailingAdd[0]", COURT["mailing"])
    set_text_exact(doc, "CourtInfo[0].CityZip[0]", COURT["cityzip"])
    set_text_exact(doc, "CourtInfo[0].CrtCityZip[0]", COURT["cityzip"])
    set_text_exact(doc, "CourtInfo[0].Branch[0]", COURT["branch"])
    set_text_exact(doc, "CourtInfo[0].CrtBranch[0]", COURT["branch"])
    set_text(doc, "CaseNumber[0]", CASE_NO)
    set_text(doc, "Party1[0]", PLAINTIFF)
    set_text(doc, "Party2[0]", defendant_caption)


def fill_civ100() -> fitz.Document:
    doc = fitz.open(ensure_blank(BLANK_CIV100, "https://www.courts.ca.gov/documents/civ100.pdf"))
    fill_caption(doc, CAPTION_DEFENDANTS)

    # Title: Court Judgment only. Default is already entered.
    check_by_label(doc, "Court Judgment", exact=True)

    set_text_exact(doc, "Lia[0].DateField1[0]", COMPLAINT_FILED)
    set_text_exact(doc, "Lib[0].FillText99[0]", PLAINTIFF)
    check_by_label(doc, "I request a court judgment")
    set_text_exact(doc, "Lic[0].TextField6[0]", RANDSTAD_AS_SUED)
    set_text_exact(doc, "Lid[0].TextField6[0]", RANDSTAD_AS_SUED)
    check_by_label(doc, "for default previously entered on")
    set_text_exact(doc, "SubLi3[0].DateField1[0]", DEFAULT_ENTERED)

    set_text_exact(doc, "SubLia[0].FillText68[0]", DEMAND)
    set_text_exact(doc, "SubLia[0].FillText67[0]", ZERO)
    set_text_exact(doc, "SubLia[0].FillText66[0]", DEMAND)
    set_text_exact(doc, "SubLic[0].FillText59[0]", INTEREST)
    set_text_exact(doc, "SubLic[0].FillText58[0]", ZERO)
    set_text_exact(doc, "SubLic[0].FillText57[0]", INTEREST)
    set_text_exact(doc, "SubLid[0].FillText56[0]", COSTS)
    set_text_exact(doc, "SubLid[0].FillText55[0]", ZERO)
    set_text_exact(doc, "SubLid[0].FillText54[0]", COSTS)
    set_text_exact(doc, "SubLie[0].FillText53[0]", FEES)
    set_text_exact(doc, "SubLie[0].FillText52[0]", ZERO)
    set_text_exact(doc, "SubLie[0].FillText51[0]", FEES)
    set_text_exact(doc, "SubLif[0].FillText73[0]", TOTAL)
    set_text_exact(doc, "SubLif[0].FillText72[0]", ZERO)
    set_text_exact(doc, "SubLif[0].FillText71[0]", TOTAL)

    set_text_exact(doc, "Signature[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Signature[0].signame[0]", PLAINTIFF_CAPS)
    check_radio_choice(doc, "UDAsst[", 2)

    check_radio_choice(doc, "List6[0].lib[0].mailStatus[0]", 2)
    set_text_exact(doc, "li1[0].FillText129[0]", DATE_LONG)
    mail_rect = None
    for page in doc:
        for w in page.widgets() or []:
            if (w.field_name or "").endswith("li2[0].FillText130[0]"):
                w.text_fontsize = 6.0
                w.field_value = MAIL_BLOCK
                w.update()
                mail_rect = fitz.Rect(w.rect)

    set_text_exact(doc, "Declaration1[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Declaration1[0].sigName[0]", PLAINTIFF_CAPS)

    check_by_label(
        doc,
        "Declaration under Code Civ. Proc., § 585.5 (for entry of default under Code Civ. Proc., § 585(a)). This action",
        exact=True,
    )
    check_radio_choice(doc, "P2Li5a[0].Contract_cb[", 2)
    check_radio_choice(doc, "P2Li5b[0].ConditionalContract_cb[", 2)
    check_radio_choice(doc, "P2Li5c[0].Obligaition_cb[", 2)

    check_by_label(doc, "Costs and disbursements are waived")
    set_text_exact(doc, "Declaration2[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Declaration2[0].sigName[0]", PLAINTIFF_CAPS)

    check_by_label(doc, "a business entity")
    for page in doc:
        for w in page.widgets() or []:
            lab = (w.field_label or "").lower()
            if "not eligible to serve in the u.s. military because" in lab:
                w.field_value = w.on_state()
                w.update()
    set_text_exact(doc, "Declaration3[0].sigDate[0]", DATE_SHORT)
    set_text_exact(doc, "Declaration3[0].sigName[0]", PLAINTIFF_CAPS)

    force_off(
        doc,
        lambda w: any(
            s in (w.field_label or "").lower()
            for s in (
                "entry of default",
                "clerk's judgment",
                "enter default of defendant",
                "enter clerk",
                "restitution of the premises",
                "under code of civil procedure section 585(a)",
                "unlawful detainer case",
            )
        )
        or (w.field_label or "").strip() in ("is", "did", "incarcerated", "other"),
    )
    check_by_label(doc, "Court Judgment", exact=True)
    check_by_label(doc, "I request a court judgment")
    check_by_label(doc, "for default previously entered on")
    check_by_label(
        doc,
        "Declaration under Code Civ. Proc., § 585.5 (for entry of default under Code Civ. Proc., § 585(a)). This action",
        exact=True,
    )
    check_radio_choice(doc, "UDAsst[", 2)
    check_radio_choice(doc, "P2Li5a[0].Contract_cb[", 2)
    check_radio_choice(doc, "P2Li5b[0].ConditionalContract_cb[", 2)
    check_radio_choice(doc, "P2Li5c[0].Obligaition_cb[", 2)
    check_radio_choice(doc, "List6[0].lib[0].mailStatus[0]", 2)
    check_by_label(doc, "Costs and disbursements are waived")
    for page in doc:
        for w in page.widgets() or []:
            lab = (w.field_label or "").lower()
            if "mailed first-class" in lab:
                w.field_value = w.on_state()
                w.update()
            if lab.strip() == "a business entity":
                w.field_value = w.on_state()
                w.update()
            if "not eligible to serve in the u.s. military because" in lab:
                w.field_value = w.on_state()
                w.update()

    if Path(SIGNATURE_PATH).is_file():
        stamp_on_pdf_line(doc[0], 400, 530, 680)
        stamp_on_pdf_line(doc[1], 400, 530, 448)
        stamp_on_pdf_line(doc[1], 400, 530, 645)
        stamp_on_pdf_line(doc[2], 400, 530, 698)

    doc.bake(annots=True, widgets=True)
    page3 = doc[2]
    page3.draw_rect(fitz.Rect(0.0, 756.0, 612.0, 792.0), color=(1, 1, 1), fill=(1, 1, 1), width=0)
    if mail_rect is not None:
        page = doc[1]
        page.draw_rect(mail_rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
        y = mail_rect.y0 + 8.0
        for line in MAIL_BLOCK.split("\n"):
            page.insert_text(
                (mail_rect.x0 + 1.5, y),
                line,
                fontsize=6.4,
                fontname="helv",
                color=(0, 0, 0),
            )
            y += 8.0
    return doc


def fill_jud100() -> fitz.Document:
    doc = fitz.open(ensure_blank(BLANK_JUD100, "https://www.courts.ca.gov/documents/jud100.pdf"))
    fill_caption(doc, f"{RANDSTAD_SHORT}, et al.")
    set_text_exact(doc, "AttyInfo[0].AttyName[0]", PARTY["name"])
    set_text_exact(doc, "AttyInfo[0].AttyStreet[0]", PARTY["street"])
    set_text_exact(doc, "AttyInfo[0].AttyCity[0]", PARTY["city"])
    set_text_exact(doc, "AttyInfo[0].AttyState[0]", PARTY["state"])
    set_text_exact(doc, "AttyInfo[0].AttyZip[0]", PARTY["zip"])
    set_text_exact(doc, "AttyInfo[0].Phone[0]", PARTY["phone"])
    set_text_exact(doc, "AttyInfo[0].Email[0]", PARTY["email"])
    set_text_exact(doc, "AttyInfo[0].AttyFor[0]", PARTY["atty_for"])

    check_by_label(doc, "By Court", exact=True)
    check_by_label(doc, "By Default", exact=True)
    check_by_label(doc, "BY DEFAULT", exact=True)
    check_by_label(doc, "Court Judgment (Code of Civil Procedure Section 585(b)")
    check_by_label(doc, "plaintiff's written declaration")
    check_by_label(doc, "THE COURT", exact=True)

    check_by_label(doc, "for plaintiff", exact=True)
    set_text_exact(doc, "Lia[0].FillText20[0]", PLAINTIFF)
    for page in doc:
        for w in page.widgets() or []:
            if (w.field_name or "").endswith("Lia[0].FillText21[0]"):
                w.text_fontsize = 7.0
                w.field_value = RANDSTAD_AS_SUED
                w.update()
    check_by_label(doc, "for defendant", on=False, exact=True)

    check_by_label(doc, "Defendant named in item 5a above must")
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if "List6[0].Lia[0].Table1[0]" not in name:
                continue
            lab = (w.field_label or "").lower().strip()
            if w.field_type_string == "CheckBox":
                money_boxes = ("damages", "costs")
                if ASK_PUNITIVE:
                    money_boxes = money_boxes + ("other",)
                if lab in money_boxes or "prejudgment interest" in lab:
                    w.field_value = w.on_state()
                    w.update()
            elif w.field_type_string == "Text":
                if name.endswith("EXPN[0]"):
                    w.field_value = STATUTORY
                    w.update()
                elif name.endswith("NumericField2[0]"):
                    w.field_value = RATE
                    w.update()
                elif name.endswith("EXPN1[0]"):
                    w.field_value = INTEREST
                    w.update()
                elif name.endswith("EXPN3[0]"):
                    w.field_value = COSTS
                    w.update()
                elif name.endswith("FillText51[0]") and ASK_PUNITIVE:
                    w.field_value = PUNITIVE_LABEL
                    w.update()
                elif name.endswith("EXPN4[0]") and ASK_PUNITIVE:
                    w.field_value = PUNITIVE
                    w.update()
                elif name.endswith("EXPN5[0]"):
                    w.field_value = TOTAL
                    w.update()

    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if name.endswith("RB2Choices87[0]"):
                w.field_value = w.on_state()
                w.update()
            if name.endswith("item8[0].FillText88[0]"):
                w.field_value = JUD100_OTHER
                w.update()

    force_off(
        doc,
        lambda w: any(
            s in (w.field_label or "").lower()
            for s in (
                "by clerk",
                "after court trial",
                "defendant did not appear at trial",
                "on stipulation",
                "clerk's judgment",
                "plaintiff's testimony and other evidence",
                "plaintiff to receive nothing from defendant",
                "defendant named in item 5b to recover",
                "for cross-complainant",
                "for cross-defendant",
            )
        )
        or (w.field_label or "").strip() == "for defendant"
        or (w.field_name or "").endswith("List5[0].Lib[0].CheckBox34[0]")
        or (w.field_name or "").endswith("List6[0].Lib[0].CBChoice41[0]")
        or (w.field_name or "").endswith("Table2[0].RB2Choices99[0]"),
    )
    check_by_label(doc, "By Court", exact=True)
    check_by_label(doc, "By Default", exact=True)
    check_by_label(doc, "BY DEFAULT", exact=True)
    check_by_label(doc, "Court Judgment (Code of Civil Procedure Section 585(b)")
    check_by_label(doc, "plaintiff's written declaration")
    check_by_label(doc, "THE COURT", exact=True)
    check_by_label(doc, "for plaintiff", exact=True)
    check_by_label(doc, "Defendant named in item 5a above must")
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            lab = (w.field_label or "").lower().strip()
            if "List6[0].Lia[0].Table1[0]" in name and w.field_type_string == "CheckBox":
                money_boxes = ("damages", "costs")
                if ASK_PUNITIVE:
                    money_boxes = money_boxes + ("other",)
                if lab in money_boxes or "prejudgment interest" in lab:
                    w.field_value = w.on_state()
                    w.update()
            if name.endswith("RB2Choices87[0]"):
                w.field_value = w.on_state()
                w.update()
    check_by_label(doc, "for defendant", on=False, exact=True)

    doc.bake(annots=True, widgets=True)
    return doc


def fill_civ110() -> fitz.Document:
    doc = fitz.open(ensure_blank(BLANK_CIV110, "https://www.courts.ca.gov/documents/civ110.pdf"))
    fill_caption(doc, CAPTION_DEFENDANTS)
    set_text_exact(doc, "AttyPartyInfo[0].Name[0]", PARTY["name"])
    set_text_exact(doc, "AttyPartyInfo[0].Street[0]", PARTY["street"])
    set_text_exact(doc, "AttyPartyInfo[0].City[0]", PARTY["city"])
    set_text_exact(doc, "AttyPartyInfo[0].State[0]", PARTY["state"])
    set_text_exact(doc, "AttyPartyInfo[0].Zip[0]", PARTY["zip"])
    set_text_exact(doc, "AttyPartyInfo[0].Phone[0]", PARTY["phone"])
    set_text_exact(doc, "AttyPartyInfo[0].Email[0]", PARTY["email"])
    set_text_exact(doc, "AttyPartyInfo[0].AttyFor[0]", PARTY["atty_for"])

    check_radio_choice(doc, "li1a2[0].RB1Choices[0]", 2)
    check_by_label(doc, "Complaint", exact=True)
    check_radio_choice(doc, "li1b6[0].RB2Choices[0]", 2)
    set_text_exact(
        doc,
        "li1b6[0].FillText109[0]",
        "Does 1 through 20, inclusive, only — not Randstad US, LLC; not The RK Logistics Group, Inc.",
    )
    force_off(
        doc,
        lambda w: (w.field_label or "").strip().lower().startswith("cross-complaint")
        or (w.field_label or "").strip() in ("Petition", "With prejudice")
        or "retaining jurisdiction" in (w.field_label or "").lower()
        or "Entire action" in (w.field_label or ""),
    )
    check_radio_choice(doc, "CheckBox2D[", 1)
    set_text_exact(doc, "List2[0].DateTimeField1[0]", DATE_SHORT)
    set_text_exact(doc, "List2[0].Sig1Name[0]", PLAINTIFF_CAPS)
    check_radio_choice(doc, "List2[0].CheckBox2A[", 2)
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            lab = (w.field_label or "").strip()
            if "List2[0]" in name and lab == "Plaintiff/Petitioner":
                w.field_value = w.on_state()
                w.update()
    if Path(SIGNATURE_PATH).is_file():
        stamp_on_pdf_line(doc[0], 430, 530, 469)

    set_text_exact(doc, "Item1[0].FillText109[0]", PLAINTIFF)
    check_radio_choice(doc, "li2c[0].CBCourtFee[0]", 3)
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            lab = (w.field_label or "").strip()
            if "Item3[0].Yes[" in name and lab == "No":
                w.field_value = w.on_state()
                w.update()
    set_text_exact(doc, "PoP[0].DateTimeField1[0]", DATE_SHORT)
    set_text_exact(doc, "PoP[0].YourName2[0]", PLAINTIFF_CAPS)
    check_radio_choice(doc, "PoP[0].CheckBox4A[", 2)
    if Path(SIGNATURE_PATH).is_file() and doc.page_count > 1:
        stamp_on_pdf_line(doc[1], 430, 530, 370)

    doc.bake(annots=True, widgets=True)
    return doc


def exhibit_cover(letter: str, title: str) -> fitz.Document:
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text((72, 300), f"EXHIBIT {letter}", fontsize=28, fontname="times-bold")
    page.insert_textbox(
        fitz.Rect(72, 340, 540, 460),
        title,
        fontsize=14,
        fontname="times-roman",
        align=fitz.TEXT_ALIGN_LEFT,
    )
    page.insert_text(
        (72, 500),
        "Newanforbi v. Randstad US, LLC, et al.",
        fontsize=11,
        fontname="times-italic",
    )
    page.insert_text((72, 516), f"Alameda Super. Ct. No. {CASE_NO}", fontsize=11, fontname="times-roman")
    return doc


def save_doc(doc: fitz.Document, name: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / name
    tmp = out.with_suffix(out.suffix + ".tmp")
    doc.save(str(tmp), garbage=4, deflate=True)
    tmp.replace(out)
    print(f"Wrote {out.relative_to(REPO)} ({out.stat().st_size} bytes, {doc.page_count} pages)")
    return out


def run_declaration() -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["MATTER27_DECL_OUT_DIR"] = str(BUILD_DIR)
    env["MATTER27_EXEC_DATE"] = DATE_LONG
    env["MATTER27_DECL_TAG"] = "Sep16_2026"
    subprocess.check_call(
        [sys.executable, str(SCRIPT_DIR / "matter27-randstad-prove-up-declaration.py")],
        env=env,
    )
    path = BUILD_DIR / "_build_Randstad_Declaration_ISO_Default_Judgment_Sep16_2026.pdf"
    if not path.is_file():
        raise SystemExit("Declaration build output missing")
    return path


def assemble(
    civ100: Path,
    jud100: Path,
    civ110: Path,
    decl: Path,
    out_path: Path,
) -> None:
    out = fitz.open()
    for path in (civ100, jud100, civ110, decl):
        part = fitz.open(path)
        out.insert_pdf(part)
        part.close()
    missing = []
    for letter, title, src in EXHIBITS:
        if not src.is_file():
            missing.append(str(src))
            continue
        cover = exhibit_cover(letter, title)
        out.insert_pdf(cover)
        cover.close()
        body = fitz.open(src)
        out.insert_pdf(body)
        body.close()
    if missing:
        out.close()
        raise SystemExit("Missing exhibits:\n  " + "\n  ".join(missing))
    tmp = out_path.with_suffix(".tmp.pdf")
    out.save(tmp, garbage=4, deflate=True)
    pages = out.page_count
    out.close()
    shutil.move(str(tmp), str(out_path))
    print(f"Wrote {out_path.relative_to(REPO)} ({out_path.stat().st_size} bytes, {pages} pages)")


def verify(path: Path) -> None:
    doc = fitz.open(path)
    full = "\n".join(page.get_text() or "" for page in doc)
    form_text = "\n".join(
        (page.get_text() or "") for page in doc if page.number < 5
    )
    checks = {
        "court_judgment": "Court Judgment" in full,
        "previously_entered": "previously entered" in full.lower() or "09/16/2026" in full,
        "demand_45000": DEMAND in full,
        "statutory_45000": STATUTORY in full,
        "interest": INTEREST in full,
        "total": TOTAL in full,
        "no_500k_on_forms": "500000" not in form_text.replace(",", "").replace(".00", ""),
        "cap_recited": "500,000" in full,
        "no_rk_as_judgment_debtor_only": "THE RK LOGISTICS GROUP" in full,
        "does_dismissal": "Does 1 through 20" in full,
        "costs_waived": "waived" in full.lower(),
        "425115": "425.115" in full,
        "no_github": "github.com" not in full.lower(),
        "randstad_named": "RANDSTAD US, LLC" in full,
        "has_exhibit_a": "EXHIBIT A" in full,
        "has_exhibit_i": "EXHIBIT I" in full,
        "exec_sep16": "September 16, 2026" in full or "09/16/2026" in full,
        "fees_zero": "attorney's fees" in full.lower() or "not requested" in full.lower(),
    }
    print(f"Verify {path.name}:")
    fails = 0
    for key, ok in checks.items():
        print(f"  {'OK' if ok else 'FAIL'}: {key}")
        if not ok:
            fails += 1
    print(f"  pages={doc.page_count}")
    doc.close()
    if fails:
        raise SystemExit(f"Prove-up packet failed {fails} check(s)")


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    ensure_forms()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    civ = fill_civ100()
    civ_path = save_doc(civ, CIV100_OUT)
    civ.close()

    jud = fill_jud100()
    jud_path = save_doc(jud, JUD100_OUT)
    jud.close()

    civ110 = fill_civ110()
    civ110_path = save_doc(civ110, CIV110_OUT)
    civ110.close()

    decl_build = run_declaration()
    decl_path = OUT_DIR / DECL_OUT
    shutil.copy2(decl_build, decl_path)
    print(f"Wrote {decl_path.relative_to(REPO)} ({decl_path.stat().st_size} bytes)")

    packet_path = OUT_DIR / PACKET_OUT
    assemble(civ_path, jud_path, civ110_path, decl_path, packet_path)
    verify(packet_path)


if __name__ == "__main__":
    main()
