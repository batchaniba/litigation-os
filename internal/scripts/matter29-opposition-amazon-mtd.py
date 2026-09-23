# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 29 -- Plaintiff's Opposition to Amazon.com Services LLC's Motion to
Dismiss the Fifth, Sixth, and Seventh Claims (N.D. Cal. No. 4:26-cv-09249-ASK),
with Table of Contents and Table of Authorities, plus a [Proposed] Order that
tracks the Conclusion, rendered on portfolio pleading paper with the canonical
signature. The Proof of Service is the house form, generated separately by
matter29-opposition-pos-email.py.

  python3 internal/scripts/matter29-opposition-amazon-mtd.py

Posture: fight the Fifth Claim (privacy); non-oppose the Sixth (UCL) and
Seventh (IIED) as against Amazon only, without prejudice; fence Claims 1-4 and
the extra-record footnote out of the motion.

Revision (Sep. 23, 2026) applied to the reviewed 8-page draft:
  - "collected or used" -> use to deny employment (the statute's actual target)
  - Hill preservation sentence added at the end of the privacy-interest section
  - "Guzman controls" softened; state-forum refiling no longer foregrounded
  - In re Facebook Internet Tracking removed (off-point; not in citation index)
  - Added: Statement of Issues (Civ. L.R. 7-4(a)(3)), TOA, record-scope section
    with the Lerma report contrast, case-by-case distinctions, Rule 8(d)
    alternative-pleading section, limited-scope request for any privacy
    dismissal, leave-to-amend section, Rule 12(a)(4) fence
  - Front matter on its own pages so the TOC no longer splits across page 1
  - Dated September 22, 2026 (POS: matter29-opposition-pos-email.py, Sep. 23)

Second review pass (Sep. 23, 2026):
  - Hill "sensitive and confidential" confronted directly; theory rests on
    restricted use, context, consent scope, and harm, not confidentiality
  - "nullify" softened; statute informs norms but does not supply every element
  - Countervailing-interest point no longer framed as an affirmative defense;
    "high bar" paragraph no longer says the Court cannot dismiss
  - "Unrebutted" -> Court takes the alternative source allegations as true
  - Lerma characterized through Compl. paras. 31-33, not the foreign order
  - Rule 12(d) conversion and Rule 12(a)(4) sentences removed from the brief
  - UCL heading and opener reworded; redundant hearing paragraph removed
  - Non-breaking spaces keep pin cites on one line; "misuse" emphasized
  - [Proposed] Order added; brief dated Sep. 23, POS Sep. 24
  - In re Facebook Internet Tracking stays out (off-point; not indexed)

Accurate answer update (Sep. 23, 2026): Accurate answered (ECF No. 21) and
did not join. Brief notes that procedurally, cites the "pending" admission
and registry denials only as a co-defendant's pleaded positions that cannot
resolve a Rule 12(b)(6) motion, and adds the admission to the UCL amendment
proffer. Accurate's defenses are not briefed. VERIFY ECF No. 21 paragraph pins.

Every authority is in internal/docs/citation_index.json (Iqbal, Starr, Erickson,
Lee, Khoja, Hill, Sonner, Guzman, Lopez) or is Amazon's own authority cited to
distinguish it (Brahmana, Estate of Hearst, Saleh, In re Yahoo Mail), or is the
Lerma docket order the Complaint already pleads.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import (  # noqa: E402
    CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH, PleadingPaper,
)
from signature_stamp import SIGNATURE_PATH, SIGNATURE_NATIVE_PX  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parent.parent

OUT_PATHS = [
    REPO_ROOT / "internal" / "public" / "documents" / "matter-29"
    / "Opposition to Amazon MTD - Pleading Paper (Sep 23 2026).pdf",
]
ORDER_OUT = (
    REPO_ROOT / "internal" / "public" / "documents" / "matter-29"
    / "Proposed Order - Amazon MTD (Sep 23 2026).pdf"
)
ORDER_SCRATCH_OUT = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "fde9b68e-7f08-5546-b231-a91ce9f193c5/scratchpad/"
    "Proposed-Order-Amazon-MTD-Sep23.pdf"
)
SCRATCH_OUT = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "fde9b68e-7f08-5546-b231-a91ce9f193c5/scratchpad/"
    "Opposition-to-Amazon-MTD-Sep23.pdf"
)

SIGN_OFF_DATE = "September 23, 2026"

DOC_TITLE_FOOTER = (
    "PLAINTIFF'S OPPOSITION TO AMAZON'S MOTION TO DISMISS -- "
    "NEWANFORBI v. AMAZON.COM SERVICES, LLC (N.D. Cal.)"
)
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
SIG_WIDTH = 235
SIG_RIGHT_OFFSET = 28
SIG_HEIGHT_SCALE = 1.25

