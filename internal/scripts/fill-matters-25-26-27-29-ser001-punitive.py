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

REVISED AUGUST 7, 2026 — AMOUNTS AND AMENDED NOTICES. The notices this
batch transmits no longer carry the flat $25,000.00 placeholder of the
August 4, 2026 batch; each is now set per defendant (see the amount
rationale in the notice generator's header). Matters 25, 26, and 27 had
already routed their August 4 notice to the Sheriff, so those four
defendants are served an AMENDED notice that supersedes the earlier one
— the SER-001s below are re-issued to transmit the amended document and
supersede the corresponding August 4 service requests. Matter 29
(Amazon / Accurate Background) had no notice served, so those two
SER-001s transmit an original notice at the revised amount.

Matter 29 (Amazon.com Services, LLC / Accurate Background LLC) is a
special case: unlike Matters 25/26/27, the FW-003 fee waiver in that
action was NOT granted -- the court found the request incomplete and
set a hearing for August 18, 2026 on Plaintiff's financial information.
Absent a granted waiver by the time these two SER-001s are actually
submitted, standard Sheriff service fees apply (as Plaintiff already
paid out of pocket, $52.05, for the original Amazon SER-001).
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
SIG_DATE = "August 7, 2026"

TYPE_PAPERS = "Notice of Amount of Punitive Damages Sought (CCP §425.115)"
TYPE_PAPERS_AMENDED = "Amended Notice of Amount of Punitive Damages Sought (CCP §425.115)"


def list_forms(amount: str, amended: bool) -> str:
    """Item 5b description of the paper being served."""
    lead = "Amended Notice" if amended else "Notice"
    return (
        f"{lead} of Amount of Punitive Damages Sought "
        f"(Code Civ. Proc. § 425.115; Civ. Code § 3294) — {amount} "
        f"(dated August 7, 2026)"
        + (" — supersedes the $25,000.00 Notice dated August 4, 2026" if amended else "")
    )


def base_fields(case_number: str, case_name: str, other: str, deadline_date: str,
                amended: bool) -> dict[str, object]:
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
        F["type_papers"]: TYPE_PAPERS_AMENDED if amended else TYPE_PAPERS,
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
        "amount": "$250,000.00",
        "amended": True,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Federal Express Corporation (Amended CCP 425.115 Notice) (Aug 7 2026).pdf",
        "county": "Los Angeles",
        "case_number": "STK-CV-UWT-2026-0009118",
        "case_name": "Newanforbi v. Federal Express Corporation",
        "entity_name": "Federal Express Corporation",
        "entity_person": "Any authorized employee",
        "entity_agent": "Ct Corporation System",
        "addr": "330 N Brand Blvd, Ste 700",
        "addr_city": "Glendale",
        "addr_zip": "91203",
        "deadline_date": "09/13/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached AMENDED Notice of Amount of "
            "Punitive Damages Sought (CCP §425.115) to Los Angeles County Sheriff "
            "Civil Division for personal service on Federal Express Corporation's "
            "registered agent at the address in item 4 — the same registered "
            "agent through which the Summons and Complaint were served July 24, "
            "2026 (File No. 2026075280). THIS REQUEST SUPERSEDES the SER-001 "
            "emailed to LASD Civil Process August 4, 2026, which transmitted a "
            "$25,000.00 Notice; the attached Amended Notice states $250,000.00 "
            "and replaces that earlier Notice in full. If the August 4 Notice "
            "has not yet been served, serve the Amended Notice in its place; if "
            "it has been served, serve the Amended Notice in addition. Plaintiff "
            "has a court fee waiver in this action (FW-003 GRANTED July 15, "
            "2026) — no sheriff service fee (Gov. Code §26721)."
        ),
    },
    {
        "matter": 26,
        "amount": "$250,000.00",
        "amended": True,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - United Parcel Service Inc (Amended CCP 425.115 Notice) (Aug 7 2026).pdf",
        "county": "Sacramento",
        "case_number": "STK-CV-UWT-2026-0009113",
        "case_name": "Newanforbi v. United Parcel Service, Inc.",
        "entity_name": "United Parcel Service, Inc.",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "deadline_date": "09/13/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached AMENDED Notice of Amount of "
            "Punitive Damages Sought (CCP §425.115) to Sacramento County Sheriff "
            "Civil Division for personal service on United Parcel Service, Inc.'s "
            "registered agent at the address in item 4 — the same registered "
            "agent through which the Summons and Complaint were served July 22, "
            "2026 (Case Manager M. Xiang). THIS REQUEST SUPERSEDES the SER-001 "
            "submitted August 3, 2026, which transmitted a $25,000.00 Notice; "
            "the attached Amended Notice states $250,000.00 and replaces that "
            "earlier Notice in full. If the August 4 Notice has not yet been "
            "served, serve the Amended Notice in its place; if it has been "
            "served, serve the Amended Notice in addition. Plaintiff has a court "
            "fee waiver in this action (FW-003 GRANTED July 15, 2026) — no "
            "sheriff service fee (Gov. Code §26721)."
        ),
    },
    {
        "matter": 27,
        "amount": "$500,000.00",
        "amended": True,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Randstad US LLC (Amended CCP 425.115 Notice) (Aug 7 2026).pdf",
        "county": "Sacramento",
        "case_number": "26CV199902",
        "case_name": "Newanforbi v. Randstad US, LLC, et al.",
        "entity_name": "Randstad US, LLC, a Delaware limited liability company",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "deadline_date": "09/18/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached AMENDED Notice of Amount of "
            "Punitive Damages Sought (CCP §425.115) to Sacramento County Sheriff "
            "Civil Division for personal service on Randstad US, LLC's registered "
            "agent at the address in item 4 — the same registered agent through "
            "which the Summons and Complaint were served July 30, 2026 (File "
            "No. 2026026857). THIS REQUEST SUPERSEDES the SER-001 dated August "
            "4, 2026, which transmitted a $25,000.00 Notice; the attached "
            "Amended Notice states $500,000.00 and replaces that earlier Notice "
            "in full. If the August 4 Notice has not yet been served, serve the "
            "Amended Notice in its place; if it has been served, serve the "
            "Amended Notice in addition. Plaintiff has a court fee waiver in "
            "this action (FW-003 GRANTED July 20, 2026) — no sheriff service "
            "fee (Gov. Code §26721). A separate SER-001 is submitted for "
            "co-defendant The RK Logistics Group, Inc. (same address)."
        ),
    },
    {
        "matter": 27,
        "amount": "$500,000.00",
        "amended": True,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - RK Logistics Group Inc (Amended CCP 425.115 Notice) (Aug 7 2026).pdf",
        "county": "Sacramento",
        "case_number": "26CV199902",
        "case_name": "Newanforbi v. Randstad US, LLC, et al.",
        "entity_name": "The RK Logistics Group, Inc., a California corporation",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
        "deadline_date": "09/18/2026 (CRC 3.110(b) proof-of-service deadline; serve before any default is taken)",
        "other": (
            "Deliver this SER-001 and the attached AMENDED Notice of Amount of "
            "Punitive Damages Sought (CCP §425.115) to Sacramento County Sheriff "
            "Civil Division for personal service on The RK Logistics Group, "
            "Inc.'s registered agent at the address in item 4 — the same "
            "registered agent through which the Summons and Complaint were "
            "served July 30, 2026 (File No. 2026026857). THIS REQUEST SUPERSEDES "
            "the SER-001 dated August 4, 2026, which transmitted a $25,000.00 "
            "Notice; the attached Amended Notice states $500,000.00 and replaces "
            "that earlier Notice in full. If the August 4 Notice has not yet "
            "been served, serve the Amended Notice in its place; if it has been "
            "served, serve the Amended Notice in addition. Plaintiff has a court "
            "fee waiver in this action (FW-003 GRANTED July 20, 2026) — no "
            "sheriff service fee (Gov. Code §26721). A separate SER-001 is "
            "submitted for co-defendant Randstad US, LLC (same address)."
        ),
    },
    {
        "matter": 29,
        "amount": "$250,000.00",
        "amended": False,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Amazon.com Services LLC (CCP 425.115 Notice) (Aug 7 2026).pdf",
        "county": "Sacramento",
        "case_number": "26CV201554",
        "case_name": "Newanforbi v. Amazon.com Services, LLC, et al.",
        "entity_name": "Amazon.com Services, LLC, a Delaware limited liability company",
        "entity_person": "Any authorized employee",
        "entity_agent": "CSC - Lawyers Incorporating Service",
        "addr": "2710 Gateway Oaks Drive, Suite 150N",
        "addr_city": "Sacramento",
        "addr_zip": "95833",
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
        "amount": "$100,000.00",
        "amended": False,
        "filename": "SER-001 Request for Sheriff to Serve Court Papers - Accurate Background LLC (CCP 425.115 Notice) (Aug 7 2026).pdf",
        "county": "Los Angeles",
        "case_number": "26CV201554",
        "case_name": "Newanforbi v. Amazon.com Services, LLC, et al.",
        "entity_name": "Accurate Background LLC",
        "entity_person": "Any authorized employee",
        "entity_agent": "CT Corporation System",
        "addr": "330 N Brand Blvd, Suite 700",
        "addr_city": "Glendale",
        "addr_zip": "91203",
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
    fields = base_fields(d["case_number"], d["case_name"], d["other"], d["deadline_date"], d["amended"])
    fields[F["county"]] = d["county"]
    fields[F["entity_name"]] = d["entity_name"]
    fields[F["entity_person"]] = d["entity_person"]
    fields[F["entity_agent"]] = d["entity_agent"]
    fields[F["addr"]] = d["addr"]
    fields[F["addr_city"]] = d["addr_city"]
    fields[F["addr_state"]] = "CA"
    fields[F["addr_zip"]] = d["addr_zip"]
    fields[F["gate"]] = ""
    fields[F["list_forms"]] = list_forms(d["amount"], d["amended"])
    return fields


def fill_one(d: dict) -> Path:
    out_dir = DOCS_ROOT / f"matter-{d['matter']:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    return fill_ser001(out_dir / d["filename"], fields_for(d), stamp_signature=True)


def verify(path: Path, d: dict) -> None:
    filled = filled_values(path)
    print(f"{path.name}: {len(filled)} filled fields")
    for key in (F["county"], F["entity_name"], F["addr"], F["addr_city"], F["sig_date"], F["type_papers"]):
        if key in filled:
            print(f"  {key.split('.')[-1]}: {filled[key]!r}")
    doc = fitz.open(path)
    try:
        xobjects = doc[SER001_SIG_PAGE_INDEX].get_images(full=True)
        print(f"  page-4 images: {len(xobjects)} (signature stamped)")
    finally:
        doc.close()


def main() -> None:
    require_template()
    for d in DEFENDANTS:
        verify(fill_one(d), d)
    amended = sum(1 for d in DEFENDANTS if d["amended"])
    print(f"Done — {len(DEFENDANTS)} SER-001 packets ({amended} transmitting amended notices).")
    print("Attach each matching CCP 425.115 Notice PDF (already generated) to its")
    print("SER-001 before delivering to the county Sheriff Civil Division named on")
    print("the form. The Matter 25/26/27 requests supersede the Aug. 4, 2026 batch")
    print("and must reach the Sheriff before any default is taken. Confirm Matter")
    print("29's pending fee-waiver status before submitting those two.")


if __name__ == "__main__":
    main()
