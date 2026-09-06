#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 38 — verified complaint, Swift Transportation Co. of Arizona LLC.

San Joaquin Superior Court. The decrypted Sept. 26, 2023 pre-adverse packet
is in hand. NSOPW remained Processing. Plaintiff pleads on information and
belief that Swift used preliminary sex-offender-registry information from
that in-process component, in whole or in part, in the denial. ICRAA and
UCL remain independent paths.

Default output is unsigned. On or after September 8, 2026, rerun with
``--execute`` only after Plaintiff confirms the role.

    python3 internal/scripts/matter38-swift-complaint.py
    python3 internal/scripts/matter38-swift-complaint.py --execute
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

_DRAFT_NOTE = re.compile(r"\s*\[[^\[\]]+\]")


def _filing_text(text: str, execute: bool) -> str:
    if not execute:
        return text
    return _DRAFT_NOTE.sub("", text).rstrip()

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-38"
    / "Verified Complaint - Ngwa Nforbi v Swift Transportation Co of Arizona LLC"
    " (Sep 8 2026).pdf"
)
DEFAULT_EXEC_DATE = "September 8, 2026"
EARLIEST_EXECUTION_DATE = dt.date(2026, 9, 8)
COURT_LINE2 = "COUNTY OF SAN JOAQUIN"
FOOTER = "VERIFIED COMPLAINT -- BRENDAN NGWA NFORBI v. SWIFT TRANSPORTATION CO. OF ARIZONA LLC"

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
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
    ("SWIFT TRANSPORTATION CO. OF", True, False),
    ("ARIZONA LLC, a limited liability", True, False),
    ("company, d/b/a SWIFT", True, False),
    ("TRANSPORTATION; and DOES 1", True, False),
    ("through 20, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. _________________", False, False),
    ("", False, False),
    ("VERIFIED COMPLAINT FOR", True, False),
    ("DAMAGES, DECLARATORY AND", True, False),
    ("INJUNCTIVE RELIEF", True, False),
    ("", False, False),
    ("(1) ICRAA, Civ. Code", False, False),
    ("      § 1786.40;", False, False),
    ("(2) CCRAA, Civ. Code", False, False),
    ("      § 1785.20.5;", False, False),
    ("(3) UCL, B&P Code § 17200;", False, False),
    ("(4) Penal Code § 290.46(j)", False, False),
    ("      (I&B — preliminary", False, False),
    ("      NSOPW / registry)", False, False),
    ("", False, False),
    ("[Unlimited Civil]", False, True),
    ("[Jury Trial Demanded]", False, True),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

