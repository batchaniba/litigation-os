#!/usr/bin/env python3
"""Fill two Matter 12 SER-001 forms for Stanislaus County Sheriff Civil.

Serve each named defendant at 1201 S Soderquist Road, Turlock, CA 95380
with the CCP §425.115 Notice of Amount of Punitive Damages Sought
(execution date August 3, 2026).
"""

from __future__ import annotations

from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "internal/public/documents/_form-library/ser001-blank-template.pdf"
OUT_DIR = ROOT / "internal/public/documents/matter-12"
SIGNATURE_IMG = Path(__file__).resolve().parent / "assets" / "newanforbi-pen-signature.png"
# Page-4 right-hand "Sign your name" line (PyMuPDF top-origin coords).
# Sized large so the pen stroke reads clearly on the Judicial Council form.
SIG_PAGE_INDEX = 3
SIG_WIDTH = 120.0
# Sit on the right-hand signature line above "Sign your name".
SIG_HEIGHT = SIG_WIDTH * (101.0 / 369.0)
SIG_BASELINE = 645.0  # just above the "Sign your name" label
SIG_RECT = fitz.Rect(360.0, SIG_BASELINE - SIG_HEIGHT, 360.0 + SIG_WIDTH, SIG_BASELINE)

CASE_NUMBER = "STK-CV-UF-2026-0001094"
COUNTY = "Stanislaus"
YOUR_NAME = "Brendan Ngwa Nforbi"
CASE_NAME = "Ngwa Nforbi v. Diamond Truck Sales, Inc., et al."
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

SERVE_ADDRESS = "1201 S Soderquist Road"
SERVE_CITY = "Turlock"
SERVE_ZIP = "95380"
SERVE_TIME = "8:00 a.m.–5:00 p.m. (business hours)"
GATE = "Truck sales lot — ask for manager / authorized agent"

TYPE_PAPERS = "Notice of Amount of Punitive Damages Sought (CCP §425.115)"
LIST_FORMS = (
    "Notice of Amount of Punitive Damages Sought "
    "(Code Civ. Proc. § 425.115; Civ. Code § 3294) — $25,000.00 "
    "(dated August 3, 2026)"
)
HEARING_DATE = "08/12/2026, 8:30 a.m., Dept. 11B"
DEADLINE_DATE = "08/11/2026 (before prove-up)"
SIG_DATE = "August 3, 2026"

F = {
    "case1": "SER-001[0].Page1[0].CaptionRight[0].CaseNo[0].CaseNumber[0]",
    "county": "SER-001[0].Page1[0].List1[0].Li1[0].NameofCounty[0]",
    "yourname": "SER-001[0].Page1[0].List2[0].Li2a[0].Yourname[0]",
    "casename": "SER-001[0].Page1[0].List2[0].Li2c[0].TextField[0]",
    "address": "SER-001[0].Page1[0].List2[0].Li2d[0].address\\.2d[0]",
    "city": "SER-001[0].Page1[0].List2[0].Li2d[0].city\\.2d[0]",
    "state": "SER-001[0].Page1[0].List2[0].Li2d[0].state\\.2d[0]",
    "zip": "SER-001[0].Page1[0].List2[0].Li2d[0].zip\\.2d[0]",
    "phone": "SER-001[0].Page1[0].List2[0].Li2d[0].telephone\\.2d[0]",
    "email": "SER-001[0].Page1[0].List2[0].Li2d[0].email\\.2d[0]",
    "serve_entity": "SER-001[0].Page2[0].List3[0].Li3b[0].servePerson[0]",
    "entity_name": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b1[0].NameType[0]",
    "entity_person": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b2[0].nameofperson[0]",
    "entity_agent": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b3[0].nameofagent[0]",
    "case2": "SER-001[0].Page2[0].PxCaption[0].CaseNumber[0]",
    "addr": "SER-001[0].Page3[0].List4[0].Li4[0].Address[0]",
    "addr_city": "SER-001[0].Page3[0].List4[0].Li4[0].City[0]",
    "addr_state": "SER-001[0].Page3[0].List4[0].Li4[0].State[0]",
    "addr_zip": "SER-001[0].Page3[0].List4[0].Li4[0].Zip[0]",
    "business": "SER-001[0].Page3[0].List4[0].Li4[0].addDef[1]",
    "serve_time": "SER-001[0].Page3[0].List4[0].Li4[0].serveTime[0]",
    "gate": "SER-001[0].Page3[0].List4[0].Li4[0].gateCode[0]",
    "type_papers": "SER-001[0].Page3[0].List5[0].Li5a[0].typePapers[0]",
    "list_forms": "SER-001[0].Page3[0].List5[0].Li5b[0].listForms[0]",
    "hearing_yes": "SER-001[0].Page3[0].List5[0].Li5c[0].Hearing[2]",
    "hearing_date": "SER-001[0].Page3[0].List5[0].Li5c[0].hearingDate[0]",
    "case3": "SER-001[0].Page3[0].PxCaption[0].CaseNumber[0]",
    "deadline_yes": "SER-001[0].Page4[0].List5Continued[0].Li5d[0].deadline[2]",
    "deadline_date": "SER-001[0].Page4[0].List5Continued[0].Li5d[0].deadlineDate[0]",
    "alt_no": "SER-001[0].Page4[0].List5Continued[0].Li5e[0].altService[1]",
    "oth_yes": "SER-001[0].Page4[0].List5Continued[0].Li5f[0].othInfo[1]",
    "oth_text": "SER-001[0].Page4[0].List5Continued[0].Li5f[0].TextField[0]",
    "case4": "SER-001[0].Page4[0].PxCaption[0].CaseNumber[0]",
    "sig_date": "SER-001[0].Page4[0].sig[0].SigDate[0]",
    "type_name": "SER-001[0].Page4[0].sig[0].typeName[0]",
    "case5": "SER-001[0].Page5[0].PxCaption[0].CaseNumber[0]",
}


