#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 40 — Complaint for Damages, Ngwa Nforbi v. Uber Technologies, Inc.

N.D. Cal. federal-question complaint (FCRA lead count; ICRAA and Penal Code
§ 290.46(j) supplemental). Supersedes the September 24, 2026 text draft.

September 23, 2026 rewrite: Section IX pleads Plaintiff's September 16
attempt to complete the First Advantage saliva collection — turned away at
LabCorp-Milpitas in Walgreens at about 3:00 p.m. (no walk-ins, no
appointment on file), First Advantage "Action Required" at 3:05 p.m. (cc
TaskUs), Plaintiff's two-minute call to the Scheduling Center at 3:06 p.m.
with no one reached — and that the schedule expired at 8:49 a.m. Pacific on
September 17, before the site's posted 9:00 a.m. opening.

Paragraphs are numbered at render time. Cross-references use {ref:label}
against a ("P", text, label) entry, so inserting a paragraph never breaks
"realleges paragraphs 1 through N".

    python3 internal/scripts/matter40-uber-complaint.py            # unsigned
    python3 internal/scripts/matter40-uber-complaint.py --execute  # signed
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-40"
    / "Complaint - Ngwa Nforbi v Uber Technologies Inc (N.D. Cal.)"
    " (Sep 23 2026).pdf"
)
DEFAULT_EXEC_DATE = "September 23, 2026"
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"
FOOTER = (
    "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. UBER TECHNOLOGIES, INC., "
    "ET AL. (N.D. Cal.)"
)

# Civil L.R. 3-4(a)(1): name, address, telephone, and email on page one.
PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, California 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("UBER TECHNOLOGIES, INC., a", True, False),
    ("Delaware corporation; TASKUS", True, False),
    ("HOLDINGS, INC., a Delaware", True, False),
    ("corporation; TASKUS USA, LLC, a", True, False),
    ("Delaware limited liability company;", True, False),
    ("and DOES 1 through 20, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. _________________", False, False),
    ("", False, False),
    ("COMPLAINT FOR DAMAGES", True, False),
    ("", False, False),
    ("(1) FCRA, 15 U.S.C. § 1681b(b)(2)(A);", False, False),
    ("(2) ICRAA, Civ. Code §§ 1786.16,", False, False),
    ("      1786.50;", False, False),
    ("(3) FCRA, 15 U.S.C. § 1681b(b)(3)(A);", False, False),
    ("(4) Penal Code § 290.46(j)(2)(E),", False, False),
    ("      (j)(4)(A);", False, False),
    ("(5) ICRAA, Civ. Code §§ 1786.40,", False, False),
    ("      1786.50", False, False),
    ("", False, False),
    ("DEMAND FOR JURY TRIAL", True, False),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

