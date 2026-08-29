# ==========================================================
# NEWANFORBI v. RANDSTAD US, LLC, ET AL. (26CV199902, Alameda Sup. Ct.)
#
# Successor settlement demand as to Randstad US, LLC only, to be
# transmitted AFTER 2:00 p.m. PT August 28, 2026 — the moment the
# August 19 $55,000 / $85,000 figures expire by their own terms.
#
# Do not send this letter before that hour. Do not attach or send the
# unsent August 18 $250,000 letter; that figure stays the internal
# aggressive ceiling.
#
# Anchor: $175,000.00 Randstad-only. Lands above the ~$110,000 moderate
# band and below $250,000 so there is room to settle without walking
# back to $55,000. RK Logistics is not a cheap add-on; a global number
# is its own number, on request.
# ==========================================================
import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

SIGNATURE_IMG = SIGNATURE_PATH
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_DIR = os.path.join(REPO_ROOT, "internal", "public", "documents", "matter-27")

DEMAND_PATH = os.path.join(
    OUT_DIR,
    "Settlement Demand - Randstad US LLC (Aug 28 2026).pdf",
)
COVER_PATH = os.path.join(
    REPO_ROOT,
    "internal",
    "docs",
    "Cover Email - Settlement Demand Randstad US LLC (Aug 28 2026).txt",
)

DATE = "August 28, 2026"
AMOUNT = "$175,000.00"
AMOUNT_WORDS = "One Hundred Seventy-Five Thousand U.S. Dollars"

body = ParagraphStyle(
    "body", fontName="Times-Roman", fontSize=12, leading=16.5,
    alignment=TA_JUSTIFY, spaceAfter=10,
)
bullet = ParagraphStyle(
    "bullet", fontName="Times-Roman", fontSize=12, leading=16.5,
    alignment=TA_JUSTIFY, spaceAfter=8, leftIndent=18, bulletIndent=4,
)
plain = ParagraphStyle(
    "plain", fontName="Times-Roman", fontSize=12, leading=16.5, alignment=TA_LEFT,
)
bold = ParagraphStyle(
    "bold", fontName="Times-Bold", fontSize=12, leading=16.5, alignment=TA_LEFT,
)
heading = ParagraphStyle(
    "heading", fontName="Times-Bold", fontSize=12, leading=16.5,
    alignment=TA_LEFT, spaceBefore=6, spaceAfter=8,
)
small = ParagraphStyle(
    "small", fontName="Times-Roman", fontSize=10, leading=13, alignment=TA_LEFT,
)


def letterhead(story, tagline=None):
    story.append(Paragraph("BRENDAN NGEHSI NEWANFORBI", bold))
    story.append(Paragraph("1455 Cat Tail Drive &bull; Stockton, CA 95204", plain))
    story.append(Paragraph(
        "Telephone: (209) 801-4442 &bull; E-mail: bnn.cdl@gmail.com", plain,
    ))
    if tagline:
        story.append(Spacer(1, 10))
        story.append(Paragraph(tagline, bold))
    story.append(Spacer(1, 16))


def signature_block(story, closing="Very truly yours,"):
    story.append(Paragraph(closing, plain))
    story.append(Spacer(1, 6))
    if os.path.isfile(SIGNATURE_IMG):
        img = Image(SIGNATURE_IMG, width=2.5 * inch, height=2.5 * inch * SIGNATURE_ASPECT)
        img.hAlign = "LEFT"
        story.append(img)
    story.append(Paragraph("Brendan Ngehsi Newanforbi", plain))
    story.append(Paragraph("Plaintiff, In Pro Per", plain))