def base_fields(other: str) -> dict[str, object]:
    return {
        F["case1"]: CASE_NUMBER,
        F["county"]: COUNTY,
        F["yourname"]: YOUR_NAME,
        F["casename"]: CASE_NAME,
        F["address"]: ADDRESS,
        F["city"]: CITY,
        F["state"]: STATE,
        F["zip"]: ZIP,
        F["phone"]: PHONE,
        F["email"]: EMAIL,
        F["case2"]: CASE_NUMBER,
        F["addr"]: SERVE_ADDRESS,
        F["addr_city"]: SERVE_CITY,
        F["addr_state"]: "CA",
        F["addr_zip"]: SERVE_ZIP,
        F["business"]: NameObject("/2"),
        F["serve_time"]: SERVE_TIME,
        F["gate"]: GATE,
        F["type_papers"]: TYPE_PAPERS,
        F["list_forms"]: LIST_FORMS,
        F["hearing_yes"]: NameObject("/3"),
        F["hearing_date"]: HEARING_DATE,
        F["case3"]: CASE_NUMBER,
        F["deadline_yes"]: NameObject("/3"),
        F["deadline_date"]: DEADLINE_DATE,
        F["alt_no"]: NameObject("/2"),
        F["oth_yes"]: NameObject("/2"),
        F["oth_text"]: other,
        F["case4"]: CASE_NUMBER,
        F["sig_date"]: SIG_DATE,
        F["type_name"]: YOUR_NAME,
        F["case5"]: CASE_NUMBER,
        F["serve_entity"]: NameObject("/2"),
    }


DEFENDANTS = [
    {
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Diamond Truck Sales (Stanislaus, Aug 3 2026).pdf"
        ),
        "entity_name": "Diamond Truck Sales, Inc., a California corporation",
        "entity_person": "Mustaqem Usmani, Manager (or person authorized to accept)",
        "entity_agent": "",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Stanislaus County Sheriff Civil "
            "Division for personal service at the address in item 4. "
            "Plaintiff has a court fee waiver in this action (FW-003) — no sheriff "
            "service fee (Gov. Code §26721). "
            "A separate SER-001 is submitted for co-defendant Alpine Truck Sales, Inc. "
            "(same address). Hearing / prove-up: August 12, 2026, 8:30 a.m., Dept. 11B, "
            "Hon. Robert T. Waters, San Joaquin Superior Court."
        ),
    },
    {
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Alpine Truck Sales (Stanislaus, Aug 3 2026).pdf"
        ),
        "entity_name": (
            "Alpine Truck Sales, Inc., a California corporation "
            "(successor/alter ego of Diamond Truck Sales, Inc.)"
        ),
        "entity_person": "Mustaqem Usmani, Manager (or person authorized to accept)",
        "entity_agent": "",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Stanislaus County Sheriff Civil "
            "Division for personal service at the address in item 4 "
            "(same location where Alpine was previously served July 1, 2026 — "
            "Levying Officer File No. 2026002577). "
            "Plaintiff has a court fee waiver in this action (FW-003) — no sheriff "
            "service fee (Gov. Code §26721). "
            "A separate SER-001 is submitted for co-defendant Diamond Truck Sales, Inc. "
            "(same address). Hearing / prove-up: August 12, 2026, 8:30 a.m., Dept. 11B, "
            "Hon. Robert T. Waters, San Joaquin Superior Court."
        ),
    },
]


def fields_for(defendant: dict) -> dict[str, object]:
    fields = base_fields(defendant["other"])
    fields[F["entity_name"]] = defendant["entity_name"]
    fields[F["entity_person"]] = defendant["entity_person"]
    if defendant.get("entity_agent"):
        fields[F["entity_agent"]] = defendant["entity_agent"]
    return fields


def fill_one(defendant: dict) -> Path:
    out_path = OUT_DIR / defendant["filename"]
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, fields_for(defendant))
    if writer.get_fields():
        try:
            writer.set_need_appearances_writer(True)
        except Exception:
            pass
    with open(out_path, "wb") as fh:
        writer.write(fh)
    affix_signature(out_path)
    return out_path


def affix_signature(path: Path) -> None:
    """Stamp pen signature large on page 4's right-hand signature line."""
    if not SIGNATURE_IMG.is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_IMG}")
    doc = fitz.open(path)
    try:
        page = doc[SIG_PAGE_INDEX]
        page.insert_image(SIG_RECT, filename=str(SIGNATURE_IMG), keep_proportion=True)
        doc.saveIncr()
    finally:
        doc.close()


def verify(path: Path) -> None:
    fields = PdfReader(str(path)).get_fields() or {}
    filled = {
        k: v.get("/V")
        for k, v in fields.items()
        if v.get("/V") not in (None, "", NameObject("/Off"), "/Off")
    }
    print(f"{path.name}: {len(filled)} filled fields")
    for key in (F["county"], F["entity_name"], F["addr"], F["addr_city"], F["sig_date"], F["type_papers"]):
        if key in filled:
            print(f"  {key.split('.')[-1]}: {filled[key]!r}")
    # Confirm an image XObject landed on the signature page.
    doc = fitz.open(path)
    try:
        xobjects = doc[SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(xobjects)} (signature stamped)")
    finally:
        doc.close()


def main() -> None:
    if not TEMPLATE.is_file() or TEMPLATE.stat().st_size < 10_000:
        raise SystemExit(f"Bad/missing template: {TEMPLATE}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for defendant in DEFENDANTS:
        verify(fill_one(defendant))
    print("Done.")


if __name__ == "__main__":
    main()
