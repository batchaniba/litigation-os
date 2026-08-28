#!/usr/bin/env python3
"""Matter 26 -- Plaintiff's Opposition to UPS's Rule 12(b)(6) Motion to Dismiss.

Newanforbi v. United Parcel Service, Inc., USDC E.D. Cal. No. 2:26-cv-02847-DAD-CKD.
Hearing: October 5, 2026, 1:30 p.m., Courtroom 4 (Hon. Dale A. Drozd).

Built off ECF No. 7 / 7-1 / 7-2 / 7-3 (filed Aug. 26, 2026), the verified
Complaint (ECF No. 1, Ex. 1), and the First Advantage report UPS lodged as
Exhibit A. Hybrid architecture (Claude Code organization + Cursor caution):

  1. Four-part (j)(3) -> Labor Code 432.7 argument, including the words UPS
     dropped from 432.7(n) and the Cel-Tech distinction UPS quoted against
     itself.
  2. Two-field layout: Record Source = database queried; SOURCE OF RECORD =
     origin of the returned record. The statute speaks to the information,
     not the portal.
  3. Characterize Exhibit A at the Rule 12(b)(6) inference level. Do not
     attack Exhibit A as a "litigation reprint." If A is out, the Complaint
     controls; if A is in, read the California-source field.
  4. To the extent Exhibit B is considered, consider it as a whole. Use its
     theft/dishonesty purpose affirmatively. Do not request Rule 12(d)
     conversion.
  5. Concede Counts II and V as labeled; ICRAA tracks 1786.16(b)(1)'s
     request-and-three-business-day rule; UCL standing was not raised.
  6. Mendoza is an anti-SLAPP employer-vs-screener discussion, not a merits
     holding that the prohibition "targets" decisionmakers as such.

Rendered on the shared pleading-paper engine and signed with the portfolio
universal signature (bnn.cdl@gmail.com -- not the UPS COS misspelling).

Date the signature and Proof of Service with --date on the day of actual
service. Do not pre-date a September 9 certificate. L.R. 230(c) due date is
September 9, 2026; that is not the certificate date. Judge Drozd Standing
Order I.E does not require a proposed order with this civil motion; generate
one only as a portfolio draft and do not file it unless the Court asks.

Service is first-class mail (Fed. R. Civ. P. 5(b)(2)(C); E.D. Cal. L.R. 135).
The Proof of Service is the portfolio four-sided-border form
(``lib/proof_of_service.py``), appended as the last page of the opposition PDF.
Do not serve or file the proposed order.

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
from pdf_packet import assemble  # noqa: E402
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
     "UPS's motion rests on a single factual premise: that \"[t]here is not a single "
     "reference to any California based sex offender registry included in the background "
     "check UPS obtained.\" (Mot. 4:18-19.) The document UPS attached to its own motion "
     "refutes that premise. On page 6 of Exhibit A, in the block describing the one "
     "search that returned a record, the report states: \"SOURCE OF RECORD: CALIFORNIA "
     "SEX OFFENDER REGISTRY.\" (ECF No. 7 at 19 (Ex. A at 6).)"),

    ("PARA",
     "UPS has also already conceded the element it now disputes. Its motion states: "
     "\"UPS does not dispute the fact that it used information derived from Plaintiff's "
     "criminal background check when it made the decision to not hire him.\" (Mot. "
     "2:14-16.) Exhibit A identifies exactly one adverse component in that background "
     "check. The criminal-records search -- \"First Advantage National Criminal File "
     "Plus,\" Stockton, San Joaquin County -- returned \"No Record Found\" and scored "
     "\"Eligible.\" (ECF No. 7 at 17-18 (Ex. A at 4-5).) The only components that "
     "returned \"Record Found\" and scored \"Decisional\" were the sex offender registry "
     "searches. (Id. at 17, 19 (Ex. A at 4, 6).) The overall result was \"INELIGIBLE.\" "
     "(Id. at 17 (Ex. A at 4).) At minimum, a reasonable inference is that the "
     "information UPS used was the registry hit."),

    ("PARA",
     "Those two propositions resolve this motion. UPS concedes that it used information "
     "derived from the report. The report supports the reasonable inference that the "
     "only adverse information in it was a sex offender registry entry whose source of "
     "record is California's registry. That is the use Penal Code section 290.46(j)(2)(E) "
     "prohibits."),

    ("PARA",
     "UPS's fallback is that Penal Code section 290.46(j)(3) directs the Court to Labor "
     "Code section 432.7 and thereby creates a \"safe harbor, protecting UPS's exact "
     "course of action.\" (Mot. 10:16-21.) It does not, for four independent reasons -- "
     "among them that UPS reaches that conclusion only by deleting the operative "
     "condition from its own quotation of the statute. Section 432.7(n) shelters an "
     "employer \"required by state, federal, or local law to conduct criminal background "
     "checks.\" UPS's brief quotes the subdivision with that clause bracketed away. "
     "(Mot. 4:3-6.) UPS identifies no state, federal, or local law requiring such "
     "screening for this position."),

    ("PARA",
     "Finally, UPS's own disclosure to Plaintiff states why it ordered the report: to "
     "evaluate whether Plaintiff \"would present an unacceptable risk of theft or other "
     "dishonest behavior.\" (ECF No. 7 at 27 (Ex. B).) A sex offender registry entry "
     "bears on neither. UPS therefore used registry information for a purpose outside "
     "not only section 290.46(j)(1), but outside the purpose UPS itself disclosed."),

    ("PARA",
     "The Court should deny the motion as to Count I and the claims that depend upon "
     "it. To the extent any claim is found deficient, dismissal should be without "
     "prejudice and with leave to amend."),

    ("HEADER", "II.\nSTATEMENT OF RELEVANT FACTS"),

    ("PARA",
     "1. On July 17, 2024, Plaintiff completed an online application for the position "
     "\"Loader/Unloader -- Hub\" at UPS's Lathrop, California hub (US -- LATHROP HUB "
     "(CALAH)), Twilight shift, Monday through Friday, 15:00-23:30. (Compl. \u00b616; "
     "ECF No. 7 at 21 (Ex. B).)"),

    ("PARA",
     "2. UPS initiated a pre-employment background screening through First Advantage, "
     "a consumer reporting agency. The report was ordered July 17, 2024 at 9:52 p.m. "
     "and completed July 18, 2024 at 6:50 p.m. (Compl. \u00b617; ECF No. 7 at 14, 17 "
     "(Ex. A at 1, 4).)"),

    ("PARA",
     "3. The report's \"Background Report Summary\" lists each component ordered and "
     "the score returned: Social Security Verification -- \"Pass\"; First Advantage "
     "National Criminal File Plus (Stockton, San Joaquin, CA) -- \"Eligible\"; National "
     "Sex Offender Registry -- \"Decisional\"; and National Sex Offender Registry Search "
     "-- Department Of Justice Web Site -- \"Decisional.\" (ECF No. 7 at 17 (Ex. A at "
     "4).)"),

    ("PARA",
     "4. The criminal-records component returned \"Search Results: No Record Found.\" "
     "(ECF No. 7 at 18 (Ex. A at 5).) No conviction record, and no arrest record, "
     "appears anywhere in Exhibit A."),

    ("PARA",
     "5. The registry component returned \"Search Results: Record Found.\" Its detail "
     "block on page 6 contains two distinct source fields. The field labeled \"Record "
     "Source\" reads \"NATIONAL SEX OFFENDER REGISTRY\" -- identifying the database "
     "queried. The field describing the record that was returned reads: \"SOURCE OF "
     "RECORD: CALIFORNIA SEX OFFENDER REGISTRY\" and \"SENTENCE: REGISTERED SEX "
     "OFFENDER.\" (ECF No. 7 at 19 (Ex. A at 6).)"),

    ("PARA",
     "6. On July 19, 2024, the report was scored: \"BASED ON YOUR CRITERIA, THE OVERALL "
     "CASE SCORE IS INELIGIBLE,\" under the comment \"Adjudicated by the Centralized "
     "Adjudication Team.\" (ECF No. 7 at 17 (Ex. A at 4).)"),

    ("PARA",
     "7. The report carried a remark directed to UPS: \"City Ordinance, State, or "
     "Federal law requires additional action and disclosure by employer to consumer "
     "prior to taking adverse action based on Consumer Report.\" (Id.)"),

    ("PARA",
     "8. UPS's written disclosure to Plaintiff stated the purpose of the report: "
     "because the position \"will involve access to confidential financial and other "
     "business information and valuable property belonging to UPS's customers, a "
     "consumer report about you is necessary and important for UPS to review in order "
     "to evaluate whether you would present an unacceptable risk of theft or other "
     "dishonest behavior in the performance of your job.\" (ECF No. 7 at 27 (Ex. B).)"),

    ("PARA",
     "9. Between July 22 and July 27, 2024, Plaintiff received pre-adverse action "
     "notices. On July 31, 2024, UPS issued a final adverse action notice denying "
     "Plaintiff employment. (Compl. \u00b6\u00b618, 19, 25.) No other disqualifying "
     "information existed. (Compl. \u00b627.)"),

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
     "for summary judgment under Rule 56\" and \"all parties must be given a reasonable "
     "opportunity to present all the material that is pertinent.\" Fed. R. Civ. P. 12(d). "
     "Plaintiff does not ask the Court to convert this motion. The Rule is stated "
     "because it supplies the procedure if the Court determines that extra-pleading "
     "material must be considered for its truth."),

    ("HEADER", "IV.\nARGUMENT"),

    ("SUBHEAD",
     "A.  UPS Concedes the Use, and Its Own Exhibit Supplies the Source"),

    ("PARA",
     "1.  UPS concedes that it used information derived from the report."),

    ("PARA",
     "Section 290.46(j)(2)(E) prohibits the \"use of any information that is disclosed "
     "pursuant to this section\" for purposes relating to employment. The operative "
     "conduct is use. UPS concedes it: \"UPS does not dispute the fact that it used "
     "information derived from Plaintiff's criminal background check when it made the "
     "decision to not hire him.\" (Mot. 2:14-16.)"),

    ("PARA",
     "What UPS disputes is only the character of the information used. To the extent "
     "the Court considers Exhibit A, as UPS asks it to, that dispute is not a pleading "
     "failure. Of the four components ordered, three were not adverse: Social Security "
     "Verification scored \"Pass,\" and the criminal-records search scored \"Eligible\" "
     "on \"No Record Found.\" (ECF No. 7 at 17-18 (Ex. A at 4-5).) The two registry "
     "searches alone scored \"Decisional,\" and the case then scored \"INELIGIBLE.\" "
     "(Id. at 17 (Ex. A at 4).) At minimum, a reasonable inference is that the "
     "information UPS used was the registry hit. That is the use section "
     "290.46(j)(2)(E) forbids."),

    ("PARA",
     "2.  Exhibit A identifies the source of that information as California's registry."),

    ("PARA",
     "UPS argues that \"[t]here is not a single reference to any California based sex "
     "offender registry included in the background check UPS obtained.\" (Mot. 4:18-19.) "
     "Page 6 of Exhibit A states: \"SOURCE OF RECORD: CALIFORNIA SEX OFFENDER "
     "REGISTRY.\" (ECF No. 7 at 19 (Ex. A at 6).) The premise of UPS's motion is "
     "contradicted by UPS's own evidence."),

    ("PARA",
     "The report does not merely mention California in passing. Its registry detail "
     "block contains two separate and differently labeled fields:"),

    ("LIST_ITEM",
     "Record Source:  NATIONAL SEX OFFENDER REGISTRY"),

    ("LIST_ITEM",
     "Sentence:  SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY / SENTENCE: "
     "REGISTERED SEX OFFENDER"),

    ("PARA",
     "(ECF No. 7 at 19 (Ex. A at 6).) The two fields report two different things. "
     "\"Record Source\" identifies the database that was queried. The \"SOURCE OF "
     "RECORD\" line identifies the origin of the record that the query returned. Read "
     "together -- and they must be read together, because they appear four lines apart "
     "in the same block of the same document UPS asks the Court to consider -- they "
     "support the reasonable inference that the record UPS acted on was a California "
     "registry record retrieved through a national index."),

    ("PARA",
     "That distinction is dispositive of UPS's argument. Section 290.46(j)(2)(E) reaches "
     "\"information that is disclosed pursuant to this section.\" The statute speaks to "
     "the information, not to the portal through which an end user retrieves it. UPS's "
     "reading would let any employer evade the prohibition by routing the same "
     "California data through a federal index. \"The fundamental purpose of statutory "
     "construction is to ascertain the intent of the lawmakers so as to effectuate the "
     "purpose of the law.\" <<i:People v. Pieters>>, 52 Cal. 3d 894, 898 (1991)."),

    ("PARA",
     "The California Court of Appeal has already located the prohibition's target, in "
     "an anti-SLAPP posture. In <<i:Mendoza v. ADP Screening & Selection Services, Inc.>>, "
     "182 Cal. App. 4th 1644 (2010), a screening company transmitted Megan's Law "
     "information to a prospective employer. The court explained that \"the statutory "
     "liability created by the MLW statute should be limited to employers who 'use' "
     "information disclosed on the MLW as a basis for an employment decision,\" and "
     "that the Legislature did not intend liability for businesses that \"merely "
     "reproduce or republish such information, without actually acting on the "
     "information.\" Id. at 1658-59. \"His cause of action, if any, lies against his "
     "prospective employer, and not SASS.\" Id. at 1659. UPS is the prospective "
     "employer. It received California-sourced registry information and, by its own "
     "concession, used the background check to deny hire. That is the conduct the "
     "statute reaches."),

    ("PARA",
     "3.  At minimum, this presents a question that cannot be resolved on the "
     "pleadings."),

    ("PARA",
     "Even if the Court were to regard the relationship between the national index and "
     "the state registry as genuinely contested, that would defeat the motion rather "
     "than support it. How First Advantage retrieved the record, what UPS instructed "
     "it to search, and what UPS in fact reviewed are questions of fact. On a Rule "
     "12(b)(6) motion they are resolved in Plaintiff's favor. Iqbal, 556 U.S. at 678; "
     "Manzarek, 519 F.3d at 1031."),

    ("SUBHEAD",
     "B.  Section 290.46(j)(3) Does Not Deliver UPS a Safe Harbor"),

    ("PARA",
     "UPS argues that section 290.46(j)(3) \"provides an exception to the general "
     "prohibition by directing us to Cal. Labor Code \u00a7 432.7(n),\" and that the "
     "Legislature thereby \"contemplated, codified, and enacted this safe harbor, "
     "protecting UPS's exact course of action.\" (Mot. 10:16-21.) Four independent "
     "defects sink that argument."),

    ("PARA",
     "1.  Subdivision (j)(3) preserves uses that section 432.7 authorizes; section "
     "432.7 authorizes nothing here."),

    ("PARA",
     "Subdivision (j)(3) provides that section 290.46 \"shall not affect authorized "
     "access to, or use of, information pursuant to\" a list of other provisions, "
     "including Labor Code section 432.7. The operative words are \"authorized\" and "
     "\"pursuant to.\" Subdivision (j)(3) preserves whatever access or use those other "
     "statutes affirmatively authorize. It does not convert every statute on the list "
     "into a general license."),

    ("PARA",
     "Labor Code section 432.7 authorizes nothing here. It is a prohibitory statute: "
     "section 432.7(a)(1) forbids employers to use records of arrest or detention that "
     "did not result in conviction. Subdivision (n) is a savings clause -- it states "
     "what the section \"does not prohibit.\" A provision declining to prohibit conduct "
     "is not a provision authorizing it. As UPS itself observes in a different part of "
     "its brief, \"[t]here is a difference between (1) not making an activity unlawful, "
     "and (2) making that activity lawful.\" <<i:Cel-Tech Commc'ns, Inc. v. Los Angeles "
     "Cellular Tel. Co.>>, 20 Cal. 4th 163, 183 (1999) (quoted at Mot. 10:12-13). UPS's "
     "safe-harbor argument requires the second; section 432.7(n) supplies at most the "
     "first."),

    ("PARA",
     "2.  UPS reaches its reading only by deleting the statute's operative condition."),

    ("PARA",
     "UPS represents that section 432.7 does not prohibit an employer from "
     "\"conduct[ing] criminal background checks for employment purposes or to restrict "
     "employment based on criminal history from complying with those requirements.\" "
     "(Mot. 4:3-6.) The bracketed alteration is not cosmetic. The statute reads:"),

    ("PARA",
     "\"This section does not prohibit an employer, whether a public agency or private "
     "individual or corporation, required by state, federal, or local law to conduct "
     "criminal background checks for employment purposes or to restrict employment "
     "based on criminal history from complying with those requirements . . . .\""),

    ("PARA",
     "Cal. Lab. Code \u00a7 432.7(n) (emphasis added). The subdivision shelters employers "
     "that are required by law to screen. UPS's bracket converts \"required . . . to "
     "conduct criminal background checks\" into \"conduct[ing] criminal background "
     "checks,\" which drops the condition on which the entire subdivision turns. UPS "
     "identifies no state, federal, or local law requiring it to conduct a sex offender "
     "registry search for a warehouse loader position. UPS screened Plaintiff "
     "voluntarily, as \"part of its standard pre-employment screening process.\" "
     "(Compl. \u00b617; ECF No. 7 at 3.)"),

    ("PARA",
     "3.  The remainder of subdivision (n) addresses seeking and receiving reports, "
     "not using registry information."),

    ("PARA",
     "The balance of section 432.7(n) provides that the section does not prohibit an "
     "employer \"from seeking or receiving an applicant's criminal history report that "
     "has been obtained pursuant to procedures otherwise provided for under federal, "
     "state, or local law.\" That clause speaks to procurement. Section 290.46(j)(2)(E) "
     "prohibits use. Lawfully receiving a report does not authorize using a registry "
     "entry within it to deny employment -- which is precisely the conduct section "
     "290.46(j)(2)(E) singles out. Reading section 432.7(n) as UPS does would repeal "
     "section 290.46(j)(2)(E) by implication as to every employer that orders a "
     "background check, which is to say all of them. Repeals by implication are "
     "disfavored."),

    ("PARA",
     "4.  Section 432.7 governs arrest and conviction records; Exhibit A shows "
     "neither."),

    ("PARA",
     "Section 432.7 is, by its terms, about records of arrest, detention, and "
     "conviction. Exhibit A contains no such record. The criminal-records search "
     "returned \"No Record Found\" and scored \"Eligible.\" (ECF No. 7 at 18 (Ex. A at "
     "5).) The only entry marked \"Record Found\" reports a registration status -- "
     "\"SENTENCE: REGISTERED SEX OFFENDER\" -- not a conviction. (Id. at 19 (Ex. A at "
     "6).) There was no section 432.7 record for section 432.7 to authorize the use of."),

    ("PARA",
     "UPS attempts to close that gap by inference: \"By alleging that UPS impermissibly "
     "accessed California's Megan's Law website, Plaintiff impliedly admits to being "
     "convicted of a sex crime . . . . Because Plaintiff admits to being convicted of "
     "a sex crime, if UPS used Plaintiff's conviction record as part of its analysis "
     "when making the decision to not hire him, it was entitled to do so.\" (Mot. "
     "4:9-13.) That argument asks the Court to draw an inference against the "
     "non-moving party on a Rule 12(b)(6) motion, to supply by implication a conviction "
     "record that UPS's own exhibit affirmatively negates, and then to assume UPS used "
     "a record it does not have. Each step is impermissible; taken together they are "
     "the opposite of the standard. Manzarek, 519 F.3d at 1031."),

    ("SUBHEAD",
     "C.  UPS's Own Disclosure Establishes That This Was Not an Authorized Use"),

    ("PARA",
     "Section 290.46(j)(1) states the only authorized use of registry information: a "
     "person \"is authorized to use information disclosed pursuant to this section only "
     "to protect a person at risk.\" Subdivision (j)(2) then prohibits every other use, "
     "employment among them."),

    ("PARA",
     "To the extent Exhibit B is properly considered, it must be considered as a whole, "
     "and it forecloses any claim that UPS acted to protect a person at risk. UPS told "
     "Plaintiff, in writing, why it was ordering the report: because the position "
     "\"will involve access to confidential financial and other business information "
     "and valuable property belonging to UPS's customers,\" the report was \"necessary "
     "and important for UPS to review in order to evaluate whether you would present "
     "an unacceptable risk of theft or other dishonest behavior in the performance of "
     "your job.\" (ECF No. 7 at 27 (Ex. B).) UPS repeated the same rationale in the "
     "authorization it asked Plaintiff to sign. (Id. at 26 (Ex. B).)"),

    ("PARA",
     "Theft and dishonesty are the stated purpose. A sex offender registry entry speaks "
     "to neither. And the position itself -- a Twilight-shift loader and unloader "
     "inside a Lathrop package hub, 15:00 to 23:30 (id. at 21 (Ex. B)) -- is not "
     "alleged to involve responsibility for, or contact with, any identified person at "
     "risk. (Compl. \u00b636.) On UPS's own account of its own screening, the registry "
     "information served no authorized purpose. It served a prohibited one."),

    ("SUBHEAD",
     "D.  If the Exhibits Are Considered, They Must Be Considered as a Whole"),

    ("PARA",
     "A document may be incorporated by reference only \"if the plaintiff refers "
     "extensively to the document or the document forms the basis of the plaintiff's "
     "claim.\" <<i:United States v. Ritchie>>, 342 F.3d 903, 908 (9th Cir. 2003) (quoted "
     "at Mot. 3:27-4:1). The Ninth Circuit has cautioned against overuse of the "
     "doctrine and instructed that a court should not \"assume the truth of an "
     "incorporated document if such assumptions only serve to dispute facts stated in "
     "a well-pleaded complaint.\" <<i:Khoja v. Orexigen Therapeutics, Inc.>>, 899 F.3d 988, "
     "998, 1003 (9th Cir. 2018)."),

    ("PARA",
     "Two consequences follow for Exhibit A. First, if Exhibit A is not incorporated, "
     "the Complaint's allegations control: the report contained California registry "
     "information, and UPS used it to deny hire. (Compl. \u00b6\u00b62, 21, 23, 26, "
     "34-36.) Second, if Exhibit A is incorporated, it must be read in its entirety, "
     "including the source-of-record line on page 6. Khoja does not permit UPS to "
     "credit the \"NATIONAL SEX OFFENDER REGISTRY\" Record Source label and disregard "
     "the Sentence field that identifies \"CALIFORNIA SEX OFFENDER REGISTRY\" as the "
     "source of record. Either path denies dismissal of Count I. What the Court may "
     "not do is take UPS's characterization of Exhibit A as true and the document's "
     "California-source field as false."),

    ("PARA",
     "To the extent Exhibit B is properly considered, it likewise must be considered "
     "as a whole. It does not establish compliance with the disputed statutory "
     "obligations. It is a printout of an applicant-tracking system's completion log. "
     "It shows that screens were displayed in July 2024. It does not show that UPS "
     "discharged Civil Code section 1786.16. What Exhibit B does show, and what "
     "Plaintiff uses it for, is the purpose UPS disclosed: theft and dishonesty. That "
     "use is addressed in Part IV.C. It does not require the Court to resolve disputed "
     "facts against Plaintiff."),

    ("PARA",
     "UPS also filed the declaration of Ashley Felsing, an HRBP Director, as ECF No. "
     "7-2, attaching the same report and the application disclosures. Incorporation by "
     "reference, if it applies, reaches those documents. It does not reach "
     "extra-pleading testimony characterizing what UPS \"accessed\" or how it decided. "
     "Those characterizations should not be resolved against Plaintiff on this motion. "
     "If the Court determines that considering such testimony would require conversion, "
     "Rule 12(d) supplies the procedure. Plaintiff does not ask the Court to convert."),

    ("SUBHEAD",
     "E.  Count III (ICRAA) Turns on Facts That Cannot Be Resolved on the Pleadings"),

    ("PARA",
     "UPS argues Plaintiff \"admits\" ICRAA compliance because Exhibit B contains a "
     "disclosure naming First Advantage and because Plaintiff received pre-adverse and "
     "final adverse notices. (ECF No. 7 at 6-7.) That is a "
     "summary-judgment argument dressed as a 12(b)(6). Khoja does not require the "
     "Court to treat UPS's characterization of Exhibit B as true over the Complaint's "
     "sworn allegations. 899 F.3d at 1003."),

    ("PARA",
     "Plaintiff does not rest Count III on a theory that Exhibit B failed to name "
     "First Advantage or to use the phrase \"investigative consumer report.\" He also "
     "does not rest Count III on a theory that a Penal Code section 290.46 violation "
     "is, without more, an ICRAA violation. Paragraph 46's \"spirit and purpose\" "
     "allegation is not the statutory hook."),

    ("PARA",
     "The Complaint's live ICRAA theory is Civil Code section 1786.16. Subdivision "
     "(a)(5) and (b)(1) require the procuring person to provide a means to request a "
     "copy of the report and, if requested, to send a copy within three business days "
     "of the date the report is provided to the recipient. Subdivision (b)(2) requires "
     "compliance with section 1786.40 if adverse action is a consideration -- advising "
     "the consumer of the action and supplying the name and address of the reporting "
     "agency. (Compl. \u00b6\u00b624, 47(b).) Paragraph 24 alleges the First Advantage "
     "portal link expired and Plaintiff no longer has access to the underlying report."),

    ("PARA",
     "To the extent Exhibit B is properly considered, it does not close that gap. The "
     "California disclosure UPS relies on offers a copy of the report \"by checking the "
     "box beneath your signature as indicated below.\" (ECF No. 7 at 27 (Ex. B).) "
     "Nothing in Exhibit B shows whether that box was checked. Nothing in Exhibit B "
     "shows that any copy of the report was ever sent, let alone within three business "
     "days of the date the report was provided to UPS. Whether UPS satisfied section "
     "1786.16(b)(1) is a question for summary judgment or trial. Khoja, 899 F.3d at "
     "1003."),

    ("PARA",
     "If the Court concludes that paragraph 47(b) was pled closer to a "
     "copy-before-adverse-action formulation than to section 1786.16(b)(1)'s "
     "request-and-three-day rule, the defect is labeling, not futility: the same facts "
     "support leave to conform the citation. Lopez, 203 F.3d at 1130. Separately, "
     "consent to procure a report is not consent to misuse its results. Even a fully "
     "compliant procurement does not make lawful a use that section 290.46(j)(2)(E) "
     "prohibits."),

    ("SUBHEAD", "F.  Count IV (Invasion of Privacy) Is Adequately Pleaded"),

    ("PARA",
     "UPS argues that Plaintiff has no protected privacy interest because criminal "
     "records are public, and that he consented in any event. (Mot. 7:17-27.) Neither "
     "argument prevails on the pleadings."),

    ("PARA",
     "Count IV arises under the California Constitution's guarantee of privacy. Cal. "
     "Const. art. I, \u00a7 1. A California constitutional privacy claim requires (1) a "
     "legally protected privacy interest, (2) a reasonable expectation of privacy under "
     "the circumstances, and (3) a serious invasion of that interest. <<i:Hill v. Nat'l "
     "Collegiate Athletic Ass'n>>, 7 Cal. 4th 1, 35-40 (1994). The privacy interest here "
     "is not an interest in secrecy; it is an interest in how information already "
     "disclosed may be used. The Legislature created exactly that interest when it "
     "authorized use of registry information solely \"to protect a person at risk\" and "
     "prohibited every other use, employment expressly among them. Cal. Penal Code "
     "\u00a7 290.46(j)(1)-(2)(E). A statute that permits publication for one purpose and "
     "forbids it for another creates a legally protected interest in the difference. "
     "That satisfies the first Hill element. Hill, 7 Cal. 4th at 40."),

    ("PARA",
     "Consent fails because consent is measured by its scope. "
     "Plaintiff consented to what UPS asked for -- a report to assess \"risk of theft "
     "or other dishonest behavior.\" (ECF No. 7 at 27 (Ex. B).) He did not consent, and "
     "could not have consented, to UPS using Megan's Law registry data in a manner the "
     "Legislature has declared unlawful. Whether the intrusion exceeded the scope of "
     "consent is a fact question. (Compl. \u00b6\u00b650-52.) Hill itself treats reasonable "
     "expectation and seriousness as mixed questions, adjudicable as law only when the "
     "facts are undisputed. 7 Cal. 4th at 40. They are not."),

    ("SUBHEAD",
     "G.  Count II (Failure to Hire) Should Be Dismissed Without Prejudice"),

    ("PARA",
     "UPS cites <<i:Williams v. Sacramento River Cats Baseball Club, LLC>>, 40 Cal. App. "
     "5th 280 (2019), for the proposition that the Tameny tort does not extend to "
     "failure-to-hire claims. Plaintiff does not defend Count II as currently pleaded "
     "and does not ask the Court to extend Tameny."),

    ("PARA",
     "Count II's disposition does not affect Count I. Count I is a statutory claim "
     "under Penal Code section 290.46(j)(4)(A), which makes any person who uses "
     "registry information in violation of subdivision (j)(2) \"liable for the actual "
     "damages, and any amount that may be determined by a jury or a court sitting "
     "without a jury, not exceeding three times the amount of actual damage, and not "
     "less than two hundred fifty dollars ($250), and attorney's fees, exemplary "
     "damages, or a civil penalty not exceeding twenty-five thousand dollars "
     "($25,000).\" That liability does not depend on any employment relationship, and "
     "Williams does not touch it. (Compl. \u00b6\u00b613, 33-37.)"),

    ("PARA",
     "Plaintiff respectfully requests that Count II be dismissed without prejudice."),

    ("SUBHEAD",
     "H.  Count V (Negligence Per Se) Should Be Dismissed With Leave to Amend"),

    ("PARA",
     "UPS correctly observes that negligence per se is a doctrine rather than an "
     "independent cause of action. <<i:Dent v. Nat'l Football League>>, 902 F.3d 1109, 1117 "
     "(9th Cir. 2018). Plaintiff does not dispute that. UPS's own authority, <<i:Quinn v. "
     "Coulton>>, 121 Cal. App. 5th 1124 (2026) (cited at Mot. 8:9-11, 8:22-24), likewise "
     "treats the doctrine as an evidentiary presumption rather than a freestanding "
     "claim."),

    ("PARA",
     "The Complaint expressly invokes Evidence Code section 669 and identifies both "
     "the class of persons the statute protects and the harm it was designed to "
     "prevent. (Compl. \u00b6\u00b654-57.) A pro se pleading is construed by its substance "
     "rather than its label. Hebbe, 627 F.3d at 342. Plaintiff requests leave to amend "
     "to plead ordinary negligence (duty, breach, causation, damages) with the section "
     "669 presumption in its proper evidentiary role. That amendment is not futile. "
     "Lopez, 203 F.3d at 1130."),

    ("SUBHEAD",
     "I.  Count VI (UCL) States a Claim Under Both the Unlawful and the Unfair Prong"),

    ("PARA",
     "Count VI arises under Business and Professions Code section 17200. Under the "
     "unlawful prong, the UCL \"borrows\" violations of other law and makes them "
     "independently actionable. Cel-Tech, 20 Cal. 4th at 180. UPS's sole answer is that "
     "it did not violate section 290.46(j)(2)(E). (Mot. 10:1-2.) For the reasons stated "
     "in Parts IV.A through IV.C, that premise fails, and the borrowed violation "
     "stands. (Compl. \u00b661.)"),

    ("PARA",
     "Under the unfair prong, a practice is unfair when it \"offends an established "
     "public policy.\" <<i:Podolsky v. First Healthcare Corp.>>, 50 Cal. App. 4th 632, 647 "
     "(1996) (cited at Mot. 10:5). Even if the Court were to conclude that section "
     "290.46(j)(2)(E) does not reach data retrieved through a national index, UPS's "
     "practice -- obtaining California registry data through an intermediary index and "
     "then denying employment on it, for a position UPS itself described as screened "
     "for theft risk -- offends the policy the Legislature established in section "
     "290.46(j). (Compl. \u00b662.) UPS's Cel-Tech argument (Mot. 10:10-22) proves "
     "nothing, because it depends entirely on the section 432.7 safe harbor addressed "
     "in Part IV.B: the Legislature has not \"made lawful\" the use of registry "
     "information for employment; it has expressly prohibited it."),

    ("PARA",
     "UPS does not challenge Plaintiff's standing under Business and Professions Code "
     "section 17204, and the issue is therefore not before the Court."),

    ("HEADER", "V.\nANY DISMISSAL SHOULD BE WITHOUT PREJUDICE AND WITH LEAVE TO AMEND"),

    ("PARA",
     "UPS asks for dismissal with prejudice and asserts that \"even with leave to amend "
     "his Complaint he would not be able to cure that deficiency.\" (Mot. 11:2-4.) That "
     "assertion cannot be squared with UPS's own exhibit, which identifies the "
     "California Sex Offender Registry as the source of record for the only adverse "
     "entry in the screening."),

    ("PARA",
     "This is Plaintiff's original complaint. It was verified and filed when the First "
     "Advantage report was not in Plaintiff's possession. (Compl. \u00b624.) \"A pro se "
     "litigant must be given leave to amend his or her complaint unless it is "
     "absolutely clear that the deficiencies of the complaint could not be cured by "
     "amendment.\" Noll, 809 F.2d at 1448; accord Lopez, 203 F.3d at 1130. Should the "
     "Court find any claim deficient, Plaintiff can plead the source-of-record evidence "
     "now in the record, restate Count V as ordinary negligence, and drop Count II."),

    ("PARA",
     "Rule 15(a)(1)(B) permits one amendment as of right within 21 days after service "
     "of a Rule 12(b) motion. UPS served the motion by mail on August 26, 2026. (ECF "
     "No. 7-3.) Twenty-one days after that service is September 16, 2026. Because "
     "service was by mail, Rule 6(d) may add three days, through September 19, 2026. "
     "Plaintiff will confirm the operative date from the envelope if it differs. L.R. "
     "230(c) is a different clock, runs from filing, and is not extended by Rule 6(d): "
     "this opposition remains due September 9, 2026. The Initial Scheduling Order "
     "advised of the Rule 15 window. (ECF No. 2.) Futility is not established. The "
     "facts that would be added are the facts UPS already put in the record: the "
     "two-field California source line, the Eligible criminal search, the INELIGIBLE "
     "centralized adjudication, and the theft-purpose disclosure. Dismissal with "
     "prejudice on this record would be an abuse of discretion."),

    ("HEADER", "VI.\nCONCLUSION"),

    ("PARA",
     "UPS cannot obtain dismissal by asserting that the information it used did not "
     "come from California's registry when its own Exhibit A names the California Sex "
     "Offender Registry as the source of record, and when UPS has conceded that it used "
     "information derived from that report. At minimum, a reasonable inference is that "
     "the information UPS used was the registry hit. Section 290.46(j)(3) and Labor "
     "Code section 432.7 do not authorize that use."),

    ("PARA",
     "Plaintiff respectfully requests that the Court deny the motion as to Count I "
     "(Penal Code \u00a7 290.46), Count III (ICRAA), Count IV (invasion of privacy), and "
     "Count VI (UCL). As to Count II and Count V, Plaintiff requests dismissal without "
     "prejudice and with leave to amend. Plaintiff further requests that, to the extent "
     "the Court considers Exhibits A and B, it consider each as a whole, including "
     "Exhibit A's source-of-record line, and that it not use those exhibits to resolve "
     "disputed facts against Plaintiff at the pleading stage."),
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
    d.ensure_space(10)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
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


def append_pdfs(front: Path, back: Path) -> Path:
    """Write front+back into front (in place). Used to attach the POS."""
    assemble([front, back], front)
    return front


def build_opposition(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    _header_block(d, CAPTION_RIGHT)
    _render_body(d, CONTENT)
    _signature(d, exec_date)
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
    if not args.skip_pos:
        pos = build_opposition_proof_of_service(
            Path(args.pos_out).resolve(), args.date, args.mailed_from
        )
        append_pdfs(path, pos)
        print(f"Generated opposition (POS attached): {path}")
        print(f"Generated proof of service: {pos}")
    else:
        print(f"Generated opposition: {path}")
    if not args.skip_order:
        order = build_proposed_order(Path(args.order_out).resolve(), args.date,
                                     args.mailed_from)
        print(f"Generated proposed order: {order}")


if __name__ == "__main__":
    main()
