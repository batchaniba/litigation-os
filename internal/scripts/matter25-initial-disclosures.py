from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import (
    PleadingPaper,
    CONTENT_LEFT,
    CONTENT_RIGHT,
)
from pdf_packet import assemble
from proof_of_service import DISTRICT_EDCAL, ProofOfServiceFields, build_proof_of_service
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH


ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal" / "public" / "documents" / "matter-25"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "Plaintiff's Initial Rule 26(a)(1) Disclosures (Oct 9 2026).pdf"
BODY = OUT_DIR / ".matter25-initial-disclosures-body.pdf"
POS = OUT_DIR / ".matter25-initial-disclosures-pos.pdf"
SIGNATURE = Path(SIGNATURE_PATH)

CASE = "2:26-cv-02881-DAD-SCR"
FOOTER = f"PLAINTIFF'S INITIAL RULE 26(a)(1) DISCLOSURES - {CASE}"


def para(doc, text, bold=False, indent=0, first_indent=36):
    doc.write_wrapped(text, bold=bold, indent=indent, first_indent=first_indent)
    doc.blank_line()


def heading(doc, text):
    doc.ensure_space(4)
    doc.write_line(text, bold=True, center=True)
    doc.blank_line()


def numbered(doc, number, text):
    doc.ensure_space(3)
    doc.write_wrapped(f"{number}. {text}", indent=18, first_indent=-18)
    doc.blank_line()


def bullet(doc, text):
    doc.ensure_space(3)
    doc.write_wrapped(f"- {text}", indent=24, first_indent=-12)
    doc.blank_line()


def draw_caption(doc):
    y = doc._line_y(doc.current_line)
    left = CONTENT_LEFT - 7.2
    split = left + 300
    bottom = y - 147
    c = doc.c
    c.setLineWidth(0.75)
    c.rect(left, bottom, 300, 161, stroke=1, fill=0)

    left_rows = [
        ("BRENDAN NGEHSI NEWANFORBI,", 0, True, "left"),
        ("Plaintiff,", 34, False, "center"),
        ("v.", 65, False, "v"),
        ("FEDERAL EXPRESS CORPORATION,", 96, True, "left"),
        ("and DOES 1 through 10, inclusive,", 111, True, "left"),
        ("Defendants.", 142, False, "center"),
    ]
    for text, offset, bold, alignment in left_rows:
        font = "Times-Bold" if bold else "Times-Roman"
        size = 12
        while c.stringWidth(text, font, size) > 276:
            size -= 0.25
        c.setFont(font, size)
        if alignment == "center":
            c.drawCentredString(left + 150, y - offset, text)
        else:
            c.drawString(left + (36 if alignment == "v" else 12), y - offset, text)

    right_rows = [
        (f"Case No. {CASE}", False),
        ("", False),
        ("PLAINTIFF'S INITIAL", True),
        ("RULE 26(a)(1) DISCLOSURES", True),
        ("", False),
        ("Complaint Filed: July 15, 2026", False),
        ("Trial Date: Not Set", False),
    ]
    for i, (text, bold) in enumerate(right_rows):
        font = "Times-Bold" if bold else "Times-Roman"
        size = 10
        while text and c.stringWidth(text, font, size) > CONTENT_RIGHT - split - 17:
            size -= 0.25
        c.setFont(font, size)
        c.drawString(split + 12, y - i * 15, text)
    doc.current_line += 8


def signature_block(doc, include_title=True):
    doc.ensure_space(8)
    doc.write_line("Dated: October 9, 2026")
    doc.write_respectfully_submitted()
    w, h = SIGNATURE_NATIVE_PX
    line = "____________________________________"
    doc.draw_signature_image(
        str(SIGNATURE), w, h, line,
        width=170, right_margin_offset=20, x_offset=0,
        height_scale=1.05, above_lines=2,
    )
    doc.write_line(line, right=True, right_margin_offset=20)
    doc.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    if include_title:
        doc.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=20)


doc = PleadingPaper(str(BODY), doc_title_footer=FOOTER)

# Compact portfolio attorney block.
for i, text in enumerate([
    "BRENDAN NGEHSI NEWANFORBI",
    "Plaintiff, In Propria Persona",
    "1455 Cat Tail Drive",
    "Stockton, CA 95204",
    "Telephone: (209) 801-4442",
    "Email: bnn.cdl@gmail.com",
]):
    doc.c.setFont("Times-Bold" if i == 0 else "Times-Roman", 12)
    doc.c.drawString(CONTENT_LEFT, doc._line_y(doc.current_line) - i * 13, text)
doc.current_line += 4
doc.blank_line()
doc.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
doc.write_line("EASTERN DISTRICT OF CALIFORNIA", bold=True, center=True)
doc.blank_line()
draw_caption(doc)
doc.blank_line()

