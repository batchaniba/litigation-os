#!/usr/bin/env python3
# ==========================================================
# NEWANFORBI v. CANDELARIA, ET AL.
# Case No. 2:26-cv-00983-DC-CSK (PS) (USDC E.D. Cal.)
# NOTICE OF VOLUNTARY DISMISSAL WITHOUT PREJUDICE
# Fed. R. Civ. P. 41(a)(1)(A)(i)
#
# Execution / service date: August 11, 2026
# FILED_STATUS: False until actually e-filed via CM/ECF.
#
# Context: neither Defendant has been served with process or has
# appeared. Plaintiff's IFP application remains pending; Mag. Judge
# Kim's June 15, 2026 F&R (ECF No. 6) recommends denying IFP and
# dismissing the FAC (ECF No. 5) without leave to amend. Plaintiff's
# June 18, 2026 Objections and July 9, 2026 Notice of Supplemental
# Authority are pending District Judge review. None of the foregoing
# is an answer or a motion for summary judgment, so the Rule 41(a)(1)
# (A)(i) right to dismiss as of right remains intact.
# ==========================================================
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import PleadingPaper  # noqa: E402

FILED_STATUS = False  # flip to True once e-filed and served

EXECUTION_DATE = "August 11, 2026"
EXECUTION_DATE_SHORT = "Aug. 11, 2026"

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUTPUT_PATH = os.path.join(
    REPO_ROOT,
    "internal",
    "public",
    "documents",
    "matter-33",
    "from-07",
    "Notice of Voluntary Dismissal Without Prejudice (Aug 11 2026).pdf",
)

DOC_TITLE_FOOTER = (
    "NOTICE OF VOLUNTARY DISMISSAL W/O PREJUDICE — "
    "NEWANFORBI v. CANDELARIA, ET AL. (2:26-cv-00983-DC-CSK)"
)