ATTORNEY_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
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
    ("AMAZON.COM SERVICES, LLC, a", True, False),
    ("Delaware limited liability company;", True, False),
    ("ACCURATE BACKGROUND, LLC, a", True, False),
    ("California limited liability company;", True, False),
    ("and DOES 1-10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
    ("", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 4:26-cv-09249-ASK", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANT AMAZON.COM", True, False),
    ("SERVICES LLC'S MOTION TO", True, False),
    ("DISMISS PLAINTIFF'S FIFTH,", True, False),
    ("SIXTH, AND SEVENTH CLAIMS", True, False),
    ("FOR RELIEF", True, False),
    ("", False, False),
    ("Date: November 18, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: 4, 3rd Floor", False, False),
    ("Judge: Hon. Ajay S. Krishnan", False, False),
]

CASE_ITALICS = sorted(
    [
        "Hill v. National Collegiate Athletic Ass'n",
        "Khoja v. Orexigen Therapeutics, Inc.",
        "Guzman v. Polaris Industries Inc.",
        "Sonner v. Premier Nutrition Corp.",
        "Lerma v. Amazon.com Services, LLC",
        "Lee v. City of Los Angeles",
        "In re Yahoo Mail Litigation",
        "Brahmana v. Henard",
        "Erickson v. Pardus",
        "Ashcroft v. Iqbal",
        "Saleh v. Nike, Inc.",
        "Estate of Hearst",
        "Starr v. Baca",
        "Lopez v. Smith",
        "Yahoo Mail",
        "Brahmana",
        "Erickson",
        "Guzman",
        "Sonner",
        "Khoja",
        "Lerma",
        "Iqbal",
        "Saleh",
        "Starr",
        "Lopez",
        "Hill",
        "Lee",
        "Id.",
        "id.",
    ],
    key=len,
    reverse=True,
)


def italicize_cases(text: str) -> str:
    out = text
    for name in CASE_ITALICS:
        if f"<<i:{name}>>" in out:
            continue
        pattern = re.compile(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])")
        parts = re.split(r"(<<i:[^>]+>>)", out)
        rebuilt = []
        for part in parts:
            if part.startswith("<<i:"):
                rebuilt.append(part)
            else:
                rebuilt.append(pattern.sub(f"<<i:{name}>>", part))
        out = "".join(rebuilt)
    return out


def nb(text: str) -> str:
    """Glue pin cites together with non-breaking spaces."""
    text = re.sub(r"(¶¶?|§) ", "\\1\u00a0", text)
    text = re.sub(r"\b(Compl\.|Mot\.|Id\.|id\.|No\.) (?=[¶\d])", "\\1\u00a0", text)
    return text


# ==========================================================
# BODY CONTENT
# ==========================================================
H, S, P, L = "HEADER", "SUBHEAD", "PARA", "LIST"

