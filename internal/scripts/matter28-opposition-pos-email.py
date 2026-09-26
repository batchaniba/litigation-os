#!/usr/bin/env python3
"""Matter 28 -- Proof of Service (by e-mail) for Plaintiff's Opposition to MTD.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

The September 22, 2026 Opposition POS already served is historical. Do not
overwrite that PDF. Any regenerated or later Matter 28 POS uses the September
26, 2026 addressee list in lib/matter28_service.py:

    Eric T. Martinez, Kim Schmitt, June Meinecke, Amber Krausse,
    slb-eservice@sims-law.net

    python3 internal/scripts/matter28-opposition-pos-email.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from matter28_service import POS_RECIPIENTS  # noqa: E402
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
# Historical output path kept so a rerun does not invent a second filename.
# Do not file a regenerated copy over the served Sep. 22 POS.

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
        recipients=POS_RECIPIENTS,
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
    print("NOTE: Sep. 22 served POS is historical. Use POS_RECIPIENTS for new papers.")


if __name__ == "__main__":
    main()