def stamp_settlement_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Bold", 8.5)
    canvas.drawCentredString(
        letter[0] / 2.0, letter[1] - 0.55 * inch,
        "CONFIDENTIAL SETTLEMENT COMMUNICATION -- Cal. Evid. Code § 1152 / Fed. R. Evid. 408",
    )
    canvas.setFont("Times-Roman", 8.5)
    canvas.drawCentredString(letter[0] / 2.0, 0.62 * inch, f"Page {canvas.getPageNumber()}")
    canvas.setFont("Times-Bold", 8.5)
    canvas.drawCentredString(
        letter[0] / 2.0, 0.45 * inch,
        "SETTLEMENT DEMAND -- NEWANFORBI v. RANDSTAD US, LLC",
    )
    canvas.restoreState()


COVER_EMAIL = """HOLD — do not send before 2:00 p.m. Pacific Time on August 28, 2026.

To: Chad Williams <CWilliams@kcozlaw.com>
Cc: Nathan Chapman <nchapman@kcozlaw.com>
Subject: Newanforbi v. Randstad US, LLC et al. — Settlement Demand (Evid. Code § 1152 / FRE 408)

Attach: Settlement Demand - Randstad US LLC (Aug 28 2026).pdf

---

Chad:

The August 19, 2026 demands ($55,000 Randstad-only / $85,000 global) expired by their own terms at 2:00 p.m. Pacific Time today and are withdrawn. They are not being held.

Attached is my demand to settle as to Randstad US, LLC only: $175,000.00, inclusive of all damages, statutory remedies, attorneys' fees, and costs asserted against Randstad in this action. Please respond on or before 5:00 p.m. Pacific Time on September 8, 2026.

This communication is for compromise purposes and is protected by California Evidence Code section 1152 and Federal Rule of Evidence 408.

Regards,
Brendan Ngehsi Newanforbi
Plaintiff, In Pro Per
(209) 801-4442
bnn.cdl@gmail.com
"""


story = []
letterhead(story, tagline=(
    "CONFIDENTIAL SETTLEMENT COMMUNICATION<br/>"
    "Protected by Cal. Evid. Code &sect; 1152 and Fed. R. Evid. 408"
))

story.append(Paragraph(DATE, plain))
story.append(Spacer(1, 12))
story.append(Paragraph("VIA ELECTRONIC MAIL ONLY", bold))
story.append(Spacer(1, 8))
story.append(Paragraph("Chadwick L. Williams, Esq.", plain))
story.append(Paragraph("Kabat Chapman &amp; Ozmer LLP", plain))
story.append(Paragraph("1150 Spring Street NW, Suite 800", plain))
story.append(Paragraph("Atlanta, GA 30309", plain))
story.append(Paragraph("E-mail: cwilliams@kcozlaw.com", plain))
story.append(Paragraph("<i>Counsel for Defendant Randstad US, LLC</i>", plain))
story.append(Spacer(1, 12))

story.append(Paragraph(
    "Re:&nbsp;&nbsp;<b>Settlement Demand as to Randstad US, LLC</b><br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Newanforbi v. Randstad US, LLC, et al.</b> — "
    "Alameda County Superior Court, Case No. 26CV199902<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Unlawful Use of California Sex Offender Registry Information for "
    "Employment (Pen. Code, &sect; 290.46, subd. (j)(2)(E)); Wrongful Termination; ICRAA<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;InfoMart Order No. 15780719 | Termination: July 15, 2026 | "
    f"<b>Demand: {AMOUNT} (Randstad only)</b>",
    body,
))
story.append(Spacer(1, 6))
story.append(Paragraph("Dear Mr. Williams:", plain))
story.append(Spacer(1, 12))

story.append(Paragraph(
    "The settlement demands I emailed you on August 19, 2026 — $55,000.00 as to Randstad US, "
    "LLC alone, or $85,000.00 globally with The RK Logistics Group, Inc. — expired by their own "
    "terms at 2:00 p.m. Pacific Time today. They are withdrawn. They are not being held. Your "
    "e-mail this morning at 6:49 a.m., stating that you are still conferring with Randstad and will "
    "attempt to respond by September 4, 2026, is noted. Silence before 2:00 p.m. was not a grant of "
    "that request, and it did not keep those figures open.",
    body,
))