CONTENT = [
    (H, "I. STATEMENT OF ISSUES TO BE DECIDED"),
    (P, """Pursuant to Civil Local Rule 7-4(a)(3), the issues presented are:"""),
    (L, """1. Whether the Fifth Claim states a claim under article I, section 1 of the California Constitution where it alleges the use of registry information to deny employment -- the specific use California law prohibits -- rather than the disclosure of secret information."""),
    (L, """2. Whether, if the Court concludes under Sonner v. Premier Nutrition Corp. that it lacks equitable jurisdiction over the Sixth Claim under Business and Professions Code section 17200, the dismissal as against Amazon should be without prejudice."""),
    (L, """3. Whether the unopposed dismissal of the Seventh Claim as against Amazon should be without prejudice."""),
    (L, """4. Whether the motion must be decided on the Complaint alone, without regard to the factual assertions in the motion's first footnote, and without any ruling on Claims One through Four."""),

    (H, "II. INTRODUCTION"),
    (P, """Amazon's motion is limited. Plaintiff pleads seven causes of action, but Amazon moves only against the Fifth Claim for invasion of privacy, the Sixth Claim under California's Unfair Competition Law (UCL), and the Seventh Claim for intentional infliction of emotional distress (IIED). It does not move against the First Claim under Penal Code section 290.46(j)(2)(E), the Second Claim under the California Fair Chance Act, the Third Claim under the Fair Credit Reporting Act (FCRA), or the Fourth Claim under the Investigative Consumer Reporting Agencies Act (ICRAA). The merits of Claims One through Four are therefore not presented for decision. Accurate Background has answered the Complaint and has not joined the motion. ECF No. 21."""),
    (P, """The motion should be denied as to the Fifth Claim. Amazon treats that claim as an assertion that public registry information is secret. Plaintiff alleges something narrower: a protected interest in freedom from the use of registry information to deny employment -- the specific use California expressly prohibits. Indeed, the statutory restriction exists only because the information is public; public availability therefore cannot be the end of the analysis. California's enactment supplies the legal and social norms that inform each element under Hill v. National Collegiate Athletic Ass'n, 7 Cal. 4th 1 (1994)."""),
    (P, """Plaintiff does not oppose dismissal of the Sixth Claim as against Amazon only, provided the dismissal is without prejudice. Plaintiff does not defend lost wages or ordinary employment benefits as UCL restitution. Any dismissal would rest on federal equitable jurisdiction under Sonner v. Premier Nutrition Corp., 971 F.3d 834 (9th Cir. 2020), not on the merits of the statutory predicates Amazon has not challenged. Under Guzman v. Polaris Industries Inc., 49 F.4th 1308 (9th Cir. 2022), such a dismissal should be without prejudice. Plaintiff likewise does not oppose dismissal of the Seventh Claim as against Amazon only, without prejudice, and without adopting Amazon's characterization of that claim."""),
    (P, """Finally, Amazon's footnote about the status of the background report is unsupported attorney argument. The motion must be decided on the Complaint, and it cannot yield a ruling on the four claims Amazon did not challenge."""),

    (H, "III. STATEMENT OF RELEVANT ALLEGATIONS"),
    (P, """On July 3, 2026, Amazon extended Plaintiff a conditional offer for a Seasonal XL Warehouse Associate position at its Fremont fulfillment center, with training fixed for July 28-29 and August 4-5, 2026. Compl. ¶¶ 7-10. The offer e-mail told Plaintiff that if pre-employment requirements were "not completed on time," he would be required to select a new start date, location, or schedule -- and added, "But don't worry if this happens!" Id. ¶ 9."""),
    (P, """Amazon procured a consumer report on Plaintiff through Defendant Accurate Background, which identified itself in writing as "a consumer reporting agency" conducting the screening on behalf of "Amazon Salesforce." Id. ¶¶ 15-16. Moments after Plaintiff completed his July 7 pre-hire appointment, Accurate also asked him to telephone and confirm his Social Security number, prior names, address history, and date of birth, describing the request as "urgent." Id. ¶ 15."""),
    (P, """On July 8, Amazon told Plaintiff that background checks for that site "are usually returned 5 days after they are submitted." Id. ¶ 17. On July 12, Amazon wrote that the application was "still in progress"; on July 17, it apologized for the delay and attributed it to its third-party vendor. Id. ¶¶ 18-19. On July 27 -- twenty days after submission and one day before the fixed training date -- Amazon's onboarding portal still showed the check as "Pending," and Plaintiff's confirmed shift had been replaced with the message "You do not have a shift selected. Please select a new shift." Id. ¶¶ 21-22."""),
    (P, """Plaintiff alleges that the specific, dated position was lost in substance while the application remained labeled pending, and that neither Defendant provided a pre-adverse-action notice, a copy of the report, an adverse-action notice, or an opportunity to respond. Id. ¶¶ 23-25. Plaintiff is a registrant on California's Sex Offender Registry. Id. ¶ 26. He alleges, in the alternative, that registry-derived information entered the screening through Accurate's registry search product, a national sex-offender database drawing on California's registry, the Megan's Law website, or another registry-derived channel. Id. ¶¶ 28, 43. He has demanded but not received the report and therefore cannot yet identify the internal source. Id. ¶ 29."""),

    (H, "IV. LEGAL STANDARD"),
    (P, """A Rule 12(b)(6) motion tests the sufficiency of the pleading, not the merits. A claim survives when the pleaded facts permit a reasonable inference that the defendant is liable. Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009). The Court accepts well-pleaded allegations as true and draws reasonable inferences in Plaintiff's favor. Starr v. Baca, 652 F.3d 1202, 1216-17 (9th Cir. 2011). A self-represented litigant's pleading is construed liberally. Erickson v. Pardus, 551 U.S. 89, 94 (2007). A pro se plaintiff should be granted leave to amend unless the pleading could not possibly be cured by additional facts. Lopez v. Smith, 203 F.3d 1122, 1127, 1130 (9th Cir. 2000) (en banc)."""),

    (H, "V. ARGUMENT"),

    (S, "A. The Motion Must Be Decided on the Complaint, and It Does Not Reach Claims One Through Four."),
    (P, """Review under Rule 12(b)(6) is limited to the Complaint, documents properly incorporated by reference, and matters properly subject to judicial notice. Lee v. City of Los Angeles, 250 F.3d 668, 688-90 (9th Cir. 2001). Even when a document is judicially noticeable, disputed facts within it may not be accepted as true. Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988, 999-1003 (9th Cir. 2018)."""),
    (P, """Amazon submits nothing outside the pleadings -- no background report, no declaration, no status record, and no request for judicial notice. Its first footnote nonetheless asserts that the report remains unfinished because certain California court records are difficult to obtain, and that no adverse action has been taken. Mot. 1 n.1. That is unsupported attorney argument, and it cannot displace the pleaded allegations. Accordingly, the motion must be decided on the Complaint and materials properly considered under Rule 12(b)(6)."""),
    (P, """That posture distinguishes Lerma v. Amazon.com Services, LLC, No. 8:22-cv-01727-FWS-JDE (C.D. Cal. May 26, 2023), which the Complaint describes. Compl. ¶¶ 31-33. As the Complaint alleges, the court in that case resolved the source of the disqualifying information on the background report itself, which was before the court and which showed court-record sourcing and no registry hit. Id. ¶ 32. Here, Amazon has placed no report in the record, and Plaintiff alleges that he has demanded it and not received it. Id. ¶ 29. For purposes of this motion, the Court therefore takes the Complaint's alternative allegations about the source of the registry information as true."""),
    (P, """Accurate's answer does not change that analysis. Accurate admits that Plaintiff's screening remains pending and denies reporting registry information. ECF No. 21 ¶¶ 23, 29-30, 42-44. A co-defendant's pleaded denials are not evidence and cannot resolve Amazon's Rule 12(b)(6) motion; the Complaint's well-pleaded allegations are accepted as true, and neither defendant has placed a background report before the Court."""),
    (P, """Nor does the motion reach Claims One through Four. Amazon moved against only the Fifth, Sixth, and Seventh Claims, and its footnote comments on the remaining claims request no relief. Those claims are not presented for decision, and the order on this motion should not be read to address them."""),

    (S, "B. Plaintiff's Fifth Claim for Invasion of Privacy Is Adequately Pleaded."),
    (P, """A claim for invasion of the California constitutional right of privacy requires a legally protected privacy interest, a reasonable expectation of privacy under the circumstances, and a serious invasion. Hill, 7 Cal. 4th at 35-37; Cal. Const. art. I, § 1. Whether a reasonable expectation exists and whether an invasion is serious are mixed questions of law and fact; they may be decided as a matter of law only where the undisputed facts show no reasonable expectation or an insubstantial impact on privacy interests. Hill, 7 Cal. 4th at 40. Amazon's arguments on each element answer a secrecy claim Plaintiff has not brought."""),

    (S, "1. The asserted interest is freedom from the prohibited use of registry information, not secrecy."),
    (P, """Amazon argues that Plaintiff has no privacy interest in public criminal records or information displayed on a government website. Mot. 5. But the Complaint does not allege that the registry listing is confidential. It alleges an interest in the information "insofar as that information is used for purposes expressly prohibited by Penal Code § 290.46(j)(2)." Compl. ¶ 73. The alleged invasion is the use of registry information to deny employment. Id. ¶¶ 74-75."""),
    (P, """Hill defines informational privacy as the interest in precluding the "dissemination or <<i:misuse>>" of sensitive and confidential information. 7 Cal. 4th at 35 (emphasis added). Plaintiff does not contend that his registry listing is confidential; Amazon is correct that it is publicly accessible. The claim does not depend on confidentiality. It depends on restricted use, context, the scope of consent, and resulting harm -- the considerations that inform whether an expectation of privacy is reasonable and an invasion serious. Id. at 35-37."""),
    (P, """The Legislature has identified the misuse at issue here. Absent a statutory exception, Penal Code section 290.46(j)(2)(E) prohibits the use of registry information disclosed under that section for purposes relating to employment -- including, as alleged here, to deny it -- and section 290.46(j)(4)(A) gives the person harmed a private civil remedy. That enactment bears on whether the asserted interest is legally protected and on the social norms governing the challenged use."""),
    (P, """At minimum, the statutory prohibition and its express civil remedy supply concrete legal and social norms relevant to the contextual Hill inquiry; they foreclose dismissal based solely on the public availability of the underlying information."""),

    (S, "2. Amazon's public-record authorities do not address a statutory use restriction."),
    (P, """Amazon relies on Brahmana v. Henard, 2010 WL 11488727, at *4 (N.D. Cal. Nov. 12, 2010), and Estate of Hearst, 67 Cal. App. 3d 777, 782 (1977). Mot. 5. As Amazon presents them, those decisions establish that court records and information about criminal convictions on a government website are publicly accessible. Plaintiff does not dispute that proposition. Neither decision addresses a statute that restricts a particular use of otherwise-public information, and neither involved a use that the Legislature has made independently actionable."""),
    (P, """The distinction is not a technicality. Section 290.46(j)(2) governs information "disclosed pursuant to this section" -- information that is, by definition, public. The Legislature chose to publish registry information for protective purposes while restricting its use for employment and other enumerated purposes. Public availability is therefore relevant, but it is not necessarily dispositive of the distinct theory pleaded here: that Defendants used registry-derived information for a purpose California expressly prohibits. Section 290.46(j) informs the objective expectations and social norms relevant under Hill, even though the statute does not itself establish every constitutional element."""),

    (S, "3. General authorization for a background check is not consent to the alleged prohibited use."),
    (P, """Amazon next argues that because Plaintiff applied, completed onboarding paperwork, and received an offer conditioned on a background check, he consented to the check and cannot claim a reasonable expectation of privacy. Mot. 5. That argument equates awareness of a background check with consent to every possible source and use. The Complaint does not support that expansion. It alleges that the offer was conditioned on a background check and that Plaintiff later opted into text-message communications from Accurate. Compl. ¶¶ 8, 20. It does not allege that Plaintiff authorized Defendants to use registry information to deny employment in violation of section 290.46(j)(2)(E)."""),
    (P, """Saleh v. Nike, Inc., 562 F. Supp. 3d 503, 524 (C.D. Cal. 2021), on which Amazon relies, recites the general principle that a plaintiff cannot claim a reasonable expectation of privacy in an intrusion to which he consented. It does not hold that consent to one activity extends to a different use, and still less to a use that state law forbids. Amazon cites no authority holding that authorization for a lawful employment screening constitutes consent to a prohibited use of the results. Under Hill, the reasonableness of an expectation of privacy is an objective question informed by widely accepted community norms and the circumstances, including the opportunity to consent. 7 Cal. 4th at 36-37. Here the governing norm is codified, and the scope of the consent alleged is narrower than the use alleged. At the pleading stage, the Court should not enlarge that consent in Amazon's favor."""),

    (S, "4. The Complaint plausibly alleges a serious invasion, and the balancing Amazon seeks is premature."),
    (P, """Seriousness is evaluated through the invasion's nature, scope, and actual or potential impact. Hill, 7 Cal. 4th at 37. Plaintiff alleges more than abstract access to a public listing. He alleges the use of registry information for the precise employment purpose California forbids, resulting in the loss of a specific, dated job without the required notices or any opportunity to respond. Compl. ¶¶ 22-25, 75-76. A use the Legislature has singled out for prohibition and made privately actionable is, at a minimum, plausibly an egregious breach of the social norms underlying the privacy right."""),
    (P, """Amazon's reliance on the "high bar" language of In re Yahoo Mail Litigation, 7 F. Supp. 3d 1016, 1038 (N.D. Cal. 2014), does not change the analysis. Privacy claims can be dismissed at the pleading stage, but dismissal is unwarranted where, as here, the pleaded circumstances plausibly support seriousness and the relevant context remains fact-dependent. See Hill, 7 Cal. 4th at 40. Any asserted countervailing interest likewise requires a fact-specific justification analysis. Id. On the pleaded allegations, Amazon identifies no basis to resolve that analysis against Plaintiff at the Rule 12 stage, and the Complaint alleges a use the Legislature has already labeled wrongful. Seriousness is at least plausible."""),
    (P, """The same alleged conduct underlies the First Claim under section 290.46(j)(2)(E). Amazon's decision not to move against that claim is not a concession that a violation occurred, but it places the statutory merits outside this motion. The question here is narrower: assuming the pleaded prohibited use, do the allegations satisfy Hill? At the Rule 12 stage, they plausibly do."""),

    (S, "5. Alternative allegations about the source of the registry information are permitted."),
    (P, """Rule 8 permits a party to set out alternative statements of a claim and to plead in the alternative regardless of consistency. Fed. R. Civ. P. 8(d)(2)-(3). The Complaint alleges alternative channels through which registry-derived information entered the screening because the report that would identify the channel is in Defendants' possession and has been demanded but not produced. Compl. ¶¶ 28-29, 43, 75. Amazon's privacy argument does not contend otherwise. It assumes the information came from the public registry and argues only public availability and consent. Plaintiff's inability to identify the internal source before discovery is not a pleading defect."""),

    (S, "6. Any dismissal of the Fifth Claim should be without prejudice and limited to the constitutional claim."),
    (P, """If the Court nonetheless concludes that the constitutional claim is deficient, the dismissal should be without prejudice and with leave to amend. Lopez, 203 F.3d at 1127, 1130. It should also be limited to the constitutional claim. Amazon did not move against the First Claim, and a ruling on the Hill elements would not determine whether registry information was used in violation of section 290.46(j)(2)(E) or whether section 290.46(j)(4)(A) affords relief."""),

    (S, "C. If the Court Dismisses the Sixth Claim Against Amazon, the Dismissal Should Be Without Prejudice."),
    (P, """Amazon argues that the UCL claim must be dismissed because the UCL affords only equitable relief and the Complaint does not allege that Plaintiff lacks an adequate legal remedy. Mot. 3-4. Plaintiff does not oppose dismissal of the Sixth Claim against Amazon on the presently pleaded equitable-relief theory, provided that dismissal is without prejudice and does not adjudicate the underlying statutory predicates. Plaintiff also clarifies that he does not defend lost wages or ordinary employment benefits as UCL restitution; those sums are sought, if recoverable, as legal damages under other claims."""),
    (P, """A Sonner disposition does not adjudicate the UCL predicates. The UCL count borrows the alleged section 290.46, FCRA, and ICRAA violations, Compl. ¶ 79, and Amazon has not moved against those claims."""),
    (P, """Under Guzman, if the Court concludes that equitable jurisdiction is absent, dismissal should be without prejudice rather than an adjudication of the UCL claim's substantive predicates. 49 F.4th at 1313-15. Plaintiff asks only that the order say so: a dismissal without prejudice, without adjudicating the UCL claim's substantive merits."""),
    (P, """Alternatively, if the Court permits amendment, Plaintiff can plead the continuing status of the screening and application, the prospective harms that damages cannot prevent, the precise injunction sought, and why monetary relief cannot supply that relief. Sonner addressed equitable restitution for past harm. 971 F.3d at 844. The Complaint alleges that the screening remains in "Pending" status, Compl. ¶ 23 -- a point Amazon's motion does not dispute, see Mot. 1 n.1, and that Accurate's answer admits, ECF No. 21 ¶ 23. Plaintiff therefore requests either dismissal without prejudice under Guzman or leave to amend under Rule 15(a)(2)."""),

    (S, "D. Plaintiff Does Not Oppose Dismissal of the Seventh Claim as Against Amazon Only and Without Prejudice."),
    (P, """Plaintiff does not oppose dismissal of the IIED claim as against Amazon only. That limited non-opposition does not adopt Amazon's reduction of the alleged course of conduct to a routine twenty-day delay. The Complaint also alleges removal of a confirmed shift one day before training, withholding of the report and required notices, prohibited use of registry information, and resulting distress. Compl. ¶¶ 22-25, 84-87."""),
    (P, """Plaintiff requests that the dismissal be without prejudice to later seeking leave under Rule 15 if the report, Amazon's decision record, or discovery supplies facts concerning Amazon's knowledge, the reason for the employment outcome, and the severity of the distress."""),

    (S, "E. Leave to Amend Should Be Granted as to Any Claim Dismissed."),
    (P, """Leave to amend should be freely given, Fed. R. Civ. P. 15(a)(2); Lopez, 203 F.3d at 1127, 1130, and amendment would not be futile. Without contradicting the Complaint, Plaintiff can allege the terms and scope of the background-check authorization he actually gave and the facts connecting the alleged employment use to the statutory prohibition, as the report and decision record are obtained through 15 U.S.C. § 1681g, Civil Code section 1786.10, or discovery. Compl. ¶¶ 29, 45. The amendments available for the Sixth and Seventh Claims are set out in Sections V.C and V.D."""),

    (H, "VI. CONCLUSION"),
    (P, """Plaintiff respectfully requests that the Court: (1) deny Amazon's motion as to the Fifth Claim or, alternatively, dismiss that claim without prejudice, with leave to amend, and without any determination concerning the First Claim; (2) dismiss the Sixth Claim as against Amazon only and without prejudice under Guzman, or alternatively grant leave to amend; and (3) dismiss the Seventh Claim as against Amazon only and without prejudice to later seeking leave to amend. Claims One through Four, and all claims against Accurate, are not before the Court on this motion."""),
]

