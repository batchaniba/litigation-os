#!/usr/bin/env python3
"""Fill the E.D. Cal. Consent / Decline of U.S. Magistrate Judge form for Matter 25.

Source page is Dkt. 3 page 4 — the court-captioned form the Clerk attached to
the FedEx removal packet (2:26-cv-02881-DAD-SCR). The N.D. Cal. template in
``_form-library/ndcal-mj-consent-declination-blank-template.pdf`` is the wrong
district for this case.

House practice in Matters 24 / 32 / 33 is CONSENT. This script checks the
CONSENT box (not DECLINE), stamps the canonical signature, and appends the
portfolio four-sided-border Proof of Service for mail on Allison A. Kray.

    python3 internal/scripts/matter25-edcal-mj-consent.py \\
        [--date "August 28, 2026"] [--mailed-from "San Jose, California"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pdf_packet import assemble  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_EDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_PATH, stamp_on_pdf_line  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
SRC = (
    ROOT
    / "internal/public/documents/matter-25"
    / "Dkt 03 - Magistrate Judge Consent Form Materials (Filed Aug 25 2026).pdf"
)
OUT_DIR = ROOT / "internal/public/documents/matter-25"
DEFAULT_OUT = OUT_DIR / (
    "Consent to Magistrate Judge Jurisdiction - "
    "Federal Express (E.D. Cal. 2-26-cv-02881) (Aug 28 2026).pdf"
)
DEFAULT_POS = OUT_DIR / (
    "Proof of Service - Consent to Magistrate Judge Jurisdiction - "
    "FedEx (E.D. Cal. 2-26-cv-02881) (Aug 28 2026).pdf"
)

DEFAULT_DATE = "August 28, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
PRINT_NAME = "BRENDAN NGEHSI NEWANFORBI"

# PyMuPDF top-origin coords on Dkt. 3 p. 4 (CONSENT box, not DECLINE).
DATE_POS = (105.0, 481.0)
NAME_POS = (300.0, 503.0)
PLAINTIFF_CHECK = (297.5, 516.5)
SIG_LINE = (288.8, 459.3, 483.4)


def fill_consent_page(out: Path, exec_date: str) -> Path:
    import fitz

    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    if not SRC.is_file():
        raise SystemExit(f"Missing court form: {SRC}")

    src = fitz.open(SRC)
    dst = fitz.open()
    dst.insert_pdf(src, from_page=3, to_page=3)
    src.close()
    page = dst[0]

    page.insert_text(
        DATE_POS, exec_date, fontname="times-roman", fontsize=10, color=(0, 0, 0)
    )
    page.insert_text(
        NAME_POS, PRINT_NAME, fontname="times-roman", fontsize=9, color=(0, 0, 0)
    )
    page.insert_text(
        PLAINTIFF_CHECK, "X", fontname="times-bold", fontsize=11, color=(0, 0, 0)
    )
    stamp_on_pdf_line(page, SIG_LINE[0], SIG_LINE[1], SIG_LINE[2])

    out.parent.mkdir(parents=True, exist_ok=True)
    dst.save(out, garbage=4, deflate=True)
    dst.close()
    return out


def build_pos(out: Path, exec_date: str, mailed_from: str) -> Path:
    return build_proof_of_service(
        out,
        ProofOfServiceFields(
            plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
            plaintiff_role="Plaintiff",
            defendant_lines=["FEDERAL EXPRESS CORPORATION"],
            defendant_role="Defendant",
            case_number="2:26-cv-02881-DAD-SCR",
            district_line=DISTRICT_EDCAL,
            title="PROOF OF SERVICE",
            service_date=exec_date,
            document_title=(
                "Consent to Jurisdiction of United States Magistrate Judge"
            ),
            mailing_location=mailed_from,
            recipients=[
                "Allison A. Kray, Esq. (SBN 312544)",
                "FEDERAL EXPRESS CORPORATION",
                "2601 Main Street, Suite 1100",
                "Irvine, CA 92614",
                "Attorney for Defendant Federal Express Corporation",
            ],
            server_name="Brendan Ngehsi Newanforbi",
            stamp_signature=True,
        ),
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=DEFAULT_DATE)
    ap.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--pos-out", default=str(DEFAULT_POS))
    args = ap.parse_args()
    path = fill_consent_page(Path(args.out).resolve(), args.date)
    pos = build_pos(Path(args.pos_out).resolve(), args.date, args.mailed_from)
    assemble([path, pos], path)
    print(f"Generated consent (POS attached): {path}")
    print(f"Generated proof of service: {pos}")


if __name__ == "__main__":
    main()
