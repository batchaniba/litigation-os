#!/usr/bin/env python3
"""Matter 12 — additional Stanislaus service on Saliman Osmani only (Sept. 9, 2026).

Levy 2026003531 returned personal service on Musdaqem Usmani/Manager with
POS-010 item 6 as an individual defendant. The August 31 SER-001 invited that
by filling both 3b(2) (officer/manager) and 3b(3) (SOS agent), and the cover
email said serve a manager or the agent.

This request blanks 3b(2), names Saliman Osmani only in 3b(3), and tells the
deputy to complete the summons Notice to the Person Served and POS-010 item 6
on behalf of the corporation under CCP § 416.10 — not as an individual.

Do not amend who was served on levy 2026003531. That return stays as written.
Do not regenerate the August 31 historical packet.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf.generic import NameObject

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from ser001 import FIELDS as F, fill_ser001, filled_values, flatten_ser001, require_template  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "internal/public/documents/matter-12/reservice-packets-sep9"

CASE_NUMBER = "STK-CV-UF-2026-0001094"
SIG_DATE = "September 9, 2026"
OUT_NAME = "1_SER-001_Diamond_Saliman_Osmani_Stanislaus.pdf"


def fields() -> dict[str, object]:
    return {
        F["case1"]: CASE_NUMBER,
        F["county"]: "Stanislaus",
        F["yourname"]: "Brendan Ngwa Nforbi",
        F["casename"]: "Ngwa Nforbi v. Diamond Truck Sales, Inc., et al.",
        F["address"]: "1455 Cat Tail Drive",
        F["city"]: "Stockton",
        F["state"]: "CA",
        F["zip"]: "95204",
        F["phone"]: "(209) 801-4442",
        F["email"]: "bnn.cdl@gmail.com",
        F["case2"]: CASE_NUMBER,
        F["addr"]: "1201 S. Soderquist Road",
        F["addr_city"]: "Turlock",
        F["addr_state"]: "CA",
        F["addr_zip"]: "95380",
        F["business"]: NameObject("/2"),
        F["serve_time"]: "8:00 a.m.–5:00 p.m. (business hours)",
        F["gate"]: "Ask for Saliman Osmani only. Do not serve a manager in lieu.",
        F["type_papers"]: "Amended Summons and First Amended Complaint",
        F["list_forms"]: (
            "Amended Summons (SUM-100); First Amended Complaint "
            "(STK-CV-UF-2026-0001094) — serve the full set"
        ),
        F["hearing_yes"]: NameObject("/3"),
        F["hearing_date"]: "12/11/2026, 8:30 a.m., Dept. 11B",
        F["case3"]: CASE_NUMBER,
        F["deadline_yes"]: NameObject("/3"),
        F["deadline_date"]: "as soon as practicable (additional service; CMC 12/11/2026)",
        F["alt_no"]: NameObject("/2"),
        F["oth_yes"]: NameObject("/2"),
        F["oth_text"]: (
            "ADDITIONAL SERVICE. Keep levy 2026003531 (Heaney, Sept. 8, 2026, "
            "Usmani/Manager) as written. Do not amend who was served. Serve "
            "Saliman Osmani only — 3b(2) blank; 3b(3) agent. Do not serve a "
            "manager in lieu. On the Amended Summons handed over, complete "
            "Notice to the Person Served on behalf of DIAMOND TRUCK SALES, "
            "INC., a California corporation, CCP § 416.10. POS-010: 3a that "
            "exact name; 3b Saliman Osmani, agent for service of process; "
            "item 6 = 6d (on behalf of the corporation / 416.10). Do not "
            "check 6a (individual). Do not serve Alpine (Kern)."
        ),
        F["case4"]: CASE_NUMBER,
        F["sig_date"]: SIG_DATE,
        F["type_name"]: "Brendan Ngwa Nforbi",
        F["case5"]: CASE_NUMBER,
        F["serve_entity"]: NameObject("/2"),
        F["entity_name"]: "DIAMOND TRUCK SALES, INC., a California corporation",
        F["entity_agent"]: "Saliman Osmani, agent for service of process",
    }


def verify_fields(path: Path) -> None:
    values = filled_values(path)
    person_key = F["entity_person"]
    agent_key = F["entity_agent"]
    if person_key in values:
        raise SystemExit(f"3b(2) must be blank; found {values[person_key]!r}")
    agent = str(values.get(agent_key, ""))
    if "Saliman Osmani" not in agent:
        raise SystemExit(f"3b(3) missing Saliman Osmani: {agent!r}")
    print(f"OK — 3b(2) blank; 3b(3)={agent}")


def verify_text(path: Path) -> None:
    import fitz

    text = "".join(page.get_text() for page in fitz.open(path))
    if "Saliman Osmani" not in text:
        raise SystemExit("flattened PDF missing Saliman Osmani")
    if "Do not check 6a" not in text:
        raise SystemExit("flattened PDF missing POS-010 item 6d instruction")
    if "Do not serve a manager" not in text:
        raise SystemExit("flattened PDF missing do-not-serve-a-manager instruction")
    print("OK — flattened text has agent name and item 6d instruction")


def main() -> None:
    require_template()
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / OUT_NAME
    fill_ser001(out, fields(), stamp_signature=True, flatten=False)
    verify_fields(out)
    flatten_ser001(out)
    verify_text(out)
    print(f"{out}: {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