# ==========================================================
# TABLE OF AUTHORITIES: (category, label, search regex)
# Pages are found by searching the rendered body pages, so the TOA always
# matches the final pagination.
# ==========================================================
AUTHORITIES = [
    ("Cases", "Ashcroft v. Iqbal, 556 U.S. 662 (2009)", r"\bIqbal\b"),
    ("Cases", "Brahmana v. Henard, 2010 WL 11488727 (N.D. Cal. Nov. 12, 2010)", r"Brahmana"),
    ("Cases", "Erickson v. Pardus, 551 U.S. 89 (2007)", r"Erickson"),
    ("Cases", "Estate of Hearst, 67 Cal. App. 3d 777 (1977)", r"Hearst"),
    ("Cases", "Guzman v. Polaris Industries Inc., 49 F.4th 1308 (9th Cir. 2022)", r"Guzman"),
    ("Cases", "Hill v. National Collegiate Athletic Ass'n, 7 Cal. 4th 1 (1994)", r"\bHill\b"),
    ("Cases", "In re Yahoo Mail Litigation, 7 F. Supp. 3d 1016 (N.D. Cal. 2014)", r"Yahoo"),
    ("Cases", "Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988 (9th Cir. 2018)", r"Khoja"),
    ("Cases", "Lee v. City of Los Angeles, 250 F.3d 668 (9th Cir. 2001)", r"Lee v\. City"),
    ("Cases", "Lerma v. Amazon.com Services, LLC, No. 8:22-cv-01727-FWS-JDE (C.D. Cal. May 26, 2023)", r"\bLerma\b"),
    ("Cases", "Lopez v. Smith, 203 F.3d 1122 (9th Cir. 2000) (en banc)", r"\bLopez\b"),
    ("Cases", "Saleh v. Nike, Inc., 562 F. Supp. 3d 503 (C.D. Cal. 2021)", r"\bSaleh\b"),
    ("Cases", "Sonner v. Premier Nutrition Corp., 971 F.3d 834 (9th Cir. 2020)", r"\bSonner\b"),
    ("Cases", "Starr v. Baca, 652 F.3d 1202 (9th Cir. 2011)", r"\bStarr\b"),
    ("Constitutional Provisions", "Cal. Const. art. I, § 1", r"art(icle|\.) I, (section|§) 1"),
    ("Statutes", "15 U.S.C. § 1681g", r"1681g"),
    ("Statutes", "Cal. Bus. & Prof. Code § 17200", r"17200"),
    ("Statutes", "Cal. Civ. Code § 1786.10", r"1786\.10"),
    ("Statutes", "Cal. Penal Code § 290.46(j)(2)", r"290\.46\(j\)\(2\)|section 290\.46,"),
    ("Statutes", "Cal. Penal Code § 290.46(j)(4)(A)", r"290\.46\(j\)\(4\)\(A\)"),
    ("Rules", "Fed. R. Civ. P. 8(d)(2)-(3)", r"8\(d\)"),
    ("Rules", "Fed. R. Civ. P. 12(b)(6)", r"12\(b\)\(6\)"),
    ("Rules", "Fed. R. Civ. P. 15(a)(2)", r"15\(a\)\(2\)|Rule 15\b"),
    ("Rules", "Civil L.R. 7-4(a)(3)", r"7-4\(a\)\(3\)"),
]
TOA_CATEGORIES = ["Cases", "Constitutional Provisions", "Statutes", "Rules"]



