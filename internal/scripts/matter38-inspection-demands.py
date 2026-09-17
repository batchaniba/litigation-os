#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 38 — unsigned inspection / personnel-file demands.

REVIEW DRAFTS. Plaintiff signs and sends these himself. Do not stamp a
signature. Not yet served.

    python3 internal/scripts/matter38-inspection-demands.py
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
OUT_DIR = ROOT / "internal/public/documents/matter-38"

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
    canvas.drawCentredString(
        letter[0] / 2.0, 0.40 * inch, f"Page {canvas.getPageNumber()}"
    )
    canvas.restoreState()


def write_asurint(path: Path) -> None:
    story = []
    letterhead(story)
    story.append(Paragraph(
        "UNSIGNED REVIEW DRAFT -- Plaintiff signs and sends this himself. "
        "Not yet served.",
        banner,
    ))
    story.append(Paragraph("Asurint", plain))
    story.append(Paragraph("P.O. Box 14730", plain))
    story.append(Paragraph("Cleveland, OH 44114", plain))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Re: Statutory inspection and consumer-file request -- Brendan Ngwa Nforbi",
        bold,
    ))
    story.append(Paragraph(
        "Employer / user: Swift Transportation Co. of Arizona LLC (USDOT 54283)",
        plain,
    ))
    story.append(Paragraph(
        "Screening: September 25-October 5, 2023 (letter 76326281-1916808)",
        plain,
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("To Asurint:", body))
    story.append(Paragraph(
        "I am Brendan Ngwa Nforbi. I also appear in records as Brendan Ngehsi "
        "Ngwa Nforbi, Brendan Ngehsi Nforbi, Ngehsi Newanforbi, and Brendan "
        "Ngehsi Ngwanforbi. I am the consumer who was the subject of an "
        "employment background screening that Swift Transportation Co. of "
        "Arizona LLC procured or caused to be prepared in connection with a "
        "Class A Driver application in September and October 2023. Swift's "
        "October 5, 2023 post-adverse letter named Asurint, of Cleveland, "
        "Ohio, as a source of a consumer report that influenced the employment "
        "decision. Swift's September 26, 2023 pre-adverse packet was numbered "
        "76326281-1916808.",
        body,
    ))
    story.append(Paragraph(
        "This is a written request under California Civil Code sections 1786.10 "
        "and 1786.22, and under 15 U.S.C. section 1681g, for inspection and a "
        "complete copy of all information Asurint maintains on me in "
        "connection with that Swift screening and generally.",
        body,
    ))
    story.append(Paragraph("Please produce, at a minimum:", body))
    items = [
        "1. My complete consumer file.",
        "2. Every consumer report, investigative consumer report, and report "
        "version furnished to Swift Transportation Co. of Arizona LLC or any "
        "Swift affiliate concerning me, including drafts, updates, and "
        "re-adjudications.",
        "3. Order number, client / requestor profile, package identifier, "
        "completion date, and transmission date, including 76326281-1916808.",
        "4. Component-by-component results and raw source-of-record fields, "
        "including any NSOPW, sex-offender-registry, Megan's Law, or "
        "California-registry search, and every snapshot while any such "
        "component remained Processing.",
        "5. Adjudication status, client-specific criteria, and any Swift "
        "decision codes applied to my file.",
        "6. Access logs identifying every Swift user who viewed the report "
        "and the timestamps, including any access between September 26, 2023, "
        "and October 5, 2023.",
        "7. Any pre-adverse or adverse-action notice generated, queued, "
        "suppressed, cancelled, or sent.",
        "8. User certifications and Swift certifications associated with "
        "the order.",
        "9. Dispute history, if any.",
        "10. A copy of the sources of information used, to the extent Civil "
        "Code sections 1786.10 / 1786.22 and the FCRA require disclosure.",
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
        "the file. I do not authorize any disclosure of this file to Swift "
        "beyond what the law already required at the time of the original "
        "employment screen.",
        body,
    ))
    story.append(Paragraph(
        "Please confirm receipt in writing and produce the file promptly. "
        "California Civil Code section 1786.22 requires that the information "
        "be provided during normal business hours and that I be permitted to "
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
            c, d, "ASURINT INSPECTION DEMAND -- MATTER 38"
        ),
        onLaterPages=lambda c, d: footer(
            c, d, "ASURINT INSPECTION DEMAND -- MATTER 38"
        ),
    )


