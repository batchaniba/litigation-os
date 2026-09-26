#!/usr/bin/env python3
"""Matter 25 -- Notice of Rule 30(b)(6) deposition of Federal Express Corporation.

Newanforbi v. Federal Express Corporation, USDC E.D. Cal.
No. 2:26-cv-02881-DAD-SCR.

Renders on the portfolio pleading paper (reusing the discovery-set helpers in
matter25-discovery-set-one.py) with Schedule A (matters for examination) and a
proof of service. Without --date it renders an unsigned HOLD copy with blank
logistics: Rule 30(b)(6) requires a good-faith conference on the matters for
examination before or promptly after the notice is served, and the date, time,
place, and recording method come out of that conference.

    python3 internal/scripts/matter25-30b6-notice.py                    # HOLD copy
    python3 internal/scripts/matter25-30b6-notice.py --stamp-signature \\
        --date "December 1, 2026" --depo-date "January 12, 2027" \\
        --depo-time "9:30 a.m. Pacific" \\
        --depo-place "By remote videoconference (Zoom) under Fed. R. Civ. P. 30(b)(4), by stipulation" \\
        --recording "stenographically by a certified shorthand reporter, and by audio-visual means" \\
        --mailed-from "San Jose, California" --also-email
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("disc", SCRIPT_DIR / "matter25-discovery-set-one.py")
disc = importlib.util.module_from_spec(_spec)
sys.modules["disc"] = disc
_spec.loader.exec_module(disc)

PleadingPaper = disc.PleadingPaper
ROOT = disc.ROOT
OUT_DIR = ROOT / "internal/docs/matter-25/depositions"
BLANK = "______________________________"

TOPICS = [
    # Entity and decision structure
    "The identity and role of each FedEx entity (including Federal Express Corporation, FedEx Ground Package System, Inc., and any unit identified as \"FEDEX GROUND HR\") that recruited, screened, extended a conditional offer to, or made the Adverse Action concerning Plaintiff, and the relationship among those entities for hiring purposes in California in 2024-2025.",
    # The 2025 application
    "Plaintiff's 2025 application, including each question, instruction, and certification presented to him (including the forms dated on or about January 8, 2025); the order and timing in which they were presented relative to any conditional offer; his answers; and the applicant-tracking-system records (including Paradox and Workday) that reflect them.",
    # Prior hires
    "Each application Plaintiff submitted to, and each period in which Plaintiff was hired, on-boarded, or employed by, any FedEx entity before 2025, including the position, dates, background checks obtained, the results of those checks, the answers Plaintiff gave to criminal-history or registry-related questions, and how each hiring decision was made.",
    # Offer and withdrawal
    "The conditional offer of employment extended to Plaintiff in or about 2025 and its withdrawal, including the position, facility, shift, hourly wage, expected hours, benefits, anticipated start date, and whether and when the position was filled by another person.",
    # FedEx - First Advantage relationship
    "The terms of FedEx's relationship with First Advantage in effect during 2024-2025 governing background screening of California applicants, including the screening package and components ordered for the position, any sex offender registry search, adjudication services, and any notice, warning, or term concerning California Penal Code section 290.46 or the permissible use of sex offender registry information.",
    # Report source
    "The background report concerning Plaintiff that FedEx received on or before March 10, 2025, including each search component, its source (including whether any registry result came from the National Sex Offender Public Website, the California Department of Justice Megan's Law website, or another database), the \"source of record\" information it contained, and every version of it.",
    # Adjudication
    "The adjudication, scoring, or eligibility criteria (including any \"client criteria\" or matrix) applied to Plaintiff's report, how sex offender registry results are scored under those criteria, who designed and who applied them, and the resulting score or status for Plaintiff.",
    # Access
    "Each person and system that received, accessed, viewed, downloaded, or evaluated Plaintiff's report or any component of it, and when, as reflected in audit logs or other records.",
    # Reasons and decisionmakers
    "The decision to take the Adverse Action, including every person who participated in, recommended, reviewed, or approved it; every reason considered or relied on at the time; and every document that records a reason.",
    # Notices
    "The pre-adverse action notice sent on or about March 10, 2025 and the adverse-action notice sent on or about March 19, 2025, including their drafting, templates, content (including any reference to the National Sex Offender Public Website or the California sex offender website), enclosures, who sent them, how they were delivered, and whether a complete copy of the report was provided to Plaintiff before the Adverse Action.",
    # Misrepresentation defense
    "The factual basis for FedEx's contention that Plaintiff's application contained material misrepresentations that independently justified the hiring decision (Status Report, ECF No. 10), and for FedEx's Seventh Affirmative Defense, including: each alleged misrepresentation; when and how FedEx first identified it; whether it was considered before the Adverse Action; FedEx's policies on application misrepresentations; and how FedEx treated the same or similar answers in Plaintiff's prior applications.",
    # Same decision
    "Whether FedEx would have taken the Adverse Action if Plaintiff's report had contained no sex offender registry information, and the facts supporting FedEx's position.",
    # (j)(1)
    "The factual basis for FedEx's Eighth Affirmative Defense (use of information to protect a person at risk under California Penal Code section 290.46(j)(1)), including the identity or description of each person or class of persons claimed to be at risk, the particular risk, any job-specific assessment made before the Adverse Action, and whether Plaintiff was told FedEx was relying on that provision.",
    # Job duties
    "The duties of the position for which Plaintiff was considered in 2025, including whether it involved supervising minors, working directly and in an unaccompanied setting with minor children, caring for elder or dependent adults, or entering customer residences.",
    # Legal requirement
    "Any federal, state, or local law that FedEx contends required or authorized it to conduct a criminal background check or sex offender registry search for the position, or to use sex offender registry information in deciding whether to hire Plaintiff.",
    # Policies
    "FedEx's policies, procedures, guidelines, and training in effect from January 1, 2023 through March 31, 2025 concerning the use of criminal history or sex offender registry information in hiring decisions for positions in California, including any that refer to California Penal Code section 290.46 or the California Fair Chance Act (Gov. Code § 12952).",
    # Fair Chance
    "Any individualized assessment, notice, or opportunity to respond that FedEx provided or performed concerning Plaintiff before the Adverse Action.",
    # Direct access
    "Whether any FedEx employee or agent directly accessed the California Megan's Law website or the National Sex Offender Public Website concerning Plaintiff, and if so, who, when, and why.",
    # Preservation
    "FedEx's preservation of documents and electronically stored information concerning Plaintiff, including any litigation hold (its date, scope, and custodians, but not privileged communications), and any loss or deletion of relevant records.",
    # Discovery responses
    "The sources searched, persons consulted, and methods used to prepare FedEx's answers to Plaintiff's First Set of Interrogatories, its responses to Plaintiff's First Set of Requests for Admission, and its production in response to Plaintiff's First Set of Requests for Production.",
]


def build(args) -> Path:
    ready = bool(args.date)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    served_name = "Notice of Rule 30(b)(6) Deposition of FedEx.pdf"
    hold_name = "HOLD - Notice of Rule 30(b)(6) Deposition of FedEx (unsigned, undated).pdf"
    final = OUT_DIR / (served_name if ready else hold_name)
    stale = OUT_DIR / (hold_name if ready else served_name)
    if stale.exists():
        stale.unlink()
    if not ready:
        args.stamp_signature = False
        args.mailed_from = ""
    depo_date = args.depo_date or BLANK
    depo_time = args.depo_time or BLANK
    depo_place = args.depo_place or BLANK
    recording = args.recording or "stenographically by a certified shorthand reporter"

    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        body = tmp / "30b6.pdf"
        d = PleadingPaper(str(body), doc_title_footer=f"NOTICE OF RULE 30(b)(6) DEPOSITION -- {disc.CAPTION_NAME}")
        disc.header(d, disc.right_block(["NOTICE OF DEPOSITION OF", "DEFENDANT FEDERAL EXPRESS", "CORPORATION UNDER", "FED. R. CIV. P. 30(b)(6)"],
                                        [f"Date: {depo_date}", f"Time: {depo_time}"]),
                    ["NOTICE OF DEPOSITION OF DEFENDANT FEDERAL EXPRESS", "CORPORATION UNDER FED. R. CIV. P. 30(b)(6)"])
        disc.para(d, "TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:", first_indent=0)
        disc.para(d, f"PLEASE TAKE NOTICE that, under Federal Rules of Civil Procedure 26 and 30(b)(6), Plaintiff Brendan Ngehsi Newanforbi will take the deposition of Defendant Federal Express Corporation on {depo_date}, beginning at {depo_time}, and continuing from day to day, excluding weekends and holidays, until completed, within the limits of Rule 30(d)(1).")
        disc.para(d, f"<<b:Place and manner.>> The deposition will take place {depo_place}. It will be recorded {recording}, before an officer authorized to administer oaths under Rule 28.")
        disc.para(d, "<<b:Designation.>> Under Rule 30(b)(6), Federal Express Corporation must designate one or more officers, directors, managing agents, or other persons who consent to testify on its behalf, and must prepare each designee to testify about information known or reasonably available to the organization concerning the matters described in Schedule A. Plaintiff requests that FedEx identify each designee and the matters on which each will testify at least seven (7) days before the deposition.")
        disc.para(d, "<<b:Conference on the matters for examination.>> As Rule 30(b)(6) requires, Plaintiff will confer in good faith with FedEx's counsel about the matters for examination, and invites counsel to raise any concern about a topic's scope promptly so that it can be resolved before the deposition rather than at it.")
        disc.para(d, "<<b:Documents.>> Plaintiff requests that each designee bring, or that FedEx produce before the deposition, the documents the designee reviewed to prepare, to the extent not already produced in response to Plaintiff's First Set of Requests for Production.")
        disc.signature(d, args.date, args.stamp_signature)
        d.start_new_page()
        disc.heading(d, "SCHEDULE A")
        d.write_line("MATTERS FOR EXAMINATION", bold=True, center=True)
        d.blank_line()
        disc.heading(d, "DEFINITIONS")
        disc.para(d, "The Definitions in Plaintiff's First Set of Interrogatories to Defendant Federal Express Corporation apply to this Schedule. In particular, \"FedEx\" means Federal Express Corporation and, to the extent it acted for or with Federal Express Corporation concerning Plaintiff, any affiliate (including FedEx Ground Package System, Inc. and \"FEDEX GROUND HR\"); \"Adverse Action\" means FedEx's decision in or about March 2025 to deny Plaintiff employment and withdraw any conditional offer. Unless otherwise stated, the relevant period is January 1, 2024 through the present, except that Matter No. 3 covers any time.", first_indent=0)
        disc.heading(d, "MATTERS")
        disc.numbered(d, "MATTER", TOPICS)
        d.save()
        parts = [body]
        parts.append(disc.pos(tmp / "pos.pdf", "Notice of Rule 30(b)(6) Deposition of Defendant FedEx, with Schedule A", args))
        disc.assemble(parts, final)
    print(f"wrote {final.relative_to(ROOT)}")
    return final


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default="", help="date the notice is signed and served; omit for the HOLD copy")
    ap.add_argument("--depo-date", default="")
    ap.add_argument("--depo-time", default="")
    ap.add_argument("--depo-place", default="")
    ap.add_argument("--recording", default="")
    ap.add_argument("--mailed-from", default="San Jose, California")
    ap.add_argument("--by-email", action="store_true")
    ap.add_argument("--also-email", action="store_true")
    ap.add_argument("--stamp-signature", action="store_true")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