def signature_lines(date: str) -> list[str]:
    return [
        f"Dated: {date}",
        "Respectfully submitted,",
        "___________________________________",
        "BRENDAN NGEHSI NEWANFORBI",
        "Plaintiff, In Pro Per",
    ]


def draw_signature(d, lines: list[str]) -> None:
    """Keep the whole block on one page. draw_signature_image inserts 2 lines of
    air and itself demands 6 free lines at the underscore, so reserve for that.
    A leading "Dated:" line shares its line with "Respectfully submitted,"."""
    if len(lines) >= 2 and lines[0].startswith("Dated:") and lines[1] == "Respectfully submitted,":
        dated, lines = lines[0], lines[1:]
    else:
        dated = None
    idx = next(i for i, ln in enumerate(lines) if ln.startswith("_"))
    d.ensure_space(idx + max(6, 2 + len(lines) - idx))
    if dated:
        d._ensure_line()
        d.c.setFont("Times-Roman", 12)
        d.c.drawString(CONTENT_LEFT, d._line_y(d.current_line), dated)
    for line in lines:
        if line.startswith("_") and os.path.isfile(SIGNATURE_PATH):
            d.draw_signature_image(
                SIGNATURE_PATH, SIG_IMG_W_PX, SIG_IMG_H_PX, line,
                width=SIG_WIDTH, right_margin_offset=SIG_RIGHT_OFFSET,
                height_scale=SIG_HEIGHT_SCALE,
            )
        d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)


