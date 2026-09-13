# ==========================================================
# NEWANFORBI v. RANDSTAD US, LLC, ET AL. (26CV199902, Alameda Sup. Ct.)
#
# Final early global settlement demand — $40,000.00.
# September 14 (RK) and September 15 (Randstad) stay put.
# Do not extend either clock. Do not hold CIV-100s past the
# file-if-silent mornings. Offer may still be accepted through
# 5:00 p.m. Pacific, September 18, 2026, including after a filing.
# Evid. Code § 1152 / FRE 408.
# ==========================================================
import os
import sys

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_DIR = os.path.join(REPO_ROOT, "internal", "docs", "matter-27-eval")

DEMAND_PATH = os.path.join(
    OUT_DIR,
    "Final Early Global Settlement Demand (Sep 12 2026).pdf",
)
COVER_PATH = os.path.join(
    OUT_DIR,
    "Cover Email - Final Early Global Settlement Demand (Sep 12 2026).txt",
)

DATE = "September 12, 2026"
AMOUNT = "$40,000.00"

body = ParagraphStyle(
    "body",
    fontName="Times-Roman",
    fontSize=11,
    leading=14.5,
    alignment=TA_JUSTIFY,
    spaceAfter=9,
)
plain = ParagraphStyle(
    "plain",
    fontName="Times-Roman",
    fontSize=11,
    leading=14.5,
    alignment=TA_LEFT,
)
bold = ParagraphStyle(
    "bold",
    fontName="Times-Bold",
    fontSize=11,
    leading=14.5,
    alignment=TA_LEFT,
)
center_bold = ParagraphStyle(
    "center_bold",
    fontName="Times-Bold",
    fontSize=12,
    leading=15,
    alignment=TA_CENTER,
    spaceAfter=4,
)
center = ParagraphStyle(
    "center",
    fontName="Times-Roman",
    fontSize=11,
    leading=14.5,
    alignment=TA_CENTER,
    spaceAfter=8,
)
heading = ParagraphStyle(
    "heading",
    fontName="Times-Bold",
    fontSize=11,
    leading=14.5,
    alignment=TA_LEFT,
    spaceBefore=8,
    spaceAfter=6,
)
term = ParagraphStyle(
    "term",
    fontName="Times-Roman",
    fontSize=11,
    leading=14.5,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leftIndent=12,
)
small = ParagraphStyle(
    "small",
    fontName="Times-Roman",
    fontSize=9,
    leading=12,
    alignment=TA_LEFT,
)


def stamp_settlement_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Bold", 7.5)
    canvas.drawCentredString(
        letter[0] / 2.0,
        letter[1] - 0.42 * inch,
        "CONFIDENTIAL — FOR SETTLEMENT PURPOSES ONLY — CAL. EVID. CODE § 1152 / FED. R. EVID. 408",
    )
    canvas.setFont("Times-Roman", 8)
    canvas.drawCentredString(
        letter[0] / 2.0,
        0.48 * inch,
        f"Newanforbi v. Randstad US, LLC et al.  |  Settlement Communication  |  Page {canvas.getPageNumber()} of 2",
    )
    canvas.restoreState()


COVER_EMAIL = """To: Chad Williams <CWilliams@kcozlaw.com>; Melinda Garcia <mgarcia@garciagurney.com>; Nathan Chapman <nchapman@kcozlaw.com>; Tod Gurney <tgurney@garciagurney.com>
Cc: Karen Tai <ktai@garciagurney.com>; Pol Minguet <pminguet@garciagurney.com>; Shinae Kim <skim@garciagurney.com>
Subject: $40K Global — Newanforbi v. Randstad, et al. — 26CV199902 (Evid. Code § 1152 / FRE 408)

Attach: Final Early Global Settlement Demand (Sep 12 2026).pdf

---

Counsel:

Attached is a final early global settlement demand in the above-referenced matter: $40,000.00 to resolve all claims against Randstad US, LLC, The RK Logistics Group, Inc., and all Doe defendants.

Key terms:

• $40,000.00 global, paid by wire within seven (7) business days after written joint acceptance.
• The RK Logistics Group, Inc.'s response date remains September 14, 2026. Randstad US, LLC's response date remains September 15, 2026. This demand does not extend either date.
• CIV-100s file if silent on September 15 (RK) and September 16 (Randstad). Settlement talks do not stay default.
• The demand remains open through 5:00 p.m. Pacific Time on September 18, 2026, including after a response is filed.
• Acceptance must be written, unconditional, and on behalf of both named defendants.

Please confirm receipt. The full terms are in the attached letter.

Regards,
Brendan Ngehsi Newanforbi
Plaintiff, In Pro Per
(209) 801-4442
bnn.cdl@gmail.com
"""


