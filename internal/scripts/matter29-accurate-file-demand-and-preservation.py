# ==========================================================
# NEWANFORBI v. AMAZON.COM SERVICES, LLC ET AL. (N.D. Cal. 4:26-cv-09249-ASK)
#
# 1. Consumer file-disclosure demand to Accurate Background, LLC
#    (15 U.S.C. § 1681g; Cal. Civ. Code §§ 1786.10, 1786.22), with a separate
#    Enclosure A identification sheet that goes to Accurate ONLY.
# 2. Preservation letter to counsel for both defendants.
# 3. Two covering-email drafts (email-ending lock applies).
#
#   python3 internal/scripts/matter29-accurate-file-demand-and-preservation.py
#
# Accurate's address: 200 Spectrum Center Drive, Suite 1100, Irvine, CA 92618,
# admitted as its principal place of business in Rangel v. Accurate Background,
# S.D. Cal. No. 3:25-cv-01983, Dkt. 8 (answer to Compl. para. 14). Counsel e-mails
# from Amazon's MTD (Dkt. 19) and Plaintiff's L.R. 3-15 POS (Dkt. 13).
#
# Never write Plaintiff's DOB or SSN into this script or the repo. Enclosure A
# leaves them blank to be completed by hand before mailing.
# Accurate's defenses are not argued here; this is a consumer-rights request
# and a preservation notice, not a brief.
# ==========================================================
import os
import sys

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_DIR = os.path.join(REPO_ROOT, "internal", "public", "documents", "matter-29")

DATE = "September 23, 2026"
DATE_TAG = "Sep 23 2026"

DEMAND_PATH = os.path.join(OUT_DIR, f"Consumer File Demand - Accurate Background - 15 USC 1681g ({DATE_TAG}).pdf")
ENCLOSURE_PATH = os.path.join(OUT_DIR, f"Consumer File Demand - Enclosure A Identification - MAIL TO ACCURATE ONLY ({DATE_TAG}).pdf")
PRESERVATION_PATH = os.path.join(OUT_DIR, f"Preservation Letter - Accurate Background and Amazon ({DATE_TAG}).pdf")
EMAIL_ALL_PATH = os.path.join(OUT_DIR, f"EMAIL_DRAFT_Preservation_Letter_All_Counsel ({DATE_TAG}).txt")
EMAIL_SEYFARTH_PATH = os.path.join(OUT_DIR, f"EMAIL_DRAFT_File_Demand_Copy_Seyfarth ({DATE_TAG}).txt")

SCREENING = "Screening Y94611404 / Search ID 496623722"
CASE_LINE = ("<i>Newanforbi v. Amazon.com Services, LLC, et al.</i>, "
             "N.D. Cal. No. 4:26-cv-09249-ASK")

body = ParagraphStyle("body", fontName="Times-Roman", fontSize=12, leading=16.5,
                      alignment=TA_JUSTIFY, spaceAfter=8)
item = ParagraphStyle("item", parent=body, leftIndent=24, firstLineIndent=-18, spaceAfter=5)
plain = ParagraphStyle("plain", fontName="Times-Roman", fontSize=12, leading=16.5, alignment=TA_LEFT)
bold = ParagraphStyle("bold", parent=plain, fontName="Times-Bold")
heading = ParagraphStyle("heading", parent=bold, spaceBefore=8, spaceAfter=6)
small = ParagraphStyle("small", fontName="Times-Roman", fontSize=10, leading=13, alignment=TA_LEFT)
field = ParagraphStyle("field", parent=plain, leading=26)
re_style = ParagraphStyle("re", parent=plain, leftIndent=36, firstLineIndent=-36, spaceAfter=8)


def letterhead(story):
    story.append(Paragraph("BRENDAN NGEHSI NEWANFORBI", bold))
    story.append(Paragraph("1455 Cat Tail Drive &bull; Stockton, CA 95204", plain))
    story.append(Paragraph("Telephone: (209) 801-4442 &bull; E-mail: bnn.cdl@gmail.com", plain))
    story.append(Spacer(1, 16))


