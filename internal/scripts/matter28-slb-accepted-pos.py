#!/usr/bin/env python3
"""Matter 28 — executed Proof of Service after SLB accepted Rule 4 service.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Blaze Van Dine (Sims, Lawrence & Broghammer) emailed on September 1, 2026 that
he accepts service on behalf of both defendants effective August 31, 2026.
This fills and stamps the house Proof of Service for that e-mail service
(slb-eservice@sims-law.net / blaze@sims-law.net). Nothing was mailed.
One combined issued AO 440 named both defendants. Do not attach the Gmail
thread as an exhibit. Do not overwrite the blank-dated
06_Proof_of_Service_Electronic_Delivery_to_SLB.pdf in the service packet.

    python3 internal/scripts/matter28-slb-accepted-pos.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_PATH  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / (
    "public/documents/matter-28/"
    "Proof of Service - SLB Accepted Service for Smith and HOPE "
    "(N.D. Cal. 3-26-cv-07504-LJC) (Sep 2 2026).pdf"
)

CASE = "3:26-cv-07504-LJC"
PLAINTIFF = "BRENDAN NGEHSI NEWANFORBI"
SERVER = "Brendan Ngehsi Newanforbi"


def pos_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line=PLAINTIFF,
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "SHANNON SMITH, LCSW;",
            "HOPE PSYCHOTHERAPY, INC.",
        ],
        defendant_role="Defendants",
        case_number=CASE,
        title="PROOF OF SERVICE",
        service_date="August 31, 2026",
        document_title=(
            "Issued Summons (AO 440) as to Shannon Smith, LCSW, and HOPE "
            "Psychotherapy, Inc. d/b/a HOPE Program; Complaint (Dkt. 1); Civil "
            "Cover Sheet (Dkt. 1-1); Order Setting Initial Case Management "
            "Conference and ADR Deadlines (Dkt. 4); and Order Regarding Payment "
            "of Filing Fee and Directing Service (Dkt. 11)"
        ),
        recipients=[
            "Sims, Lawrence & Broghammer e-service — slb-eservice@sims-law.net",
            "Blaze Van Dine, Esq. — blaze@sims-law.net",
            "Counsel for Shannon Smith, LCSW, and HOPE Psychotherapy, Inc.",
            "(Accepted service for both defendants effective August 31, 2026)",
        ],
        server_name=SERVER,
        stamp_signature=True,
        district_line=DISTRICT_NDCAL,
        by_email=True,
    )


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    path = build_proof_of_service(OUT, pos_fields())
    print(f"Wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
