#!/usr/bin/env python3
"""Generate the portfolio-wide Proof of Service blank + Meza/Candelaria fills.

Canonical API: ``internal/scripts/lib/proof_of_service.py``
Canonical blank: ``_form-library/proof-of-service-blank-template.pdf``

Usage:
  python3 internal/scripts/generate-proof-of-service.py
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from proof_of_service import (  # noqa: E402
    ProofOfServiceFields,
    build_proof_of_service,
    write_blank_template,
)

ROOT = SCRIPT_DIR.parent
OUT_MEZA = (
    ROOT
    / "public/documents/matter-32/ndcal"
    / "Proof of Service - FAC Dkt 05 Mailed to Melano (Aug 21 2026).pdf"
)
OUT_CAND = (
    ROOT
    / "public/documents/matter-33/ndcal"
    / "Proof of Service - FAC Dkt 06 Mailed to Candelaria and Gordon (Aug 21 2026).pdf"
)


def meza_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGWA NFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "SANTIAGO MEZA-GONZALEZ;",
            "JOSE MELANO; and DOES 1-10",
        ],
        defendant_role="Defendants",
        case_number="3:26-cv-08271-PHK",
        title="PROOF OF SERVICE",
        service_date="August 21, 2026",
        document_title="First Amended Complaint for Damages (Dkt. 5)",
        mailing_location="San Jose, California",
        recipients=[
            "Officer Jose Melano (CHP Badge #023054)",
            "California Highway Patrol, South Sacramento Area",
            "6 Massie Court",
            "Sacramento, CA 95823",
        ],
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
    )


def candelaria_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGWA NFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "DIANA CANDELARIA, individually;",
            "STEVE GORDON, officially; and DOES 1-10",
        ],
        defendant_role="Defendants",
        case_number="3:26-cv-08272-LJC",
        title="PROOF OF SERVICE",
        service_date="August 21, 2026",
        document_title="First Amended Complaint for Damages and Injunctive Relief (Dkt. 6)",
        mailing_location="San Jose, California",
        recipients=[
            "Diana Candelaria, Driver Safety Hearing Officer",
            "California Department of Motor Vehicles",
            "Legal Affairs Division, Mail Station C128",
            "2415 First Avenue",
            "Sacramento, CA 95818",
            "",
            "Steve Gordon, Director",
            "California Department of Motor Vehicles",
            "Legal Affairs Division, Mail Station C128",
            "2415 First Avenue",
            "Sacramento, CA 95818",
        ],
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
    )


def main() -> None:
    blank = write_blank_template()
    print(f"Wrote {blank}")
    for path, fields in ((OUT_MEZA, meza_fields()), (OUT_CAND, candelaria_fields())):
        build_proof_of_service(path, fields)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
