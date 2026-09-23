#!/usr/bin/env python3
"""Build a private-process-server RE-SERVICE packet for Officer Jose Melano.

Matter 32 - Nforbi v. Meza-Gonzalez, et al., N.D. Cal. No. 4:26-cv-08271-ASK
(opened as 3:26-cv-08271-PHK; reassigned to Mag. J. Krishnan Aug. 24, 2026).

Re-service packet for a *private* process server (personal service under Fed.
R. Civ. P. 4(e)): issued summons (Melano page) + blank AO 440 Proof of Service
return + operative First Amended Complaint (Dkt. 5) + CMC/ADR order (Dkt. 4),
behind a one-page cover of service instructions. Includes the FAC.

Outputs (matter-32/ndcal/):
  Melano Private Process Server Re-Service Bundle (Sep 23 2026).pdf
  Melano Process Server Cover Sheet (Sep 23 2026).pdf
"""

from __future__ import annotations

from pathlib import Path

import pymupdf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def page_count(p: Path) -> int:
    d = pymupdf.open(str(p))
    try:
        return d.page_count
    finally:
        d.close()

ROOT = Path(__file__).resolve().parents[2]
NDCAL = ROOT / "internal/public/documents/matter-32/ndcal"

SUMMONS_ISSUED = NDCAL / "Dkt 03 - Summons Issued - Meza-Gonzalez and Melano (Aug 10 2026).pdf"
# Dkt. 3 page index 0 = Melano (CHP South Sacramento / 6 Massie Court); page 1 = Meza.
MELANO_SUMMONS_PAGE = 0

FAC = NDCAL / "Dkt 05 - First Amended Complaint (CONFORMED, Filed Aug 17 2026).pdf"
CMC = NDCAL / (
    "Dkt 04 - Order Setting Initial Case Management Conference and ADR Deadlines "
    "(Aug 10 2026).pdf"
)
AO440 = NDCAL / "AO 440 Summons - Jose Melano (N.D. Cal.) (Aug 7 2026).pdf"
# Page 2 (index 1) of the AO 440 is the blank Proof of Service return.
AO440_POS_PAGE = 1

OUT_COVER = NDCAL / "Melano Process Server Cover Sheet (Sep 23 2026).pdf"
OUT_BUNDLE = NDCAL / "Melano Private Process Server Re-Service Bundle (Sep 23 2026).pdf"

CASE = "4:26-cv-08271-ASK"
ORIG_CASE = "3:26-cv-08271-PHK"
JUDGE = "Hon. Ajay S. Krishnan"
DEFENDANT = "Officer Jose Melano (CHP Badge #023054), individually"
SERVE_LINES = [
    "California Highway Patrol, South Sacramento Area",
    "6 Massie Court",
    "Sacramento, CA 95823",
]
PLAINTIFF = "Brendan Ngwa Nforbi, Plaintiff In Propria Persona"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"


