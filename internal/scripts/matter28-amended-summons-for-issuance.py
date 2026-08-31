#!/usr/bin/env python3
"""Matter 28 — Amended AO 440 summonses for clerk issuance at the courthouse.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Dkt. 3 is a Proposed Summons (filed Jul. 20, 2026) with blank Date and blank
Deputy Clerk signature — never issued. Dkt. 11 (Aug. 26, 2026) directs Rule 4
service after the filing fee was paid. These Amended Summonses correct the
defendant address block (street address was missing on Dkt. 3), type the
caption cleanly, and leave the clerk Date / signature lines blank for stamping.

Outputs (matter-28/amended-summons-for-issuance/):
  00_Request_for_Issuance_of_Amended_Summons.pdf
  01_Amended_Summons_Shannon_Smith.pdf   (AO 440 page 1 only)
  02_Amended_Summons_HOPE_Psychotherapy.pdf  (AO 440 page 1 only)
  COMPLETE_Amended_Summons_Packet_for_Clerk.pdf
    = Request + Exhibit A (Smith) + Exhibit B (HOPE) — single download
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, FloatObject, NameObject, TextStringObject
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pymupdf

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pdf_packet import assemble  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
M28 = ROOT / "internal/public/documents/matter-28"
OUT = M28 / "amended-summons-for-issuance"
AO440_TEMPLATE = ROOT / "internal/public/documents/_form-library/ao440-blank-template.pdf"

CASE = "3:26-cv-07504-LJC"
PLAINTIFF = "BRENDAN NGEHSI NEWANFORBI"
PLAINTIFF_MIXED = "Brendan Ngehsi Newanforbi"
PLAINTIFF_ADDRESS = "1455 Cat Tail Drive"
PLAINTIFF_CITY = "Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"

DEFENDANTS_BLOCK = (
    "SHANNON SMITH, LCSW, Chief Executive Officer and Founder of HOPE Program, "
    "an individual; and HOPE PSYCHOTHERAPY, INC., d/b/a HOPE PROGRAM, "
    "a California corporation"
)

AO440_DISTRICT = "        Northern District of California"
AO440_PLAINTIFF_ADDRESS_RECT = (219.0, 286.0)
AO440_FONT_OVERRIDES = {"Plaintiff address": "/Helv 9.00 Tf 0 g"}

DEFENDANTS = [
    {
        "filename": "01_Amended_Summons_Shannon_Smith.pdf",
        "exhibit": "A",
        "banner": "EXHIBIT A — AMENDED SUMMONS — Shannon Smith, LCSW",
        "address": [
            "Shannon Smith, LCSW, Chief Executive Officer",
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "1245 B Street",
            "Hayward, CA 94541",
        ],
        "proof_of_service_name": "Shannon Smith, LCSW, CEO — HOPE Program",
    },
    {
        "filename": "02_Amended_Summons_HOPE_Psychotherapy.pdf",
        "exhibit": "B",
        "banner": "EXHIBIT B — AMENDED SUMMONS — HOPE Psychotherapy, Inc.",
        "address": [
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "c/o Shannon Smith, LCSW, Chief Executive Officer",
            "1245 B Street",
            "Hayward, CA 94541",
        ],
        "proof_of_service_name": "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
    },
]


def set_default_appearance(writer: PdfWriter, qualified_name: str, da: str) -> None:
    leaf = qualified_name.split(".")[-1]
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if str(obj.get("/T")) == leaf:
                obj[NameObject("/DA")] = TextStringObject(da)


def set_field_rect(writer: PdfWriter, field_name: str, bottom: float, top: float) -> None:
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            if str(obj.get("/T")) != field_name:
                continue
            x0, _, x1, _ = (float(v) for v in obj["/Rect"])
            obj[NameObject("/Rect")] = ArrayObject(
                [FloatObject(x0), FloatObject(bottom), FloatObject(x1), FloatObject(top)]
            )


def fill_form(template: Path, out_path: Path, fields: dict[str, object], page_index: int = 0,
              font_overrides: dict[str, str] | None = None) -> Path:
    reader = PdfReader(str(template))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(writer.pages[page_index], fields)
    for name, da in (font_overrides or {}).items():
        set_default_appearance(writer, name, da)
    writer.set_need_appearances_writer(True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def stamp_amended_banner(pdf_path: Path, banner: str) -> None:
    """Overlay a clear AMENDED SUMMONS banner so the clerk sees the ask."""
    doc = pymupdf.open(str(pdf_path))
    page = doc[0]
    # Top margin below the AO 440 header line — wider for EXHIBIT A/B banner.
    rect = pymupdf.Rect(28, 22, 584, 46)
    page.draw_rect(rect, color=(0, 0, 0), fill=(1, 1, 1), width=0.6)
    page.insert_textbox(
        rect,
        banner,
        fontsize=9,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_CENTER,
    )
    # Footer cue: leave Date / Deputy Clerk blank for issuance.
    foot = pymupdf.Rect(36, 740, 576, 762)
    page.insert_textbox(
        foot,
        "FOR CLERK ISSUANCE -- leave Date and Deputy Clerk signature blank for court stamp/signature",
        fontsize=7,
        fontname="helv",
        align=pymupdf.TEXT_ALIGN_CENTER,
    )
    doc.saveIncr()
    doc.close()


def drop_proof_of_service_page(pdf_path: Path) -> None:
    """Keep AO 440 page 1 only (drop the blank Proof of Service page)."""
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.add_page(reader.pages[0])
    with open(pdf_path, "wb") as fh:
        writer.write(fh)


def fill_amended_summons(defendant: dict) -> Path:
    fields: dict[str, object] = {
        "Dist.Info": AO440_DISTRICT,
        "Plaintiff": PLAINTIFF,
        "Defendant": DEFENDANTS_BLOCK,
        "Civil action number": CASE,
        # Date_Today and Deputy Clerk Signature intentionally omitted — clerk stamps.
        "Defendant address": "\n".join(defendant["address"]),
        "Plaintiff address": "\n".join(
            [
                PLAINTIFF_MIXED,
                "Plaintiff, In Pro Per",
                PLAINTIFF_ADDRESS,
                PLAINTIFF_CITY,
                f"Telephone: {PHONE} — E-mail: {EMAIL}",
            ]
        ),
    }
    out_path = fill_form(
        AO440_TEMPLATE,
        OUT / defendant["filename"],
        fields,
        font_overrides=AO440_FONT_OVERRIDES,
    )
    reader = PdfReader(str(out_path))
    writer = PdfWriter()
    writer.append(reader)
    set_field_rect(writer, "Plaintiff address", *AO440_PLAINTIFF_ADDRESS_RECT)
    writer.set_need_appearances_writer(True)
    with open(out_path, "wb") as fh:
        writer.write(fh)

    # Page 2 (Proof of Service) is not needed for clerk issuance — drop it.
    drop_proof_of_service_page(out_path)
    stamp_amended_banner(out_path, defendant["banner"])
    return out_path


def write_clerk_request(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    y = h - 54

    def line(text: str, size: float = 11, bold: bool = False, dy: float = 15) -> None:
        nonlocal y
        c.setFont("Times-Bold" if bold else "Times-Roman", size)
        c.drawString(54, y, text[:100])
        y -= dy

    def wrap(text: str, size: float = 11, dy: float = 14) -> None:
        nonlocal y
        c.setFont("Times-Roman", size)
        words = text.split()
        row = ""
        max_w = w - 108
        for word in words:
            trial = (row + " " + word).strip()
            if c.stringWidth(trial, "Times-Roman", size) <= max_w:
                row = trial
            else:
                c.drawString(54, y, row)
                y -= dy
                row = word
        if row:
            c.drawString(54, y, row)
            y -= dy

    line("UNITED STATES DISTRICT COURT", 12, True, 14)
    line("NORTHERN DISTRICT OF CALIFORNIA", 12, True, 18)
    line("REQUEST FOR ISSUANCE OF AMENDED SUMMONS", 13, True, 18)
    line(f"{PLAINTIFF_MIXED} v. Shannon Smith, LCSW, et al.", 11, True)
    line(f"Case No. {CASE}    Hon. Lisa J. Cisneros", 11, True, 18)

    wrap(
        "Plaintiff, appearing In Propria Persona, respectfully requests that the Clerk "
        "issue Amended Summonses in this action under Fed. R. Civ. P. 4(b)."
    )
    y -= 6
    line("Background", 11, True)
    wrap(
        "1. On July 20, 2026, Plaintiff filed a Proposed Summons (Dkt. 3). The filed "
        "Proposed Summons does not bear a Date or Signature of the Clerk or Deputy "
        "Clerk and therefore has not been issued."
    )
    wrap(
        "2. Plaintiff paid the filing fee (Dkt. 8). On August 26, 2026, the Court "
        "denied the IFP application as moot and directed Plaintiff to serve process "
        "consistent with Rule 4 (Dkt. 11)."
    )
    wrap(
        "3. Attached as Exhibit A (Shannon Smith, LCSW) and Exhibit B "
        "(HOPE Psychotherapy, Inc. d/b/a HOPE Program) are Amended Summonses that "
        "(a) state the assigned case number, (b) identify each defendant with a "
        "complete service address (1245 B Street, Hayward, CA 94541), and "
        "(c) leave the Date and Deputy Clerk signature lines blank for issuance."
    )
    y -= 6
    line("Request", 11, True)
    wrap(
        "Please sign, seal, and issue the Amended Summonses attached as Exhibits A "
        "and B so Plaintiff may effect Rule 4 service as directed in Dkt. 11."
    )
    y -= 10
    line("Respectfully submitted,", 11, False, 28)
    line("________________________________", 11, False, 14)
    line(PLAINTIFF_MIXED, 11, True)
    line("Plaintiff In Propria Persona", 11, False, 14)
    line(f"{PLAINTIFF_ADDRESS}", 11)
    line(PLAINTIFF_CITY, 11)
    line(f"Tel: {PHONE}", 11)
    line(f"Email: {EMAIL}", 11, False, 18)
    line("Dated: August 31, 2026", 11)
    y -= 10
    line("Exhibits (for clerk stamping -- please return issued originals to Plaintiff):", 10, True, 14)
    line("  Exhibit A  Amended Summons -- Shannon Smith, LCSW (AO 440)", 10)
    line("  Exhibit B  Amended Summons -- HOPE Psychotherapy, Inc. (AO 440)", 10)
    c.save()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert AO440_TEMPLATE.is_file(), f"missing {AO440_TEMPLATE}"

    request = OUT / "00_Request_for_Issuance_of_Amended_Summons.pdf"
    write_clerk_request(request)
    summons_paths = [fill_amended_summons(d) for d in DEFENDANTS]
    complete = OUT / "COMPLETE_Amended_Summons_Packet_for_Clerk.pdf"
    pages = assemble([request, *summons_paths], complete)
    print(f"Wrote {complete} ({pages} pages)")
    for p in sorted(OUT.iterdir()):
        print(f"  {p.name}  ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
