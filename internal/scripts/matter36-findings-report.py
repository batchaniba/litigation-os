#!/usr/bin/env python3
"""Render the Matter 36 AT&T evidence-review memorandum."""

from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        BaseDocTemplate,
        Frame,
        HRFlowable,
        PageTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError as exc:
    raise SystemExit("Install reportlab before running this script: python3 -m pip install reportlab") from exc


ROOT = Path(__file__).resolve().parents[2]
OUT = (
    ROOT
    / "internal/public/documents/matter-36"
    / "Matter 36 Findings - AT&T Offer Rescission Evidence Review (Sep 5 2026).pdf"
)

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2E5D7B")
PALE_BLUE = colors.HexColor("#EAF1F5")
PALE_GOLD = colors.HexColor("#F7F1DF")
CHARCOAL = colors.HexColor("#263238")
GRAY = colors.HexColor("#66727A")
LIGHT_GRAY = colors.HexColor("#E2E7EA")
RED = colors.HexColor("#9A2F2F")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT_GRAY)
    canvas.line(0.7 * inch, 0.55 * inch, 7.8 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.7 * inch, 0.36 * inch, "MATTER 36 — PRIVATE LITIGATION-PLANNING MEMORANDUM — NOT FOR FILING")
    canvas.drawRightString(7.8 * inch, 0.36 * inch, f"Page {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceAfter=16,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=7,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=BLUE,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyReport",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.4,
        leading=13.2,
        textColor=CHARCOAL,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletReport",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=12.8,
        leftIndent=15,
        firstLineIndent=-7,
        bulletIndent=5,
        textColor=CHARCOAL,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10.2,
        leading=14.5,
        textColor=RED,
        borderColor=colors.HexColor("#D9B8B8"),
        borderWidth=0.8,
        borderPadding=9,
        backColor=colors.HexColor("#FAEEEE"),
        spaceBefore=6,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="Quote",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=10,
        leading=14,
        textColor=NAVY,
        leftIndent=18,
        rightIndent=18,
        borderColor=BLUE,
        borderWidth=0,
        borderLeftWidth=2,
        borderPadding=8,
        backColor=PALE_BLUE,
        spaceBefore=5,
        spaceAfter=8,
    )
)


def p(text, style="BodyReport"):
    return Paragraph(text.replace("AT&T", "AT&amp;T"), styles[style])


def bullets(items):
    return [p(f"• {item}", "BulletReport") for item in items]


story = [
    Spacer(1, 0.25 * inch),
    p("MATTER 36", "ReportSubtitle"),
    p("AT&T Offer Rescission", "ReportTitle"),
    p("Evidence Review, Litigation Angles, and Pre-Drafting Assessment", "ReportSubtitle"),
    HRFlowable(width="80%", thickness=1.2, color=BLUE, spaceAfter=14),
]

summary_data = [
    [p("<b>Prepared</b>"), p("September 5, 2026")],
    [p("<b>Record reviewed</b>"), p("24 PDFs (42 pages) and one SMS screenshot")],
    [p("<b>Applications</b>"), p("R-107776 Stockton; R-106742 Bilingual Spanish Lodi")],
    [p("<b>Current posture</b>"), p("Pre-filing evidence development; no pleading, demand, or administrative charge")],
]
summary_table = Table(summary_data, colWidths=[1.35 * inch, 5.55 * inch])
summary_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
            ("BOX", (0, 0), (-1, -1), 0.6, LIGHT_GRAY),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT_GRAY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.extend([summary_table, Spacer(1, 12)])

story.extend(
    [
        p("Executive assessment", "Section"),
        p(
            "The record proves that AT&T issued an express written offer for the Lodi bilingual-sales position, "
            "immediately initiated offer and screening tasks, and then withdrew the offer approximately two hours "
            "later. The recruiter attributed the reversal to an unnamed manager’s statement that the applicant did "
            "not pass a Spanish assessment. The record does not contain the actual assessment result, formal offer "
            "terms, acceptance record, or completed background report."
        ),
        p(
            "The strongest present issue is therefore an internally inconsistent hiring process requiring focused "
            "preservation and discovery. The current exhibits do not yet establish discrimination, fraud, retaliation, "
            "consumer-report misuse, or compensable reliance."
        ),
        p(
            "Drafting gate: do not prepare a complaint from the present record. Obtain the formal offer, acceptance "
            "audit, language-assessment file, internal decision communications, screening file, employer identity, "
            "and reliance evidence first.",
            "Callout",
        ),
        p("The central May 28 sequence", "Section"),
    ]
)

