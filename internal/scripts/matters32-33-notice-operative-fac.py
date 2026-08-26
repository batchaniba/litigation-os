#!/usr/bin/env python3
"""Notices identifying the operative First Amended Complaint.

Meza (3:26-cv-08271-PHK): Dkt. 5 (Aug. 17) is operative; Dkt. 6 (Aug. 14) superseded.
Candelaria (3:26-cv-08272-LJC): Dkt. 6 (Aug. 17) is operative; Dkt. 5 (Aug. 14) superseded.

  python3 internal/scripts/matters32-33-notice-operative-fac.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
EXEC_DATE = "August 24, 2026"

OUT_MEZA = (
    ROOT
    / "public/documents/matter-32/ndcal"
    / "Notice Identifying Operative First Amended Complaint (Meza) (Aug 24 2026).pdf"
)
OUT_CAND = (
    ROOT
    / "public/documents/matter-33/ndcal"
    / "Notice Identifying Operative First Amended Complaint (Candelaria) (Aug 24 2026).pdf"
)

ATTY = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()


def _sign_block(d: PleadingPaper) -> None:
    d.ensure_space(7)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    # One blank -- stamp seats on the rule below.
    d.blank_line()
    d.write_line("___________________________________")
    d.write_line("BRENDAN NGWA NFORBI", bold=True)
    d.write_line("Plaintiff, In Propria Persona")


def _stamp_sig(path: Path) -> None:
    doc = fitz.open(str(path))
    line = None
    page = None
    for candidate in doc:
        hits = candidate.search_for("_______________________________")
        if hits:
            page = candidate
            line = hits[-1]
            break
    if page is None or line is None:
        doc.close()
        raise RuntimeError(f"No signature line found in {path}")
    width = 135.0
    height = width * SIGNATURE_ASPECT
    # Seat on the visible underscore stroke (near glyph baseline), not the tall
    # text bbox top; otherwise the ink floats ~10pt above the rule.
    y1 = line.y1 - 2.0
    y0 = y1 - height
    rect = fitz.Rect(line.x0, y0, line.x0 + width, y1)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)
    doc.saveIncr()
    doc.close()


def build_meza_notice(path: Path) -> None:
    d = PleadingPaper(
        str(path),
        doc_title_footer="NOTICE IDENTIFYING OPERATIVE FAC -- NFORBI v. MEZA-GONZALEZ ET AL.",
    )
    _header(d)
    left = [
        ("BRENDAN NGWA NFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("SANTIAGO MEZA-GONZALEZ;", True, False),
        ("JOSE MELANO; and DOES 1-10,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        ("Case No. 3:26-cv-08271-PHK", False, False),
        ("", False, False),
        ("NOTICE IDENTIFYING", True, False),
        ("OPERATIVE FIRST", True, False),
        ("AMENDED COMPLAINT", True, False),
        ("", False, False),
        ("[Fed. R. Civ. P. 15]", False, False),
        ("", False, False),
        ("Hon. Peter H. Kang", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("NOTICE IDENTIFYING OPERATIVE FIRST AMENDED COMPLAINT", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "TO THE COURT AND ALL PARTIES AND THEIR ATTORNEYS OF RECORD:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngwa Nforbi, appearing in propria persona, submits this "
        "Notice solely to clarify the record concerning two clerk-stamped First "
        "Amended Complaints now appearing on the docket of this action.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "1. On August 14, 2026, the Clerk filed a First Amended Complaint as Dkt. 6 "
        "(21 pages; caption-dated August 12, 2026).",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2. On August 17, 2026, the Clerk filed a First Amended Complaint as Dkt. 5 "
        "(21 pages; caption-dated August 17, 2026). The Melano proof of service of "
        "summons was filed the same day as Dkt. 5-1.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3. For the avoidance of doubt, and notwithstanding that Dkt. 5 bears a "
        "lower docket number than Dkt. 6, the operative pleading of record is the "
        "First Amended Complaint filed August 17, 2026 as Dkt. 5. The earlier "
        "First Amended Complaint filed August 14, 2026 as Dkt. 6 is superseded in "
        "full and is of no further force or effect. See Fed. R. Civ. P. 15(a); "
        "Lacey v. Maricopa County, 693 F.3d 896, 927 (9th Cir. 2012) (en banc).",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "4. This Notice does not amend, supplement, or withdraw any allegation in "
        "Dkt. 5. It is filed only to identify the operative pleading clearly on "
        "the face of the docket before any responsive pleading or Rule 12 motion.",
        first_indent=0,
    )
    _sign_block(d)
    d.save()
    _stamp_sig(path)


def build_candelaria_notice(path: Path) -> None:
    d = PleadingPaper(
        str(path),
        doc_title_footer="NOTICE IDENTIFYING OPERATIVE FAC -- NFORBI v. CANDELARIA ET AL.",
    )
    _header(d)
    left = [
        ("BRENDAN NGWA NFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("DIANA CANDELARIA, in her", True, False),
        ("individual capacity; STEVE", True, False),
        ("GORDON, in his official", True, False),
        ("capacity; and DOES 1-10,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        ("Case No. 3:26-cv-08272-LJC", False, False),
        ("", False, False),
        ("NOTICE IDENTIFYING", True, False),
        ("OPERATIVE FIRST", True, False),
        ("AMENDED COMPLAINT", True, False),
        ("", False, False),
        ("[Fed. R. Civ. P. 15]", False, False),
        ("", False, False),
        ("Hon. Lisa J. Cisneros", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("NOTICE IDENTIFYING OPERATIVE FIRST AMENDED COMPLAINT", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "TO THE COURT AND ALL PARTIES AND THEIR ATTORNEYS OF RECORD:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff Brendan Ngwa Nforbi, appearing in propria persona, submits this "
        "Notice solely to clarify the record concerning two clerk-stamped First "
        "Amended Complaints now appearing on the docket of this action.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "1. On August 14, 2026, the Clerk filed a First Amended Complaint as Dkt. 5 "
        "(46 pages).",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2. On August 17, 2026, the Clerk filed a First Amended Complaint as Dkt. 6 "
        "(44 pages). Among other conforming edits, Dkt. 6 omits the Burrell v. "
        "Jackson passage that appeared in the original complaint.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3. The operative pleading of record is the First Amended Complaint filed "
        "August 17, 2026 as Dkt. 6. The earlier First Amended Complaint filed "
        "August 14, 2026 as Dkt. 5 is superseded in full and is of no further "
        "force or effect. See Fed. R. Civ. P. 15(a); Lacey v. Maricopa County, "
        "693 F.3d 896, 927 (9th Cir. 2012) (en banc).",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "4. This Notice does not amend, supplement, or withdraw any allegation in "
        "Dkt. 6. It is filed only to identify the operative pleading clearly on "
        "the face of the docket before any responsive pleading or Rule 12 motion.",
        first_indent=0,
    )
    _sign_block(d)
    d.save()
    _stamp_sig(path)


def main() -> None:
    OUT_MEZA.parent.mkdir(parents=True, exist_ok=True)
    OUT_CAND.parent.mkdir(parents=True, exist_ok=True)
    build_meza_notice(OUT_MEZA)
    print(f"Wrote {OUT_MEZA}")
    build_candelaria_notice(OUT_CAND)
    print(f"Wrote {OUT_CAND}")


if __name__ == "__main__":
    main()