def write_swift(path: Path) -> None:
    story = []
    letterhead(story)
    story.append(Paragraph(
        "UNSIGNED REVIEW DRAFT -- Plaintiff signs and sends this himself. "
        "Serve the current California Secretary of State agent, not a "
        "terminal. Not yet served.",
        banner,
    ))
    story.append(Paragraph("Swift Transportation Co. of Arizona LLC", plain))
    story.append(Paragraph("c/o current California registered agent", plain))
    story.append(Paragraph("(confirm Secretary of State listing before mailing)", plain))
    story.append(Paragraph(
        "Courtesy copy: ATTN Recruiting / Background Screening",
        plain,
    ))
    story.append(Paragraph("2200 South 75th Avenue, Phoenix, AZ 85043", plain))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Re: Labor Code section 1198.5 personnel-file request",
        bold,
    ))
    story.append(Paragraph(
        "Brendan Ngwa Nforbi -- Class A Driver application",
        plain,
    ))
    story.append(Paragraph(
        "September 22 through October 5, 2023 -- USDOT 54283",
        plain,
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("To Swift Transportation Co. of Arizona LLC:", body))
    story.append(Paragraph(
        "I am Brendan Ngwa Nforbi. I also appear in records as Brendan Ngehsi "
        "Ngwa Nforbi, Brendan Ngehsi Nforbi, Ngehsi Newanforbi, and Brendan "
        "Ngehsi Ngwanforbi. On September 22, 2023, Swift recruiters Robin "
        "Kaufman and Matt Hutto emailed me through Tenstreet about a Class A "
        "Driver application. On September 25, Swift queried my FMCSA "
        "Clearinghouse record (USDOT 54283). On September 26, Swift sent a "
        "pre-adverse packet numbered 76326281-1916808. On October 5, Swift "
        "sent a post-adverse letter stating that it had decided not to employ "
        "me based in whole or in part on consumer reports from Asurint, "
        "Tenstreet, DriverIQ, FMCSA-DOT, and Equifax Work Number.",
        body,
    ))
    story.append(Paragraph(
        "This is a written request under California Labor Code section 1198.5 "
        "to inspect and receive a copy of my personnel records relating to my "
        "performance and to any grievance concerning me, and of every related "
        "hiring, onboarding, screening, and decision record Swift maintains.",
        body,
    ))
    story.append(Paragraph(
        "Because I am not employed by Swift, I request that copies be produced "
        "by mail and by email rather than an in-person inspection. Produce "
        "complete copies within the time Labor Code section 1198.5 requires.",
        body,
    ))
    story.append(Paragraph("Please produce, at a minimum:", body))
    items = [
        "1. My complete applicant, onboarding, and personnel file.",
        "2. Every offer, application, start-date, or recruiting record, "
        "including Tenstreet / Driver Pulse records and communications "
        "involving Robin Kaufman and Matt Hutto.",
        "3. Every background-check disclosure, authorization, consent, and "
        "related form shown to or signed by me.",
        "4. Every consumer report or investigative consumer report Swift "
        "obtained concerning me, including complete Asurint, Tenstreet, "
        "DriverIQ, Clearinghouse, PSP, CDLIS, MVR, and Equifax Work Number "
        "reports and all versions and snapshots.",
        "5. Order, package, adjudication, access, and transmission records "
        "for that screen, including 76326281-1916808 and any NSOPW component "
        "while it remained Processing.",
        "6. Applicant-tracking status history and reason codes.",
        "7. All pre-adverse and adverse-action notices, including the "
        "September 26 and October 5, 2023 letters and records showing whether "
        "any later report was generated, queued, transmitted, suppressed, or "
        "cancelled.",
        "8. Communications concerning my screen, application, or the decision "
        "not to employ me.",
        "9. The identity of the Swift legal entity that employed or would "
        "have employed me and that ordered or used the reports.",
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
        "reserve all rights, including claims under Penal Code section "
        "290.46, the Investigative Consumer Reporting Agencies Act, and the "
        "Unfair Competition Law.",
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
            c, d, "SWIFT SECTION 1198.5 DEMAND -- MATTER 38"
        ),
        onLaterPages=lambda c, d: footer(
            c, d, "SWIFT SECTION 1198.5 DEMAND -- MATTER 38"
        ),
    )


def main() -> None:
    out_dir = Path(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else OUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    fa = out_dir / "Inspection Demand - Asurint ICRAA 1786.22 (Sep 15 2026).pdf"
    sw = out_dir / "Personnel File Demand - Swift Labor Code 1198.5 (Sep 15 2026).pdf"
    write_asurint(fa)
    write_swift(sw)
    print(f"Wrote {fa}")
    print(f"Wrote {sw}")


if __name__ == "__main__":
    main()