para(
    doc,
    "Plaintiff Brendan Ngehsi Newanforbi provides the following initial disclosures under "
    "Federal Rule of Civil Procedure 26(a)(1). These disclosures are based on information "
    "reasonably available at this stage and will be corrected or supplemented as required by "
    "Rule 26(e).",
)

heading(doc, "I. INDIVIDUALS LIKELY TO HAVE DISCOVERABLE INFORMATION")

numbered(
    doc, "1",
    "Brendan Ngehsi Newanforbi, 1455 Cat Tail Drive, Stockton, California 95204; "
    "telephone (209) 801-4442. Plaintiff has knowledge concerning his application, prior "
    "employment with FedEx-related operations, the conditional hiring process, the background "
    "screening and notices he received, the final adverse action, his qualifications, mitigation "
    "efforts, emotional distress, and damages.",
)
numbered(
    doc, "2",
    "Laurie Rosehill, Manager Compliance, Federal Express Corporation; current contact "
    "information through Defendant's counsel. FedEx identifies Ms. Rosehill as having knowledge "
    "of communication processes between First Advantage, FedEx, and job applicants. Plaintiff "
    "may also use her testimony concerning the transmission, receipt, review, and use of the "
    "background report and adverse-action communications.",
)
numbered(
    doc, "3",
    "Sharon Tokarczyk, Compliance and Regulatory Support Representative, Federal Express "
    "Corporation; current contact information through Defendant's counsel. FedEx identifies Ms. "
    "Tokarczyk as having knowledge of Defendant's hiring practices. Plaintiff may also use her "
    "testimony concerning screening criteria, adjudication practices, application review, and the "
    "basis for the challenged hiring decision.",
)
numbered(
    doc, "4",
    "The FedEx recruiter, hiring manager, human-resources personnel, compliance personnel, and "
    "final decisionmaker who handled or reviewed Plaintiff's 2025 application, conditional offer, "
    "background report, eligibility determination, or adverse action. Their identities and contact "
    "information are presently controlled by Defendant and have been requested in discovery. "
    "Plaintiff will supplement after they are identified.",
)
numbered(
    doc, "5",
    "The First Advantage custodian and personnel who prepared, transmitted, administered, or "
    "maintained Plaintiff's background-screening report and the related pre-adverse and final "
    "adverse-action notices. Their individual identities and current contact information are not "
    "presently known to Plaintiff and will be supplemented after discovery.",
)
numbered(
    doc, "6",
    "Custodians or representatives of Plaintiff's employers and prospective employers during the "
    "claimed loss period, solely concerning earnings, job searches, employment obtained, and "
    "mitigation. Plaintiff will identify specific custodians or witnesses if he may use their "
    "testimony beyond authenticating employment records.",
)

heading(doc, "II. DOCUMENTS, ESI, AND TANGIBLE THINGS")

para(
    doc,
    "The following categories are located in Plaintiff's email account, electronic files, and "
    "personal records in Stockton, California, unless otherwise stated. Plaintiff will make "
    "nonprivileged responsive materials available for inspection and copying or produce them in "
    "electronic form. Identification of a category does not represent that every described item is "
    "presently in Plaintiff's possession.",
)

for text in [
    "Plaintiff's FedEx application materials and communications concerning the 2025 hiring process, conditional offer, onboarding, and employment eligibility.",
    "The March 10, 2025 First Advantage/FedEx pre-adverse-action notification and related portal or email communications available to Plaintiff.",
    "The March 19, 2025 First Advantage/FedEx final adverse-action notification and related portal or email communications available to Plaintiff.",
    "Documents and communications concerning the First Advantage background report, Plaintiff's request for or attempted access to that report, and the expired report link. The complete report and associated audit data are believed to be in Defendant's or First Advantage's possession.",
    "Records concerning Plaintiff's prior employment or onboarding with FedEx or affiliated operations, to the extent available to Plaintiff; additional records are believed to be in Defendant's possession.",
    "Employment, earnings, tax, job-search, application, conditional-offer, and mitigation records that Plaintiff may use to establish economic loss or mitigation.",
    "Documents concerning Plaintiff's qualifications and employment history relevant to the position at issue.",
    "Nonprivileged contemporaneous communications and records concerning the effects of the challenged decision, including emotional distress and financial impact, if used to support damages.",
    "The pleadings, disclosures, discovery requests and responses, productions, deposition transcripts, court orders, and other nonprivileged litigation materials in this action that Plaintiff may use to support his claims.",
]:
    bullet(doc, text)

heading(doc, "III. COMPUTATION OF DAMAGES")

