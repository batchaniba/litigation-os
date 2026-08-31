#!/usr/bin/env python3
"""Matter 28 — Amended Summons packet for clerk issuance (pleading paper).

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Dkt. 3 Proposed Summons was never issued (blank Date / Deputy Clerk). Dkt. 11
directs Rule 4 service after fee payment. This packet is what Plaintiff prints
and takes to the courthouse:

  1. Request for Issuance — portfolio pleading paper
  2. Exhibit A cover — portfolio exhibit-cover style
  3. Amended Summons — Shannon Smith (AO 440 page 1 only)
  4. Exhibit B cover — portfolio exhibit-cover style
  5. Amended Summons — HOPE Psychotherapy (AO 440 page 1 only)

Outputs under matter-28/amended-summons-for-issuance/.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, FloatObject, NameObject, TextStringObject

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import assemble  # noqa: E402
from pleading_paper import PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

import pymupdf  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
M28 = ROOT / "internal/public/documents/matter-28"
OUT = M28 / "amended-summons-for-issuance"
AO440_TEMPLATE = ROOT / "internal/public/documents/_form-library/ao440-blank-template.pdf"

CASE = "3:26-cv-07504-LJC"
CASE_SHORT = "3:26-cv-07504"
JUDGE = "Hon. Lisa J. Cisneros"
PLAINTIFF = "BRENDAN NGEHSI NEWANFORBI"
PLAINTIFF_MIXED = "Brendan Ngehsi Newanforbi"
PLAINTIFF_ADDRESS = "1455 Cat Tail Drive"
PLAINTIFF_CITY = "Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
EXEC_DATE = "August 31, 2026"
FOOTER = "REQUEST FOR ISSUANCE OF AMENDED SUMMONS -- NEWANFORBI v. SMITH, ET AL."
CAPTION = "NEWANFORBI v. SMITH, ET AL."

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
        "cover_filename": "01a_Exhibit_A_Cover.pdf",
        "title": "Amended Summons — Shannon Smith, LCSW (AO 440)",
        "details": [
            "Fed. R. Civ. P. 4(b) — for clerk issuance (Date / signature blank)",
            "Serve: Shannon Smith, LCSW, CEO",
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "1245 B Street, Hayward, CA 94541",
        ],
        "address": [
            "Shannon Smith, LCSW, Chief Executive Officer",
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "1245 B Street",
            "Hayward, CA 94541",
        ],
    },
    {
        "filename": "02_Amended_Summons_HOPE_Psychotherapy.pdf",
        "exhibit": "B",
        "cover_filename": "02a_Exhibit_B_Cover.pdf",
        "title": "Amended Summons — HOPE Psychotherapy, Inc. (AO 440)",
        "details": [
            "Fed. R. Civ. P. 4(b) — for clerk issuance (Date / signature blank)",
            "Serve: HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "c/o Shannon Smith, LCSW, Chief Executive Officer",
            "1245 B Street, Hayward, CA 94541",
        ],
        "address": [
            "HOPE Psychotherapy, Inc. d/b/a HOPE Program",
            "c/o Shannon Smith, LCSW, Chief Executive Officer",
            "1245 B Street",
            "Hayward, CA 94541",
        ],
    },
]


def _caption_left() -> list[tuple[str, bool, bool]]:
    return [
        ("BRENDAN NGEHSI NEWANFORBI,", False, False),
        ("", False, False),
        ("               Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("SHANNON SMITH, LCSW, Chief", False, False),
        ("Executive Officer and Founder of", False, False),
        ("HOPE Program, an individual; and", False, False),
        ("HOPE PSYCHOTHERAPY, INC., d/b/a", False, False),
        ("HOPE PROGRAM, a California", False, False),
        ("corporation,", False, False),
        ("", False, False),
        ("               Defendants.", False, False),
    ]


def _write_party_header(d: PleadingPaper) -> None:
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, size=11)
    d.write_line("Plaintiff In Pro Per", size=11)
    d.write_line("1455 Cat Tail Drive", size=11)
    d.write_line("Stockton, CA 95204", size=11)
    d.write_line("Tel: (209) 801-4442", size=11)
    d.write_line("E-mail: bnn.cdl@gmail.com", size=11)
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True, size=11)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True, size=11)
    d.blank_line()


def _stamp_signature(path: Path) -> None:
    if not Path(SIGNATURE_PATH).is_file():
        return
    doc = pymupdf.open(str(path))
    page = line = None
    for candidate in doc:
        hits = candidate.search_for("_______________________________")
        if hits:
            page = candidate
            line = hits[-1]
            break
    if page is None or line is None:
        doc.close()
        return
    width = 135.0
    height = width * SIGNATURE_ASPECT
    y1 = line.y1 - 2.0
    y0 = y1 - height
    rect = pymupdf.Rect(line.x0, y0, line.x0 + width, y1)
    page.insert_image(rect, filename=str(SIGNATURE_PATH), keep_proportion=True)
    tmp = path.with_name(path.stem + ".signed.pdf")
    doc.save(tmp, garbage=4, deflate=True, incremental=False)
    doc.close()
    tmp.replace(path)


def write_request(path: Path) -> None:
    d = PleadingPaper(str(path), doc_title_footer=FOOTER)
    _write_party_header(d)

    right = [
        (f"Case No.: {CASE}", True, False),
        ("", False, False),
        ("REQUEST FOR ISSUANCE OF", True, False),
        ("AMENDED SUMMONS", True, False),
        ("[Fed. R. Civ. P. 4(b)]", False, False),
        ("", False, False),
        (f"Judge: {JUDGE}", False, False),
    ]
    d.draw_caption_block(_caption_left(), right, caption_size=9, tight_lh=12)
    d.blank_line()

    d.write_line("REQUEST FOR ISSUANCE OF AMENDED SUMMONS", bold=True, center=True, size=11)
    d.blank_line()
    d.write_line("TO THE CLERK OF THE COURT:", bold=True)
    d.write_wrapped(
        "Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, "
        "respectfully requests that the Clerk issue Amended Summonses in this "
        "action pursuant to Federal Rule of Civil Procedure 4(b)."
    )
    d.blank_line()
    d.write_line("I.  BACKGROUND", bold=True)
    d.write_wrapped(
        "1. On July 20, 2026, Plaintiff filed a Proposed Summons (Dkt. 3). The "
        "filed Proposed Summons does not bear a Date or Signature of the Clerk "
        "or Deputy Clerk and therefore has not been issued."
    )
    d.write_wrapped(
        "2. Plaintiff paid the filing fee (Dkt. 8). On August 26, 2026, the Court "
        "denied the IFP application as moot and directed Plaintiff to serve "
        "process consistent with Rule 4 (Dkt. 11)."
    )
    d.write_wrapped(
        "3. Attached hereto as Exhibit A (Shannon Smith, LCSW) and Exhibit B "
        "(HOPE Psychotherapy, Inc. d/b/a HOPE Program) are Amended Summonses "
        "that (a) state the assigned case number, (b) identify each defendant "
        "with a complete service address (1245 B Street, Hayward, CA 94541), "
        "and (c) leave the Date and Deputy Clerk signature lines blank for "
        "issuance."
    )
    d.blank_line()
    d.write_line("II.  REQUEST", bold=True)
    d.write_wrapped(
        "Plaintiff respectfully requests that the Clerk sign, seal, and issue "
        "the Amended Summonses attached as Exhibits A and B so that Plaintiff "
        "may effect Rule 4 service as directed in Dkt. 11. Please return the "
        "issued originals to Plaintiff."
    )
    d.blank_line()
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.blank_line()
    d.write_line("_______________________________")
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")
    d.write_line(f"{PLAINTIFF_ADDRESS}")
    d.write_line(PLAINTIFF_CITY)
    d.write_line(f"Tel: {PHONE}  |  Email: {EMAIL}", size=10)
    d.blank_line()
    d.write_line("Exhibits:", bold=True)
    d.write_line("  Exhibit A — Amended Summons (Shannon Smith, LCSW)")
    d.write_line("  Exhibit B — Amended Summons (HOPE Psychotherapy, Inc.)")
    d.save()
    _stamp_signature(path)


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


def fill_form(
    template: Path,
    out_path: Path,
    fields: dict[str, object],
    page_index: int = 0,
    font_overrides: dict[str, str] | None = None,
) -> Path:
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


def drop_proof_of_service_page(pdf_path: Path) -> None:
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
    drop_proof_of_service_page(out_path)
    return out_path


def write_exhibit_pages() -> list[Path]:
    paths: list[Path] = []
    for defendant in DEFENDANTS:
        cover = OUT / defendant["cover_filename"]
        write_exhibit_cover(
            cover,
            court="UNITED STATES DISTRICT COURT",
            court_line2="NORTHERN DISTRICT OF CALIFORNIA",
            caption=CAPTION,
            case_no=f"Case No. {CASE}",
            exhibit=defendant["exhibit"],
            title=defendant["title"],
            details=defendant["details"],
            footer=f"Request for Issuance of Amended Summons — {CAPTION}",
        )
        summons = fill_amended_summons(defendant)
        paths.extend([cover, summons])
    return paths


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert AO440_TEMPLATE.is_file(), f"missing {AO440_TEMPLATE}"

    request = OUT / "00_Request_for_Issuance_of_Amended_Summons.pdf"
    write_request(request)
    exhibit_and_summons = write_exhibit_pages()
    complete = OUT / "COMPLETE_Amended_Summons_Packet_for_Clerk.pdf"
    pages = assemble([request, *exhibit_and_summons], complete)
    print(f"Wrote {complete} ({pages} pages)")
    for p in sorted(OUT.iterdir()):
        print(f"  {p.name}  ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
