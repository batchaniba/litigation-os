#!/usr/bin/env python3
"""Matter 27 — clerk's Request for Entry of Default (CIV-100) as to each defendant.

Alameda Super. Ct. No. 26CV199902, Dept. 20 (Hon. Thomas Weathers).

These are clerk-default papers only. They do not ask for a clerk's judgment or
a court judgment. Punitive damages stay off the CIV-100 (no item 2 money);
the amended CCP §425.115 notices were personally served August 21, 2026.

Randstad US, LLC: default ENTERED September 16, 2026 (conformed CIV-100 on
file). Do not regenerate over that stamped copy. CRC 3.110(h) then runs 45
days from entry to obtain a default judgment.

The RK Logistics Group, Inc.: still HOLD. Do not e-file until eCourt is
checked for Gurney's September 14 CIV-141 (or an answer / demurrer /
stipulation). Prepared papers are dated September 15, 2026.

  python3 internal/scripts/matter27-request-for-default.py

FILED_STATUS: Randstad entered 09/16/2026; RK remains False until e-filed
and the CCP §587 copies have been mailed.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_PATH, stamp_on_pdf_line  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "internal" / "public" / "documents" / "matter-27"
FORMS_DIR = REPO / "internal" / "public" / "documents" / "_form-library"
BLANK_CIV100 = FORMS_DIR / "civ100-blank-template.pdf"
CIV100_URL = "https://www.courts.ca.gov/documents/civ100.pdf"

FILED_STATUS = False

PLAINTIFF = "Brendan Ngehsi Newanforbi"
PLAINTIFF_CAPS = "BRENDAN NGEHSI NEWANFORBI"
CASE_NO = "26CV199902"
COMPLAINT_FILED = "07/20/2026"
CAPTION_DEFENDANTS = "Randstad US, LLC, et al."

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


@dataclass(frozen=True)
class DefaultTarget:
    slug: str
    as_sued: str
    short: str
    date_short: str
    date_long: str
    mail_block: str
    out_name: str


RANDSTAD = DefaultTarget(
    slug="randstad",
    as_sued="RANDSTAD US, LLC, a Delaware limited liability company",
    short="Randstad US, LLC",
    date_short="09/16/2026",
    date_long="September 16, 2026",
    mail_block=(
        "Chadwick L. Williams, Esq., Kabat Chapman & Ozmer LLP\n"
        "1150 Spring Street NW, Suite 800, Atlanta, GA 30309\n"
        "Randstad US, LLC, c/o CSC - Lawyers Incorporating Service\n"
        "2710 Gateway Oaks Drive, Suite 150N, Sacramento, CA 95833"
    ),
    out_name=(
        "CIV-100 Request for Entry of Default - Randstad US LLC "
        "(Clerk Default Only, Sep 16 2026).pdf"
    ),
)

RK = DefaultTarget(
    slug="rk",
    as_sued="THE RK LOGISTICS GROUP, INC., a California corporation",
    short="The RK Logistics Group, Inc.",
    date_short="09/15/2026",
    date_long="September 15, 2026",
    mail_block=(
        "Melinda Garcia, Esq., Garcia & Gurney, ALC\n"
        "6600 Koll Center Parkway, Suite 200, Pleasanton, CA 94566\n"
        "The RK Logistics Group, Inc., c/o CSC - Lawyers Incorporating Service\n"
        "2710 Gateway Oaks Drive, Suite 150N, Sacramento, CA 95833"
    ),
    out_name=(
        "CIV-100 Request for Entry of Default - RK Logistics Group Inc "
        "(Clerk Default Only, Sep 15 2026).pdf"
    ),
)


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


def check_by_label(doc: fitz.Document, label_substr: str, on: bool = True) -> int:
    n = 0
    target = label_substr.lower()
    for page in doc:
        for w in page.widgets() or []:
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            lab = (w.field_label or "").strip().lower()
            if target in lab:
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


def off_by_name(doc: fitz.Document, *name_contains: str) -> int:
    n = 0
    for page in doc:
        for w in page.widgets() or []:
            name = w.field_name or ""
            if w.field_type_string not in ("CheckBox", "RadioButton"):
                continue
            if any(s in name for s in name_contains):
                w.field_value = "Off"
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


def ensure_blank() -> Path:
    if BLANK_CIV100.is_file() and BLANK_CIV100.stat().st_size > 10_000:
        return BLANK_CIV100
    BLANK_CIV100.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        ["curl", "-fsSL", "-A", "Mozilla/5.0", "-L", CIV100_URL, "-o", str(BLANK_CIV100)]
    )
    return BLANK_CIV100


def fill_caption(doc: fitz.Document) -> None:
    set_text(doc, "AttyName[0]", PARTY["name"])
    set_text(doc, "AttyStreet[0]", PARTY["street"])
    set_text(doc, "AttyCity[0]", PARTY["city"])
    set_text(doc, "AttyState[0]", PARTY["state"])
    set_text(doc, "AttyZip[0]", PARTY["zip"])
    set_text(doc, "Phone[0]", PARTY["phone"])
    set_text(doc, "Email[0]", PARTY["email"])
    set_text(doc, "AttyFor[0]", PARTY["atty_for"])
    set_text(doc, "CrtCounty[0]", COURT["county"])
    set_text_exact(doc, "CourtInfo[0].Street[0]", COURT["street"])
    set_text_exact(doc, "CourtInfo[0].MailingAdd[0]", COURT["mailing"])
    set_text_exact(doc, "CourtInfo[0].CityZip[0]", COURT["cityzip"])
    set_text_exact(doc, "CourtInfo[0].Branch[0]", COURT["branch"])
    set_text(doc, "CaseNumber[0]", CASE_NO)
    set_text(doc, "Party1[0]", PLAINTIFF)
    set_text(doc, "Party2[0]", CAPTION_DEFENDANTS)


def fill_civ100(target: DefaultTarget) -> fitz.Document:
    doc = fitz.open(ensure_blank())
    fill_caption(doc)

    check_by_label(doc, "Entry of Default")
    set_text_exact(doc, "Lia[0].DateField1[0]", COMPLAINT_FILED)
    set_text_exact(doc, "Lib[0].FillText99[0]", PLAINTIFF)
    check_by_label(doc, "Enter default of defendant")
    set_text_exact(doc, "Lic[0].TextField6[0]", target.as_sued)

    set_text_exact(doc, "Signature[0].sigDate[0]", target.date_short)
    set_text_exact(doc, "Signature[0].signame[0]", PLAINTIFF_CAPS)

    check_radio_choice(doc, "UDAsst[", 2)

    check_radio_choice(doc, "List6[0].lib[0].mailStatus[0]", 2)
    set_text_exact(doc, "li1[0].FillText129[0]", target.date_long)
    mail_rect = None
    for page in doc:
        for w in page.widgets() or []:
            if (w.field_name or "").endswith("li2[0].FillText130[0]"):
                w.text_fontsize = 6.0
                w.field_value = target.mail_block
                w.update()
                mail_rect = fitz.Rect(w.rect)

    set_text_exact(doc, "Declaration1[0].sigDate[0]", target.date_short)
    set_text_exact(doc, "Declaration1[0].sigName[0]", PLAINTIFF_CAPS)

    check_by_label(doc, "a business entity")
    for page in doc:
        for w in page.widgets() or []:
            lab = (w.field_label or "").lower()
            if "not eligible to serve in the u.s. military because" in lab:
                w.field_value = w.on_state()
                w.update()
    set_text_exact(doc, "Declaration3[0].sigDate[0]", target.date_short)
    set_text_exact(doc, "Declaration3[0].sigName[0]", PLAINTIFF_CAPS)

    force_off(
        doc,
        lambda w: any(
            s in (w.field_label or "").lower()
            for s in (
                "clerk's judgment",
                "i request a court judgment",
                "enter clerk",
                "restitution of the premises",
                "under code of civil procedure section 585(a)",
                "for default previously entered",
                "unlawful detainer case",
                "declaration under code civ. proc., § 585.5",
                "costs and disbursements are waived",
            )
        )
        or (w.field_label or "").strip() in ("is", "did", "incarcerated", "other"),
    )
    check_by_label(doc, "Entry of Default")
    check_by_label(doc, "Enter default of defendant")
    check_radio_choice(doc, "UDAsst[", 2)
    check_radio_choice(doc, "List6[0].lib[0].mailStatus[0]", 2)
    check_by_label(doc, "a business entity")
    for page in doc:
        for w in page.widgets() or []:
            lab = (w.field_label or "").lower()
            if "mailed first-class" in lab:
                w.field_value = w.on_state()
                w.update()
            if "not eligible to serve in the u.s. military because" in lab:
                w.field_value = w.on_state()
                w.update()
    off_by_name(
        doc,
        "FormTitle[0].CheckBox12345125q[0]",
        "FormTitle[0].CheckBox12t342563426y[0]",
        "List1[0].Lid[0].CheckBox8[0]",
        "List1[0].Lie[0]",
        "List5[0].CheckBox25[0]",
        "P2Li7f[0]",
        "MPLast[0]",
    )

    if Path(SIGNATURE_PATH).is_file():
        stamp_on_pdf_line(doc[0], 400, 530, 680)
        stamp_on_pdf_line(doc[1], 400, 530, 448)
        stamp_on_pdf_line(doc[2], 400, 530, 698)

    doc.bake(annots=True, widgets=True)
    page3 = doc[2]
    page3.draw_rect(fitz.Rect(0.0, 756.0, 612.0, 792.0), color=(1, 1, 1), fill=(1, 1, 1), width=0)
    if mail_rect is not None:
        page = doc[1]
        page.draw_rect(mail_rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
        y = mail_rect.y0 + 8.0
        for line in target.mail_block.split("\n"):
            page.insert_text(
                (mail_rect.x0 + 1.5, y),
                line,
                fontsize=6.4,
                fontname="helv",
                color=(0, 0, 0),
            )
            y += 8.0
    return doc


HOLD_PATH = REPO / "internal" / "docs" / (
    "HOLD - Request for Default Randstad and RK (do not file until deadline).txt"
)

HOLD_TEXT = """HOLD — RK Logistics CIV-100 only. Randstad default is already entered.