def signature_block(story, closing="Very truly yours,"):
    bits = [Paragraph(closing, plain), Spacer(1, 4)]
    if os.path.isfile(SIGNATURE_PATH):
        img = Image(SIGNATURE_PATH, width=2.5 * inch, height=2.5 * inch * SIGNATURE_ASPECT)
        img.hAlign = "LEFT"
        bits.append(img)
    bits.append(Paragraph("Brendan Ngehsi Newanforbi", plain))
    bits.append(Paragraph("Plaintiff, In Pro Per", plain))
    story.append(KeepTogether(bits))


def footer(title):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8.5)
        canvas.drawCentredString(letter[0] / 2.0, 0.62 * inch, f"Page {canvas.getPageNumber()}")
        canvas.setFont("Times-Bold", 8.5)
        canvas.drawCentredString(letter[0] / 2.0, 0.45 * inch, title)
        canvas.restoreState()
    return draw


def build(path, story, title, footer_title):
    SimpleDocTemplate(
        path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
        topMargin=1.0 * inch, bottomMargin=1.0 * inch, title=title,
        author="Brendan Ngehsi Newanforbi",
    ).build(story, onFirstPage=footer(footer_title), onLaterPages=footer(footer_title))
    print(f"Generated: {path}")


def numbered(story, items):
    for i, text in enumerate(items, 1):
        story.append(Paragraph(f"{i}.&nbsp;&nbsp;{text}", item))


