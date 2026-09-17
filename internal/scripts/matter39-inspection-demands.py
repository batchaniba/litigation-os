#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 39 — unsigned inspection / personnel-file demands.

REVIEW DRAFTS. Plaintiff signs and sends these himself. Do not stamp a
signature. Not yet served.

    python3 internal/scripts/matter39-inspection-demands.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal/public/documents/matter-39"

DATE = "September 15, 2026"

body = ParagraphStyle(
    "body",
    fontName="Times-Roman",
    fontSize=12,
    leading=16.5,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
)
plain = ParagraphStyle(
    "plain",
    fontName="Times-Roman",
    fontSize=12,
    leading=16.5,
    alignment=TA_LEFT,
    spaceAfter=2,
)
bold = ParagraphStyle(
    "bold",
    fontName="Times-Bold",
    fontSize=12,
    leading=16.5,
    alignment=TA_LEFT,
    spaceAfter=2,
)
bullet = ParagraphStyle(
    "bullet",
    fontName="Times-Roman",
    fontSize=12,
    leading=16.5,
    alignment=TA_JUSTIFY,
    spaceAfter=4,
    leftIndent=18,
    bulletIndent=4,
)
banner = ParagraphStyle(
    "banner",
    fontName="Times-Bold",
    fontSize=10,
    leading=13,
    alignment=TA_LEFT,
    spaceAfter=10,
)


def letterhead(story):
    story.append(Paragraph("BRENDAN NGWA NFORBI", bold))
    story.append(Paragraph("Plaintiff, In Propria Persona", plain))
    story.append(Paragraph("1455 Cat Tail Drive", plain))
    story.append(Paragraph("Stockton, CA 95204", plain))
    story.append(Paragraph("Telephone: (209) 801-4442", plain))
    story.append(Paragraph("E-mail: bnn.cdl@gmail.com", plain))
    story.append(Spacer(1, 14))
    story.append(Paragraph(DATE, plain))
    story.append(Spacer(1, 12))


def signature_block(story):
    story.append(Spacer(1, 8))
    story.append(Paragraph("Very truly yours,", plain))
    story.append(Spacer(1, 36))
    story.append(Paragraph("_________________________________", plain))
    story.append(Paragraph("Brendan Ngwa Nforbi", plain))
    story.append(Paragraph("Plaintiff, In Propria Persona", plain))
    story.append(Paragraph("Telephone: (209) 801-4442", plain))
    story.append(Paragraph("E-mail: bnn.cdl@gmail.com", plain))