Matter 27 — Newanforbi v. Randstad US, LLC et al., Alameda Super. Ct. No. 26CV199902
Dept. 20, Hon. Thomas Weathers.

Randstad US, LLC — DONE
- CIV-100 (item 1c only) Electronically Received 09/16/2026 06:28 AM.
- FILE stamp 09/16/2026, Deputy S. Pesko. Default ENTERED as requested on 09/16/2026.
- No clerk's judgment. No court judgment. No item 2 money.
- CRC 3.110(h): obtain a default judgment within 45 days of entry
  (Oct. 31, 2026; CCP §12a to Mon. Nov. 2 if the clerk is closed Saturday).
- Same-day CCP §587 mailing was declared to Williams and CSC. Mail the copies
  if that has not already gone out.

The RK Logistics Group, Inc. — still HOLD
- Do not e-file the RK CIV-100 until eCourt shows no accepted CIV-141, answer,
  demurrer, motion to strike, or stipulation. Tai served Gurney's CIV-141 on
  Sept. 14; the served copy had no clerk stamp.
- Prepared papers remain dated September 15, 2026.
- Same-day mailing if filed: Melinda Garcia, Garcia & Gurney, ALC, 6600 Koll
  Center Parkway, Suite 200, Pleasanton, CA 94566; and RK c/o CSC - Lawyers
  Incorporating Service, 2710 Gateway Oaks Drive, Suite 150N, Sacramento,
  CA 95833.