# ----------------------------------------------------------
# 1. FILE DEMAND (Accurate, certified mail; courtesy copy to Seyfarth)
# ----------------------------------------------------------
def file_demand():
    s = []
    letterhead(s)
    s.append(Paragraph(DATE, plain))
    s.append(Spacer(1, 12))
    s.append(Paragraph("VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED", bold))
    s.append(Paragraph("Copy (without Enclosure A) by e-mail to counsel of record", small))
    s.append(Spacer(1, 8))
    for ln in ("Accurate Background, LLC", "Attn: Consumer Disclosure / Compliance",
               "200 Spectrum Center Drive, Suite 1100", "Irvine, CA 92618"):
        s.append(Paragraph(ln, plain))
    s.append(Spacer(1, 12))
    s.append(Paragraph(
        "Re:\u00a0\u00a0\u00a0\u00a0\u00a0<b>Request for Complete File Disclosure</b><br/>"
        "<b>15 U.S.C. &sect;&nbsp;1681g; Cal. Civ. Code &sect;&sect;&nbsp;1786.10, 1786.22</b><br/>"
        "Consumer: Brendan Ngehsi Newanforbi<br/>"
        f"{SCREENING}<br/>"
        "Requested by Amazon (identified as &ldquo;Amazon Salesforce&rdquo;)<br/>"
        f"{CASE_LINE}", re_style))
    s.append(Spacer(1, 4))
    s.append(Paragraph("To Accurate Background, LLC:", plain))
    s.append(Spacer(1, 10))

    s.append(Paragraph(
        "I am the consumer who is the subject of the screening identified above. On July 7, 2026, "
        "Accurate notified me that it is a consumer reporting agency and that it had been asked by "
        "&ldquo;Amazon Salesforce&rdquo; to complete screening Y94611404. The same day, under search "
        "ID 496623722, Accurate asked me to confirm my Social Security number, prior names, address "
        "history, and date of birth. Under 15 U.S.C. &sect; 1681g(a) and California Civil Code "
        "sections 1786.10 and 1786.22, I request disclosure of my complete file.", body))

    s.append(Paragraph(
        "This request covers all information about me that Accurate has recorded and retained, "
        "regardless of how it is stored, as of the date Accurate receives this letter. 15 U.S.C. "
        "&sect;&sect; 1681a(g), 1681g(a)(1). It does not depend on whether Accurate has completed, "
        "finalized, or furnished a &ldquo;consumer report&rdquo; or &ldquo;investigative consumer "
        "report.&rdquo; Accurate&rsquo;s answer in the pending action states that my screening "
        "remains pending. Information gathered for a pending screening is still part of my file, "
        "and this request reaches it.", body))

    s.append(Paragraph("Please disclose:", heading))
    numbered(s, [
        "All information in my file, including information gathered for any search or component "
        "that is pending, on hold, in review, cancelled, or not completed. 15 U.S.C. "
        "&sect;&sect; 1681a(g), 1681g(a)(1).",
        "Each search, product, or component ordered for screening Y94611404, including any "
        "sex-offender-registry search, national sex offender database search, county or state "
        "criminal search, and identity-verification component, with the date each was ordered, "
        "started, completed, placed on hold, or cancelled.",
        "The result of each search or component, including any record-found, no-record-found, "
        "possible-match, name-match, hold, or review result, and the records or data returned.",
        "The sources of the information in my file. 15 U.S.C. &sect; 1681g(a)(2).",
        "Each person or entity, including Amazon, that procured or received a consumer report, or "
        "any status, result, or other information about me, and the date of each. 15 U.S.C. "
        "&sect; 1681g(a)(3).",
        "The status history of the screening and every status, adjudication, or disposition code "
        "applied to my file, with an explanation of each code. See 15 U.S.C. &sect; 1681h(c).",
        "What prompted the July 7, 2026 identity-verification request under search ID 496623722, "
        "what information it was meant to verify, and its result.",
        "The reason the screening remains pending.",
    ])
    s.append(Paragraph(
        "To the extent items 7 and 8 are recorded in my file, they are part of the required "
        "disclosure. If they are not, I ask that Accurate provide them anyway.", body))

    s.append(Paragraph("Identification and delivery", heading))
    s.append(Paragraph(
        "Proper identification is enclosed as Enclosure A: my identifying information, a copy of my "
        "government-issued photo identification, and proof of my current address. 15 U.S.C. "
        "&sect; 1681h(a)(1). Enclosure A is sent to Accurate only and is not included in the copy of "
        "this letter provided to counsel.", body))
    s.append(Paragraph(
        "Please send the disclosure in writing to my address above and, if available, by e-mail to "
        "bnn.cdl@gmail.com. I ask that it be provided within 15 days of Accurate&rsquo;s receipt of "
        "this letter. If Accurate contends that a charge applies under 15 U.S.C. &sect; 1681j, "
        "please tell me the amount in writing before processing so that the request is not delayed. "
        "If Accurate needs anything further to identify me, please tell me promptly and in writing.",
        body))

    s.append(Paragraph("Reservation of rights", heading))
    s.append(Paragraph(
        "I make this request under my statutory rights as a consumer. It is not a discovery request, "
        "and it does not limit discovery in the pending action or any claim, right, or remedy, all of "
        "which are reserved. Because Accurate is represented in that action, a copy of this letter, "
        "without Enclosure A, is being sent to its counsel. A separate letter addresses preservation "
        "of evidence.", body))

    s.append(Spacer(1, 6))
    signature_block(s)
    s.append(Spacer(1, 10))
    s.append(Paragraph("Enclosure A: Consumer identification (to Accurate only)", small))
    s.append(Paragraph(
        "cc (by e-mail, without Enclosure A): Jasmine J. Stanzick, Esq., and John W. Drury, Esq., "
        "Seyfarth Shaw LLP, counsel for Accurate Background, LLC", small))
    build(DEMAND_PATH, s, "Request for Complete File Disclosure - Accurate Background",
          "REQUEST FOR COMPLETE FILE DISCLOSURE -- 15 U.S.C. § 1681g; CAL. CIV. CODE §§ 1786.10, 1786.22")