sequence = [
    [p("<b>Time</b>"), p("<b>Documented event</b>")],
    [p("10:13 a.m."), p("Workday: AT&T is “excited to officially offer” R-106742 and directs the applicant to review and accept the formal offer.")],
    [p("10:15 a.m."), p("Workday issues the offer-document review task.")],
    [p("10:16 a.m."), p("Workday issues the government-identifiers task.")],
    [p("10:17 a.m."), p("Workday issues the personal-information task.")],
    [p("10:19 a.m."), p("First Advantage invites screening and possible ID.me identity verification for “AT&T Non Management.”")],
    [p("12:23 p.m."), p("Recruiter text: manager will not proceed because the role needs a Spanish speaker and the applicant “did not pass the Spanish assessment.”")],
]
seq_table = Table(sequence, colWidths=[1.1 * inch, 5.8 * inch], repeatRows=1)
seq_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_BLUE]),
            ("BOX", (0, 0), (-1, -1), 0.6, LIGHT_GRAY),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT_GRAY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.extend(
    [
        seq_table,
        Spacer(1, 8),
        p(
            "“Hi Brendan. Unfortunately, the manager advised me that he no longer wants to move forward with your "
            "offer. He stated that he need a Spanish speaker and you did not pass the Spanish assessment. Sorry for "
            "the inconvenience.”",
            "Quote",
        ),
        p(
            "<b>Important qualification:</b> this SMS is the only exhibit asserting a failed result. The LTI notice "
            "contains instructions—not a score, rating, completion record, or pass/fail determination."
        ),
        p("Verified chronology", "Section"),
        p("<b>May 16 — applications and immediate advancement.</b> AT&T received R-107776 for the non-bilingual Stockton Pacific position at 1:15 p.m. and R-106742 for the Bilingual Spanish Lodi position at 2:31 p.m. Both generated interview invitations; Stockton also generated a Virtual Job Tryout."),
        p("<b>May 19–20 — last-minute administrative rescheduling.</b> Stockton’s May 19 interview was canceled 59 minutes before its scheduled time and simultaneously reset for May 22. Lodi’s May 20 interview was canceled nine minutes before its scheduled time and simultaneously reset for May 21. The exhibits prove scheduling, not attendance."),
        p("<b>May 22–25 — Spanish assessment window.</b> AT&T’s provider requested a pre-employment assessment. LTI supplied an ACTFL Telephone OPIc Spanish speaking test, stated that the rating would go to AT&T Taleo, and set expiration at midnight May 25. The record does not prove test completion or the resulting score."),
        p("<b>May 28 — offer, onboarding, screening, and reversal.</b> AT&T’s Workday and First Advantage systems advanced the applicant through an explicit offer workflow before the recruiter communicated the manager’s reversal."),
        p("Ranked litigation angles", "Section"),
        p("1. Offer withdrawal / promissory estoppel", "Subsection"),
        p(
            "This is the strongest factual inquiry. The offer email and the recruiter’s phrase “your offer” establish "
            "that AT&T communicated an offer. The onboarding cascade reinforces that the process had advanced beyond "
            "an interview indication. A viable claim still requires a clear promise, reasonable reliance, actual "
            "detriment, and enforceable terms."
        ),
    ]
)
story.extend(
    bullets(
        [
            "<b>Evidence needed:</b> acceptance timestamp; resignation or reduced work; declined opportunities; travel, relocation, screening, or equipment expenses; compensation and start date.",
            "<b>Principal defenses:</b> no acceptance; express language-test or screening condition; automated offer issued in error; at-will employment; no measurable reliance during the two-hour interval.",
        ]
    )
)
story.extend(
    [
        p("2. Contract / implied covenant", "Subsection"),
        p(
            "Potentially viable only after production of the formal offer and Candidate Home audit. The current email "
            "directs the applicant to review and accept a separate formal document; it does not itself prove acceptance. "
            "Conditional and at-will terms may foreclose expectancy damages even if an agreement briefly existed."
        ),
        p("3. Negligent misrepresentation or fraud", "Subsection"),
        p(
            "The near-immediate reversal supports inquiry into whether AT&T lacked a reasonable basis to issue the "
            "offer after the assessment window closed. It does not prove that the offer was false when made, that anyone "
            "knew it was false, or that AT&T intended consequential reliance. A workflow mistake is at least as consistent "
            "with the exhibits as fraudulent intent."
        ),
        p("4. FEHA national-origin, ancestry, accent, or language discrimination", "Subsection"),
        p(
            "Presently weak. The stated reason is failure to satisfy Spanish proficiency for an expressly bilingual "
            "position—a facially job-related criterion. The theory materially improves only if the score was inaccurate, "
            "accent-biased, inconsistently applied, unsupported by a validated standard, or used as pretext after the "
            "manager learned protected information."
        ),
    ]
)
story.extend(
    bullets(
        [
            "<b>Useful proof:</b> actual score and audio; passing threshold; rater and methodology; human review; retest policy; comparator outcomes; adverse-impact validation; applicant’s independent Spanish qualifications.",
            "<b>Stockton relevance:</b> the unresolved non-bilingual application may test AT&T’s explanation, but different stores, managers, and requisitions limit the comparison.",
        ]
    )
)
story.extend(
    [
        p("5. Fair Chance Act, FCRA, and ICRAA", "Subsection"),
        p(
            "Contingent only. The First Advantage invitation proves that screening was initiated after the offer. It "
            "does not prove authorization, report completion, report contents, delivery to AT&T, or screening-based "
            "adverse action. The post-offer timing may favor AT&T under the Fair Chance Act. Consumer-report claims "
            "require the complete First Advantage file and disclosure/adverse-action workflow."
        ),
        p("6. Penal Code § 290.46 registry-information use", "Subsection"),
        p(
            "No present factual basis. Nothing in the 25 exhibits identifies criminal history or Megan’s Law registry "
            "information. The recruiter’s contemporaneous Spanish-assessment explanation points elsewhere. Preserve "
            "the issue only if the screening file later proves prohibited employment use."
        ),
        p("7. Disability, accommodation, and retaliation", "Subsection"),
        p(
            "Unsupported on this record. The assessment materials offered accommodation channels, and there is no "
            "documented disability, request, denial, protected complaint, or pre-decision opposition activity."
        ),
        p("Material evidentiary tensions", "Section"),
    ]
)
story.extend(
    bullets(
        [
            "<b>Offer despite alleged failure:</b> if AT&T already possessed a disqualifying score, why did it issue an official offer and screening tasks?",
            "<b>No primary score evidence:</b> the asserted failure is secondhand through the recruiter and unnamed manager.",
            "<b>System mismatch:</b> LTI identifies “AT&T Taleo,” while applications and offer processing use Workday; the score-transfer timing is unknown.",
            "<b>Two requisitions:</b> the record does not disclose the final disposition of the non-bilingual Stockton application.",
            "<b>Attendance gap:</b> reminders establish appointments, but there are no interview attendance records, notes, or scorecards.",
            "<b>Entity gap:</b> “AT&T” and “AT&T Non Management” do not identify the legal employing entity or Lodi store operator.",
        ]
    )
)
story.extend(
    [
        p("Priority evidence plan", "Section"),
    ]
)
evidence_rows = [
    [p("<b>Priority</b>"), p("<b>Evidence to obtain</b>"), p("<b>Why it matters</b>")],
    [p("1"), p("Formal offer packet and Workday audit trail"), p("Terms, conditions, acceptance, approvers, reason codes, arbitration, rescission event")],
    [p("2"), p("Complete LTI/ACTFL file"), p("Completion, audio, score, threshold, transmission time, rater, review and retest procedures")],
    [p("3"), p("Patterson and manager communications"), p("Who decided, when, and whether the stated reason was genuine or pretextual")],
    [p("4"), p("Native SMS export and device metadata"), p("Authenticates the screenshot, sender attribution, timing, and complete context")],
    [p("5"), p("Stockton application file"), p("Disposition, interview results, selected candidate, and whether a non-bilingual opening remained")],
    [p("6"), p("First Advantage and ID.me file"), p("Consent, report request/delivery, report contents, cancellation, and adverse-action workflow")],
    [p("7"), p("Reliance and damages records"), p("Acceptance, resignation, declined work, expenses, mitigation, wage rate, start date")],
    [p("8"), p("Legal-employer records"), p("Correct defendant, store operator, service, venue, and contractual party")],
]
evidence_table = Table(evidence_rows, colWidths=[0.7 * inch, 2.4 * inch, 3.8 * inch], repeatRows=1)
evidence_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_BLUE]),
            ("BOX", (0, 0), (-1, -1), 0.6, LIGHT_GRAY),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT_GRAY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (0, 1), (0, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story.extend(
    [
        evidence_table,
        p("Conservative deadline controls", "Section"),
        p(
            "Use May 28, 2026 as the conservative adverse-act/accrual date unless later evidence establishes another "
            "date. Independently calendar any CRD/EEOC exhaustion requirement and any contract, misrepresentation, "
            "consumer-report, or privacy limitation period before drafting. Do not rely solely on this memorandum for "
            "deadline computation because the correct period depends on the final theory, discovery date, tolling, "
            "right-to-sue process, and the missing offer terms."
        ),
        p("Conclusion", "Section"),
        p(
            "The record justifies immediate evidence preservation and targeted information requests. It does not yet "
            "justify naming AT&T’s parent, the recruiter, LTI, First Advantage, or ID.me as defendants. The matter should "
            "remain in pre-filing evidence development until the formal offer and audit trail, language-assessment file, "
            "internal decision communications, screening file, employing-entity identity, and reliance evidence are in hand."
        ),
        Spacer(1, 10),
        p(
            "<b>Bottom line:</b> the process anomaly is real and well documented; actionable liability and damages are not yet established.",
            "Callout",
        ),
    ]
)


doc = BaseDocTemplate(
    str(OUT),
    pagesize=letter,
    rightMargin=0.7 * inch,
    leftMargin=0.7 * inch,
    topMargin=0.65 * inch,
    bottomMargin=0.72 * inch,
    title="Matter 36 Findings — AT&T Offer Rescission Evidence Review",
    author="Interactive Litigation Portfolio",
    subject="Pre-filing evidence review and litigation-angle assessment",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=footer)])
OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story)
print(OUT)
