#!/usr/bin/env python3
"""Matter 25 -- Plaintiff's Status Report (Dkt. 8).

Newanforbi v. Federal Express Corporation, USDC E.D. Cal.
No. 2:26-cv-02881-DAD-SCR.

Dkt. 8 (dated Sep. 4; filed Sep. 8) sets a Zoom status (pretrial scheduling)
conference for Thursday, October 8, 2026, 11:00 a.m., and requires each party
to file a status report not later than 14 days before (September 24). Because
Plaintiff is pro se, the matter is referred under E.D. Cal. L.R. 302(c)(21).

Plaintiff's individual report under Dkt. 8. It does not move any
court-set date.

    python3 internal/scripts/matter25-status-report.py \\
        [--date "September 14, 2026"] [--mailed-from "Milpitas, California"]
"""

from __future__ import annotations

import argparse
import shutil
import sys
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
OUT_DIR = ROOT / "internal/public/documents/matter-25"
DEFAULT_OUT = OUT_DIR / (
    "Plaintiff's Status Report (E.D. Cal. 2-26-cv-02881) (Sep 14 2026).pdf"
)
DEFAULT_POS_OUT = OUT_DIR / (
    "Proof of Service - Plaintiff's Status Report "
    "(E.D. Cal. 2-26-cv-02881) (Sep 14 2026).pdf"
)

DEFAULT_EXEC_DATE = "September 14, 2026"
DEFAULT_SIGNED_CITY = "Milpitas, California"
DEFAULT_MAILED_FROM = "Milpitas, California"
ARTIFACTS_DIR = Path("/opt/cursor/artifacts")
FOOTER = (
    "PLAINTIFF'S STATUS REPORT -- "
    "NEWANFORBI v. FEDERAL EXPRESS CORPORATION"
)

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "EASTERN DISTRICT OF CALIFORNIA"

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

