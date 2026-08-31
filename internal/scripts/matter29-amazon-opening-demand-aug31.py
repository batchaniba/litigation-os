# ==========================================================
# NEWANFORBI v. AMAZON.COM SERVICES, LLC ET AL. (26CV201554)
#
# Opening settlement demand as to Amazon.com Services, LLC only.
# $250,000.00 — matches the operative Aug. 7 CCP §425.115 notice.
# Not yet transmitted. Evid. Code §1152 / FRE 408.
#
# Do not say Amazon settled the identical §290.46 claim. Lerma Dkt. 36
# dismissed Megan's Law; Dkt. 46 settled the surviving Fair Chance claim.
# Do not cc Seyfarth on an Amazon-only demand.
# ==========================================================
import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

SIGNATURE_IMG = SIGNATURE_PATH
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_DIR = os.path.join(REPO_ROOT, "internal", "public", "documents", "matter-29")

DEMAND_PATH = os.path.join(
    OUT_DIR,
    "Opening Settlement Demand - Amazon.com Services LLC (Aug 31 2026).pdf",
)
COVER_PATH = os.path.join(
    OUT_DIR,
    "EMAIL_DRAFT_Opening_Demand_Amazon.com_Services_LLC (Aug 31 2026).txt",
)

DATE = "August 31, 2026"
AMOUNT = "$250,000.00"
AMOUNT_WORDS = "Two Hundred Fifty Thousand U.S. Dollars"

body = ParagraphStyle(
    "body", fontName="Times-Roman", fontSize=12, leading=16.5,
    alignment=TA_JUSTIFY, spaceAfter=8,
)
bullet = ParagraphStyle(
    "bullet", fontName="Times-Roman", fontSize=12, leading=16.5,
    alignment=TA_JUSTIFY, spaceAfter=6, leftIndent=18, bulletIndent=4,
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
    bits = [Paragraph(closing, plain), Spacer(1, 4)]
    if os.path.isfile(SIGNATURE_IMG):
        img = Image(SIGNATURE_IMG, width=2.5 * inch, height=2.5 * inch * SIGNATURE_ASPECT)
        img.hAlign = "LEFT"
        bits.append(img)
    bits.append(Paragraph("Brendan Ngehsi Newanforbi", plain))
    bits.append(Paragraph("Plaintiff, In Pro Per", plain))
    story.append(KeepTogether(bits))


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
        "OPENING SETTLEMENT DEMAND -- NEWANFORBI v. AMAZON.COM SERVICES, LLC",
    )
    canvas.restoreState()


