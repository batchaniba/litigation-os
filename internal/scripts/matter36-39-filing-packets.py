#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble San Joaquin print packets for Matters 36–39.

Walk-up order for a fee-waiver unlimited filing:
  1. CM-010 Civil Case Cover Sheet
  2. FW-001 Request to Waive Court Fees
  3. SUM-100 Summons
  4. Verified Complaint

Does not attach exhibits. Does not include the Swift decrypted packet.

    python3 internal/scripts/matter36-39-filing-packets.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pdf_packet import assemble, page_count  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DOCS = ROOT / "internal/public/documents"
DATE = "Sep 8 2026"

CASES = [
    {
        "number": 36,
        "dir": DOCS / "matter-36",
        "stem": "Ngwa Nforbi v AT&T Mobility Services LLC",
    },
    {
        "number": 37,
        "dir": DOCS / "matter-37",
        "stem": "Ngwa Nforbi v Home Depot USA Inc",
    },
    {
        "number": 38,
        "dir": DOCS / "matter-38",
        "stem": "Ngwa Nforbi v Swift Transportation Co of Arizona LLC",
    },
    {
        "number": 39,
        "dir": DOCS / "matter-39",
        "stem": "Ngwa Nforbi v Best Buy Co Inc",
    },
]


def packet_name(stem: str) -> str:
    return f"Filing Packet - {stem} ({DATE}).pdf"


def sources_for(case: dict) -> list[Path]:
    d = case["dir"]
    stem = case["stem"]
    paths = [
        d / f"CM-010 Civil Case Cover Sheet - {stem} ({DATE}).pdf",
        d / f"FW-001 Request to Waive Court Fees - {stem} ({DATE}).pdf",
        d / f"SUM-100 Summons - {stem} ({DATE}).pdf",
        d / f"Verified Complaint - {stem} ({DATE}).pdf",
    ]
    missing = [p for p in paths if not p.is_file()]
    if missing:
        raise SystemExit(
            "Missing packet parts:\n  " + "\n  ".join(str(p) for p in missing)
        )
    return paths


def main() -> None:
    for case in CASES:
        parts = sources_for(case)
        out = case["dir"] / packet_name(case["stem"])
        total = assemble(parts, out)
        part_pages = [page_count(p) for p in parts]
        print(
            f"Wrote {out.name} — {total} pages "
            f"(CM-010 {part_pages[0]} + FW-001 {part_pages[1]} + "
            f"SUM-100 {part_pages[2]} + complaint {part_pages[3]})"
        )


if __name__ == "__main__":
    main()
