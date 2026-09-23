#!/usr/bin/env python3
"""Matter 28 -- Plaintiff's [Proposed] Order Denying Defendants' Motion to
Dismiss, on portfolio pleading paper.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Cleans up the Sep. 23, 2026 12-pt draft: house attorney block (adds e-mail),
movants named in full, no recital of a reply that has not been filed, and a
judicial-notice paragraph that tracks the Opposition's Section IV concession
(existence, filing dates, and legal effect -- not truth, not demurrer
advocacy; the July 15, 2026 state order is an order sustaining a demurrer,
not a judgment). Denial + Rule 12(a)(4)(A) answer deadline unchanged.
The POS is matter28-proposed-order-pos-email.py (run it after this).

    python3 internal/scripts/matter28-proposed-order-mtd.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402

ROOT = SCRIPT_DIR.parent
OUT = ROOT / "public/documents/matter-28/Proposed Order Denying MTD (N.D. Cal. 3-26-cv-07504-LJC) (Sep 23 2026).pdf"
SCRATCH = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "fde9b68e-7f08-5546-b231-a91ce9f193c5/scratchpad/Proposed-Order-Denying-MTD-Sep23.pdf"
)

FOOTER = "[PROPOSED] ORDER DENYING DEFENDANTS' MOTION TO DISMISS -- NEWANFORBI v. SMITH (N.D. Cal.)"
RIGHT_OFFSET = 28

ATTORNEY_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("SHANNON SMITH, LCSW, Chief", True, False),
    ("Executive Officer and Founder of", True, False),
    ("HOPE Program, an individual; and", True, False),
    ("HOPE PSYCHOTHERAPY, INC.,", True, False),
    ("d/b/a HOPE PROGRAM, a California", True, False),
    ("corporation,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
    ("", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 3:26-cv-07504-LJC", False, False),
    ("", False, False),
    ("[PROPOSED] ORDER", True, False),
    ("DENYING DEFENDANTS'", True, False),
    ("MOTION TO DISMISS", True, False),
    ("(ECF NO. 15)", True, False),
    ("", False, False),
    ("Date: October 20, 2026", False, False),
    ("Time: 10:30 a.m.", False, False),
    ("Courtroom: G, 15th Floor", False, False),
    ("Judge: Hon. Lisa J. Cisneros", False, False),
]

PARAS = [
    "Before the Court is the Motion to Dismiss Plaintiff's Complaint filed by Defendants "
    "Shannon Smith, LCSW, and HOPE Psychotherapy, Inc., d/b/a HOPE Program (ECF No. 15). "
    "Having considered the motion, Defendants' request for judicial notice, the papers filed "
    "in support of and in opposition to the motion, and the record, and good cause appearing, "
    "the Court ORDERS as follows:",
    "1.  Defendants' request for judicial notice is GRANTED IN PART. The Court takes judicial "
    "notice of the existence, filing dates, and legal effect of the state-court records, but not "
    "of the truth of any disputed factual assertion in them. Grounds argued in the state-court "
    "demurrer papers are not treated as findings of that court. The state court's July 15, 2026 "
    "order is noticed as an order sustaining a demurrer; it is not a judgment of dismissal.",
    "2.  Defendants' Motion to Dismiss Plaintiff's Complaint (ECF No. 15) is DENIED.",
    "3.  Defendants shall serve and file their answer to the Complaint within fourteen (14) "
    "days after notice of this Order. Fed. R. Civ. P. 12(a)(4)(A).",
]


def main() -> None:
    for out in (OUT, SCRATCH):
        out.parent.mkdir(parents=True, exist_ok=True)
        d = PleadingPaper(str(out), doc_title_footer=FOOTER)
        c = d.c
        y0 = d._line_y(0)
        for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
            c.setFont(font, size)
            c.drawString(CONTENT_LEFT, y0 - i * 15, text)
        d.current_line = 4
        d.blank_line()
        d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
        d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
        d.blank_line()
        d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
        d.blank_line()
        for i, para in enumerate(PARAS):
            d.write_wrapped(para, first_indent=36)
            d.blank_line()
        d.ensure_space(9)
        d.write_line("IT IS SO ORDERED.", bold=True)
        d.blank_line()
        d.write_line("Dated: ________________")
        d.blank_line()
        d.blank_line()
        d.write_line("________________________________________", right=True, right_margin_offset=RIGHT_OFFSET)
        d.write_line("HON. LISA J. CISNEROS", right=True, right_margin_offset=RIGHT_OFFSET)
        d.write_line("United States Magistrate Judge", right=True, right_margin_offset=RIGHT_OFFSET)
        d.save()
        print(f"Wrote {out} ({d.page_num} pages)")


if __name__ == "__main__":
    main()
