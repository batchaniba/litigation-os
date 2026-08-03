#!/usr/bin/env python3
"""Fill six SER-001 forms to serve the CCP §425.115 punitive-damages
notices drafted for Matters 25, 26, 27, and 29.

Each defendant below was personally served with the summons and
complaint but not with a CCP §425.115 Notice of Amount of Punitive
Damages Sought at that time (see
matters25-26-27-29-ccp-425115-punitive-notices.py, which generated the
six notices this SER-001 batch transmits). Route each SER-001 to the
same county Sheriff Civil Division that handled the original summons/
complaint service for that defendant, directed at the same registered
agent address, so the notice is served before any default is taken.

Matter 29 (Amazon.com Services, LLC / Accurate Background LLC) is a
special case: unlike Matters 25/26/27, the FW-003 fee waiver in that
action was NOT granted -- the court found the request incomplete and
set a hearing for August 18, 2026 on Plaintiff's financial information.
Absent a granted waiver by the time these two SER-001s are actually
submitted, standard Sheriff service fees apply (as Plaintiff already
paid out of pocket, $52.05, for the original Amazon SER-001).
"""

from __future__ import annotations

from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "internal/public/documents/_form-library/ser001-blank-template.pdf"
DOCS_ROOT = ROOT / "internal/public/documents"
SIGNATURE_IMG = Path(__file__).resolve().parent / "assets" / "newanforbi-pen-signature.png"

# Page-4 right-hand "Sign your name" line (PyMuPDF top-origin coords) --
# same placement used for Matter 12's SER-001s.
SIG_PAGE_INDEX = 3
SIG_WIDTH = 120.0
SIG_HEIGHT = SIG_WIDTH * (101.0 / 369.0)
SIG_BASELINE = 645.0
SIG_RECT = fitz.Rect(360.0, SIG_BASELINE - SIG_HEIGHT, 360.0 + SIG_WIDTH, SIG_BASELINE)

YOUR_NAME = "Brendan Ngehsi Newanforbi"
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
SIG_DATE = "August 4, 2026"

TYPE_PAPERS = "Notice of Amount of Punitive Damages Sought (CCP §425.115)"

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


def base_fields(case_number: str, case_name: str, other: str, deadline_date: str) -> dict[str, object]:
    return {
        F["case1"]: case_number,
        F["yourname"]: YOUR_NAME,
        F["casename"]: case_name,
        F["address"]: ADDRESS,
        F["city"]: CITY,
        F["state"]: STATE,
        F["zip"]: ZIP,
        F["phone"]: PHONE,
        F["email"]: EMAIL,
        F["case2"]: case_number,
        F["business"]: NameObject("/2"),
        F["serve_time"]: "Business hours (9:00 a.m.–5:00 p.m.)",
        F["type_papers"]: TYPE_PAPERS,
        F["case3"]: case_number,
        F["deadline_yes"]: NameObject("/3"),
        F["deadline_date"]: deadline_date,
        F["alt_no"]: NameObject("/2"),
        F["oth_yes"]: NameObject("/2"),
        F["oth_text"]: other,
        F["case4"]: case_number,
        F["sig_date"]: SIG_DATE,
        F["type_name"]: YOUR_NAME,
        F["case5"]: case_number,
        F["serve_entity"]: NameObject("/2"),
    }