story = []
story.append(Paragraph(DATE, plain))
story.append(Spacer(1, 10))
story.append(Paragraph("VIA EMAIL", bold))
story.append(Spacer(1, 8))
story.append(Paragraph("Chadwick L. Williams, Esq.", plain))
story.append(Paragraph("Nathan D. Chapman, Esq.", plain))
story.append(Paragraph("Kabat Chapman &amp; Ozmer LLP", plain))
story.append(Paragraph("cwilliams@kcozlaw.com &nbsp;&nbsp; nchapman@kcozlaw.com", plain))
story.append(Paragraph("<i>Counsel for Randstad US, LLC</i>", plain))
story.append(Spacer(1, 8))
story.append(Paragraph("Melinda Garcia, Esq.", plain))
story.append(Paragraph("Tod Gurney, Esq.", plain))
story.append(Paragraph("Garcia &amp; Gurney, ALC", plain))
story.append(Paragraph("mgarcia@garciagurney.com &nbsp;&nbsp; tgurney@garciagurney.com", plain))
story.append(Paragraph("<i>Counsel for The RK Logistics Group, Inc.</i>", plain))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Re:&nbsp;&nbsp;<b>Final Early Global Settlement Demand</b><br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Newanforbi v. Randstad US, LLC et al.</b><br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Alameda County Superior Court, Case No. 26CV199902<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hon. Karin Schwartz, Department 20",
    body,
))
story.append(Paragraph("Counsel:", plain))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "I am writing to make a final early global settlement demand resolving all claims in this action "
    "against Randstad US, LLC, The RK Logistics Group, Inc., and all Doe defendants. The complaint "
    "alleges prohibited employment use of information disclosed under California's "
    "sex-offender-registration statute in violation of Penal Code section 290.46(j)(2)(E), together "
    "with related statutory and common-law claims.",
    body,
))

story.append(Paragraph("FINAL GLOBAL RESOLUTION", heading))
story.append(Paragraph(AMOUNT, center_bold))
story.append(Paragraph(
    "All claims against Randstad US, LLC, The RK Logistics Group, Inc., and Does 1–20",
    center,
))

story.append(Paragraph(
    "THE STATUTORY AND EVIDENTIARY RECORD SUPPORTS EARLY EVALUATION",
    heading,
))
story.append(Paragraph(
    "Penal Code section 290.46(j)(2)(E) prohibits the use of information disclosed under "
    "section 290.46 for employment purposes unless a statutory exception applies. The complaint "
    "alleges that defendants used such information in the employment decision at issue and pleads "
    "related claims arising from the same conduct.",
    body,
))
story.append(Paragraph(
    "Early discovery already completed and in plaintiff's possession materially supports the pleaded "
    "claims. Without disclosing that material here, the present record warrants evaluation now. "
    "Acceptance would avoid the expense of briefing a demurrer or other pleading motion and allow "
    "both defendants to resolve the action without allocating fault or engaging in finger-pointing "
    "between them.",
    body,
))
story.append(Paragraph(
    "Randstad requested additional time on September 9. RK Logistics requested an extension through "
    "September 30 on September 10, and Mr. Gurney renewed that request. I declined those requests. "
    "The September 14 and September 15 response dates are unchanged. This demand does not extend "
    "either deadline.",
    body,
))