def footer(canvas, doc, title):
    canvas.saveState()
    canvas.setFont("Times-Bold", 8)
    canvas.drawCentredString(
        letter[0] / 2.0,
        0.55 * inch,
        f"{title} -- UNSIGNED REVIEW DRAFT -- NOT YET SERVED",
    )
    canvas.setFont("Times-Roman", 8)
    canvas.drawCentredString(letter[0] / 2.0, 0.40 * inch, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def write_fa(path: Path) -> None:
    story = []
    letterhead(story)
    story.append(Paragraph(
        "UNSIGNED REVIEW DRAFT -- Plaintiff signs and sends this himself. "
        "Not yet served.",
        banner,
    ))
    story.append(Paragraph("First Advantage Background Services Corp.", plain))
    story.append(Paragraph("Consumer Disclosure Center", plain))
    story.append(Paragraph("P.O. Box 105292", plain))
    story.append(Paragraph("Atlanta, GA 30348", plain))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Re: Statutory inspection and consumer-file request -- Brendan Ngwa Nforbi",
        bold,
    ))
    story.append(Paragraph("Employer / user: Best Buy Co., Inc.", plain))
    story.append(Paragraph(
        "Worksite: 6653 Hopkins Road, Tracy, California 95377", plain,
    ))
    story.append(Paragraph(
        "Screening: October 17, 2023 (Q09078711; account BEST BUY 11759586)",
        plain,
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("To First Advantage Background Services Corp.:", body))
    story.append(Paragraph(
        "I am Brendan Ngwa Nforbi. I also appear in records as Brendan Ngehsi "
        "Newanforbi and Ngehsi Newanforbi. I am the consumer who was the subject "
        "of an employment background screening that Best Buy Co., Inc. procured "
        "or caused you to prepare in connection with an accepted hire at the "
        "Tracy, California warehouse at 6653 Hopkins Road, on October 17, 2023. "
        "Best Buy's own authorization named First Advantage Consumer Center. "
        "Your reporting service emailed me a Best Buy drug-test order that "
        "afternoon, Re:Quest QPassport/Barcode Q09078711, account BEST BUY "
        "(11759586).",
        body,
    ))
    story.append(Paragraph(
        "This is a written request under California Civil Code sections 1786.10 "
        "and 1786.22, and under 15 U.S.C. section 1681g, for inspection and a "
        "complete copy of all information First Advantage maintains on me in "
        "connection with that Best Buy screening and generally.",
        body,
    ))
    story.append(Paragraph("Please produce, at a minimum:", body))
    items = [
        "1. My complete consumer file.",
        "2. Every consumer report, investigative consumer report, and report "
        "version furnished to Best Buy Co., Inc. or any Best Buy affiliate "
        "concerning me, including drafts, updates, and re-adjudications.",
        "3. Order number, client / requestor profile, package identifier, "
        "completion date, and transmission date, including Q09078711 and "
        "account 11759586.",
        "4. Component-by-component results and raw source-of-record fields, "
        "including any sex-offender-registry, Megan's Law, or California-registry "
        "search.",
        "5. Adjudication status, client-specific criteria, and any Best Buy "
        "decision codes applied to my file.",
        "6. Access logs identifying every Best Buy user who viewed the report "
        "and the timestamps.",
        "7. Any pre-adverse or adverse-action notice generated, queued, "
        "suppressed, cancelled, or sent.",
        "8. User certifications and Best Buy certifications associated with "
        "the order.",
        "9. Dispute history, if any.",
        "10. A copy of the sources of information used, to the extent Civil Code "
        "sections 1786.10 / 1786.22 and the FCRA require disclosure.",
    ]
    for item in items:
        story.append(Paragraph(item, bullet))
    story.append(Paragraph(
        "I request mailed copies and electronic copies. Mail paper copies to "
        "Brendan Ngwa Nforbi, 1455 Cat Tail Drive, Stockton, CA 95204. Also "
        "email complete electronic copies to bnn.cdl@gmail.com. Email is the "
        "reliable channel.",
        body,
    ))
    story.append(Paragraph(
        "I will supply additional identification reasonably required to locate "
        "the file. I do not authorize any disclosure of this file to Best Buy "
        "beyond what the law already required at the time of the original "
        "employment screen.",
        body,
    ))
    story.append(Paragraph(
        "Please confirm receipt in writing and produce the file promptly. "
        "California Civil Code section 1786.22 requires that the information be "
        "provided during normal business hours and that I be permitted to "
        "receive a copy.",
        body,
    ))
    signature_block(story)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.9 * inch,
    )
    doc.build(
        story,
        onFirstPage=lambda c, d: footer(
            c, d, "FIRST ADVANTAGE INSPECTION DEMAND -- MATTER 39"
        ),
        onLaterPages=lambda c, d: footer(
            c, d, "FIRST ADVANTAGE INSPECTION DEMAND -- MATTER 39"
        ),
    )