DEFENDANTS = [
    {
        "matter": 25,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Federal Express Corporation (CCP 425.115 Notice) (Aug 4 2026).pdf",
        "county": "Los Angeles",
        "case_number": "STK-CV-UWT-2026-0009118",
        "case_name": "Newanforbi v. Federal Express Corporation",
        "entity_name": "Federal Express Corporation",
        "entity_person": "Any authorized employee",
        "entity_agent": "Ct Corporation System",
        "addr": "330 N Brand Blvd, Ste 700",
        "addr_city": "Glendale",
        "addr_zip": "91203",
        "list_forms": (
            "Notice of Amount of Punitive Damages Sought "
            "(Code Civ. Proc. § 425.115; Civ. Code § 3294) — $25,000.00 "
            "(dated August 4, 2026)"
        ),
        "deadline_date": "09/13/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Los Angeles County Sheriff Civil "
            "Division for personal service on Federal Express Corporation's "
            "registered agent at the address in item 4 — the same registered "
            "agent through which the Summons and Complaint were served July 24, "
            "2026 (File No. 2026075280). Plaintiff has a court fee waiver in "
            "this action (FW-003 GRANTED July 15, 2026) — no sheriff service "
            "fee (Gov. Code §26721)."
        ),
    },
    {
        "matter": 26,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - United Parcel Service Inc (CCP 425.115 Notice) (Aug 4 2026).pdf",
        "county": "Sacramento",
        "case_number": "STK-CV-UWT-2026-0009113",
        "case_name": "Newanforbi v. United Parcel Service, Inc.",
        "entity_name": "United Parcel Service, Inc.",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "list_forms": (
            "Notice of Amount of Punitive Damages Sought "
            "(Code Civ. Proc. § 425.115; Civ. Code § 3294) — $25,000.00 "
            "(dated August 4, 2026)"
        ),
        "deadline_date": "09/13/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Sacramento County Sheriff Civil "
            "Division for personal service on United Parcel Service, Inc.'s "
            "registered agent at the address in item 4 — the same registered "
            "agent through which the Summons and Complaint were served July 22, "
            "2026 (Case Manager M. Xiang). Plaintiff has a court fee waiver in "
            "this action (FW-003 GRANTED July 15, 2026) — no sheriff service "
            "fee (Gov. Code §26721)."
        ),
    },
    {
        "matter": 27,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Randstad US LLC (CCP 425.115 Notice) (Aug 4 2026).pdf",
        "county": "Sacramento",
        "case_number": "26CV199902",
        "case_name": "Newanforbi v. Randstad US, LLC, et al.",
        "entity_name": "Randstad US, LLC, a Delaware limited liability company",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "list_forms": (
            "Notice of Amount of Punitive Damages Sought "
            "(Code Civ. Proc. § 425.115; Civ. Code § 3294) — $25,000.00 "
            "(dated August 4, 2026)"
        ),
        "deadline_date": "09/18/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Sacramento County Sheriff Civil "
            "Division for personal service on Randstad US, LLC's registered "
            "agent at the address in item 4 — the same registered agent through "
            "which the Summons and Complaint were served July 30, 2026 (File "
            "No. 2026026857). Plaintiff has a court fee waiver in this action "
            "(FW-003 GRANTED July 20, 2026) — no sheriff service fee (Gov. "
            "Code §26721). A separate SER-001 is submitted for co-defendant "
            "The RK Logistics Group, Inc. (same address)."
        ),
    },
    {
        "matter": 27,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - RK Logistics Group Inc (CCP 425.115 Notice) (Aug 4 2026).pdf",
        "county": "Sacramento",
        "case_number": "26CV199902",
        "case_name": "Newanforbi v. Randstad US, LLC, et al.",
        "entity_name": "The RK Logistics Group, Inc., a California corporation",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "list_forms": (
            "Notice of Amount of Punitive Damages Sought "
            "(Code Civ. Proc. § 425.115; Civ. Code § 3294) — $25,000.00 "
            "(dated August 4, 2026)"
        ),
        "deadline_date": "09/18/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Sacramento County Sheriff Civil "
            "Division for personal service on The RK Logistics Group, Inc.'s "
            "registered agent at the address in item 4 — the same registered "
            "agent through which the Summons and Complaint were served July 30, "
            "2026 (File No. 2026026857). Plaintiff has a court fee waiver in "
            "this action (FW-003 GRANTED July 20, 2026) — no sheriff service "
            "fee (Gov. Code §26721). A separate SER-001 is submitted for "
            "co-defendant Randstad US, LLC (same address)."
        ),
    },
    {
        "matter": 29,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Amazon.com Services LLC (CCP 425.115 Notice) (Aug 4 2026).pdf",
        "county": "Sacramento",
        "case_number": "26CV201554",
        "case_name": "Newanforbi v. Amazon.com Services, LLC, et al.",
        "entity_name": "Amazon.com Services, LLC, a Delaware limited liability company",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "list_forms": (
            "Notice of Amount of Punitive Damages Sought "
            "(Code Civ. Proc. § 425.115; Civ. Code § 3294) — $25,000.00 "
            "(dated August 4, 2026)"
        ),
        "deadline_date": "09/28/2026 (CRC 3.110(b) proof-of-service deadline, as adjusted by CCP §12a; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Sacramento County Sheriff Civil "
            "Division for personal service on Amazon.com Services, LLC's "
            "registered agent at the address in item 4 — the same registered "
            "agent through which the Summons and Complaint were served July 31, "
            "2026 (Levy Officer File No. 2026027206). NOTE — FEE WAIVER NOT YET "
            "GRANTED: Plaintiff's Request to Waive Court Fees in this action "
            "remains pending; the court found it incomplete and set a hearing "
            "for August 18, 2026, 11:30 a.m., Dept. FHO, Hayward Hall of "
            "Justice, on Plaintiff's income/living situation (FW-003, filed "
            "July 28, 2026). Absent a granted waiver by the time this SER-001 "
            "is submitted, the standard Sheriff service fee applies and should "
            "be paid directly, as Plaintiff did for the original Amazon "
            "SER-001 ($52.05). A separate SER-001 is submitted for "
            "co-defendant Accurate Background LLC."
        ),
    },
    {
        "matter": 29,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Accurate Background LLC (CCP 425.115 Notice) (Aug 4 2026).pdf",
        "county": "Los Angeles",
        "case_number": "26CV201554",
        "case_name": "Newanforbi v. Amazon.com Services, LLC, et al.",
        "entity_name": "Accurate Background LLC",
        "entity_person": "Any authorized employee",
        "entity_agent": "CT Corporation System",
        "addr": "330 N Brand Blvd, Suite 700",
        "addr_city": "Glendale",
        "addr_zip": "91203",
        "list_forms": (
            "Notice of Amount of Punitive Damages Sought "
            "(Code Civ. Proc. § 425.115; Civ. Code § 3294) — $25,000.00 "
            "(dated August 4, 2026)"
        ),
        "deadline_date": "09/28/2026 (CRC 3.110(b) proof-of-service deadline, as adjusted by CCP §12a; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Los Angeles County Sheriff Civil "
            "Division for personal service on Accurate Background LLC's "
            "registered agent at the address in item 4. NOTE: for the original "
            "Summons and Complaint, Plaintiff used a private process server "
            "(Sarah Thompson, L.A. Process Servers, $60 flat fee) rather than "
            "the Sheriff for this defendant, personally serving Jaqueline "
            "Mejia, Agent, July 31, 2026, 11:00 a.m. — that channel remains "
            "available as a faster/cheaper alternative to this SER-001 if "
            "preferred. Same pending-fee-waiver caveat as Amazon.com Services, "
            "LLC applies (hearing Aug. 18, 2026, Dept. FHO) — if routed "
            "through the Sheriff, standard service fees apply absent a "
            "granted waiver. A separate SER-001 is submitted for co-defendant "
            "Amazon.com Services, LLC."
        ),
    },
]


