#!/usr/bin/env python3
"""Fill the E.D. Cal. Consent / Decline of U.S. Magistrate Judge form for Matter 25.

Source is the court's fillable web form (consentmagweb), stored at
``_form-library/edcal-mj-consent-declination-blank-template.pdf``. Do not overlay
Dkt. 3 page 4 — that copy is already filed, and it is not the fillable form.

House practice in Matters 24 / 32 / 33 is CONSENT. This script checks the
CONSENT box (not DECLINE), marks Plaintiff/Petitioner, stamps the canonical
signature, and appends the portfolio four-sided-border Proof of Service for
mail on Allison A. Kray.

    python3 internal/scripts/matter25-edcal-mj-consent.py \\
        [--date "August 28, 2026"] [--mailed-from "San Jose, California"]
"""

from __future__ import annotations

import argparse
import re
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
    / "internal/public/documents/_form-library"
    / "edcal-mj-consent-declination-blank-template.pdf"
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
CASE_NO = "2:26-cv-02881-DAD-SCR"
DEFENDANT = "FEDERAL EXPRESS CORPORATION"

# Consent Signature widget is (306.4, 419.1, 487.4, 441.1). Stamp starts
# right of the "Signature:" label; y sits on the rule without covering
# Print Name (field begins at y=444.3). Skip white-out so the rule remains.
SIG_LINE = (320.0, 487.4, 444.0)


def _parent_xref(doc, kid_xref: int) -> int | None:
    m = re.search(r"/Parent (\d+) 0 R", doc.xref_object(kid_xref))
    return int(m.group(1)) if m else None


def fill_consent_page(out: Path, exec_date: str) -> Path:
    import fitz

    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    if not SRC.is_file() or SRC.stat().st_size < 10_000:
        raise SystemExit(f"Missing court form: {SRC}")

    doc = fitz.open(SRC)
    page = doc[0]
    g6_parent = g7_parent = None

    for w in page.widgets():
        name = w.field_name
        if name == "PlaintiffsPetitioners":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = PRINT_NAME
        elif name == "CASE NO":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = CASE_NO
        elif name == "DefendantsRespondents":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = DEFENDANT
        elif name == "Consent Check":
            w.field_value = w.on_state()
        elif name == "Decline Check":
            w.field_value = "Off"
        elif name == "Date":
            w.text_fontname = "tiro"
            w.text_fontsize = 10
            w.field_value = exec_date
        elif name == "Print Name":
            w.text_fontname = "tiro"
            w.text_fontsize = 9
            w.field_value = PRINT_NAME
        elif name == "Group6":
            # Blank template defaults this group to Defendant. Force Plaintiff.
            w.field_value = w.on_state() if w.on_state() == "Pltf" else "Off"
            g6_parent = _parent_xref(doc, w.xref)
        elif name == "Group7":
            # Blank template defaults this group to Plaintiff. Leave empty.
            w.field_value = "Off"
            g7_parent = _parent_xref(doc, w.xref)
        elif w.field_type_string == "Text":
            w.field_value = ""
        w.update()

    # Widget.update() does not always clear leftover /AS on the sibling
    # radios. Patch appearance states and parent /V before bake.
    for w in page.widgets():
        if w.field_name == "Group6":
            doc.xref_set_key(
                w.xref, "AS", "/Pltf" if w.on_state() == "Pltf" else "/Off"
            )
        elif w.field_name == "Group7":
            doc.xref_set_key(w.xref, "AS", "/Off")
    if g6_parent:
        doc.xref_set_key(g6_parent, "V", "/Pltf")
    if g7_parent:
        doc.xref_set_key(g7_parent, "V", "/Off")

    doc.bake(annots=True, widgets=True)
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
