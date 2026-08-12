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
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "internal/public/documents/_form-library/ser001-blank-template.pdf"

# Page-4 right-hand "Sign your name" line (PyMuPDF top-origin coords) —
# same placement used for the Matter 12 and Matters 25/26/27/29 SER-001s.
SIG_PAGE_INDEX = 3
SIG_WIDTH = 120.0
SIG_HEIGHT = SIG_WIDTH * SIGNATURE_ASPECT
SIG_BASELINE = 645.0
SIG_RECT = fitz.Rect(360.0, SIG_BASELINE - SIG_HEIGHT, 360.0 + SIG_WIDTH, SIG_BASELINE)

YOUR_NAME = "Brendan Ngwa Nforbi"
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

SERVE_TIME = "8:00 a.m.–5:00 p.m. (business hours)"
TYPE_PAPERS = "Summons and Complaint (Fed. R. Civ. P. 4)"
SIG_DATE = "August 12, 2026"

DMV_LEGAL_AFFAIRS_GATE = (
    "California DMV, Legal Affairs Division, Mail Station C128, "
    "2415 First Avenue — attn: {who}"
)

FEE_NOTE = (
    "No California state-court fee waiver applies to this federal action "
    "(filing fee paid, not waived); enclose the Sacramento County Sheriff's "
    "civil service fee per its published fee schedule with this request."
)

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
            "Jose Melano (Sacramento, Aug 12 2026).pdf"
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
            "Diana Candelaria (Sacramento, Aug 12 2026).pdf"
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
            "Steve Gordon (Sacramento, Aug 12 2026).pdf"
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
    out_path = out_dir / respondent["filename"]
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, base_fields(respondent))
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
    """Stamp the portfolio's canonical e-signature on page 4's signature line."""
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    doc = fitz.open(path)
    try:
        page = doc[SIG_PAGE_INDEX]
        page.insert_image(SIG_RECT, filename=SIGNATURE_PATH, keep_proportion=True)
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
    for key in (F["county"], F["casename"], F["person_name"], F["addr"], F["addr_zip"], F["gate"]):
        short = key.split(".")[-1]
        if key in filled:
            print(f"  {short}: {filled[key]!r}")
    doc = fitz.open(path)
    try:
        images = doc[SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(images)} (signature stamped)")
    finally:
        doc.close()


def main() -> None:
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    if TEMPLATE.stat().st_size < 10_000:
        raise SystemExit(f"Template looks like an LFS pointer ({TEMPLATE.stat().st_size} bytes)")
    for respondent in RESPONDENTS:
        path = fill_one(respondent)
        verify(path)
    print("Done.")


if __name__ == "__main__":
    main()
