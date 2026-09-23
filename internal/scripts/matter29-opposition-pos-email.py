#!/usr/bin/env python3
"""Matter 29 -- Proof of Service (by e-mail) for Plaintiff's Opposition to
Amazon's Motion to Dismiss.

Newanforbi v. Amazon.com Services, LLC, et al., N.D. Cal. No. 4:26-cv-09249-ASK.

Plaintiff serves the Opposition on counsel of record for both defendants by
electronic mail on September 23, 2026. Uses the house four-border Proof of
Service (lib/proof_of_service) with the universal signature stamped. Nothing
mailed.

Amazon counsel and e-mail addresses are taken from Amazon's MTD signature block
and certificate of service (Dkt. 19, 19-2); Douglass G. Brown's pro hac vice
application was granted September 22, 2026 (Dkt. 18). Seyfarth addresses are
from Plaintiff's Civil L.R. 3-15 proof of service (Dkt. 13) and the Accurate
extension correspondence.

    python3 internal/scripts/matter29-opposition-pos-email.py
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
    "public/documents/matter-29/"
    "Proof of Service by Email - Opposition to Amazon MTD "
    "(N.D. Cal. 4-26-cv-09249-ASK) (Sep 23 2026).pdf"
)
SCRATCH_OUT = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "fde9b68e-7f08-5546-b231-a91ce9f193c5/scratchpad/"
    "Proof-of-Service-by-Email-Opposition-to-Amazon-MTD-Sep23.pdf"
)

CASE = "4:26-cv-09249-ASK"
PLAINTIFF = "BRENDAN NGEHSI NEWANFORBI"
SERVER = "Brendan Ngehsi Newanforbi"


def pos_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line=PLAINTIFF,
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "AMAZON.COM SERVICES, LLC;",
            "ACCURATE BACKGROUND, LLC; and",
            "DOES 1-10, inclusive",
        ],
        defendant_role="Defendants",
        case_number=CASE,
        title="PROOF OF SERVICE",
        service_date="September 23, 2026",
        document_title=(
            "PLAINTIFF'S OPPOSITION TO DEFENDANT AMAZON.COM SERVICES LLC'S "
            "MOTION TO DISMISS PLAINTIFF'S FIFTH, SIXTH, AND SEVENTH CLAIMS FOR RELIEF"
        ),
        recipients=[
            "Andrew P. Frederick, Esq. — andrew.frederick@morganlewis.com",
            "Douglass G. Brown, Esq. — douglass.brown@morganlewis.com",
            "Morgan, Lewis & Bockius LLP",
            "Attorneys for Defendant Amazon.com Services LLC",
            "",
            "Jasmine J. Stanzick, Esq. — jstanzick@seyfarth.com",
            "John W. Drury, Esq. — jdrury@seyfarth.com",
            "Seyfarth Shaw LLP",
            "Attorneys for Defendant Accurate Background, LLC",
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
