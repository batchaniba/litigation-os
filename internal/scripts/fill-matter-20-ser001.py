#!/usr/bin/env python3
"""Fill four Matter 20 SER-001 forms (one per named respondent).

Service target matches the July 31, 2026 Proof of Service on the Opposition
to Individual Respondents' Demurrers: Alameda County Sheriff Civil Section
mail service on Deputy AG Vanessa Ing at the SF AG office, under Petitioner's
fee waiver (Gov. Code §26721). SER-001 requires a separate form per person/
entity served.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "internal/public/documents/_form-library/ser001-blank-template.pdf"
OUT_DIR = ROOT / "internal/public/documents/matter-20"

CASE_NUMBER = "26CV191136"
COUNTY = "Alameda"
YOUR_NAME = "Brendan Ngehsi Newanforbi"
CASE_NAME = "Newanforbi v. California Highway Patrol, et al."
ADDRESS = "1090 S Milpitas Blvd, Unit #304"
CITY = "Milpitas"
STATE = "CA"
ZIP = "95035"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

AG_ADDRESS = "455 Golden Gate Avenue, Suite 11000"
AG_CITY = "San Francisco"
AG_STATE = "CA"
AG_ZIP = "94102-7004"
AG_AGENT = "Vanessa Ing, Deputy Attorney General"
SERVE_TIME = "Mail — business hours"

TYPE_PAPERS = "Opposition to Demurrers and Joinders (subsequent papers)"
LIST_FORMS = (
    "Petitioner's Opposition to Individual Respondents' Demurrers and "
    "Joinders to Respondent CHP's Demurrer; Memorandum of Points and Authorities "
    "(dated July 31, 2026)"
)
# hearingDate widget is ~202pt wide — keep short
HEARING_DATE = "08/28/2026, 9:00 a.m., Dept. 25"
DEADLINE_DATE = "08/21/2026 (before hearing)"
SIG_DATE = "July 31, 2026"

# Fully-qualified AcroForm names on the Judicial Council SER-001 (Rev. Jan 1, 2026)
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
    "serve_person": "SER-001[0].Page2[0].List3[0].Li3a[0].servePerson[0]",
    "person_name": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a1[0].personName[0]",
    "nicknames": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a1[0].nicknames[0]",
    "desc_no": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a3[0].Description[0]",
    "safety_no": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a4[0].SafetyAccessibility[0]",
    "serve_entity": "SER-001[0].Page2[0].List3[0].Li3b[0].servePerson[0]",
    "entity_name": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b1[0].NameType[0]",
    "entity_person": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b2[0].nameofperson[0]",
    "entity_agent": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b3[0].nameofagent[0]",
    "case2": "SER-001[0].Page2[0].PxCaption[0].CaseNumber[0]",
    "addr": "SER-001[0].Page3[0].List4[0].Li4[0].Address[0]",
    "addr_city": "SER-001[0].Page3[0].List4[0].Li4[0].City[0]",
    "addr_state": "SER-001[0].Page3[0].List4[0].Li4[0].State[0]",
    "addr_zip": "SER-001[0].Page3[0].List4[0].Li4[0].Zip[0]",
    "home": "SER-001[0].Page3[0].List4[0].Li4[0].addDef[0]",
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


def base_fields(other_info: str) -> dict[str, object]:
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
        F["addr"]: AG_ADDRESS,
        F["addr_city"]: AG_CITY,
        F["addr_state"]: AG_STATE,
        F["addr_zip"]: AG_ZIP,
        F["business"]: NameObject("/2"),
        F["serve_time"]: SERVE_TIME,
        # gateCode widget is ~362pt — keep short; detail goes in item 5f
        F["gate"]: "MAIL on counsel; fee waiver (Gov. Code §26721)",
        F["type_papers"]: TYPE_PAPERS,
        F["list_forms"]: LIST_FORMS,
        F["hearing_yes"]: NameObject("/3"),
        F["hearing_date"]: HEARING_DATE,
        F["case3"]: CASE_NUMBER,
        F["deadline_yes"]: NameObject("/3"),
        F["deadline_date"]: DEADLINE_DATE,
        F["alt_no"]: NameObject("/2"),
        F["oth_yes"]: NameObject("/2"),
        F["oth_text"]: other_info,
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
        "entity_name": "California Highway Patrol (state agency)",
        "entity_person": "Vanessa Ing, Deputy Attorney General",
        "entity_agent": AG_AGENT,
        "other": (
            "Request MAIL service (not personal) under Petitioner's court fee waiver "
            "(Gov. Code §26721) via Alameda County Sheriff Civil Section, "
            "1225 Fallon Street, #104, Oakland, CA 94612. "
            "Serve counsel of record for Respondent California Highway Patrol: "
            "Vanessa Ing, DAG, Office of the Attorney General, at the address in item 4. "
            "Separate SER-001s are submitted for co-respondents Serrato, Paul, and Dutra "
            "(same counsel/address)."
        ),
    },
    {
        "slug": "G. Serrato",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "G Serrato (Jul 31 2026).pdf"
        ),
        "kind": "person",
        "person_name": "G. Serrato (Gerardo Serrato)",
        "nicknames": "Capt./Cmdr., CHP Dublin — via counsel of record",
        "other": (
            "Request MAIL service (not personal) under Petitioner's court fee waiver "
            "(Gov. Code §26721) via Alameda County Sheriff Civil Section, "
            "1225 Fallon Street, #104, Oakland, CA 94612. "
            "Serve counsel of record for Respondent G. Serrato (Gerardo Serrato): "
            "Vanessa Ing, DAG, Office of the Attorney General, at the address in item 4. "
            "Separate SER-001s are submitted for co-respondents CHP, Paul, and Dutra "
            "(same counsel/address)."
        ),
    },
    {
        "slug": "Gary Paul",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Gary Paul (Jul 31 2026).pdf"
        ),
        "kind": "person",
        "person_name": "Gary Paul",
        "nicknames": "Lt., CHP Dublin — via counsel of record",
        "other": (
            "Request MAIL service (not personal) under Petitioner's court fee waiver "
            "(Gov. Code §26721) via Alameda County Sheriff Civil Section, "
            "1225 Fallon Street, #104, Oakland, CA 94612. "
            "Serve counsel of record for Respondent Gary Paul: "
            "Vanessa Ing, DAG, Office of the Attorney General, at the address in item 4. "
            "Separate SER-001s are submitted for co-respondents CHP, Serrato, and Dutra "
            "(same counsel/address)."
        ),
    },
    {
        "slug": "Eric Dutra",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Eric Dutra (Jul 31 2026).pdf"
        ),
        "kind": "person",
        "person_name": "Eric Dutra",
        "nicknames": "Sgt., CHP Dublin — via counsel of record",
        "other": (
            "Request MAIL service (not personal) under Petitioner's court fee waiver "
            "(Gov. Code §26721) via Alameda County Sheriff Civil Section, "
            "1225 Fallon Street, #104, Oakland, CA 94612. "
            "Serve counsel of record for Respondent Eric Dutra: "
            "Vanessa Ing, DAG, Office of the Attorney General, at the address in item 4. "
            "Separate SER-001s are submitted for co-respondents CHP, Serrato, and Paul "
            "(same counsel/address)."
        ),
    },
]


def fields_for(respondent: dict) -> dict[str, object]:
    fields = base_fields(respondent["other"])
    if respondent["kind"] == "entity":
        fields[F["serve_entity"]] = NameObject("/2")
        fields[F["entity_name"]] = respondent["entity_name"]
        fields[F["entity_person"]] = respondent["entity_person"]
        fields[F["entity_agent"]] = respondent["entity_agent"]
    else:
        fields[F["serve_person"]] = NameObject("/1")
        fields[F["person_name"]] = respondent["person_name"]
        fields[F["nicknames"]] = respondent["nicknames"]
        fields[F["desc_no"]] = NameObject("/1")
        fields[F["safety_no"]] = NameObject("/1")
    return fields


def fill_one(respondent: dict) -> Path:
    out_path = OUT_DIR / respondent["filename"]
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, fields_for(respondent))
    # Keep fields visible/editable for review & wet/e-signature
    if writer.get_fields():
        try:
            writer.set_need_appearances_writer(True)
        except Exception:
            pass
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def verify(path: Path) -> None:
    fields = PdfReader(str(path)).get_fields() or {}
    filled = {
        k: v.get("/V")
        for k, v in fields.items()
        if v.get("/V") not in (None, "", NameObject("/Off"), "/Off")
    }
    print(f"{path.name}: {len(filled)} filled fields")
    for key in (
        F["county"],
        F["yourname"],
        F["person_name"],
        F["entity_name"],
        F["addr"],
        F["hearing_date"],
        F["sig_date"],
    ):
        short = key.split(".")[-1]
        if key in filled:
            print(f"  {short}: {filled[key]!r}")


def main() -> None:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Touch template size sanity (reject LFS pointer)
    if TEMPLATE.stat().st_size < 10_000:
        raise SystemExit(f"Template looks like an LFS pointer ({TEMPLATE.stat().st_size} bytes)")
    for respondent in RESPONDENTS:
        path = fill_one(respondent)
        verify(path)
    print("Done.")


if __name__ == "__main__":
    main()