CONTENT = [
    (
        "NOTICE",
        "REVIEW DRAFT — DO NOT FILE OR SIGN BEFORE SEPTEMBER 8, 2026. "
        "THE SEPTEMBER 26, 2023 PRE-ADVERSE PACKET HAS BEEN DECRYPTED. "
        "NSOPW REMAINED PROCESSING. THE SECTION 290.46(j) COUNT IS "
        "PLEADED ON INFORMATION AND BELIEF THAT SWIFT USED PRELIMINARY "
        "SEX-OFFENDER-REGISTRY INFORMATION FROM THAT IN-PROCESS COMPONENT. "
        "CONFIRM THE DRIVER ROLE.",
    ),
    ("PARA", 'Plaintiff BRENDAN NGWA NFORBI ("Plaintiff") alleges as follows:'),
    ("HEADER", "I.\nINTRODUCTION"),
    (
        "PARA",
        "1. This is an action under Penal Code section 290.46, subdivision (j), "
        "the California Investigative Consumer Reporting Agencies Act, and the "
        "Unfair Competition Law. In September 2023, Plaintiff applied to Swift "
        "Transportation Co. of Arizona LLC for a Class A Driver position. On "
        "September 26, 2023, Swift sent a pre-adverse packet whose National "
        "Sex Offender Public Website component remained 'Processing.' On "
        "October 5, 2023, Swift sent a post-adverse letter admitting that "
        "consumer reports from Asurint, Tenstreet, DriverIQ, FMCSA-DOT, and "
        "Equifax Work Number caused the denial. Plaintiff is informed and "
        "believes, and on that basis alleges, that Swift's decision was based "
        "in whole or in part on preliminary information from that report "
        "citing a sex-offender registry.",
    ),
    (
        "PARA",
        "2. The September 26, 2023 pre-adverse packet has been decrypted. "
        "Plaintiff alleges its contents as known facts. The packet does not "
        "state 'SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY.' The "
        "National Criminal search run without a sex-offender component "
        "returned Clear / No Reportable Records Found. Federal criminal "
        "returned Clear. The county criminal searches that had completed "
        "returned Clear. The National Sex Offender Public Website component "
        "remained 'Processing' on every snapshot in the packet. It never "
        "completed. It reported no hit. Clearinghouse returned Driver Not "
        "Prohibited. What the packet does contain — a Class A commercial "
        "driver's license, an April 22, 2022 improper-lane moving violation "
        "with zero points, PSP inspection history, and a CDLIS license-"
        "identity match — is not information disclosed pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "3. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk. "
        "Subdivision (j)(2)(E) prohibits use of that information for purposes "
        "relating to employment, except as another law authorizes. A "
        "commercial-driver hiring decision is a purpose relating to employment.",
    ),
    (
        "PARA",
        "4. Federal motor-carrier screening does not swallow this claim. The "
        "FMCSA Drug and Alcohol Clearinghouse and the Pre-Employment Screening "
        "Program concern drug-and-alcohol violations and crash or inspection "
        "history. They are not Penal Code section 290.46 disclosures. An "
        "employer that may lawfully obtain ordinary criminal-history or "
        "safety records is not thereby authorized to use Megan's Law website "
        "information for employment. Penal Code section 290.46(j)(3) says so. "
        "This count does not ask the Court to forbid Swift from using the "
        "Clearinghouse, PSP, CDLIS, or other federally required or permitted "
        "safety databases. It asks the Court to forbid employment use of "
        "information disclosed pursuant to Penal Code section 290.46. Federal "
        "motor-carrier regulations do not preempt that narrower claim and do "
        "not authorize Megan's Law use.",
    ),
    (
        "PARA",
        "5. Plaintiff does not allege that the decrypted packet contains a "
        "completed NSOPW hit or the words 'SOURCE OF RECORD: CALIFORNIA SEX "
        "OFFENDER REGISTRY.' He does allege, on information and belief, that "
        "Swift used preliminary information from the still-Processing NSOPW "
        "component — information citing a sex-offender registry, including "
        "information disclosed pursuant to Penal Code section 290.46 or a "
        "derivative national compilation whose source was the California "
        "registry — in whole or in part in the denial. Code of Civil "
        "Procedure section 425.10 requires a statement of the facts "
        "constituting the cause of action in ordinary and concise language. "
        "Section 452 requires this Court to construe the pleading liberally. "
        "The vendor adjudication log, interim NSOPW return, and "
        "decision-maker communications are exclusively in Defendants' "
        "possession. Information disclosed pursuant to Penal Code section "
        "290.46 does not lose that character because a vendor also searched "
        "the National Sex Offender Public Website or another public "
        "sex-offender compilation. Searching a public website is not a free "
        "pass. Subdivision (j)(3)'s reference to publicly available "
        "information does not authorize employment use of Megan's Law "
        "disclosures. The prohibition is on use of information disclosed "
        "pursuant to section 290.46 for purposes relating to employment.",
    ),
    (
        "PARA",
        "6. Plaintiff is a person as to whom information is disclosed on the "
        "California Megan's Law website. He does not possess any completed "
        "NSOPW result from Swift. The vendor adjudication log, any later "
        "NSOPW return, and the decision-maker communications are exclusively "
        "in Defendants' possession. He will seek them in discovery.",
    ),
    (
        "PARA",
        "7. Plaintiff does not name Knight-Swift Transportation Holdings, Inc., "
        "or any other parent, merely because it owns affiliated entities. He "
        "has sued DOES 1 through 10 for the consumer reporting agency that "
        "actually returned registry-derived information and for any Swift "
        "affiliate that was the actual employing or decision-making entity.",
    ),
    (
        "PARA",
        "8. This Complaint does not plead a Tameny wrongful-termination or "
        "failure-to-hire count, an IIED count, a Fair Credit Reporting Act "
        "count, a contract or promissory-estoppel count, or a FEHA or "
        "Government Code section 12952 Fair Chance Act count. The Fair "
        "Chance reservation is not a count. Plaintiff will timely exhaust "
        "California Civil Rights Department rights and seek leave to amend "
        "if discovery shows Swift considered conviction history before any "
        "conditional offer, or used conviction history without the "
        "individualized assessment and notices section 12952 requires. The "
        "section 290.46(j) count is pleaded on information and belief that "
        "Swift used preliminary sex-offender-registry information from the "
        "in-process NSOPW component. Civil Code sections 1786.40 and "
        "1786.50, Civil Code section 1785.20.5, and Business and Professions "
        "Code section 17200 are independent paths that do not require a "
        "completed registry hit. ICRAA and CCRAA are pleaded in the "
        "alternative so the claim survives whether the reports were "
        "investigative or ordinary consumer reports. Plaintiff does not "
        "presently plead Labor Code section 432.7 or section 1198.5. He "
        "has not alleged that any report used an arrest that did not result "
        "in a conviction, diversion, or a dismissed conviction, and he has "
        "not yet served a section 1198.5 inspection request. He preserves "
        "leave to amend if the file later supports those reserved theories.",
    ),
    ("HEADER", "II.\nPARTIES"),
    (
        "PARA",
        "9. Plaintiff BRENDAN NGWA NFORBI is a natural person residing in "
        "Stockton, San Joaquin County, California. He is also identified in "
        "employment and court records as Brendan Ngehsi Ngwa Nforbi and "
        "Brendan Ngehsi Ngwanforbi. Those name variants refer to Plaintiff.",
    ),
    (
        "PARA",
        "10. Plaintiff is required to register under California Penal Code "
        "section 290. At all times relevant to this Complaint, information "
        "identifying him appeared on California's Megan's Law website and "
        "California Sex Offender Registry, operated pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "11. Defendant SWIFT TRANSPORTATION CO. OF ARIZONA LLC ('Swift') is a "
        "limited liability company that does business as Swift Transportation. "
        "Its October 5, 2023 letter lists 2200 South 75th Avenue, Phoenix, "
        "Arizona 85043. On September 25, 2023, the FMCSA Clearinghouse "
        "identified the querying employer as SWIFT TRANSPORTATION CO OF "
        "ARIZONA LLC, USDOT number 54283. On information and belief, Swift "
        "is qualified to transact business in California and was the entity "
        "that recruited Plaintiff, ordered the reports, and made the "
        "employment decision challenged here.",
    ),
    (
        "PARA",
        "12. On information and belief, Swift's designated agent for service "
        "of process in California is National Registered Agents, Inc. "
        "Plaintiff will serve Swift through the agent listed on the California "
        "Secretary of State record as of the date of service. Service is not "
        "to be made at a terminal or recruiter's phone number merely because "
        "that is how Plaintiff first heard from Swift.",
    ),
    (
        "PARA",
        "13. The true names and capacities of DOES 1 through 20 are unknown to "
        "Plaintiff, who therefore sues them by fictitious names under Code of "
        "Civil Procedure section 474. DOES 1 through 10 include the consumer "
        "reporting agency, investigative consumer reporting agency, or other "
        "vendor that assembled, evaluated, furnished, or scored background "
        "information about Plaintiff for Swift — including, if discovery so "
        "shows, Asurint, Tenstreet, LLC, DriverIQ / Cisive, or Equifax "
        "Workforce Solutions — and the individuals who ordered, reviewed, or "
        "acted on that information. Plaintiff will amend when their identities "
        "and roles are ascertained.",
    ),
    (
        "PARA",
        "14. Robin Kaufman and Matt Hutto communicated with Plaintiff as "
        "Swift driver recruiters. They are percipient witnesses, not presently "
        "named as defendants. Matt Hutto's message used a Class A Recruiting "
        "address while stating it was sent on behalf of Swift Transportation "
        "Co. of Arizona LLC by Tenstreet, LLC.",
    ),
    (
        "PARA",
        "15. Plaintiff is informed and believes that each DOE Defendant "
        "participated in, authorized, directed, furnished information for, "
        "implemented, concealed, or ratified one or more acts alleged and is "
        "legally responsible for the resulting harm.",
    ),
    ("HEADER", "III.\nJURISDICTION AND VENUE"),
    (
        "PARA",
        "16. This Court has subject-matter jurisdiction under article VI, "
        "section 10 of the California Constitution and Code of Civil Procedure "
        "section 410.10.",
    ),
    (
        "PARA",
        "17. This action is properly designated unlimited civil under Code of "
        "Civil Procedure sections 85 and 88 because the aggregate relief sought "
        "exceeds $35,000, exclusive of interest and costs. No specific "
        "personal-injury or punitive-damages amount is pleaded.",
    ),
    (
        "PARA",
        "18. This Court has personal jurisdiction over Swift because Swift "
        "recruited Plaintiff, a California resident, for work; caused "
        "consumer reports to be procured about a California resident; sent "
        "the pre-adverse and post-adverse communications to Plaintiff in "
        "California; and is, on information and belief, qualified to do "
        "business in California.",
    ),
    (
        "PARA",
        "19. Venue is proper in the County of San Joaquin under Code of Civil "
        "Procedure sections 395 and 395.5 because Plaintiff resides here, he "
        "received the recruiting, screening, and adverse-action "
        "communications here, and the liability and injury arose here.",
    ),
    (
        "PARA",
        "20. Plaintiff has not pleaded a federal claim. This Complaint is a "
        "California statutory action belonging in this Court.",
    ),
    ("HEADER", "IV.\nTIMELINESS"),
    (
        "PARA",
        "21. Penal Code section 290.46 does not prescribe its own limitations "
        "period. This action upon a liability created by that statute is timely "
        "under Code of Civil Procedure section 338, subdivision (a), which "
        "requires that such an action, other than a penalty or forfeiture, be "
        "commenced within three years after accrual.",
    ),
    (
        "PARA",
        "22. The cause of action accrued, if at all, when Swift used registry "
        "information for purposes relating to Plaintiff's employment — that "
        "is, on the date of the employment decision, not on the date of "
        "application, and not on the date Plaintiff first registered under "
        "section 290.",
    ),
    (
        "PARA",
        "23. Swift's written post-adverse letter is dated October 5, 2023, "
        "at 5:09 a.m. Swift Recruiting emailed that letter the same day. "
        "Three years from October 5, 2023, is October 5, 2026. Swift "
        "Recruiting emailed a password-protected pre-adverse letter on "
        "September 26, 2023. Three years from that earlier date is September "
        "26, 2026. This Complaint is prepared for execution on September 8, "
        "2026, inside both dates. [PLAINTIFF MUST NOT DELAY PAST SEPTEMBER "
        "26, 2026 IF HE TREATS THE PRE-ADVERSE LETTER AS ACCRUAL.]",
    ),
    (
        "PARA",
        "24. Plaintiff does not concede that Code of Civil Procedure section "
        "335.1 or section 340, subdivision (a), supplies the limitations period "
        "for the section 290.46(j) count. The actual-damages and discretionary "
        "enhancement authorized by section 290.46(j)(4)(A) are a liability "
        "created by statute, not an action upon a statute for a penalty. The "
        "labeled civil-penalty slice of subdivision (j)(4)(A) is pleaded in "
        "the alternative and is not the sole theory. He does not plead a "
        "Tameny or personal-injury count. A two-year clock from September 26 "
        "or October 5, 2023, would have closed in 2025. He has not pleaded "
        "the Fair Credit Reporting Act; the two-year FCRA discovery clock "
        "from those same 2023 letters would likewise have closed.",
    ),
    (
        "PARA",
        "24A. Civil Code section 1786.52 requires that an ICRAA action be "
        "brought within two years from the date the plaintiff knew or should "
        "have known of the violation. The September 26 and October 5, 2023 "
        "letters described consumer reports. They did not advise that an "
        "investigative consumer report had been obtained. Plaintiff did not "
        "then possess a complete investigative-consumer-report file and did "
        "not know the NSOPW component remained Processing until the encrypted "
        "attachment was later decrypted. The face of this Complaint does not "
        "establish that discovery date. If Defendants interpose section "
        "1786.52, the date is a fact to be proven; it does not appear from "
        "the pleading as a complete bar.",
    ),
    (
        "PARA",
        "24B. The Unfair Competition Law claim is timely under Business and "
        "Professions Code section 17208's four-year period. That period is "
        "independent of any shorter period that may apply to a borrowed "
        "predicate. The UCL count is not pleaded to resurrect a time-barred "
        "statutory right. It is pleaded as an independent equitable claim "
        "for ongoing standardized screening practices and for restitution of "
        "any vested money or property Defendants acquired.",
    ),
    ("HEADER", "V.\nCOMMON FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. The Swift Application"),
    (
        "PARA",
        "25. On Friday, September 22, 2023, at 3:02 p.m., Robin Kaufman, "
        "identifying herself as a Swift Transportation Driver Recruiter, "
        "emailed Plaintiff that she had received his information and asked "
        "him to complete the full application. The message was sent on "
        "behalf of Swift Transportation Co. of Arizona LLC by Tenstreet, LLC, "
        "120 W. 3rd Street, Tulsa, Oklahoma 74103. Her stated direct line was "
        "623-907-7414 and her address robin_kaufman@swifttrans.com.",
    ),
    (
        "PARA",
        "26. That same evening, at 10:03 p.m., Matt Hutto, also identifying "
        "himself as a Swift Driver Recruiter, emailed that he was trying to "
        "reach Plaintiff at the number Plaintiff had provided, asked him to "
        "complete the full driver application, and gave 803-564-3092 as a "
        "return number. The message used Mhutto@classarecruitinginc.com and "
        "was likewise sent on behalf of Swift Transportation Co. of Arizona "
        "LLC by Tenstreet, LLC.",
    ),
    (
        "PARA",
        "27. The application was for a Class A Driver position. The file does "
        "not contain the completed application, a written offer, a terminal "
        "assignment, or a rate of pay.",
    ),
    ("SUBHEAD", "B. The September 25, 2023 Screen"),
    (
        "PARA",
        "28. On Monday, September 25, 2023, at 11:54 a.m., Tenstreet notified "
        "Plaintiff that a DriverIQ employment background document ordered in "
        "connection with Swift was available in Driver Pulse.",
    ),
    (
        "PARA",
        "29. Four minutes later, at 11:58 a.m., the FMCSA Office of Safety "
        "Programs emailed Plaintiff that SWIFT TRANSPORTATION CO OF ARIZONA "
        "LLC (USDOT# 54283) had requested access to his FMCSA Drug and "
        "Alcohol Clearinghouse record. The email warned that refusal would "
        "prohibit him from operating a commercial motor vehicle or performing "
        "other safety-sensitive functions for Swift.",
    ),
    (
        "PARA",
        "30. At 1:20 p.m. the same day, Tenstreet notified Plaintiff that his "
        "FMCSA Clearinghouse result ordered by Swift Transportation Co. of "
        "Arizona LLC was available for review. The decrypted pre-adverse "
        "packet includes a Clearinghouse result of Driver Not Prohibited, "
        "with no open violations.",
    ),
    (
        "PARA",
        "31. The Clearinghouse query is alleged as proof that Swift was then "
        "treating Plaintiff as a prospective commercial-driver hire and was "
        "running federally required safety screens. It is not alleged to be "
        "a Penal Code section 290.46 disclosure. Clearinghouse records "
        "concern drug and alcohol program violations, not Megan's Law.",
    ),
    ("SUBHEAD", "C. The Pre-Adverse and Post-Adverse Letters"),
    (
        "PARA",
        "32. On Tuesday, September 26, 2023, at 3:09 a.m., Swift Recruiting "
        "(recruitadmin@swifttrans.com) emailed Plaintiff a message titled "
        "'Swift Transportation - FCRA,' addressed to Brendan Ngehsi Ngwa "
        "Nforbi, stating that an important communication was attached as "
        "Pre_Adverse_Action_Letter_76326281-1916808-encrypted.pdf and that "
        "the password was the last four digits of his Social Security number.",
    ),
    (
        "PARA",
        "33. The pre-adverse attachment has been decrypted. It is a composite "
        "screening packet, not a blank cover letter. It includes completed "
        "criminal-file components returning Clear, an NSOPW component that "
        "remained Processing on every snapshot, a Clearinghouse result of "
        "Driver Not Prohibited, an MVR, PSP inspection history, and CDLIS "
        "license-identity information. Plaintiff does not republish "
        "identifiers from that packet in this pleading. He alleges the "
        "adjudication results as known facts.",
    ),
    (
        "PARA",
        "34. On Thursday, October 5, 2023, at 3:09 a.m., Swift Recruiting "
        "emailed Plaintiff a second 'Swift Transportation - FCRA' message, "
        "this time attaching Post_Adverse_Action_Letter_76326281-1916809_em.pdf.",
    ),
    (
        "PARA",
        "35. The enclosed letter is on Swift Transportation Co. of Arizona LLC "
        "letterhead, dated October 5, 2023, 5:09 a.m., and addressed to "
        "Brendan Ngehsi Nforbi at 1455 Cat Tail Drive, Stockton, California "
        "95204. It states that offers of employment at Swift are contingent "
        "upon successful completion of a background check, and that the "
        "letter 'serves as notification that we have decided not to employ "
        "you or have decided to take other adverse action based in whole or "
        "in part on a consumer report received from a consumer reporting "
        "agency.'",
    ),
    (
        "PARA",
        "36. The letter states that Asurint (Cleveland, Ohio), Tenstreet "
        "(Tulsa, Oklahoma), DriverIQ (Tulsa, Oklahoma; disputes at Cisive), "
        "FMCSA-DOT, and The Work Number / Equifax Workforce Solutions "
        "'provided us with consumer reports which, in whole or in part, "
        "influenced our employment decision.' It states those agencies "
        "played no part in the decision other than providing the reports.",
    ),
    (
        "PARA",
        "37. The October 5 letter says a copy of the consumer report and a "
        "Summary of Rights were attached. The decrypted September 26 packet "
        "is the report-side paper in Plaintiff's files. It does not contain "
        "a completed NSOPW result, a California Sex Offender Registry source "
        "line, or a separate later Asurint, Tenstreet, or DriverIQ printout "
        "showing a registry hit. Civil Code sections 1786.10 and 1786.22 "
        "entitle Plaintiff to inspect the files those agencies maintain on "
        "him. Plaintiff has not yet served those inspection requests. He will.",
    ),
    (
        "PARA",
        "38. The California disclosure in that packet states that Swift may "
        "order a consumer report or investigative consumer report including "
        "'federal criminal history, state criminal history, [and] public "
        "court records,' and names the same agencies. Criminal-history and "
        "court-record searches are not this claim. This claim is the use of "
        "information disclosed pursuant to Penal Code section 290.46.",
    ),
    ("SUBHEAD", "D. Facts Supporting the Registry-Use Inference"),
    (
        "PARA",
        "39. Plaintiff is a person as to whom information is disclosed on the "
        "California Megan's Law website. That website, and the statute that "
        "created it, warn that the information may not be used for employment.",
    ),
    (
        "PARA",
        "40. Swift is a national motor carrier. On information and belief, it "
        "maintains written background-screening policies for driver applicants, "
        "contracts with the agencies named in its October 5 letter, and "
        "adjudicates hits through a centralized process rather than by ad hoc "
        "decision of a single recruiter.",
    ),
    (
        "PARA",
        "41. On information and belief, the ordinary Swift driver screen in "
        "2023 included a search, or caused a vendor to search, sex-offender "
        "registry or Department of Justice public-notification sources, "
        "including sources that republish or are derived from California "
        "Penal Code section 290.46 disclosures.",
    ),
    (
        "PARA",
        "42. Plaintiff does not attach a completed NSOPW result because the "
        "packet furnished to him does not contain one. Swift's adjudication "
        "log and any later NSOPW return are the documents that will confirm "
        "or refute preliminary registry use. They are exclusively in "
        "Defendants' possession.",
    ),
    (
        "PARA",
        "43. The NSOPW component was still Processing. A search that never "
        "completed is not a completed 'no record' result. It is also not a "
        "completed printed hit. Plaintiff is informed and believes, and on "
        "that basis alleges, that Swift or a DOE obtained, displayed, "
        "scored, or was informed of preliminary information from that "
        "in-process NSOPW component citing a sex-offender registry — "
        "including information disclosed pursuant to Penal Code section "
        "290.46 or a derivative national compilation whose source of record "
        "was the California registry — and used that preliminary information "
        "in whole or in part in the October 5, 2023 decision.",
    ),
    (
        "PARA",
        "44. The basis for paragraph 43 is the combination of: Swift ordered "
        "an NSOPW sex-offender-website search; that component remained "
        "Processing on every snapshot in the packet sent with the "
        "pre-adverse notice; Swift then denied employment based in whole or "
        "in part on consumer reports; the completed criminal, Clearinghouse, "
        "and MVR components that are in the packet do not themselves "
        "explain a registry-based denial; Plaintiff was then listed on the "
        "California Megan's Law website; and the interim NSOPW return, "
        "adjudication notes, and "
        "decision-maker communications are exclusively in Defendants' "
        "possession.",
    ),
    (
        "PARA",
        "45. Swift admitted in writing that the denial was based in whole "
        "or in part on consumer reports. Civil Code section 1786.40(a) "
        "required, if an investigative consumer report had been obtained, "
        "that Swift advise Plaintiff that an investigative consumer report "
        "had been obtained and supply the name and address of the "
        "investigative consumer reporting agency. The October 5 letter "
        "stated that consumer reports from named agencies influenced the "
        "decision. It named Asurint, Tenstreet, DriverIQ, FMCSA-DOT, and "
        "Equifax Work Number and listed cities. It did not advise that an "
        "investigative consumer report had been obtained. Plaintiff does "
        "not contend that section 1786.40 required Swift to identify the "
        "decisive component, to explain the unfinished NSOPW search, or to "
        "attach a complete report. Those facts are alleged as "
        "circumstantial support for the registry-use inference and as "
        "context for the alternative CCRAA count, not as elements of "
        "section 1786.40(a). Cessation of hiring after those reports is "
        "the adverse action. The ICRAA and CCRAA counts can reach "
        "discovery even if the preliminary-registry-use inference later "
        "fails.",
    ),
    (
        "PARA",
        "46. Alternative explanations — a failed Clearinghouse or drug-and-"
        "alcohol result, a driving-record or crash disqualification, a "
        "lawful criminal-history adjudication under a statute that actually "
        "authorizes the use, a CDL defect, or a withdrawal of the application "
        "— can be tested against a discrete set of records. Plaintiff will "
        "seek the application file, the Asurint, Tenstreet, and DriverIQ "
        "reports, the Clearinghouse and PSP results, adjudication notes, and "
        "communications of the decision-maker.",
    ),
    (
        "PARA",
        "47. Lerma v. Amazon.com Services, LLC, C.D. Cal. No. 8:22-cv-01727, "
        "Dkt. 36, dismissed a Megan's Law count after the employer's report "
        "was in the record and showed ordinary court records and a completed "
        "national sex-offender search returning no record. This packet is "
        "not that report. The NSOPW component never completed. A demurrer "
        "may take the printed snapshots as what Plaintiff has pleaded them "
        "to be. It cannot convert an incomplete NSOPW into Lerma's completed "
        "no-record search, and it cannot decide — without the adjudication "
        "log — whether Swift used preliminary registry information from that "
        "in-process component. Defendants may not obtain a pleading-stage "
        "dismissal by withholding the interim NSOPW return and the "
        "decision-maker file. If production shows a completed NSOPW "
        "returning no record and no preliminary registry use, the Penal "
        "Code count will stand or fall on that file — after production, "
        "not by assuming it now.",
    ),
    (
        "PARA",
        "48. The use was not to protect a person at risk within the meaning of "
        "section 290.46(j)(1). A general commercial-driver assignment is not, "
        "without more, the narrow authorization that subdivision (j)(1) "
        "describes. FMCSA authorization to query the Clearinghouse or PSP is "
        "not authorization to use Megan's Law website information. Swift has "
        "the burden of proving any other statutory authorization as a defense.",
    ),
    ("SUBHEAD", "E. Knowledge, Concealment, and Harm"),
    (
        "PARA",
        "49. Swift knew or should have known that employment use of Megan's "
        "Law information is prohibited. The registry website displays that "
        "warning. Swift is a sophisticated interstate carrier with dedicated "
        "compliance and screening functions. On information and belief, its "
        "vendor contracts and adjudication guides address or should address "
        "California registry restrictions.",
    ),
    (
        "PARA",
        "50. On information and belief, Swift did not identify the registry, "
        "or any other specific ground, as the basis for the decision. The "
        "October 5 letter names agencies, not hits. That omission deprived "
        "Plaintiff of a meaningful opportunity to inspect the source, dispute "
        "a mismatch, and invoke the statutory remedies before the decision "
        "became final.",
    ),
    (
        "PARA",
        "51. As a result of the decision, Plaintiff lost the Class A Driver "
        "opportunity, including the wages and benefits of that position, "
        "according to proof and subject to mitigation. He also suffered "
        "emotional distress, humiliation, and anxiety from an unexplained "
        "denial he is informed and believes rested on a status the Legislature "
        "has forbidden employers to use. Wages earned, if any, will be proven.",
    ),
    (
        "PARA",
        "52. Plaintiff has sought and continues to seek replacement employment "
        "and does not claim a guaranteed lifetime expectancy from an unaccepted "
        "driver application. Economic damages will be limited to losses proven "
        "with reasonable certainty and without double recovery against other "
        "dockets that arise from different employers and different decisions.",
    ),
    ("HEADER", "VI.\nFIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Civil Code sections 1786.40 and 1786.50 — Against Swift and User DOES\n"
        "(Pleaded in the Alternative to CCRAA)",
    ),
    (
        "PARA",
        "59. Plaintiff realleges paragraphs 1 through 52 and 56 through 57 to "
        "the extent consistent with this cause.",
    ),
    (
        "PARA",
        "60. On information and belief, one or more of the agencies Swift "
        "named assembled or evaluated information concerning Plaintiff's "
        "character, general reputation, personal characteristics, or mode of "
        "living for employment purposes at Swift's request, and Swift was the "
        "user of that information before the October 5, 2023 decision. Civil "
        "Code section 1786.2 defines an investigative consumer report as one "
        "in which information on those subjects is obtained. Plaintiff "
        "alleges the products concerned those subjects. He does not invent "
        "personal interviews. If this Court concludes that interviews are "
        "required and none occurred, this ICRAA count does not apply and "
        "the CCRAA count does.",
    ),
    (
        "PARA",
        "61. Civil Code section 1786.40(a) required Swift, under circumstances "
        "in which employment was denied and an investigative consumer report "
        "had been obtained, to advise Plaintiff of that fact and supply the "
        "agency's name and address. Swift's October 5 letter names agencies "
        "and cities and states that consumer reports influenced the decision. "
        "It does not advise that an investigative consumer report had been "
        "obtained. That is the notice failure alleged. Plaintiff does not "
        "allege that section 1786.40 independently required Swift to identify "
        "the decisive component, to complete the NSOPW search, or to attach "
        "every unfinished printout.",
    ),
    (
        "PARA",
        "62. The omission caused incremental harm distinct from the denial "
        "itself. Plaintiff could not timely inspect the investigative file, "
        "learn whether an investigative report rather than an ordinary "
        "consumer report had been obtained, or invoke Civil Code sections "
        "1786.10 and 1786.22 before the decision became final. He has not "
        "yet served those inspection requests. He will. Those records, "
        "together with the adjudication log, will confirm whether an "
        "investigative report was obtained.",
    ),
    (
        "PARA",
        "63. This ICRAA count does not depend on proving Penal Code section "
        "290.46(j). A notice failure under Civil Code section 1786.40 is "
        "independently actionable if an investigative consumer report was "
        "obtained and employment was denied without the required advice. "
        "If Defendants establish that the reports were ordinary consumer "
        "reports and not investigative, this count does not apply and the "
        "CCRAA count does.",
    ),
    (
        "PARA",
        "64. Under Civil Code section 1786.50, Plaintiff seeks actual damages "
        "or $10,000, whichever is greater, costs, attorney's fees if later "
        "represented, and punitive damages upon proof of gross negligence or "
        "willfulness.",
    ),
    (
        "PARA",
        "65. This ICRAA count is not a Fair Credit Reporting Act count. "
        "Plaintiff has not pleaded 15 U.S.C. section 1681b(b)(3). He reserves "
        "amendment if production shows a timely FCRA claim and a notice or "
        "copy defect that the 2023 letters did not cure. He also reserves "
        "amendment under Civil Code section 1786.16 if production shows Swift "
        "procured an investigative report before the required standalone "
        "disclosure and written authorization. The California disclosure in "
        "the packet recites that Swift may order a consumer report or "
        "investigative consumer report. Plaintiff does not presently allege "
        "nonauthorization as an established fact.",
    ),
    ("HEADER", "VII.\nSECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Consumer Credit Reporting Agencies Act\n"
        "Civil Code sections 1785.20.5 and 1785.31 — Against Swift and User DOES\n"
        "(Pleaded in the Alternative to ICRAA)",
    ),
    (
        "PARA",
        "65A. Plaintiff realleges paragraphs 1 through 52 and 59 through 65 "
        "to the extent consistent with this cause.",
    ),
    (
        "PARA",
        "65B. In the alternative, if the reports Swift obtained were ordinary "
        "consumer credit reports rather than investigative consumer reports, "
        "the California Consumer Credit Reporting Agencies Act applies. "
        "Civil Code section 1785.20.5 required Swift, before procuring a "
        "consumer credit report for employment purposes, to provide written "
        "notice that a report would be used, and, before taking adverse "
        "action based in whole or in part on the report, to provide a copy "
        "of the report and a notice of rights.",
    ),
    (
        "PARA",
        "65C. Swift's October 5 letter stated that a copy of the consumer "
        "report and a Summary of Rights were attached. The decrypted "
        "September 26 packet is the report-side paper in Plaintiff's files. "
        "On information and belief, any later-completed component used in "
        "the October 5 decision — including any completed NSOPW or other "
        "agency report that was not in that packet — was not provided to "
        "Plaintiff before the adverse action. Plaintiff does not invent "
        "the contents of any unproduced later report.",
    ),
    (
        "PARA",
        "65D. The October 5 denial was based in whole or in part on consumer "
        "reports, as Swift admitted. If those reports were consumer credit "
        "reports, the failure to furnish a complete copy of every report "
        "actually used, before the decision, violated section 1785.20.5. "
        "If they were investigative, this count does not apply and the "
        "ICRAA count does.",
    ),
    (
        "PARA",
        "65E. Under Civil Code section 1785.31, Plaintiff seeks actual "
        "damages, costs, attorney's fees if later represented, and punitive "
        "damages upon proof of willfulness, according to proof.",
    ),
    ("HEADER", "VIII.\nTHIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unlawful and Unfair Business Practices\n"
        "Business and Professions Code section 17200 — Against All Defendants",
    ),
    (
        "PARA",
        "66. Plaintiff realleges paragraphs 1 through 65E to the extent "
        "consistent with this equitable cause.",
    ),
    (
        "PARA",
        "67. Defendants engaged in unlawful practices by violating, to the "
        "extent proven, Civil Code section 1786.40, Civil Code section "
        "1785.20.5, and Penal Code section 290.46(j)(2)(E). They engaged in "
        "unfair practices because the gravity of the harm — denial of "
        "employment on a criterion the Legislature has forbidden, or on "
        "consumer reports without the advice the statute required — outweighs "
        "any utility of taking adverse action while a sex-offender-website "
        "component remained Processing and while a complete copy of every "
        "report actually used was withheld.",
    ),
    (
        "PARA",
        "68. Plaintiff suffered injury in fact and lost money or property "
        "through the lost Swift employment opportunity, the compelled "
        "disclosure of personal identifying information for screening, and "
        "other economic losses to be proven. Injury in fact sufficient for "
        "UCL standing is not the same as recoverable restitution. He does "
        "not seek future unearned wages as UCL restitution. He seeks "
        "restitution only of money or property in which he had a vested "
        "interest and that Defendants acquired through the challenged "
        "practices — including, according to proof, the value of personal "
        "information he was compelled to disclose. He does not allege that "
        "Swift holds a fund of unearned future wages.",
    ),
    (
        "PARA",
        "69. Legal damages are not an adequate remedy for Defendants' "
        "retention, use, and dissemination of registry-derived screening data. "
        "On information and belief, Swift continues to use the same or "
        "similar standardized screening procedures for California driver "
        "applicants. That continuing practice, not a single past denial, is "
        "the basis for UCL injunctive relief and for declaratory relief under "
        "Code of Civil Procedure section 1060. Plaintiff seeks an injunction "
        "requiring Defendants to cease prohibited employment use of California "
        "registry information in California recruiting; preserve and disclose "
        "the source and audit trail of Plaintiff's screening; and correct or "
        "segregate unlawfully used data, together with restitution of vested "
        "money or property actually acquired, under Business and Professions "
        "Code section 17203.",
    ),
    ("HEADER", "IX.\nFOURTH CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Penal Code section 290.46(j) — Against All Defendants\n"
        "(Pleaded on Information and Belief — Preliminary NSOPW / Registry Use)",
    ),
    (
        "PARA",
        "53. Plaintiff realleges paragraphs 1 through 52, except allegations "
        "expressly pleaded in the alternative are incorporated only to the "
        "extent consistent with this cause.",
    ),
    (
        "PARA",
        "54. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk, except "
        "as otherwise authorized by law. Section 290.46(j)(2)(E) prohibits use "
        "of that information for purposes relating to employment unless another "
        "law authorizes the use.",
    ),
    (
        "PARA",
        "55. Section 290.46(j)(4)(A) makes the user liable for the actual "
        "damages, and any amount that may be determined by a jury or a court "
        "sitting without a jury, not exceeding three times the amount of actual "
        "damage, and not less than two hundred fifty dollars ($250), and "
        "attorney's fees, exemplary damages, or a civil penalty not exceeding "
        "twenty-five thousand dollars ($25,000). The $25,000 figure is a cap "
        "on the civil penalty, not a substitute floor that displaces actual "
        "damages. Plaintiff seeks the civil remedies the statute authorizes "
        "for unauthorized employment use of information disclosed pursuant to "
        "section 290.46, whether this Court locates those remedies in "
        "subdivision (j)(4)(A) or in another subdivision of section 290.46. "
        "He does not rest this cause on a criminal-enhancement theory.",
    ),
    (
        "PARA",
        "56. On information and belief, Swift used preliminary information "
        "from the still-Processing NSOPW component citing a sex-offender "
        "registry — including information disclosed pursuant to section "
        "290.46 concerning Plaintiff — in whole or in part in the employment "
        "decision. The user is the employer that takes the information into "
        "account in making the employment decision, not a consumer reporting "
        "agency that merely retrieves, scores, or republishes it. Plaintiff "
        "does not sue Asurint, Tenstreet, DriverIQ, or Equifax for mere "
        "furnishing. This count is directed at Swift's use. Plaintiff does "
        "not allege that the printed snapshots contain a completed NSOPW hit "
        "or the words 'SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY.' "
        "The use alleged is the use of preliminary registry information from "
        "that in-process component.",
    ),
    (
        "PARA",
        "57. The use related directly to employment: it concerned the Swift "
        "Class A Driver application and the October 5, 2023 decision not to employ "
        "Plaintiff. The use was not authorized by section 290.46(j)(1) or by "
        "any other provision of law applicable to that application. "
        "Defendants knew or should have known that employment use was "
        "prohibited. The use was a substantial factor in the decision and "
        "caused the loss and injury alleged.",
    ),
    (
        "PARA",
        "58. Plaintiff seeks the remedies authorized by section 290.46(j)(4)(A), "
        "or by whichever subdivision this Court holds supplies the civil "
        "remedy for unauthorized employment use. He does not presently allege "
        "a multi-incident pattern or practice at Swift sufficient for "
        "subdivision (j)(4)(B) preventive relief. He seeks that remedy only "
        "if discovery shows reasonable cause to believe such a pattern or "
        "practice. The damages claim under subdivision (j)(4)(A) does not "
        "depend on pattern or practice. Civil Code section 3294 punitive "
        "damages, if any, are pleaded in the alternative to the statute's "
        "exemplary damages or civil penalty for the same conduct. Plaintiff "
        "will elect. He does not seek double punitive recovery.",
    ),
    (
        "PARA",
        "58A. On information and belief, Swift's human-resources and "
        "centralized driver-adjudication personnel are managing agents "
        "within the meaning of Civil Code section 3294(b): they exercise "
        "substantial discretionary authority over hiring and screening "
        "policy, not merely the power to accept or reject a single applicant. "
        "Those managing agents established, implemented, and ratified the "
        "standardized screening practices alleged. Plaintiff seeks section "
        "3294 punitive damages only upon proof of oppression, fraud, or "
        "malice and of managing-agent authorization, ratification, or "
        "personal participation. ICRAA punitive damages, if any, rest on "
        "Civil Code section 1786.50 and do not depend on section 3294.",
    ),
    ("HEADER", "X.\nPRESERVATION OF EVIDENCE"),
    (
        "PARA",
        "70. Defendants are on notice to preserve Plaintiff's complete Swift "
        "and Tenstreet application file; recruiter communications of Kaufman "
        "and Hutto; the Asurint, Tenstreet, DriverIQ, Clearinghouse, PSP, and "
        "Equifax / Work Number orders, reports, component searches, "
        "adjudication, access, and cancellation logs; the decrypted September "
        "26, 2023 pre-adverse packet; and policies governing Megan's Law, "
        "FCRA, ICRAA, and driver adjudication in 2023.",
    ),
    (
        "PARA",
        "71. Relevant electronically stored information includes applicant-"
        "tracking and Driver Pulse audit fields, event timestamps, reason "
        "codes, report-view logs, emails, chats, SMS, and data-retention "
        "records from September 1, 2023 through December 31, 2023, and any "
        "later date on which the employment decision was recorded or revisited.",
    ),
    (
        "PARA",
        "72. Swift's own application file, vendor reports, and NSOPW "
        "adjudication log are the documents that will confirm or refute "
        "registry use.",
    ),
    ("HEADER", "XI.\nPRAYER FOR RELIEF"),
    ("PARA", "WHEREFORE, Plaintiff prays for judgment against Defendants as follows:"),
    (
        "LIST_ITEM",
        "1. For actual, consequential, and economic damages according to proof, "
        "without double recovery;",
    ),
    (
        "LIST_ITEM",
        "2. For the remedies authorized by Penal Code section 290.46(j)(4)(A), "
        "including statutory, treble, exemplary, or civil-penalty relief as "
        "the trier of fact and law permit;",
    ),
    (
        "LIST_ITEM",
        "3. For ICRAA actual damages or $10,000, whichever is greater, and "
        "punitive damages upon the showing required by Civil Code section "
        "1786.50, if that count is proven;",
    ),
    (
        "LIST_ITEM",
        "4. For CCRAA actual damages and punitive damages upon the showing "
        "required by Civil Code section 1785.31, if that alternative count "
        "is proven;",
    ),
    (
        "LIST_ITEM",
        "5. For punitive damages under Civil Code section 3294 against only "
        "those Defendants for whom the statutory prerequisites are proven, "
        "pleaded in the alternative to any exemplary damages or civil penalty "
        "awarded under Penal Code section 290.46 for the same conduct, with "
        "no double recovery and no amount pleaded;",
    ),
    (
        "LIST_ITEM",
        "6. For restitution under Business and Professions Code section 17203 "
        "of vested money or property Defendants acquired, not unearned future "
        "wages;",
    ),
    (
        "LIST_ITEM",
        "7. For injunctive relief under Business and Professions Code section "
        "17203, and for Penal Code section 290.46(j)(4)(B) preventive relief "
        "only if discovery shows reasonable cause to believe a pattern or "
        "practice;",
    ),
    (
        "LIST_ITEM",
        "8. For declaratory relief under Code of Civil Procedure section 1060 "
        "concerning whether Defendants' standardized California screening "
        "practices may use information disclosed pursuant to Penal Code "
        "section 290.46 for employment;",
    ),
    (
        "LIST_ITEM",
        "9. For costs of suit and attorney's fees where authorized if Plaintiff "
        "obtains counsel;",
    ),
    (
        "LIST_ITEM",
        "10. For prejudgment and post-judgment interest as allowed by law; and",
    ),
    (
        "LIST_ITEM",
        "11. For such other relief as the Court deems just and proper.",
    ),
    ("HEADER", "XII.\nDEMAND FOR JURY TRIAL"),
    (
        "PARA",
        "73. Plaintiff demands trial by jury on all causes of action and issues "
        "so triable.",
    ),
]


