#!/usr/bin/env python3
"""Matter 12 — sheriff re-service packets (Aug. 31, 2026).

Diamond (Stanislaus) — four documents:
  1. SER-001
  2. FW-003 (already on file)
  3. Clerk-issued Amended Summons + First Amended Complaint
  4. Unlocked Stanislaus CC authorization (printing only)

Alpine (Kern) — documents 1–3 only. No printing charge.

Do not reuse the Aug. 3, 2026 SER-001s (those were CCP §425.115 at Turlock).
"""

from __future__ import annotations

import importlib.util
import shutil
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

# Clerk-issued Jun. 11, 2026: NOTICE TO DEFENDANT names Diamond (handwritten)
# and Alpine as sued (typed successor/alter-ego caption). Do not use the
# Diamond-only "AMENDED Summons - Civil.pdf" or the Alpine-only Civil 2 scan.
SUMMONS = M12 / (
    "1094 SUM100 AMENDED Summons - Both Defendants (Issued Jun 11 2026).pdf"
)
FAC = M12 / "1094 Amended Complaint.pdf"
FW003 = M12 / "1094 FW003 Order on Court Fee Waiver (for Stanislaus Sheriff Service Packets).pdf"


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
    "ser001_name": "1_SER-001_Diamond_Truck_Sales_Stanislaus.pdf",
    "packet3_name": "3_Summons_FAC_Diamond_Truck_Sales.pdf",
    "county": "Stanislaus",
    "addr": "1201 S. Soderquist Road",
    "city": "Turlock",
    "zip": "95380",
    "gate": "Truck sales lot — ask for manager / authorized agent for Diamond Truck Sales, Inc.",
    "entity_name": "DIAMOND TRUCK SALES, INC., a California corporation",
    "entity_person": "Officer, manager, or person authorized to accept (CCP §416.10)",
    "entity_agent": "Saliman Osmani (SOS agent for service of process)",
    "other": (
        "RE-SERVICE of Amended Summons and First Amended Complaint. "
        "FW-003 fee waiver is already on file as to Diamond and Alpine. "
        "On the POS-010, list the party served using the exact caption name as sued: "
        "DIAMOND TRUCK SALES, INC., a California corporation. "
        "Do not shorten to 'Diamond Truck Sales' or an individual name. "
        "Do NOT serve Alpine Truck Sales, Inc. under this Stanislaus request "
        "(Alpine is Kern County — Sheran Osmani, 7156 Golden State Highway, Bakersfield). "
        "CMC: December 11, 2026, 8:30 a.m., Dept. 11B. "
        "Four documents: (1) this SER-001, (2) FW-003, (3) Amended Summons + FAC, "
        "(4) unlocked printing authorization ($43.75 for 35 pp. at $1.25/page); no password. "
        "Print packet 3 in full (Summons 1 p. + FAC 34 pp.)."
    ),
}

ALPINE = {
    "ser001_name": "1_SER-001_Alpine_Truck_Sales_Kern.pdf",
    "packet3_name": "3_Summons_FAC_Alpine_Truck_Sales.pdf",
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
    "other": (
        "RE-SERVICE of Amended Summons and First Amended Complaint in Kern County. "
        "FW-003 fee waiver is already on file as to Diamond and Alpine. "
        "On the POS-010, list the party served using the exact caption name as sued: "
        "ALPINE TRUCK SALES, INC., a California corporation (sued individually and as "
        "the successor in interest, mere continuation, and/or alter ego of Diamond "
        "Truck Sales, Inc.). Do not shorten to 'Alpine Truck Sales' or an individual name. "
        "Do NOT serve Diamond Truck Sales, Inc. under this Kern request "
        "(Diamond is Stanislaus County — Saliman Osmani, Turlock). "
        "CMC: December 11, 2026, 8:30 a.m., Dept. 11B. "
        "Three packets: (1) this SER-001, (2) FW-003, (3) Amended Summons + FAC. "
        "No printing charge requested."
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


FW003_PACKET_NAME = "2_FW-003_Order_on_Court_Fee_Waiver.pdf"
HANDOFF = ROOT / "internal/handoff"
CC_DOC4_NAME = "4_Stanislaus_Credit_Card_Authorization_Diamond.pdf"


def _load_cc_module():
    path = SCRIPT_DIR / "fill-matter-12-stanislaus-cc-authorization.py"
    spec = importlib.util.spec_from_file_location("matter12_cc_auth", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def copy_fw003() -> Path:
    dest = OUT / FW003_PACKET_NAME
    shutil.copyfile(FW003, dest)
    return dest


def assemble_packet3(spec: dict) -> Path:
    packet = OUT / spec["packet3_name"]
    pages = assemble([SUMMONS, FAC], packet)
    print(f"{packet.name}: {pages} pages")
    return packet


def fill_document4_cc() -> Path:
    dest = OUT / CC_DOC4_NAME
    if dest.is_file() and dest.stat().st_size > 10_000:
        print(f"{dest.name}: already present")
        return dest
    cc = _load_cc_module()
    cc.fill(dest)
    cc.verify(dest)
    return dest


def remove_legacy_combined() -> None:
    for name in (
        "COMPLETE_Stanislaus_Service_Packet_Diamond_Truck_Sales.pdf",
        "COMPLETE_Kern_Service_Packet_Alpine_Truck_Sales.pdf",
        "SER-001_Diamond_Truck_Sales_Stanislaus_Aug31_2026.pdf",
        "SER-001_Alpine_Truck_Sales_Kern_Aug31_2026.pdf",
        "3_Summons_FAC_SOS_Diamond_Truck_Sales.pdf",
        "3_Summons_FAC_SOS_Alpine_Truck_Sales.pdf",
        "3_Summons_FAC_SOS_CC_Diamond_Truck_Sales.pdf",
    ):
        for folder in (OUT, HANDOFF):
            path = folder / name
            if path.exists():
                path.unlink()


def main() -> None:
    require_template()
    OUT.mkdir(parents=True, exist_ok=True)
    remove_legacy_combined()
    fw = copy_fw003()
    print(f"{fw.name}: copied")
    for spec in (DIAMOND, ALPINE):
        ser001 = fill_one(spec)
        print(f"{ser001.name}: filled")
        assemble_packet3(spec)
    doc4 = fill_document4_cc()
    print(f"Diamond document 4: {doc4}")


if __name__ == "__main__":
    main()