def write_bb(path: Path) -> None:
    story = []
    letterhead(story)
    story.append(Paragraph(
        "UNSIGNED REVIEW DRAFT -- Plaintiff signs and sends this himself. "
        "Serve the current California Secretary of State agent, not "
        "6653 Hopkins Road. Not yet served.",
        banner,
    ))
    story.append(Paragraph("Best Buy Co., Inc.", plain))
    story.append(Paragraph("c/o current California registered agent", plain))
    story.append(Paragraph("(confirm Secretary of State listing before mailing)", plain))
    story.append(Paragraph("Copy: ATTN Employment Screening", plain))
    story.append(Paragraph("7601 Penn Avenue South, Richfield, MN 55423", plain))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Re: Labor Code section 1198.5 personnel-file request",
        bold,
    ))
    story.append(Paragraph(
        "Brendan Ngwa Nforbi -- accepted hire, Tracy warehouse",
        plain,
    ))
    story.append(Paragraph(
        "6653 Hopkins Road, Tracy, California 95377 -- October 17, 2023",
        plain,
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("To Best Buy Co., Inc.:", body))
    story.append(Paragraph(
        "I am Brendan Ngwa Nforbi. I also appear in records as Brendan Ngehsi "
        "Newanforbi and Ngehsi Newanforbi. On October 17, 2023, Best Buy offered "
        "me employment as General Warehouse Worker / 2nd Shift at $22.60 per "
        "hour, requisition 928556BR, at 6653 Hopkins Road, Tracy, California. "
        "I accepted the offer. Best Buy required a background check the same "
        "afternoon, named First Advantage, ordered a drug test (Q09078711), I "
        "completed the drug screening, and Best Buy then ceased communication.",
        body,
    ))
    story.append(Paragraph(
        "This is a written request under California Labor Code section 1198.5 "
        "to inspect and receive a copy of my personnel records relating to my "
        "performance and to any grievance concerning me, and of every related "
        "hiring, onboarding, screening, and decision record Best Buy maintains.",
        body,
    ))
    story.append(Paragraph(
        "Because I am no longer employed by Best Buy, I request that copies "
        "be produced by mail and by email rather than an in-person inspection. "
        "Produce complete copies within the time Labor Code section 1198.5 "
        "requires.",
        body,
    ))
    story.append(Paragraph("Please produce, at a minimum:", body))
    items = [
        "1. My complete applicant, onboarding, and personnel file.",
        "2. Every offer, acceptance, start-date, badge, scheduling, or "
        "onboarding record, including the October 17, 2023 offer and Candidate "
        "Zone records.",
        "3. Every background-check disclosure, authorization, consent, and "
        "related form shown to or signed by me, including the California "
        "disclosure PDFs attached to the October 17, 2023 sequence.",
        "4. Every consumer report or investigative consumer report Best Buy "
        "obtained concerning me, including the complete First Advantage report "
        "and all versions.",
        "5. Order, package, adjudication, access, and transmission records for "
        "that screen, including Q09078711 and account 11759586.",
        "6. Applicant-tracking or hiring-system status history and reason codes.",
        "7. All pre-adverse and adverse-action notices, including records "
        "showing whether any were generated, queued, transmitted, suppressed, "
        "or cancelled.",
        "8. Communications concerning my screen, hire, or the decision to stop "
        "the employment, including communications involving Jose Tapia and "
        "Daisy Calvary.",
        "9. The identity of the Best Buy legal entity that employed or would "
        "have employed me and that ordered or used the report.",
    ]
    for item in items:
        story.append(Paragraph(item, bullet))
    story.append(Paragraph(
        "Mail paper copies to Brendan Ngwa Nforbi, 1455 Cat Tail Drive, "
        "Stockton, CA 95204. Also email complete electronic copies to "
        "bnn.cdl@gmail.com. Email is the reliable channel.",
        body,
    ))
    story.append(Paragraph(
        "This request is not a settlement communication, not a complaint, and "
        "not a waiver of any claim, defense, or statute of limitations. I "
        "reserve all rights, including claims under the Fair Credit Reporting "
        "Act, the Investigative Consumer Reporting Agencies Act, and Penal Code "
        "section 290.46.",
        body,
    ))
    signature_block(story)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.9 * inch,
    )
    doc.build(
        story,
        onFirstPage=lambda c, d: footer(
            c, d, "BEST BUY SECTION 1198.5 DEMAND -- MATTER 39"
        ),
        onLaterPages=lambda c, d: footer(
            c, d, "BEST BUY SECTION 1198.5 DEMAND -- MATTER 39"
        ),
    )


def main() -> None:
    out_dir = Path(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else OUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    fa = out_dir / "Inspection Demand - First Advantage ICRAA 1786.22 (Sep 15 2026).pdf"
    bb = out_dir / "Personnel File Demand - Best Buy Labor Code 1198.5 (Sep 15 2026).pdf"
    write_fa(fa)
    write_bb(bb)
    print(f"Wrote {fa}")
    print(f"Wrote {bb}")


if __name__ == "__main__":
    main()
