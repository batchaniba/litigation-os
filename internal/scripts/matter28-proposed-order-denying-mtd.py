# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Matter 28 -- [Proposed] Order Denying Defendants' Motion to Dismiss.

Newanforbi v. Shannon Smith, LCSW, et al., N.D. Cal. No. 3:26-cv-07504-LJC.

Regenerates the plaintiff-lodged proposed order on the house pleading paper,
with the four-border Proof of Service appended, and the hearing date corrected
to October 27, 2026 per the Court's Order Continuing Motion Hearing (ECF No.
22). The order page carries the JUDGE's signature block (no plaintiff stamp);
only the POS is stamped with the universal signature.

    python3 internal/scripts/matter28-proposed-order-denying-mtd.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pymupdf

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL, ProofOfServiceFields, build_proof_of_service,
)

REPO_ROOT = SCRIPT_DIR.parent.parent
DOCS = REPO_ROOT / "internal" / "public" / "documents" / "matter-28"
OUT = DOCS / "Proposed Order Denying MTD with POS (Oct 27 hearing) (Sep 24 2026).pdf"
SCRATCH = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "3fd8a963-2d26-598c-823f-b47c1b152f34/scratchpad/"
    "Proposed-Order-Denying-MTD-with-POS.pdf"
)
_TMP = SCRATCH.parent / "_order_pages.pdf"

DOC_TITLE_FOOTER = (
    "[PROPOSED] ORDER DENYING DEFENDANTS' MOTION TO DISMISS -- "
    "NEWANFORBI v. SMITH (N.D. Cal.)"
)
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

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
    ("[PROPOSED] ORDER DENYING", True, False),
    ("DEFENDANTS' MOTION TO", True, False),
    ("DISMISS (ECF No. 15)", True, False),
    ("", False, False),
    ("Date: October 27, 2026", False, False),
    ("Time: 10:30 a.m.", False, False),
    ("Courtroom: G, 15th Floor", False, False),
    ("Judge: Hon. Lisa J. Cisneros", False, False),
]

BODY = [
    ("P", "Before the Court is the Motion to Dismiss Plaintiff's Complaint filed by "
          "Defendants Shannon Smith, LCSW, and HOPE Psychotherapy, Inc., d/b/a HOPE "
          "Program (ECF No. 15). Having considered the motion, Defendants' request for "
          "judicial notice, the papers filed in support of and in opposition to the "
          "motion, and the record, and good cause appearing, the Court ORDERS as follows:"),
    ("P", "1.  Defendants' request for judicial notice is GRANTED IN PART. The Court "
          "takes judicial notice of the existence, filing dates, and legal effect of the "
          "state-court records, but not of the truth of any disputed factual assertion in "
          "them. Grounds argued in the state-court demurrer papers are not treated as "
          "findings of that court. The state court's July 15, 2026 order is noticed as an "
          "order sustaining a demurrer; it is not a judgment of dismissal."),
    ("P", "2.  Defendants' Motion to Dismiss Plaintiff's Complaint (ECF No. 15) is DENIED."),
    ("P", "3.  Defendants shall serve and file their answer to the Complaint within "
          "fourteen (14) days after notice of this Order. Fed. R. Civ. P. 12(a)(4)(A)."),
    ("P", "IT IS SO ORDERED."),
]

SIG_LINES = [
    "Dated: ________________",
    "",
    "",
    "________________________________________",
    "HON. LISA J. CISNEROS",
    "United States Magistrate Judge",
]


def render_order(path: Path) -> None:
    d = PleadingPaper(str(path), doc_title_footer=DOC_TITLE_FOOTER)
    c = d.c
    atty_y = d._line_y(0)
    for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
        c.setFont(font, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, text)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    for _kind, text in BODY:
        d.write_wrapped(text, first_indent=36)
        d.blank_line()
    d.ensure_space(len(SIG_LINES) + 1)
    for ln in SIG_LINES:
        if ln:
            d.write_line(ln, indent=36)
        else:
            d.blank_line()
    d.save()


def pos_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=["SHANNON SMITH, LCSW;", "HOPE PSYCHOTHERAPY, INC."],
        defendant_role="Defendants",
        case_number="3:26-cv-07504-LJC",
        title="PROOF OF SERVICE",
        service_date="September 24, 2026",
        document_title="[PROPOSED] ORDER DENYING DEFENDANTS' MOTION TO DISMISS",
        recipients=[
            "Cynthia G. Lawrence, Esq. — cynthia@sims-law.net",
            "Blaze Van Dine, Esq. — blaze@sims-law.net",
            "Eric T. Martinez, Esq. — emartinez@sims-law.net",
            "Sims, Lawrence & Broghammer (e-service) — SLB@sims-law.net; "
            "slb-eservice@sims-law.net",
            "",
            "Attorneys for Defendants Shannon Smith, LCSW, and",
            "HOPE Psychotherapy, Inc. (d/b/a HOPE Program)",
        ],
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=True,
        district_line=DISTRICT_NDCAL,
        by_email=True,
    )


def main() -> None:
    _TMP.parent.mkdir(parents=True, exist_ok=True)
    render_order(_TMP)
    pos_tmp = _TMP.parent / "_order_pos.pdf"
    build_proof_of_service(pos_tmp, pos_fields())
    m = pymupdf.open(str(_TMP))
    n = m.page_count
    m.insert_pdf(pymupdf.open(str(pos_tmp)))
    for out in (OUT, SCRATCH):
        out.parent.mkdir(parents=True, exist_ok=True)
        m.save(str(out))
    for p in (_TMP, pos_tmp):
        try:
            p.unlink()
        except OSError:
            pass
    print(f"Wrote {OUT} ({n} order pages + {m.page_count - n} POS = {m.page_count} pages)")


if __name__ == "__main__":
    main()