# Kinds: ("H", heading lines) centered bold; ("P", text[, label]) numbered
# paragraph; ("U", text) unnumbered paragraph; ("B", text) bullet;
# ("L", text) prayer item.
CONTENT = [
    ("U", "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, alleges:"),
    ("H", "I.\nNATURE OF THE ACTION"),
    ("P",
     "This action concerns an employment background-screening process for a "
     "written, accepted temporary-employment offer on the Uber AV Teammate "
     "campaign in San Jose, California -- including Defendants' procurement of "
     "a consumer report without the required standalone disclosures, and their "
     "post-report withholding of that accepted assignment after First Advantage "
     "furnished California-registry-sourced information."),
    ("P",
     "On September 14, 2026, TaskUs, LLC issued Plaintiff a written Offer of "
     "Temporary Employment for a Teammate position at $22.00 per hour, "
     "production hours 2PM-11PM, with an anticipated September 23, 2026 start "
     "and an assignment expected to run through on or around December 4, 2026. "
     "Plaintiff accepted the offer."),
    ("P",
     "The WorkDay offer communication identified the assignment as Uber AV "
     "Teammate (SJ: 09/23/2026), requisition R_2608_10812, candidate "
     "C261051599."),
    ("P",
     "The onboarding documents used multiple TaskUs entities. The written "
     "offer named TaskUs, LLC. The United States Background Consent Form "
     "directed screening information to TaskUs USA, LLC. TaskUs Holdings, Inc. "
     "was the counterparty on other onboarding documents and was later "
     "identified by First Advantage as the employment-report recipient."),
    ("P",
     "On September 14, 2026, First Advantage Background Services Corp. "
     "(\"First Advantage\") initiated employment screening through Profile "
     "Advantage, Order WPS-361214148."),
    ("P",
     "The written offer itself stated that \"[t]he Company will provide "
     "required standalone disclosures and obtain required authorizations "
     "before obtaining a consumer or investigative consumer report.\" The "
     "preserved onboarding packet includes a United States Background Consent "
     "Form. That form is a consent/release document authorizing release of "
     "screening information to TaskUs USA, LLC. It is not a standalone "
     "disclosure consisting solely of the disclosure required by 15 U.S.C. "
     "§ 1681b(b)(2)(A), and it does not itself supply the pre-procurement "
     "content required by Civil Code § 1786.16. Plaintiff did not receive, "
     "before procurement, a separate compliant FCRA or ICRAA standalone "
     "disclosure."),
    ("P",
     "At approximately 10:20 a.m. PDT on September 14, the Profile Advantage "
     "portal showed several screening components complete, while the "
     "felony-including-misdemeanor component and PRINSOS, First Advantage's "
     "national sex-offender component, remained In Progress."),
    ("P",
     "At 11:24 a.m. on September 14, TaskUs Talent Acquisition Operations "
     "emailed Plaintiff that his scheduled start was being placed on a "
     "\"standard administrative hold while final onboarding reviews are "
     "completed, including the processing of your background screening "
     "report.\" The email stated that the application remained pending."),
    ("P",
     "The September 14 hold is important context. Plaintiff does not allege "
     "that the hold itself was adverse action based on the completed "
     "California-registry result. The relevant registry component had not yet "
     "been furnished as a completed result."),
    ("P",
     "On September 15, 2026, First Advantage issued a consumer disclosure "
     "stating that public-record information concerning Plaintiff was being "
     "reported to TASKUS HOLDINGS INC USA, Client Account 417722USA."),
    ("P",
     "The enclosed national sex offender registry component of Order "
     "WPS-361214148 states, verbatim: \"SOURCE OF RECORD: CALIFORNIA SEX "
     "OFFENDER REGISTRY. SENTENCE: REGISTERED SEX OFFENDER.\""),
    ("P",
     "Plaintiff therefore alleges as known fact -- not on information and "
     "belief -- that First Advantage furnished employment-screening "
     "information expressly sourced to the California Sex Offender Registry. "
     "That information is information disclosed pursuant to Penal Code "
     "§ 290.46."),
    ("P",
     "First Advantage's September 15 cover letter stated that the reported "
     "results themselves do not constitute acceptance or rejection and that an "
     "employment decision would come from the requesting organization."),
    ("P",
     "First Advantage separately administered a saliva drug-test product for "
     "TaskUs Holdings, Inc., Schedule ID 96558696. The schedule named a "
     "collection site but set no appointment. On September 16, 2026, Plaintiff "
     "went to that site to provide the sample. Site staff turned him away "
     "because walk-ins were not accepted and no appointment existed for him, "
     "and directed him to the scheduling number in First Advantage's email. "
     "Minutes later First Advantage emailed Plaintiff and TaskUs that the "
     "schedule \"could not be successfully completed.\" Plaintiff called that "
     "number one minute after the email arrived and could not reach anyone. "
     "The schedule then expired before the collection site opened on "
     "September 17."),
    ("P",
     "The saliva schedule lapsed inside First Advantage's own scheduling "
     "process after Plaintiff appeared to test -- not through any refusal by "
     "Plaintiff -- and it lapsed after the September 14 background-report hold "
     "and after the September 15 furnishing of the California-registry-sourced "
     "report. Whether Defendants now treat it as an independent employment "
     "reason is a causation question distinct from whether Defendants procured "
     "the report lawfully and whether they actually used California-registry "
     "information for an employment decision."),
    ("P",
     "After September 15, 2026, Defendants maintained the administrative "
     "hold, did not restore the September 23 Uber AV Teammate start, did not "
     "issue a new start date, and did not issue a Fair Chance restoration or "
     "individualized assessment stating that California-registry information "
     "was disregarded. On September 23, 2026 -- the anticipated start date and "
     "the first day of scheduled orientation -- Plaintiff was not permitted to "
     "begin. The accepted assignment was withheld and effectively rescinded."),
    ("P",
     "Before that post-report withholding, the persons taking and maintaining "
     "the adverse action did not provide Plaintiff both a copy of Order "
     "WPS-361214148 and the written Summary of Rights required by 15 U.S.C. "
     "§ 1681b(b)(3)(A)."),
    ("P",
     "The California-registry-sourced component was a substantial factor in "
     "the post-report employment decision. The September 14 hold identified "
     "the background screening report as controlling release of the start; "
     "the report that then arrived expressly sourced the sex-offender "
     "component to the California Sex Offender Registry; and the start was "
     "never restored after that report was furnished."),
    ("P",
     "Uber Technologies, Inc. is named because the only assignment offered "
     "was Uber's branded AV Teammate campaign and because -- on information "
     "and belief grounded in the campaign documents alleged below -- Uber set, "
     "specified, or approved the First Advantage search criteria and screening "
     "package used for that campaign, including the national sex-offender "
     "components that returned California-registry SOURCE OF RECORD "
     "information, and shared control over start authorization. Uber is not "
     "sued merely because its name appears on WorkDay."),
    ("P",
     "First Advantage is the consumer reporting agency that generated Order "
     "WPS-361214148. It is not named as a defendant in this Complaint. "
     "Plaintiff reserves all claims against First Advantage arising from its "
     "furnishing of California-registry-sourced employment reports."),

    ("H", "II.\nJURISDICTION AND VENUE"),
    ("P",
     "This Court has federal-question jurisdiction under 28 U.S.C. § 1331 "
     "because Counts One and Three arise under the Fair Credit Reporting Act, "
     "15 U.S.C. § 1681 et seq."),
    ("P",
     "This Court has supplemental jurisdiction under 28 U.S.C. § 1367(a) over "
     "Counts Two, Four, and Five because they arise from the same onboarding, "
     "screening order, report, hold, and withheld start."),
    ("P",
     "Plaintiff has Article III standing. He alleges concrete injuries to the "
     "privacy and information-control interests protected by the "
     "employment-screening statutes and a concrete economic injury from the "
     "loss and withholding of the accepted Uber AV Teammate assignment at the "
     "documented $22.00 hourly rate (production hours 2PM-11PM) and the "
     "associated $1,000 retention-bonus opportunity. He sues as a prospective "
     "employee adversely affected by an employment decision within the meaning "
     "of 15 U.S.C. § 1681a(k)(1)(B)(ii)."),
    ("P",
     "Venue is proper in this District under 28 U.S.C. § 1391(b)(1) and "
     "(b)(2). A substantial part of the events giving rise to the claims "
     "occurred here: the offered assignment was USA - San Jose - San Jose "
     "(Delivery); the WorkDay campaign was Uber AV Teammate (SJ: 09/23/2026); "
     "orientation was scheduled at 1631 N. 1st Street, Suite 200, San Jose; "
     "production was identified at 3030 Corvin Drive, Santa Clara; the saliva "
     "collection site was in Milpitas; and Defendants sought to place "
     "Plaintiff into Northern District operations. Uber is headquartered in "
     "San Francisco and resides in this District."),
    ("P",
     "Intra-district assignment. Under Civil Local Rule 3-2(c) and (e), the "
     "action arises in Santa Clara County. Plaintiff states those venue facts "
     "so the Clerk may assign the action accordingly."),

    ("H", "III.\nPARTIES"),
    ("P",
     "Plaintiff Brendan Ngwa Nforbi is a natural person and California "
     "resident. He is a person as to whom information is disclosed through "
     "California's Megan's Law internet website operated under Penal Code "
     "§ 290.46."),
    ("P",
     "Defendant TaskUs Holdings, Inc. (\"TaskUs Holdings\") is a Delaware "
     "corporation registered in California, Entity No. 3828721, with "
     "California registered agent C T Corporation System. First Advantage "
     "identified TASKUS HOLDINGS INC USA, Client Account Number 417722USA, at "
     "1650 Independence Drive, Ste 100, New Braunfels, Texas -- the same "
     "street address on the offer letter -- as the recipient account for Order "
     "WPS-361214148. TaskUs Holdings is the named employer on the First "
     "Advantage saliva-drug-test order and the Adobe Sign / NDA counterparty "
     "on the onboarding packet."),
    ("P",
     "Defendant TaskUs USA, LLC (\"TaskUs USA\") is an active Delaware limited "
     "liability company registered in California, Entity No. 201729810166. "
     "Plaintiff's September 14 United States Background Consent Form "
     "identifies TaskUs USA as a recipient of screening information."),
    ("P",
     "The written Offer of Temporary Employment was issued in the name of "
     "TaskUs, LLC. California Secretary of State records reviewed on "
     "September 14 reflected TaskUs, LLC, Entity No. 200826810086, as "
     "Converted Out. Plaintiff does not treat the former California entity or "
     "its last-listed agent as the service target for the active TaskUs "
     "enterprise. TaskUs, LLC's role is pleaded in the facts and among the "
     "DOES."),
    ("P",
     "The use of different TaskUs entities in the offer, authorization, "
     "report-recipient account, NDA, drug-test order, and arbitration "
     "documents makes the allocation of procurement and decision authority "
     "information primarily within Defendants' possession. Plaintiff pleads "
     "alternative and overlapping responsibility among TaskUs Holdings, TaskUs "
     "USA, and presently unidentified TaskUs entities as permitted by Rule "
     "8(d). Plaintiff does not allege alter ego merely from common branding."),
    ("P",
     "Defendant Uber Technologies, Inc. (\"Uber\") is a Delaware corporation "
     "that does business in this District, including autonomous-vehicle and "
     "delivery operations in Santa Clara County. The offered assignment was "
     "expressly identified as Uber AV Teammate, requisition R_2608_10812. "
     "\"Uber AV\" is a campaign title, not a separate legal entity named as a "
     "defendant."),
    ("P",
     "Plaintiff does not allege that Uber became a statutory user of the "
     "report merely because its name appeared on the campaign. Uber's "
     "liability under Counts Three and Four is asserted because -- on "
     "information and belief grounded in the facts alleged in Sections IV "
     "through X -- Uber set, specified, or approved the First Advantage search "
     "criteria and screening package for Uber AV Teammate placements "
     "(including national sex-offender / PRINSOS / NSOR components), shared "
     "control over start authorization, and received the benefit of TaskUs's "
     "hold and non-restoration pending that report."),
    ("P",
     "Plaintiff is ignorant of the true names and capacities of DOES 1 "
     "through 20 and will amend when ascertained. DOES include TaskUs, LLC; "
     "TaskUs, Inc.; any other TaskUs affiliate that procured, adjudicated, or "
     "used the report or issued the hold; any Uber operating affiliate that "
     "directed the AV Teammate placement or screening; and any person who "
     "received, accessed, or used the California-registry-sourced information "
     "for an employment purpose on this hire."),

    ("H", "IV.\nTHE ACCEPTED UBER AV TEAMMATE ASSIGNMENT"),
    ("P",
     "On September 14, 2026, at approximately 6:50 a.m., WorkDay emailed "
     "Plaintiff from taskus@myworkday.com: \"Congratulations! We are pleased "
     "to make you an offer for the Uber AV Teammate (SJ: 09/23/2026) "
     "position.\""),
    ("P",
     "The same day, TaskUs, LLC issued a written Offer of Temporary "
     "Employment stating, among other things:"),
    ("B", "hiring employer: TaskUs, LLC;"),
    ("B", "position: Teammate;"),
    ("B", "base pay: $22.00 per hour, non-exempt;"),
    ("B", "location: USA - San Jose - San Jose (Delivery);"),
    ("B", "production hours: 2PM - 11PM;"),
    ("B",
     "anticipated assignment: September 23, 2026 through on or around "
     "December 4, 2026;"),
    ("B",
     "retention bonus: $1,000 if still employed in good standing on "
     "December 4, 2026;"),
    ("B",
     "employment at-will and contingent on job-related background screening "
     "and a Fair Chance Act process for conviction history; and"),
    ("B",
     "screening usually takes two weeks and employment may begin while "
     "screening is pending."),
    ("P",
     "Plaintiff accepted the offer the same day. The Adobe Acrobat Sign "
     "signature request for that offer packet was sent by John Malones "
     "(john.malones@taskus.com) on September 14, 2026, at approximately 6:55 "
     "a.m. Plaintiff completed the Adobe Sign packet the same morning "
     "(completion notice Reply-To: John Malones / TaskUs Holdings Inc) at "
     "approximately 8:21 a.m. PDT and signed the United States Background "
     "Consent Form, the TaskUs Holdings, Inc. non-disclosure / "
     "invention-assignment agreement, and related onboarding documents."),
    ("P",
     "DLSE Form 2810.5 identified TaskUs, LLC as the hiring employer. It did "
     "not list Uber as the entity for whom the work would be performed. That "
     "wage-notice fact does not negate Uber's end-client role on the "
     "Uber-branded campaign as alleged herein."),
    ("P",
     "The only assignment offered was the Uber AV Teammate campaign. Without "
     "Uber's campaign, there was no Teammate placement for Plaintiff to "
     "accept."),
    ("P",
     "At approximately 6:51 a.m. the same day, TA Ops US emailed Plaintiff "
     "\"Action Required Today\" onboarding tasks that separately listed "
     "Workday, Adobe Sign, I-9, the First Advantage background check, and the "
     "drug test -- treating the consumer-report screen and the saliva product "
     "as distinct items."),

    ("H", "V.\nPROCUREMENT OF ORDER WPS-361214148"),
    ("P",
     "On September 14, 2026, at approximately 6:50 a.m., First Advantage "
     "emailed Plaintiff from do_not_reply@fadv.com inviting him to start a "
     "Profile Advantage background check (invite key GK5HGWELSS)."),
    ("P",
     "The same day, Profile Advantage opened Order WPS-361214148 (portal "
     "candidate name Brendan Ngwanforbi)."),
    ("P",
     "Order WPS-361214148 was a \"consumer report\" within the meaning of 15 "
     "U.S.C. § 1681a(d): a written communication by First Advantage, a "
     "consumer reporting agency, bearing on Plaintiff's character, general "
     "reputation, and mode of living -- including the national sex-offender "
     "registry component -- that was furnished and used for employment "
     "purposes.",
     "consumer_report"),
    ("P",
     "The report was procured for employment purposes. TaskUs Holdings and "
     "TaskUs USA procured or caused the report to be procured and received or "
     "were entitled to receive its results. Their exact contractual allocation "
     "is information primarily within Defendants' knowledge and is pleaded in "
     "the alternative under Rule 8(d)."),
    ("P",
     "The written Offer of Temporary Employment stated that the Company would "
     "provide required standalone disclosures and obtain required "
     "authorizations before obtaining a consumer or investigative consumer "
     "report."),
    ("P",
     "Plaintiff's preserved documents include a United States Background "
     "Consent Form permitting release of screening information to TaskUs USA, "
     "LLC. That form is a release/consent. It does not itself contain all of "
     "the content required of a standalone FCRA disclosure and does not itself "
     "identify all information required by Civil Code § 1786.16."),
    ("P",
     "Before procurement, Defendants did not provide Plaintiff a separate "
     "compliant document that consisted solely of the disclosure required by "
     "15 U.S.C. § 1681b(b)(2)(A) and that informed him that a consumer report "
     "could be obtained for employment purposes -- notwithstanding the offer's "
     "promise that such standalone disclosures would be provided."),
    ("P",
     "Before procurement, Defendants likewise did not provide Plaintiff a "
     "compliant ICRAA standalone disclosure identifying the investigative "
     "consumer reporting agency actually conducting the investigation and "
     "providing the required California-specific information."),
    ("P",
     "As of approximately 10:20 a.m. PDT on September 14, 2026, the portal "
     "showed:"),
    ("B",
     "Completed: MVR; Federal Felony And Misdemeanor; PRICPGS; FADV National "
     "Criminal File; Social Security Verification;"),
    ("B", "In Progress: Felony Including Misdemeanor; PRINSOS."),
    ("P",
     "The portal stated the report was not viewable until the order "
     "completed. A component marked Completed is not itself a result and is "
     "not a registry hit. As of the 10:20 a.m. snapshot -- about one hour "
     "before the hold email -- the sex-offender component had not finished."),

    ("H", "VI.\nTHE SEPTEMBER 14 HOLD IS CONTEXT,\nNOT THE COMPLETED-REPORT ADVERSE ACTION"),
    ("P",
     "On September 14, 2026, at 11:24 a.m., TA Ops US (taops.us@taskus.com), "
     "copying Liz Ramirez (liz.ramirez02@taskus.com), emailed Plaintiff "
     "\"Important Update Regarding Your Application with TaskUs.\""),
    ("P",
     "The email stated that TaskUs had placed Plaintiff's start date on a "
     "\"standard administrative hold while final onboarding reviews are "
     "completed, including the processing of your background screening "
     "report,\" that the scheduled start must be adjusted pending completion "
     "of that process, that Plaintiff should monitor First Advantage "
     "(Customer Support 800-888-5773), and that the application \"remains in "
     "a pending status.\""),
    ("P",
     "That email is in Plaintiff's possession and will be produced as "
     "appropriate. It is not a First Advantage pre-adverse notice. It did not "
     "enclose a copy of a consumer report. It did not enclose a written "
     "Summary of Rights."),
    ("P",
     "At the time of that message, the portal reflected that PRINSOS remained "
     "In Progress. Plaintiff therefore does not plead that the September 14 "
     "hold was an adverse action based on the completed California-registry "
     "result."),
    ("P",
     "The hold instead establishes that the background screening process was "
     "an identified condition affecting release of Plaintiff's accepted start "
     "and supplies context for evaluating what happened after the completed "
     "report was furnished."),
    ("P",
     "The hold contradicted the offer's statement that employment may begin "
     "while screening is pending."),

    ("H", "VII.\nFIRST ADVANTAGE FURNISHED\nCALIFORNIA-REGISTRY-SOURCED INFORMATION"),
    ("P",
     "On September 15, 2026, First Advantage issued a consumer disclosure "
     "letter to Plaintiff at his Stockton address. The letter advised that "
     "First Advantage was reporting public-record information concerning "
     "Plaintiff to TASKUS HOLDINGS INC USA, 1650 Independence Dr., Ste 100, "
     "New Braunfels, TX 78132-3832."),
    ("P",
     "That consumer disclosure, including the enclosed registry component, is "
     "in Plaintiff's possession and will be produced as appropriate."),
    ("P",
     "The enclosed national sex offender registry component of Order "
     "WPS-361214148 states, among other things:"),
    ("B", "Record Source: NATIONAL SEX OFFENDER REGISTRY;"),
    ("B",
     "Type of Search: NATIONAL SEX OFFENDER REGISTRY SEARCH-DEPT OF JUSTICE;"),
    ("B", "Date of Search: 09/14/2026;"),
    ("B", "Name on File: NGWANFORBI, BRENDAN NGEHSI; and"),
    ("B",
     "Sentence: SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY. "
     "SENTENCE: REGISTERED SEX OFFENDER."),
    ("P",
     "Plaintiff therefore possesses a document directly attributing the "
     "sex-offender component to the California Sex Offender Registry."),
    ("P",
     "Procurement and furnishing do not, standing alone, establish actionable "
     "\"use\" under Penal Code § 290.46(j)(2)(E). Count Four is based on "
     "actual employment use after the report was received -- the post-report "
     "maintenance of the hold and the never-restored start -- not on First "
     "Advantage's transmission alone."),

    ("H", "VIII.\nTHE COMPLETED ADVERSE ACTION --\nPOST-REPORT NON-RESTORATION"),
    ("P",
     "After First Advantage furnished Order WPS-361214148 to TASKUS HOLDINGS "
     "INC USA on September 15, 2026, Defendants had the consumer report that "
     "the September 14 hold had been waiting on."),
    ("P",
     "From September 15 through the anticipated September 23 start, "
     "Defendants:"),
    ("B", "maintained the administrative hold;"),
    ("B", "did not restore the September 23 Uber AV Teammate start;"),
    ("B", "did not issue a new start date;"),
    ("B",
     "did not provide Plaintiff a copy of Order WPS-361214148 and a written "
     "Summary of Rights before maintaining that hold and withholding the "
     "assignment;"),
    ("B",
     "did not advise Plaintiff under Civil Code § 1786.40, at the time of the "
     "employment denial or withholding, that an investigative consumer report "
     "had been obtained, or supply First Advantage's name and address; and"),
    ("B",
     "did not issue a Fair Chance notice or individualized assessment stating "
     "that California-registry information was disregarded."),
    ("P",
     "The completed adverse employment action alleged in this Complaint is "
     "therefore the post-furnishing withholding and effective rescission of "
     "the accepted assignment. The September 14 hold is the employer's own "
     "writing that the background report controlled the start. The September "
     "15 disclosure is the report that then arrived, expressly sourced to the "
     "California Sex Offender Registry. The September 23 start date arrived "
     "without restoration."),
    ("P",
     "Freezing an accepted start date, placing the application in pending "
     "status, maintaining that freeze after the report arrived, and "
     "withholding the Uber AV Teammate assignment are adverse employment "
     "actions -- employment decisions adversely affecting a prospective "
     "employee within the meaning of 15 U.S.C. § 1681a(k)(1)(B)(ii) -- and "
     "purposes relating to employment within the meaning of Penal Code "
     "§ 290.46(j)."),
    ("P",
     "No Defendant has identified to Plaintiff any reason for the hold other "
     "than the background screening report."),

    ("H", "IX.\nTHE SALIVA SCHEDULE WAS SEPARATE, LATER, AND\nLAPSED IN FIRST ADVANTAGE'S OWN PROCESS"),
    ("P",
     "On September 14, 2026, at approximately 8:49 a.m. Pacific, First "
     "Advantage separately ordered a Saliva Drug Test Full Service NonDOT for "
     "employer TaskUs Holdings, Inc. (Schedule ID 96558696; LabCorp Web COC "
     "Order Registration Number 610727488). The designated collection site "
     "was LabCorp-Milpitas in Walgreens, 342 W. Calaveras Boulevard, "
     "Milpitas, California. The schedule was set to expire September 17, "
     "2026, at 11:49 a.m. Eastern."),
    ("P",
     "Page 9 of the offer packet is a California medical release for that "
     "drug/alcohol product \"as facilitated by First Advantage and/or its "
     "network of authorized laboratories.\" That authorization is not a "
     "consumer-report disclosure and is not Order WPS-361214148."),
    ("P",
     "First Advantage emailed reminders for Schedule ID 96558696 on September "
     "15, 2026, at 9:02 a.m., and September 16, 2026, at 9:57 a.m. Each was "
     "addressed to Plaintiff and to taops-bgvglobal@taskus.com. Neither set "
     "an appointment. Under \"Appointment Details,\" each stated only: "
     "\"Contact site to determine appointment requirements.\" Each listed the "
     "site's hours as \"M-F 9am-11:30am, 1:30pm-3pm.\""),
    ("P",
     "On September 16, 2026, at approximately 3:00 p.m., Plaintiff went to "
     "LabCorp-Milpitas in Walgreens to provide the saliva sample. The staff "
     "member at the collection site told him: \"We do not accept walk-ins and "
     "we do not have any scheduled appointments for you. Please call the "
     "number in the email to schedule an appointment.\"",
     "saliva_site"),
    ("P",
     "At 3:05 p.m. the same day, First Advantage emailed \"Employment "
     "Screening: Action Required\" to Plaintiff and to "
     "taops-bgvglobal@taskus.com. It stated: \"Your confirmation could not be "
     "successfully completed. Please call the First Advantage Corporation "
     "Scheduling Center @ 866-682-4166 to schedule your appointment "
     "immediately.\""),
    ("P",
     "At 3:06 p.m., one minute after that email, Plaintiff called the First "
     "Advantage Scheduling Center at (866) 682-4166. The call lasted "
     "approximately two minutes. Plaintiff was unable to reach anyone.",
     "saliva_call"),
    ("P",
     "The schedule expired on September 17, 2026, at 11:49 a.m. Eastern -- "
     "8:49 a.m. Pacific -- before the collection site's posted 9:00 a.m. "
     "opening that morning. No collection window remained on September 17."),
    ("P",
     "The saliva schedule therefore lapsed within First Advantage's own "
     "scheduling process: the site would not collect without an appointment, "
     "First Advantage had set none, and Plaintiff could not reach anyone at "
     "the scheduling line he was directed to call. Plaintiff did not refuse or decline "
     "the test. TaskUs was copied on each schedule notice, including the "
     "September 16 Action Required message."),
    ("P",
     "Plaintiff does not collapse the saliva product into the consumer "
     "report."),
    ("P", "The September 14 hold:"),
    ("B",
     "issued on September 14 at 11:24 a.m., two days before Plaintiff went "
     "to the collection site;"),
    ("B", "expressly named the background screening report;"),
    ("B", "did not name the saliva test; and"),
    ("B",
     "remained operative after First Advantage furnished the "
     "California-registry-sourced report on September 15 -- still one day "
     "before the saliva schedule lapsed."),
    ("P",
     "A later lapse in First Advantage's saliva scheduling cannot, at the "
     "pleading stage, erase the employer's own September 14 writing or the "
     "September 15 California-registry-sourced report. Plaintiff alleges that "
     "the California-registry-sourced information in Order WPS-361214148 was "
     "a substantial factor in Defendants' post-report freezing and withholding "
     "of the accepted Uber AV Teammate assignment."),

    ("H", "X.\nUBER AS END CLIENT / JOINT EMPLOYER"),
    ("P",
     "Every candidate-facing WorkDay communication that announced the offer "
     "identified the position as Uber AV Teammate, not a generic TaskUs "
     "role."),
    ("P",
     "The requisition identifier is R_2608_10812 / C261051599 -- Uber AV "
     "Teammate (SJ: 09/23/2026)."),
    ("P",
     "The anticipated work was San Jose delivery on Uber's AV campaign. The "
     "offer packet supplied orientation at 1631 N. 1st Street, Suite 200, San "
     "Jose, a production depot at 3030 Corvin Drive, Santa Clara, and "
     "closed-course training in Sonoma -- locations of the work to be "
     "performed for Uber's campaign, not generic TaskUs office work."),
    ("P",
     "TaskUs Holdings and TaskUs USA functioned as the staffing / payroll / "
     "offer-letter / consent / report-recipient enterprise. Uber functioned as "
     "the end client whose branded campaign created the temporary need for "
     "Teammates and whose Northern District operations would receive "
     "Plaintiff's labor."),
    ("P",
     "On information and belief, grounded in the offer packet, the WorkDay "
     "campaign title and requisition, the September 14 hold, and the "
     "September 15 consumer disclosure:"),
    ("B",
     "Uber directed or approved the Uber AV Teammate requisition, headcount, "
     "San Jose location, and September 23, 2026 start cohort;"),
    ("B",
     "Uber set, specified, or approved the First Advantage search criteria "
     "and screening package TaskUs ordered for Uber AV Teammate placements -- "
     "including the national sex-offender / PRINSOS / NSOR search components "
     "that returned the California Sex Offender Registry SOURCE OF RECORD "
     "line on Order WPS-361214148;"),
    ("B", "TaskUs ran that package as the staffing vendor for Uber's campaign;"),
    ("B",
     "Uber received, was entitled to receive, or caused TaskUs to obtain and "
     "use First Advantage screening results -- including the "
     "California-registry-sourced component -- before authorizing Plaintiff's "
     "start on Uber's campaign;"),
    ("B",
     "TaskUs's September 14 hold pending the background report, and the "
     "post-September 15 non-restoration, were taken in the course of staffing "
     "Uber's campaign and for Uber's benefit; and"),
    ("B",
     "Uber and the TaskUs defendants are joint employers and/or agents of one "
     "another with respect to the hiring decision on this placement."),
    ("P",
     "Uber's campaign created the only job offered. The First Advantage "
     "package run for that campaign returned California-registry SOURCE OF "
     "RECORD information. TaskUs froze the start pending that report and "
     "never restored it after the report arrived."),
    ("P",
     "Penal Code § 290.46(j)(2)(E) prohibits use of § 290.46-disclosed "
     "information \"for purposes relating to employment.\" Using that "
     "information to freeze or deny placement onto Uber's AV Teammate campaign "
     "is such a purpose, whether the offer letter is on TaskUs letterhead or "
     "Uber's."),
    ("P",
     "The Form 2810.5's naming of TaskUs, LLC is a wage-notice fact. It does "
     "not preclude Uber's liability under Penal Code § 290.46(j) or the FCRA "
     "as end client and joint employer on the Uber AV Teammate campaign."),

    ("H", "XI.\nNO STATUTORY AUTHORIZATION; NO PRE-ADVERSE PACKET\nBEFORE THE COMPLETED ADVERSE ACTION"),
    ("P",
     "The use alleged was not \"to protect a person at risk\" within the "
     "meaning of Penal Code § 290.46(j)(1). Plaintiff is unaware of any other "
     "provision of law authorizing Defendants to use information disclosed "
     "pursuant to Penal Code § 290.46 for this Teammate / Uber AV delivery "
     "assignment."),
    ("P",
     "Before taking and completing adverse action based in whole or in part "
     "on Order WPS-361214148 -- specifically, before maintaining the hold and "
     "withholding the assignment after that report was furnished -- "
     "Defendants did not provide Plaintiff a copy of the First Advantage "
     "consumer report and a written Summary of Rights as required by 15 "
     "U.S.C. § 1681b(b)(3)(A)."),
    ("P",
     "Defendants did not, at the time of the employment denial or "
     "withholding, advise Plaintiff under Civil Code § 1786.40 that an "
     "investigative consumer report had been obtained, or supply First "
     "Advantage's name and address."),
    ("P",
     "The offer referenced a Fair Chance Act process for conviction history. "
     "Defendants did not provide Plaintiff a Fair Chance notice restoring the "
     "start or an individualized assessment stating that California-registry "
     "information was disregarded."),

    ("H", "XII.\nDAMAGES"),
    ("P",
     "Plaintiff lost an accepted temporary assignment at $22.00 per hour, "
     "production hours 2PM-11PM, from September 23, 2026 through on or around "
     "December 4, 2026, and lost the opportunity to earn the $1,000 retention "
     "bonus if still employed in good standing on December 4, 2026."),
    ("P",
     "Those offer terms supply a concrete, non-speculative damages floor for "
     "the rate and window. This Complaint does not assume an unguaranteed "
     "40-hour schedule. The precise hour count and any overtime will be "
     "proved according to the assignment schedule and proof at trial."),
    ("P",
     "Plaintiff also seeks nonduplicative statutory, actual, exemplary, "
     "punitive, fee, cost, and interest remedies authorized by the surviving "
     "claims.",
     "last_fact"),

    ("H", "XIII.\nCOUNT ONE\nFair Credit Reporting Act -- 15 U.S.C. § 1681b(b)(2)(A)\n(Against TaskUs Holdings, TaskUs USA, and the Procuring DOE Defendants)"),
    ("P", "Plaintiff realleges paragraphs 1 through {ref:last_fact}."),
    ("P",
     "Plaintiff was a consumer. Order WPS-361214148 was a consumer report "
     "under 15 U.S.C. § 1681a(d) as alleged in paragraph {ref:consumer_report}. "
     "The TaskUs defendants procured or caused that consumer report to be "
     "procured for employment purposes."),
    ("P",
     "Section 1681b(b)(2)(A) requires a clear and conspicuous written "
     "disclosure, made before procurement, in a document consisting solely of "
     "the disclosure, that a consumer report may be obtained for employment "
     "purposes, together with written authorization."),
    ("P",
     "Before procurement, Defendants did not provide Plaintiff a compliant "
     "standalone disclosure satisfying § 1681b(b)(2)(A). The preserved United "
     "States Background Consent Form is a consent/release, not that "
     "standalone disclosure. The offer's own promise that required standalone "
     "disclosures would be provided before obtaining a consumer or "
     "investigative consumer report was not kept."),
    ("P",
     "Defendants nevertheless caused First Advantage to procure and furnish "
     "Order WPS-361214148."),
    ("P",
     "The violation was at least negligent under 15 U.S.C. § 1681o. On proof "
     "concerning Defendants' standardized screening architecture and "
     "compliance procedures, it was willful under 15 U.S.C. § 1681n."),
    ("P",
     "Plaintiff seeks relief authorized by 15 U.S.C. §§ 1681n and 1681o, "
     "without duplicative recovery."),

    ("H", "XIV.\nCOUNT TWO\nCalifornia Investigative Consumer Reporting Agencies Act --\nPre-Procurement Disclosure, Civil Code §§ 1786.16, 1786.50\n(Against TaskUs Holdings, TaskUs USA, and the Procuring DOE Defendants)"),
    ("P", "Plaintiff realleges paragraphs 1 through {ref:last_fact}."),
    ("P",
     "The First Advantage Profile Advantage employment background report "
     "(Order WPS-361214148) was an investigative consumer report under ICRAA: "
     "a consumer report bearing on Plaintiff's character, general reputation, "
     "personal characteristics, and mode of living -- including registry "
     "status -- obtained through database and public-record compilation for "
     "employment. Civil Code § 1786.2(c) defines \"investigative consumer "
     "report\" to reach such information \"obtained through any means.\"",
     "icr_def"),
    ("P",
     "Civil Code § 1786.16 requires specified clear and conspicuous "
     "pre-procurement disclosures in a document consisting solely of the "
     "disclosure, including identification of the investigative consumer "
     "reporting agency conducting the investigation and California-specific "
     "information concerning the nature and scope of the investigation and "
     "consumer rights."),
    ("P",
     "The preserved TaskUs onboarding documents did not provide Plaintiff the "
     "required § 1786.16 standalone disclosure before First Advantage "
     "procured Order WPS-361214148."),
    ("P",
     "Defendants nevertheless procured or caused the investigative consumer "
     "report to be prepared and furnished."),
    ("P",
     "Plaintiff seeks the remedies authorized by Civil Code § 1786.50 "
     "according to proof, including actual damages or the statutory amount "
     "where available, costs and attorney's fees where recoverable, and "
     "punitive damages upon proof of grossly negligent or willful "
     "noncompliance."),

    ("H", "XV.\nCOUNT THREE\nFair Credit Reporting Act -- 15 U.S.C. § 1681b(b)(3)(A)\n(Against TaskUs Holdings, TaskUs USA, Uber, and the\nPost-Report User DOE Defendants)"),
    ("P", "Plaintiff realleges paragraphs 1 through {ref:last_fact}."),
    ("P",
     "Order WPS-361214148 was a consumer report used for employment "
     "purposes."),
    ("P",
     "After First Advantage furnished Order WPS-361214148 to TASKUS HOLDINGS "
     "INC USA on September 15, 2026, Defendants used that report for "
     "employment purposes by maintaining the September 14 hold, refusing to "
     "restore the September 23 start, and withholding or rescinding the "
     "accepted Uber AV Teammate assignment. The September 23 start date "
     "arrived without restoration."),
    ("P",
     "Those post-furnishing acts were adverse actions based in whole or in "
     "part on the consumer report -- employment decisions adversely affecting "
     "a prospective employee within the meaning of 15 U.S.C. "
     "§ 1681a(k)(1)(B)(ii)."),
    ("P",
     "Before taking those post-furnishing adverse actions, Defendants did not "
     "provide Plaintiff a copy of that report and the written Summary of "
     "Rights required by § 1681b(b)(3)(A)."),
    ("P",
     "The September 14 hold is not pleaded as the completed-report adverse "
     "action; it is context showing that report processing affected release "
     "of the start, and part of a continuous adverse-action sequence that "
     "matured when the report arrived and the start was never restored."),
    ("P",
     "The saliva schedule does not supply a lawful independent basis for "
     "those actions. As alleged in paragraphs {ref:saliva_site} through "
     "{ref:saliva_call}, Plaintiff appeared at the designated collection site "
     "and called the number he was directed to call; the schedule lapsed in "
     "First Advantage's own process, after the report had been furnished."),
    ("P",
     "Uber's liability on this Count rests on the joint-employer / "
     "package-specification and start-authorization facts alleged in Section "
     "X, not on campaign branding alone."),
    ("P",
     "The count is timely. The completed adverse action occurred on and after "
     "September 15, 2026, and crystallized on September 23, 2026, when the "
     "start date arrived without restoration."),
    ("P",
     "Noncompliance was at least negligent under 15 U.S.C. § 1681o. On proof, "
     "it was willful under 15 U.S.C. § 1681n: Defendants are sophisticated "
     "users of employment consumer reports; TaskUs operates high-volume "
     "background screening as a standard part of its staffing business; the "
     "offer packet invoked a Fair Chance Act process; First Advantage's own "
     "September 15 package identified the document as a consumer disclosure "
     "of public-record information being reported to TASKUS HOLDINGS INC USA; "
     "and Defendants nonetheless completed the withholding without the "
     "required pre-adverse copy and Summary of Rights."),
    ("P",
     "Plaintiff seeks relief authorized by 15 U.S.C. §§ 1681n and 1681o "
     "according to proof."),

    ("H", "XVI.\nCOUNT FOUR\nUnauthorized Employment Use of Information Disclosed\nPursuant to Penal Code § 290.46 -- Penal Code § 290.46(j)(2)(E), (j)(4)(A)\n(Against TaskUs Holdings, TaskUs USA, Uber, and the\nActual-Use DOE Defendants)"),
    ("P", "Plaintiff realleges paragraphs 1 through {ref:last_fact}."),
    ("P",
     "Plaintiff is a person as to whom information is disclosed through "
     "California's Megan's Law internet website."),
    ("P",
     "Section 290.46(j)(2)(E) prohibits use of information disclosed pursuant "
     "to § 290.46 for purposes relating to employment, except as authorized "
     "under § 290.46(j)(1) or any other provision of law."),
    ("P",
     "First Advantage furnished to TaskUs Holdings Inc USA, on Order "
     "WPS-361214148, information concerning Plaintiff whose sex-offender "
     "component expressly states SOURCE OF RECORD: CALIFORNIA SEX OFFENDER "
     "REGISTRY."),
    ("P",
     "That information is information disclosed pursuant to Penal Code "
     "§ 290.46. Plaintiff does not ask the Court to infer the source. The "
     "Sentence field states it."),
    ("P",
     "Plaintiff does not base this Count on ordinary court-record conviction "
     "information and does not allege that mere republication by First "
     "Advantage, standing alone, is the prohibited employment use."),
    ("P",
     "After receiving the report, Defendants actually used that "
     "California-registry-sourced information for purposes relating to "
     "employment by maintaining the administrative hold pending the "
     "background screening report, refusing to restore the September 23 Uber "
     "AV Teammate start, and withholding or rescinding Plaintiff's accepted "
     "assignment after the report -- with its California-registry SOURCE OF "
     "RECORD line -- was in their hands."),
    ("P",
     "The California-registry-sourced information was a substantial factor "
     "in those employment actions. The September 14 hold named the background "
     "screening report as a basis for freezing the start. The report that "
     "then arrived contained the California-registry SOURCE OF RECORD line. "
     "The start was never restored."),
    ("P",
     "Uber used, caused the use of, or is jointly liable for the use of that "
     "information for purposes relating to employment on its Uber AV Teammate "
     "campaign, as end client and joint employer -- including by setting or "
     "approving the search criteria that caused the "
     "California-registry-sourced component to be ordered and by receiving "
     "the benefit of TaskUs's hold and non-restoration pending that report."),
    ("P",
     "The use was not to protect a person at risk under § 290.46(j)(1), and "
     "Plaintiff is unaware of any other law authorizing use of "
     "§ 290.46-disclosed information for this assignment."),
    ("P",
     "The use occurred on and after September 15, 2026. This action is "
     "timely."),
    ("P", "Defendants thereby violated Penal Code § 290.46(j)(2)(E)."),
    ("P",
     "Plaintiff seeks the remedies authorized by § 290.46(j)(4)(A): actual "
     "damages, and any amount determined by the jury or the Court not "
     "exceeding three times the actual damages and not less than $250, plus "
     "attorney's fees, exemplary damages, and costs as authorized -- without "
     "duplicative recovery."),
    ("P",
     "Plaintiff does not presently seek preventive relief under "
     "§ 290.46(j)(4)(B)."),
    ("P",
     "This Count is limited to use of information disclosed pursuant to "
     "§ 290.46, as shown by the SOURCE OF RECORD field on Order "
     "WPS-361214148."),

    ("H", "XVII.\nCOUNT FIVE\nICRAA Adverse-Employment Notice -- Civil Code §§ 1786.40, 1786.50\n(Against TaskUs Holdings, TaskUs USA, and the Denial-Actor DOE Defendants)"),
    ("P", "Plaintiff realleges paragraphs 1 through {ref:last_fact}."),
    ("P",
     "Order WPS-361214148 was an investigative consumer report under Civil "
     "Code § 1786.2(c) as alleged in paragraph {ref:icr_def}."),
    ("P",
     "Defendants denied, withheld, or refused to proceed with Plaintiff's "
     "accepted employment under circumstances in which they had obtained the "
     "First Advantage investigative consumer report. The September 23 start "
     "date arrived without restoration."),
    ("P",
     "At the time of that employment denial or withholding, Defendants did "
     "not provide the § 1786.40 advice -- including First Advantage's name "
     "and address."),
    ("P",
     "The § 1786.40 omission alleged here is separate from the FCRA "
     "pre-adverse omission alleged in Count Three. First Advantage's September "
     "15 consumer disclosure to Plaintiff is not Defendants' contemporaneous "
     "§ 1786.40 advice at the time they withheld the assignment."),
    ("P",
     "Plaintiff seeks the remedies authorized by Civil Code § 1786.50 "
     "according to proof."),

    ("H", "XVIII.\nPRAYER FOR RELIEF"),
    ("U", "WHEREFORE, Plaintiff requests:"),
    ("L",
     "A. Actual and compensatory damages according to proof, including the "
     "value of the accepted $22.00-per-hour assignment (production hours "
     "2PM-11PM) for the September 23 through on or around December 4, 2026 "
     "window and the $1,000 retention-bonus opportunity, without inventing an "
     "unguaranteed hour count;"),
    ("L", "B. Relief authorized by 15 U.S.C. §§ 1681n and 1681o;"),
    ("L", "C. Relief authorized by Civil Code § 1786.50;"),
    ("L", "D. Relief authorized by Penal Code § 290.46(j)(4)(A);"),
    ("L",
     "E. Punitive or exemplary damages where authorized and supported by "
     "proof;"),
    ("L",
     "F. Taxable costs and attorney's fees where authorized by statute or "
     "rule;"),
    ("L", "G. Prejudgment and postjudgment interest as allowed by law; and"),
    ("L", "H. Such other nonduplicative relief as the Court deems proper."),

    ("H", "XIX.\nDEMAND FOR JURY TRIAL"),
    ("U",
     "Pursuant to Federal Rule of Civil Procedure 38(b) and Civil Local Rule "
     "3-6, Plaintiff demands trial by jury on all issues so triable."),
]

