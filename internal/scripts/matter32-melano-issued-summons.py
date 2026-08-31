#!/usr/bin/env python3
"""Extract the clerk-issued Melano AO 440 (Dkt. 3 p.1) as a standalone PDF.

Matter 32 — Nforbi v. Meza-Gonzalez, et al., N.D. Cal. No. 3:26-cv-08271-PHK.

Dkt. 3 is the two-defendant issued summons (filed Aug. 10, 2026):
  page 1 (index 0) = Jose Melano @ CHP South Sacramento Area, 6 Massie Court
  page 2 (index 1) = Santiago Meza-Gonzalez @ CHP Modesto Area

This writes Melano's issued page only. It is not a new issuance — Date,
Deputy Clerk (Charles Ho / Mark B. Busby), and the case number are already
on the clerk-stamped original. Melano Rule 4 POS is separately on file as
Dkt. 5-1 (filed Aug. 17).
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfWriter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pdf_packet import append_page, page_count  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
NDCAL = ROOT / "internal/public/documents/matter-32/ndcal"

SUMMONS_ISSUED = NDCAL / "Dkt 03 - Summons Issued - Meza-Gonzalez and Melano (Aug 10 2026).pdf"
# Dkt. 3 page index 0 = Melano (CHP South Sacramento / 6 Massie Court).
MELANO_SUMMONS_PAGE = 0

OUT = NDCAL / "Summons Issued - Jose Melano only (N.D. Cal. Dkt. 3) (Aug 10 2026).pdf"


def main() -> None:
    if not SUMMONS_ISSUED.is_file() or SUMMONS_ISSUED.stat().st_size < 1000:
        raise SystemExit(f"Missing or empty: {SUMMONS_ISSUED}")
    n = page_count(SUMMONS_ISSUED)
    if n < 2:
        raise SystemExit(f"Expected 2-page issued summons, got {n}: {SUMMONS_ISSUED}")

    writer = PdfWriter()
    append_page(writer, SUMMONS_ISSUED, MELANO_SUMMONS_PAGE)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "wb") as fh:
        writer.write(fh)

    if page_count(OUT) != 1:
        raise SystemExit(f"Expected 1-page Melano extract, got {page_count(OUT)}")
    print(f"Wrote {OUT.name} (1 p., from Dkt. 3 p.{MELANO_SUMMONS_PAGE + 1})")


if __name__ == "__main__":
    main()
