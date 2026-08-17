#!/usr/bin/env python3
"""Fill two Matter 29 SER-001 forms dated August 17, 2026.

Transmits the operative August 7, 2026 CCP §425.115 Notices
($250,000 Amazon.com Services, LLC / $100,000 Accurate Background LLC)
for personal service in the same manner as a summons. Routes each
request to the same county Sheriff Civil Division and registered-agent
address used for the July 31, 2026 summons service.

These requests supersede the unsubmitted August 7, 2026 SER-001s.
The $435 first-paper fee has been paid and the FW-001 withdrawn as
moot, so standard sheriff service fees apply.
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
DOCS_ROOT = ROOT / "internal/public/documents"

# Page-4 right-hand "Sign your name" line (PyMuPDF top-origin coords) —
# same placement used for the Matter 12 and Matters 25/26/27/29 SER-001s.
SIG_PAGE_INDEX = 3
SIG_WIDTH = 120.0
SIG_HEIGHT = SIG_WIDTH * SIGNATURE_ASPECT
SIG_BASELINE = 645.0
SIG_RECT = fitz.Rect(360.0, SIG_BASELINE - SIG_HEIGHT, 360.0 + SIG_WIDTH, SIG_BASELINE)

YOUR_NAME = "Brendan Ngehsi Newanforbi"
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
SIG_DATE = "August 17, 2026"

TYPE_PAPERS = "Notice of Amount of Punitive Damages Sought (CCP §425.115)"


def list_forms(amount: str) -> str:
    return (
        "Notice of Amount of Punitive Damages Sought "
        f"(Code Civ. Proc. § 425.115; Civ. Code § 3294) — {amount} "
        "(dated August 7, 2026)"
    )


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
        "matter": 29,
        "amount": "$250,000.00",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Amazon.com Services LLC (CCP 425.115 Notice) (Aug 17 2026).pdf"
        ),
        "county": "Sacramento",
        "case_number": "26CV201554",
        "case_name": "Newanforbi v. Amazon.com Services, LLC, et al.",
        "entity_name": "Amazon.com Services, LLC, a Delaware limited liability company",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "deadline_date": (
            "08/31/2026 (responsive-pleading deadline; serve before any default "
            "is taken — CCP §425.115(f), (g)(1))"
        ),
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Sacramento County Sheriff Civil "
            "Division for personal service on Amazon.com Services, LLC's "
            "registered agent at the address in item 4 — the same registered "
            "agent through which the Summons and Complaint were served July 31, "
            "2026 (Levy Officer File No. 2026027206, Rebecca Vang, Authorized "
            "Agent). THIS REQUEST SUPERSEDES the unsubmitted SER-001 dated "
            "August 7, 2026. The attached Notice (dated August 7, 2026) states "
            "$250,000.00. Plaintiff's $435.00 first-paper fee has been paid in "
            "full and the FW-001 fee-waiver request withdrawn as moot — there "
            "is no granted fee waiver; the standard Sheriff service fee applies "
            "and should be paid with this request (Plaintiff previously paid "
            "$52.05 for the original Amazon summons SER-001). A separate "
            "SER-001 is submitted for co-defendant Accurate Background LLC."
        ),
    },
    {
        "matter": 29,
        "amount": "$100,000.00",
        "filename": (
            "SER-001 Request for Sheriff to Serve Court Papers - "
            "Accurate Background LLC (CCP 425.115 Notice) (Aug 17 2026).pdf"
        ),
        "county": "Los Angeles",
        "case_number": "26CV201554",
        "case_name": "Newanforbi v. Amazon.com Services, LLC, et al.",
        "entity_name": "Accurate Background LLC",
        "entity_person": "Any authorized employee",
        "entity_agent": "CT Corporation System",
        "addr": "330 N Brand Blvd, Suite 700",
        "addr_city": "Glendale",
        "addr_zip": "91203",
        "deadline_date": (
            "08/31/2026 (responsive-pleading deadline; serve before any default "
            "is taken — CCP §425.115(f), (g)(1))"
        ),
        "other": (
            "Deliver this SER-001 and the attached Notice of Amount of Punitive "
            "Damages Sought (CCP §425.115) to Los Angeles County Sheriff Civil "
            "Division for personal service on Accurate Background LLC's "
            "registered agent at the address in item 4. NOTE: for the original "
            "Summons and Complaint, Plaintiff used a private process server "
            "(Sarah Thompson, L.A. Process Servers, $60 flat fee) rather than "
            "the Sheriff for this defendant, personally serving Jaqueline "
            "Mejia, Agent, July 31, 2026, 11:00 a.m. — that channel remains "
            "available as a faster alternative to this SER-001 if preferred. "
            "THIS REQUEST SUPERSEDES the unsubmitted SER-001 dated August 7, "
            "2026. The attached Notice (dated August 7, 2026) states "
            "$100,000.00. Plaintiff's $435.00 first-paper fee has been paid in "
            "full and the FW-001 fee-waiver request withdrawn as moot — there "
            "is no granted fee waiver; if routed through the Sheriff, the "
            "standard service fee applies. A separate SER-001 is submitted for "
            "co-defendant Amazon.com Services, LLC."
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
    fields[F["list_forms"]] = list_forms(d["amount"])
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
    """Stamp the portfolio's canonical e-signature on page 4's signature line."""
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    doc = fitz.open(path)
    try:
        page = doc[SIG_PAGE_INDEX]
        page.insert_image(SIG_RECT, filename=SIGNATURE_PATH, keep_proportion=True)
        tmp = path.with_suffix(".signed.pdf")
        doc.save(tmp, garbage=4, deflate=True, incremental=False)
    finally:
        doc.close()
    tmp.replace(path)


def verify(path: Path, d: dict) -> None:
    fields = PdfReader(str(path)).get_fields() or {}
    filled = {
        k: v.get("/V")
        for k, v in fields.items()
        if v.get("/V") not in (None, "", NameObject("/Off"), "/Off")
    }
    print(f"{path.name}: {len(filled)} filled fields")
    for key in (F["county"], F["entity_name"], F["entity_agent"], F["addr"], F["sig_date"], F["type_papers"]):
        if key in filled:
            print(f"  {key.split('.')[-1]}: {filled[key]!r}")
    expected = {
        F["county"]: d["county"],
        F["entity_agent"]: d["entity_agent"],
        F["sig_date"]: SIG_DATE,
        F["type_name"]: YOUR_NAME,
    }
    for key, want in expected.items():
        got = filled.get(key)
        if got != want:
            raise SystemExit(f"{path.name}: field {key.split('.')[-1]}={got!r}, expected {want!r}")
    doc = fitz.open(path)
    try:
        xobjects = doc[SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(xobjects)} (signature stamped)")
        if not xobjects:
            raise SystemExit(f"{path.name}: no signature image on page 4")
        page4 = doc[SIG_PAGE_INDEX].get_text()
        if SIG_DATE not in page4 and SIG_DATE not in (filled.get(F["sig_date"]) or ""):
            raise SystemExit(f"{path.name}: missing signature date")
    finally:
        doc.close()


def main() -> None:
    if not TEMPLATE.is_file() or TEMPLATE.stat().st_size < 10_000:
        raise SystemExit(f"Bad/missing template: {TEMPLATE}")
    for d in DEFENDANTS:
        verify(fill_one(d), d)
    print(f"Done — {len(DEFENDANTS)} SER-001 packets dated {SIG_DATE}.")
    print("Attach each matching August 7, 2026 CCP §425.115 Notice PDF before")
    print("delivering to the county Sheriff Civil Division named on the form.")
    print("Standard sheriff service fees apply (fee waiver withdrawn as moot).")


if __name__ == "__main__":
    main()