def toc_level(ctype: str, text: str):
    if ctype == H:
        return 0
    if ctype == S and re.match(r"^[A-H]\.\s", text):
        return 1
    if ctype == S and re.match(r"^\d\.\s", text):
        return 2
    return None


def toc_row(d, label: str, page_str: str, bold: bool = False, indent: float = 0,
            num_reserve: float = 64) -> None:
    c = d.c
    fn = "Times-Bold" if bold else "Times-Roman"
    size = 12
    left_x = CONTENT_LEFT + indent
    right_x = CONTENT_RIGHT - 8
    avail = CONTENT_WIDTH - indent - num_reserve - 6
    words = label.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, fn, size) > avail and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        d._ensure_line()
        y = d._line_y(d.current_line)
        c.setFont(fn, size)
        c.drawString(left_x + (0 if i == 0 else 12), y, ln)
        if i == len(lines) - 1:
            c.setFont("Times-Roman", size)
            c.drawRightString(right_x, y, page_str)
            label_end = left_x + (0 if i == 0 else 12) + c.stringWidth(ln, fn, size) + 4
            num_w = c.stringWidth(page_str, "Times-Roman", size)
            leader_end = right_x - num_w - 4
            if leader_end > label_end:
                dw = c.stringWidth(". ", "Times-Roman", size)
                ndots = max(0, int((leader_end - label_end) / dw))
                c.drawString(label_end, y, ". " * ndots)
        d.current_line += 1