def enclosure_a():
    s = []
    s.append(Paragraph("ENCLOSURE A &mdash; CONSUMER IDENTIFICATION", heading))
    s.append(Paragraph("15 U.S.C. &sect; 1681h(a)(1); Cal. Civ. Code &sect;&sect; 1786.10, 1786.22", plain))
    s.append(Paragraph(f"{SCREENING}", plain))
    s.append(Paragraph(
        "<b>Mailed to Accurate Background, LLC only. Not e-mailed. Not sent to counsel.</b>", plain))
    s.append(Spacer(1, 16))
    rows = [
        ("Full name", "Brendan Ngehsi Newanforbi"),
        ("Other names or spellings used", "Brendan Ngwa Nforbi; ______________________"),
        ("Current address", "1455 Cat Tail Drive, Stockton, CA 95204"),
        ("Prior addresses (past 2 years)", "____________________________________"),
        ("", "_______________________________________________________________"),
        ("Date of birth", "______________________"),
        ("Social Security number", "______________________"),
        ("Telephone", "(209) 801-4442"),
        ("E-mail", "bnn.cdl@gmail.com"),
    ]
    for label, value in rows:
        s.append(Paragraph(f"<b>{label}{':' if label else ''}</b>&nbsp;&nbsp;{value}", field))
    s.append(Spacer(1, 12))
    s.append(Paragraph("Enclosed:", bold))
    s.append(Paragraph("[&nbsp;&nbsp;]&nbsp;&nbsp;Copy of government-issued photo identification", field))
    s.append(Paragraph("[&nbsp;&nbsp;]&nbsp;&nbsp;Proof of current address (e.g., utility bill or bank statement)", field))
    s.append(Spacer(1, 18))
    s.append(Paragraph(
        "I am the consumer identified above and request disclosure of my complete file.", body))
    s.append(Spacer(1, 24))
    s.append(Paragraph("_____________________________________&nbsp;&nbsp;&nbsp;&nbsp;Date: ________________", plain))
    s.append(Paragraph("Brendan Ngehsi Newanforbi", plain))
    build(ENCLOSURE_PATH, s, "Enclosure A - Consumer Identification",
          "ENCLOSURE A -- CONSUMER IDENTIFICATION -- MAIL TO ACCURATE BACKGROUND ONLY")