Do not attach the 425.115 notices to a clerk-default CIV-100. The amended
notices were personally served August 21, 2026; POS-040s filed September 9.

Files
- internal/public/documents/matter-27/CIV-100 Request for Entry of Default - Randstad US LLC (Default Entered, Filed Sep 16 2026).pdf
- internal/public/documents/matter-27/CIV-100 Request for Entry of Default - RK Logistics Group Inc (Clerk Default Only, Sep 15 2026).pdf
"""


def main() -> None:
    if FILED_STATUS:
        raise SystemExit("Flip FILED_STATUS only after the clerk enters default.")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    HOLD_PATH.write_text(HOLD_TEXT)
    print(f"Wrote {HOLD_PATH.relative_to(REPO)}")
    for target in (RK,):
        doc = fill_civ100(target)
        out = OUT_DIR / target.out_name
        tmp = out.with_suffix(out.suffix + ".tmp")
        doc.save(str(tmp), garbage=4, deflate=True)
        doc.close()
        tmp.replace(out)
        text = fitz.open(out)
        body = "\n".join(page.get_text() for page in text)
        text.close()
        checks = {
            "Entry of Default": "Entry of Default" in body or "ENTRY OF DEFAULT" in body,
            "as-sued name": target.as_sued.split(",")[0][:20] in body,
            "no court judgment request": "I request a court judgment" not in body
            or "Enter default of defendant" in body,
            "date": target.date_short in body or target.date_long in body,
            "CSC": "2710 Gateway Oaks" in body,
        }
        print(f"Wrote {out.relative_to(REPO)} ({out.stat().st_size} bytes)")
        for label, ok in checks.items():
            print(f"  {label}: {ok}")
        if "Court Judgment" in body and "Enter default of defendant" not in body:
            raise SystemExit("CIV-100 did not check clerk default")


if __name__ == "__main__":
    main()