story.append(Paragraph(
    "TERMS OF THE FINAL EARLY GLOBAL SETTLEMENT DEMAND",
    heading,
))
story.append(Paragraph("Terms continue on page 2.", small))

story.append(Paragraph(
    f"<b>1. Global amount.</b> Defendants shall pay {AMOUNT} to resolve in full all of my claims "
    "against Randstad US, LLC, The RK Logistics Group, Inc., and all Doe defendants arising from "
    "the facts alleged in this action.",
    term,
))
story.append(Paragraph(
    "<b>2. Payment.</b> The settlement amount shall be paid within seven (7) business days after "
    "defendants' written acceptance, by wire transfer to plaintiff's bank account. Wire instructions "
    "will follow upon acceptance. The wire shall be made payable to Brendan Ngwa Nforbi.",
    term,
))
story.append(Paragraph(
    "<b>3. Dismissal and release.</b> Upon clearance of the settlement funds, I will dismiss this "
    "action with prejudice as to both named defendants and all Doe defendants. The parties will "
    "exchange a mutual general release of all claims arising from the facts alleged in this action. "
    "Each side will bear its own attorney's fees and costs.",
    term,
))
story.append(Paragraph(
    "<b>4. Response dates unchanged; no stay of default.</b> The RK Logistics Group, Inc.'s time "
    "to demur or otherwise respond remains September 14, 2026. Randstad US, LLC's time remains "
    "September 15, 2026. This demand does not extend either date. Settlement discussions do not "
    "extend any deadline. I have prepared CIV-100 Requests for Entry of Default as to RK Logistics "
    "(September 15) and Randstad (September 16). Those requests will be filed if eCourt that morning "
    "shows no answer, demurrer, CIV-141, or stipulation. The demand may still be accepted through "
    "the expiration in paragraph 6, including after a response is filed.",
    term,
))
story.append(Paragraph(
    "<b>5. Joint written acceptance.</b> Because this is a global resolution, acceptance must be "
    "written, unconditional, and communicated on behalf of both Randstad US, LLC and The RK "
    "Logistics Group, Inc.",
    term,
))
story.append(Paragraph(
    "<b>6. Expiration.</b> This demand expires automatically at 5:00 p.m. Pacific Time on Friday, "
    "September 18, 2026. If it has not been accepted in writing by then, the demand is withdrawn "
    "and I will proceed with litigation and, if the docket is empty, with the prepared default "
    "requests.",
    term,
))

story.append(Paragraph("OPPORTUNITY TO RESOLVE THE MATTER", heading))
story.append(Paragraph(
    "This demand gives both companies complete resolution of the action. It avoids the expense and "
    "uncertainty of further motion practice, discovery, and trial. Please direct a joint written "
    "acceptance to me before the deadline. If counsel would like to circulate a short-form agreement "
    "consistent with these terms, I will review it promptly.",
    body,
))

story.append(Paragraph("Respectfully,", plain))
story.append(Spacer(1, 16))
story.append(Paragraph("Brendan Ngehsi Newanforbi", plain))
story.append(Paragraph("Plaintiff in pro per", plain))
story.append(Spacer(1, 8))
story.append(Paragraph(f"{DATE}", small))

os.makedirs(OUT_DIR, exist_ok=True)
SimpleDocTemplate(
    DEMAND_PATH,
    pagesize=letter,
    leftMargin=1.0 * inch,
    rightMargin=1.0 * inch,
    topMargin=0.7 * inch,
    bottomMargin=0.7 * inch,
    title="Final Early Global Settlement Demand (Sep 12 2026)",
).build(story, onFirstPage=stamp_settlement_page, onLaterPages=stamp_settlement_page)
print(f"Generated: {DEMAND_PATH}")

with open(COVER_PATH, "w", encoding="utf-8") as fh:
    fh.write(COVER_EMAIL)
print(f"Generated: {COVER_PATH}")