CAPTION_RIGHT = [
    ("Case No. 2:26-cv-02881-DAD-SCR", False, False),
    ("", False, False),
    ("PLAINTIFF'S STATUS REPORT", True, False),
    ("(Fed. R. Civ. P. 16, 26(f);", False, False),
    ("E.D. Cal. L.R. 240;", False, False),
    ("Dkt. 8)", False, False),
    ("", False, False),
    ("Status Conference:", False, False),
    ("October 8, 2026, 11:00 a.m.", False, False),
    ("Zoom (dial-in to follow)", False, False),
    ("Judge: Hon. Sean C. Riordan", False, False),
    ("District Judge: Hon. Dale A. Drozd", False, False),
    ("", False, False),
    ("Action filed: July 15, 2026", False, False),
    ("Removed: August 24, 2026", False, False),
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


CONTENT = [
    ("PARA",
     "TO THE HONORABLE COURT, AND TO DEFENDANT FEDERAL EXPRESS "
     "CORPORATION AND ITS ATTORNEY OF RECORD:"),

    ("PARA",
     "Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, "
     "submits this Status Report under Federal Rules of Civil Procedure 16 "
     "and 26(f), Eastern District Local Rule 240, and the Order Setting "
     "Status (Pretrial Scheduling) Conference (Dkt. 8, dated September 4, "
     "2026; filed September 8, 2026). Dkt. 8 directs each party to file a "
     "separate report not later than fourteen days before the October 8, "
     "2026 conference. This is Plaintiff's report."),

    ("HEADER", "I.\nINTRODUCTION"),

    ("PARA",
     "Defendant answered on August 31, 2026 (Dkt. 4). There is no pending "
     "motion to dismiss. The case is referred to Magistrate Judge Sean C. "
     "Riordan for pretrial proceedings under Local Rule 302(c)(21) because "
     "Plaintiff is pro se. The Status (Pretrial Scheduling) Conference is "
     "set for Thursday, October 8, 2026, at 11:00 a.m., by Zoom. Plaintiff "
     "will appear. Plaintiff understands the courtroom deputy will send "
     "the dial-in about one week before."),

    ("PARA",
     "Plaintiff is available to confer under Rule 26(f) and Local Rule "
     "240(b) by telephone or Zoom this week, before the September 24 "
     "filing deadline. As of this writing Defendant has not proposed a "
     "conference date or a joint report. If the parties reach a joint "
     "plan before September 24, Plaintiff will supplement. Until then, "
     "this report is Plaintiff's proposed plan. Written email alone is "
     "not a substitute for a live conference if Defendant will hold one."),

    ("HEADER",
     "II.\nSUMMARY OF CLAIMS AND LEGAL THEORIES"),

    ("PARA",
     "This is a failure-to-hire case. Plaintiff applied for work in "
     "Defendant's California delivery and package-handling operations. "
     "Defendant engaged First Advantage to run a pre-employment "
     "background check for \"FEDEX GROUND HR.\" On March 10, 2025, "
     "First Advantage sent a pre-adverse notice. After a series of "
     "reminders, First Advantage sent a final adverse-action notice on "
     "March 19, 2025, confirming Defendant had denied employment."),

    ("PARA",
     "Plaintiff's records include a July 17, 2024 Paradox confirmation "
     "that the online application was completed. Defendant's Answer "
     "describes a January 2025 package-handler application and background "
     "check. Discovery will resolve the timeline. Plaintiff does not "
     "abandon either date."),

    ("PARA",
     "The operative pleading is the verified Complaint filed July 15, "
     "2026, in San Joaquin Superior Court, No. STK-CV-UWT-2026-0009118, "
     "and removed here on August 24, 2026. It alleges six counts: "
     "(1) Penal Code section 290.46(j)(2)(E) (unlawful employment use of "
     "Megan's Law website information); (2) failure to hire in violation "
     "of public policy; (3) Investigative Consumer Reporting Agencies "
     "Act, Civil Code section 1786 et seq.; (4) invasion of privacy "
     "(Cal. Const., art. I, section 1); (5) negligence per se; and "
     "(6) Business and Professions Code section 17200. Plaintiff "
     "demanded a jury."),

    ("PARA",
     "The Answer (Dkt. 4) admits that Defendant engaged First Advantage; "
     "that a report was provided to Defendant on or before March 10, "
     "2025; that pre-adverse notice issued on or about that date; that "
     "Defendant took adverse action on or about March 19, 2025, and "
     "withdrew a conditional offer; that the adverse-action letter "
     "referenced NSOPW and the California sex-offender website and "
     "identified a Penal Code section 220(a)(1) conviction; and that "
     "the First Advantage report identified Plaintiff as a registrant "
     "on California's sex-offender registry in connection with that "
     "conviction. Defendant denies that any use was unlawful and "
     "pleads forty-three affirmative defenses, including an alleged "
     "independent basis and unclean hands from employment forms, and "
     "a section 290.46(j)(1) \"persons at risk\" theory. The fight is "
     "use and lawfulness, not whether the report named the registry."),

    ("HEADER", "III.\nSERVICE"),

    ("PARA",
     "Service is complete. The Los Angeles County Sheriff served "
     "Defendant's registered agent, C T Corporation System, 330 North "
     "Brand Boulevard, Suite 700, Glendale, California, on July 24, "
     "2026. Defendant removed on August 24, 2026, and answered on "
     "August 31, 2026. There are no unserved named defendants. DOES 1 "
     "through 10 remain unnamed. There are no cross-defendants."),

    ("HEADER", "IV.\nJOINDER OF ADDITIONAL PARTIES"),

    ("PARA",
     "Plaintiff does not presently move to add a party. First Advantage "
     "is the consumer-reporting agency that generated the notices and "
     "the report. Plaintiff reserves the right to amend to name First "
     "Advantage, or to identify a Doe, after the report and the "
     "decision-file are produced. Plaintiff does not waive joinder by "
     "filing this report. Plaintiff does not ask the Court to stay this "
     "action while any other case proceeds."),

    ("HEADER", "V.\nAMENDMENT OF THE PLEADINGS"),

    ("PARA",
     "Defendant has answered. Amendment now requires written consent or "
     "leave of court under Rule 15(a)(2). Plaintiff contemplates "
     "amendment after initial document production if the report, the "
     "application file, or the decision-file requires a more definite "
     "statement of dates, the decisionmaker, or a named Doe. Plaintiff "
     "does not presently intend to drop a claim. Plaintiff proposes "
     "December 18, 2026, as the last date to amend or join parties "
     "without a showing of good cause. That date is after initial "
     "disclosures and the first wave of documents. It does not compress "
     "Plaintiff's time, and it is a date certain."),

    ("HEADER", "VI.\nJURISDICTION AND VENUE"),

    ("PARA",
     "Subject-matter jurisdiction is diversity, 28 U.S.C. sections 1332 "
     "and 1441. Defendant removed on that basis. Plaintiff does not "
     "seek remand. Personal jurisdiction is not disputed. Venue is "
     "proper in this District because the "
     "application, screening, and denial concerned California employment "
     "and the state action was filed in San Joaquin County. Local Rule "
     "120(d). Plaintiff is not aware of a venue motion."),

    ("PARA",
     "Defendant's certificates of service have used the address "
     "bnn.cdla@gmail.com. The correct address is bnn.cdl@gmail.com. "
     "Mail service to 1455 Cat Tail Drive, Stockton, California 95204, "
     "has reached Plaintiff. Please use the correct email going "
     "forward."),

    ("HEADER", "VII.\nRULE 26(f) DISCOVERY PLAN"),

    ("SUBHEAD", "A.  Initial disclosures"),

    ("PARA",
     "No change to the form of Rule 26(a)(1) disclosures is needed. "
     "Plaintiff will serve initial disclosures on October 22, 2026 -- "
     "fourteen days after the conference -- and asks that Defendant "
     "serve the same day. That is a date certain. Plaintiff does not "
     "agree to delay disclosures until a later motion, a later "
     "conference, or a date that runs from an event that has not "
     "occurred. A further discovery conference should be set only if a "
     "dispute remains after the parties confer live."),

    ("SUBHEAD", "B.  Subjects, phasing, and cutoff"),

    ("PARA",
     "Discovery should not be phased so that Defendant's documents wait "
     "on a motion that has not been filed. Defendant answered. "
     "Discovery should proceed now. The subjects include:"),

    ("LIST_ITEM",
     "1.  The First Advantage report provided to Defendant on or before "
     "March 10, 2025, and every communication between Defendant and "
     "First Advantage about Plaintiff;"),

    ("LIST_ITEM",
     "2.  The application file for both the July 17, 2024 Paradox "
     "confirmation and the January 2025 application described in the "
     "Answer, including any conditional offer;"),

    ("LIST_ITEM",
     "3.  The identity of every person who reviewed the report, "
     "recommended denial, or withdrew the offer, and their files;"),

    ("LIST_ITEM",
     "4.  Defendant's policies and training on Penal Code section "
     "290.46, Megan's Law, NSOPW, and the use of registry information "
     "in hiring;"),

    ("LIST_ITEM",
     "5.  The independent-basis and unclean-hands facts Defendant "
     "pleaded, including the January 8, 2025 forms; and"),

    ("LIST_ITEM",
     "6.  ESI in ordinary HR, recruiting, and vendor systems (Paradox, "
     "email, the First Advantage portal, and any applicant-tracking "
     "system)."),

    ("PARA",
     "Plaintiff will take written discovery and a focused set of "
     "depositions (the decisionmaker, a Rule 30(b)(6) witness on "
     "screening policy, and, if needed, a First Advantage custodian). "
     "Plaintiff will serve a Rule 45 subpoena on First Advantage for "
     "the report and the transmittal file. Plaintiff proposes a fact-"
     "discovery cutoff of April 16, 2027. No change to the numerical "
     "limits in Rules 30, 33, and 36 is requested. Plaintiff does not "
     "agree to a discovery stay."),

    ("SUBHEAD", "C.  Experts"),

    ("PARA",
     "Plaintiff may disclose an economist or human-resources expert on "
     "lost opportunity and on screening practice. Plaintiff proposes: "
     "opening expert disclosures under Rule 26(a)(2) on May 14, 2027; "
     "rebuttal disclosures on June 11, 2027; expert discovery closed "
     "June 25, 2027. Those are dates certain. They do not reset from "
     "the conference or from a later order."),

    ("SUBHEAD", "D.  ESI and privilege"),

    ("PARA",
     "Plaintiff has preserved the Paradox confirmation, the First "
     "Advantage notices, and related email, and has not run a "
     "destruction program. Plaintiff asks Defendant to confirm a "
     "litigation hold covering the categories above, including First "
     "Advantage communications and any copy of the report. Plaintiff is "
     "willing to use the District's model ESI order. Privilege logs "
     "should be served with the production they withhold from, not at "
     "the end of discovery."),

    ("HEADER", "VIII.\nANTICIPATED MOTIONS"),

    ("PARA",
     "No Rule 12 motion is pending. Plaintiff does not anticipate "
     "filing one. After document production Plaintiff may move under "
     "Rule 15 if amendment is needed, may move to compel if the report "
     "or the decision-file is withheld, and may move for summary "
     "judgment after the close of fact discovery. Defendant may file a "
     "dispositive motion. Plaintiff proposes that all non-discovery "
     "motions be heard by Thursday, August 12, 2027, at 10:00 a.m., on "
     "Judge Riordan's civil-motion calendar, or the first available "
     "Thursday thereafter. Discovery disputes should use Judge "
     "Riordan's informal two-page letter and telephone conference "
     "before a Local Rule 251 motion."),

    ("PARA",
     "Plaintiff does not invite a delayed Rule 12(c) motion as a "
     "substitute for an answer that is already on file. If Defendant "
     "later moves, Plaintiff will oppose on the schedule the Local "
     "Rules set. This report does not extend any defense clock."),

    ("HEADER", "IX.\nUNNECESSARY PROOF AND RULE 702"),

    ("PARA",
     "The parties should be able to stipulate to authenticity of the "
     "Paradox confirmation, the First Advantage notices, the Sheriff's "
     "proof of service, the Notice of Removal, and the Answer. "
     "Plaintiff will consider a stipulation that the First Advantage "
     "report produced in discovery is authentic. Plaintiff does not "
     "presently anticipate a Rule 702 fight. If one arises, it should "
     "be raised with the expert-disclosure dates, not as a surprise at "
     "trial."),

    ("HEADER", "X.\nFINAL PRETRIAL CONFERENCE"),

    ("PARA",
     "Plaintiff proposes Thursday, September 16, 2027, at 11:00 a.m., "
     "or the first available date the Court sets. That is a date "
     "certain. It does not float from the trial date."),

    ("HEADER", "XI.\nTRIAL"),

    ("PARA",
     "Plaintiff demanded a jury. Plaintiff estimates three to four "
     "court days. Plaintiff proposes Tuesday, October 12, 2027, or the "
     "first available trial date thereafter. The case is an individual "
     "failure-to-hire action. It is not a class action and is not "
     "suitable for the Judicial Panel on Multidistrict Litigation."),

    ("HEADER", "XII.\nSPECIAL PROCEDURES AND 28 U.S.C. § 636(c)"),

    ("PARA",
     "No special master is needed. Plaintiff has consented to proceed "
     "before the assigned magistrate judge for all purposes, including "
     "trial, under 28 U.S.C. section 636(c). Plaintiff mailed that "
     "consent on September 1, 2026. Consent is effective only if "
     "Defendant also consents and both judges accept. Plaintiff does "
     "not know Defendant's position. Docket entries 5, 6, and 7 are "
     "captioned as consent-or-decline filings; Plaintiff has not "
     "assigned those entries to a party. This report does not change "
     "Plaintiff's consent."),

    ("HEADER", "XIII.\nMODIFICATION OF STANDARD PROCEDURES"),

    ("PARA",
     "None, other than the separate-report procedure Dkt. 8 already "
     "set because Plaintiff is pro se. The case is not complex. "
     "Standard limits and a standard scheduling order are enough."),

    ("HEADER", "XIV.\nRELATED CASES"),

    ("PARA",
     "Pending in this District: <<i:Newanforbi v. United Parcel Service, "
     "Inc.>>, No. 2:26-cv-02847-DAD-CKD (Hon. Dale A. Drozd; Hon. "
     "Carolyn K. Delaney). Same plaintiff. Similar Penal Code section "
     "290.46(j)(2)(E) and ICRAA theories. Same background-check vendor "
     "(First Advantage). Different employer, different application, "
     "different adverse-action dates. UPS has a pending Rule 12(b)(6) "
     "motion set for October 7, 2026. Plaintiff discloses the case "
     "under Local Rule 123. Plaintiff does not seek consolidation or "
     "a stay of this action behind that motion. Defendant here has "
     "already answered. Discovery in this case should not wait on "
     "another defendant's pleading motion."),

    ("PARA",
     "No related bankruptcy case is pending in this District. Other "
     "employment-screening actions Plaintiff has filed (including a "
     "resolved San Joaquin action against Pilot Travel Centers LLC, "
     "and pending actions in Alameda Superior Court and the Northern "
     "District of California against different employers and different "
     "vendors) arise from different transactions. They are not pending "
     "in this District and are not offered for assignment or "
     "consolidation."),

    ("HEADER",
     "XV.\nSETTLEMENT CONFERENCE, MAGISTRATE SETTLEMENT JUDGE, AND VDRP"),

    ("PARA",
     "A court-convened settlement conference should be scheduled. "
     "Plaintiff stipulates to the assigned magistrate judge, Hon. Sean "
     "C. Riordan, as settlement judge. Plaintiff prefers Zoom. "
     "Plaintiff will submit a settlement-conference statement to "
     "chambers seven days before the conference, as Judge Riordan's "
     "standing order requires, and will file a notice of submission on "
     "the docket. Plaintiff asks that Defendant appear with a person "
     "who has full settlement authority, and that any insurer with "
     "coverage for this claim be present or available by telephone for "
     "the entire conference."),

    ("PARA",
     "Plaintiff proposes the week of November 16, 2026, or the first "
     "available date thereafter -- after the October 22 disclosures and "
     "with time to exchange the report and the decision-file. That is "
     "a date-certain window. It does not reset from the October 8 "
     "conference. If the Court prefers a later date, Plaintiff asks "
     "that the order name the date."),

    ("PARA",
     "Plaintiff does not stipulate to the District Judge acting as "
     "settlement judge if the District Judge will try the case. The "
     "assigned magistrate is the right settlement judge. That is the "
     "question Dkt. 8 asked. Plaintiff answers it yes."),

    ("PARA",
     "Voluntary Dispute Resolution under Local Rule 271: Plaintiff will "
     "participate if the Court directs it. Plaintiff prefers a "
     "magistrate-judge settlement conference to VDRP. The two are not "
     "substitutes for each other unless the Court says so. This "
     "paragraph is Plaintiff's L.R. 271(d) position."),

    ("HEADER", "XVI.\nOTHER MATTERS"),

    ("PARA",
     "Plaintiff will appear at the October 8 Zoom conference. Please "
     "send the dial-in to bnn.cdl@gmail.com and to (209) 801-4442. "
     "Plaintiff's address of record remains 1455 Cat Tail Drive, "
     "Stockton, California 95204. This report is executed in "
     "Milpitas, California."),

    ("PARA",
     "Plaintiff asks the Court to adopt the dates below in the "
     "scheduling order. Every date is a calendar date. Nothing in this "
     "report continues the October 8 conference, vacates Dkt. 8, or "
     "waives any claim, defense, or right."),

    ("SUBHEAD", "Plaintiff's proposed dates"),

    ("LIST_ITEM",
     "Rule 26(a)(1) initial disclosures:  October 22, 2026"),

    ("LIST_ITEM",
     "Last day to amend or join parties:  December 18, 2026"),

    ("LIST_ITEM",
     "Settlement conference before Judge Riordan:  week of "
     "November 16, 2026, or first available date thereafter"),

    ("LIST_ITEM",
     "Fact-discovery cutoff:  April 16, 2027"),

    ("LIST_ITEM",
     "Opening expert disclosures:  May 14, 2027"),

    ("LIST_ITEM",
     "Rebuttal expert disclosures:  June 11, 2027"),

    ("LIST_ITEM",
     "Expert-discovery cutoff:  June 25, 2027"),

    ("LIST_ITEM",
     "Last day to hear non-discovery motions:  August 12, 2027, "
     "10:00 a.m."),

    ("LIST_ITEM",
     "Final pretrial conference:  September 16, 2027, 11:00 a.m."),

    ("LIST_ITEM",
     "Jury trial (3-4 court days):  October 12, 2027, or first "
     "available date thereafter"),
]


def _header_block(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10,
                         tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("PLAINTIFF'S STATUS REPORT", bold=True, center=True)
    d.write_line("(Fed. R. Civ. P. 16, 26(f); L.R. 240; Dkt. 8)", center=True)
    d.blank_line()


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            d.ensure_space(3)
            d.write_line(text, bold=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=18, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")


def _signature(d: PleadingPaper, exec_date: str, signed_city: str) -> None:
    d.ensure_space(11)
    d.write_line(f"Dated: {exec_date}")
    d.write_line(f"       {signed_city}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=220,
        x_offset=15,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def pos_fields(exec_date: str, mailed_from: str) -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "FEDERAL EXPRESS CORPORATION; and",
            "DOES 1 through 10, inclusive",
        ],
        defendant_role="Defendants",
        case_number="2:26-cv-02881-DAD-SCR",
        district_line=DISTRICT_EDCAL,
        title="PROOF OF SERVICE",
        service_date=exec_date,
        document_title="Plaintiff's Status Report (Dkt. 8)",
        mailing_location=mailed_from,
        recipients=list(SERVICE_ADDRESSEES),
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=True,
    )


def build_report(out: Path, exec_date: str, signed_city: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    _header_block(d)
    _render_body(d, CONTENT)
    _signature(d, exec_date, signed_city)
    d.save()
    return out


def build_pos(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    return build_proof_of_service(out, pos_fields(exec_date, mailed_from))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--date", default=DEFAULT_EXEC_DATE)
    ap.add_argument("--signed-city", default=DEFAULT_SIGNED_CITY)
    ap.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM)
    ap.add_argument("--pos-out", default=str(DEFAULT_POS_OUT))
    ap.add_argument("--skip-pos", action="store_true")
    args = ap.parse_args()
    path = build_report(Path(args.out).resolve(), args.date, args.signed_city)
    if not args.skip_pos:
        pos = build_pos(Path(args.pos_out).resolve(), args.date, args.mailed_from)
        assemble([path, pos], path)
        print(f"Generated status report (POS attached): {path}")
        print(f"Generated proof of service: {pos}")
    else:
        print(f"Generated status report: {path}")
    if ARTIFACTS_DIR.is_dir():
        shutil.copy2(path, ARTIFACTS_DIR / path.name)
        print(f"Copied {path.name} to {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
