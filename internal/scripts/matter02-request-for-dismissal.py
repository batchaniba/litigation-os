#!/usr/bin/env python3
# ==========================================================
# NEWANFORBI v. MEZA-GONZALEZ, ET AL.
# Case No. 26CV168913 (Alameda Sup. Ct., Hayward Hall of Justice, Dept. 518)
# REQUEST FOR DISMISSAL WITHOUT PREJUDICE
# Cal. Code Civ. Proc. § 581(b)(1), (c)
#
# Execution / service date: August 11, 2026
# FILED_STATUS: False until actually filed with the Clerk.
#
# IMPORTANT DRAFTING NOTE: California superior courts ordinarily require
# a request for dismissal to be submitted on the mandatory Judicial
# Council form (CIV-110; Cal. Rules of Court, rule 1.31(a)) so the clerk
# can process it and enter it in the register of actions. No blank
# CIV-110 template was available in this environment to fill directly
# (see internal/scripts/fill-matter-22-civ110-cm200.py and
# matter12-build-aug4-filing-packets.py, both of which pulled a blank
# CIV-110 from an external uploads directory not present here). This
# script instead drafts the substantive CCP § 581 request on the
# portfolio's standard numbered pleading paper. Before filing, either
# (a) transcribe Item 1 (entire action / without prejudice) and the
# declaration below onto an actual CIV-110 and sign that instead, or
# (b) confirm with the Clerk's Office / e-filing vendor whether this
# narrative form will be accepted for a self-represented litigant.
# ==========================================================
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import PleadingPaper  # noqa: E402

FILED_STATUS = False  # flip to True once actually filed with the Clerk

EXECUTION_DATE = "August 11, 2026"
EXECUTION_DATE_SHORT = "Aug. 11, 2026"

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUTPUT_PATH = os.path.join(
    REPO_ROOT,
    "internal",
    "public",
    "documents",
    "matter-32",
    "from-02",
    "Request for Dismissal Without Prejudice (Draft, Aug 11 2026).pdf",
)

DOC_TITLE_FOOTER = (
    "REQUEST FOR DISMISSAL W/O PREJUDICE — "
    "NEWANFORBI v. MEZA-GONZALEZ, ET AL. (26CV168913)"
)


