#!/usr/bin/env python3
"""Build a private-process-server re-service packet for Santiago Meza-Gonzalez.

Matter 32 - Nforbi v. Meza-Gonzalez, et al., N.D. Cal. No. 3:26-cv-08271-PHK.

Melano's Rule 5 FAC mail POS (Aug 21) expressly noted that Rule 4 process as
to Meza-Gonzalez had not been completed. This packet is for a *private*
process server (not Stanislaus Sheriff / SER-001): issued summons + operative
FAC + operative-FAC notice + CMC/ADR order + blank AO 440 Proof of Service
return, with a one-page cover of service instructions.

Outputs (matter-32/ndcal/):
  Meza-Gonzalez Private Process Server Bundle (Aug 25 2026).pdf
  Meza-Gonzalez Process Server Cover Sheet (Aug 25 2026).pdf
"""

from __future__ import annotations

from pathlib import Path
import sys

import fitz
from pypdf import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pdf_packet import append_page, append_pdf, page_count  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
NDCAL = ROOT / "internal/public/documents/matter-32/ndcal"

SUMMONS_ISSUED = NDCAL / "Dkt 03 - Summons Issued - Meza-Gonzalez and Melano (Aug 10 2026).pdf"
# Dkt. 3 page index 1 = Meza (CHP Modesto / 4030 Kiernan); page 0 = Melano.
MEZA_SUMMONS_PAGE = 1

FAC = NDCAL / "Dkt 05 - First Amended Complaint (CONFORMED, Filed Aug 17 2026).pdf"
NOTICE = NDCAL / "Notice Identifying Operative First Amended Complaint (Meza) (Aug 24 2026).pdf"
CMC = NDCAL / (
    "Dkt 04 - Order Setting Initial Case Management Conference and ADR Deadlines "
    "(Aug 10 2026).pdf"
)
AO440 = NDCAL / "AO 440 Summons - Santiago Meza-Gonzalez (N.D. Cal.) (Aug 7 2026).pdf"
# Page 2 of AO 440 is the blank Proof of Service return the server completes.
AO440_POS_PAGE = 1

OUT_COVER = NDCAL / "Meza-Gonzalez Process Server Cover Sheet (Aug 25 2026).pdf"
OUT_BUNDLE = NDCAL / "Meza-Gonzalez Private Process Server Bundle (Aug 25 2026).pdf"

