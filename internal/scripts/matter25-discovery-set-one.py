#!/usr/bin/env python3
"""Matter 25 -- Plaintiff's first-wave discovery on pleading paper.

Newanforbi v. Federal Express Corporation, USDC E.D. Cal.
No. 2:26-cv-02881-DAD-SCR.

Served after the Sep. 25, 2026 Rule 26(f) conference. Discovery requests are
served, not filed (E.D. Cal. L.R. 250.2-250.4). Builds, each with a proof of
service attached via the shared proof_of_service engine:

  01 Interrogatories, Set One          02 Requests for Admission, Set One
  03 Requests for Production, Set One  04 Rule 45 subpoena Attachments A and B
  05 Rule 45(a)(4) notice of subpoena (for the clerk-issued AO 88B)

    python3 internal/scripts/matter25-discovery-set-one.py \\
        [--date "September 25, 2026"] [--mailed-from "Stockton, California"] \\
        [--by-email] [--stamp-signature]

Signature lines print blank by default: Rule 26(g) makes the signature a
certification, so Plaintiff signs after reviewing. --stamp-signature applies
the canonical signature (signature_stamp.SIGNATURE_PATH) the way the other
matter scripts do.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_EDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal/docs/matter-25/discovery-set-one"
CASE_NO = "2:26-cv-02881-DAD-SCR"
CAPTION_NAME = "NEWANFORBI v. FEDERAL EXPRESS CORPORATION"

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("FEDERAL EXPRESS CORPORATION;", True, False),
    ("and DOES 1 through 10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

SIGNOFF_NAME = "BRENDAN NGEHSI NEWANFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

SERVICE_ADDRESSEES = [
    "Allison A. Kray, Esq. (SBN 312544)",
    "Federal Express Corporation",
    "2601 Main Street, Suite 1100",
    "Irvine, CA 92614",
    "allison.kray@fedex.com",
    "Attorney for Defendant Federal Express Corporation",
]

DEFINITIONS = [
    "1. <<b:\"FedEx,\" \"Defendant,\" \"You,\" and \"Your\">> mean Defendant Federal Express Corporation and, to the extent it acted for or with Federal Express Corporation in connection with Plaintiff's applications, background screening, or hiring decisions, any parent, subsidiary, or affiliate (including FedEx Ground Package System, Inc. and any unit identified as \"FEDEX GROUND HR\"), and their officers, employees, agents, and vendors.",
    "2. <<b:\"Plaintiff\">> means Brendan Ngehsi Newanforbi, including under any variation of that name (for example, Brendan Ngwa Nforbi, Brendan Ngwanforbi, or Ngwa-Nforbi).",
    "3. <<b:\"First Advantage\">> means First Advantage Background Services Corp. and any affiliate that prepared or furnished a background report about Plaintiff to FedEx.",
    "4. <<b:\"Report\">> means every consumer report, investigative consumer report, background report, and update or version of one, concerning Plaintiff that First Advantage or any other consumer reporting agency furnished to FedEx, including the report FedEx admits (Answer, ECF No. 4, paragraphs 17, 20, 34) was provided to it on or before March 10, 2025.",
    "5. <<b:\"Adverse Action\">> means FedEx's decision to deny Plaintiff employment, and to withdraw any conditional offer of employment, in or about March 2025, including the adverse-action notice dated on or about March 19, 2025.",
    "6. <<b:\"Registry Information\">> means any information identifying Plaintiff as a registered sex offender, from any source, including the California Department of Justice Megan's Law website (Cal. Penal Code \u00a7 290.46), the National Sex Offender Public Website (NSOPW), any state registry, or any database compiled from them.",
    "7. <<b:\"Prior Employment\">> means each period, before January 2025, in which FedEx hired or employed Plaintiff, and each application Plaintiff submitted to FedEx before January 2025.",
    "8. <<b:\"Document\">> and <<b:\"communication\">> have the broadest meaning allowed by Fed. R. Civ. P. 34(a)(1)(A), and include electronically stored information such as email, chat and instant messages, applicant-tracking-system records (including Paradox and Workday), portal records, notes, and audit logs.",
    "9. <<b:\"Identify,\">> for a person, means full name, job title, employer, and last known business address; for a document, its date, author, recipients, type, and Bates number if produced.",
    "10. Unless otherwise stated, the relevant period is January 1, 2024 through the present, except that requests about Prior Employment cover any time.",
]

ROGS = [
    "Identify each person who participated in, recommended, reviewed, or approved the Adverse Action, and describe each person's role.",
    "Identify the legal entity that (a) received Plaintiff's January 2025 application, (b) ordered the Report from First Advantage, and (c) made the Adverse Action, and state whether that entity was Federal Express Corporation, FedEx Ground Package System, Inc., or another entity.",
    "State every reason for the Adverse Action, and for each reason identify the documents and the persons with knowledge that support it.",
    "State all facts supporting Your contention (Status Report, ECF No. 10, at 2) that Plaintiff's application \"contained material misrepresentations that independently justified the hiring decision,\" including, for each alleged misrepresentation: the exact wording of the question; Plaintiff's answer; the date the question was presented; whether it was presented before or after any conditional offer of employment; and the date FedEx first contended the answer was a misrepresentation.",
    "State whether FedEx would have taken the Adverse Action if the Report had contained no Registry Information, and state all facts supporting Your answer.",
    "Describe each search or component FedEx ordered from First Advantage concerning Plaintiff (including the package name, any sex offender registry search, and each account, client code, order, or search ID number used), identify who selected that package for the position, and state the source First Advantage searched for any Registry Information (for example, NSOPW, the California Megan's Law website, or another database).",
    "Describe the adjudication or scoring criteria (including any \"client criteria\" or eligibility matrix) applied to the Report, including how Registry Information is scored, and identify who applied the criteria to Plaintiff's Report.",
    "Identify each position and period of Prior Employment (title, facility, start and end dates, and reason employment ended), and identify each background check or consumer report FedEx obtained on Plaintiff in connection with each, from any vendor.",
    "For each background check identified in response to Interrogatory No. 8, state whether it disclosed Registry Information about Plaintiff and what, if anything, FedEx did in response.",
    "Describe each policy, procedure, guideline, or training in effect between January 1, 2024 and March 31, 2025 concerning the use of Registry Information in hiring decisions in California, including any that refers to California Penal Code section 290.46.",
    "Identify each communication between FedEx and First Advantage concerning Plaintiff, by date, participants, and substance.",
    "Describe the position for which Plaintiff was considered in 2025, including title, facility, shift, duties, and whether the position involved supervising, or unsupervised contact with, minors or elder or dependent adults.",
    "State all facts supporting Your Eighth Affirmative Defense (that any use of Registry Information was to protect a person at risk under Cal. Penal Code § 290.46(j)(1)), and identify each person at risk You contend was protected.",
    "Describe any conditional offer of employment extended to Plaintiff in or about 2025, including its date, the position, hourly wage, expected weekly hours, and benefits.",
    "Identify each person who drafted, approved, or sent the adverse-action notice dated on or about March 19, 2025, and state the source of that notice's reference to the National Sex Offender Public Website and the California sex offender website (Answer ¶ 26).",
    "State whether any FedEx employee or agent accessed the California Megan's Law website or NSOPW concerning Plaintiff, and if so identify who, when, and for what purpose.",
    "State whether and when FedEx issued a litigation hold covering Plaintiff's application files, the Report, and communications with First Advantage, identify the custodians it covers, and state whether any document or electronically stored information concerning those subjects has been deleted, discarded, or lost since March 1, 2025, describing any such loss.",
    "If You contend that California Penal Code section 290.46(j)(2)(E) does not apply to the Adverse Action (including because any Registry Information came through the National Sex Offender Public Website or another source rather than the California Megan's Law website), state every factual basis for that contention and identify the documents supporting it.",
    "For each application identified in response to Interrogatory No. 8 that resulted in FedEx hiring or on-boarding Plaintiff, state whether You contend Plaintiff gave the same or a materially similar answer to each question You identified in response to Interrogatory No. 4, and state whether FedEx hired or on-boarded Plaintiff after receiving that answer.",
    "Identify each person who accessed, viewed, downloaded, or received the Report or any component of it, and state the date and purpose of each access known to You.",
]

RFAS = [
    "Admit that You engaged First Advantage to prepare a background report on Plaintiff in connection with his application for employment with You in 2025.",
    "Admit that the Report provided to You on or before March 10, 2025 identified Plaintiff as a registered sex offender.",
    "Admit that the Report identified the California sex offender registry as the source of the registry record concerning Plaintiff.",
    "Admit that You reviewed the Registry Information in the Report before taking the Adverse Action.",
    "Admit that You considered the Registry Information in deciding to take the Adverse Action.",
    "Admit that the Registry Information was a reason for the Adverse Action.",
    "Admit that You extended Plaintiff a conditional offer of employment before March 10, 2025.",
    "Admit that You withdrew Plaintiff's conditional offer of employment on or about March 19, 2025.",
    "Admit that the adverse-action notice sent to Plaintiff on or about March 19, 2025 referenced the National Sex Offender Public Website.",
    "Admit that the adverse-action notice sent to Plaintiff on or about March 19, 2025 referenced the California sex offender website.",
    "Admit that the adverse-action notice sent to Plaintiff on or about March 19, 2025 did not state that any answer on Plaintiff's application was a reason for the Adverse Action.",
    "Admit that, before March 19, 2025, You did not inform Plaintiff in writing that You believed any answer on his application was false.",
    "Admit that the position for which Plaintiff was considered in 2025 did not involve supervising minors.",
    "Admit that the position for which Plaintiff was considered in 2025 did not involve unsupervised contact with minors.",
    "Admit that the position for which Plaintiff was considered in 2025 did not involve caring for elder or dependent adults.",
    "Admit that, before taking the Adverse Action, You did not identify any specific person at risk whom the Adverse Action was intended to protect.",
    "Admit that no federal, state, or local law required You to conduct a criminal background check for the position for which Plaintiff was considered in 2025.",
    "Admit that no federal, state, or local law required You to search any sex offender registry for the position for which Plaintiff was considered in 2025.",
    "Admit that You employed Plaintiff at least once before January 2025.",
    "Admit that You conducted, or caused First Advantage to conduct, a background check on Plaintiff in connection with at least one period of Prior Employment.",
    "Admit that You hired Plaintiff at least once before January 2025 after receiving a background report about him.",
    "Admit that You did not send Plaintiff a copy of the Report within three business days after You received it.",
    "Admit that You have no written policy, in effect between January 1, 2024 and March 31, 2025, that prohibits using Registry Information in hiring decisions for positions in California.",
    "Admit that You possess personnel, recruiting, or onboarding records for Plaintiff other than those for the application that ended in March 2025.",
    "Admit that Plaintiff's complaint, filed in San Joaquin County Superior Court before removal, demanded a jury trial on all issues.",
    "Admit that Plaintiff has not consented to a trial without a jury in this action.",
    "Admit that, before the Adverse Action, You did not ask Plaintiff to explain or correct any application answer that You now contend was a misrepresentation.",
    "Admit that You possess no document created before March 19, 2025 stating that an answer on Plaintiff's application, standing alone, required rejecting him.",
    "Admit that You first contended that Plaintiff's application contained a material misrepresentation after Plaintiff filed this action.",
    "Admit that no law categorically prohibited You from hiring Plaintiff for the position for which he was considered in 2025.",
    "Admit that the position for which Plaintiff was considered in 2025 did not require him to work directly and in an unaccompanied setting with minor children on more than an incidental and occasional basis.",
    "Admit that First Advantage supplied You, with the Report or under its service agreement with You, a notice concerning restrictions on the use of sex offender registry information in employment decisions in California.",
    "Admit that the position for which Plaintiff was considered in 2025 was filled by another person.",
]

RFPS = [
    "All documents concerning each application Plaintiff submitted to You at any time, including the application reflected in the July 17, 2024 confirmation from fedex@paradox.ai and the application You describe as submitted in January 2025, together with all forms Plaintiff completed, including the forms dated on or about January 8, 2025.",
    "Plaintiff's complete personnel, onboarding, and separation files for each period of Prior Employment.",
    "Each Report, in every version and in the form furnished to You, including all attachments, component results, and updates.",
    "All communications between You and First Advantage concerning Plaintiff, including portal messages, emails, adjudication notes, and status updates.",
    "All documents reflecting the adjudication, scoring, or eligibility determination applied to each Report, including any \"client criteria,\" eligibility matrix, or adjudication guideline used.",
    "Each conditional offer of employment, offer letter, or offer communication extended to Plaintiff at any time.",
    "Each pre-adverse action notice and adverse-action notice sent to Plaintiff at any time, with all enclosures, in the form sent, together with any drafts and distribution lists, and documents showing the dates and method of delivery.",
    "All documents You relied on, reviewed, or considered in taking the Adverse Action.",
    "All internal communications (including email, chat, and instant messages) concerning Plaintiff's 2025 application, the Report, or the Adverse Action.",
    "All documents supporting Your contention that Plaintiff's application \"contained material misrepresentations that independently justified the hiring decision\" (ECF No. 10 at 2).",
    "All documents supporting Your Eighth Affirmative Defense (use of information to protect a person at risk).",
    "All policies, procedures, guidelines, and training materials in effect at any time from January 1, 2024 through March 31, 2025 concerning the use of criminal history or Registry Information in hiring decisions for positions in California, including materials on the California Fair Chance Act (Gov. Code § 12952).",
    "All policies, procedures, guidelines, and training materials in effect at any time from January 1, 2024 through March 31, 2025 that refer to California Penal Code section 290.46 or the Megan's Law website.",
    "The portions of each agreement, statement of work, or package configuration between You and First Advantage in effect during 2024 or 2025 that govern the searches ordered for California applicants, any sex offender registry search, adjudication criteria, or compliance with California law. Pricing terms may be redacted.",
    "The job posting, job description, and documents sufficient to show the duties of each position for which Plaintiff applied or was considered in 2024 or 2025.",
    "Documents sufficient to show the hourly wage, expected hours, and benefits of the position for which Plaintiff was considered in 2025.",
    "All applicant-tracking-system records concerning Plaintiff (including Paradox, Workday, and any successor or related system), including status histories, notes, and audit logs.",
    "All disclosure and authorization forms concerning background reports that Plaintiff signed or acknowledged at any time, and all documents showing whether Plaintiff requested a copy of any Report.",
    "Documents sufficient to show the date and time You received each Report.",
    "Documents sufficient to show each First Advantage account, client code, order, or search ID number used for Plaintiff.",
    "Documents sufficient to show the date, scope, and recipients of any litigation hold covering Plaintiff's application files, the Report, or communications with First Advantage.",
    "All documents concerning any background check performed on Plaintiff in connection with any period of Prior Employment.",
    "All documents identified, referred to, or relied on in Your answers to Plaintiff's First Set of Interrogatories.",
    "All written or recorded statements of any witness concerning the facts of this action.",
    "All documents You obtain from any third party, by subpoena or otherwise, concerning Plaintiff or this action.",
    "A native or readable export of Plaintiff's 2025 application, including every question, answer, certification, timestamp, revision, and audit field.",
    "Audit logs showing when, how, and by whom the Report or any component of it was ordered, received, displayed, accessed, downloaded, transmitted, or evaluated.",
    "Each policy, standard, rubric, or instruction in effect from January through March 2025 that defines a material application misrepresentation or prescribes the consequences of one.",
    "All documents showing when You first identified each alleged misrepresentation in Plaintiff's application and what action You took because of it.",
    "All documents comparing or relating any answer on Plaintiff's 2025 application to any answer he gave on an earlier application to FedEx.",
    "Every warning, notice, compliance material, or term that First Advantage supplied to You concerning permissible or prohibited uses of the Report or of sex offender registry information, including California Penal Code section 290.46.",
    "Documents sufficient to show whether, when, and at what pay rate and expected hours the position for which Plaintiff was considered in 2025 was filled, with personal identifiers of any nonparty redacted.",
    "Any insurance agreement under which an insurer may be liable to satisfy all or part of a judgment in this action, or to indemnify or reimburse payments made to satisfy it (Fed. R. Civ. P. 26(a)(1)(A)(iv)).",
]

FA_REQS = [
    "Each consumer report and investigative consumer report concerning Plaintiff that You prepared for, or furnished to, Federal Express Corporation, FedEx Ground Package System, Inc., or any other FedEx entity (together, \"FedEx\") at any time from January 1, 2019 through the present, in every version and in the form furnished, including all component results and updates.",
    "For each report in Request No. 1, all records of each criminal-history and sex offender registry search performed, including: the vendor, database, or website queried (for example, the National Sex Offender Public Website, the California Department of Justice Megan's Law website, or another source); the jurisdiction, query, and search terms used; the retrieval method; the raw result returned; the \"source of record\" information; the date and time retrieved; and the chain of transmission from the source to FedEx.",
    "Order records for each report in Request No. 1, including the package ordered, each component, the requesting FedEx user or account, and the dates ordered and completed.",
    "All records of any adjudication, scoring, or eligibility determination applied to each report in Request No. 1, including the \"client criteria\" or matrix applied and the resulting score.",
    "All communications with FedEx concerning Plaintiff, including portal messages, emails, adjudication notes, and status updates.",
    "Each pre-adverse action and adverse-action notice sent to Plaintiff on behalf of FedEx, with enclosures, and records showing when each was sent and when Plaintiff accessed any portal link.",
    "All disclosure and authorization forms concerning Plaintiff that You received or maintain in connection with any FedEx order, and records of any request by Plaintiff for a copy of a report.",
    "Documents sufficient to show, for the period January 1, 2024 through March 31, 2025, how the search labeled \"National Sex Offender Registry\" or \"National Sex Offender Registry Search - Department of Justice Web Site\" retrieves records of California registrants, including whether it queries the National Sex Offender Public Website, the California Megan's Law website, or a database compiled from either.",
    "Documents sufficient to show the terms of any agreement between You and FedEx in effect during 2024 or 2025 that govern sex offender registry searches for California applicants or compliance with California Penal Code section 290.46.",

    "Audit logs showing when each report in Request No. 1 was ordered, searched, completed, changed, delivered, displayed, accessed, opened, downloaded, or transmitted, including the user or account identifier of each FedEx or First Advantage user involved.",
    "All records of any manual review, quality-control review, identity-matching decision, suppression, dispute, reinvestigation, correction, or update concerning any report in Request No. 1.",
    "Every warning, disclaimer, compliance notice, instruction, or term You supplied to FedEx, with any report in Request No. 1 or under Your service agreement, concerning permissible or prohibited employment use of criminal-history or sex offender registry information, including California Penal Code section 290.46.",
    "Documents sufficient to identify each person or organizational unit at First Advantage that collected, reviewed, approved, transmitted, or maintained any report in Request No. 1.",]


# ----------------------------------------------------------------- rendering

def header(d: PleadingPaper, right: list[tuple[str, bool, bool]], title_lines: list[str]) -> None:
    c = d.c
    y0 = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, y0 - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("EASTERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    for t in title_lines:
        d.write_line(t, bold=True, center=True)
    d.blank_line()


def heading(d: PleadingPaper, text: str) -> None:
    d.ensure_space(4)
    d.write_line(text, bold=True, center=True)
    d.blank_line()


def para(d: PleadingPaper, text: str, first_indent: int = 36) -> None:
    d.write_wrapped(text, first_indent=first_indent)
    d.blank_line()


def numbered(d: PleadingPaper, label: str, items: list[str]) -> None:
    for i, text in enumerate(items, 1):
        d.ensure_space(3)
        d.write_line(f"{label} NO. {i}:", bold=True)
        d.write_wrapped(text, first_indent=36)
        d.blank_line()


def signature(d: PleadingPaper, date: str, stamp: bool) -> None:
    d.ensure_space(11)
    d.write_line(f"Dated: {date}")
    d.blank_line()
    d.write_respectfully_submitted()
    if stamp:
        d.draw_signature_image(SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1],
                               SIG_LINE, width=220, x_offset=15)
    else:
        d.blank_line()
        d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def right_block(title: list[str], extra: list[str]) -> list[tuple[str, bool, bool]]:
    rows = [(f"Case No. {CASE_NO}", False, False), ("", False, False)]
    rows += [(t, True, False) for t in title]
    rows += [("", False, False)] + [(t, False, False) for t in extra]
    rows += [("", False, False), ("Magistrate Judge: Hon. Sean C. Riordan", False, False),
             ("District Judge: Hon. Dale A. Drozd", False, False)]
    return rows


SET_ONE = ["Propounding Party: Plaintiff", "Responding Party: Defendant", "  Federal Express Corporation", "Set No.: One"]


def definitions(d: PleadingPaper) -> None:
    heading(d, "DEFINITIONS")
    for t in DEFINITIONS:
        para(d, t, first_indent=0)


def pos(out: Path, doc_title: str, args) -> Path:
    fields = ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=["FEDERAL EXPRESS CORPORATION; and", "DOES 1 through 10, inclusive"],
        defendant_role="Defendants",
        case_number=CASE_NO,
        district_line=DISTRICT_EDCAL,
        title="PROOF OF SERVICE",
        service_date=args.date,
        document_title=doc_title,
        mailing_location=args.mailed_from,
        recipients=list(SERVICE_ADDRESSEES),
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=args.stamp_signature,
        by_email=args.by_email,
    )
    return build_proof_of_service(out, fields)


def finish(d: PleadingPaper, body_path: Path, final: Path, pos_title: str | None, args, tmp: Path) -> None:
    d.save()
    parts = [body_path]
    if pos_title:
        parts.append(pos(tmp / (final.stem + " POS.pdf"), pos_title, args))
    assemble(parts, final)
    print(f"wrote {final.relative_to(ROOT)}")


# ----------------------------------------------------------------- documents

def build_rogs(args, tmp):
    final = OUT_DIR / "01 - Plaintiff First Set of Interrogatories to FedEx (Set One).pdf"
    body = tmp / "01.pdf"
    d = PleadingPaper(str(body), doc_title_footer=f"PLAINTIFF'S FIRST SET OF INTERROGATORIES -- {CAPTION_NAME}")
    header(d, right_block(["PLAINTIFF'S FIRST SET OF", "INTERROGATORIES TO", "DEFENDANT FEDERAL EXPRESS", "CORPORATION"], SET_ONE + ["(Fed. R. Civ. P. 26, 33)"]),
           ["PLAINTIFF'S FIRST SET OF INTERROGATORIES", "TO DEFENDANT FEDERAL EXPRESS CORPORATION"])
    para(d, "TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:", first_indent=0)
    para(d, "Under Federal Rules of Civil Procedure 26 and 33, Plaintiff Brendan Ngehsi Newanforbi requests that Defendant Federal Express Corporation answer each interrogatory below separately and fully, in writing and under oath, and serve its answers on Plaintiff within thirty (30) days after service (plus three days if service is by mail under Rule 6(d)).")
    heading(d, "INSTRUCTIONS")
    for t in [
        "1. Answer each interrogatory on the basis of all information available to You, including information held by Your employees, affiliates, agents, and vendors. If You cannot answer fully, answer to the extent possible and explain why.",
        "2. Any objection must be stated with specificity (Rule 33(b)(4)). If You object to part of an interrogatory, answer the rest.",
        "3. If You answer by reference to business records under Rule 33(d), identify the records by Bates number in enough detail for Plaintiff to locate them as readily as You could.",
        "4. If You withhold information on a claim of privilege, describe it as required by Rule 26(b)(5)(A).",
        "5. These interrogatories are continuing. Supplement Your answers as required by Rule 26(e).",
    ]:
        para(d, t, first_indent=0)
    definitions(d)
    heading(d, "INTERROGATORIES")
    numbered(d, "INTERROGATORY", ROGS)
    signature(d, args.date, args.stamp_signature)
    finish(d, body, final, "Plaintiff's First Set of Interrogatories to Defendant FedEx (Set One)", args, tmp)


def build_rfas(args, tmp):
    final = OUT_DIR / "02 - Plaintiff First Set of Requests for Admission to FedEx (Set One).pdf"
    body = tmp / "02.pdf"
    d = PleadingPaper(str(body), doc_title_footer=f"PLAINTIFF'S FIRST SET OF REQUESTS FOR ADMISSION -- {CAPTION_NAME}")
    header(d, right_block(["PLAINTIFF'S FIRST SET OF", "REQUESTS FOR ADMISSION TO", "DEFENDANT FEDERAL EXPRESS", "CORPORATION"], SET_ONE + ["(Fed. R. Civ. P. 26, 36)"]),
           ["PLAINTIFF'S FIRST SET OF REQUESTS FOR ADMISSION", "TO DEFENDANT FEDERAL EXPRESS CORPORATION"])
    para(d, "TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:", first_indent=0)
    para(d, "Under Federal Rules of Civil Procedure 26 and 36, Plaintiff Brendan Ngehsi Newanforbi requests that Defendant Federal Express Corporation admit the truth of each matter below, in writing, within thirty (30) days after service (plus three days if service is by mail under Rule 6(d)).")
    para(d, "<<b:Notice under Rule 36(a)(3):>> each matter is admitted unless, within the time allowed, You serve a written answer or objection addressed to it, signed by You or Your attorney.")
    heading(d, "INSTRUCTIONS")
    for t in [
        "1. If You do not admit a matter, specifically deny it or state in detail why You cannot truthfully admit or deny it (Rule 36(a)(4)). A denial must fairly respond to the substance of the matter; when good faith requires, specify the part admitted and qualify or deny only the rest.",
        "2. You may assert lack of knowledge or information as a reason for failing to admit or deny only if You state that You have made reasonable inquiry and that the information You know or can readily obtain is insufficient.",
        "3. The Definitions below are the same as those in Plaintiff's First Set of Interrogatories, served with these requests.",
    ]:
        para(d, t, first_indent=0)
    definitions(d)
    heading(d, "REQUESTS FOR ADMISSION")
    numbered(d, "REQUEST FOR ADMISSION", RFAS)
    signature(d, args.date, args.stamp_signature)
    finish(d, body, final, "Plaintiff's First Set of Requests for Admission to Defendant FedEx (Set One)", args, tmp)


def build_rfps(args, tmp):
    final = OUT_DIR / "03 - Plaintiff First Set of Requests for Production to FedEx (Set One).pdf"
    body = tmp / "03.pdf"
    d = PleadingPaper(str(body), doc_title_footer=f"PLAINTIFF'S FIRST SET OF REQUESTS FOR PRODUCTION -- {CAPTION_NAME}")
    header(d, right_block(["PLAINTIFF'S FIRST SET OF", "REQUESTS FOR PRODUCTION OF", "DOCUMENTS TO DEFENDANT", "FEDERAL EXPRESS CORPORATION"], SET_ONE + ["(Fed. R. Civ. P. 26, 34)"]),
           ["PLAINTIFF'S FIRST SET OF REQUESTS FOR PRODUCTION OF", "DOCUMENTS TO DEFENDANT FEDERAL EXPRESS CORPORATION"])
    para(d, "TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:", first_indent=0)
    para(d, "Under Federal Rules of Civil Procedure 26 and 34, Plaintiff Brendan Ngehsi Newanforbi requests that Defendant Federal Express Corporation serve a written response within thirty (30) days after service (plus three days if service is by mail under Rule 6(d)), and produce the documents requested below at that time or by another reasonable date stated in the response.")
    para(d, "<<b:Place and manner of production:>> by delivery of copies to Plaintiff at 1455 Cat Tail Drive, Stockton, California 95204, or by secure electronic delivery to bnn.cdl@gmail.com.")
    heading(d, "INSTRUCTIONS")
    for t in [
        "1. Produce documents in Your possession, custody, or control, including documents held by Your affiliates, agents, and vendors (including First Advantage) that You have the legal right or practical ability to obtain.",
        "2. Produce electronically stored information as searchable PDF, except that spreadsheets, audit logs, and applicant-tracking-system data should be produced in native or other reasonably usable form with metadata showing dates and authors (Rule 34(b)(1)(C), (b)(2)(E)).",
        "3. Organize and label documents to correspond to the requests, or produce them as kept in the usual course of business (Rule 34(b)(2)(E)(i)). Bates-number each page.",
        "4. For each request, state whether responsive documents are being withheld on the basis of any objection (Rule 34(b)(2)(C)). For any document withheld as privileged, serve the information required by Rule 26(b)(5)(A) with the production, not at the close of discovery.",
        "5. If a responsive document no longer exists, identify it and explain the circumstances of its loss or destruction.",
        "6. The Definitions below are the same as those in Plaintiff's First Set of Interrogatories, served with these requests.",
    ]:
        para(d, t, first_indent=0)
    definitions(d)
    heading(d, "DOCUMENTS REQUESTED")
    numbered(d, "REQUEST FOR PRODUCTION", RFPS)
    signature(d, args.date, args.stamp_signature)
    finish(d, body, final, "Plaintiff's First Set of Requests for Production to Defendant FedEx (Set One)", args, tmp)


def build_attachments(args, tmp):
    final = OUT_DIR / "04 - Rule 45 Subpoena Attachments A and B - First Advantage.pdf"
    body = tmp / "04.pdf"
    d = PleadingPaper(str(body), doc_title_footer=f"ATTACHMENTS A AND B TO SUBPOENA (FIRST ADVANTAGE) -- {CAPTION_NAME}")
    header(d, right_block(["ATTACHMENT A TO SUBPOENA", "TO PRODUCE DOCUMENTS", "(FIRST ADVANTAGE BACKGROUND", "SERVICES CORP.)"], ["(Fed. R. Civ. P. 45)", "Attachment B: Declaration of", "  Custodian of Records"]),
           ["ATTACHMENT A TO SUBPOENA TO PRODUCE DOCUMENTS", "FIRST ADVANTAGE BACKGROUND SERVICES CORP."])
    heading(d, "DEFINITIONS")
    for t in [
        "1. \"You\" and \"Your\" mean First Advantage Background Services Corp. and its affiliates that prepared or furnished background reports to FedEx.",
        "2. \"Plaintiff\" means Brendan Ngehsi Newanforbi, including under any variation of that name (for example, Brendan Ngwa Nforbi, Brendan Ngwanforbi, Brendan Ngehsi Ngwa-Nforbi, or Ngwa-Nforbi).",
        "3. \"Document\" has the broadest meaning allowed by Fed. R. Civ. P. 34(a)(1)(A) and includes electronically stored information.",
    ]:
        para(d, t, first_indent=0)
    heading(d, "CONSUMER IDENTIFICATION")
    for t in [
        "To help You locate the records, the consumer and screening are: Brendan Ngehsi Newanforbi (also Brendan Ngwa Nforbi, Brendan Ngwanforbi, Brendan Ngehsi Ngwa-Nforbi); email bnn.cdl@gmail.com; client FEDEX GROUND HR / Federal Express Corporation; application on or about January 8, 2025; pre-adverse action notice on or about March 10, 2025; final adverse action on or about March 19, 2025.",
        "Plaintiff's date of birth and other identifiers are omitted because this attachment is served on the parties. Plaintiff will provide them to First Advantage directly through a secure channel on request. No records concerning any other consumer are requested.",
    ]:
        para(d, t, first_indent=0)
    heading(d, "INSTRUCTIONS")
    for t in [
        "1. Produce responsive documents in Your possession, custody, or control, as kept in the ordinary course of business. Produce electronically stored information as searchable PDF, and spreadsheets, databases, structured exports, and audit logs in reasonably usable native form, preserving metadata showing creation, modification, access, transmission, and status-change dates.",
        "2. <<b:No appearance is required.>> The place of compliance stated on the subpoena is Your office at 1 Concourse Parkway NE, Suite 200, Atlanta, Georgia 30328. You may instead comply by mailing or securely transmitting true copies of the documents, with the completed Declaration of Custodian of Records (Attachment B), to: Brendan Ngehsi Newanforbi, 1455 Cat Tail Drive, Stockton, California 95204; bnn.cdl@gmail.com, on or before the date stated on the subpoena.",
        "2A. If any responsive record no longer exists, produce any retention, deletion, purge, or destruction record sufficient to identify what was removed and when.",
        "3. Plaintiff is the consumer to whom these records relate. Plaintiff consents to Your disclosure of his own consumer file and report records to him for purposes of this action.",
        "4. If You withhold any document on a claim of privilege or protection, provide the information required by Fed. R. Civ. P. 45(e)(2)(A).",
        "5. Plaintiff will reimburse the reasonable copying costs of production on request. Please contact Plaintiff at bnn.cdl@gmail.com with any question about the scope or format of production before the compliance date.",
    ]:
        para(d, t, first_indent=0)
    heading(d, "DOCUMENTS TO BE PRODUCED")
    numbered(d, "REQUEST", FA_REQS)
    # Attachment B on its own page
    d.start_new_page()
    heading(d, "ATTACHMENT B")
    d.write_line("DECLARATION OF CUSTODIAN OF RECORDS", bold=True, center=True)
    d.write_line("(Fed. R. Evid. 803(6), 902(11), 902(13))", center=True)
    d.blank_line()
    para(d, f"<<i:Newanforbi v. Federal Express Corporation>>, E.D. Cal. No. {CASE_NO}", first_indent=0)
    para(d, "I, ____________________________________, declare:", first_indent=0)
    para(d, "1. I am employed by First Advantage Background Services Corp. as ____________________________, and I am a custodian of records, or am otherwise qualified by my position, to make this declaration.")
    para(d, "2. The records produced with this declaration, consisting of ________ pages (identified as ______________________), are true copies of records that were (a) made at or near the time of the acts, events, or conditions they record, by, or from information transmitted by, someone with knowledge; (b) kept in the course of a regularly conducted activity of First Advantage; and (c) made as a regular practice of that activity. To the extent the records are electronic, they were generated by an electronic process or system that produces an accurate result, and any copies were made by a process of digital identification that accurately reproduces the originals.")
    para(d, "3. [  ] A diligent search was made, and no records responsive to Request No(s). ______________ were found.")
    d.ensure_space(14)  # keep the declaration, date, and custodian signature together
    para(d, "I declare under penalty of perjury under the laws of the United States of America that the foregoing is true and correct.")
    para(d, "Executed on ______________, 20___, at ______________________.", first_indent=0)
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("Signature", right=True, right_margin_offset=20)
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("Printed name and title", right=True, right_margin_offset=20)
    finish(d, body, final, None, args, tmp)


def build_notice(args, tmp):
    final = OUT_DIR / "05 - Rule 45(a)(4) Notice of Subpoena to FedEx.pdf"
    body = tmp / "05.pdf"
    d = PleadingPaper(str(body), doc_title_footer=f"NOTICE OF SUBPOENA TO NONPARTY FIRST ADVANTAGE -- {CAPTION_NAME}")
    header(d, right_block(["NOTICE OF SUBPOENA TO", "PRODUCE DOCUMENTS TO", "NONPARTY FIRST ADVANTAGE", "BACKGROUND SERVICES CORP."], ["(Fed. R. Civ. P. 45(a)(4))"]),
           ["NOTICE OF SUBPOENA TO PRODUCE DOCUMENTS TO NONPARTY", "FIRST ADVANTAGE BACKGROUND SERVICES CORP."])
    para(d, "TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:", first_indent=0)
    para(d, "PLEASE TAKE NOTICE that, under Federal Rule of Civil Procedure 45(a)(4), Plaintiff Brendan Ngehsi Newanforbi will serve the attached Subpoena to Produce Documents, Information, or Objects (Form AO 88B), with its Attachments A and B, on nonparty First Advantage Background Services Corp. The subpoena commands production of the documents described in Attachment A on or before the date stated on the subpoena, at First Advantage\'s Atlanta, Georgia office or, at First Advantage\'s option, by mail or secure electronic delivery to Plaintiff at 1455 Cat Tail Drive, Stockton, California 95204. No appearance or deposition is commanded.")
    para(d, "A copy of the subpoena and its attachments is served with this notice, before the subpoena is served on the nonparty. Plaintiff will make any documents produced in response available to Defendant for copying on request.")
    signature(d, args.date, args.stamp_signature)
    finish(d, body, final, "Rule 45(a)(4) Notice of Subpoena to First Advantage, with Subpoena and Attachments", args, tmp)


# ----------------------------------------------------------------- subpoena issuance

FORMS_DIR = OUT_DIR / "forms"
AO88B_BLANK = FORMS_DIR / "AO88B (Rev. 02-14) Subpoena to Produce Documents - blank.pdf"
FA_NAME = "First Advantage Background Services Corp."
FA_PLACE = ("First Advantage, 1 Concourse Pkwy NE, Ste 200, Atlanta, GA 30328 "
            "(or by mail/email to Plaintiff per Attachment A)")


def build_ao88b(args, tmp):
    """Proposed AO 88B for the Clerk to issue (Rule 45(a)(3)). Unsigned: the
    Clerk signs. The Clerk may instead issue a signed blank; fill it the same way."""
    from pypdf import PdfReader, PdfWriter
    final = OUT_DIR / "08 - Proposed AO 88B Subpoena to First Advantage (for Clerk issuance).pdf"
    reader = PdfReader(str(AO88B_BLANK))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    values = {
        "District Information": "         Eastern District of California",
        "Plaintiff": "BRENDAN NGEHSI NEWANFORBI",
        "Defendant": "FEDERAL EXPRESS CORPORATION, et al.",
        "Case_Num": CASE_NO,
        "Subpoena_To": f"{FA_NAME}\nc/o its registered agent for service of process",
        "check_1": "/Production",
        "Sampling_Material": "See Attachment A (Document Requests Nos. 1-13 and Instructions), attached and incorporated. Attachment B (Declaration of Custodian of Records) may be returned with the production.",
        "Production_Place": FA_PLACE,
        "Production_DateTime": args.subpoena_compliance,
        "Attorney_Information": "1455 Cat Tail Dr., Stockton, CA 95204; bnn.cdl@gmail.com; (209) 801-4442",
        "Name.Party.1": "Plaintiff (pro se)",
        "Name.Party.2": "Brendan Ngehsi Newanforbi, Plaintiff, In Propria Persona",
    }
    for page in writer.pages:
        writer.update_page_form_field_values(page, values, auto_regenerate=False)
    writer.set_need_appearances_writer(True)
    with open(final, "wb") as f:
        writer.write(f)
    print(f"wrote {final.relative_to(ROOT)}")


def build_clerk_letter(args, tmp):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer
    final = OUT_DIR / "07 - Request to Clerk for Issuance of AO 88B Subpoena.pdf"
    st = ParagraphStyle("b", fontName="Times-Roman", fontSize=12, leading=16, spaceAfter=10)
    bold = ParagraphStyle("h", parent=st, fontName="Times-Bold")
    story = [Paragraph("Brendan Ngehsi Newanforbi<br/>Plaintiff, In Propria Persona<br/>1455 Cat Tail Drive<br/>Stockton, CA 95204<br/>(209) 801-4442 | bnn.cdl@gmail.com", st),
             Spacer(1, 6), Paragraph(args.date, st), Spacer(1, 6),
             Paragraph("Clerk of Court<br/>United States District Court, Eastern District of California<br/>Robert T. Matsui United States Courthouse<br/>501 I Street, Room 4-200<br/>Sacramento, CA 95814", st),
             Spacer(1, 6),
             Paragraph(f"Re: <i>Newanforbi v. Federal Express Corporation</i>, No. {CASE_NO} &mdash; Request for Issuance of Subpoena (Fed. R. Civ. P. 45(a)(3))", bold),
             Paragraph("Dear Clerk:", st),
             Paragraph("I am the self-represented Plaintiff in this action. Under Federal Rule of Civil Procedure 45(a)(3), I respectfully request that the Clerk issue the enclosed Subpoena to Produce Documents, Information, or Objects (Form AO 88B) directed to nonparty First Advantage Background Services Corp.", st),
             Paragraph("The subpoena commands the production of documents only. It does not command attendance at a deposition, hearing, or trial. The requested documents are listed in the enclosed Attachment A. The parties held their Rule 26(f) conference on September 25, 2026, so discovery is open.", st),
             Paragraph("If the Clerk's practice is to issue a subpoena signed but otherwise blank, please sign and return the enclosed AO 88B, and I will complete it before service. I have enclosed a self-addressed, stamped envelope for its return. Before serving the subpoena, I will serve notice and a copy on Defendant's counsel as Rule 45(a)(4) requires.", st),
             Paragraph("Thank you for your assistance.", st),
             Paragraph("Respectfully,", st)]
    if args.stamp_signature:
        w = 180
        h = w * SIGNATURE_NATIVE_PX[1] / SIGNATURE_NATIVE_PX[0]
        img = Image(SIGNATURE_PATH, width=w, height=h)
        img.hAlign = "LEFT"
        story.append(img)
    else:
        story.append(Spacer(1, 36))
    story += [Paragraph("___________________________________<br/>Brendan Ngehsi Newanforbi<br/>Plaintiff, In Propria Persona", st),
              Spacer(1, 8),
              Paragraph("Enclosures: (1) proposed AO 88B subpoena; (2) Attachment A and Attachment B; (3) self-addressed, stamped return envelope.", st)]
    SimpleDocTemplate(str(final), pagesize=letter, leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72).build(story)
    print(f"wrote {final.relative_to(ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default="September 25, 2026")
    ap.add_argument("--mailed-from", default="Stockton, California")
    ap.add_argument("--by-email", action="store_true", help="proofs recite email service (only with written consent)")
    ap.add_argument("--stamp-signature", action="store_true", help="apply the canonical signature stamp")
    ap.add_argument("--subpoena-compliance", default="11/02/2026 10:00 a.m. ET", help="AO 88B production date/time")
    args = ap.parse_args()
    if args.stamp_signature and not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for fn in (build_rogs, build_rfas, build_rfps, build_attachments, build_notice):
            fn(args, tmp)
        build_clerk_letter(args, tmp)
        build_ao88b(args, tmp)


if __name__ == "__main__":
    main()