story.append(Paragraph(
    "This letter is the demand that is open now. It is made as to Randstad alone. A demand against "
    "both defendants would be a different number and is addressed at the end of this letter.",
    body,
))

story.append(Paragraph("I.&nbsp;&nbsp;WHERE THE CASE STANDS", heading))

story.append(Paragraph(
    "The Complaint was filed July 20, 2026 and assigned to the Honorable Karin Schwartz, Department "
    "20. Both defendants were personally served through their shared agent for service of process on "
    "July 30, 2026, by the Sacramento County Sheriff (Levying Officer File No. 2026026857); the "
    "proofs of service were filed and accepted by the Court on August 7, 2026. Amended notices of the "
    "amount of punitive damages sought under Code of Civil Procedure section 425.115 — $500,000.00 "
    "as to each defendant — were filed and accepted August 6, 2026. A case management conference is "
    "set for December 17, 2026. Randstad's response is due September 15, 2026 under the fifteen-day "
    "extension we agreed on August 18, 2026. RK Logistics' response is due September 14, 2026 under "
    "the single extension I granted its counsel; I will not grant a further one.",
    body,
))

story.append(Paragraph(
    "I mention the posture for one reason: this is a filed, served, and calendared case. The July 20, "
    "2026 pre-filing figure of $85,000.00, and the August 19, 2026 $55,000.00 / $85,000.00 figures "
    "that expired today, have been overtaken by events and are withdrawn.",
    body,
))

story.append(Paragraph("II.&nbsp;&nbsp;THE DOCUMENTARY RECORD", heading))

story.append(Paragraph(
    "Every material fact in this case is documented in Randstad's own records or in the records of "
    "the consumer reporting agency Randstad retained. Nothing turns on whose recollection a jury "
    "credits.",
    body,
))

for text in [
    "<b>June 30, 2026.</b> I applied through Indeed for the “Class C Driver — Bobtail” "
    "position posted by The RK Logistics Group, Inc. at its Newark, California facility. RK Logistics "
    "sent an automated acknowledgment the same evening.",

    "<b>July 1, 2026, 8:08 a.m.</b> Randstad recruiter Dishon Bryant texted me — roughly twelve "
    "hours after the application — “regarding the class C driver position you applied for at "
    "RK Logistics.” On July 2 he referred me to the embedded site manager by name and cell number.",

    "<b>July 7, 2026.</b> Randstad notified me that my “employee status has changed to Rehired.” "
    "That afternoon, Randstad Inhouse Services Site Manager II Danyea Watkins — a Randstad employee "
    "working inside the RK Logistics Fremont facility, using a randstadusa.com address — sent me the "
    "MVR authorization form. At 6:22 p.m., Randstad ordered a background report from InfoMart LLC "
    "(Order No. 15780719).",

    "<b>July 13, 2026.</b> The InfoMart report came back. Seven county and state criminal searches: "
    "“No Record.” Federal criminal: “No Record.” OFAC, OIG, and GSA exclusion "
    "searches: negative. The single adverse item in the entire report is one line — “Subject is "
    "a registered Sex Offender in California” — and the report's overall status reads "
    "“NEEDS APPROVAL, PER CLIENT CRITERIA.” InfoMart sent me the pre-adverse action notice at "
    "1:31 p.m. that day.",

    "<b>July 15, 2026.</b> Randstad terminated me — two business days after the pre-adverse notice, "
    "and without the written adverse action notice the Investigative Consumer Reporting Agencies Act "
    "requires.",
]:
    story.append(Paragraph(text, bullet, bulletText="•"))

story.append(Paragraph(
    "I hold the complete fifteen-page InfoMart report, the pre-adverse notice, the recruiter's text "
    "messages, the rehire notification, and the MVR request. Randstad holds the same records, plus "
    "the internal communications that decided the placement.",
    body,
))

story.append(Paragraph("III.&nbsp;&nbsp;WHY THIS IS RANDSTAD'S EXPOSURE", heading))

