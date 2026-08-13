#!/usr/bin/env python3
"""Fill the Stanislaus County Sheriff Civil Division Credit Card Authorization
form for the Meza-Gonzalez SER-001 (Matter 32).

The blank template (internal/public/documents/_form-library/
stanislaus-cc-authorization-blank-template.pdf) is the Department's own form,
supplied directly by Plaintiff. It is not a fillable AcroForm — every field is
drawn as overlay text at fixed coordinates, matching the layout the Department
used on the prior Matter 12 (Diamond/Alpine Truck Sales) authorization.

Card/billing constants are the same portfolio-canonical card used on that
Matter 12 authorization (internal/handoff/Stanislaus-Civil-Credit-Card-
Authorization-Aug3-2026-PASSWORD.pdf) — reused here rather than introduced.

Payment Amount is the printing charge only ($1.25/side/page, per the
Department's Aug. 2026 Civil Fax reply), computed from the actual page count
of the papers enclosed with the Meza-Gonzalez SER-001. The credit card
processing fee is NOT pre-added to Payment Amount — the form's own fee table
covers that, matching the Matter 12 precedent.

Produces the unlocked (reviewable) PDF only. The password-protected copy for
email attachment is generated separately, out of this script, so its password
is never written to a file tracked by this repository.
"""

from __future__ import annotations

import sys
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "internal/public/documents/_form-library/stanislaus-cc-authorization-blank-template.pdf"
OUT_DIR = ROOT / "internal/handoff"

UNLOCKED_NAME = "Stanislaus-CC-Authorization-Meza-Gonzalez-Aug12-2026.pdf"

# ---- portfolio-canonical card/billing constants (same card used on the
# Matter 12 Stanislaus authorization) -----------------------------------
CARDHOLDER = "Brendan Ngwa Nforbi"
CARD_NUMBER = "5143 7734 2833 2398"
CARD_CVV = "575"
CARD_EXP = "09/29"
BILLING_STREET = "1455 Cat Tail Drive"
BILLING_CITY = "Stockton"
BILLING_STATE = "CA"
BILLING_ZIP = "95204"
BILLING_PHONE = "(209) 801-4442"

# ---- per-request fields -------------------------------------------------
ATTACHMENT_DATE = "August 12, 2026"
SIG_DATE = "August 12, 2026"
DESCRIBE = (
    "Serve Summons & Complaint on Santiago Meza-Gonzalez, CHP Modesto "
    "Area, Modesto (3:26-cv-08271-PHK)"
)

# Enclosed papers (Meza-Gonzalez packet only — his own Dkt. 3 summons page,
# not Melano's, who is served separately in Sacramento):
#   Complaint (Dkt. 1)             31 pp.
#   Dkt. 1-1 Filing Fee Receipt     1 p.
#   Dkt. 1-2 JS-CAND 44 Cover Sheet 1 p.
#   Dkt. 3 Summons (his page only)  1 p.
#   Dkt. 4 CMC/ADR Order            2 pp.
PAGE_COUNT = 31 + 1 + 1 + 1 + 2  # 36
PRICE_PER_PAGE = 1.25
PAYMENT_AMOUNT = PAGE_COUNT * PRICE_PER_PAGE  # $45.00

# (x, y) = PyMuPDF top-left-origin baseline coordinates, matched against the
# blank template's static label positions.
FIELDS = [
    # (text, x, y, size)
    ("X", 119.5, 234.5, 11),
    (CARDHOLDER, 248.0, 256.5, 10),
    (CARD_NUMBER, 135.0, 278.5, 10),
    (CARD_CVV, 178.0, 300.5, 10),
    (CARD_EXP, 438.0, 300.5, 10),
    (BILLING_STREET, 190.0, 319.5, 10),
    (BILLING_CITY, 180.0, 339.0, 10),
    (BILLING_STATE, 390.0, 339.0, 10),
    (BILLING_ZIP, 470.0, 339.0, 10),
    (BILLING_PHONE, 232.0, 358.5, 10),
    (f"{PAYMENT_AMOUNT:.2f}", 160.0, 382.5, 11),
    (CARDHOLDER, 78.0, 413.5, 9),
    (ATTACHMENT_DATE, 272.0, 490.5, 9),
    (DESCRIBE, 115.0, 504.5, 8),
    (CARDHOLDER, 64.0, 576.5, 10),
    (SIG_DATE, 424.0, 576.5, 10),
]

# Signature line (PyMuPDF top-origin), same box the Department's own copy used.
SIG_RECT = fitz.Rect(248.0, 552.0, 378.0, 583.0)


def fill(out_path: Path) -> None:
    doc = fitz.open(TEMPLATE)
    page = doc[0]
    for text, x, y, size in FIELDS:
        page.insert_text((x, y), text, fontname="helv", fontsize=size, color=(0, 0, 0))
    height = (SIG_RECT.x1 - SIG_RECT.x0) * SIGNATURE_ASPECT
    sig_rect = fitz.Rect(SIG_RECT.x0, SIG_RECT.y1 - height, SIG_RECT.x1, SIG_RECT.y1)
    page.insert_image(sig_rect, filename=SIGNATURE_PATH, keep_proportion=True)
    doc.save(out_path)
    doc.close()


def verify(path: Path) -> None:
    doc = fitz.open(path)
    text = doc[0].get_text()
    doc.close()
    checks = [CARDHOLDER, f"{PAYMENT_AMOUNT:.2f}", ATTACHMENT_DATE, "Meza-Gonzalez"]
    missing = [c for c in checks if c not in text]
    print(f"{path.name}: {'OK' if not missing else 'MISSING ' + str(missing)}")


def main() -> None:
    if not TEMPLATE.is_file() or TEMPLATE.stat().st_size < 10_000:
        raise SystemExit(f"Bad/missing template: {TEMPLATE}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Page count: {PAGE_COUNT} pp. -> printing fee ${PAYMENT_AMOUNT:.2f} "
          f"(plus card processing fee per the form's own table)")

    unlocked = OUT_DIR / UNLOCKED_NAME
    fill(unlocked)
    verify(unlocked)
    print("Done. Password-protect a copy separately for email attachment —")
    print("see internal/handoff/README or run the lock step out of version control.")


if __name__ == "__main__":
    main()