COVER_EMAIL = """To: Andrew P. Frederick <andrew.frederick@morganlewis.com>
Subject: Newanforbi v. Amazon.com Services, LLC et al. — Opening Settlement Demand (Evid. Code § 1152 / FRE 408)

Attach: Opening Settlement Demand - Amazon.com Services LLC (Aug 31 2026).pdf

---

Mr. Frederick:

Attached is my opening demand to settle as to Amazon.com Services, LLC only: $250,000.00, inclusive of all claims against Amazon in this action. Please respond on or before 5:00 p.m. Pacific Time on September 11, 2026.

This communication is for compromise purposes and is protected by California Evidence Code section 1152 and Federal Rule of Evidence 408. Settlement discussions do not extend Amazon's August 31, 2026 date to respond to the Complaint.

Regards,
Brendan Ngehsi Newanforbi
Plaintiff, In Pro Per
(209) 801-4442
bnn.cdl@gmail.com

---
Note to self (do not send this footer):
Draft of Aug. 31, 2026. NOT YET TRANSMITTED.
- Attach the PDF. Do not paste the letter into the email body.
- Amazon-only $250,000. Matches the operative Aug. 7 / e-filed Aug. 6 CCP §425.115 notice. Do not cite the unserved Aug. 4 $25,000 draft.
- Do not cc Jasmine Stanzick or John Drury.
- Before sending, confirm on the Alameda docket whether Amazon has already answered or demurred. If the Aug. 31 date has moved, edit the last sentence of the cover and Sections I and VII of the letter.
- Do not say Amazon settled the identical §290.46 claim.
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
story.append(Paragraph("Andrew P. Frederick, Esq.", plain))
story.append(Paragraph("Morgan, Lewis &amp; Bockius LLP", plain))
story.append(Paragraph("1400 Page Mill Road", plain))
story.append(Paragraph("Palo Alto, CA 94304", plain))
story.append(Paragraph("E-mail: andrew.frederick@morganlewis.com", plain))
story.append(Paragraph("<i>Counsel for Defendant Amazon.com Services, LLC</i>", plain))
story.append(Spacer(1, 12))

story.append(Paragraph(
    "Re:&nbsp;&nbsp;<b>Opening Demand to Settle as to Amazon.com Services, LLC</b><br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Newanforbi v. Amazon.com Services, LLC, et al.</b> — "
    "Superior Court of California, County of Alameda, Case No. 26CV201554<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hon. Jamilah Jefferson, Department 520 (Hayward Hall of Justice)<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pen. Code, &sect; 290.46, subd. (j)(2)(E); Fair Chance Act, "
    "Gov. Code &sect; 12952; FCRA; ICRAA; Cal. Const., art. I, &sect; 1; Bus. &amp; Prof. Code "
    "&sect; 17200; IIED<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Accurate Background screening Y94611404 / search ID 496623722 | "
    f"<b>Demand: {AMOUNT} (Amazon only)</b>",
    body,
))
story.append(Spacer(1, 6))
story.append(Paragraph("Dear Mr. Frederick:", plain))
story.append(Spacer(1, 12))

story.append(Paragraph(
    "This is my opening demand to settle the claims against Amazon.com Services, LLC in the "
    "above-captioned action. It is made as to Amazon alone. A demand that also resolved Accurate "
    "Background LLC would be a different number, and is addressed at the end of this letter.",
    body,
))

story.append(Paragraph("I.&nbsp;&nbsp;WHERE THE CASE STANDS", heading))

story.append(Paragraph(
    "The Complaint was filed July 28, 2026, accepted July 29, 2026, and assigned to the Honorable "
    "Jamilah Jefferson, Department 520. Amazon was personally served through CSC — Lawyers "
    "Incorporating Service on July 31, 2026, by the Sacramento County Sheriff (Rebecca Vang / "
    "Authorized Agent; Levying Officer File No. 2026027206). Accurate Background LLC was personally "
    "served the same day. Notices of the amount of punitive damages sought under Code of Civil "
    "Procedure section 425.115 — $250,000.00 as to Amazon and $100,000.00 as to Accurate "
    "Background — were e-filed and accepted August 6, 2026. Your Notice of Appearance was filed "
    "August 24, 2026. A case management conference is set for January 6, 2027, at 10:00 a.m. "
    "Amazon's time to respond to the Complaint is August 31, 2026. This demand does not extend "
    "that date.",
    body,
))

story.append(Paragraph(
    "I mention the posture for one reason: this is a filed, served, and calendared case, not a "
    "pre-filing inquiry.",
    body,
))

story.append(Paragraph("II.&nbsp;&nbsp;THE DOCUMENTARY RECORD", heading))

story.append(Paragraph(
    "Every material fact below is in Amazon's own hiring system, Amazon's own emails and texts, or "
    "the contemporaneous communications of the consumer reporting agency Amazon retained. Nothing "
    "turns on whose recollection a jury credits.",
    body,
))

for text in [
    "I applied through hiring.amazon.com for Seasonal XL Warehouse Associate at Amazon's "
    "fulfillment center at 44051 Osgood Road, Fremont, California 94539. The posted terms were "
    "$21.50 per hour (the offer letter stated a range of $21.50 to $24.00), approximately 19 hours "
    "per week, with a possible start date of July 28, 2026.",

    "<b>July 3, 2026, 2:09 p.m.</b> Amazon Jobs emailed “Congratulations on Your Amazon Offer!” "
    "The email stated: “This offer is confirmation that you will be hired* as an employee of Amazon "
    "and depends on the successful completion of your background check, drug test, and all pre-hire "
    "activities.” Training was set for July 28–29 and August 4–5, 2026.",

    "<b>July 3, 2026, 2:20 p.m.</b> Amazon confirmed a Pre-Hire Appointment for July 7, 2026, "
    "9:00–9:30 a.m., at the onsite recruiting office at that Fremont facility.",

    "<b>July 4–5, 2026.</b> I completed Form I-9 online. Amazon's Simple Hire checklist later "
    "confirmed Drug Test COMPLETE and I-9 Verification COMPLETE. The only open item was the "
    "background check.",

    "<b>July 7, 2026.</b> I attended the pre-hire appointment. Amazon emailed “Completed Pre-Hire "
    "Appointment” at 9:20 a.m.",

    "<b>July 7, 2026.</b> Accurate Background — Amazon's consumer reporting agency for this "
    "pipeline, communicating as “Amazon Salesforce” — opened screening Y94611404 (search ID "
    "496623722). Accurate identified itself in writing as “a consumer reporting agency” "
    "“requesting background check on behalf of Amazon.” The same day, Accurate emailed an "
    "“Other Information Needed for Screening Request” notice asking me to confirm Social Security "
    "number, prior names, address history, and date of birth as “an urgent matter,” and warning "
    "that failure to respond promptly “will result in delays in processing your screening.”",

    "<b>July 8, 2026.</b> Amazon's own text stated that, at the site I applied to, “background "
    "checks are usually returned 5 days after they are submitted.”",

    "<b>July 12 and July 17, 2026.</b> Amazon emailed that the application was “still in progress” "
    "and then that Amazon was “still waiting for your background check results and sincerely "
    "apologize[d] for the delay,” attributing the delay to “a third-party vendor.”",

    "<b>July 27, 2026, 3:23 p.m.</b> — the day before training was to begin — Amazon's Simple Hire "
    "checklist still read Background Check PENDING, 20 days after the check was opened, against "
    "Amazon's own five-day norm. The same checklist had overwritten the locked July 28–29 / "
    "August 4–5 training shift with: “You do not have a shift selected — Please select a new "
    "shift.”",
]:
    story.append(Paragraph(text, bullet, bulletText="•"))

story.append(Paragraph(
    "No copy of the consumer report, no FCRA summary of rights, no ICRAA summary of rights, no "
    "Government Code section 12952 written notice of a disqualifying conviction, and no formal "
    "adverse-action letter has ever been provided to me. The specific, dated position was vacated "
    "on the eve of its own start date while Amazon held the file in perpetual “Pending.” That is "
    "the adverse action. Amazon already has these records. Accurate Background's report will be "
    "obtained under 15 U.S.C. section 1681g, Civil Code section 1786.10, or discovery. This demand "
    "does not wait on that production.",
    body,
))

story.append(Paragraph("III.&nbsp;&nbsp;THE CLAIMS AND THE LAW", heading))

story.append(Paragraph(
    "The Complaint pleads seven causes of action. The demand is inclusive of all of them as to "
    "Amazon.",
    body,
))

story.append(Paragraph(
    "<b>First.</b> Penal Code section 290.46, subdivision (j)(2)(E), categorically prohibits use of "
    "information disclosed on the Megan's Law website “for purposes relating to … Employment.” "
    "The narrow authorization in subdivision (j)(1) — use “to protect a person at risk” — has no "
    "application to an XL Warehouse Associate assignment, and no other exception exists. Subdivision "
    "(j)(4)(A) makes a prohibited use actionable for “actual damages, and any amount that may be "
    "determined by a jury or a court sitting without a jury, not exceeding three times the amount of "
    "actual damage, and not less than two hundred fifty dollars ($250), and attorney's fees, "
    "exemplary damages, or a civil penalty not exceeding twenty-five thousand dollars ($25,000).” "
    "Amazon is the user. Accurate Background is Amazon's agent for the screen. The mid-screening "
    "identity-verification hold, the fourfold overrun of Amazon's own five-day background-check "
    "norm, and the silent cancellation of the locked training shift are the documented sequence. The "
    "statute does not require Amazon to style the cancellation as a “denial” before the prohibition "
    "attaches.",
    body,
))

story.append(Paragraph(
    "<b>Second.</b> Government Code section 12952 — the Fair Chance Act — required Amazon, before "
    "denying the position in whole or in part because of conviction history, to make an "
    "individualized assessment of whether that history has a direct and adverse relationship with "
    "the specific duties of Seasonal XL Warehouse Associate, considering (i) the nature and gravity "
    "of the offense or conduct, (ii) the time that has passed since the offense or conduct and "
    "completion of the sentence, and (iii) the nature of the job. Gov. Code, &sect; 12952, subd. "
    "(c)(1). Before taking adverse action, Amazon also had to notify me in writing of the "
    "disqualifying conviction or convictions, provide a copy of any conviction-history report used, "
    "and give me an opportunity to respond. <i>Id.</i>, subd. (c)(2). Amazon's Simple Hire process "
    "as I experienced it contains no individualized-assessment step of any kind. The file moved from "
    "“Background Check — Pending” to the silent removal of the confirmed shift. Section 12952 is "
    "enforced through the Fair Employment and Housing Act. The remedies include compensatory "
    "damages, emotional-distress damages, punitive damages where authorized, and attorney's fees. "
    "This is an Amazon-only claim. It does not depend on proving that the Megan's Law website, as "
    "opposed to some other source, was the input to the screen.",
    body,
))

story.append(Paragraph(
    "<b>Third.</b> The Fair Credit Reporting Act. Accurate Background is a consumer reporting "
    "agency. Amazon is a user. Before taking adverse action based in whole or in part on a consumer "
    "report, Amazon had to provide a copy of the report and a written description of my FCRA rights. "
    "15 U.S.C. &sect; 1681b(b)(3). After taking adverse action, Amazon had to provide the notice "
    "specified in section 1681m(a). “Adverse action” includes a denial of employment or any other "
    "decision for employment purposes that adversely affects a prospective employee. 15 U.S.C. "
    "&sect; 1681a(k)(1)(B)(ii). Vacating a locked, dated training shift on the eve of its start, "
    "while leaving the check in perpetual pending status, is an adverse action in substance. Amazon "
    "furnished none of the required notices. Willful violations carry statutory damages of $100 to "
    "$1,000 per violation, or actual damages, plus punitive damages as the court may allow, plus "
    "fees. 15 U.S.C. &sect; 1681n. Negligent violations carry actual damages and fees. 15 U.S.C. "
    "&sect; 1681o.",
    body,
))

story.append(Paragraph(
    "<b>Fourth.</b> The Investigative Consumer Reporting Agencies Act. Amazon caused an "
    "investigative consumer report to be prepared. Civ. Code, &sect; 1786.16. It did not provide "
    "the three-day written notice section 1786.16, subdivision (a)(2), requires. It took adverse "
    "action without providing a copy of the report and a summary of ICRAA rights. Civ. Code, "
    "&sect; 1786.40. Knowing violations carry actual damages or $10,000, whichever is greater; "
    "willful violations add punitive damages, costs, and fees. Civ. Code, &sect; 1786.50.",
    body,
))

story.append(Paragraph(
    "<b>Fifth.</b> California Constitution, article I, section 1. The Legislature's prohibition on "
    "using Megan's Law information for employment is a legislative determination that the privacy "
    "interest in freedom from that use outweighs any employer interest in unrestricted access. "
    "Gathering and using that information to take away a confirmed warehouse assignment is a "
    "serious invasion of that interest.",
    body,
))

story.append(Paragraph(
    "<b>Sixth.</b> Business and Professions Code section 17200. The unlawful prong is independently "
    "satisfied by each of the Penal Code, FCRA, and ICRAA violations. Separately, the unfair prong "
    "reaches Amazon's own offer language. The July 3 email told me that if the background check was "
    "not completed on time I would have to “select a new start date, location or schedule,” that "
    "training spots might no longer be available, and — in Amazon's words — “But don't worry if "
    "this happens!” That language pre-authorized the outcome that followed: the confirmed shift "
    "silently disappeared, the check remained “Pending,” and no document Amazon would have to call "
    "a denial was ever generated. The functional equivalent of a denial, structured to avoid the "
    "notice-and-response framework the FCRA, the ICRAA, and the Fair Chance Act require, is an "
    "unfair business practice. Restitution and injunctive relief lie under section 17203.",
    body,
))

story.append(Paragraph(
    "<b>Seventh.</b> Intentional infliction of emotional distress. Amazon held the check pending "
    "for twenty days — four times its own stated norm — vacated the shift the day before training, "
    "and never issued a notice, a copy of the report, or an opportunity to be heard. That course of "
    "conduct was extreme and outrageous, and it was carried out with actual notice of the governing "
    "statutes.",
    body,
))

story.append(Paragraph(
    "The lost wages on a seasonal 19-hour assignment at $21.50 an hour are not why this demand is "
    "$250,000. The statutes, the Fair Chance Act, emotional-distress damages, fee-shifting, and "
    "punitive exposure are.",
    body,
))

story.append(Paragraph("IV.&nbsp;&nbsp;<i>LERMA</i> — WHAT IT IS AND WHAT IT IS NOT", heading))

story.append(Paragraph(
    "You do not need an introduction to this statutory cluster. You and Morgan, Lewis &amp; "
    "Bockius LLP represented Amazon.com Services, LLC in <i>Lerma v. Amazon.com Services, LLC et "
    "al.</i>, No. 8:22-cv-01727 (C.D. Cal.). You signed Amazon's motion to dismiss the Megan's Law "
    "and UCL claims (Dkt. 24) and Amazon's answer to the surviving Fair Chance Act claim (Dkt. 45). "
    "Accurate Background was the same vendor.",
    body,
))

story.append(Paragraph(
    "I will not misstate that docket. On May 26, 2023, Judge Slaughter dismissed the Megan's Law, "
    "FCRA, and UCL claims without prejudice (Dkt. 36), holding that Accurate's report — subject to "
    "judicial notice — showed the disqualifying 2013 convictions came from ordinary Orange County "
    "criminal records, and that the report's own National Sex Offender Database Search returned "
    "“NO RECORD FOUND.” The Fair Chance Act claim against Amazon was not challenged on those "
    "motions. Amazon answered it. The case settled on that surviving claim on September 21, 2023 "
    "(Dkt. 46). The terms were not filed.",
    body,
))

story.append(Paragraph(
    "<i>Lerma</i> is therefore not a settlement of an identical Penal Code section 290.46(j) claim. "
    "It is two other things, both of which this case uses. First, it is actual notice to Amazon, and "
    "to you, of this vendor relationship and of Government Code section 12952's "
    "individualized-assessment and notice requirements. Amazon paid to resolve the absence of that "
    "assessment in 2023. Amazon's Simple Hire process as I experienced it in July 2026 still had no "
    "such step. Second, it identifies the fact question this case will try on the Megan's Law count: "
    "what Accurate's report on me actually says. If that report's sex-offender-database component "
    "returns a hit, a hold, or a client-criteria flag keyed to registry status, this case is not "
    "<i>Lerma</i>. If it does not, the Fair Chance, FCRA, ICRAA, UCL-unfair, and IIED claims still "
    "remain, because none of those claims requires the Megan's Law website to have been the source.",
    body,
))

story.append(Paragraph(
    "Willfulness and punitive damages under Civil Code section 3294, the FCRA, and the ICRAA rest "
    "on that notice and on Amazon's conduct in this hiring file, not on a claim that Amazon "
    "“settled the identical section 290.46 claim.” The operative Code of Civil Procedure section "
    "425.115 notice as to Amazon is $250,000.00.",
    body,
))

story.append(Paragraph("V.&nbsp;&nbsp;THE DEMAND", heading))

story.append(Paragraph(
    f"<b>Settlement payment: {AMOUNT} ({AMOUNT_WORDS}), Amazon.com Services, LLC only.</b> "
    "Inclusive of all claims against Amazon arising from the July 2026 XL Warehouse Associate "
    "application, conditional offer, background screen, and loss of the July 28, 2026 training "
    "assignment.",
    body,
))

for text in [
    "Payable by check or electronic transfer. Payee details and payment instructions will follow on "
    "acceptance.",

    "Written confirmation that Amazon has issued binding guidance to its California staffing, "
    "recruiting, and background-screening personnel, and to Accurate Background and any other "
    "consumer reporting agency Amazon uses for California hiring, that information disclosed "
    "pursuant to Penal Code section 290.46 shall not be used, directly or indirectly, as a basis "
    "for any employment decision, and that any intended denial based on conviction history will be "
    "preceded by the individualized assessment and notices Government Code section 12952 requires "
    "and by the pre-adverse and adverse-action notices the FCRA and the ICRAA require.",

    "Correction of all internal records of this application so that I am eligible for rehire / "
    "further consideration, and a commitment that any future employer or agency inquiry about this "
    "application will be answered with dates of application and eligible-for-rehire status only.",

    "Confidentiality of the settlement amount only. The fact of settlement and the non-monetary "
    "terms may be disclosed. I will not agree to a non-disparagement clause, and I will not sign a "
    "release broader than the claims arising from this application and this background screen.",

    "The release runs to Amazon.com Services, LLC and its officers, employees, and affiliates only. "
    "It does not extend to Accurate Background LLC. My claims against Accurate Background are "
    "expressly preserved.",
]:
    story.append(Paragraph(text, bullet, bulletText="•"))

story.append(Paragraph("VI.&nbsp;&nbsp;A GLOBAL RESOLUTION", heading))

story.append(Paragraph(
    "I am willing to discuss a global number that would also resolve Accurate Background LLC, and "
    "if Seyfarth Shaw wishes to participate jointly I will provide that number on request. Two "
    "conditions apply. First, a global number will be its own number; it will not be produced by "
    "dividing this demand between the two defendants. Second, nothing about a global discussion "
    "extends either defendant's time to respond to the Complaint.",
    body,
))

story.append(Paragraph("VII.&nbsp;&nbsp;RESPONSE", heading))

story.append(Paragraph(
    "Please respond in writing to bnn.cdl@gmail.com on or before <b>5:00 p.m. Pacific Time on "
    "Friday, September 11, 2026</b>, with an acceptance, a good-faith counter-offer, or a request "
    "to schedule a call. I am available to discuss this matter by telephone. If it would move "
    "things forward, I am also willing to consider an early mediation.",
    body,
))

story.append(Paragraph(
    "That date is my date. It is not a court deadline. Settlement discussions do not extend "
    "Amazon's August 31, 2026 date to respond to the Complaint, which I have not extended and do "
    "not intend to extend.",
    body,
))

story.append(Paragraph("VIII.&nbsp;&nbsp;PROTECTION AND RESERVATION OF RIGHTS", heading))

story.append(Paragraph(
    "This letter is offered in compromise of a disputed claim and is inadmissible to prove "
    "liability under Evidence Code section 1152 and Federal Rule of Evidence 408. Nothing in it "
    "limits my right to introduce the underlying documentary evidence at trial. Nothing in it "
    "waives, releases, or limits any claim, right, or remedy, all of which are expressly reserved. "
    "This letter is not an offer to settle for any amount less than that stated, nor an admission "
    "of fact, law, or comparative fault.",
    body,
))

story.append(Paragraph("I look forward to hearing from you.", body))
story.append(Paragraph("Method of delivery: Electronic mail only.", small))
story.append(Paragraph(
    "cc: file (Newanforbi v. Amazon.com Services, LLC, et al., 26CV201554)",
    small,
))
story.append(Spacer(1, 6))

signature_block(story)

SimpleDocTemplate(
    DEMAND_PATH,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.15 * inch,
    bottomMargin=1.0 * inch,
    title="Opening Settlement Demand - Amazon.com Services LLC (Aug 31 2026)",
    author="Brendan Ngehsi Newanforbi",
).build(story, onFirstPage=stamp_settlement_page, onLaterPages=stamp_settlement_page)
print(f"Generated: {DEMAND_PATH}")

with open(COVER_PATH, "w", encoding="utf-8") as fh:
    fh.write(COVER_EMAIL)
print(f"Generated: {COVER_PATH}")
print()
print(COVER_EMAIL)
