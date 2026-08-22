#!/usr/bin/env python3
"""Certificates of Service for Aug. 21, 2026 First-Class mailing of operative FACs.

Matter 32 (Meza): FAC Dkt. 5 mailed to Melano (already served).
Matter 33 (Candelaria): FAC Dkt. 6 mailed to Candelaria and Gordon (already served).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

import fitz  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

MAIL_DATE = "August 21, 2026"
EXEC_DATE = "August 24, 2026"
EXEC_CITY = "San Jose, California"

ROOT = SCRIPT_DIR.parent
OUT_MEZA = (
    ROOT
    / "public/documents/matter-32/ndcal"
    / "Certificate of Service - FAC Dkt 05 Mailed to Melano (Aug 21 2026).pdf"
)
OUT_CAND = (
    ROOT
    / "public/documents/matter-33/ndcal"
    / "Certificate of Service - FAC Dkt 06 Mailed to Candelaria and Gordon (Aug 21 2026).pdf"
)

ATTORNEY_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTORNEY_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()


def _sign(d: PleadingPaper) -> None:
    d.ensure_space(8)
    d.blank_line()
    d.write_line(f"I declare under penalty of perjury under the laws of the United States")
    d.write_line(f"that the foregoing is true and correct.")
    d.blank_line()
    d.write_line(f"Executed on {EXEC_DATE}, in {EXEC_CITY}.")
    d.blank_line()
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.blank_line()
    d.write_line("___________________________________")
    d.write_line("BRENDAN NGWA NFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")


def stamp_signature(path: Path) -> None:
    doc = fitz.open(str(path))
    page = doc[-1]
    # Place above the printed name line near bottom signature block
    # Find underscore line via text search
    hits = page.search_for("_______________________________")
    if hits:
        line = hits[-1]
        width = 160
        height = width * SIGNATURE_ASPECT
        rect = fitz.Rect(line.x0, line.y0 - height - 2, line.x0 + width, line.y0 - 2)
    else:
        rect = fitz.Rect(320, 620, 480, 655)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)
    doc.saveIncr()
    doc.close()


def build_meza(out: Path) -> None:
    d = PleadingPaper(
        str(out),
        doc_title_footer="CERTIFICATE OF SERVICE -- NFORBI v. MEZA-GONZALEZ ET AL.",
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
        ("CERTIFICATE OF SERVICE", True, False),
        ("", False, False),
        ("[Fed. R. Civ. P. 5]", False, False),
        ("", False, False),
        ("Hon. Peter H. Kang", False, False),
        ("", False, False),
        ("Re: First Amended Complaint", False, False),
        ("(Dkt. 5)", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_wrapped(
        "I, BRENDAN NGWA NFORBI, declare as follows:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "1. I am the Plaintiff in the above-captioned action and appear in propria persona. "
        "I am over the age of eighteen years and not a party to be served with the papers "
        "described below within the meaning of Fed. R. Civ. P. 5.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2. On August 21, 2026, I caused a true and correct copy of the First Amended "
        "Complaint for Damages filed in this action on August 17, 2026 as Dkt. 5 (the "
        "operative pleading) to be served by United States First-Class Mail, postage "
        "prepaid, addressed as follows:",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("Officer Jose Melano (CHP Badge #023054)", indent=36)
    d.write_line("California Highway Patrol, South Sacramento Area", indent=36)
    d.write_line("6 Massie Court", indent=36)
    d.write_line("Sacramento, CA 95823", indent=36)
    d.blank_line()
    d.write_wrapped(
        "3. Defendant Melano was previously served with the summons and original "
        "complaint on August 14, 2026; proof of that service was filed on August 17, 2026 "
        "as Dkt. 5-1. This mailing was made pursuant to Fed. R. Civ. P. 5(a) and 5(b)(2)(C) "
        "to serve the First Amended Complaint on a party who has been served with process "
        "but has not yet appeared.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "4. No copy of the First Amended Complaint was mailed under Rule 5 to Defendant "
        "Santiago Meza-Gonzalez by this Certificate, because Meza-Gonzalez has not been "
        "successfully served with process under Fed. R. Civ. P. 4.",
        first_indent=0,
    )
    _sign(d)
    d.save()
    stamp_signature(out)
    print(f"Wrote {out}")


def build_candelaria(out: Path) -> None:
    d = PleadingPaper(
        str(out),
        doc_title_footer="CERTIFICATE OF SERVICE -- NFORBI v. CANDELARIA ET AL.",
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
        ("CERTIFICATE OF SERVICE", True, False),
        ("", False, False),
        ("[Fed. R. Civ. P. 5]", False, False),
        ("", False, False),
        ("Hon. Lisa J. Cisneros", False, False),
        ("", False, False),
        ("Re: First Amended Complaint", False, False),
        ("(Dkt. 6)", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_wrapped(
        "I, BRENDAN NGWA NFORBI, declare as follows:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "1. I am the Plaintiff in the above-captioned action and appear in propria persona. "
        "I am over the age of eighteen years and not a party to be served with the papers "
        "described below within the meaning of Fed. R. Civ. P. 5.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2. On August 21, 2026, I caused a true and correct copy of the First Amended "
        "Complaint for Damages and Injunctive Relief filed in this action on August 17, 2026 "
        "as Dkt. 6 (the operative pleading) to be served by United States First-Class Mail, "
        "postage prepaid, upon each of the following:",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("Diana Candelaria, Driver Safety Hearing Officer", indent=18)
    d.write_line("California Department of Motor Vehicles", indent=18)
    d.write_line("Legal Affairs Division, Mail Station C128", indent=18)
    d.write_line("2415 First Avenue", indent=18)
    d.write_line("Sacramento, CA 95818", indent=18)
    d.blank_line()
    d.write_line("Steve Gordon, Director", indent=18)
    d.write_line("California Department of Motor Vehicles", indent=18)
    d.write_line("Legal Affairs Division, Mail Station C128", indent=18)
    d.write_line("2415 First Avenue", indent=18)
    d.write_line("Sacramento, CA 95818", indent=18)
    d.blank_line()
    d.write_wrapped(
        "3. Defendants Candelaria and Gordon were previously personally served with the "
        "summons and original complaint on August 14, 2026, through the Sacramento County "
        "Sheriff at the DMV Legal Affairs Division address set forth above. This mailing "
        "was made pursuant to Fed. R. Civ. P. 5(a) and 5(b)(2)(C) to serve the First Amended "
        "Complaint on parties who have been served with process but have not yet appeared.",
        first_indent=0,
    )
    _sign(d)
    d.save()
    stamp_signature(out)
    print(f"Wrote {out}")


def main() -> None:
    OUT_MEZA.parent.mkdir(parents=True, exist_ok=True)
    OUT_CAND.parent.mkdir(parents=True, exist_ok=True)
    build_meza(OUT_MEZA)
    build_candelaria(OUT_CAND)


if __name__ == "__main__":
    main()