def write_cover(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    y = h - 54

    def line(text: str, size: float = 10, bold: bool = False, dy: float = 14) -> None:
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(54, y, text)
        y -= dy

    line("PRIVATE PROCESS SERVER - RE-SERVICE PACKET", 13, True, 18)
    line("Nforbi v. Meza-Gonzalez, et al. - U.S. District Court, N.D. Cal.", 10, True)
    line(f"Case No. {CASE}  |  {JUDGE}", 10, True, 18)

    line("SERVE THIS DEFENDANT (personal service under Fed. R. Civ. P. 4(e)):", 10, True)
    line(f"  {DEFENDANT}")
    for s in SERVE_LINES:
        line(f"  {s}")
    y -= 6

    line("SERVICE ADDRESS NOTES", 10, True)
    line("  * Serve at the CHP South Sacramento Area duty station above (current station).")
    line("  * Individual-capacity suit - serve the officer personally, or by another")
    line("    Rule 4(e) method. Leave a complete set of the enclosed papers with him.")
    line("  * The enclosed clerk-issued summons bears the original case number")
    line(f"    {ORIG_CASE}. This is the same action, later reassigned to")
    line(f"    {CASE} ({JUDGE}); the reassignment is on the docket.")
    y -= 6

    line("ENCLOSED DOCUMENTS (in this order - serve the full set)", 10, True)
    breakdown = [
        ("1. This cover sheet (for server; optional to leave with defendant)", 1),
        ("2. Issued Summons - Melano only (Dkt. 3)", 1),
        ("3. Blank AO 440 Proof of Service return (server completes & returns to plaintiff)", 1),
        ("4. First Amended Complaint - OPERATIVE (Dkt. 5, filed Aug. 17, 2026)", 21),
        ("5. Order Setting Initial CMC and ADR Deadlines (Dkt. 4)", 2),
    ]
    total = 0
    for label, n in breakdown:
        line(f"  {label} - {n} p.")
        total += n
    line(f"  TOTAL PAGES IN BUNDLE: {total}", 10, True, 16)

    line("WHAT TO DO", 10, True)
    line("  1. Personally serve Defendant with documents 2, 4, and 5 (summons + FAC +")
    line("     CMC order). Leave the complete set with him.")
    line("  2. Complete the AO 440 Proof of Service (document 3): date/time/place of")
    line("     service, how served, your name/address, and sign under penalty of perjury.")
    line("  3. Return the completed Proof of Service (and any server affidavit you use)")
    line("     to Plaintiff immediately for filing with the Court as the Rule 4(l) return.")
    y -= 6

    line("DEADLINES / CASE CONTEXT", 10, True)
    line("  * Response due 21 days after service (Fed. R. Civ. P. 12(a)(1)(A)(i)).")
    line("  * Rule 4(m) outer service deadline from docketing: November 8, 2026.")
    line("  * Initial CMC: December 2, 2026, 11:00 a.m., Courtroom F, 450 Golden Gate Ave.,")
    line("    San Francisco (see Dkt. 4; subject to rescheduling upon reassignment).")
    y -= 6

    line("RETURN COMPLETED PROOF TO PLAINTIFF", 10, True)
    line(f"  {PLAINTIFF}")
    line("  1455 Cat Tail Drive, Stockton, CA 95204")
    line(f"  {PHONE}  |  {EMAIL}")
    y -= 10

    line("Private process server only - not for a sheriff / SER-001 form.", 9, True)
    c.showPage()
    c.save()


def annotate_pos_page(src: Path, page_index: int, out_tmp: Path) -> Path:
    """Stamp current case number + defendant name onto the blank AO 440 POS page."""
    doc = pymupdf.open(str(src))
    page = doc[page_index]
    page.insert_text((420, 72), CASE, fontname="helv", fontsize=9, color=(0, 0, 0))
    page.insert_text((54, 118), DEFENDANT, fontname="helv", fontsize=8, color=(0, 0, 0))
    single = pymupdf.open()
    single.insert_pdf(doc, from_page=page_index, to_page=page_index)
    doc.close()
    single.save(str(out_tmp))
    single.close()
    return out_tmp


def build_bundle() -> Path:
    for p in (SUMMONS_ISSUED, FAC, CMC, AO440):
        if not p.is_file() or p.stat().st_size < 1000:
            raise SystemExit(f"Missing or empty: {p}")

    write_cover(OUT_COVER)

    tmp_pos = NDCAL / "_tmp_melano_ao440_pos.pdf"
    annotate_pos_page(AO440, AO440_POS_PAGE, tmp_pos)

    out = pymupdf.open()
    out.insert_pdf(pymupdf.open(str(OUT_COVER)))
    _s = pymupdf.open(str(SUMMONS_ISSUED))
    out.insert_pdf(_s, from_page=MELANO_SUMMONS_PAGE, to_page=MELANO_SUMMONS_PAGE)
    out.insert_pdf(pymupdf.open(str(tmp_pos)))
    out.insert_pdf(pymupdf.open(str(FAC)))
    out.insert_pdf(pymupdf.open(str(CMC)))
    out.save(str(OUT_BUNDLE))
    tmp_pos.unlink(missing_ok=True)

    n = page_count(OUT_BUNDLE)
    expected = 1 + 1 + 1 + page_count(FAC) + page_count(CMC)
    print(f"Wrote {OUT_COVER.name} (1 p.)")
    print(f"Wrote {OUT_BUNDLE.name} ({n} pp.)")
    if n != expected:
        raise SystemExit(f"Page count mismatch: got {n}, expected {expected}")
    return OUT_BUNDLE


def main() -> None:
    build_bundle()
    print("Done - Melano private process server re-service packet (FAC included).")


if __name__ == "__main__":
    main()