story.append(Paragraph(
    "Penal Code section 290.46, subdivision (j)(2)(E), categorically prohibits the use of registry "
    "information “for purposes relating to … Employment.” The narrow exception in "
    "subdivision (j)(1) for use “to protect a person at risk” has no application to a bobtail "
    "driving assignment, and no other exception exists. Subdivision (j) makes any such use actionable: "
    "it “shall make the user liable for the actual damages, and any amount that may be determined "
    "by a jury or a court sitting without a jury, not exceeding three times the amount of actual "
    "damage, and not less than two hundred fifty dollars ($250), and attorney's fees, exemplary "
    "damages, or a civil penalty” of up to $25,000.",
    body,
))

story.append(Paragraph(
    "The “NEEDS APPROVAL, PER CLIENT CRITERIA” designation is a documentary admission that "
    "the adverse decision was the output of a predetermined screening rule keyed to registry status "
    "rather than an individualized assessment. That is the precise conduct the statute forbids.",
    body,
))

story.append(Paragraph(
    "Counsel for RK Logistics has already written that Randstad, not RK Logistics, was my employer, "
    "and that the rejection rested on my motor vehicle record. Whatever the merits of those positions "
    "as to RK Logistics, neither one is available to Randstad:",
    body,
))

for text in [
    "<b>Employer status.</b> Randstad rehired me, opened the payroll relationship, assigned the site "
    "manager, ordered the consumer report, received the pre-adverse notice, and delivered the "
    "termination. It has no argument that someone else was the employer — its co-defendant has "
    "already told me Randstad was.",

    "<b>The MVR theory.</b> The commercial disqualification RK Logistics produced attaches to Class A "
    "commercial privileges and was cleared May 19, 2026. The posting was for a non-commercial Class C "
    "driver. My Class C license was reissued June 11, 2026 — three weeks after the clearance and "
    "five weeks before I applied. The MVR document RK Logistics relies on was not circulated internally "
    "until July 20, 2026, five days after the termination and the same day my demand letters went out.",

    "<b>The FCRA and ICRAA timing.</b> The pre-adverse notice issued July 13. Randstad terminated July "
    "15 — two business days later, inside the statutory waiting period, before the "
    "“NEEDS APPROVAL” flag was ever resolved into a final determination, and with no written "
    "adverse action notice at any point.",
]:
    story.append(Paragraph(text, bullet, bulletText="•"))

story.append(Paragraph(
    "Independent claims lie under the Investigative Consumer Reporting Agencies Act (Civ. Code, "
    "&sect; 1786 et seq.), under <i>Tameny v. Atlantic Richfield Co.</i> (1980) 27 Cal.3d 167 for "
    "termination in violation of fundamental public policy, under Evidence Code section 669 for "
    "negligence per se, and under Business and Professions Code section 17200. Fee-shifting attaches "
    "to the statutory claims. I am in pro per today and am seeking counsel on contingency; a "
    "resolution now is a resolution before that fee exposure begins to accrue.",
    body,
))

story.append(Paragraph("IV.&nbsp;&nbsp;THE DEMAND", heading))

story.append(Paragraph(
    f"<b>Settlement payment: {AMOUNT} ({AMOUNT_WORDS}), Randstad US, LLC only,</b> inclusive of "
    "all damages, statutory remedies, attorneys' fees, and costs asserted against Randstad in this "
    "action.",
    body,
))

