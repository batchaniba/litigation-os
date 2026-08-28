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
from pypdf.generic import NameObject

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from ser001 import FIELDS as F, fill_ser001, filled_values, require_template  # noqa: E402
from signature_stamp import SER001_SIG_PAGE_INDEX  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = ROOT / "internal/public/documents"

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
    return fill_ser001(out_dir / d["filename"], fields_for(d), stamp_signature=True)


def verify(path: Path, d: dict) -> None:
    filled = filled_values(path)
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
        xobjects = doc[SER001_SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(xobjects)} (signature stamped)")
        if not xobjects:
            raise SystemExit(f"{path.name}: no signature image on page 4")
        page4 = doc[SER001_SIG_PAGE_INDEX].get_text()
        if SIG_DATE not in page4 and SIG_DATE not in (filled.get(F["sig_date"]) or ""):
            raise SystemExit(f"{path.name}: missing signature date")
    finally:
        doc.close()


def main() -> None:
    require_template()
    for d in DEFENDANTS:
        verify(fill_one(d), d)
    print(f"Done — {len(DEFENDANTS)} SER-001 packets dated {SIG_DATE}.")
    print("Attach each matching August 7, 2026 CCP §425.115 Notice PDF before")
    print("delivering to the county Sheriff Civil Division named on the form.")
    print("Standard sheriff service fees apply (fee waiver withdrawn as moot).")


if __name__ == "__main__":
    main()
