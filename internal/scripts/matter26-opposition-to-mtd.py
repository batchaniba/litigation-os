#!/usr/bin/env python3
"""Matter 26 -- Plaintiff's Opposition to UPS's Rule 12(b)(6) Motion to Dismiss.

Newanforbi v. United Parcel Service, Inc., USDC E.D. Cal. No. 2:26-cv-02847-DAD-CKD.
Hearing: October 5, 2026, 1:30 p.m., Courtroom 4 (Hon. Dale A. Drozd).

Built off ECF No. 7 / 7-1 / 7-2 / 7-3 (filed Aug. 26, 2026), the verified
Complaint (ECF No. 1, Ex. 1), and the First Advantage report UPS lodged as
Exhibit A. Architecture:

  1. UPS conceded it used the background check to deny hire; Exhibit A shows
     the only Decisional / INELIGIBLE component is the registry hit.
  2. Answer the (j)(3) -> Labor Code 432.7 path UPS actually argued, including
     the words UPS dropped from 432.7(n).
  3. Quote Exhibit A's two-field layout (Record Source vs Sentence) so the
     California-source line cannot be impeached as cherry-picking.

Rendered on the shared pleading-paper engine and signed with the portfolio
universal signature (bnn.cdl@gmail.com -- not the UPS COS misspelling).

Date the signature and Proof of Service with --date on the day of actual
service. Do not pre-date a September 9 certificate. L.R. 230(c) due date is
September 9, 2026; that is not the certificate date. Judge Drozd Standing
Order I.E does not require a proposed order with this civil motion; generate
one only as a portfolio draft and do not file it unless the Court asks.

Service is first-class mail (Fed. R. Civ. P. 5(b)(2)(C); E.D. Cal. L.R. 135).
The Proof of Service is the portfolio four-sided-border form
(``lib/proof_of_service.py``), not a pleading-paper certificate. Do not serve
or file the proposed order.

    python3 internal/scripts/matter26-opposition-to-mtd.py \\
        [--date "August 28, 2026"] [--mailed-from "San Jose, California"] [OUT_PDF]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_EDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-26"
    / "Opposition to UPS Rule 12(b)(6) Motion to Dismiss (E.D. Cal. 2-26-cv-02847) (Sep 9 2026).pdf"
)
DEFAULT_ORDER_OUT = (
    ROOT
    / "internal/public/documents/matter-26"
    / "Proposed Order Denying UPS Rule 12(b)(6) Motion to Dismiss (E.D. Cal. 2-26-cv-02847) (Sep 9 2026).pdf"
)

DEFAULT_EXEC_DATE = "August 28, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
DEFAULT_POS_OUT = (
    ROOT
    / "internal/public/documents/matter-26"
    / "Proof of Service - Opposition to UPS Rule 12(b)(6) (E.D. Cal. 2-26-cv-02847) (Aug 28 2026).pdf"
)
FOOTER = (
    "PLAINTIFF'S OPPOSITION TO RULE 12(b)(6) MOTION -- "
    "NEWANFORBI v. UNITED PARCEL SERVICE, INC."
)
ORDER_FOOTER = (
    "[PROPOSED] ORDER DENYING MOTION TO DISMISS -- "
    "NEWANFORBI v. UNITED PARCEL SERVICE, INC."
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
COURT_LINE2 = "EASTERN DISTRICT OF CALIFORNIA -- SACRAMENTO DIVISION"

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("UNITED PARCEL SERVICE, INC.; and", True, False),
    ("DOES 1 through 10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 2:26-cv-02847-DAD-CKD", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANT UNITED PARCEL", True, False),
    ("SERVICE, INC.'S RULE 12(b)(6)", True, False),
    ("MOTION TO DISMISS", True, False),
    ("", False, False),
    ("Hearing: October 5, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: 4 (civil L&M by Zoom)", False, False),
    ("Judge: Hon. Dale A. Drozd", False, False),
    ("", False, False),
    ("Action filed: July 15, 2026", False, False),
    ("Removed: August 20, 2026", False, False),
]

ORDER_CAPTION_RIGHT = [
    ("Case No. 2:26-cv-02847-DAD-CKD", False, False),
    ("", False, False),
    ("[PROPOSED] ORDER DENYING", True, False),
    ("DEFENDANT UNITED PARCEL", True, False),
    ("SERVICE, INC.'S RULE 12(b)(6)", True, False),
    ("MOTION TO DISMISS", True, False),
    ("", False, False),
    ("Hearing: October 5, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: 4 (civil L&M by Zoom)", False, False),
    ("Judge: Hon. Dale A. Drozd", False, False),
]

SIGNOFF_NAME = "BRENDAN NGEHSI NEWANFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

SERVICE_ADDRESSEES = [
    "Vanessa W. Mott, Esq. (SBN 184606)",
    "Alyssa R. Daskas, Esq. (SBN 359379)",
    "MARTENSON, HASBROUCK & SIMON LLP",
    "600 Anton Boulevard, Suite 1250",
    "Costa Mesa, CA 92626",
    "",
    "AND TO (address of record on the docket):",
    "Vanessa W. Mott, Esq.",
    "MARTENSON, HASBROUCK & SIMON LLP",
    "5800 Armada Drive, Suite 101",
    "Carlsbad, CA 92008",
    "Attorneys for Defendant United Parcel Service, Inc.",
]


CONTENT = [
    ("PARA",
     "TO THE HONORABLE COURT, AND TO DEFENDANT UNITED PARCEL SERVICE, INC. AND ITS "
     "ATTORNEYS OF RECORD:"),

    ("PARA",
     "Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, respectfully "
     "submits this Opposition to Defendant United Parcel Service, Inc.'s (\"UPS\") Motion "
     "to Dismiss under Federal Rule of Civil Procedure 12(b)(6) (ECF No. 7)."),

    ("HEADER", "I.\nINTRODUCTION"),

    ("PARA",
     "UPS cannot obtain Rule 12(b)(6) dismissal -- much less dismissal with prejudice -- "
     "on a factual premise its own filing destroys. UPS \"does not dispute the fact that "
     "it used information derived from Plaintiff's criminal background check when it made "
     "the decision to not hire him.\" (ECF No. 7 at 3.) The report UPS asks this Court to "
     "treat as part of the Complaint then shows what that information was. The First "
     "Advantage National Criminal File Plus search returned \"No Record Found\" and was "
     "scored \"Eligible.\" (ECF No. 7 at 18 (Ex. A at 5).) The only search scored "
     "\"Decisional,\" and the only search that produced the overall result \"INELIGIBLE,\" "
     "is the National Sex Offender Registry / Department of Justice website hit. (Id. at "
     "17, 19 (Ex. A at 4, 6).) UPS conceded use. Exhibit A identifies the only adverse "
     "component it could have used."),

    ("PARA",
     "UPS's motion nonetheless tells the Court: \"There is not a single reference to any "
     "California based sex offender registry included in the background check UPS "
     "obtained.\" (ECF No. 7 at 5.) Page 6 of 6 of that same report contains two fields, "
     "and both must be read together. The designated Record Source field states "
     "\"NATIONAL SEX OFFENDER REGISTRY.\" The Sentence field then states, verbatim: "
     "\"SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY\" and \"SENTENCE: REGISTERED "
     "SEX OFFENDER.\" (ECF No. 7 at 19 (Ex. A at 6).) That is not cherry-picking a stray line. "
     "It is the vendor's own two-field dump of a national search whose source of record "
     "is California's registry. The Complaint already alleges that the First Advantage "
     "report contained information derived from California's Megan's Law registry and "
     "that UPS used it to deny employment. (Compl. ¶¶ 2, 21, 23, 26, 34-36.) "
     "Exhibit A confirms those allegations. It does not refute them."),

    ("PARA",
     "UPS's remaining statutory argument fares no better. It does not defend a "
     "freestanding Labor Code section 432.7(n) safe harbor. It routes through Penal Code "
     "section 290.46(j)(3), which preserves uses of information \"pursuant to\" listed "
     "statutes, including Labor Code section 432.7, and then quotes section 432.7(n) "
     "with the words \"required by state, federal, or local law to\" omitted. (ECF No. 7 "
     "at 5, 11.) Those words are the limitation. UPS -- a private package company hiring "
     "a loader/unloader at the Lathrop hub -- has not identified any law that required "
     "it to run a sex-offender-registry screen for that job. Section 432.7(a) restricts "
     "the use of arrest records that did not result in conviction. It does not authorize "
     "Megan's Law employment screening. And Exhibit A's own criminal-file search found "
     "no record at all. UPS did not use a court conviction file. It used a registry "
     "alert scored INELIGIBLE by a \"Centralized Adjudication Team.\" (ECF No. 7 at 17 "
     "(Ex. A at 4).)"),

    ("PARA",
     "Because UPS's central premise collapses under its own record, the Complaint states "
     "plausible claims. Even if the Court finds any count deficient as labeled, dismissal "
     "with prejudice is improper on a pro se plaintiff's original complaint, and Rule "
     "15(a)(1)(B) still permits one amendment as of right."),

    ("HEADER", "II.\nSTATEMENT OF RELEVANT FACTS"),

    ("PARA",
     "1. In or around mid-2024, Plaintiff applied for a loader/unloader position at UPS's "
     "hub in Lathrop, San Joaquin County, California. (Compl. ¶ 16; ECF No. 7 at 14 (Ex. A at 1) "
     "[Position: \"Loader/Unloader - Hub / US - LATHROP HUB (CALAH)\"])."),

    ("PARA",
     "2. UPS initiated a pre-employment background screening through First Advantage. "
     "(Compl. ¶ 17.) The report was ordered July 17, 2024, and completed July 18, "
     "2024. (ECF No. 7 at 14 (Ex. A at 1).)"),

    ("PARA",
     "3. On July 19, 2024, the screening system recorded: \"BASED ON YOUR CRITERIA, THE "
     "OVERALL CASE SCORE IS INELIGIBLE,\" with the notation \"Adjudicated by the "
     "Centralized Adjudication Team.\" (ECF No. 7 at 17 (Ex. A at 4).)"),

    ("PARA",
     "4. The First Advantage National Criminal File Plus search for Stockton, San Joaquin "
     "County, returned \"No Record Found\" and was scored \"Eligible.\" (ECF No. 7 at 18 "
     "(Ex. A at 5).) Social Security verification passed. (Id. at 17-18.)"),

    ("PARA",
     "5. The only component scored \"Decisional\" is \"National Sex Offender Registry "
     "Search - Department Of Justice Web Site.\" On page 6 of 6, Record Source is "
     "\"NATIONAL SEX OFFENDER REGISTRY\"; Search Results are \"Record Found\"; Name on File "
     "is \"BRENDAN NGEHSI NGWANFORBI\"; and the Sentence field reads \"SOURCE OF RECORD: "
     "CALIFORNIA SEX OFFENDER REGISTRY\" / \"SENTENCE: REGISTERED SEX OFFENDER.\" (Id. at "
     "6.)"),

    ("PARA",
     "6. Between July 22 and July 27, 2024, First Advantage sent pre-adverse action "
     "notices. On July 31, 2024, UPS issued a final adverse action notice denying "
     "Plaintiff employment. (Compl. ¶¶ 18, 25.) UPS identified no other basis for "
     "the denial. (Compl. ¶ 27.)"),

    ("PARA",
     "7. UPS's own California disclosures, lodged as Exhibit B, told Plaintiff the "
     "consumer report would be used \"to evaluate whether you would present an "
     "unacceptable risk of theft or other dishonest behavior in the job for which you "
     "are being considered,\" including a Labor Code section 1024.5(a)(7) credit-purpose "
     "box keyed to access to confidential financial and business information. (ECF No. 7 "
     "at 27 (Ex. B).) A California sex-offender-registry listing is not a theft or "
     "dishonesty record, and it is not a court conviction file -- Exhibit A's criminal "
     "search found none."),

    ("HEADER", "III.\nSTANDARD OF REVIEW"),

    ("PARA",
     "On a Rule 12(b)(6) motion the Court must \"accept all factual allegations in the "
     "complaint as true and construe the pleadings in the light most favorable to the "
     "nonmoving party.\" <<i:Manzarek v. St. Paul Fire & Marine Ins. Co.>>, 519 F.3d 1025, "
     "1031 (9th Cir. 2008). A claim is plausible when \"the plaintiff pleads factual "
     "content that allows the court to draw the reasonable inference that the defendant "
     "is liable for the misconduct alleged.\" <<i:Ashcroft v. Iqbal>>, 556 U.S. 662, 678 "
     "(2009)."),

    ("PARA",
     "Pro se pleadings \"must be held to less stringent standards than formal pleadings "
     "drafted by lawyers,\" <<i:Erickson v. Pardus>>, 551 U.S. 89, 94 (2007), and must be "
     "construed liberally, <<i:Hebbe v. Pliler>>, 627 F.3d 338, 342 (9th Cir. 2010). "
     "\"Dismissal without leave to amend is improper unless it is clear . . . that the "
     "complaint could not be saved by any amendment.\" <<i:Lopez v. Smith>>, 203 F.3d 1122, "
     "1130 (9th Cir. 2000) (en banc); see also <<i:Noll v. Carlson>>, 809 F.2d 1446, 1448 "
     "(9th Cir. 1987)."),

    ("PARA",
     "On a 12(b)(6) motion the Court \"may generally consider only allegations contained "
     "in the pleadings, exhibits attached to the complaint, and matters properly subject "
     "to judicial notice.\" <<i:Swartz v. KPMG LLP>>, 476 F.3d 756, 763 (9th Cir. 2007). If "
     "matters outside the pleadings are considered, \"the motion must be treated as one "
     "for summary judgment under Rule 56\" and the parties must be given a reasonable "
     "opportunity to present material. Fed. R. Civ. P. 12(d)."),

    ("HEADER", "IV.\nARGUMENT"),

    ("SUBHEAD",
     "A.  If Exhibit A Is Considered, It Must Be Considered Whole -- and It\n"
     "Proves Plaintiff's Allegations"),

    ("PARA",
     "UPS asks the Court to incorporate Exhibit A and Exhibit B by reference because the "
     "Complaint refers to the background check and to ICRAA disclosures. (ECF No. 7 at "
     "3-4); see <<i:United States v. Ritchie>>, 342 F.3d 903, 908 (9th Cir. 2003). Plaintiff "
     "does not object to the Court reading Exhibit A. He objects to UPS using "
     "incorporation as a one-way valve."),

    ("PARA",
     "In <<i:Khoja v. Orexigen Therapeutics, Inc.>>, 899 F.3d 988, 998 (9th Cir. 2018), the "
     "Ninth Circuit warned against \"overuse\" of the doctrine and cautioned that a court "
     "should not \"assume the truth of an incorporated document if such assumptions only "
     "serve to dispute facts stated in a well-pleaded complaint.\" Id. at 1003. UPS "
     "offers Exhibit A to dispute the allegation that it used California Megan's Law "
     "information. The document, read as a whole, reinforces that allegation. Khoja does "
     "not permit UPS to credit the \"NATIONAL SEX OFFENDER REGISTRY\" Record Source label "
     "and disregard the Sentence field that identifies \"CALIFORNIA SEX OFFENDER "
     "REGISTRY\" as the source of record."),

    ("PARA",
     "UPS also filed the declaration of Ashley Felsing, an HRBP Director, as ECF No. 7-2, "
     "attaching the same report and the application disclosures as exhibits. Incorporation "
     "by reference reaches those documents because the Complaint already describes them. "
     "It does not reach extra-pleading testimony. If the Court is asked to credit anything "
     "in the Felsing declaration beyond authenticating Exhibits A and B, Rule 12(d) "
     "requires conversion. Plaintiff asks the Court to read the documents. He does not "
     "stipulate to UPS's characterization of what it \"accessed.\""),

    ("PARA",
     "Two consequences follow. First, if Exhibit A is out, the Complaint's allegations "
     "control: the report contained California registry information, and UPS used it to "
     "deny hire. (Compl. ¶¶ 21, 23, 26, 34-36.) Second, if Exhibit A is in, UPS's "
     "sentence that the report contains \"not a single reference to any California based "
     "sex offender registry\" (ECF No. 7 at 5) is simply false. Either path denies "
     "dismissal of Count I. What the Court may not do is take UPS's characterization of "
     "Exhibit A as true and the document's California-source field as false."),

    ("SUBHEAD",
     "B.  Count I States a Claim Under Penal Code Section 290.46(j)(2)(E)"),

    ("PARA",
     "Section 290.46(j)(1) authorizes use of \"information disclosed pursuant to this "
     "section\" only \"to protect a person at risk.\" Section 290.46(j)(2)(E) then "
     "prohibits, except as authorized under paragraph (1) or any other provision of law, "
     "use of that information for purposes relating to employment. Section 290.46(j)(4)(A) "
     "supplies the private right of action. The user is \"liable for the actual damages, "
     "and any amount that may be determined by a jury or a court sitting without a jury, "
     "not exceeding three times the amount of actual damage, and not less than two hundred "
     "fifty dollars ($250), and attorney's fees, exemplary damages, or a civil penalty not "
     "exceeding twenty-five thousand dollars ($25,000).\" The $25,000 figure is a cap on "
     "the civil penalty, not a floor alternative to actual damages."),

    ("PARA",
     "The Complaint alleges each element. Plaintiff is a registrant. (Compl. ¶ 34.) "
     "The First Advantage report disclosed that status from California's registry. "
     "(Compl. ¶¶ 2, 21, 34.) UPS used the information to deny employment on or "
     "about July 31, 2024. (Compl. ¶¶ 26, 35.) The loader/unloader position did "
     "not implicate protecting an identified person at risk. (Compl. ¶ 36.) Those "
     "allegations are accepted as true. UPS's motion does not say Plaintiff failed to "
     "allege use. It says the use was of a \"national\" registry rather than California's "
     "Megan's Law website. (ECF No. 7 at 5.) That is a construction argument, not a "
     "pleading failure."),

    ("PARA",
     "1.  The conceded use, and the only adverse component, is the registry hit."),

    ("PARA",
     "UPS \"does not dispute\" that it used information from the background check to not "
     "hire Plaintiff. (ECF No. 7 at 3.) Exhibit A then shows the criminal-records search "
     "was Eligible / No Record Found, and the registry search was the only Decisional "
     "component feeding an INELIGIBLE overall score. (ECF No. 7 at 17-19 (Ex. A at 4-6).) "
     "At minimum, a reasonable inference is that the information UPS used was the "
     "registry hit. That is the use section 290.46(j)(2)(E) forbids."),

    ("PARA",
     "UPS argues that by alleging a Megan's Law violation Plaintiff \"impliedly admits\" a "
     "sex-crime conviction, so UPS was entitled to use a conviction record. (ECF No. 7 "
     "at 5.) The argument is a bait-and-switch. Exhibit A's criminal-file search returned "
     "no record. Registry status on a Department of Justice website search is not a "
     "court conviction file. Plaintiff does not concede, and this motion does not "
     "establish, that UPS reviewed or relied on any judicial conviction record."),

    ("PARA",
     "2.  The two-field layout supports California as the source of record."),

    ("PARA",
     "UPS's theory is that it \"did not access California's Megan's Law website\" and "
     "therefore cannot have used \"information that is disclosed pursuant to this "
     "section.\" (ECF No. 7 at 5); Cal. Penal Code section 290.46(j)(2). The statute "
     "does not say \"information an employer personally downloaded from meganslaw.ca.gov.\" "
     "It says \"any information that is disclosed pursuant to this section.\" Section "
     "290.46 is the statute by which the California Department of Justice makes "
     "registrant information available to the public via an internet website. (Cal. "
     "Penal Code section 290.46(a)(1).) Exhibit A does not describe an independent "
     "federal conviction database. It describes a \"National Sex Offender Registry Search "
     "- Department Of Justice Web Site\" whose Sentence field identifies the source of "
     "record as the California Sex Offender Registry. (ECF No. 7 at 19 (Ex. A at 6).)"),

    ("PARA",
     "That two-field structure supports Plaintiff's pass-through theory, and it is in UPS's own exhibit. "
     "A construction that lets an employer evade section 290.46(j)(2)(E) by running the "
     "same California data through a national query portal would make the employment "
     "prohibition surplusage. \"[A] statute should not be given an interpretation that "
     "fails to accomplish its purpose.\" <<i:People v. Pieters>>, 52 Cal. 3d 894, 898-99 "
     "(1991). The phrase \"disclosed pursuant to this section\" refers to the information "
     "California discloses under section 290.46 -- not the brand name on the search "
     "window."),

    ("PARA",
     "In <<i:Mendoza v. ADP Screening & Selection Services, Inc.>>, 182 Cal. App. 4th 1644 "
     "(2010), the Court of Appeal addressed section 290.46's civil-liability framework "
     "in an anti-SLAPP posture. It distinguished the screening company that reports "
     "Megan's Law information from the employer that uses the information for an "
     "employment decision. Id. at 1658-59. UPS is the employer. It received "
     "California-sourced registry information and, by its own concession, used the "
     "background check to deny hire. That is the conduct the statute reaches."),

    ("PARA",
     "3.  Section 290.46(j)(3) and Labor Code section 432.7 do not save this hiring\n"
     "decision."),

    ("PARA",
     "UPS's actual statutory hook is not a freestanding 432.7(n) argument. It is that "
     "section 290.46(j)(3) \"specifically carves out authorized access of otherwise "
     "protected information under Cal. Labor Code. section 432.7,\" after which UPS "
     "quotes 432.7(n) as if it \"explicitly permits\" any employer to run criminal "
     "background checks and use the results. (ECF No. 7 at 5, 11.)"),

    ("PARA",
     "Subdivision (j)(3) states that section 290.46 \"shall not affect authorized access "
     "to, or use of, information pursuant to, among other provisions, Sections 11105 and "
     "11105.3 of this code, Section 8808 of the Family Code, Sections 777.5 and 14409.2 "
     "of the Financial Code, Sections 1522.01 and 1596.871 of the Health and Safety Code, "
     "and Section 432.7 of the Labor Code.\" Cal. Penal Code section 290.46(j)(3). That "
     "is a savings clause for uses those statutes independently authorize -- DOJ rap "
     "sheets, childcare licensing, and the like. It is not a license to use Megan's Law "
     "website information to reject a warehouse loader."),

    ("PARA",
     "Labor Code section 432.7(n), quoted in full, provides: \"This section does not "
     "prohibit an employer, whether a public agency or private individual or corporation, "
     "required by state, federal, or local law to conduct criminal background checks for "
     "employment purposes or to restrict employment based on criminal history from "
     "complying with those requirements, or to prohibit the employer from seeking or "
     "receiving an applicant's criminal history report that has been obtained pursuant to "
     "procedures otherwise provided for under federal, state, or local law.\" UPS's "
     "quotation drops \"required by state, federal, or local law to.\" (ECF No. 7 at 5.) "
     "Those words are the limitation. UPS has not identified any statute, regulation, or "
     "ordinance that required a sex-offender-registry check for a Lathrop "
     "loader/unloader. It screened Plaintiff as \"part of its standard pre-employment "
     "screening process.\" (Compl. ¶ 17; ECF No. 7 at 3.)"),

    ("PARA",
     "Section 432.7(a) is in any event a restriction on using arrest or detention records "
     "that did not result in conviction. It is not an affirmative grant of authority to "
     "use California's public sex-offender website for employment. And again, UPS's "
     "criminal-file search returned no record. (ECF No. 7 at 18 (Ex. A at 5).) There is no "
     "432.7 \"conviction history\" use on this exhibit. There is a registry alert."),

    ("PARA",
     "4.  The use was not \"to protect a person at risk,\" and it was not the theft\n"
     "purpose UPS disclosed."),

    ("PARA",
     "The only use section 290.46(j)(1) authorizes is \"to protect a person at risk.\" A "
     "warehouse loader/unloader job is not that use. (Compl. ¶ 36.) UPS's Exhibit B "
     "disclosures go further: they told Plaintiff the report would be used to assess "
     "\"risk of theft or other dishonest behavior,\" including under Labor Code section "
     "1024.5(a)(7). (ECF No. 7 at 27 (Ex. B).) Protecting packages from theft is not "
     "protecting \"a person at risk\" within the meaning of Megan's Law. A registry "
     "listing is not a theft record. UPS disclosed one purpose and, on this exhibit, "
     "adjudicated another."),

    ("PARA",
     "5.  At minimum, the statutory question is not a 12(b)(6) knockout."),

    ("PARA",
     "Whether California-sourced registry information retrieved through a \"National Sex "
     "Offender Registry / Department of Justice Web Site\" search is \"information "
     "disclosed pursuant to\" section 290.46 is, at worst, a plausible reading in "
     "Plaintiff's favor. Iqbal requires plausibility, not that Plaintiff win the "
     "statutory fight in the opposition. How First Advantage queried California's "
     "registry, what \"Department Of Justice Web Site\" means on this vendor form, and "
     "what UPS's adjudication criteria actually scored are fact questions. If the Court "
     "is inclined to resolve them on the exhibits, Rule 12(d) requires conversion and a "
     "reasonable opportunity to take discovery -- including from First Advantage -- not "
     "a with-prejudice dismissal on a cold record UPS assembled."),

    ("SUBHEAD",
     "C.  Count II: Williams Does Not Extinguish the Statutory Claim, and Any\n"
     "Tameny Labeling Defect Is Curable"),

    ("PARA",
     "UPS cites <<i:Williams v. Sacramento River Cats Baseball Club, LLC>>, 40 Cal. App. 5th "
     "280 (2019), for the proposition that the common-law Tameny tort does not extend to "
     "failure-to-hire. (ECF No. 7 at 6.) Williams holds that a Tameny duty of care "
     "requires a prior employment relationship, so a job applicant's public-policy "
     "remedy for a discriminatory refusal to hire is statutory, not common-law. Id. at "
     "286-90."),

    ("PARA",
     "Two points follow, and neither is dismissal of the case. First, Count I is not a "
     "Tameny claim. Section 290.46(j)(4)(A) is an express private right of action for "
     "use of registry information \"for purposes relating to . . . employment.\" It does "
     "not require a prior employment relationship. Applicants are the people the "
     "employment prohibition exists to protect. Williams does not touch Count I."),

    ("PARA",
     "Second, Count II as currently captioned invokes Tameny and City of Moorpark. "
     "(Compl. ¶ 39.) To the extent that caption is a common-law failure-to-hire "
     "theory Williams forecloses, the facts pleaded in Count II are the same facts as "
     "Count I. (Compl. ¶¶ 40-42.) The Court should either treat Count II as a "
     "restatement of the statutory right of action already pleaded, or grant leave to "
     "amend to caption it as such. A labeling defect on a pro se original complaint is "
     "not futility. Lopez, 203 F.3d at 1130. Plaintiff does not abandon the claim; he "
     "asks that it be read, or repled, as the statute that actually supplies the duty."),

    ("SUBHEAD",
     "D.  Count III States an ICRAA Claim on the Theories Actually Pled"),

    ("PARA",
     "UPS argues Plaintiff \"admits\" ICRAA compliance because Exhibit B contains a "
     "disclosure naming First Advantage and because Plaintiff received pre-adverse and "
     "final adverse notices. (ECF No. 7 at 6-7.) That is a summary-judgment argument "
     "dressed as a 12(b)(6). Khoja does not require the Court to treat UPS's "
     "characterization of Exhibit B as true over the Complaint's sworn allegations. 899 "
     "F.3d at 1003."),

    ("PARA",
     "Plaintiff does not rest Count III on a theory that Exhibit B failed to name First "
     "Advantage or to use the phrase \"investigative consumer report.\" He also does "
     "not rest Count III on a theory that a Penal Code section 290.46 violation is, "
     "without more, an ICRAA violation. Paragraph 46's \"spirit and purpose\" allegation "
     "is not the statutory hook."),

    ("PARA",
     "The Complaint's live ICRAA theory is Civil Code section 1786.16. Subdivision "
     "(a)(5) and (b)(1) require the procuring person to provide a means to request a "
     "copy of the report and, if requested, to send a copy within three business days of "
     "the date the report is provided to the recipient. Subdivision (b)(2) requires "
     "compliance with section 1786.40 if adverse action is a consideration -- advising "
     "the consumer of the action and supplying the name and address of the reporting "
     "agency. (Compl. ¶¶ 24, 47(b).) Paragraph 24 alleges the First Advantage portal "
     "link expired and Plaintiff no longer has access to the underlying report. Whether "
     "UPS actually sent a complete copy of Exhibit A within the time section 1786.16(b)(1) "
     "requires is a fact question. It is not resolved by UPS attaching an application "
     "packet. If the Court concludes paragraph 47(b) was pled closer to a copy-before-"
     "adverse-action formulation than to section 1786.16(b)(1)'s request-and-three-day "
     "rule, the defect is labeling, not futility: the same facts support leave to "
     "conform the citation. Lopez, 203 F.3d at 1130."),

    ("SUBHEAD", "E.  Count IV States a Constitutional Privacy Claim"),

    ("PARA",
     "A California constitutional privacy claim requires (1) a legally protected privacy "
     "interest, (2) a reasonable expectation of privacy under the circumstances, and (3) "
     "a serious invasion of that interest. <<i:Hill v. Nat'l Collegiate Athletic Ass'n>>, 7 "
     "Cal. 4th 1, 35-40 (1994). UPS recites that test and then answers a different "
     "question: whether court records are public. (ECF No. 7 at 7-8.)"),

    ("PARA",
     "The Legislature created a legally protected interest in how section 290.46 "
     "information may be used. Authorized use is limited to protecting a person at "
     "risk; employment use is prohibited. Cal. Penal Code section 290.46(j)(1)-(2). That "
     "is not a claim that judicial conviction records are secret. It is a claim that "
     "the State put a use-restriction on a specific public-website disclosure, and that "
     "UPS invaded that interest by using the information for the one purpose the "
     "statute names and forbids. (Compl. ¶¶ 50-52.) Estate of Hearst and Alfaro, "
     "which UPS cites for access to court files, do not repeal section 290.46(j)."),

    ("PARA",
     "On expectation and consent: UPS argues Plaintiff cannot have a reasonable "
     "expectation of privacy because he signed Exhibit B. (ECF No. 7 at 8.) Consent is "
     "measured by its scope. Exhibit B disclosed a theft-and-dishonesty purpose, "
     "including Labor Code section 1024.5(a)(7). Plaintiff did not consent to UPS using "
     "California registry information in a manner the Legislature has declared "
     "unlawful. Whether that scope question can be decided as a matter of law on these "
     "exhibits is, at minimum, mixed. Hill itself treats reasonable expectation and "
     "seriousness as mixed questions, adjudicable as law only when the facts are "
     "undisputed. 7 Cal. 4th at 40. They are not. The claim is properly pled. It is "
     "not the claim on which this opposition principally stands."),

    ("SUBHEAD",
     "F.  Count V: Negligence Per Se Is a Doctrine -- Leave to Amend Should Be\n"
     "Granted to Plead Ordinary Negligence"),

    ("PARA",
     "UPS is correct that, under California law, negligence per se is a doctrine, not an "
     "independent cause of action. <<i:Dent v. Nat'l Football League>>, 902 F.3d 1109, 1117 "
     "(9th Cir. 2018). Plaintiff does not dispute the label. The Complaint nonetheless "
     "pleads the substance: section 290.46(j)(2)(E) protects a defined class against a "
     "defined harm; Plaintiff is in that class; UPS violated the statute; the violation "
     "caused the harm. (Compl. ¶¶ 54-58); see Cal. Evid. Code section 669. A pro "
     "se complaint is construed by its substance, not its caption. Hebbe, 627 F.3d at "
     "342. Plaintiff requests leave to amend to plead ordinary negligence (duty, breach, "
     "causation, damages) with Evidence Code section 669 as the presumption, not the "
     "cause of action. That amendment is not futile. Lopez, 203 F.3d at 1130."),

    ("SUBHEAD", "G.  Count VI States a UCL Claim"),

    ("PARA",
     "The UCL borrows violations of other laws as independently actionable \"unlawful\" "
     "practices. <<i:Cel-Tech Commc'ns, Inc. v. Los Angeles Cellular Tel. Co.>>, 20 Cal. 4th "
     "163, 180 (1999). Count VI's unlawful prong is predicated on Count I. (Compl. ¶ "
     "61.) If Count I states a claim -- and it does -- the unlawful prong states a "
     "claim. UPS's chain of \"because we did not violate 290.46, the UCL dies\" is only "
     "as strong as its Megan's Law argument, which Exhibit A does not establish."),

    ("PARA",
     "The unfair prong is independently pled. (Compl. ¶ 62.) UPS disclosed that the "
     "report would be used to assess theft and dishonest behavior, then scored Plaintiff "
     "INELIGIBLE off a California registry alert that its own criminal search did not "
     "corroborate with any conviction record. That practice offends the policy section "
     "290.46(j) encodes. Plaintiff does not argue, and does not need to argue, that the "
     "conduct would be \"unfair\" even if the Legislature had authorized it. Cel-Tech's "
     "safe-harbor discussion applies when a statute affirmatively permits the conduct. "
     "20 Cal. 4th at 182-83. Section 290.46(j)(3) does not affirmatively permit this "
     "use; 432.7(n) does not apply to an employer not required by law to screen; and "
     "nothing in Exhibit A is a court-file conviction UPS was independently entitled to "
     "adjudicate."),

    ("HEADER", "V.\nLEAVE TO AMEND MUST BE GRANTED AS TO ANY COUNT FOUND DEFICIENT"),

    ("PARA",
     "This is Plaintiff's original complaint. It was verified and filed when the First "
     "Advantage report was not in Plaintiff's possession. (Compl. ¶ 24.) UPS then "
     "lodged that report as Exhibit A. Even if the Court finds Count II's Tameny caption, "
     "Count V's per se caption, or any ICRAA sub-theory deficient, \"[a] pro se litigant "
     "must be given leave to amend his or her complaint unless it is absolutely clear "
     "that the deficiencies of the complaint could not be cured by amendment.\" Noll, 809 "
     "F.2d at 1448."),

    ("PARA",
     "Rule 15(a)(1)(B) permits one amendment as of right within 21 days after service of "
     "a Rule 12(b) motion. UPS served the motion by mail on August 26, 2026. (ECF No. "
     "7-3.) Twenty-one days after that service is September 16, 2026. Because service "
     "was by mail, Rule 6(d) may add three days, through September 19, 2026. Plaintiff "
     "will confirm the operative date from the envelope if it differs. L.R. 230(c) is a "
     "different clock, runs from filing, and is not extended by Rule 6(d): this "
     "opposition remains due September 9, 2026. The Initial Scheduling Order advised of "
     "the Rule 15 window. (ECF No. 2.) Futility is not established. The facts that "
     "would be added are the facts UPS already put in the record: the two-field "
     "California source line, the Eligible criminal search, the INELIGIBLE centralized "
     "adjudication, and the theft-purpose disclosure. Dismissal with prejudice on this "
     "record would be an abuse of discretion."),

    ("HEADER", "VI.\nCONCLUSION"),

    ("PARA",
     "UPS conceded it used the background check to deny hire. Its own Exhibit A shows "
     "the only adverse component is a National Sex Offender Registry / Department of "
     "Justice website hit whose Sentence field identifies the California Sex Offender "
     "Registry as the source of record. That is a use of information disclosed pursuant "
     "to Penal Code section 290.46, for employment, of a person who is not a \"person at "
     "risk\" under subdivision (j)(1). Section 290.46(j)(3) and Labor Code section 432.7 "
     "do not authorize it."),

    ("PARA",
     "Plaintiff respectfully requests that the Court deny the Motion to Dismiss in its "
     "entirety. In the alternative, Plaintiff requests that the Court deny the motion as "
     "to Counts I, III, IV, and VI; dismiss Counts II and V with leave to amend; and in "
     "all events deny dismissal with prejudice."),
]


ORDER_CONTENT = [
    ("PARA",
     "Defendant United Parcel Service, Inc.'s Motion to Dismiss pursuant to Federal Rule "
     "of Civil Procedure 12(b)(6) (ECF No. 7) came on for hearing on October 5, 2026. "
     "Plaintiff BRENDAN NGEHSI NEWANFORBI appeared in propria persona. Defendant appeared "
     "through counsel. The Court, having considered the papers and arguments, and good "
     "cause appearing, ORDERS as follows:"),

    ("LIST_ITEM",
     "1.  The motion is DENIED as to the First Cause of Action (Cal. Penal Code "
     "section 290.46(j)(2)(E))."),

    ("LIST_ITEM",
     "2.  The motion is DENIED as to the Third, Fourth, and Sixth Causes of Action."),

    ("LIST_ITEM",
     "3.  The Second Cause of Action (failure to hire in violation of public policy) is "
     "DISMISSED WITH LEAVE TO AMEND."),

    ("LIST_ITEM",
     "4.  The Fifth Cause of Action (negligence per se) is DISMISSED WITH LEAVE TO "
     "AMEND."),

    ("LIST_ITEM",
     "5.  Plaintiff shall file any amended complaint within twenty-one (21) days of this "
     "Order. Defendant shall file a responsive pleading within the time provided by the "
     "Federal Rules of Civil Procedure."),

    ("PARA", "IT IS SO ORDERED."),
]


def opposition_pos_fields(exec_date: str, mailed_from: str) -> ProofOfServiceFields:
    """Fill the portfolio four-sided-border Proof of Service (not pleading paper)."""
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "UNITED PARCEL SERVICE, INC.; and",
            "DOES 1 through 10, inclusive",
        ],
        defendant_role="Defendants",
        case_number="2:26-cv-02847-DAD-CKD",
        district_line=DISTRICT_EDCAL,
        title="PROOF OF SERVICE",
        service_date=exec_date,
        document_title="Plaintiff's Opposition to UPS's Rule 12(b)(6) Motion to Dismiss",
        mailing_location=mailed_from,
        recipients=list(SERVICE_ADDRESSEES),
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=True,
    )


def build_opposition_proof_of_service(
    out: Path, exec_date: str, mailed_from: str
) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    return build_proof_of_service(out, opposition_pos_fields(exec_date, mailed_from))


def _signature(d: PleadingPaper, exec_date: str) -> None:
    d.ensure_space(9)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _certificate_of_service(d: PleadingPaper, exec_date: str, mailed_from: str,
                            document_title: str) -> None:
    d.start_new_page()
    d.write_line("CERTIFICATE OF SERVICE", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in this action and am over the age of eighteen years. My "
        "email address is bnn.cdl@gmail.com. On "
        f"{exec_date}, I served the foregoing {document_title} pursuant to Federal Rule "
        "of Civil Procedure 5(b)(2)(C) and E.D. Cal. Local Rule 135 by placing a true "
        "and correct copy in a sealed envelope, with first-class postage fully prepaid, "
        "and depositing it with the United States Postal Service at "
        f"{mailed_from}, addressed as follows:",
        first_indent=36,
    )
    d.blank_line()
    for line in SERVICE_ADDRESSEES:
        d.write_line(line, indent=54)
    d.blank_line()
    d.write_wrapped(
        "I also transmitted a courtesy copy of the same document by electronic mail to "
        "vmott@martensonlaw.com and adaskas@martensonlaw.com. Counsel has not consented "
        "in writing to electronic service under Rule 5(b)(2)(E). The courtesy email is "
        "not the method of service.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the United States of America "
        f"that the foregoing is true and correct. Executed on {exec_date}, at "
        f"{mailed_from}.",
        first_indent=36,
    )
    d.ensure_space(6)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=False)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")


def _header_block(d: PleadingPaper, right_caption: list) -> None:
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
    d.draw_caption_block(CAPTION_LEFT, right_caption, caption_size=10,
                         tight_lh=13, boxed=True)
    d.blank_line()


def build_opposition(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    _header_block(d, CAPTION_RIGHT)
    _render_body(d, CONTENT)
    _signature(d, exec_date)
    _certificate_of_service(
        d, exec_date, mailed_from,
        "PLAINTIFF'S OPPOSITION TO DEFENDANT UNITED PARCEL SERVICE, INC.'S "
        "RULE 12(b)(6) MOTION TO DISMISS",
    )
    d.save()
    return out


def build_proposed_order(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=ORDER_FOOTER)
    _header_block(d, ORDER_CAPTION_RIGHT)
    _render_body(d, ORDER_CONTENT)
    d.ensure_space(8)
    d.blank_line()
    d.write_line("Dated: _______________, 2026")
    d.blank_line()
    d.blank_line()
    d.write_line("___________________________________________")
    d.write_line("HON. DALE A. DROZD")
    d.write_line("United States District Judge")
    d.blank_line()
    d.write_line("Presented by:", italic=True)
    _signature(d, exec_date)
    # Drozd Standing Order I.E: do not file a proposed order with this motion
    # unless the Court requests one. No certificate of service: this draft is
    # not for lodging with the opposition.
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--order-out", default=str(DEFAULT_ORDER_OUT))
    ap.add_argument("--date", default=DEFAULT_EXEC_DATE,
                    help="Date of actual service, printed on the signature and "
                         "Proof of Service. Do not pass the L.R. 230(c) due date unless "
                         "that is the day the papers are actually served.")
    ap.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM,
                    help="City and state where the service copy is deposited with the "
                         "USPS and where the Proof of Service is executed")
    ap.add_argument("--pos-out", default=str(DEFAULT_POS_OUT),
                    help="Path for the four-sided-border Proof of Service PDF")
    ap.add_argument("--skip-order", action="store_true")
    ap.add_argument("--skip-pos", action="store_true")
    args = ap.parse_args()
    path = build_opposition(Path(args.out).resolve(), args.date, args.mailed_from)
    print(f"Generated opposition: {path}")
    if not args.skip_pos:
        pos = build_opposition_proof_of_service(
            Path(args.pos_out).resolve(), args.date, args.mailed_from
        )
        print(f"Generated proof of service: {pos}")
    if not args.skip_order:
        order = build_proposed_order(Path(args.order_out).resolve(), args.date,
                                     args.mailed_from)
        print(f"Generated proposed order: {order}")


if __name__ == "__main__":
    main()