def build():
    d = PleadingPaper(OUTPUT_PATH, doc_title_footer=DOC_TITLE_FOOTER)

    # ---- attorney / pro se block ----
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")
    d.write_line("1455 Cat Tail Drive, Stockton, CA 95204")
    d.write_line("Tel: (209) 801-4442 · E-mail: bnn.cdl@gmail.com")

    # ---- court ----
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("FOR THE EASTERN DISTRICT OF CALIFORNIA", bold=True, center=True)

    # ---- caption ----
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("DIANA CANDELARIA, in her individual", False, False),
        ("capacity; and STEVE GORDON, Director", False, False),
        ("of the California Department of Motor", False, False),
        ("Vehicles, in his official capacity,", False, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        ("Case No. 2:26-cv-00983-DC-CSK (PS)", True, False),
        ("", False, False),
        ("NOTICE OF VOLUNTARY", True, False),
        ("DISMISSAL WITHOUT PREJUDICE", True, False),
        ("[Fed. R. Civ. P. 41(a)(1)(A)(i)]", False, False),
        ("", False, False),
        ("Judge: Hon. Dena M. Coggins", False, False),
        ("Mag. Judge: Hon. Chi Soo Kim", False, False),
        ("", False, False),
        ("FAC Filed: April 29, 2026", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=11, boxed=True)

    d.write_wrapped(
        "TO THE CLERK OF THE COURT, ALL PARTIES, AND THEIR COUNSEL OF RECORD, IF ANY:",
        bold=True,
        first_indent=0,
    )

    d.write_wrapped(
        "PLEASE TAKE NOTICE that, pursuant to Rule 41(a)(1)(A)(i) of the Federal Rules of "
        "Civil Procedure, Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, "
        "hereby voluntarily dismisses the above-captioned action in its entirety, without "
        "prejudice, as to all Defendants, including Defendants DIANA CANDELARIA, in her "
        "individual capacity, and STEVE GORDON, Director of the California Department of "
        "Motor Vehicles, in his official capacity."
    )

    d.write_wrapped(
        "Plaintiff is entitled to dismiss this action as a matter of right because no "
        "Defendant has been served with process, has appeared, or has served either an "
        "answer or a motion for summary judgment. (Fed. R. Civ. P. 41(a)(1)(A)(i).) Plaintiff "
        "initiated this action on March 19, 2026 and applied to proceed in forma pauperis "
        "under 28 U.S.C. § 1915 (ECF Nos. 1, 2); after the Court denied that application "
        "without prejudice (ECF No. 3), Plaintiff filed a renewed IFP application and the "
        "operative First Amended Complaint on April 29, 2026 (ECF Nos. 4, 5). Because IFP "
        "screening under 28 U.S.C. § 1915(e) remains pending, no summons has issued and "
        "neither Defendant has been served or has entered an appearance. The only filings "
        "in this action are Plaintiff's own papers and the Magistrate Judge's June 15, 2026 "
        "Findings and Recommendations (ECF No. 6), which recommend that Plaintiff's IFP "
        "application be denied and the First Amended Complaint be dismissed without leave "
        "to amend. Neither the F&R, Plaintiff's June 18, 2026 Objections thereto, nor "
        "Plaintiff's July 9, 2026 Notice of Supplemental Authority is an answer or a motion "
        "for summary judgment within the meaning of Rule 41(a)(1)(A)(i). "
        "(See <<i:Hamilton v. Shearson-Lehman American Express, Inc.>>, 813 F.2d 1532, "
        "1534-35 (9th Cir. 1987) [right to dismiss under Rule 41(a)(1) is absolute until the "
        "defendant serves an answer or motion for summary judgment]; <<i:Concha v. London>>, "
        "62 F.3d 1493, 1506 (9th Cir. 1995) [same, as to a Rule 12(b)(6) motion]; "
        "<<i:Miller v. Terramite Corp.>>, 114 F. App'x 536, 539 (4th Cir. 2004) [same rule "
        "applies a fortiori where the defendant has not yet been served].)"
    )

    d.write_wrapped(
        "This is Plaintiff's first dismissal of any action based on or including the claims "
        "asserted against these Defendants. Plaintiff notes that Matter 1 of Plaintiff's "
        "related-case docket, <<i:Newanforbi v. State of California, et al.>>, No. "
        "2:25-cv-01460-DC-CSK (E.D. Cal.), arises from the same November 1, 2024 CHP "
        "encounter but asserts distinct Fourth and Fourteenth Amendment claims against "
        "different defendants (CHP Officers Meza-Gonzalez and Melano) arising from the "
        "traffic stop itself, not the subsequent DMV APS hearing at issue here; a voluntary "
        "dismissal of that separate action accordingly does not implicate the two-dismissal "
        "rule of Rule 41(a)(1)(B) as to the claims dismissed here. Because this is the first "
        "voluntary dismissal by Plaintiff of any action based on or including the claims "
        "asserted in this action, the dismissal is <<b:without prejudice>> and does not "
        "operate as an adjudication on the merits. (Fed. R. Civ. P. 41(a)(1)(B).) No court "
        "order is required to effect this dismissal. (See <<i:Commercial Space Mgmt. Co. v. "
        "Boeing Co.>>, 193 F.3d 1074, 1077-78 (9th Cir. 1999) [Rule 41(a)(1) notice of "
        "dismissal is self-executing and terminates the action automatically upon filing].) "
        "The Clerk of the Court is respectfully requested to close the file. Each party shall "
        "bear its own costs and attorneys' fees, if any."
    )

    # ---- signature ----
    d.ensure_space(7)
    d.blank_line()
    d.write_line(f"Dated: {EXECUTION_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.write_line("___________________________________")
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")
    d.write_line("1455 Cat Tail Drive, Stockton, CA 95204")
    d.write_line("(209) 801-4442 · bnn.cdl@gmail.com")

    # ---- Certificate of Service ----
    d.start_new_page()
    d.write_line("CERTIFICATE OF SERVICE", bold=True, center=True, underline=True)
    d.blank_line()

    d.write_wrapped(
        f"I, BRENDAN NGEHSI NEWANFORBI, declare under penalty of perjury under the laws "
        f"of the United States of America that on {EXECUTION_DATE}, I caused a true and "
        f"correct copy of the foregoing <<b:NOTICE OF VOLUNTARY DISMISSAL WITHOUT "
        f"PREJUDICE>> to be filed with the Clerk of the Court through the Court's CM/ECF "
        f"system, which will provide electronic notice to any counsel of record registered "
        f"through CM/ECF. As of the date of this filing, neither Defendant Diana Candelaria "
        f"nor Defendant Steve Gordon has been served with process or has appeared in this "
        f"action; accordingly, no further service is required as to either Defendant under "
        f"Fed. R. Civ. P. 5(a)(2).",
        first_indent=0,
    )
    d.blank_line()
    d.write_line(f"Executed on {EXECUTION_DATE}, at Stockton, California.")
    d.write_line("___________________________________")
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")

    d.save()
    print(f"Wrote {OUTPUT_PATH}")
    print(f"FILED_STATUS={FILED_STATUS}; execution date={EXECUTION_DATE_SHORT}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    build()
