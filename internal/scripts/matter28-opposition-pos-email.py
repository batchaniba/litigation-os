#!/usr/bin/env python3
"""Matter 28 -- Proof of Service (by e-mail) for Plaintiff's Opposition to MTD.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Plaintiff serves the Opposition to Defendants' Motion to Dismiss on opposing
counsel of record at Sims, Lawrence & Broghammer by electronic mail on
September 22, 2026. Uses the house four-border Proof of Service
(lib/proof_of_service) with the universal signature stamped. Nothing mailed.

Counsel of record and e-mail addresses are taken from Defendants' own MTD
signature block (ECF Doc. 15) and certificate of service (Doc. 18).

    python3 internal/scripts/matter28-opposition-pos-email.py
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
    "Proof of Service by Email - Opposition to MTD "
    "(N.D. Cal. 3-26-cv-07504-LJC) (Sep 22 2026).pdf"
)
SCRATCH_OUT = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "3fd8a963-2d26-598c-823f-b47c1b152f34/scratchpad/"
    "Proof-of-Service-by-Email-Opposition-to-MTD-Sep22.pdf"
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
        service_date="September 22, 2026",
        document_title="PLAINTIFF'S OPPOSITION TO DEFENDANTS' MOTION TO DISMISS",
        recipients=[
            "Cynthia G. Lawrence, Esq. — cynthia@sims-law.net",
            "Blaze Van Dine, Esq. — blaze@sims-law.net",
            "Eric T. Martinez, Esq. — emartinez@sims-law.net",
            "Sims, Lawrence & Broghammer (e-service) — SLB@sims-law.net; "
            "slb-eservice@sims-law.net",
            "",
            "Attorneys for Defendants Shannon Smith, LCSW, and",
            "HOPE Psychotherapy, Inc. (d/b/a HOPE Program)",
        ],
        server_name=SERVER,
        stamp_signature=True,
        district_line=DISTRICT_NDCAL,
        by_email=True,
    )


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    for out in (OUT, SCRATCH_OUT):
        path = build_proof_of_service(out, pos_fields())
        print(f"Wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
