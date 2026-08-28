#!/usr/bin/env python3
"""Fill the Stanislaus County SER-001 form — Matter 32, Santiago Meza-Gonzalez.

Companion to the three Sacramento County SER-001s in
fill-matters-32-33-sacramento-ser001.py (Melano, Candelaria, Gordon).
Meza-Gonzalez's current duty station is CHP Modesto Area — Stanislaus
County — so his request goes to a different sheriff and is kept in its
own script, matching the Matter 12 / Matter 20 precedent of one script
per county batch.

Docketed Aug. 10, 2026 as No. 3:26-cv-08271-PHK; neither Defendant has
been served (Fed. R. Civ. P. 4(m) deadline computed as Nov. 8, 2026 — 90
days from docketing). No CA state-court fee waiver applies to this
federal action; the sheriff's civil service fee must accompany the
request.
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
OUT_DIR = ROOT / "internal/public/documents/matter-32/ndcal"

YOUR_NAME = "Brendan Ngwa Nforbi"
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

CASE_NUMBER = "3:26-cv-08271-PHK"
CASE_NAME = "Ngwa Nforbi v. Meza-Gonzalez, et al."
COUNTY = "Stanislaus"

# Current duty station (per matter32-ndcal-intake-packet.py) — not the
# CHP Dublin Area office pleaded in the Complaint for the Nov. 1, 2024
# incident, which is in Alameda County.
SERVE_ADDRESS = "4030 Kiernan Avenue"
SERVE_CITY = "Modesto"
SERVE_ZIP = "95356"
GATE = "California Highway Patrol, Modesto Area — official duty station"

SERVE_TIME = "8:00 a.m.–5:00 p.m. (business hours)"
TYPE_PAPERS = "Summons and Complaint (Fed. R. Civ. P. 4)"

# Page count for the enclosed papers (Meza-Gonzalez's own Dkt. 3 summons
# page only — Melano's page of that same 2-page docket entry goes with his
# separate Sacramento packet, not here).
PAGE_BREAKDOWN = (
    ("Complaint (Dkt. 1, Aug. 10, 2026)", 31),
    ("Dkt. 1-1 Civil Filing Fee Receipt", 1),
    ("Dkt. 1-2 JS-CAND 44 Civil Cover Sheet", 1),
    ("Dkt. 3 Summons (Meza-Gonzalez page only)", 1),
    ("Dkt. 4 Order Setting Initial CMC/ADR Deadlines", 2),
)
PAGE_COUNT = sum(n for _, n in PAGE_BREAKDOWN)  # 36
PRICE_PER_PAGE = 1.25
PRINT_FEE = PAGE_COUNT * PRICE_PER_PAGE  # $45.00
CARD_PROCESSING_FEE = 1.75  # per the Department's fee table, $0.01-$50.00 bracket
CARD_TOTAL = PRINT_FEE + CARD_PROCESSING_FEE  # $46.75

LIST_FORMS = (
    "AO 440 Summons issued to Santiago Meza-Gonzalez (Dkt. 3, p. 2 of 2, "
    "Aug. 10, 2026); Complaint (Dkt. 1, Aug. 10, 2026); Dkt. 1-1 Civil "
    "Filing Fee Receipt; Dkt. 1-2 JS-CAND 44 Civil Cover Sheet; Dkt. 4 "
    f"Order Setting Initial CMC/ADR Deadlines — {PAGE_COUNT} pp. total"
)
HEARING_DATE = (
    "12/02/2026, 11:00 a.m., Courtroom F, 450 Golden Gate Ave., San Francisco "
    "(Initial Case Management Conference, Dkt. 4)"
)
DEADLINE_DATE = (
    "08/21/2026 (requested; Rule 4(m) deadline 11/08/2026)"
)
SIG_DATE = "8/13/2026"

OTHER = (
    "Serve at Respondent's current duty station (CHP Modesto Area) — not "
    "the CHP Dublin Area station pleaded in the Complaint for the Nov. 1, "
    "2024 incident, which is in Alameda County. No California state-court "
    "fee waiver applies to this federal action (filing fee paid, not "
    "waived); the Department's civil service fee per its published "
    f"schedule also applies. Enclosed papers total {PAGE_COUNT} pp. "
    f"(printing at $1.25/side/page = ${PRINT_FEE:.2f}). A signed Credit "
    f"Card Authorization for ${PRINT_FEE:.2f} (plus the Department's "
    f"${CARD_PROCESSING_FEE:.2f} card processing fee — ${CARD_TOTAL:.2f} "
    "total if charged) is enclosed to cover printing; mail this SER-001 "
    "and enclosures to Stanislaus County Sheriff – Civil Division, P.O. "
    "Box 3288, Modesto, CA 95353. Co-Defendant Jose Melano is served "
    "under a separate SER-001 at CHP South Sacramento Area (Sacramento "
    "County Sheriff), outside this Stanislaus request."
)

FILENAME = (
    "SER-001 Request for Sheriff to Serve Court Papers - "
    "Santiago Meza-Gonzalez (Stanislaus, Aug 13 2026).pdf"
)

FIELDS: dict[str, object] = {
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
    F["serve_person"]: NameObject("/1"),
    F["person_name"]: "Santiago Meza-Gonzalez (CHP Badge #023295)",
    F["nicknames"]: "Officer, CHP Modesto Area",
    F["desc_no"]: NameObject("/1"),
    F["safety_no"]: NameObject("/1"),
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
    F["oth_text"]: OTHER,
    F["case4"]: CASE_NUMBER,
    F["sig_date"]: SIG_DATE,
    F["type_name"]: YOUR_NAME,
    F["case5"]: CASE_NUMBER,
}


def fill() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return fill_ser001(OUT_DIR / FILENAME, FIELDS, stamp_signature=True)


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
    verify(fill())
    print("Done.")


if __name__ == "__main__":
    main()
