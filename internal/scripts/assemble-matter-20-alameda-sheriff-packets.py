#!/usr/bin/env python3
"""Assemble Matter 20 Alameda Sheriff Civil service packets.

Each packet (one per Individual Respondent) is ordered:
  SER-001 (5) → FW-003 Order on Court Fee Waiver (4) → Opposition + MPA (12)
= 21 pages.

Destination: Alameda County Sheriff Civil Division, for service at
CHP Dublin Area duty station (4999 Gleason Drive, Dublin, CA 94568).
"""

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pdf_packet import assemble, page_count  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DOC_DIR = ROOT / "internal/public/documents/matter-32/from-20"

FEE_WAIVER = DOC_DIR / "FW-003 Order on Court Fee Waiver - GRANTED (Jun 3 2026).pdf"
OPPOSITION = DOC_DIR / "Opposition-to-Individual-Respondents-Demurrers.pdf"

RESPONDENTS = [
    {
        "key": "Serrato",
        "ser": DOC_DIR
        / "SER-001 Request for Sheriff to Serve Court Papers - G Serrato (Jul 31 2026).pdf",
        "out": DOC_DIR
        / "Alameda Sheriff Service Packet - G Serrato (SER-001, FW-003, Opposition-MPA) (Aug 3 2026).pdf",
    },
    {
        "key": "Paul",
        "ser": DOC_DIR
        / "SER-001 Request for Sheriff to Serve Court Papers - Gary Paul (Jul 31 2026).pdf",
        "out": DOC_DIR
        / "Alameda Sheriff Service Packet - Gary Paul (SER-001, FW-003, Opposition-MPA) (Aug 3 2026).pdf",
    },
    {
        "key": "Dutra",
        "ser": DOC_DIR
        / "SER-001 Request for Sheriff to Serve Court Papers - Eric Dutra (Jul 31 2026).pdf",
        "out": DOC_DIR
        / "Alameda Sheriff Service Packet - Eric Dutra (SER-001, FW-003, Opposition-MPA) (Aug 3 2026).pdf",
    },
]


def assemble_packet(ser_path: Path, out_path: Path) -> tuple[int, int, int, int]:
    n_ser = page_count(ser_path)
    n_fw = page_count(FEE_WAIVER)
    n_opp = page_count(OPPOSITION)
    assemble([ser_path, FEE_WAIVER, OPPOSITION], out_path)
    return n_ser, n_fw, n_opp, n_ser + n_fw + n_opp


def main() -> None:
    for missing in (FEE_WAIVER, OPPOSITION):
        if not missing.exists():
            raise SystemExit(f"Missing required PDF: {missing}")

    for item in RESPONDENTS:
        if not item["ser"].exists():
            raise SystemExit(f"Missing SER-001: {item['ser']}")
        n_ser, n_fw, n_opp, total = assemble_packet(item["ser"], item["out"])
        print(
            f"{item['key']}: {total} pp "
            f"(SER-001 {n_ser} + FW-003 {n_fw} + Opposition/MPA {n_opp}) "
            f"→ {item['out'].name}"
        )


if __name__ == "__main__":
    main()
