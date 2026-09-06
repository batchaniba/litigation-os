#!/usr/bin/env python3
"""Matter 32 — Exhibit A cover + USPS e-receipt for FAC mail service on Melano.

Attaches the August 21, 2026 San Jose MO Finance e-receipt (First-Class
Large Envelope to Sacramento 95823 — Melano FAC Dkt. 5 — and the other
First-Class mailings that afternoon) behind a Diamond-style Exhibit A
cover. Does not restamp the e-receipt or the FAC proof of service.

  python3 internal/scripts/matter32-exhibit-a-usps-ereceipt-fac-melano.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import assemble  # noqa: E402

ROOT = SCRIPT_DIR.parent
OUT_DIR = ROOT / "public/documents/matter-32/ndcal"

CASE_NO = "4:26-cv-08271-ASK"
CAPTION = "NFORBI v. MEZA-GONZALEZ ET AL."

ERECEIPT = OUT_DIR / (
    "USPS eReceipt - Service of FAC on Melano and other Mailings "
    "(Aug 21 2026).pdf"
)
POS = OUT_DIR / "Proof of Service - FAC Dkt 05 Mailed to Melano (Aug 21 2026).pdf"

COVER = OUT_DIR / (
    "Exhibit A Cover - USPS eReceipt FAC Service on Melano (Aug 21 2026).pdf"
)
EXHIBIT = OUT_DIR / (
    "Exhibit A - USPS eReceipt FAC Service on Melano (Aug 21 2026).pdf"
)
PACKET = OUT_DIR / (
    "Proof of Service Packet - FAC Dkt 05 Mailed to Melano with Exhibit A "
    "(Aug 21 2026).pdf"
)


def build_cover(path: Path) -> Path:
    return write_exhibit_cover(
        path,
        court="UNITED STATES DISTRICT COURT",
        court_line2="NORTHERN DISTRICT OF CALIFORNIA",
        caption=CAPTION,
        case_no=f"Case No. {CASE_NO}",
        exhibit="A",
        title="USPS eReceipt — Service of FAC on Melano",
        details=[
            "First-Class Large Envelope to Sacramento, CA 95823",
            "San Jose MO Finance — August 21, 2026, 5:40 p.m.",
            "Receipt 840-59500196-3-10335441-2  ·  $14.78",
            "Also records other First-Class mailings that afternoon",
        ],
        footer=(
            "Proof of Service — FAC Dkt. 5 mailed to Melano — "
            "Nforbi v. Meza-Gonzalez et al. — Exhibit A"
        ),
    )


def main() -> None:
    if not ERECEIPT.is_file():
        raise SystemExit(f"Missing e-receipt (do not restamp): {ERECEIPT}")
    if not POS.is_file():
        raise SystemExit(f"Missing FAC proof of service (do not restamp): {POS}")

    build_cover(COVER)
    n_ex = assemble([COVER, ERECEIPT], EXHIBIT)
    n_pkt = assemble([POS, COVER, ERECEIPT], PACKET)
    print(f"Wrote {COVER.name}")
    print(f"Wrote {EXHIBIT.name} ({n_ex} pp.)")
    print(f"Wrote {PACKET.name} ({n_pkt} pp.)")


if __name__ == "__main__":
    main()
