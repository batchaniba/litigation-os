#!/usr/bin/env python3
# ==========================================================
# NEWANFORBI v. STATE OF CALIFORNIA / CHP ET AL.
# Case No. 2:25-cv-01460-DC-CSK (USDC E.D. Cal.)
# NOTICE OF VOLUNTARY DISMISSAL WITHOUT PREJUDICE
# Fed. R. Civ. P. 41(a)(1)(A)(i)
#
# Execution / service date: August 7, 2026
# FILED_STATUS: False until actually e-filed via CM/ECF.
# ==========================================================
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import PleadingPaper  # noqa: E402

FILED_STATUS = False  # flip to True once e-filed and served

EXECUTION_DATE = "August 7, 2026"
EXECUTION_DATE_SHORT = "Aug. 7, 2026"

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUTPUT_PATH = os.path.join(
    REPO_ROOT,
    "internal",
    "public",
    "documents",
    "matter-32",
    "from-01",
    "Notice of Voluntary Dismissal Without Prejudice (Aug 7 2026).pdf",
)

DOC_TITLE_FOOTER = (
    "NOTICE OF VOLUNTARY DISMISSAL W/O PREJUDICE — "
    "NEWANFORBI v. STATE OF CALIFORNIA ET AL. (2:25-cv-01460-DC-CSK)"
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
        ("STATE OF CALIFORNIA; CALIFORNIA", False, False),
        ("HIGHWAY PATROL; OFFICER SANTIAGO", False, False),
        ("MEZA-GONZALEZ (#023295); OFFICER", False, False),
        ("MELANO (#023054),", False, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        ("Case No. 2:25-cv-01460-DC-CSK", True, False),
        ("", False, False),
        ("NOTICE OF VOLUNTARY", True, False),
        ("DISMISSAL WITHOUT PREJUDICE", True, False),
        ("[Fed. R. Civ. P. 41(a)(1)(A)(i)]", False, False),
        ("", False, False),
        ("Judge: Hon. Dena M. Coggins", False, False),
        ("Mag. Judge: Hon. Chi Soo Kim", False, False),
        ("", False, False),
        ("Complaint Filed: May 27, 2025", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=11, boxed=True)

    d.write_wrapped(
        "TO THE CLERK OF THE COURT, ALL PARTIES, AND THEIR COUNSEL OF RECORD:",
        bold=True,
        first_indent=0,
    )

    d.write_wrapped(
        "PLEASE TAKE NOTICE that, pursuant to Rule 41(a)(1)(A)(i) of the Federal Rules of "
        "Civil Procedure, Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, "
        "hereby voluntarily dismisses the above-captioned action in its entirety, without "
        "prejudice, as to all Defendants, including Defendants STATE OF CALIFORNIA; "
        "CALIFORNIA HIGHWAY PATROL; OFFICER SANTIAGO MEZA-GONZALEZ (#023295); and "
        "OFFICER MELANO (#023054)."
    )

    d.write_wrapped(
        "Plaintiff is entitled to dismiss this action as a matter of right because no "
        "Defendant has served either an answer or a motion for summary judgment. "
        "(Fed. R. Civ. P. 41(a)(1)(A)(i).) The only dispositive motion served by any "
        "Defendant in this action is Defendants' Motion to Dismiss under Rule 12(b)(6) "
        "(filed December 10, 2025), which is neither an answer nor a motion for summary "
        "judgment within the meaning of Rule 41(a)(1)(A)(i). (See <<i:Hamilton v. "
        "Shearson-Lehman American Express, Inc.>>, 813 F.2d 1532, 1534-35 (9th Cir. 1987) "
        "[right to dismiss under Rule 41(a)(1) is absolute until the defendant serves an "
        "answer or motion for summary judgment]; <<i:Concha v. London>>, 62 F.3d 1493, "
        "1506 (9th Cir. 1995) [Rule 12(b)(6) motion does not terminate the plaintiff's "
        "absolute right to dismiss under Rule 41(a)(1)].) The Magistrate Judge's April 20, "
        "2026 Findings and Recommendations recommending dismissal, Plaintiff's April 21, "
        "2026 Objections thereto, and Plaintiff's July 7, 2026 Notice of Supplemental "
        "Authority likewise do not constitute an answer or a motion for summary judgment."
    )

    d.write_wrapped(
        "Because this is the first voluntary dismissal by Plaintiff of any action based "
        "on or including the claims asserted in this action, the dismissal is <<b:without "
        "prejudice>> and does not operate as an adjudication on the merits. "
        "(Fed. R. Civ. P. 41(a)(1)(B).) No court order is required to effect this dismissal. "
        "(See <<i:Commercial Space Mgmt. Co. v. Boeing Co.>>, 193 F.3d 1074, 1077-78 "
        "(9th Cir. 1999) [Rule 41(a)(1) notice of dismissal is self-executing and terminates "
        "the action automatically upon filing].) The Clerk of the Court is respectfully "
        "requested to close the file. Each party shall bear its own costs and attorneys' "
        "fees, if any."
    )

    # ---- signature ----
    d.ensure_space(7)
    d.blank_line()
    d.write_line(f"Dated: {EXECUTION_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.write_line("/s/ Brendan Ngehsi Newanforbi", bold=True)
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
        f"system, which will provide electronic notice to all counsel of record registered "
        f"through CM/ECF, and, to the extent required, to be served by United States "
        f"first-class mail, postage prepaid, and/or by electronic mail, upon the following:",
        first_indent=0,
    )
    d.blank_line()

    d.write_line("Counsel for Defendants:", bold=True)
    d.write_line("Haiyang A. Li, Deputy Attorney General")
    d.write_line("Office of the Attorney General / Department of Justice")
    d.write_line("300 South Spring Street, Suite 1702, Los Angeles, CA 90013")
    d.write_line("Haiyang.Li@doj.ca.gov")
    d.write_line("cc: Adriana Zagal, Legal Secretary — Adriana.Zagal@doj.ca.gov")
    d.blank_line()
    d.write_line(f"Executed on {EXECUTION_DATE}, at Stockton, California.")
    d.write_line("/s/ Brendan Ngehsi Newanforbi", bold=True)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")

    d.save()
    print(f"Wrote {OUTPUT_PATH}")
    print(f"FILED_STATUS={FILED_STATUS}; execution date={EXECUTION_DATE_SHORT}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    build()
