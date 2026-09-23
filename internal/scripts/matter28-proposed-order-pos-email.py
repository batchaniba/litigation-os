#!/usr/bin/env python3
"""Matter 28 -- Proof of Service (by e-mail) for Plaintiff's [Proposed] Order
Denying Defendants' Motion to Dismiss.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Plaintiff serves the [Proposed] Order (companion to the Opposition served
September 22, 2026) on opposing counsel of record at Sims, Lawrence &
Broghammer by electronic mail on September 23, 2026. Uses the house
four-border Proof of Service (lib/proof_of_service) with the universal
signature stamped, then appends it behind the order as one packet.
Service list matches matter28-opposition-pos-email.py (Defendants' MTD
signature block, ECF Doc. 15, and certificate of service, Doc. 18).

    python3 internal/scripts/matter28-proposed-order-pos-email.py
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
DOCS = ROOT / "public/documents/matter-28"
ORDER = DOCS / "Proposed Order Denying MTD (N.D. Cal. 3-26-cv-07504-LJC) (Sep 23 2026).pdf"
OUT = DOCS / "Proof of Service by Email - Proposed Order Denying MTD (N.D. Cal. 3-26-cv-07504-LJC) (Sep 23 2026).pdf"
OUT_PACKET = DOCS / "Proposed Order Denying MTD with POS (N.D. Cal. 3-26-cv-07504-LJC) (Sep 23 2026).pdf"
SCRATCH = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "fde9b68e-7f08-5546-b231-a91ce9f193c5/scratchpad/"
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
        service_date="September 23, 2026",
        document_title="[PROPOSED] ORDER DENYING DEFENDANTS' MOTION TO DISMISS",
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


def merge_packet(pos_path: Path) -> None:
    import pymupdf
    if not ORDER.is_file():
        print(f"Missing {ORDER} - skipped packet")
        return
    merged = pymupdf.open()
    for src in (ORDER, pos_path):
        doc = pymupdf.open(src)
        merged.insert_pdf(doc)
        doc.close()
    for out in (OUT_PACKET, SCRATCH / "Proposed-Order-Denying-MTD-with-POS-Sep23.pdf"):
        merged.save(out)
        print(f"Wrote {out} ({merged.page_count} pages)")
    merged.close()


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
    path = build_proof_of_service(OUT, pos_fields())
    print(f"Wrote {path} ({path.stat().st_size} bytes)")
    merge_packet(path)


if __name__ == "__main__":
    main()