para(
    doc,
    "Plaintiff's present computation is preliminary. California Penal Code section "
    "290.46(j)(4)(A) does not provide a $25,000 minimum; the $25,000 figure is a cap on the "
    "alternative civil penalty. The record reflects compensation beginning at $20.25 per hour for "
    "up to 20 hours per week. Defendant controls additional material inputs, including the "
    "anticipated start date, position classification, benefits, and complete hiring records. "
    "Plaintiff requested those facts in written discovery served October 6, 2026 and will "
    "supplement under Rule 26(e) after receiving them and completing his mitigation compilation.",
)

numbered(
    doc, "1",
    "Accrued lost wages: $20.25 per hour x 20 hours per week = $405 per week. From the March "
    "19, 2025 final adverse action through October 9, 2026 (569 days, or approximately 81.2857 "
    "weeks), gross accrued wage loss is approximately $32,920.71, less interim earnings and "
    "other amounts properly attributable to mitigation. The amount continues to accrue at $405 "
    "per week, subject to proof, mitigation, and the appropriate legal cutoff.",
)
numbered(
    doc, "2",
    "Front pay: using a provisional two-year period, 104 weeks x $405 per week = $42,120, less "
    "interim earnings and other amounts properly attributable to mitigation. Plaintiff will "
    "supplement this period and calculation as the case schedule, discovery, and mitigation record "
    "develop.",
)
numbered(
    doc, "3",
    "Lost employment benefits: the value of employer-provided benefits Plaintiff would have "
    "received during the compensable period, less corresponding benefits obtained through "
    "mitigation. The plan terms and employer contribution data are presently controlled by "
    "Defendant and will be incorporated after production.",
)
numbered(
    doc, "4",
    "Statutory remedy under California Penal Code section 290.46(j)(4)(A): actual damages; an "
    "additional amount determined by the trier of fact, not exceeding three times actual damages "
    "and not less than $250; attorney's fees; exemplary damages; or, in the alternative, a civil "
    "penalty not exceeding $25,000. Attorney's fees are not claimed for Plaintiff's own time.",
)
numbered(
    doc, "5",
    "Emotional-distress and other noneconomic damages: Plaintiff presently estimates $100,000, "
    "subject to supplementation based on discovery and the nature, duration, and effects of the "
    "distress established through testimony and other admissible evidence. These damages are not "
    "susceptible to a precise mathematical calculation.",
)
numbered(
    doc, "6",
    "Punitive damages: an amount sufficient to punish and deter under California Civil Code "
    "section 3294, to be determined by the trier of fact based on the evidence of authorization, "
    "ratification, malice, oppression, and Defendant's financial condition. Plaintiff will provide "
    "a more specific computation if and when the necessary financial and decisionmaking evidence "
    "is obtained.",
)
numbered(
    doc, "7",
    "Recoverable litigation costs, pre- and post-judgment interest, equitable relief, restitution, "
    "and any other relief authorized by the operative pleadings and governing law, in amounts to "
    "be updated as incurred or determined.",
)

para(
    doc,
    "The presently quantifiable damages are approximately $175,040.71 before "
    "mitigation, consisting of $32,920.71 in accrued gross wage loss, $42,120 in provisional front "
    "pay, and $100,000 in noneconomic damages. Accrued wage loss continues at $405 per week. "
    "The alternative civil penalty under section 290.46(j)(4)(A) is not included as an additive "
    "amount in this total. Benefits, statutory enhancements, exemplary or punitive damages, "
    "recoverable costs, interest, restitution, and equitable relief remain additional or subject to "
    "later computation as permitted by law. This is a Rule 26 computation, not a settlement "
    "demand or a waiver of any remedy.",
)

heading(doc, "IV. INSURANCE AGREEMENTS")
para(
    doc,
    "Plaintiff is not aware of and does not possess or control any insurance agreement under "
    "which an insurance business may be liable to satisfy all or part of a possible judgment "
    "against Plaintiff in this action or to indemnify or reimburse payments made to satisfy such "
    "a judgment.",
)

signature_block(doc)
doc.save()
fields = ProofOfServiceFields(
    plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
    plaintiff_role="Plaintiff",
    defendant_lines=["FEDERAL EXPRESS CORPORATION; and", "DOES 1 through 10, inclusive"],
    defendant_role="Defendants",
    case_number=CASE,
    district_line=DISTRICT_EDCAL,
    title="PROOF OF SERVICE",
    service_date="October 9, 2026",
    document_title="Plaintiff's Initial Rule 26(a)(1) Disclosures",
    recipients=[
        "Allison A. Kray, Esq. - allison.kray@fedex.com",
        "Gabriella Bow - gabriella.bow@fedex.com",
        "Michele Wilson - michele.wilson@fedex.com",
    ],
    server_name="Brendan Ngehsi Newanforbi",
    stamp_signature=True,
    by_email=True,
)
build_proof_of_service(POS, fields)
assemble([BODY, POS], OUT)
BODY.unlink(missing_ok=True)
POS.unlink(missing_ok=True)
print(OUT)