def render(out_path: Path, toc_pages: dict, toa_pages: dict, meta: dict) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out_path), doc_title_footer=DOC_TITLE_FOOTER)
    c = d.c

    # --- Caption page ---
    atty_y = d._line_y(0)
    for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
        c.setFont(font, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, text)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)

    # --- Table of Contents (own page) ---
    d.start_new_page()
    d.write_line("TABLE OF CONTENTS", bold=True, center=True)
    d.blank_line()
    for ctype, text in CONTENT:
        lvl = toc_level(ctype, text)
        if lvl is None:
            continue
        toc_row(d, text, str(toc_pages.get(text, "0")), bold=(lvl == 0), indent=[0, 18, 36][lvl])

    # --- Table of Authorities (own page) ---
    d.start_new_page()
    d.write_line("TABLE OF AUTHORITIES", bold=True, center=True)
    d.blank_line()
    for cat in TOA_CATEGORIES:
        d.ensure_space(3)
        d.write_line(cat, bold=True)
        for acat, label, _ in AUTHORITIES:
            if acat == cat:
                toc_row(d, label, toa_pages.get(label, "0"), indent=18)
        d.blank_line()

    # --- Body ---
    d.start_new_page()
    meta["body_start"] = d.page_num
    for c_type, text in CONTENT:
        if c_type == H:
            # Keep the Conclusion on the same page as the signature block.
            d.ensure_space(18 if text.endswith("CONCLUSION") else 4)
            toc_pages_capture = meta.setdefault("toc", {})
            toc_pages_capture[text] = d.page_num
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == S:
            d.ensure_space(6)
            meta.setdefault("toc", {})[text] = d.page_num
            d.write_wrapped(f"<<b:{text}>>", first_indent=0)
            d.blank_line()
        elif c_type == P:
            d.write_wrapped(italicize_cases(nb(text)), first_indent=36)
            d.blank_line()
        elif c_type == L:
            d.write_wrapped(italicize_cases(nb(text)), indent=36, first_indent=0)
            d.blank_line()
    draw_signature(d, signature_lines(SIGN_OFF_DATE))
    meta["body_end"] = d.page_num

    d.save()
    meta["pages"] = d.page_num