def _signature_block(d: PleadingPaper, exec_date: str, execute: bool) -> None:
    d.ensure_space(12)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(
            SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
        )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _verification(d: PleadingPaper, exec_date: str, execute: bool) -> None:
    d.start_new_page()
    d.write_line("VERIFICATION", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, BRENDAN NGWA NFORBI, declare:", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in this action. I have read the foregoing VERIFIED "
        "COMPLAINT and know its contents. The matters stated are true of my own "
        "knowledge, except those stated on information and belief, and as to those "
        "matters I believe them to be true.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the State of "
        "California that the foregoing is true and correct.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        f"Signed on {exec_date}, at Milpitas, California.", first_indent=36
    )
    d.ensure_space(10)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(
            SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
        )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)


def build(out: Path, exec_date: str, execute: bool) -> Path:
    if execute and not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    c = d.c

    atty_y = d._line_y(0)
    for i, (txt, font_name, size) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(font_name, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(
        CAPTION_LEFT, CAPTION_RIGHT, caption_size=8.2, tight_lh=10.5, boxed=True
    )
    d.blank_line()

    for kind, text in CONTENT:
        if kind == "NOTICE":
            if execute:
                continue
            d.ensure_space(7)
            d.write_wrapped(text, bold=True)
            d.blank_line()
        elif kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(_filing_text(text, execute), first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(_filing_text(text, execute), indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"Unknown content kind: {kind}")

    _signature_block(d, exec_date, execute)
    _verification(d, exec_date, execute)
    d.save()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    parser.add_argument("--date", default=DEFAULT_EXEC_DATE)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Affix Plaintiff's signature and drop review-draft notices",
    )
    args = parser.parse_args()
    path = build(Path(args.out).resolve(), args.date, args.execute)
    print(f"Generated: {path}")


if __name__ == "__main__":
    main()
