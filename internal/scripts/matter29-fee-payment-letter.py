# ==========================================================
# NEWANFORBI v. AMAZON.COM SERVICES, LLC, ET AL. (26CV201554)
# Cover letter to the Court Clerk transmitting payment in full of
# the $435.00 first-paper filing fee, to moot the pending Request to
# Waive Court Fees and the August 18, 2026 fee-waiver hearing.
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
OUT_PATH = os.path.join(
    REPO_ROOT,
    "internal", "public", "documents", "matter-29",
    "Letter to Court Clerk - Filing Fee Paid in Full, Fee Waiver Hearing Moot (Aug 3 2026).pdf",
)

DATE = "August 3, 2026"

body = ParagraphStyle(
    "body", fontName="Times-Roman", fontSize=12, leading=16.5,
    alignment=TA_JUSTIFY, spaceAfter=12,
)
plain = ParagraphStyle(
    "plain", fontName="Times-Roman", fontSize=12, leading=16.5, alignment=TA_LEFT,
)
bold = ParagraphStyle(
    "bold", fontName="Times-Bold", fontSize=12, leading=16.5, alignment=TA_LEFT,
)
center_bold = ParagraphStyle(
    "center_bold", fontName="Times-Bold", fontSize=12, leading=16.5, alignment=1,
)

story = []

story.append(Paragraph("BRENDAN NGEHSI NEWANFORBI", bold))
story.append(Paragraph("1455 Cat Tail Drive", plain))
story.append(Paragraph("Stockton, CA 95204", plain))
story.append(Paragraph("Telephone: (209) 801-4442", plain))
story.append(Paragraph("E-mail: bnn.cdl@gmail.com", plain))
story.append(Paragraph("Plaintiff In Pro Per", plain))
story.append(Spacer(1, 28))

story.append(Paragraph(DATE, plain))
story.append(Spacer(1, 18))

story.append(Paragraph("Clerk of the Court", plain))
story.append(Paragraph("Superior Court of California, County of Alameda", plain))
story.append(Paragraph("Hayward Hall of Justice, Department FHO", plain))
story.append(Paragraph("24405 Amador Street", plain))
story.append(Paragraph("Hayward, CA 94544", plain))
story.append(Spacer(1, 18))

story.append(Paragraph(
    "Re:&nbsp;&nbsp;<b>Newanforbi v. Amazon.com Services, LLC, et al.</b> — Case No. 26CV201554<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Payment in Full of First-Paper Filing Fee ($435.00) — "
    "Request to Waive Court Fees Withdrawn as Moot<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hearing currently set: August 18, 2026, 11:30 a.m., Department FHO",
    body,
))
story.append(Spacer(1, 6))

story.append(Paragraph("Dear Clerk of the Court:", plain))
story.append(Spacer(1, 12))

story.append(Paragraph(
    "I am the Plaintiff in the above-referenced action, appearing in pro per. I write to enclose "
    "payment in full of the standard first-paper filing fee for this unlimited civil action — "
    "$435.00 (Gov. Code, &sect; 70611(a)) — by money order, and to respectfully request that the "
    "Court treat my pending Request to Waive Court Fees (Judicial Council Form FW-001, filed "
    "July 28, 2026) as withdrawn and moot in light of this payment.",
    body,
))

story.append(Paragraph(
    "By way of background, the Court's Order on Court Fee Waiver (Form FW-003), signed July 31, "
    "2026 and served August 3, 2026, found that it needed additional information before ruling on "
    "my fee waiver request and set a hearing for August 18, 2026, at 11:30 a.m. in Department FHO "
    "to address that question. Rather than take the Court's time at a hearing on my eligibility for "
    "a waiver, I am instead paying the fee in full. Because the underlying fee is now paid, there is "
    "no longer a request pending for the Court to decide, and I respectfully ask that the August 18, "
    "2026 hearing be taken off calendar as unnecessary.",
    body,
))

story.append(Paragraph(
    "Enclosed please find a money order in the amount of $435.00, made payable to the Clerk of the "
    "Superior Court of California, County of Alameda, referencing Case No. 26CV201554. I respectfully "
    "request that the Court apply this payment to the filing fee due in this action and update the "
    "docket accordingly.",
    body,
))

story.append(Paragraph(
    "If, for any reason, this payment is not received, processed, or reflected in the Court's records "
    "before August 18, 2026, I will appear as scheduled at the hearing to avoid any risk that my "
    "Request to Waive Court Fees is denied for nonappearance. I would appreciate written or electronic "
    "confirmation that this payment has been received and applied, and that the hearing has been taken "
    "off calendar, at the Court's earliest convenience.",
    body,
))

story.append(Paragraph(
    "Thank you for your attention to this matter.",
    body,
))
story.append(Spacer(1, 12))

story.append(Paragraph("Respectfully submitted,", plain))
story.append(Spacer(1, 6))
if os.path.isfile(SIGNATURE_IMG):
    img = Image(SIGNATURE_IMG, width=1.9 * inch, height=1.9 * inch * SIGNATURE_ASPECT)
    img.hAlign = "LEFT"
    story.append(img)
story.append(Paragraph("Brendan Ngehsi Newanforbi", plain))
story.append(Paragraph("Plaintiff, In Pro Per", plain))
story.append(Spacer(1, 18))

story.append(Paragraph("Enclosure: Money Order No. ___________________, $435.00", plain))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "cc: File (Newanforbi v. Amazon.com Services, LLC, et al., 26CV201554)",
    plain,
))

doc = SimpleDocTemplate(
    OUT_PATH,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=1.0 * inch,
    bottomMargin=1.0 * inch,
    title="Letter to Court Clerk - Filing Fee Paid in Full (Aug 3 2026)",
)
doc.build(story)
print(f"Generated: {OUT_PATH}")
