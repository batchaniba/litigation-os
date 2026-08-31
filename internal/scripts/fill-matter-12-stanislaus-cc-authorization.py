#!/usr/bin/env python3
"""Fill the Stanislaus County Sheriff Civil Division Credit Card Authorization
for Matter 12 Diamond Truck Sales re-service (printing charge only).

Unlocked PDF — no password. Sheriff service fee is covered by the FW-003
already on file; this authorization is for printing at $1.25/side/page.
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

UNLOCKED_NAME = "Stanislaus-CC-Authorization-Diamond-Truck-Sales-Aug31-2026.pdf"

# Same portfolio card as fill-matter-32-stanislaus-cc-authorization.py.
CARDHOLDER = "Brendan Ngwa Nforbi"
CARD_NUMBER = "5143 7734 2833 2398"
CARD_CVV = "575"
CARD_EXP = "09/29"
BILLING_STREET = "1455 Cat Tail Drive"
BILLING_CITY = "Stockton"
BILLING_STATE = "CA"
BILLING_ZIP = "95204"
BILLING_PHONE = "(209) 801-4442"

ATTACHMENT_DATE = "August 31, 2026"
SIG_DATE = "August 31, 2026"
DESCRIBE = (
    "Print/serve Amended Summons & FAC — Diamond Truck Sales, Inc. "
    "(as sued), Turlock (STK-CV-UF-2026-0001094)"
)

# Papers the deputy prints to serve (SER-001 / FW-003 stay with the file):
#   Amended Summons (SUM-100)     1 p.
#   First Amended Complaint      34 pp.
PAGE_COUNT = 1 + 34  # 35
PRICE_PER_PAGE = 1.25
PAYMENT_AMOUNT = PAGE_COUNT * PRICE_PER_PAGE  # $43.75

FIELDS = [
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

SIG_RECT = fitz.Rect(248.0, 552.0, 378.0, 583.0)


def fill(out_path: Path) -> None:
    doc = fitz.open(TEMPLATE)
    page = doc[0]
    for text, x, y, size in FIELDS:
        page.insert_text((x, y), text, fontname="helv", fontsize=size, color=(0, 0, 0))
    height = (SIG_RECT.x1 - SIG_RECT.x0) * SIGNATURE_ASPECT
    sig_rect = fitz.Rect(SIG_RECT.x0, SIG_RECT.y1 - height, SIG_RECT.x1, SIG_RECT.y1)
    page.insert_image(sig_rect, filename=SIGNATURE_PATH, keep_proportion=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path, garbage=4, deflate=True)
    doc.close()


def verify(path: Path) -> None:
    doc = fitz.open(path)
    text = doc[0].get_text()
    doc.close()
    checks = [CARDHOLDER, f"{PAYMENT_AMOUNT:.2f}", ATTACHMENT_DATE, "Diamond"]
    missing = [c for c in checks if c not in text]
    print(f"{path.name}: {'OK' if not missing else 'MISSING ' + str(missing)}")


def main() -> None:
    if not TEMPLATE.is_file() or TEMPLATE.stat().st_size < 10_000:
        raise SystemExit(f"Bad/missing template: {TEMPLATE}")
    print(
        f"Page count: {PAGE_COUNT} pp. -> printing fee ${PAYMENT_AMOUNT:.2f} "
        "(plus card processing fee per the form's own table); unlocked, no password"
    )
    unlocked = OUT_DIR / UNLOCKED_NAME
    fill(unlocked)
    verify(unlocked)


if __name__ == "__main__":
    main()
