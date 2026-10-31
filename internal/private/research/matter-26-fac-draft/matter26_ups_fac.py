#!/usr/bin/env python3
"""Matter 26 -- FIRST AMENDED COMPLAINT (DRAFT, NOT FOR FILING WITHOUT REVIEW).

Newanforbi v. United Parcel Service, Inc., USDC E.D. Cal. No. 2:26-cv-02847-DAD-CKD.

Source of the draft FAC. Renders on the portfolio's shared pleading-paper
engine (internal/scripts/lib/pleading_paper.py) and stamps the canonical
signature via internal/scripts/signature_stamp.py (never a typed /s/).
The signature date is intentionally blank; it is the only blank.

Exhibits 1 and 2 are excerpts of the documents UPS itself filed with its
Rule 12(b)(6) motion (Felsing Decl., ECF No. 7-2):
  Exhibit 1 = First Advantage Background Report (ECF 7-2 pp. 4-9)
  Exhibit 2 = UPS applicant-system record excerpts (ECF 7-2 pp. 11, 16, 17,
              18, 23, 24) -- the arbitration-agreement pages and the
              disability-questionnaire page are deliberately NOT attached.

    python3 internal/private/research/matter-26-fac-draft/matter26_ups_fac.py [OUT_PDF]

Status: draft for Plaintiff's review. Do not file, serve, or send.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SCRIPTS = ROOT / "internal" / "scripts"
sys.path.insert(0, str(SCRIPTS / "lib"))
sys.path.insert(0, str(SCRIPTS))

from pypdf import PdfReader, PdfWriter  # noqa: E402

from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

DEFAULT_OUT = HERE / "First Amended Complaint - Newanforbi v UPS (E.D. Cal. 2-26-cv-02847) DRAFT (Oct 31 2026).pdf"
FELSING_PDF = ROOT / "documents" / "matter-26" / "Dkt 07-2 - Felsing Declaration with Exhibits (Filed Aug 26 2026).pdf"
EX1_PAGES = [4, 5, 6, 7, 8, 9]          # 1-based pages of ECF No. 7-2
EX2_PAGES = [11, 16, 17, 18, 23, 24]    # 1-based pages of ECF No. 7-2

FOOTER = "FIRST AMENDED COMPLAINT -- NEWANFORBI v. UNITED PARCEL SERVICE, INC."
CASE_NO = "Case No. 2:26-cv-02847-DAD-CKD"

# Plaintiff block: copied EXACTLY from the original Complaint (July 15, 2026),
# including its e-mail line. See README: the portfolio record elsewhere uses
# bnn.cdl@gmail.com -- Plaintiff must confirm before filing.
PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdla@gmail.com", "Times-Roman", 12),
]

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "EASTERN DISTRICT OF CALIFORNIA"

# Party caption: exactly as the original Complaint.
CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("UNITED PARCEL SERVICE, INC.,", True, False),
    ("and DOES 1 through 10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    (CASE_NO, False, False),
    ("", False, False),
    ("FIRST AMENDED COMPLAINT FOR", True, False),
    ("DAMAGES AND INJUNCTIVE RELIEF", True, False),
    ("", False, False),
    ("(1) Violation of Cal. Penal Code", False, False),
    ("     § 290.46(j)(2)(E), (j)(4)(A);", False, False),
    ("(2) Preventive Relief, Cal. Penal Code", False, False),
    ("     § 290.46(j)(4)(B);", False, False),
    ("(3) Violation of ICRAA, Cal. Civ. Code", False, False),
    ("     § 1786.16(b)(1);", False, False),
    ("(4) Violation of ICRAA, Cal. Civ. Code", False, False),
    ("     § 1786.16(a)(2)(B)", False, False),
    ("", False, False),
    ("DEMAND FOR JURY TRIAL", True, False),
    ("", False, False),
    ("Action filed: July 15, 2026", False, False),
    ("Removed: August 20, 2026", False, False),
]

SIGNOFF_NAME = "BRENDAN NGEHSI NEWANFORBI"
SIGNOFF_ROLE = "Plaintiff, In Pro Per"
SIG_LINE = "___________________________________"
DATE_LINE = "Dated: ____________________"

S = "§"

# ---------------------------------------------------------------------------
# CONTENT
#   ("H", text)            centered bold heading (\n splits lines)
#   ("SH", text)           left bold subheading
#   ("P", text[, label])   numbered paragraph; label lets later text cite it
#   ("Q", text)            block quotation (indented, unnumbered)
#   ("U", text)            unnumbered paragraph
#   ("L", text)            indented list item (unnumbered)
# Numbered paragraphs may reference labels as {label}.
# ---------------------------------------------------------------------------
CONTENT = [
    ("U", "Plaintiff BRENDAN NGEHSI NEWANFORBI (\"Plaintiff\") alleges as follows against "
          "Defendant UNITED PARCEL SERVICE, INC. (\"UPS\") and DOES 1 through 10. Allegations "
          "about Plaintiff's own acts and experiences are made on personal knowledge. "
          "Allegations about the contents of documents are made on the documents themselves, "
          "copies of which are attached as Exhibits 1 and 2 (both excerpts of records UPS "
          "filed with its motion to dismiss in this action). All other allegations are made on "
          "information and belief, formed after reasonable inquiry; facts about UPS's "
          "internal screening criteria, adjudication, and decision records are peculiarly "
          "within the possession of UPS and its screening vendor. Page citations to an exhibit "
          "refer to the page of that exhibit following its cover sheet."),

    ("H", "INTRODUCTION"),
    ("P", "On July 17, 2024, Plaintiff applied to work as a Loader/Unloader on the Twilight "
          "shift at UPS's Lathrop, California hub. UPS's screening vendor, First Advantage, ran "
          "four searches for UPS. The Social Security verification scored \"Pass.\" The "
          "criminal-records search returned \"No Record Found\" and scored \"Eligible.\" The "
          "only searches that returned anything were the sex offender registry searches. They "
          "returned one record, scored \"Decisional,\" whose report entry reads: \"SOURCE OF "
          "RECORD: CALIFORNIA SEX OFFENDER REGISTRY.\" On July 19, 2024, the report was scored: "
          "\"BASED ON YOUR CRITERIA, THE OVERALL CASE SCORE IS INELIGIBLE.\" Two days later "
          "UPS cancelled Plaintiff's scheduled first-day appointment, and on July 31, 2024 it "
          "took final adverse action denying him the job.", "intro_first"),
    ("P", "California law forbids that use. Except as authorized to protect a person at risk "
          "or by another provision of law, \"use of any information that is disclosed pursuant "
          "to this section for purposes relating to any of the following is prohibited: "
          ". . . (E) Employment.\" Cal. Penal Code "
          f"{S} 290.46(j)(2) (the \"section\" is section 290.46). UPS has told this Court that it \"used\" the sex offender registry "
          "result \"when making its employment decisions related to Plaintiff.\" The registry "
          "record UPS used came from California. This action seeks the damages and preventive "
          f"relief that section 290.46(j)(4) provides, and statutory damages under the "
          "Investigative Consumer Reporting Agencies Act for UPS's separate failures in "
          "procuring the report."),
    ("P", "This First Amended Complaint supersedes the original Complaint and is intended to "
          "be complete in itself without reference to any prior pleading [E.D. Cal. L.R. 220]. "
          "It does not reassert the original Complaint's Second (failure to hire in violation "
          "of public policy), Fourth (invasion of privacy), Fifth (negligence per se), or "
          "Sixth (Business and Professions Code section 17200) causes of action."),

    ("H", "PARTIES"),
    ("P", "Plaintiff is a natural person who resides in Stockton, San Joaquin County, "
          "California, and is a citizen of California. UPS's records and its vendor's report "
          "refer to Plaintiff as \"Brendan Ngwanforbi,\" \"Brendan Ngehsi Ngwanforbi,\" "
          "\"Brendan Ngehsi Ngwa-Nforbi,\" and \"Nforbi Brendan Ngwa.\" Each refers to "
          "Plaintiff.", "party_pl"),
    ("P", "Defendant UPS is, as UPS alleged in its Notice of Removal, an Ohio corporation "
          "with its principal place of business in Atlanta, Georgia. UPS does business "
          "throughout California, including at its Lathrop hub, 11800 South Harlan Road, "
          "Lathrop, San Joaquin County, California. At all relevant times UPS was a "
          "prospective employer of Plaintiff and the person that requested, procured, received, "
          "and used the background report described below for employment purposes."),
    ("P", "Plaintiff does not know the true names or capacities of Defendants sued as DOES 1 "
          "through 10. On information and belief, each DOE is an individual or entity -- "
          "including any UPS adjudicator, hiring manager, or agent acting for UPS -- who "
          "participated in, directed, or ratified the use of Plaintiff's registry information "
          "for employment purposes or the procurement of the report described below, and is "
          "responsible in some manner for the injuries alleged. Plaintiff will seek leave to "
          "amend when their identities are ascertained. Each defendant acted as the agent of "
          "UPS within the course and scope of that agency."),

    ("H", "JURISDICTION AND VENUE"),
    ("P", "Plaintiff commenced this action on July 15, 2026, in the Superior Court of "
          "California, County of San Joaquin. UPS removed it to this Court on August 20, 2026, "
          "invoking diversity jurisdiction. Plaintiff is a citizen of California; UPS is a "
          "citizen of Ohio and Georgia; and UPS has alleged that the amount in controversy "
          "exceeds $75,000, exclusive of interest and costs. This Court has subject-matter "
          f"jurisdiction under 28 U.S.C. {S} 1332(a)."),
    ("P", "Venue is proper in this District because this is the district embracing the place "
          f"where the state action was pending, 28 U.S.C. {S} 1441(a), and because a "
          "substantial part of the events giving rise to the claims occurred in San Joaquin "
          f"County, 28 U.S.C. {S} 1391(b)(2). Assignment to the Sacramento Division is proper "
          "[E.D. Cal. L.R. 120(d)]."),
    ("P", "This Court has personal jurisdiction over UPS, which does business in California, "
          "operates the Lathrop hub where Plaintiff applied, removed this action, and has "
          "appeared in it."),

    ("H", "STATUTORY BACKGROUND"),
    ("SH", f"A.  Penal Code {S} 290.46 (\"Megan's Law\")"),
    ("P", f"Penal Code section 290.46(a)(1) provides that \"the Department of Justice shall "
          "make available information concerning persons who are required to register "
          f"pursuant to Section 290 to the public via an internet website as specified in this "
          "section.\" That website is commonly called the \"Megan's Law website.\""),
    ("P", "Section 290.46(j)(1) provides: \"A person is authorized to use information "
          "disclosed pursuant to this section only to protect a person at risk.\""),
    ("P", "Section 290.46(j)(2) provides:"),
    ("Q", "\"Except as authorized under paragraph (1) or any other provision of law, use of "
          "any information that is disclosed pursuant to this section for purposes relating to "
          "any of the following is prohibited: (A) Health insurance. (B) Insurance. (C) Loans. "
          "(D) Credit. (E) Employment. (F) Education, scholarships, or fellowships. "
          "(G) Housing or accommodations. (H) Benefits, privileges, or services provided by "
          "any business establishment.\""),
    ("P", "Section 290.46(j)(3) provides: \"This section shall not affect authorized access "
          "to, or use of, information pursuant to, among other provisions, Section 11105 and "
          "11105.3 of this code, Section 8808 of the Family Code, Section 777.5 and 14409.2 of "
          "the Financial Code, Section 1522.01 and 1596.871 of the Health and Safety Code, and "
          "Section 432.7 of the Labor Code.\"", "pc_j3"),
    ("P", "Section 290.46(j)(4)(A) provides:"),
    ("Q", "\"Any use of information disclosed pursuant to this section for purposes other "
          "than those provided by paragraph (1) or in violation of paragraph (2) shall make "
          "the user liable for the actual damages, and any amount that may be determined by "
          "a jury or a court sitting without a jury, not exceeding three times the amount of "
          "actual damage, and not less than two hundred fifty dollars ($250), and attorney's "
          "fees, exemplary damages, or a civil penalty not exceeding twenty-five thousand "
          "dollars ($25,000).\""),
    ("P", "Section 290.46(j)(4)(B) provides, in part:"),
    ("Q", "\"Whenever there is reasonable cause to believe that any person or group of "
          "persons is engaged in a pattern or practice of misuse of the information available "
          "via an internet website established pursuant to this section in violation of "
          "paragraph (2), the Attorney General, any district attorney, or city attorney, or "
          "any person aggrieved by the misuse is authorized to bring a civil action in the "
          "appropriate court requesting preventive relief, including an application for a "
          "permanent or temporary injunction, restraining order, or other order against the "
          "person or group of persons responsible for the pattern or practice of misuse.\""),
    ("P", "The prohibition in section 290.46(j)(2) and the damages remedy in section "
          "290.46(j)(4)(A) both attach to \"information disclosed pursuant to this section.\" "
          "Neither is limited to a person who personally visits the Megan's Law website. An "
          "employer that receives California Megan's Law information through an intermediary "
          "-- a screening company, or a search engine that queries the California website -- "
          "and acts on it uses \"information disclosed pursuant to this section\" just as "
          "surely as an employer that types in the website address."),
    ("P", "The California Court of Appeal has explained that \"the statutory liability "
          "created by the MLW statute should be limited to employers who 'use' information "
          "disclosed on the MLW as a basis for an employment decision,\" and that an "
          "applicant's \"cause of action, if any, lies against his prospective employer,\" not "
          "the screening company that reported the information. Mendoza v. ADP Screening & "
          "Selection Services, Inc. (2010) 182 Cal.App.4th 1644 [pin cites unverified]. UPS "
          "is the prospective employer here."),

    ("SH", "B.  The National Sex Offender Public Website Searches the State Websites"),
    ("P", "The United States Department of Justice, through its Office of Sex Offender "
          "Sentencing, Monitoring, Apprehending, Registering, and Tracking (\"SMART\"), "
          "maintains the National Sex Offender Public Website (\"NSOPW\"). According to the "
          "Department of Justice's own published fact sheet, \"NSOPW vs NSOR,\" NSOPW \"uses "
          "web services to search the individual public registry websites from each of the "
          "jurisdictions in real time\"; \"NSOPW is not a single national database of all "
          "registered sex offenders\"; and \"NSOPW serves merely as a central search engine "
          "for all public registry websites.\" (U.S. Dep't of Justice, SMART Office, \"NSOPW "
          "vs NSOR\" fact sheet, smart.ojp.gov/nsopw-nsor-fact-sheet.)", "nsopw"),
    ("P", "The same fact sheet states: \"If an offender is not displayed on the "
          "jurisdiction's public registry website, the offender will not appear on NSOPW.\" "
          "A California registrant appears in an NSOPW search result only because, and only "
          "to the extent that, the California Department of Justice has displayed that "
          "person's information on the California Megan's Law website under section 290.46."),
    ("P", "The only single national database of registered sex offenders is the National "
          "Sex Offender Registry (\"NSOR\") maintained by the Federal Bureau of "
          "Investigation's Criminal Justice Information Services Division. According to the "
          "Department of Justice fact sheet, NSOR information is \"available only to law "
          "enforcement and authorized criminal justice agencies.\" On information and belief, "
          "First Advantage is a private screening company, not a law-enforcement or criminal "
          "justice agency, and has no access to NSOR for employment screening.", "nsor"),
    ("P", "On information and belief, outside of law enforcement, California registry "
          "information is made available to the public through the Megan's Law website "
          "maintained under section 290.46, and a private screening company that reports a "
          "record whose source is the California sex offender registry obtained that record, "
          "directly or through NSOPW, from information disclosed pursuant to section 290.46."),

    ("SH", f"C.  Labor Code {S} 432.7(n)"),
    ("P", "Labor Code section 432.7(n) provides, in relevant part: \"This section does not "
          "prohibit an employer, whether a public agency or private individual or corporation, "
          "required by state, federal, or local law to conduct criminal background checks for "
          "employment purposes or to restrict employment based on criminal history from "
          "complying with those requirements, or to prohibit the employer from seeking or "
          "receiving an applicant's criminal history report that has been obtained pursuant "
          "to procedures otherwise provided for under federal, state, or local law.\"",
     "lab_n"),
    ("P", "Section 432.7(n) states what section 432.7 \"does not prohibit.\" It does not "
          "authorize any use of information disclosed under Penal Code section 290.46. Its "
          "first clause applies only to an employer \"required by state, federal, or local law\" "
          "to conduct criminal background checks or to restrict employment based on criminal "
          "history. Its second clause concerns \"seeking or receiving\" a \"criminal history "
          "report\"; it says nothing about using Megan's Law information to deny employment."),

    ("H", "FACTUAL ALLEGATIONS"),
    ("SH", "D.  Plaintiff Applies, Qualifies, and Is Scheduled to Start"),
    ("P", "On July 17, 2024, beginning at approximately 6:46 p.m., Plaintiff applied online "
          "through UPS's applicant system for the position designated \"US - LATHROP HUB "
          "(CALAH) - 75456-Loader/Unloader - Hub - H345 - E&L - Twilight Monday-Friday "
          "15:00-23:30 - External.\" (Ex. 2 at 1.)", "fact_first"),
    ("P", "The position was a Loader/Unloader job inside UPS's Lathrop package hub on the "
          "Twilight shift, Monday through Friday, 3:00 p.m. to 11:30 p.m. On information and "
          "belief, the position involved loading, unloading, and sorting packages inside the "
          "hub; it did not involve entering customers' homes, delivering to residences, or "
          "supervising or caring for children, elders, dependent adults, or any other "
          "identified person at risk.", "position"),
    ("P", "Plaintiff was qualified for the position. He answered UPS's qualification "
          "questions in the affirmative (reliable transportation; ability to perform the "
          "essential functions; work authorization; age 18 or older). (Ex. 2 at 1.) UPS's "
          "system advanced him through every application stage. At 6:53 p.m. on July 17, "
          "2024, he accepted the pay UPS offered for the position (\"I accept this pay\"). "
          "(Ex. 2 at 4.) He completed UPS's policy sign-offs and its safety training video, "
          "which UPS's system described as preparation \"for your first day on the job.\" "
          "(Ex. 2 at 4-5.)"),
    ("P", "At 7:06 p.m. on July 17, 2024, UPS's system scheduled Plaintiff's \"Hired Date\" "
          "appointment for July 22, 2024, 4:00 p.m. to 8:00 p.m. (PDT), at 11800 S. Harlan "
          "Road, Lathrop, California. (Ex. 2 at 5.) UPS then directed him to complete "
          "Section 2 of his Form I-9 \"as soon as possible and before your first day of "
          "work.\" (Id.)", "hired_date"),

    ("SH", "E.  The Disclosure and Authorization Screens"),
    ("P", "At 6:49 p.m. on July 17, 2024, UPS's system presented Plaintiff with three "
          "screens in succession: (a) an \"FCRA Notice\" containing a federal Fair Credit "
          "Reporting Act disclosure followed by an \"Authorization\"; (b) a screen titled "
          "\"FCRA - State Group 1 Disclosure (CA, MN, NJ, OK),\" containing notices for "
          "applicants in California, Minnesota, New Jersey, and Oklahoma, including a "
          "Minnesota statutory-rights notice; and (c) a screen titled \"FCRA California "
          "Disclosure,\" headed \"ADDITIONAL DISCLOSURES FOR CALIFORNIA APPLICANTS.\" "
          "(Ex. 2 at 2-3.) Each screen ended with a statement in substantially this form: "
          "\"I agree that my electronic "
          "signature is the legally binding equivalent to my handwritten signature. By my "
          "electronic signature, I acknowledge that I have carefully reviewed this agreement "
          "and understand its contents,\" followed by \"I agree.\" (Id.)", "screens"),
    ("P", "The \"ADDITIONAL DISCLOSURES FOR CALIFORNIA APPLICANTS\" screen told Plaintiff that "
          "UPS \"may obtain a report about you for employment purposes that is defined under "
          "the California Investigative Consumer Reporting Agencies Act, Cal. Civ. Code "
          f"{S}{S} 1786 to 1786.80, as an 'investigative consumer report,'\" to be prepared by "
          "First Advantage, and that the information \"will be used to evaluate whether you "
          "would present an unacceptable risk of theft or other dishonest behavior in the job "
          "for which you are being considered.\" (Ex. 2 at 3.)", "icraa_screen"),
    ("P", "The California paragraph of the multi-state screen told Plaintiff that, because "
          "the position \"will involve access to confidential financial and other business "
          "information and valuable property belonging to UPS's customers,\" UPS needed a "
          "report \"to evaluate whether you would present an unacceptable risk of theft or "
          "other dishonest behavior in the performance of your job,\" and that UPS intended "
          "to obtain it \"pursuant to section 1024.5(a)(7) of the California Labor Code.\" "
          "It then stated: \"You may elect to receive a copy of the report, free of charge, "
          "by checking the box beneath your signature as indicated below.\" (Ex. 2 at 3.)",
     "box_promise"),
    ("P", "There was no such box. In UPS's own record of the screen, the only thing beneath "
          "the electronic-signature statement is \"I agree.\" (Ex. 2 at 3.) The \"ADDITIONAL "
          "DISCLOSURES FOR CALIFORNIA APPLICANTS\" screen likewise contains no box by which "
          "Plaintiff could request a copy of the report. (Id.) The open squares printed beside "
          "the words \"CALIFORNIA,\" \"MINNESOTA,\" \"NEW JERSEY,\" and \"OKLAHOMA\" on the "
          "multi-state screen are not beneath any signature, are not labeled as a request for "
          "a copy, and show no mark in UPS's record. On information and belief, UPS's "
          "application process gave Plaintiff no means, by a box to check on a written form, "
          "to indicate that he wished to receive a copy of the report, and UPS's records "
          "reflect no such election by Plaintiff.", "no_box"),
    ("P", "On information and belief, UPS did not itself send Plaintiff a copy of the report. "
          "The only access Plaintiff received was a First Advantage portal link sent with the "
          "July 22, 2024 pre-adverse action e-mail described below. That link has since "
          "expired."),
    ("P", "None of UPS's screens identified the searches UPS actually ordered. The FCRA "
          "Notice referred generally to \"a criminal background report, employment history, "
          "driving record, education history, and/or other consumer reports.\" (Ex. 2 at 2.) "
          "The California screen stated only that the report \"may include information on "
          "your character, general reputation, personal characteristics, and mode of living.\" "
          "(Ex. 2 at 3.) No screen told Plaintiff that UPS would order a sex offender registry "
          "search, or a search of a Department of Justice website, as part of the "
          "investigation.", "scope"),
    ("P", "The \"ADDITIONAL DISCLOSURES FOR CALIFORNIA APPLICANTS\" screen lists First "
          "Advantage's mailing address, telephone, fax, e-mail, and \"Web: www.fadv.com\" as "
          "contact information, but it does not tell the consumer that the website is where "
          "the consumer may find information about First Advantage's privacy practices, and "
          "it says nothing about whether the consumer's personal information will be sent "
          "outside the United States or its territories. (Ex. 2 at 3.)", "privacy"),
    ("P", "The California-required disclosures were thus split between the multi-state "
          "screen, which also carried other States' notices and rights, and the California "
          "screen, which also carried an electronic-signature agreement and an acknowledgment "
          "that the applicant had \"carefully reviewed this Agreement.\" (Ex. 2 at 2-3.) "
          "Neither was a document consisting solely of the disclosure."),

    ("SH", "F.  The First Advantage Report"),
    ("P", "UPS ordered the report from First Advantage at 9:52 p.m. Eastern Time on July 17, "
          "2024 (6:52 p.m. Pacific). The report was completed at 6:50 p.m. Eastern Time on "
          "July 18, 2024. It lists the client as \"UNITED PARCEL SERVICE,\" the job profile as "
          "\"H345 - Loader/Unloader - Hub,\" the primary job location as \"US - LATHROP HUB "
          "(CALAH),\" and the package as \"STANDARD PACKAGE.\" (Ex. 1 at 3-4.)", "report_first"),
    ("P", "The report's \"Background Report Summary\" lists each search ordered and its "
          "score: \"Social Security Verification\" -- \"Pass\"; \"First Advantage National "
          "Criminal File Plus STOCKTON, SAN JOAQUIN, CA\" -- \"Eligible\"; and \"National Sex "
          "Offender Registry Search - Department Of Justice Web Site\" -- \"Decisional.\" The "
          "registry searches are the only components marked for review (\"Yes**\"). "
          "(Ex. 1 at 4.)", "summary"),
    ("P", "The criminal-records search returned \"Search Results No Record Found\" and scored "
          "\"Eligible.\" (Ex. 1 at 5.) The report contains no record of any arrest, detention, "
          "or conviction.", "no_crim"),
    ("P", "The registry search's detail block reads, in relevant part: \"National Sex "
          "Offender Registry Search - Department Of Justice Web Site Score: Decisional\"; "
          "\"Record Source NATIONAL SEX OFFENDER REGISTRY\"; \"Search Results Record Found\"; "
          "\"Search Type NATIONAL SEX OFFENDER REGISTRY SEARCH-DEPT OF JUSTICE\"; and, in the "
          "field describing the record returned, \"SOURCE OF RECORD: CALIFORNIA SEX OFFENDER "
          "REGISTRY\" and \"SENTENCE: REGISTERED SEX OFFENDER.\" (Ex. 1 at 6.)", "detail"),
    ("P", "The two source fields report different things. \"Record Source\" identifies the "
          "search that was run. \"SOURCE OF RECORD\" identifies the registry that supplied the "
          "record the search returned: California's."),
    ("P", "On information and belief, the search First Advantage ran for UPS -- labeled a "
          "\"Department Of Justice Web Site\" search -- was a search of NSOPW, the United "
          "States Department of Justice's public website, which returned Plaintiff's "
          "information from the California Megan's Law website in real time as alleged in "
          "paragraphs {nsopw} through {nsor}. In the alternative, on information and belief, "
          "the search was run directly or indirectly against the California Department of "
          "Justice's Megan's Law website. Either way, the record originated in information "
          "disclosed pursuant to Penal Code section 290.46.", "which_site"),
    ("P", "Plaintiff is required to register under Penal Code section 290. On information "
          "and belief, in July 2024 the California Department of Justice displayed "
          "information about Plaintiff on the Megan's Law website pursuant to section 290.46, "
          "and that displayed information is the information First Advantage reported to UPS "
          "as \"SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY.\"", "registrant"),
    ("P", "On July 19, 2024, the report was scored: \"BASED ON YOUR CRITERIA, THE OVERALL "
          "CASE SCORE IS INELIGIBLE,\" with the comment \"Adjudicated by the Centralized "
          "Adjudication Team.\" (Ex. 1 at 4.) \"YOUR CRITERIA\" refers to UPS's criteria. On "
          "information and belief, UPS supplied First Advantage with adjudication criteria "
          "under which a sex offender registry record is \"Decisional\" -- that is, "
          "disqualifying -- for UPS hub positions in California. Because every other component "
          "of the report was clear, the \"INELIGIBLE\" score rests on the California registry "
          "record.", "ineligible"),
    ("P", "The report also carried this remark to UPS: \"City Ordinance, State, or Federal "
          "law requires additional action and disclosure by employer to consumer prior to "
          "taking adverse action based on Consumer Report. FADV cannot provide Adverse Action "
          "letter mailing service on this candidate.\" (Ex. 1 at 4.)"),

    ("SH", "G.  UPS Uses the Registry Record to Deny Plaintiff the Job"),
    ("P", "At 3:59 a.m. on July 21, 2024 -- two days after the \"INELIGIBLE\" score and "
          "before UPS or First Advantage had sent Plaintiff any notice -- UPS's applicant "
          "system recorded Plaintiff's July 22 \"Hired Date\" appointment as \"Cancelled "
          "07/21/2024 03:59AM.\" (Ex. 2 at 5.) On information and belief, UPS cancelled the "
          "appointment because of the \"INELIGIBLE\" score.", "cancel"),
    ("P", "At 9:57 a.m. on July 22, 2024, Plaintiff received an e-mail from First Advantage "
          "(DoNotReply@fadv.com) titled \"Pre Adverse Action Notification regarding your "
          "application with UPS,\" directing him to a First Advantage portal. Reminder e-mails "
          "followed on July 23 and July 27, 2024."),
    ("P", "At 9:57 a.m. on July 31, 2024, Plaintiff received an e-mail from First Advantage "
          "titled \"Final Adverse Action Notification regarding your application with UPS.\" "
          "UPS's applicant system now records Plaintiff's application at the stage "
          "\"Rejected,\" stating: \"This opportunity was not a match at this time.\" "
          "(Ex. 2 at 6.)", "final"),
    ("P", "UPS never identified to Plaintiff any reason for the denial other than the "
          "background report. Nothing else in Plaintiff's application or the report was "
          "disqualifying."),
    ("P", "UPS has since represented to this Court that it \"does not dispute the fact that "
          "it used information derived from Plaintiff's criminal background check when it made "
          "the decision to not hire him\" (UPS's Rule 12(b)(6) Motion to Dismiss, Part IV), "
          "and that \"when UPS learned that Plaintiff was included on the National Sex "
          "Offender Registry, it used that information when making its employment decisions "
          "related to Plaintiff\" (UPS's Reply in Support of Motion to Dismiss, Part II.A). UPS "
          "has also acknowledged that the search \"yielded a result indicating that Plaintiff "
          "was also included on the California Sex Offender Registry.\" (Id.) Because the "
          "criminal-records search found nothing (paragraph {no_crim}), the \"information\" "
          "UPS used was the registry record.", "admission"),

    ("SH", "H.  UPS's Use Was Not Authorized by Section 290.46(j)(1) or Any Other Law"),
    ("P", "UPS did not use the registry information to protect a person at risk. UPS told "
          "Plaintiff in writing that it obtained the report to evaluate \"an unacceptable risk "
          "of theft or other dishonest behavior.\" (Paragraphs {icraa_screen}-{box_promise}.) "
          "A sex offender registration says nothing about theft or dishonesty. UPS invoked "
          "Labor Code section 1024.5(a)(7), a statute governing consumer credit reports. The "
          "position was an in-hub package-handling job with no identified person at risk "
          "(paragraph {position}). The adjudication was a score applied \"BASED ON YOUR "
          "CRITERIA\" by a centralized team, not an assessment of any risk to any identified "
          "person.", "not_j1"),
    ("P", "No federal, state, or local law required UPS to conduct criminal background "
          "checks for, or to restrict employment based on criminal history in, a "
          "Loader/Unloader hub position. UPS ran the check as part of its standard "
          "pre-employment screening, and UPS has not identified any law requiring it. "
          f"Labor Code section 432.7(n) therefore does not apply (paragraphs {{lab_n}}-"
          "{lab_n_end})."),
    ("P", "Labor Code section 432.7 concerns records of arrest, detention, and conviction. "
          "The report contained none (paragraph {no_crim}). A registration status reported "
          "from the California sex offender registry is not a section 432.7 record, and "
          "section 432.7 does not authorize the use of information disclosed pursuant to "
          "Penal Code section 290.46 for employment. Nothing in Penal Code section "
          "290.46(j)(3) or any other provision of law authorized UPS's use."),
    ("P", f"UPS has asserted that it complied with Government Code section 12952 [statute "
          "text not verified for this draft]. Any such compliance would not authorize the use "
          f"of information disclosed pursuant to Penal Code section 290.46, which section "
          "290.46(j)(2) prohibits independently. In any event, on information and belief, UPS "
          "made no individualized assessment of Plaintiff and cancelled his scheduled start "
          "before giving him any notice (paragraph {cancel})."),

    ("SH", "I.  UPS's Conduct Was Deliberate and Is a Continuing Practice"),
    ("P", "UPS is one of the largest employers in the United States. It maintains a "
          "\"Centralized Adjudication Team,\" supplies its own adjudication criteria to its "
          "screening vendor, and includes a \"National Sex Offender Registry Search - "
          "Department Of Justice Web Site\" in its \"STANDARD PACKAGE\" for California hub "
          "positions. (Ex. 1 at 3-4.) On information and belief, UPS applies the same package "
          "and the same criteria -- treating a registry hit as \"Decisional\" -- to applicants "
          "throughout California, so that every California applicant who appears on the "
          "California Megan's Law website is scored ineligible. UPS has maintained in this "
          "action that this use is lawful.", "practice"),
    ("P", "UPS chose to use California Megan's Law information to disqualify Plaintiff "
          "despite the plain prohibition in section 290.46(j)(2)(E), despite its own written "
          "statement that the report was for evaluating theft and dishonesty risk, and "
          "despite its vendor's remark that the law required additional action before adverse "
          "action. Its conduct was knowing and willful."),

    ("SH", "J.  Damages"),
    ("P", "As a direct and proximate result of UPS's conduct, Plaintiff lost the "
          "Loader/Unloader position and the wages and benefits it would have paid, at the "
          "rate UPS offered and Plaintiff accepted on July 17, 2024, from the scheduled July "
          "22, 2024 start forward, in an amount to be proven at trial.", "damages_first"),
    ("P", "Plaintiff also suffered emotional distress, including humiliation, anxiety, and "
          "mental anguish, from being told he was \"Ready to Hire,\" scheduled for his first "
          "day, and then branded \"INELIGIBLE\" and rejected because of information the "
          "Legislature has forbidden employers to use, together with financial hardship to "
          "himself and his household."),
    ("P", "Plaintiff remains subject to registration. He continues to seek warehouse and "
          "package-handling work in the Stockton-Lathrop area, where UPS operates a major hub, "
          "and UPS's rejection notice told him that \"there are many other opportunities at "
          "UPS\" and invited him to \"explore more at UPSjobs.com.\" "
          "(Ex. 2 at 6.) Plaintiff would apply again for UPS hub positions, but UPS's "
          "criteria will again score him \"INELIGIBLE\" on the basis of California Megan's Law "
          "information unless UPS is restrained.", "future"),

    # ------------------------------------------------------------------ COUNT I
    ("H", "FIRST CAUSE OF ACTION\nUse of Megan's Law Information for Employment\n"
          f"(Cal. Penal Code {S} 290.46(j)(2)(E), (j)(4)(A))\n(Against All Defendants)"),
    ("P", "Plaintiff incorporates paragraphs {intro_first} through {facts_end} as though "
          "fully set forth here.", "c1_first"),
    ("P", "The California sex offender registry record that First Advantage reported to UPS "
          "was \"information disclosed pursuant to\" Penal Code section 290.46 (paragraphs "
          "{nsopw}-{nsor} and {detail}-{registrant})."),
    ("P", "UPS used that information for purposes relating to employment: it applied "
          "criteria that scored the record \"Decisional,\" scored Plaintiff \"INELIGIBLE,\" "
          "cancelled his scheduled start, and denied him the position (paragraphs "
          "{ineligible}-{admission})."),
    ("P", "UPS's use was not authorized by section 290.46(j)(1), because it was not made to "
          "protect a person at risk, and was not authorized by any other provision of law, "
          "including Labor Code section 432.7 (paragraphs {not_j1}-{not_auth_end}). The use "
          "therefore was \"for purposes other than those provided by paragraph (1)\" and \"in "
          "violation of paragraph (2)\" within section 290.46(j)(4)(A)."),
    ("P", "UPS's use of the information was a substantial factor in causing Plaintiff's "
          "damages alleged in paragraphs {damages_first} through {damages_end}."),
    ("P", "Under section 290.46(j)(4)(A), UPS is liable to Plaintiff for his actual damages; "
          "for an additional amount, as determined by the jury, not exceeding three times the "
          "amount of actual damage and not less than the statutory minimum; and for "
          "attorney's fees, exemplary damages, or a civil penalty as provided by that "
          "subparagraph. Because UPS's use was knowing and willful (paragraphs "
          "{practice}-{willful_end}), Plaintiff seeks exemplary damages or, in the "
          "alternative, the civil penalty.", "c1_end"),

    # ------------------------------------------------------------------ COUNT II
    ("H", "SECOND CAUSE OF ACTION\nPreventive Relief Against a Pattern or Practice of Misuse\n"
          f"(Cal. Penal Code {S} 290.46(j)(4)(B))\n(Against UPS)"),
    ("P", "Plaintiff incorporates paragraphs {intro_first} through {facts_end} and "
          "{c1_first} through {c1_end} as though fully set forth here."),
    ("P", "The California Megan's Law website is \"an internet website established pursuant "
          "to\" section 290.46. NSOPW searches that website in real time and returns its "
          "information (paragraphs {nsopw}-{nsor}). The registry information UPS used is "
          "\"information available via\" that website."),
    ("P", "There is reasonable cause to believe that UPS is engaged in a pattern or practice "
          "of misuse of that information in violation of section 290.46(j)(2): UPS includes a "
          "sex offender registry search in its standard package for California hub positions; "
          "it supplies criteria under which a registry record is \"Decisional\"; a centralized "
          "team applies those criteria; and UPS maintains in this action that the practice is "
          "lawful (paragraphs {ineligible} and {practice})."),
    ("P", "Plaintiff is a \"person aggrieved by the misuse.\" He was denied employment by it, "
          "remains subject to registration, would apply again for UPS hub positions, and "
          "faces a real and immediate threat that UPS's criteria will again disqualify him "
          "(paragraph {future}). Damages cannot prevent that future misuse."),
    ("P", "Plaintiff is entitled to preventive relief, including a permanent injunction "
          "restraining UPS from using information disclosed pursuant to Penal Code section "
          "290.46 -- including such information obtained through NSOPW or through a screening "
          "vendor reporting the California sex offender registry as the source of record -- "
          "for purposes relating to employment, except as authorized by section 290.46(j)(1) "
          "or another provision of law, and requiring UPS to withdraw any adjudication "
          "criteria that treat such information as disqualifying for California positions."),

    # ------------------------------------------------------------------ COUNT III
    ("H", "THIRD CAUSE OF ACTION\nFailure to Provide a Box to Request a Copy of the Report\n"
          f"(Cal. Civ. Code {S}{S} 1786.16(b)(1), 1786.50)\n(Against All Defendants)"),
    ("P", "Plaintiff incorporates paragraphs {intro_first} through {facts_end} as though "
          "fully set forth here.", "c3_first"),
    ("P", "The First Advantage report was an investigative consumer report within the "
          "Investigative Consumer Reporting Agencies Act, Civil Code section 1786 et seq. "
          "(\"ICRAA\"). UPS itself told Plaintiff that the report it would obtain is defined "
          "under ICRAA \"as an 'investigative consumer report'\" (paragraph {icraa_screen}), "
          "and the report conveyed information on Plaintiff's character, general reputation, "
          "personal characteristics, or mode of living, obtained through public-record and "
          "other searches [Cal. Civ. Code " + S + " 1786.2(c) -- definition not verified for "
          "this draft]. First Advantage, which assembles such reports for a fee, is an "
          "investigative consumer reporting agency."),
    ("P", "UPS requested and procured the report for employment purposes, and is a person "
          "described in subdivision (d) of Civil Code section 1786.12."),
    ("P", "Civil Code section 1786.16(b)(1) requires the employer to \"Provide the consumer a means "
          "by which the consumer may indicate on a written form, by means of a box to check, "
          "that the consumer wishes to receive a copy of any report that is prepared.\""),
    ("P", "UPS did not do so. Its own screen promised a \"box beneath your signature,\" but "
          "none existed, and no other form gave Plaintiff a box to check to request a copy "
          "(paragraphs {box_promise}-{no_box})."),
    ("P", "Civil Code section 1786.50(a) provides that a \"user of information that fails to "
          "comply with any requirement under this title with respect to an investigative "
          "consumer report is liable to the consumer who is the subject of the report in an "
          "amount equal to the sum of all the following: (1) Any actual damages sustained by "
          "the consumer as a result of the failure or, except in the case of class actions, "
          "ten thousand dollars ($10,000), whichever sum is greater. (2) In the case of any "
          "successful action to enforce any liability under this chapter, the costs of the "
          "action together with reasonable attorney's fees as determined by the court.\"",
     "icraa_50"),
    ("P", "Section 1786.50(b) provides: \"If the court determines that the violation was "
          "grossly negligent or willful, the court may, in addition, assess, and the consumer "
          "may recover, punitive damages.\" UPS's violation was at least grossly negligent: "
          "UPS drafted a screen that told applicants to check a box UPS never provided."),
    ("P", "Plaintiff is entitled to the greater of his actual damages or the statutory amount "
          "under section 1786.50(a)(1), costs, any attorney's fees recoverable, and punitive "
          "damages under section 1786.50(b).", "c3_end"),

    # ------------------------------------------------------------------ COUNT IV
    ("H", "FOURTH CAUSE OF ACTION\nDeficient Investigative Consumer Report Disclosure\n"
          f"(Cal. Civ. Code {S}{S} 1786.16(a)(2)(B), 1786.50)\n(Against All Defendants)"),
    ("P", "Plaintiff incorporates paragraphs {intro_first} through {facts_end} and "
          "{c3_first} through {c3_end} as though fully set forth here."),
    ("P", "Civil Code section 1786.16(a)(2)(B) permitted UPS to procure the report only if "
          "UPS first provided \"a clear and conspicuous disclosure in writing to the consumer "
          "at any time before the report is procured or caused to be made in a document that "
          "consists solely of the disclosure,\" that, among other things, \"(v) Notifies the "
          "consumer in writing of the nature and scope of the investigation requested, "
          "including a summary of the provisions of Section 1786.22,\" and \"(vi) Notifies the "
          "consumer of the Internet Web site address of the investigative consumer reporting "
          "agency identified in clause (iv), or, if the agency has no Internet Web site "
          "address, the telephone number of the agency, where the consumer may find "
          "information about the investigative reporting agency's privacy practices, "
          "including whether the consumer's personal information will be sent outside the "
          "United States or its territories.\""),
    ("P", "UPS procured the report without satisfying those conditions:"),
    ("L", "(a) Not a document consisting solely of the disclosure. The California-required "
          "content was spread across a multi-state screen carrying other States' notices and "
          "rights and a California screen carrying an electronic-signature agreement and an "
          "acknowledgment that the applicant had reviewed \"this Agreement\" (paragraphs "
          "{screens}-{icraa_screen} and {privacy_end}). See Gilberg v. California Check "
          "Cashing Stores, LLC, 913 F.3d 1169 (9th Cir. 2019) [pin cite unverified]."),
    ("L", "(b) No notice of the nature and scope of the investigation requested. UPS never "
          "disclosed that it would order a sex offender registry search or a search of a "
          "Department of Justice website, the very search on which it denied Plaintiff "
          "employment (paragraph {scope})."),
    ("L", "(c) No privacy-practices notice. The California disclosure did not identify the "
          "website where Plaintiff could find First Advantage's privacy practices or say "
          "whether his personal information would be sent outside the United States "
          "(paragraph {privacy})."),
    ("P", "Each failure is a failure to \"comply with any requirement under this title with "
          "respect to an investigative consumer report\" within section 1786.50(a). On "
          "information and belief, UPS uses the same screens for California applicants "
          "statewide and adopted them knowingly; the violations were willful or, at minimum, "
          "grossly negligent."),
    ("P", "Plaintiff is entitled to the greater of his actual damages or the statutory amount "
          "under section 1786.50(a)(1), costs, any attorney's fees recoverable, and punitive "
          "damages under section 1786.50(b)."),
    ("P", "Plaintiff asserts no claim in this action under 15 U.S.C. " + S + " 1681n or "
          + S + " 1681o."),

    # ------------------------------------------------------------------ PRAYER
    ("H", "PRAYER FOR RELIEF"),
    ("U", "WHEREFORE, Plaintiff BRENDAN NGEHSI NEWANFORBI prays for judgment against "
          "Defendant UNITED PARCEL SERVICE, INC. and DOES 1 through 10, inclusive, as follows:"),
    ("L", "1.  On the First Cause of Action: actual damages, including lost wages and "
          "benefits and damages for emotional distress, according to proof; an additional "
          "amount as determined by the jury, not exceeding three times the amount of actual "
          f"damage and not less than the minimum provided by Penal Code section "
          "290.46(j)(4)(A); and exemplary damages or, in the alternative, a civil penalty, as "
          "provided by Penal Code section 290.46(j)(4)(A);"),
    ("L", "2.  On the Second Cause of Action: preventive relief under Penal Code section "
          "290.46(j)(4)(B), including a permanent injunction as described in this pleading;"),
    ("L", "3.  On the Third and Fourth Causes of Action: on each cause of action, the greater "
          "of actual damages or the amount provided by Civil Code section 1786.50(a)(1), and "
          "punitive damages under Civil Code section 1786.50(b);"),
    ("L", f"4.  Costs of suit, and attorney's fees to the extent recoverable under Penal Code "
          "section 290.46(j)(4)(A) or Civil Code section 1786.50(a)(2);"),
    ("L", "5.  Prejudgment and post-judgment interest as permitted by law; and"),
    ("L", "6.  Such other and further relief as the Court deems just and proper."),

    ("H", "DEMAND FOR JURY TRIAL"),
    ("U", "Under Federal Rule of Civil Procedure 38(b), Plaintiff BRENDAN NGEHSI NEWANFORBI "
          "demands a trial by jury on all claims and issues so triable."),
]

# Labels that close a range: the paragraph immediately before a section break.
# Resolved as "last numbered paragraph before label X".
END_ALIASES = {
    "facts_end": "c1_first",          # last para before Count I
    "lab_n_end": "fact_first",        # last para of 432.7 discussion
    "not_auth_end": "practice",       # last para of section H
    "willful_end": "damages_first",   # last para of section I
    "damages_end": "c1_first",        # last para of section J (= facts_end)
    "privacy_end": "report_first",    # 'Neither was a document...' para
}


def number_paragraphs(content):
    labels, n = {}, 0
    for item in content:
        if item[0] == "P":
            n += 1
            if len(item) > 2:
                labels[item[2]] = n
    for alias, nxt in END_ALIASES.items():
        labels[alias] = labels[nxt] - 1
    return labels


def _header_block(d: PleadingPaper) -> None:
    c = d.c
    y0 = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, y0 - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()


def _render(d: PleadingPaper, labels: dict) -> None:
    n = 0
    for item in CONTENT:
        kind, text = item[0], item[1]
        if kind == "P":
            n += 1
            body = text.format(**labels)
            d.write_wrapped(f"{n}.  {body}", first_indent=36)
            d.blank_line()
        elif kind == "H":
            lines = text.split("\n")
            # Keep the jury demand on the signature page.
            d.ensure_space(17 if text == "DEMAND FOR JURY TRIAL" else len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SH":
            d.ensure_space(4)
            d.write_line(text, bold=True)
            d.blank_line()
        elif kind == "Q":
            d.write_wrapped(text, indent=36, first_indent=0, right_inset=52)
            d.blank_line()
        elif kind == "U":
            d.write_wrapped(text.format(**labels), first_indent=36)
            d.blank_line()
        elif kind == "L":
            d.write_wrapped(text.format(**labels), indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(kind)


def _signature(d: PleadingPaper) -> None:
    d.ensure_space(10)
    d.write_line(DATE_LINE)
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1],
                           SIG_LINE, width=220, x_offset=15)
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _extract(src: Path, pages: list[int], out: Path) -> Path:
    r = PdfReader(str(src))
    w = PdfWriter()
    for p in pages:
        w.add_page(r.pages[p - 1])
    with open(out, "wb") as fh:
        w.write(fh)
    return out


def build(out: Path) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing canonical signature: {SIGNATURE_PATH}")
    labels = number_paragraphs(CONTENT)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        body = td / "body.pdf"
        d = PleadingPaper(str(body), doc_title_footer=FOOTER)
        _header_block(d)
        _render(d, labels)
        _signature(d)
        d.save()

        parts = [body]
        exhibits = [
            ("1", "First Advantage Background Report", EX1_PAGES,
             ["As filed by UPS, Felsing Decl. Ex. A (ECF No. 7-2 at 4-9)",
              "Ordered July 17, 2024; scored July 19, 2024"]),
            ("2", "UPS Applicant-System Record (Excerpts)", EX2_PAGES,
             ["As filed by UPS, Felsing Decl. Ex. B (ECF No. 7-2 at 11, 16-18, 23-24)",
              "Position, disclosure screens, pay, Hired Date, Rejected stage"]),
        ]
        for mark, title, pages, details in exhibits:
            cover = write_exhibit_cover(
                td / f"cover{mark}.pdf",
                court=COURT_LINE1,
                court_line2=COURT_LINE2,
                caption="NEWANFORBI v. UNITED PARCEL SERVICE, INC.",
                case_no=CASE_NO,
                exhibit=mark,
                title=title,
                details=details,
                footer="First Amended Complaint -- Newanforbi v. United Parcel Service, Inc.",
            )
            parts += [cover, _extract(FELSING_PDF, pages, td / f"ex{mark}.pdf")]
        assemble(parts, out)
    return out


def main() -> None:
    out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUT
    print(f"Generated FAC draft: {build(out)}")


if __name__ == "__main__":
    main()