for text in [
    "Payable within fifteen (15) business days after execution of a mutually acceptable written "
    "settlement agreement, by check or electronic transfer; payee details and payment instructions "
    "to follow upon acceptance.",

    "Written confirmation that Randstad has issued binding guidance to its California staffing, "
    "recruiting, and background-screening personnel that California Sex Offender Registry information "
    "shall not be used, directly or indirectly, as a basis for any employment or placement decision, "
    "and that its screening vendors are instructed accordingly.",

    "Correction of all internal records of the July 15, 2026 separation to reflect that I am eligible "
    "for rehire, and a commitment that any future employer or agency inquiry about this assignment "
    "will be answered with dates of assignment and eligible-for-rehire status only.",

    "Confidentiality of the settlement amount only. The fact of settlement and the non-monetary terms "
    "may be disclosed. I will not agree to a non-disparagement clause, and I will not sign a release "
    "broader than the claims arising from the July 7 through July 15, 2026 placement and termination.",

    "The release runs to Randstad US, LLC and its officers, employees, and affiliates only. It does "
    "not extend to The RK Logistics Group, Inc., and my claims against RK Logistics are expressly "
    "preserved. Dismissal with prejudice as to Randstad follows cleared payment. No admission of "
    "liability.",
]:
    story.append(Paragraph(text, bullet, bulletText="•"))

story.append(Paragraph("V.&nbsp;&nbsp;A GLOBAL RESOLUTION", heading))

story.append(Paragraph(
    "Your August 18 e-mail invited a global demand against both defendants. I am willing to discuss "
    "one, and if counsel for RK Logistics wishes to participate jointly, I will provide a global "
    "number on request. Two conditions apply. First, a global number will be its own number; it will "
    "not be this demand plus a token for RK Logistics, and it will not be produced by dividing this "
    "demand between the two defendants. Second, nothing about a global discussion changes RK "
    "Logistics' September 14, 2026 deadline to respond. That date is a single extension. I will not "
    "grant a further one.",
    body,
))

story.append(Paragraph("VI.&nbsp;&nbsp;RESPONSE", heading))

story.append(Paragraph(
    "Please respond in writing to bnn.cdl@gmail.com on or before <b>5:00 p.m. Pacific Time on "
    "September 8, 2026</b> — one week before Randstad's responsive pleading is due — with an "
    "acceptance, a good-faith counter-offer, or a request to schedule a call. I am available to "
    "discuss this matter by telephone at any time. If it would move things forward, I am also willing "
    "to consider an early mediation.",
    body,
))

story.append(Paragraph(
    "Settlement discussions do not extend any deadline. The September 15, 2026 date for Randstad's "
    "response stands as agreed. RK Logistics' September 14, 2026 date stands, and no further "
    "extension as to RK Logistics will be granted.",
    body,
))

story.append(Paragraph("VII.&nbsp;&nbsp;PROTECTION AND RESERVATION OF RIGHTS", heading))

story.append(Paragraph(
    "This letter is offered in compromise of a disputed claim and is inadmissible to prove liability "
    "under Evidence Code section 1152 and Federal Rule of Evidence 408. Nothing in it limits my right "
    "to introduce the underlying documentary evidence at trial. Nothing in it waives, releases, or "
    "limits any claim, right, or remedy, all of which are expressly reserved. This letter is not an "
    "offer to settle for any amount less than that stated, nor an admission of fact, law, or "
    "comparative fault.",
    body,
))

story.append(Paragraph("I look forward to hearing from you.", body))
story.append(Spacer(1, 6))

signature_block(story)
story.append(Spacer(1, 8))
story.append(Paragraph("Method of delivery: Electronic mail only.", small))
story.append(Paragraph(
    "cc (by e-mail): nchapman@kcozlaw.com; file (Newanforbi v. Randstad US, LLC, et al., 26CV199902)",
    small,
))

SimpleDocTemplate(
    DEMAND_PATH,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.15 * inch,
    bottomMargin=1.0 * inch,
    title="Settlement Demand - Randstad US LLC (Aug 28 2026)",
).build(story, onFirstPage=stamp_settlement_page, onLaterPages=stamp_settlement_page)
print(f"Generated: {DEMAND_PATH}")

with open(COVER_PATH, "w", encoding="utf-8") as fh:
    fh.write(COVER_EMAIL)
print(f"Generated: {COVER_PATH}")
print()
print(COVER_EMAIL)