def build():
    d = PleadingPaper(OUTPUT_PATH, doc_title_footer=DOC_TITLE_FOOTER)

    # ---- party block ----
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")
    d.write_line("1455 Cat Tail Drive, Stockton, CA 95204")
    d.write_line("Tel: (209) 801-4442 · E-mail: bnn.cdl@gmail.com")

    # ---- court ----
    d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    d.write_line("COUNTY OF ALAMEDA — HAYWARD HALL OF JUSTICE", bold=True, center=True)

    # ---- caption ----
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("SANTIAGO MEZA-GONZALEZ; JOSE MELANO;", False, False),
        ("STATE OF CALIFORNIA / CALIFORNIA", False, False),
        ("HIGHWAY PATROL; and DOES 1-10,", False, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        ("Case No. 26CV168913", True, False),
        ("", False, False),
        ("REQUEST FOR DISMISSAL", True, False),
        ("WITHOUT PREJUDICE", True, False),
        ("[Code Civ. Proc., § 581(b)(1), (c)]", False, False),
        ("", False, False),
        ("Assigned to: Hon. Mark Fickes", False, False),
        ("Dept. 518", False, False),
        ("", False, False),
        ("Complaint Filed: Feb. 4, 2026", False, False),
        ("Action currently STAYED per", False, False),
        ("Stipulation filed Apr. 14, 2026", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=11, boxed=True)

    d.write_wrapped(
        "TO THE CLERK OF THE COURT, ALL PARTIES, AND THEIR COUNSEL OF RECORD:",
        bold=True,
        first_indent=0,
    )

    d.write_wrapped(
        "PLEASE TAKE NOTICE that, pursuant to Code of Civil Procedure section 581, "
        "subdivisions (b)(1) and (c), Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in "
        "propria persona, hereby requests dismissal, without prejudice, of the "
        "above-captioned action in its entirety, as to all Defendants, including SANTIAGO "
        "MEZA-GONZALEZ; JOSE MELANO; STATE OF CALIFORNIA / CALIFORNIA HIGHWAY PATROL; and "
        "DOES 1 through 10."
    )

    d.write_wrapped(
        "Plaintiff is entitled to this dismissal without leave of court because no "
        "Defendant has filed an answer or a cross-complaint in this action. (Code Civ. "
        "Proc., § 581, subd. (b)(1) [plaintiff may dismiss with a written request to the "
        "clerk where no answer or cross-complaint has been filed]; <<i:id.,>> subd. (c) "
        "[plaintiff may dismiss an entire complaint at any time before the actual "
        "commencement of trial, upon written request to the clerk].) No trial date has "
        "been set, and no Defendant has served or filed an answer, demurrer, or other "
        "responsive pleading; the anticipated demurrer noticed by the Attorney General's "
        "Office on April 2, 2026 was never briefed and its filing was superseded by the "
        "April 14, 2026 stipulated stay, before any responsive pleading was filed."
    )

    d.write_wrapped(
        "On April 14, 2026, the parties stipulated, and the Court ordered, that this "
        "action be stayed in its entirety pending final resolution of the related federal "
        "action, <<i:Newanforbi v. State of California, et al.>>, No. 2:25-cv-01460-DC-CSK "
        "(E.D. Cal.) (the <<b:\"Federal Action\">>). Concurrently with this Request, "
        "Plaintiff is filing a Notice of Voluntary Dismissal Without Prejudice of the "
        "Federal Action under Fed. R. Civ. P. 41(a)(1)(A)(i). Nothing in the April 14, "
        "2026 stipulation or stay order restricts Plaintiff's independent, unilateral "
        "right under Code of Civil Procedure section 581 to dismiss this action without "
        "prejudice, and this Request is filed notwithstanding the stay because it "
        "terminates, rather than advances, the stayed proceedings."
    )

    d.write_wrapped(
        "Plaintiff further gives notice that entry of this dismissal will moot Plaintiff's "
        "pending Motion for U-Visa Certification, heard June 18, 2026 in Dept. 518 and "
        "currently awaiting ruling, as well as the July 6, 2026 Case Management Conference "
        "and all other dates suspended by the April 14, 2026 stay order. The Clerk is "
        "respectfully requested to reflect this Request for Dismissal in the register of "
        "actions, vacate all further proceedings, and close the file. This dismissal is "
        "<<b:without prejudice>> and does not operate as an adjudication on the merits of "
        "any claim. Each party shall bear its own costs and attorneys' fees, if any."
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
    d.write_line("PROOF OF SERVICE", bold=True, center=True, underline=True)
    d.blank_line()

    d.write_wrapped(
        f"I, BRENDAN NGEHSI NEWANFORBI, declare under penalty of perjury under the laws "
        f"of the State of California that on {EXECUTION_DATE}, I caused a true and "
        f"correct copy of the foregoing <<b:REQUEST FOR DISMISSAL WITHOUT PREJUDICE>> to "
        f"be filed with the Clerk of the Alameda County Superior Court, Hayward Hall of "
        f"Justice, 24405 Amador Street, Hayward, California 94544 (through the Court's "
        f"e-filing system, to the extent Plaintiff is so registered), and to be served by "
        f"electronic mail and/or United States first-class mail, postage prepaid, upon the "
        f"following:",
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
    d.write_line(f"Executed on {EXECUTION_DATE}, at Milpitas, California.")
    d.write_line("/s/ Brendan Ngehsi Newanforbi", bold=True)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")

    d.save()
    print(f"Wrote {OUTPUT_PATH}")
    print(f"FILED_STATUS={FILED_STATUS}; execution date={EXECUTION_DATE_SHORT}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    build()