# ----------------------------------------------------------
# 2. PRESERVATION LETTER (all counsel, e-mail)
# ----------------------------------------------------------
def preservation():
    s = []
    letterhead(s)
    s.append(Paragraph(DATE, plain))
    s.append(Spacer(1, 12))
    s.append(Paragraph("VIA ELECTRONIC MAIL", bold))
    s.append(Spacer(1, 8))
    for ln in ("Jasmine J. Stanzick, Esq. (jstanzick@seyfarth.com)",
               "John W. Drury, Esq. (jdrury@seyfarth.com)",
               "Seyfarth Shaw LLP",
               "<i>Counsel for Defendant Accurate Background, LLC</i>"):
        s.append(Paragraph(ln, plain))
    s.append(Spacer(1, 8))
    for ln in ("Andrew P. Frederick, Esq. (andrew.frederick@morganlewis.com)",
               "Douglass G. Brown, Esq. (douglass.brown@morganlewis.com)",
               "Morgan, Lewis &amp; Bockius LLP",
               "<i>Counsel for Defendant Amazon.com Services LLC</i>"):
        s.append(Paragraph(ln, plain))
    s.append(Spacer(1, 12))
    s.append(Paragraph(
        "Re:\u00a0\u00a0\u00a0\u00a0\u00a0<b>Preservation of Documents and Electronically Stored Information</b><br/>"
        f"{CASE_LINE}<br/>"
        f"Accurate Background {SCREENING}", re_style))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Counsel:", plain))
    s.append(Spacer(1, 10))

    s.append(Paragraph(
        "This letter confirms each Defendant&rsquo;s obligation to preserve documents, electronically "
        "stored information (ESI), and tangible things relevant to the claims and defenses in this "
        "action. That obligation arose no later than service of the Complaint on July 31, 2026, and "
        "it continues through the end of the case. Failure to preserve ESI may result in measures "
        "under Federal Rule of Civil Procedure 37(e).", body))
    s.append(Paragraph(
        "Unless otherwise stated, the relevant period is July 1, 2026 to the present. Please preserve "
        "ESI in native format with its metadata, including information held by vendors, "
        "subcontractors, and agents under your clients&rsquo; control, such as court researchers, "
        "data providers, text-message and e-mail platforms, and applicant-tracking and onboarding "
        "systems. Please suspend any automatic deletion, overwriting, or retention-schedule purge that "
        "would affect these materials, including backups and system logs.", body))

    s.append(Paragraph("A.&nbsp;&nbsp;Accurate Background, LLC", heading))
    numbered(s, [
        "The complete file and all records for screening Y94611404 and search ID 496623722, "
        "including the order, the package or components ordered, and any change, hold, or "
        "cancellation.",
        "For each search or component, including any sex-offender-registry, national sex offender "
        "database, county or state criminal, and identity-verification component: the request, each "
        "status and status change with timestamps, raw and processed results, possible-match or "
        "name-match data, and the sources queried.",
        "Audit logs, system logs, workflow and queue records, adjudication or disposition codes, and "
        "manual-review or reviewer notes concerning Plaintiff.",
        "Records of every communication, status update, result, or data transmission to Amazon "
        "concerning Plaintiff, including portal, API, integration, and e-mail records.",
        "Communications with Plaintiff, including the July 7, 2026 notices, SMS records for shortcode "
        "45996, e-mails from noreply@accurate.com and infoneeded@accurate.com, and any call records "
        "or recordings relating to the identity-verification request.",
        "Communications with any court, court researcher, or data vendor concerning Plaintiff&rsquo;s "
        "screening, including records bearing on why the screening remains pending.",
        "Any certification Amazon provided under 15 U.S.C. &sect; 1681b(b)(1), and the agreements, "
        "statements of work, and package configurations governing Amazon&rsquo;s California "
        "screenings in effect during July 2026.",
        "Policies, procedures, and system rules in effect during 2026 for the use, suppression, or "
        "reporting of California sex-offender-registry information for employment purposes, and for "
        "placing screenings on hold or in pending status.",
        "Plaintiff&rsquo;s requests for his file, including his request dated "
        f"{DATE} sent by certified mail, and Accurate&rsquo;s responses.",
    ])

    s.append(Paragraph("B.&nbsp;&nbsp;Amazon.com Services LLC", heading))
    numbered(s, [
        "Plaintiff&rsquo;s application, candidate record, and onboarding (Simple Hire) records, "
        "including checklist and status history with timestamps.",
        "Records showing the removal of Plaintiff&rsquo;s July 28&ndash;29 and August 4&ndash;5, 2026 "
        "training shift, including who or what removed it, when, and why, and any system rule or "
        "automation that caused it.",
        "All information Amazon received from Accurate concerning Plaintiff, including statuses, "
        "results, flags, and reports, and records of when it was received and who viewed it.",
        "Internal communications and notes concerning Plaintiff&rsquo;s background check, start date, "
        "shift, or eligibility for hire.",
        "Communications with Plaintiff, including e-mails and SMS messages from shortcodes 31432 and "
        "39816, and any call records.",
        "Records of any individualized assessment, pre-adverse-action notice, adverse-action notice, "
        "or Fair Chance Act process concerning Plaintiff, or of any decision not to use one.",
        "Any certification Amazon provided to Accurate under 15 U.S.C. &sect; 1681b(b)(1), and "
        "Amazon&rsquo;s agreements with Accurate governing its California screenings in effect "
        "during July 2026.",
        "Policies, procedures, and system rules in effect during 2026 governing (a) background checks "
        "that remain pending past a scheduled start date, (b) removal or reassignment of training "
        "shifts, (c) use of criminal-history or registry information in California hiring, and "
        "(d) the Fair Chance Act process.",
    ])

    s.append(Paragraph(
        "Plaintiff is preserving his own relevant materials, including e-mails, text messages, and "
        "screenshots. This letter does not limit discovery, and Plaintiff expects to address ESI and "
        "preservation in the Rule 26(f) conference and the joint case management statement.", body))
    s.append(Paragraph(
        "Please confirm in writing within ten days that a litigation hold covering these categories "
        "is in place. If either Defendant contends that a category is overbroad or unduly "
        "burdensome, please say so now so that we can confer before any information is lost.", body))
    s.append(Spacer(1, 6))
    signature_block(s)
    build(PRESERVATION_PATH, s, "Preservation Letter - Accurate Background and Amazon",
          "PRESERVATION LETTER -- NEWANFORBI v. AMAZON.COM SERVICES, LLC, NO. 4:26-cv-09249-ASK")


