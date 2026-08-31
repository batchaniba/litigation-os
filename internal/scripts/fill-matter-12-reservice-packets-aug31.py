#!/usr/bin/env python3
"""Matter 12 — re-service SER-001s and combined sheriff packets (Aug. 31, 2026).

Diamond → Stanislaus (Saliman Osmani, Turlock).
Alpine → Kern (Sheran Osmani, Bakersfield).

Do not reuse the Aug. 3, 2026 SER-001s (those were CCP §425.115 at Turlock).
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf.generic import NameObject

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pdf_packet import assemble  # noqa: E402
from ser001 import FIELDS as F, fill_ser001, require_template  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
M12 = ROOT / "internal/public/documents/matter-12"
OUT = M12 / "reservice-packets-aug31"

CASE_NUMBER = "STK-CV-UF-2026-0001094"
YOUR_NAME = "Brendan Ngwa Nforbi"
CASE_NAME = "Ngwa Nforbi v. Diamond Truck Sales, Inc., et al."
ADDRESS = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

TYPE_PAPERS = "Amended Summons and First Amended Complaint"
LIST_FORMS = (
    "Amended Summons (SUM-100); First Amended Complaint "
    "(STK-CV-UF-2026-0001094) — serve the full set"
)
HEARING_DATE = "12/11/2026, 8:30 a.m., Dept. 11B"
DEADLINE_DATE = "as soon as practicable (re-service to cure; CMC 12/11/2026)"
SIG_DATE = "August 31, 2026"

SUMMONS = M12 / "1094 SUM100 AMENDED Summons - Civil.pdf"
FAC = M12 / "1094 Amended Complaint.pdf"
FW003 = M12 / "1094 FW003 Order on Court Fee Waiver (for Stanislaus Sheriff Service Packets).pdf"
SOS_DIAMOND = M12 / (
    "Diamond Truck Sales Inc - CA SOS Registered Agent for Service of Process "
    "(Aug 28 2026).pdf"
)
SOS_ALPINE = M12 / (
    "Alpine Truck Sales Inc - CA SOS Registered Agent for Service of Process "
    "(Aug 28 2026).pdf"
)


def base_fields(*, county: str, addr: str, city: str, zip_code: str,
                gate: str, other: str) -> dict[str, object]:
    return {
        F["case1"]: CASE_NUMBER,
        F["county"]: county,
        F["yourname"]: YOUR_NAME,
        F["casename"]: CASE_NAME,
        F["address"]: ADDRESS,
        F["city"]: CITY,
        F["state"]: STATE,
        F["zip"]: ZIP,
        F["phone"]: PHONE,
        F["email"]: EMAIL,
        F["case2"]: CASE_NUMBER,
        F["addr"]: addr,
        F["addr_city"]: city,
        F["addr_state"]: "CA",
        F["addr_zip"]: zip_code,
        F["business"]: NameObject("/2"),
        F["serve_time"]: "8:00 a.m.–5:00 p.m. (business hours)",
        F["gate"]: gate,
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


DIAMOND = {
    "ser001_name": "SER-001_Diamond_Truck_Sales_Stanislaus_Aug31_2026.pdf",
    "packet_name": "COMPLETE_Stanislaus_Service_Packet_Diamond_Truck_Sales.pdf",
    "county": "Stanislaus",
    "addr": "1201 S. Soderquist Road",
    "city": "Turlock",
    "zip": "95380",
    "gate": "Truck sales lot — ask for manager / authorized agent for Diamond Truck Sales, Inc.",
    "entity_name": "DIAMOND TRUCK SALES, INC., a California corporation",
    "entity_person": "Officer, manager, or person authorized to accept (CCP §416.10)",
    "entity_agent": "Saliman Osmani (SOS agent for service of process)",
    "sos": SOS_DIAMOND,
    "other": (
        "RE-SERVICE of Amended Summons and First Amended Complaint. "
        "FW-003 fee waiver is already on file as to Diamond and Alpine. "
        "On the POS-010, list the party served using the exact caption name as sued: "
        "DIAMOND TRUCK SALES, INC., a California corporation. "
        "Do not shorten to 'Diamond Truck Sales' or an individual name. "
        "Do NOT serve Alpine Truck Sales, Inc. under this Stanislaus request "
        "(Alpine is Kern County — Sheran Osmani, 7156 Golden State Highway, Bakersfield). "
        "CMC: December 11, 2026, 8:30 a.m., Dept. 11B. "
        "Printing authorization ($43.75 for 35 pp. at $1.25/page) is a separate attachment; "
        "no password."
    ),
}

ALPINE = {
    "ser001_name": "SER-001_Alpine_Truck_Sales_Kern_Aug31_2026.pdf",
    "packet_name": "COMPLETE_Kern_Service_Packet_Alpine_Truck_Sales.pdf",
    "county": "Kern",
    "addr": "7156 Golden State Highway",
    "city": "Bakersfield",
    "zip": "93308",
    "gate": "Principal office / SOS agent address — ask for manager or Sheran Osmani",
    "entity_name": (
        "ALPINE TRUCK SALES, INC., a California corporation (sued individually "
        "and as the successor in interest, mere continuation, and/or alter ego "
        "of Diamond Truck Sales, Inc.)"
    ),
    "entity_person": "Officer, manager, or person authorized to accept (CCP §416.10)",
    "entity_agent": "Sheran Osmani (SOS agent for service of process)",
    "sos": SOS_ALPINE,
    "other": (
        "RE-SERVICE of Amended Summons and First Amended Complaint in Kern County. "
        "FW-003 fee waiver is already on file as to Diamond and Alpine. "
        "On the POS-010, list the party served using the exact caption name as sued: "
        "ALPINE TRUCK SALES, INC., a California corporation (sued individually and as "
        "the successor in interest, mere continuation, and/or alter ego of Diamond "
        "Truck Sales, Inc.). Do not shorten to 'Alpine Truck Sales' or an individual name. "
        "Do NOT serve Diamond Truck Sales, Inc. under this Kern request "
        "(Diamond is Stanislaus County — Saliman Osmani, Turlock). "
        "CMC: December 11, 2026, 8:30 a.m., Dept. 11B."
    ),
}


def fill_one(spec: dict) -> Path:
    fields = base_fields(
        county=spec["county"],
        addr=spec["addr"],
        city=spec["city"],
        zip_code=spec["zip"],
        gate=spec["gate"],
        other=spec["other"],
    )
    fields[F["entity_name"]] = spec["entity_name"]
    fields[F["entity_person"]] = spec["entity_person"]
    fields[F["entity_agent"]] = spec["entity_agent"]
    out = OUT / spec["ser001_name"]
    return fill_ser001(out, fields, stamp_signature=True)


def assemble_packet(spec: dict, ser001: Path) -> Path:
    packet = OUT / spec["packet_name"]
    pages = assemble(
        [ser001, FW003, SUMMONS, FAC, spec["sos"]],
        packet,
    )
    print(f"{packet.name}: {pages} pages")
    return packet


def main() -> None:
    require_template()
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in (DIAMOND, ALPINE):
        ser001 = fill_one(spec)
        assemble_packet(spec, ser001)


if __name__ == "__main__":
    main()
