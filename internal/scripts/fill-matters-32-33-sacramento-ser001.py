#!/usr/bin/env python3
"""Fill three Sacramento County SER-001 forms — Matters 32 and 33.

Both N.D. Cal. actions were docketed Aug. 10, 2026 and neither Defendant
has been served (Fed. R. Civ. P. 4(m) deadline computed as Nov. 8, 2026 —
90 days from docketing — for both cases). Of the four named Defendants,
three currently have a Sacramento County service address:

- Jose Melano (Matter 32, 3:26-cv-08271-PHK) — CHP South Sacramento Area,
  his current duty station (not the Nov. 1, 2024 Dublin assignment pleaded
  in the Complaint).
- Diana Candelaria and Steve Gordon (Matter 33, 3:26-cv-08272-LJC) — both
  served via DMV Legal Affairs Division, Mail Station C128.

Co-Defendant Santiago Meza-Gonzalez (Matter 32) is served at CHP Modesto
Area — Stanislaus County — and is out of scope for this Sacramento batch.

No CA state-court fee waiver applies to either federal action; the sheriff's
civil service fee must accompany each request.
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

YOUR_NAME = "Brendan Ngwa Nforbi"
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

SERVE_TIME = "8:00 a.m.–5:00 p.m. (business hours)"
TYPE_PAPERS = "Summons and Complaint (Fed. R. Civ. P. 4)"
SIG_DATE = "8/13/2026"

DMV_LEGAL_AFFAIRS_GATE = (
    "California DMV, Legal Affairs Division, Mail Station C128, "
    "2415 First Avenue — attn: {who}"
)

FEE_NOTE = (
    "No California state-court fee waiver applies to this federal action "
    "(filing fee paid, not waived); enclose the Sacramento County Sheriff's "
    "civil service fee per its published fee schedule with this request."
)


def base_fields(r: dict) -> dict[str, object]:
    return {
        F["case1"]: r["case_number"],
        F["county"]: "Sacramento",
        F["yourname"]: YOUR_NAME,
        F["casename"]: r["case_name"],
        F["address"]: ADDRESS,
        F["city"]: CITY,
        F["state"]: STATE,
        F["zip"]: ZIP,
        F["phone"]: PHONE,
        F["email"]: EMAIL,
        F["serve_person"]: NameObject("/1"),
        F["person_name"]: r["person_name"],
        F["nicknames"]: r["nicknames"],
        F["desc_no"]: NameObject("/1"),
        F["safety_no"]: NameObject("/1"),
        F["case2"]: r["case_number"],
        F["addr"]: r["serve_address"],
        F["addr_city"]: "Sacramento",
        F["addr_state"]: "CA",
        F["addr_zip"]: r["serve_zip"],
        F["business"]: NameObject("/2"),
        F["serve_time"]: SERVE_TIME,
        F["gate"]: r["gate"],
        F["type_papers"]: TYPE_PAPERS,
        F["list_forms"]: r["list_forms"],
        F["hearing_yes"]: NameObject("/3"),
        F["hearing_date"]: r["hearing_date"],
        F["case3"]: r["case_number"],
        F["deadline_yes"]: NameObject("/3"),
        F["deadline_date"]: r["deadline_date"],
        F["alt_no"]: NameObject("/2"),
        F["oth_yes"]: NameObject("/2"),
        F["oth_text"]: r["other"],
        F["case4"]: r["case_number"],
        F["sig_date"]: SIG_DATE,
        F["type_name"]: YOUR_NAME,
        F["case5"]: r["case_number"],
    }


MATTER32_CASE = "3:26-cv-08271-PHK"
MATTER32_NAME = "Ngwa Nforbi v. Meza-Gonzalez, et al."
MATTER32_HEARING = (
    "12/02/2026, 11:00 a.m., Courtroom F, 450 Golden Gate Ave., San Francisco "
    "(Initial Case Management Conference, Dkt. 4)"
)
MATTER32_DEADLINE = (
    "08/21/2026 (requested; Rule 4(m) deadline 11/08/2026)"
)
MATTER32_FORMS = (
    "AO 440 Summons issued to Jose Melano (Dkt. 3, Aug. 10, 2026); "
    "Complaint (Dkt. 1, Aug. 10, 2026); Dkt. 1-1 Civil Filing Fee Receipt; "
    "Dkt. 1-2 JS-CAND 44 Civil Cover Sheet; Dkt. 4 Order Setting Initial "
    "Case Management Conference and ADR Deadlines"
)

MATTER33_CASE = "3:26-cv-08272-LJC"
MATTER33_NAME = "Nforbi v. Candelaria et al."
MATTER33_HEARING = (
    "11/12/2026, 1:30 p.m., by Zoom (cand.uscourts.gov/ljc) before Magistrate "
    "Judge Lisa J. Cisneros (Initial Case Management Conference, Dkt. 4)"
)
MATTER33_DEADLINE = (
    "08/21/2026 (requested; Rule 4(m) deadline 11/08/2026)"
)
MATTER33_FORMS_TEMPLATE = (
    "AO 440 Summons issued to {who} (Dkt. 2, Aug. 10, 2026); Complaint "
    "(Dkt. 1, Aug. 10, 2026); Dkt. 4 Order Setting Initial Case Management "
    "Conference and ADR Deadlines"
)

RESPONDENTS = [
    {
        "slug": "Jose Melano",
        "out_dir": ROOT / "internal/public/documents/matter-32/ndcal",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Jose Melano (Sacramento, Aug 13 2026).pdf"
        ),
        "case_number": MATTER32_CASE,
        "case_name": MATTER32_NAME,
        "person_name": "Jose Melano (CHP Badge #023054)",
        "nicknames": "Officer, CHP South Sacramento Area",
        "serve_address": "6 Massie Court",
        "serve_zip": "95823",
        "gate": "California Highway Patrol, South Sacramento Area — official duty station",
        "list_forms": MATTER32_FORMS,
        "hearing_date": MATTER32_HEARING,
        "deadline_date": MATTER32_DEADLINE,
        "other": (
            "Serve at Respondent's current duty station (CHP South Sacramento "
            "Area) — not the CHP Dublin Area station pleaded in the Complaint "
            "for the Nov. 1, 2024 incident, which is in Alameda County. "
            f"{FEE_NOTE} Co-Defendant Santiago Meza-Gonzalez is served under a "
            "separate SER-001 at CHP Modesto Area (Stanislaus County Sheriff), "
            "outside this Sacramento batch."
        ),
    },
    {
        "slug": "Diana Candelaria",
        "out_dir": ROOT / "internal/public/documents/matter-33/ndcal",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Diana Candelaria (Sacramento, Aug 13 2026).pdf"
        ),
        "case_number": MATTER33_CASE,
        "case_name": MATTER33_NAME,
        "person_name": "Diana Candelaria",
        "nicknames": "Driver Safety Hearing Officer, California DMV",
        "serve_address": "2415 First Avenue",
        "serve_zip": "95818",
        "gate": DMV_LEGAL_AFFAIRS_GATE.format(who="Diana Candelaria"),
        "list_forms": MATTER33_FORMS_TEMPLATE.format(who="Diana Candelaria"),
        "hearing_date": MATTER33_HEARING,
        "deadline_date": MATTER33_DEADLINE,
        "other": (
            "The Complaint gives no office address for Respondent (her Jan. 24, "
            "2025 APS hearing was conducted remotely); serve care of DMV Legal "
            "Affairs Division, the DMV's published address for service on "
            f"Department personnel. {FEE_NOTE} Co-Defendant Steve Gordon "
            "(Director, official capacity) is served under a separate SER-001 "
            "at the same DMV Legal Affairs address."
        ),
    },
    {
        "slug": "Steve Gordon",
        "out_dir": ROOT / "internal/public/documents/matter-33/ndcal",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Steve Gordon (Sacramento, Aug 13 2026).pdf"
        ),
        "case_number": MATTER33_CASE,
        "case_name": MATTER33_NAME,
        "person_name": "Steve Gordon",
        "nicknames": "Director, California DMV (sued in his official capacity)",
        "serve_address": "2415 First Avenue",
        "serve_zip": "95818",
        "gate": DMV_LEGAL_AFFAIRS_GATE.format(who="Director Steve Gordon"),
        "list_forms": MATTER33_FORMS_TEMPLATE.format(who="Steve Gordon"),
        "hearing_date": MATTER33_HEARING,
        "deadline_date": MATTER33_DEADLINE,
        "other": (
            "Respondent is sued in his official capacity as DMV Director; serve "
            "care of DMV Legal Affairs Division, the DMV's published address for "
            f"service on Department personnel. {FEE_NOTE} Co-Defendant Diana "
            "Candelaria (individual capacity) is served under a separate SER-001 "
            "at the same DMV Legal Affairs address."
        ),
    },
]


def fill_one(respondent: dict) -> Path:
    out_dir = respondent["out_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    return fill_ser001(out_dir / respondent["filename"], base_fields(respondent), stamp_signature=True)


def verify(path: Path) -> None:
    filled = filled_values(path)
    print(f"{path.name}: {len(filled)} filled fields")
    for key in (F["county"], F["casename"], F["person_name"], F["addr"], F["addr_zip"], F["gate"]):
        short = key.split(".")[-1]
        if key in filled:
            print(f"  {short}: {filled[key]!r}")
    doc = fitz.open(path)
    try:
        images = doc[SER001_SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(images)} (signature stamped)")
    finally:
        doc.close()


def main() -> None:
    require_template()
    for respondent in RESPONDENTS:
        path = fill_one(respondent)
        verify(path)
    print("Done.")


if __name__ == "__main__":
    main()
