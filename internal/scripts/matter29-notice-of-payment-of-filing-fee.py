# ==========================================================
# NEWANFORBI v. AMAZON.COM SERVICES, LLC, ET AL. (26CV201554)
# NOTICE OF PAYMENT OF FILING FEE; WITHDRAWAL OF REQUEST TO
# WAIVE COURT FEES AS MOOT
# (Gov. Code § 70611(a); Cal. Rules of Court, rule 3.55)
#
# Companion to the August 3, 2026 cover letter to the clerk
# (matter29-fee-payment-letter.py). The letter was correspondence; this
# is the filed pleading that puts the payment on the docket, so the
# August 18, 2026 fee-waiver hearing in Dept. FHO can be taken off
# calendar on a record rather than on a letter in the clerk's inbox.
#
# MONEY ORDER IDENTIFICATION — READ BEFORE EDITING. Plaintiff purchased
# TWO $435.00 USPS money orders at the same Milpitas post office on
# August 3, 2026, and only one of them belongs to this action:
#
#   Serial #55201761577 — 12:53 p.m., paid in cash — MATTER 22 (Pilot),
#       the Gov. Code § 68637 waived-fee repayment mailed with the
#       CIV-110 Request for Dismissal. NOT this action.
#   Serial #55300687696 — 4:29 p.m., paid by debit — THIS ACTION, the
#       first-paper filing fee under Gov. Code § 70611(a).
#
# The two are told apart by the postage purchased minutes after each:
# the 4:38 p.m. First-Class large-envelope transaction on the same
# receipt is addressed to Hayward, CA 94544 — the Hayward Hall of
# Justice — while Matter 22's mailing was a single $0.82 stamp at
# 12:54 p.m. Source of both: the USPS eReceipt PDF already in the file
# at documents/matter-29/Gmail - USPS eReceipt - Filing Fee Money Order
# and Postage (Aug 3 2026).pdf, pages 4 and 6.
#
# Neither defendant has appeared as of the execution date, so no proof
# of service accompanies this notice; it is filed with the court.
# ==========================================================
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import (  # noqa: E402
    PleadingPaper,
    CONTENT_LEFT,
    COURT_LINE1,
)

from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

SIGNATURE_IMG = SIGNATURE_PATH
SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_DIR = os.path.join(REPO_ROOT, "internal", "public", "documents", "matter-29")
OUT_NAME = (
    "Notice of Payment of Filing Fee and Withdrawal of Fee Waiver Request "
    "as Moot (Aug 7 2026).pdf"
)

CASE_NO = "26CV201554"
EXEC_DATE = "August 7, 2026"
PLAINTIFF = "Brendan Ngehsi Newanforbi"

FEE = "$435.00"
MONEY_ORDER = "55300687696"
MO_FEE = "$2.65"
MO_TOTAL = "$437.65"
PAY_DATE = "August 3, 2026"
FOOTER = "NOTICE OF PAYMENT OF FILING FEE — NEWANFORBI v. AMAZON.COM SERVICES, LLC, ET AL."

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

PARTY_BLOCK_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("AMAZON.COM SERVICES, LLC, a", True, False),
    ("Delaware limited liability company;", True, False),
    ("ACCURATE BACKGROUND LLC; and", True, False),
    ("DOES 1 through 10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    (f"Case No. {CASE_NO}", False, False),
    ("", False, False),
    ("NOTICE OF PAYMENT OF", True, False),
    ("FILING FEE; WITHDRAWAL OF", True, False),
    ("REQUEST TO WAIVE COURT", True, False),
    ("FEES AS MOOT", True, False),
    ("", False, False),
    ("(Gov. Code § 70611(a))", False, False),
    ("", False, False),
    ("Fee Waiver Hearing:", False, False),
    ("Date: August 18, 2026", False, False),
    ("Time: 11:30 a.m.", False, False),
    ("Dept.: FHO", False, False),
    ("", False, False),
    ("Assigned for all purposes to:", False, False),
    ("Hon. Jamilah Jefferson, Dept. 520", False, False),
    ("CMC: Jan. 6, 2027, 10:00 a.m.", False, False),
    ("Action Filed: July 28, 2026", False, False),
]