_REF = re.compile(r"\{ref:([a-z_]+)\}")


def _number(content):
    labels, n = {}, 0
    for item in content:
        if item[0] == "P":
            n += 1
            if len(item) > 2:
                labels[item[2]] = n
    return labels


def _signature_block(d: PleadingPaper, exec_date: str, execute: bool) -> None:
    d.ensure_space(10)
    d.blank_line()
    d.write_line(f"Dated: {exec_date}")
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    if execute:
        d.draw_signature_image(
            SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
        )
    else:
        d.blank_line()
        d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def build(out: Path, exec_date: str, execute: bool) -> Path:
    if execute and not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    labels = _number(CONTENT)
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    c = d.c

    top_y = d._line_y(0)
    for i, (txt, font_name, size) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(font_name, size)
        c.drawString(CONTENT_LEFT, top_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(
        CAPTION_LEFT, CAPTION_RIGHT, caption_size=9.0, tight_lh=11.0, boxed=True
    )
    d.blank_line()

    n = 0
    prev = None
    for item in CONTENT:
        kind, text = item[0], item[1]
        text = _REF.sub(lambda m: str(labels[m.group(1)]), text)
        if prev == "B" and kind != "B":
            d.blank_line()
        prev = kind
        if kind == "H":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "P":
            n += 1
            d.write_wrapped(f"{n}. {text}", first_indent=36)
            d.blank_line()
        elif kind == "U":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "B":
            d.write_wrapped(f"•  {text}", indent=54, first_indent=0)
        elif kind == "L":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"Unknown content kind: {kind}")

    _signature_block(d, exec_date, execute)
    d.save()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    parser.add_argument("--date", default=DEFAULT_EXEC_DATE)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Affix Plaintiff's signature",
    )
    args = parser.parse_args()
    path = build(Path(args.out).resolve(), args.date, args.execute)
    print(f"Generated: {path}")


if __name__ == "__main__":
    main()
