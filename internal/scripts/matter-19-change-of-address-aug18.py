#!/usr/bin/env python3
"""Matter 19 Notice of Change of Address — August 18, 2026.

States Petitioner's address of record on C2604791 as
1455 Cat Tail Drive, Stockton, CA 95204 only. Does not recite any
prior address. Signed with the portfolio universal signature.
Does not overwrite the August 17 file.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pleading_paper import (  # noqa: E402
    CONTENT_LEFT,
    COURT_LINE1,
    PleadingPaper,
)
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT = (
    ROOT
    / "internal/public/documents/matter-19"
    / "Notice of Change of Address (Aug 18 2026).pdf"
)

EXEC_DATE = "August 18, 2026"
ADDRESS = "1455 Cat Tail Drive, Stockton, CA 95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
FOOTER = "NOTICE OF CHANGE OF ADDRESS -- IN RE NEWANFORBI v. DODD ET AL."

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Petitioner, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]


def build() -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(OUT), doc_title_footer=FOOTER)
    c = d.c

    atty_y = d._line_y(0)
    atty_lh = 15
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, txt)
    d.current_line = 4
    d.blank_line()

    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line("COUNTY OF SANTA CLARA", bold=True, center=True)
    d.blank_line()

    left = [
        ("In re:", False, False),
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("CDC No. BF3571,", False, False),
        ("", False, False),
        ("                          Petitioner,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("KEELY DODD, CDCR, in her individual", True, False),
        ("capacity;", True, False),
        ("JEFF MACOMBER, Secretary, CDCR;", True, False),
        ("", False, False),
        ("                          Respondents.", False, False),
    ]
    right = [
        ("Case No. C2604791", False, False),
        ("", False, False),
        ("NOTICE OF CHANGE OF ADDRESS", True, False),
        ("", False, False),
        ("(California Rules of Court, rule 2.200)", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()

    d.write_line("NOTICE OF CHANGE OF ADDRESS", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "TO THE CLERK OF THE COURT AND ALL PARTIES AND THEIR ATTORNEYS "
        "OF RECORD:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Pursuant to California Rules of Court, rule 2.200, Petitioner hereby "
        "notifies the Court and all parties that Petitioner's address of record "
        "is, effective immediately:",
        first_indent=36,
    )
    d.blank_line()
    d.write_line(ADDRESS, bold=True)
    d.blank_line()
    d.write_wrapped(
        "All future notices, papers, correspondence, and communications in this "
        "action should be directed to the undersigned at the address set forth "
        f"above. The telephone number is {PHONE}. The email address is {EMAIL}.",
        first_indent=36,
    )
    d.blank_line()
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}", bold=False)
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()

    sig_line = "___________________________________"
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], sig_line
    )
    d.write_line(sig_line, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", right=True, right_margin_offset=20)
    d.write_line("Petitioner, In Pro Per", right=True, right_margin_offset=20)
    d.save()
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Generated: {path}")