def fields_for(d: dict) -> dict[str, object]:
    fields = base_fields(d["case_number"], d["case_name"], d["other"], d["deadline_date"])
    fields[F["county"]] = d["county"]
    fields[F["entity_name"]] = d["entity_name"]
    fields[F["entity_person"]] = d["entity_person"]
    fields[F["entity_agent"]] = d["entity_agent"]
    fields[F["addr"]] = d["addr"]
    fields[F["addr_city"]] = d["addr_city"]
    fields[F["addr_state"]] = "CA"
    fields[F["addr_zip"]] = d["addr_zip"]
    fields[F["gate"]] = ""
    fields[F["list_forms"]] = d["list_forms"]
    return fields


def fill_one(d: dict) -> Path:
    out_dir = DOCS_ROOT / f"matter-{d['matter']:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / d["filename"]
    reader = PdfReader(str(TEMPLATE))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, fields_for(d))
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
    if not SIGNATURE_IMG.is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_IMG}")
    doc = fitz.open(path)
    try:
        page = doc[SIG_PAGE_INDEX]
        page.insert_image(SIG_RECT, filename=str(SIGNATURE_IMG), keep_proportion=True)
        doc.saveIncr()
    finally:
        doc.close()


def verify(path: Path, d: dict) -> None:
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
    doc = fitz.open(path)
    try:
        xobjects = doc[SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(xobjects)} (signature stamped)")
    finally:
        doc.close()


def main() -> None:
    if not TEMPLATE.is_file() or TEMPLATE.stat().st_size < 10_000:
        raise SystemExit(f"Bad/missing template: {TEMPLATE}")
    for d in DEFENDANTS:
        verify(fill_one(d), d)
    print(f"Done — {len(DEFENDANTS)} SER-001 packets.")
    print("Attach each matching CCP 425.115 Notice PDF (already generated) to its")
    print("SER-001 before delivering to the county Sheriff Civil Division named on")
    print("the form. Confirm the $25,000 punitive figure and Matter 29's pending")
    print("fee-waiver status before submitting.")


if __name__ == "__main__":
    main()
