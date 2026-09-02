#!/usr/bin/env python3
"""Fill the N.D. Cal. Consent or Declination to Magistrate Judge Jurisdiction
form for Matter 29 (Amazon).

Source is ``_form-library/ndcal-mj-consent-declination-blank-template.pdf``.
House practice in Matters 24 / 32 / 33 is CONSENT. This script checks CONSENT
(not DECLINE), stamps the canonical signature, and appends the portfolio
Proof of Service for mail on Frederick (Amazon) and Stanzick (Accurate).

    python3 internal/scripts/matter29-ndcal-mj-consent.py \\
        [--date "September 1, 2026"] [--mailed-from "San Jose, California"]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pdf_packet import assemble  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_PATH, stamp_on_pdf_line  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
SRC = (
    ROOT
    / "internal/public/documents/_form-library"
    / "ndcal-mj-consent-declination-blank-template.pdf"
)
OUT_DIR = ROOT / "internal/public/documents/matter-29"
DEFAULT_OUT = OUT_DIR / (
    "Consent to Magistrate Judge Jurisdiction - "
    "Amazon (N.D. Cal. 3-26-cv-09249-ASK) (Sep 1 2026).pdf"
)
DEFAULT_POS = OUT_DIR / (
    "Proof of Service - Consent to Magistrate Judge Jurisdiction - "
    "Amazon (N.D. Cal. 3-26-cv-09249-ASK) (Sep 1 2026).pdf"
)

DEFAULT_DATE = "September 1, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
ARTIFACTS_DIR = Path("/opt/cursor/artifacts")
ARTIFACT_PDF = ARTIFACTS_DIR / "amazon_mj_consent_with_pos.pdf"
SHORT_LINK_SLUG = "amazon-consent"
PRINT_NAME = "BRENDAN NGEHSI NEWANFORBI"
PRINT_NAME_MIXED = "Brendan Ngehsi Newanforbi"
CASE_NO = "3:26-cv-09249-ASK"
DEFENDANT = "AMAZON.COM SERVICES, LLC, et al."

# DATE / YEAR / NAME sit on the printed "DATE: ____, 20__  NAME:" rule.
# PyMuPDF top-origin: the printed baseline is ~y=566. ProSe sits on
# "COUNSEL FOR (OR “PRO SE”):" at ~y=632. The ProSe widget is a tall box
# that would otherwise dump the letters at the top of the box.
DATE_BASELINE = 566.4
PROSE_BASELINE = 631.8

# Signature widget (346.2, 574.5, 546.4, 596.5). Stamp sits on the rule.
# stamp_on_pdf_line(page, x0, x1, y_line)
SIG_LINE = (350.0, 520.0, 596.4)


def _draw_times(page, text: str, x: float, baseline: float, size: float = 10) -> None:
    import fitz

    page.insert_text(
        fitz.Point(x, baseline),
        text,
        fontsize=size,
        fontname="tiro",
        color=(0, 0, 0),
    )


def fill_consent_page(out: Path, exec_date: str) -> Path:
    import fitz

    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    if not SRC.is_file() or SRC.stat().st_size < 10_000:
        raise SystemExit(f"Missing court form: {SRC}")

    # Form prints "DATE: _______________, 20____"
    # "September 1, 2026" → DATE "September 1" / YEAR "26"
    date_part, _, year = exec_date.rpartition(",")
    date_part = date_part.strip() or exec_date
    year = year.strip()
    year_yy = year[-2:] if len(year) >= 2 else year

    doc = fitz.open(SRC)
    page = doc[0]

    for w in page.widgets():
        name = w.field_name
        if name == "Plaintiff Name(s)":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = PRINT_NAME
        elif name == "Defendant Name(s)":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = DEFENDANT
        elif name == "Case number":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = CASE_NO
        elif name == "Consent to Magistrate Judge Jurisdiction":
            w.field_value = w.on_state()
        elif name == "Decline Magistrate Judge Jurisdiction":
            w.field_value = "Off"
        elif name in {"DATE", "YEAR", "NAME", "ProSe", "sig"}:
            # Drawn after bake so they sit on the printed rules.
            w.field_value = ""
        elif name == "Reset Form":
            continue
        w.update()

    # Drop the template's Reset Form button so it does not print.
    for w in list(page.widgets() or []):
        if w.field_name == "Reset Form":
            page.delete_widget(w)

    doc.bake(annots=True, widgets=True)

    # Caption names survive bake. Date / name / PRO SE are drawn on the rules.
    _draw_times(page, date_part, 116.0, DATE_BASELINE, 10)
    _draw_times(page, year_yy, 228.5, DATE_BASELINE, 10)
    _draw_times(page, PRINT_NAME_MIXED, 348.0, DATE_BASELINE, 9)
    _draw_times(page, "PRO SE", 348.0, PROSE_BASELINE, 10)

    stamp_on_pdf_line(page, SIG_LINE[0], SIG_LINE[1], SIG_LINE[2], whiteout=False)

    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return out


def build_pos(out: Path, exec_date: str, mailed_from: str) -> Path:
    return build_proof_of_service(
        out,
        ProofOfServiceFields(
            plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
            plaintiff_role="Plaintiff",
            defendant_lines=[
                "AMAZON.COM SERVICES, LLC;",
                "ACCURATE BACKGROUND LLC",
            ],
            defendant_role="Defendants",
            case_number=CASE_NO,
            district_line=DISTRICT_NDCAL,
            title="PROOF OF SERVICE",
            service_date=exec_date,
            document_title=(
                "Consent or Declination to Magistrate Judge Jurisdiction (CONSENT)"
            ),
            mailing_location=mailed_from,
            recipients=[
                "Andrew P. Frederick, Esq. (SBN 284832)",
                "Morgan, Lewis & Bockius LLP",
                "1400 Page Mill Road",
                "Palo Alto, CA 94304",
                "Attorneys for Defendant Amazon.com Services, LLC",
                "",
                "Jasmine J. Stanzick, Esq. (SBN 354704)",
                "Seyfarth Shaw LLP",
                "2029 Century Park East, Suite 3500",
                "Los Angeles, CA 90067-3021",
                "Attorneys for Defendant Accurate Background LLC",
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
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, ARTIFACT_PDF)
    short = publish_short_link(path, SHORT_LINK_SLUG)
    print(f"Generated consent (POS attached): {path}")
    print(f"Generated proof of service: {pos}")
    print(f"Download copy: {ARTIFACT_PDF}")
    print(f"Short link copy: {short}")


if __name__ == "__main__":
    main()