ORDER_CAPTION_RIGHT = [
    ("Case No. 4:26-cv-09249-ASK", False, False),
    ("", False, False),
    ("[PROPOSED] ORDER ON", True, False),
    ("DEFENDANT AMAZON.COM", True, False),
    ("SERVICES LLC'S MOTION TO", True, False),
    ("DISMISS PLAINTIFF'S FIFTH,", True, False),
    ("SIXTH, AND SEVENTH CLAIMS", True, False),
    ("FOR RELIEF (DKT. 19)", True, False),
    ("", False, False),
    ("Judge: Hon. Ajay S. Krishnan", False, False),
]

ORDER_PARAS = [
    """Having considered Defendant Amazon.com Services LLC's Motion to Dismiss Plaintiff's Fifth, Sixth, and Seventh Claims for Relief (Dkt. 19), the papers filed in support of and in opposition to the motion, and the record, the Court ORDERS as follows:""",
    """1.  The motion is DENIED as to the Fifth Claim for invasion of privacy under article I, section 1 of the California Constitution.""",
    """2.  The motion is GRANTED as to the Sixth Claim under Business and Professions Code section 17200, as against Amazon only. The Sixth Claim is DISMISSED as against Amazon WITHOUT PREJUDICE. This dismissal rests on the absence of federal equitable jurisdiction and does not adjudicate the merits of the claim or of its statutory predicates.""",
    """3.  The motion is GRANTED as to the Seventh Claim for intentional infliction of emotional distress, as against Amazon only. The Seventh Claim is DISMISSED as against Amazon WITHOUT PREJUDICE to Plaintiff later seeking leave to amend.""",
    """4.  This Order does not address or adjudicate Plaintiff's First, Second, Third, or Fourth Claims for Relief, and it does not dismiss any claim against Defendant Accurate Background, LLC.""",
    """5.  Amazon shall answer the Complaint's remaining claims against it within fourteen (14) days after entry of this Order. Fed. R. Civ. P. 12(a)(4)(A).""",
]


def render_proposed_order(out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(
        str(out_path),
        doc_title_footer="[PROPOSED] ORDER ON AMAZON'S MOTION TO DISMISS -- "
                         "NEWANFORBI v. AMAZON.COM SERVICES, LLC (N.D. Cal.)",
    )
    c = d.c
    atty_y = d._line_y(0)
    for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
        c.setFont(font, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, text)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, ORDER_CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_line("[PROPOSED] ORDER", bold=True, center=True)
    d.blank_line()
    for i, para in enumerate(ORDER_PARAS):
        d.write_wrapped(nb(para), first_indent=36 if i == 0 else 0)
        d.blank_line()
    d.ensure_space(9)
    d.write_line("IT IS SO ORDERED.", bold=True)
    d.blank_line()
    d.write_line("Dated: ________________")
    d.blank_line()
    d.blank_line()
    d.write_line("________________________________________", right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    d.write_line("HON. AJAY S. KRISHNAN", right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    d.write_line("United States Magistrate Judge", right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    d.save()
    return d.page_num


def find_toa_pages(pdf_path: Path, body_start: int, body_end: int) -> dict:
    import pymupdf
    doc = pymupdf.open(str(pdf_path))
    texts = {}
    for i in range(body_start - 1, body_end):
        t = doc[i].get_text()
        t = re.sub(r"(?m)^\s*\d{1,2}\s*$", " ", t)   # pleading line numbers
        texts[i + 1] = re.sub(r"\s+", " ", t)
    out = {}
    for _, label, rx in AUTHORITIES:
        pages = [p for p, t in texts.items() if re.search(rx, t)]
        out[label] = "passim" if len(pages) >= 5 else (", ".join(map(str, pages)) or "MISSING")
    return out


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing canonical signature: {SIGNATURE_PATH}")
    SCRATCH_OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = SCRATCH_OUT.parent / "_m29_opp_pass.pdf"
    toc, toa = {}, {}
    for _ in range(4):   # iterate until pagination is stable
        meta: dict = {}
        render(tmp, toc, toa, meta)
        new_toc = meta["toc"]
        new_toa = find_toa_pages(tmp, meta["body_start"], meta["body_end"])
        if new_toc == toc and new_toa == toa:
            break
        toc, toa = new_toc, new_toa
    missing = [k for k, v in toa.items() if v == "MISSING"]
    if missing:
        raise SystemExit(f"TOA entries not found in body: {missing}")
    for out in list(OUT_PATHS) + [SCRATCH_OUT]:
        meta = {}
        render(out, toc, toa, meta)
        print(f"Wrote {out} ({meta['pages']} pages; body pp. {meta['body_start']}-{meta['body_end']})")
    for out in (ORDER_OUT, ORDER_SCRATCH_OUT):
        n = render_proposed_order(out)
        print(f"Wrote {out} ({n} pages)")
    try:
        tmp.unlink()
    except OSError:
        pass


if __name__ == "__main__":
    main()