def build() -> str:
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, OUT_NAME)
    d = PleadingPaper(out_path, doc_title_footer=FOOTER)
    c = d.c

    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()

    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
    d.blank_line()

    d.draw_caption_block(PARTY_BLOCK_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()

    d.write_line("NOTICE OF PAYMENT OF FILING FEE; WITHDRAWAL OF", bold=True, center=True)
    d.write_line("REQUEST TO WAIVE COURT FEES AS MOOT", bold=True, center=True)
    d.blank_line()

    d.write_wrapped(
        "TO THE HONORABLE COURT, THE CLERK OF THE COURT, AND ALL PARTIES AND THEIR "
        "ATTORNEYS OF RECORD:",
        first_indent=0,
    )
    d.blank_line()

    d.write_wrapped(
        f"PLEASE TAKE NOTICE that Plaintiff {PLAINTIFF}, appearing in propria persona, "
        f"has paid the first-paper filing fee in this action in full, in the amount of "
        f"{FEE} (Gov. Code, § 70611(a)). The particulars of payment are as follows.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        f"<<b:1. Payment.>> On {PAY_DATE}, Plaintiff purchased a United States Postal "
        f"Service money order in the amount of {FEE}, bearing <<b:Serial No. "
        f"{MONEY_ORDER}>>, at the United States Post Office located at 450 South Abel "
        f"Street, Milpitas, California 95035, at approximately 4:29 p.m. Pacific Time. "
        f"A money order issuance fee of {MO_FEE} was paid in addition to the face "
        f"amount, for a total of {MO_TOTAL}.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        f"<<b:2. Transmittal to the Court.>> At approximately 4:38 p.m. Pacific Time "
        f"the same day, Plaintiff deposited the money order with the United States "
        f"Postal Service at the same location, enclosed in a First-Class Mail large "
        f"envelope together with a cover letter dated {PAY_DATE}, addressed to the "
        f"Clerk of the Court, Department FHO, Hayward Hall of Justice, 24405 Amador "
        f"Street, Hayward, California 94544. Postage of $1.69 was prepaid and the "
        f"Postal Service gave an estimated delivery date of Thursday, August 6, 2026. "
        f"The envelope was sent by standard First-Class Mail and therefore bears no "
        f"tracking number.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        f"<<b:3. Documentary support.>> The foregoing is documented by the United "
        f"States Postal Service electronic receipt for {PAY_DATE}, which records both "
        f"the issuance of money order Serial No. {MONEY_ORDER} (transaction no. 061, "
        f"receipt no. 036372) and the First-Class Mail large-envelope postage to "
        f"Hayward, California 94544 purchased nine minutes later (transaction no. 062, "
        f"receipt no. 036373). Plaintiff has retained that receipt and will lodge a "
        f"copy with the Court upon request or at any hearing on this matter.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "<<b:4. Request to Waive Court Fees is moot.>> Because the filing fee has now "
        "been paid in full, Plaintiff hereby <<b:WITHDRAWS>> his pending Request to "
        "Waive Court Fees (Judicial Council form FW-001) in this action. Plaintiff no "
        "longer seeks a waiver of court fees and costs here, and the Court need not "
        "reach the questions identified in its Order on Court Fee Waiver (form FW-003) "
        "signed July 31, 2026.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "<<b:5. Request that the August 18, 2026 hearing be taken off calendar.>> The "
        "Court's Order on Court Fee Waiver set a hearing for August 18, 2026, at 11:30 "
        "a.m. in Department FHO for the sole purpose of obtaining further information "
        "in support of the fee-waiver request. That request having been withdrawn and "
        "the fee having been paid, no issue remains for the Court to decide, and "
        "Plaintiff respectfully requests that the hearing be taken off calendar. "
        "Plaintiff will appear on that date notwithstanding this notice if the Court "
        "requires his appearance or if payment has not by then been posted to the "
        "docket.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "<<b:6. No effect on the merits.>> This notice addresses the payment of court "
        "fees only. Nothing in it is intended as, or shall be construed as, a waiver "
        "or limitation of any claim, right, or remedy asserted in the Verified "
        "Complaint, nor does it alter any deadline in this action.",
        first_indent=36,
    )
    d.blank_line()
    d.blank_line()

    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}", bold=False)
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()

    sig_line = "___________________________________"
    if os.path.isfile(SIGNATURE_IMG):
        d.draw_signature_image(SIGNATURE_IMG, SIG_IMG_W_PX, SIG_IMG_H_PX, sig_line)
    d.write_line(sig_line, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)

    # ---- Declaration, so the notice proves its own facts ----
    d.start_new_page()
    d.write_line(f"DECLARATION OF {PLAINTIFF.upper()}", bold=True, center=True)
    d.blank_line()

    d.write_wrapped(
        f"I, {PLAINTIFF}, declare:",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "1. I am the Plaintiff in this action and appear in propria persona. I have "
        "personal knowledge of the facts stated below and, if called as a witness, "
        "could and would testify competently to them.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        f"2. On {PAY_DATE}, at approximately 4:29 p.m. Pacific Time, I purchased a "
        f"United States Postal Service money order in the amount of {FEE}, bearing "
        f"Serial No. {MONEY_ORDER}, at the United States Post Office located at 450 "
        f"South Abel Street, Milpitas, California 95035, and paid an additional {MO_FEE} "
        f"money order issuance fee, for a total of {MO_TOTAL}.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        f"3. That money order was purchased for the specific purpose of paying the "
        f"{FEE} first-paper filing fee in this action, Newanforbi v. Amazon.com "
        f"Services, LLC, et al., Case No. {CASE_NO}. On the same date I purchased a "
        f"separate money order in the same amount for an unrelated matter; that other "
        f"money order bears a different serial number and was mailed to a different "
        f"court. The money order identified in paragraph 2, Serial No. {MONEY_ORDER}, "
        f"is the one mailed to this Court.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        f"4. At approximately 4:38 p.m. Pacific Time on {PAY_DATE}, at the same post "
        f"office, I enclosed that money order in a First-Class Mail large envelope "
        f"together with a cover letter of the same date, addressed the envelope to the "
        f"Clerk of the Court, Department FHO, Hayward Hall of Justice, 24405 Amador "
        f"Street, Hayward, California 94544, prepaid $1.69 in postage, and deposited "
        f"it with the United States Postal Service. The Postal Service gave an "
        f"estimated delivery date of Thursday, August 6, 2026. I did not purchase "
        f"tracking, and the mailing therefore bears no tracking number.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "5. I have retained the United States Postal Service electronic receipt "
        "documenting both transactions described above, and I am prepared to lodge a "
        "copy of it with the Court.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        f"I declare under penalty of perjury under the laws of the State of California "
        f"that the foregoing is true and correct. Executed on {EXEC_DATE}, at Stockton, "
        f"California.",
        first_indent=36,
    )
    d.blank_line()
    d.blank_line()

    d.ensure_space(6)
    if os.path.isfile(SIGNATURE_IMG):
        d.draw_signature_image(SIGNATURE_IMG, SIG_IMG_W_PX, SIG_IMG_H_PX, sig_line)
    d.write_line(sig_line, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", right=True, right_margin_offset=20)
    d.write_line("Declarant", right=True, right_margin_offset=20)

    d.save()
    print(f"Generated: {out_path}")
    return out_path


def main():
    build()
    print(f"Money order Serial No. {MONEY_ORDER} ({FEE}, {PAY_DATE}) — Matter 29.")
    print("Do NOT confuse with Serial No. 55201761577, the Matter 22 (Pilot)")
    print("Gov. Code 68637 waived-fee repayment purchased the same day.")
    print("Neither defendant has appeared; no proof of service required.")


if __name__ == "__main__":
    main()
