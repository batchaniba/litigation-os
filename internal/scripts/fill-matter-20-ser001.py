#!/usr/bin/env python3
"""Fill four Matter 20 SER-001 forms (one per named respondent).

- Serrato / Paul / Dutra: serve at CHP Dublin Area duty station
  (4999 Gleason Drive, Dublin — Alameda County); SER-001s go to
  Alameda County Sheriff Civil Division.
- CHP (entity): serve at CHP Headquarters in Sacramento
  (601 North 7th Street); SER-001 goes to Sacramento County Sheriff.
- Courtesy copy of the Opposition already emailed to DAG Vanessa Ing.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf.generic import NameObject

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from ser001 import FIELDS as F, fill_ser001, filled_values, require_template  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "internal/public/documents/matter-32/from-20"

CASE_NUMBER = "26CV191136"
YOUR_NAME = "Brendan Ngehsi Newanforbi"
CASE_NAME = "Newanforbi v. California Highway Patrol, et al."
# Caption / POS address used on the Opposition packet
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

# Petition ¶: CHP Dublin Area Office
DUBLIN_ADDRESS = "4999 Gleason Drive"
DUBLIN_CITY = "Dublin"
DUBLIN_ZIP = "94568"

# CHP Headquarters (Sacramento) — same track as prior CHP entity service
SAC_ADDRESS = "601 North 7th Street"
SAC_CITY = "Sacramento"
SAC_ZIP = "95811"

SERVE_TIME = "8:00 a.m.–5:00 p.m. (business hours)"

TYPE_PAPERS = "Opposition to Demurrers and Joinders (subsequent papers)"
LIST_FORMS = (
    "Petitioner's Opposition to Individual Respondents' Demurrers and "
    "Joinders to Respondent CHP's Demurrer; Memorandum of Points and Authorities "
    "(dated July 31, 2026)"
)
HEARING_DATE = "08/28/2026, 9:00 a.m., Dept. 25"
DEADLINE_DATE = "08/21/2026 (before hearing)"
SIG_DATE = "July 31, 2026"

COURTESY = (
    "Courtesy copy of the Opposition already emailed to counsel of record "
    "(DAG Vanessa Ing). Fee waiver granted — no sheriff service fee "
    "(Gov. Code §26721)."
)

def base_fields(respondent: dict) -> dict[str, object]:
    return {
        F["case1"]: CASE_NUMBER,
        F["county"]: respondent["county"],
        F["yourname"]: YOUR_NAME,
        F["casename"]: CASE_NAME,
        F["address"]: ADDRESS,
        F["city"]: CITY,
        F["state"]: STATE,
        F["zip"]: ZIP,
        F["phone"]: PHONE,
        F["email"]: EMAIL,
        F["case2"]: CASE_NUMBER,
        F["addr"]: respondent["serve_address"],
        F["addr_city"]: respondent["serve_city"],
        F["addr_state"]: "CA",
        F["addr_zip"]: respondent["serve_zip"],
        F["business"]: NameObject("/2"),
        F["serve_time"]: SERVE_TIME,
        F["gate"]: respondent["gate"],
        F["type_papers"]: TYPE_PAPERS,
        F["list_forms"]: LIST_FORMS,
        F["hearing_yes"]: NameObject("/3"),
        F["hearing_date"]: HEARING_DATE,
        F["case3"]: CASE_NUMBER,
        F["deadline_yes"]: NameObject("/3"),
        F["deadline_date"]: DEADLINE_DATE,
        F["alt_no"]: NameObject("/2"),
        F["oth_yes"]: NameObject("/2"),
        F["oth_text"]: respondent["other"],
        F["case4"]: CASE_NUMBER,
        F["sig_date"]: SIG_DATE,
        F["type_name"]: YOUR_NAME,
        F["case5"]: CASE_NUMBER,
    }


RESPONDENTS = [
    {
        "slug": "California Highway Patrol",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "California Highway Patrol (Jul 31 2026).pdf"
        ),
        "kind": "entity",
        "county": "Sacramento",
        "serve_address": SAC_ADDRESS,
        "serve_city": SAC_CITY,
        "serve_zip": SAC_ZIP,
        "gate": "CHP Headquarters — person authorized to accept service",
        "entity_name": "California Highway Patrol (state agency)",
        "entity_person": "Person authorized to accept service",
        "entity_agent": "",
        "other": (
            "Serve Respondent California Highway Patrol at CHP Headquarters "
            "(item 4). Mail/deliver this SER-001 and service packet to the "
            "Sacramento County Sheriff's Office (Civil). "
            f"{COURTESY} Separate SER-001s for Individual Respondents Serrato, "
            "Paul, and Dutra go to Alameda County Sheriff Civil for service at "
            "CHP Dublin Area (4999 Gleason Drive)."
        ),
    },
    {
        "slug": "G. Serrato",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "G Serrato (Jul 31 2026).pdf"
        ),
        "kind": "person",
        "county": "Alameda",
        "serve_address": DUBLIN_ADDRESS,
        "serve_city": DUBLIN_CITY,
        "serve_zip": DUBLIN_ZIP,
        "gate": "CHP Dublin Area Office — official duty station",
        "person_name": "G. Serrato (Gerardo Serrato)",
        "nicknames": "Capt./Commander, CHP Dublin Area",
        "other": (
            "Serve at Respondent's official duty station: CHP Dublin Area Office "
            "(item 4). Mail/deliver this SER-001 and service packet to Alameda "
            "County Sheriff Civil Division, 1225 Fallon Street, #104, Oakland, "
            f"CA 94612. {COURTESY} Separate SER-001s submitted for Paul and Dutra "
            "(same Dublin address); CHP entity SER-001 goes to Sacramento County "
            "Sheriff for service at CHP Headquarters."
        ),
    },
    {
        "slug": "Gary Paul",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Gary Paul (Jul 31 2026).pdf"
        ),
        "kind": "person",
        "county": "Alameda",
        "serve_address": DUBLIN_ADDRESS,
        "serve_city": DUBLIN_CITY,
        "serve_zip": DUBLIN_ZIP,
        "gate": "CHP Dublin Area Office — official duty station",
        "person_name": "Gary Paul",
        "nicknames": "Lieutenant, CHP Dublin Area",
        "other": (
            "Serve at Respondent's official duty station: CHP Dublin Area Office "
            "(item 4). Mail/deliver this SER-001 and service packet to Alameda "
            "County Sheriff Civil Division, 1225 Fallon Street, #104, Oakland, "
            f"CA 94612. {COURTESY} Separate SER-001s submitted for Serrato and "
            "Dutra (same Dublin address); CHP entity SER-001 goes to Sacramento "
            "County Sheriff for service at CHP Headquarters."
        ),
    },
    {
        "slug": "Eric Dutra",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Eric Dutra (Jul 31 2026).pdf"
        ),
        "kind": "person",
        "county": "Alameda",
        "serve_address": DUBLIN_ADDRESS,
        "serve_city": DUBLIN_CITY,
        "serve_zip": DUBLIN_ZIP,
        "gate": "CHP Dublin Area Office — official duty station",
        "person_name": "Eric Dutra",
        "nicknames": "Sergeant, CHP Dublin Area",
        "other": (
            "Serve at Respondent's official duty station: CHP Dublin Area Office "
            "(item 4). Mail/deliver this SER-001 and service packet to Alameda "
            "County Sheriff Civil Division, 1225 Fallon Street, #104, Oakland, "
            f"CA 94612. {COURTESY} Separate SER-001s submitted for Serrato and "
            "Paul (same Dublin address); CHP entity SER-001 goes to Sacramento "
            "County Sheriff for service at CHP Headquarters."
        ),
    },
]


def fields_for(respondent: dict) -> dict[str, object]:
    fields = base_fields(respondent)
    if respondent["kind"] == "entity":
        fields[F["serve_entity"]] = NameObject("/2")
        fields[F["entity_name"]] = respondent["entity_name"]
        fields[F["entity_person"]] = respondent["entity_person"]
        if respondent.get("entity_agent"):
            fields[F["entity_agent"]] = respondent["entity_agent"]
    else:
        fields[F["serve_person"]] = NameObject("/1")
        fields[F["person_name"]] = respondent["person_name"]
        fields[F["nicknames"]] = respondent["nicknames"]
        fields[F["desc_no"]] = NameObject("/1")
        fields[F["safety_no"]] = NameObject("/1")
    return fields


def fill_one(respondent: dict) -> Path:
    return fill_ser001(OUT_DIR / respondent["filename"], fields_for(respondent))


def verify(path: Path) -> None:
    filled = filled_values(path)
    print(f"{path.name}: {len(filled)} filled fields")
    for key in (
        F["county"],
        F["address"],
        F["city"],
        F["person_name"],
        F["entity_name"],
        F["addr"],
        F["addr_city"],
        F["gate"],
    ):
        short = key.split(".")[-1]
        if key in filled:
            print(f"  {short}: {filled[key]!r}")


def main() -> None:
    require_template()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for respondent in RESPONDENTS:
        path = fill_one(respondent)
        verify(path)
    print("Done.")


if __name__ == "__main__":
    main()
