#!/usr/bin/env python3
"""Fill two Matter 12 SER-001 forms for Stanislaus County Sheriff Civil.

HISTORICAL — August 3, 2026 CCP §425.115 punitive-notice service only.
Do not reuse these packets to re-serve the Amended Summons / FAC.

As of the August 28, 2026 SOS bizfile printouts:
  - Diamond agent: Saliman Osmani, 1201 S. Soderquist Road, Turlock (Stanislaus).
  - Alpine agent: Sheran Osmani, 7156 Golden State Highway, Bakersfield (Kern).
Alpine's summons re-service is Kern County, not Turlock.
"""

from __future__ import annotations

import sys
from pathlib import Path

import fitz
from pypdf.generic import NameObject

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from ser001 import FIELDS as F, fill_ser001, filled_values, require_template  # noqa: E402
from signature_stamp import SER001_SIG_PAGE_INDEX  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "internal/public/documents/matter-12"

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
    return fill_ser001(OUT_DIR / defendant["filename"], fields_for(defendant), stamp_signature=True)


def verify(path: Path) -> None:
    filled = filled_values(path)
    print(f"{path.name}: {len(filled)} filled fields")
    for key in (F["county"], F["entity_name"], F["addr"], F["addr_city"], F["sig_date"], F["type_papers"]):
        if key in filled:
            print(f"  {key.split('.')[-1]}: {filled[key]!r}")
    # Confirm an image XObject landed on the signature page.
    doc = fitz.open(path)
    try:
        xobjects = doc[SER001_SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(xobjects)} (signature stamped)")
    finally:
        doc.close()


def main() -> None:
    require_template()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for defendant in DEFENDANTS:
        verify(fill_one(defendant))
    print("Done.")


if __name__ == "__main__":
    main()