CASE = "3:26-cv-08271-PHK"
DEFENDANT = "Santiago Meza-Gonzalez (CHP Badge #023295), individually"
SERVE_LINES = [
    "California Highway Patrol, Modesto Area",
    "4030 Kiernan Avenue",
    "Modesto, CA 95356",
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

    line("PRIVATE PROCESS SERVER - SERVICE PACKET", 13, True, 18)
    line("Nforbi v. Meza-Gonzalez, et al. - U.S. District Court, N.D. Cal.", 10, True)
    line(f"Case No. {CASE}  |  Hon. Peter H. Kang", 10, True, 18)

    line("SERVE THIS DEFENDANT (personal service under Fed. R. Civ. P. 4):", 10, True)
    line(f"  {DEFENDANT}")
    for s in SERVE_LINES:
        line(f"  {s}")
    y -= 6

    line("SERVICE ADDRESS NOTES", 10, True)
    line("  * Serve at the Modesto Area duty station above (current station).")
    line("  * Do NOT serve at CHP Dublin Area (incident location - Alameda County).")
    line("  * Individual-capacity suit - serve the officer personally (or other Rule 4(e)")
    line("    method). Leave a complete set of the enclosed papers with him.")
    y -= 6

    line("ENCLOSED DOCUMENTS (in this order - serve the full set)", 10, True)
    breakdown = [
        ("1. This cover sheet (for server; optional to leave with defendant)", 1),
        ("2. Issued Summons - Meza-Gonzalez only (Dkt. 3)", 1),
        ("3. Blank AO 440 Proof of Service return (server completes & returns to plaintiff)", 1),
        ("4. First Amended Complaint - OPERATIVE (Dkt. 5, filed Aug. 17, 2026)", 21),
        ("5. Notice Identifying Operative First Amended Complaint (Aug. 24, 2026)", 2),
        ("6. Order Setting Initial CMC and ADR Deadlines (Dkt. 4)", 2),
    ]
    total = 0
    for label, n in breakdown:
        line(f"  {label} - {n} p.")
        total += n
    line(f"  TOTAL PAGES IN BUNDLE: {total}", 10, True, 16)

    line("WHAT TO DO", 10, True)
    line("  1. Personally serve Defendant with documents 2, 4, 5, and 6 (summons + FAC +")
    line("     notice + CMC order). Leave the complete set with him.")
    line("  2. Complete the AO 440 Proof of Service (document 3): date/time/place of")
    line("     service, how served, your name/address, and sign under penalty of perjury.")
    line("  3. Return the completed Proof of Service (and any server affidavit you use)")
    line("     to Plaintiff immediately for filing with the Court as the Rule 4(l) return.")
    y -= 6

    line("DEADLINES / CASE CONTEXT", 10, True)
    line("  * Response due 21 days after service (Fed. R. Civ. P. 12(a)(1)(A)(i)).")
    line("  * Rule 4(m) outer service deadline from docketing: November 8, 2026.")
    line("  * Initial CMC: December 2, 2026, 11:00 a.m., Courtroom F, 450 Golden Gate Ave.,")
    line("    San Francisco (see Dkt. 4).")
    line("  * Co-defendant Jose Melano already has summons POS on file (Dkt. 5-1); this")
    line("    packet is Meza-Gonzalez only.")
    y -= 6

    line("RETURN COMPLETED PROOF TO PLAINTIFF", 10, True)
    line(f"  {PLAINTIFF}")
    line("  1455 Cat Tail Drive, Stockton, CA 95204")
    line(f"  {PHONE}  |  {EMAIL}")
    y -= 10

    line("NOT for Stanislaus County Sheriff / SER-001 - private process server only.", 9, True)
    c.showPage()
    c.save()


def annotate_pos_page(src: Path, page_index: int, out_tmp: Path) -> Path:
    """Stamp case number + defendant name onto the blank AO 440 POS page."""
    doc = fitz.open(src)
    page = doc[page_index]
    # Case number near "Civil Action No." on AO 440 page 2 (top band).
    page.insert_text(
        (420, 72),
        CASE,
        fontname="helv",
        fontsize=9,
        color=(0, 0, 0),
    )
    page.insert_text(
        (54, 118),
        DEFENDANT,
        fontname="helv",
        fontsize=8,
        color=(0, 0, 0),
    )
    single = fitz.open()
    single.insert_pdf(doc, from_page=page_index, to_page=page_index)
    doc.close()
    single.save(out_tmp)
    single.close()
    return out_tmp


def build_bundle() -> Path:
    for p in (SUMMONS_ISSUED, FAC, NOTICE, CMC, AO440):
        if not p.is_file() or p.stat().st_size < 1000:
            raise SystemExit(f"Missing or empty: {p}")

    write_cover(OUT_COVER)

    tmp_pos = NDCAL / "_tmp_meza_ao440_pos.pdf"
    annotate_pos_page(AO440, AO440_POS_PAGE, tmp_pos)

    writer = PdfWriter()
    append_pdf(writer, OUT_COVER)
    append_page(writer, SUMMONS_ISSUED, MEZA_SUMMONS_PAGE)
    append_pdf(writer, tmp_pos)
    append_pdf(writer, FAC)
    append_pdf(writer, NOTICE)
    append_pdf(writer, CMC)

    with open(OUT_BUNDLE, "wb") as fh:
        writer.write(fh)
    tmp_pos.unlink(missing_ok=True)

    n = page_count(OUT_BUNDLE)
    print(f"Wrote {OUT_COVER.name} (1 p.)")
    print(f"Wrote {OUT_BUNDLE.name} ({n} pp.)")
    expected = 1 + 1 + 1 + page_count(FAC) + page_count(NOTICE) + page_count(CMC)
    if n != expected:
        raise SystemExit(f"Page count mismatch: got {n}, expected {expected}")
    return OUT_BUNDLE


def main() -> None:
    build_bundle()
    print("Done - private process server packet (no SER-001 / no sheriff forms).")


if __name__ == "__main__":
    main()