# ----------------------------------------------------------
# 3. COVER EMAILS (email-ending lock: two-line close, no phone/email)
# ----------------------------------------------------------
EMAIL_ALL = f"""To: Jasmine J. Stanzick <jstanzick@seyfarth.com>; John W. Drury <jdrury@seyfarth.com>; Andrew P. Frederick <andrew.frederick@morganlewis.com>; Douglass G. Brown <douglass.brown@morganlewis.com>
Subject: Newanforbi v. Amazon.com Services, LLC, et al., No. 4:26-cv-09249-ASK - Preservation Letter

Attach: Preservation Letter - Accurate Background and Amazon ({DATE_TAG}).pdf

---

Counsel:

Attached is a letter concerning preservation of documents and electronically stored information in this action. Please confirm within ten days that a litigation hold covering the listed categories is in place.

Thank you,

Brendan Ngwa Nforbi
Plaintiff, In Propria Persona

---
Note to self (do not send this footer):
- Attach the PDF. Do not paste the letter into the email body. No links.
- Log the send in Matter 29 events.
"""

EMAIL_SEYFARTH = f"""To: Jasmine J. Stanzick <jstanzick@seyfarth.com>; John W. Drury <jdrury@seyfarth.com>
Subject: Newanforbi v. Amazon.com Services, LLC, et al., No. 4:26-cv-09249-ASK - Copy of Consumer File Disclosure Request

Attach: Consumer File Demand - Accurate Background - 15 USC 1681g ({DATE_TAG}).pdf

---

Counsel:

Attached for your records is a copy of my request to Accurate Background, LLC for disclosure of my complete file under 15 U.S.C. section 1681g and California Civil Code sections 1786.10 and 1786.22. The original is being sent to Accurate by certified mail with my identification enclosure, which is not included in this copy.

Thank you,

Brendan Ngwa Nforbi
Plaintiff, In Propria Persona

---
Note to self (do not send this footer):
- Do NOT attach Enclosure A. It carries DOB/SSN and goes to Accurate only, by mail.
- Before mailing: complete Enclosure A by hand (DOB, SSN, prior addresses), sign and date it,
  and enclose a copy of photo ID and proof of address.
- Mail the letter + Enclosure A certified mail, return receipt requested, to
  Accurate Background, LLC, Attn: Consumer Disclosure / Compliance,
  200 Spectrum Center Drive, Suite 1100, Irvine, CA 92618.
- Keep the certified-mail receipt and green card; log tracking number and delivery date in Matter 29.
- Send this copy to Seyfarth only. Amazon's counsel gets the preservation letter, not this.
"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    file_demand()
    enclosure_a()
    preservation()
    for path, text in ((EMAIL_ALL_PATH, EMAIL_ALL), (EMAIL_SEYFARTH_PATH, EMAIL_SEYFARTH)):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Generated: {path}")


if __name__ == "__main__":
    main()
