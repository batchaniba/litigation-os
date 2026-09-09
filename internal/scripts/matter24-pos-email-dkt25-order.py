#!/usr/bin/env python3
"""Matter 24 - Proof of Service (by e-mail) for the Dkt. 25 order transmittal.

Uses the portfolio's canonical bordered federal POS form
(``internal/scripts/lib/proof_of_service.py``) with ``by_email=True``,
matching matter24-rule26-and-jcms.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
OUT = (
    ROOT
    / "public/documents/matter-24"
    / "Proof of Service by Email - Dkt 25 Order Continuing Initial CMC (Sep 9 2026).pdf"
)

EXEC_DATE = "September 9, 2026"


def pos_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "CAPTAIN G. SERRATO, in his individual",
            "and official capacities as Commander,",
            "Dublin Area, California Highway Patrol",
        ],
        defendant_role="Defendant",
        case_number="4:26-cv-05953-ASK",
        title="PROOF OF SERVICE",
        service_date=EXEC_DATE,
        document_title=(
            "Plaintiff's correspondence regarding the Order entered September 9, "
            "2026 (Dkt. 25) continuing the initial case management conference, and "
            "the Joint Stipulation to Continue Initial Case Management Conference "
            "and Order (Dkt. 25)"
        ),
        recipients=[
            "Haiyang A. Li, Deputy Attorney General — Haiyang.Li@doj.ca.gov",
            "Office of the Attorney General, 300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Attorney for Defendant Captain G. Serrato",
        ],
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=True,
        district_line=DISTRICT_NDCAL,
        by_email=True,
    )


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    out = build_proof_of_service(OUT, pos_fields())
    print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
