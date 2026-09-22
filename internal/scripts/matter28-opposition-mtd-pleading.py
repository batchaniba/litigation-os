# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 28 -- Plaintiff's Opposition to Smith / HOPE Motion to Dismiss
on portfolio pleading paper, with the universal signature affixed.

  python3 internal/scripts/matter28-opposition-mtd-pleading.py

Renders the opposition body onto lib/pleading_paper.PleadingPaper and stamps
internal/assets/signature/brendan-newanforbi-signature.png over the sign-off.

Two docket-hygiene edits applied against the reviewed draft:
  1. Due-process section D: Greenholtz swapped for Neal v. Shimoda as the
     liberty-interest anchor; Greenholtz kept only to distinguish it.
  2. State-action section B: one sentence added on the 1502-DR's other
     supervision factors (they do not defeat joint action or make amendment
     futile).
Sign-off date set to September 21, 2026.
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
    REPO_ROOT / "internal" / "public" / "documents" / "matter-28"
    / "Opposition to MTD - Pleading Paper (Sep 21 2026).pdf",
]
SCRATCH_OUT = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "3fd8a963-2d26-598c-823f-b47c1b152f34/scratchpad/"
    "Opposition-to-MTD-Pleading-Paper-Sep21.pdf"
)

DOC_TITLE_FOOTER = (
    "PLAINTIFF'S OPPOSITION TO MOTION TO DISMISS -- NEWANFORBI v. SMITH (N.D. Cal.)"
)
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
SIG_WIDTH = 235          # enlarged sign-off stamp
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
    ("SHANNON SMITH, LCSW, Chief", True, False),
    ("Executive Officer and Founder of", True, False),
    ("HOPE Program, an individual; and", True, False),
    ("HOPE PSYCHOTHERAPY, INC.,", True, False),
    ("d/b/a HOPE PROGRAM, a California", True, False),
    ("corporation,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
    ("", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 3:26-cv-07504-LJC", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANTS' MOTION TO", True, False),
    ("DISMISS", True, False),
    ("", False, False),
    ("Date: October 20, 2026", False, False),
    ("Time: 10:30 a.m.", False, False),
    ("Courtroom: G, 15th Floor", False, False),
    ("Judge: Hon. Lisa J. Cisneros", False, False),
]

# Longest-first so full names beat short forms; short forms are distinctive.
CASE_ITALICS = sorted(
    [
        "Arizona Students' Association v. Arizona Board of Regents",
        "Boeken v. Philip Morris USA, Inc.",
        "Caviness v. Horizon Community Learning Center, Inc.",
        "Cedric Kushner Promotions, Ltd. v. King",
        "DKN Holdings LLC v. Faerber",
        "Drawsand v. F.F. Properties, L.L.P.",
        "Florer v. Congregation Pidyon Shevuyim, N.A.",
        "Goddard v. Security Title Insurance & Guarantee Co.",
        "Greenholtz v. Inmates of Nebraska Penal & Correctional Complex",
        "Schreiber Distributing Co. v. Serv-Well Furniture Co.",
        "Perez v. City of San Bruno",
        "Rawson v. Recovery Innovations, Inc.",
        "Valvo v. University of Southern California",
        "Khoja v. Orexigen Therapeutics, Inc.",
        "Berri v. Superior Court",
        "Kearns v. Ford Motor Co.",
        "Logan v. Zimmerman Brush Co.",
        "Ashcroft v. Iqbal",
        "Hishon v. King & Spalding",
        "Erickson v. Pardus",
        "Franklin v. Fox",
        "Heath v. Cleary",
        "Lopez v. Smith",
        "Neal v. Shimoda",
        "Patsy v. Board of Regents",
        "Scott v. Kuhlmann",
        "West v. Atkins",
        "Zinermon v. Burch",
        "In re Dwyer",
        "DKN Holdings",
        "Cedric Kushner",
        "Arizona Students' Association",
        "Greenholtz",
        "Caviness",
        "Drawsand",
        "Schreiber",
        "Rawson",
        "Franklin",
        "Florer",
        "Zinermon",
        "Goddard",
        "Boeken",
        "Erickson",
        "Kearns",
        "Patsy",
        "Valvo",
        "Berri",
        "Khoja",
        "Scott",
        "Lopez",
        "Perez",
        "Iqbal",
        "Logan",
        "Neal",
        "West",
        "Dwyer",
    ],
    key=len,
    reverse=True,
)


def italicize_cases(text: str) -> str:
    out = text
    for name in CASE_ITALICS:
        if f"<<i:{name}>>" in out:
            continue
        # word-boundary match so short forms don't hit inside other words
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


# ==========================================================
# BODY CONTENT  (I. ISSUES PRESENTED -> VI. CONCLUSION)
# ==========================================================
H, S, P, L = "HEADER", "SUBHEAD", "PARA", "LIST"

CONTENT = [
    (H, "I. ISSUES PRESENTED"),
    (P, "1. Whether claim preclusion can be decided on a Rule 12(b)(6) motion when Defendants' own judicially noticed packet contains only an order sustaining a demurrer--not a judgment of dismissal--and therefore does not establish a final judgment."),
    (P, "2. Whether the Complaint plausibly alleges state action where a contracted treatment provider and parole officials jointly generated, signed, transmitted, and relied on treatment-retention records that governed Plaintiff's mandatory treatment and continued parole supervision."),
    (P, "3. Whether the Complaint's remaining allegations state plausible First Amendment, due-process, Bane Act, fraud, and RICO claims, or at minimum identify defects that can be cured by amendment."),

    (H, "II. INTRODUCTION"),
    (P, "Defendants' threshold defense fails on the record they selected. Their Exhibit C is a four-page order sustaining a demurrer without leave to amend. It is not a judgment of dismissal. The document was drafted and lodged by the state-court defendants on May 22, 2026; its caption originally read \"[PROPOSED] ORDER,\" with \"PROPOSED\" later crossed out by hand; and its footer still reads \"[PROPOSED] ORDER ON DEFENDANTS KATIE PALACIOS AND HOPE PROGRAM'S DEMURRER.\" Judge George J. Abdallah, Jr. signed it, and it was filed July 15, 2026. But it neither dismisses the action nor enters judgment. Under California law, an order sustaining a demurrer is not itself a final judgment and does not acquire claim-preclusive effect before judgment is entered."),
    (P, "The order also does not adopt any one of the four grounds Defendants presented in their demurrer. It says only that the first amended complaint \"fails to allege facts sufficient to state any cause of action.\" It contains no finding on causation, exhaustion, habeas, or any other disputed issue. Thus, Defendants' exhibits establish neither the final-judgment element of claim preclusion nor the actual-and-necessary decision required for issue preclusion."),
    (P, "Defendants' separate nonparty theory reaches only Shannon Smith. Smith was not named in the state action, and Defendants have not established privity as a matter of law. Their authorities involve employees or agents sued for the same conduct previously litigated against their employer. The federal Complaint, by contrast, alleges Smith's own post-policy conduct as HOPE's chief executive and sole policy authority: personally approving and maintaining a statewide retention policy, issuing a later manual that continued it, and failing to correct it despite notice. ECF No. 1 ¶¶ 12, 42-44, 54-55. At minimum, whether those personal acts were represented in the state action is a factual question that cannot be resolved against Plaintiff on the pleadings."),
    (P, "On the merits, Defendants reduce the Complaint to a private vendor's independent treatment decision. That is not what is pleaded. The Complaint alleges that HOPE is integrated into California's parole-supervision machinery; that HOPE and parole personnel jointly create and sign the Form 3043 retention determination; that a parole agent directed HOPE to record Plaintiff as a \"no show\" despite acknowledging a technological error; and that CDCR expressly relied on HOPE's treatment report when denying discharge. Id. ¶¶ 18-19, 31-37. Those allegations plausibly satisfy the joint-action and close-nexus tests. They also make this case the opposite of Defendants' cases, where the State had no involvement in the specific challenged decision."),
    (P, "The motion should be denied. If the Court finds any count insufficiently particular, the cure is an amended pleading--not dismissal with prejudice."),

    (H, "III. RELEVANT ALLEGATIONS AND PROCEDURAL RECORD"),
    (P, "California requires covered parolees to participate in a sex-offender management program. The treatment period runs from at least one year through the remaining parole term and is determined by the certified treatment professional \"in consultation with the parole officer and as approved by the court.\" Cal. Penal Code § 3008(d)(2). The implementing regulation requires good cause for retention and a written Form 3043 signed by both the treatment provider and parole agent. 15 Cal. Code Regs. § 3574(f)(1)."),
    (P, "The Complaint alleges that HOPE contracts with CDCR to perform this mandatory treatment function and was the sole CASOMB-certified provider serving the Stockton region during the relevant period. ECF No. 1 ¶¶ 13, 17-19. It alleges a corporate policy under which no parolee could be deemed to have completed treatment before discharge from parole, regardless of individualized progress. Id. ¶¶ 1-4, 20-25. Smith, HOPE's chief executive and founder, allegedly had exclusive authority to modify company policy and personally approved, implemented, and maintained that policy. Id. ¶¶ 12, 42-44."),
    (P, "The challenged conduct is concrete. HOPE allegedly supplied CDCR with Form 3043 treatment-status content stating that Plaintiff only partially completed homework and had not completed treatment. Id. ¶¶ 31-33. On March 31, 2026, a parole agent allegedly acknowledged a \"technological error\" yet instructed HOPE to \"mark him as a no show.\" Id. ¶ 34. CDCR's November 2025 discharge-review report then expressly cited HOPE's progress assessment and recommendation for continued treatment before concluding \"Discharge Denied/No Action.\" Id. ¶¶ 35-37. Plaintiff alleges that continued GPS monitoring, curfew restrictions, mandatory attendance, and lost commercial-driving work followed. Id. ¶¶ 37, 48-52."),
    (P, "Plaintiff previously sued HOPE Psychotherapy, Inc. and Katie Palacios in San Joaquin County Superior Court, Case No. STK-CV-UF-2026-0001032. Defendants' present request for judicial notice repeatedly identifies the year as \"2006,\" but the state-court order confirms \"2026.\" On July 15, 2026, Judge Abdallah filed the order sustaining the demurrer without leave to amend. RJN Ex. C. The packet contains no judgment of dismissal. The proof of service attached to Exhibit C is dated May 22, 2026 and concerns the proposed order as lodged; it is not proof of service of the entered July 15 order."),

    (H, "IV. LEGAL STANDARD AND THE PROPER SCOPE OF JUDICIAL NOTICE"),
    (P, "A Rule 12(b)(6) motion tests the legal sufficiency of the complaint. The Court accepts well-pleaded factual allegations as true and draws reasonable inferences in Plaintiff's favor. Hishon v. King & Spalding, 467 U.S. 69, 73 (1984); Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009). A self-represented pleading is liberally construed, and leave to amend must be granted unless it is absolutely clear the defects cannot be cured. Erickson v. Pardus, 551 U.S. 89, 94 (2007); Lopez v. Smith, 203 F.3d 1122, 1130-31 (9th Cir. 2000) (en banc); see Fed. R. Civ. P. 15(a)(2) (leave to amend shall be freely given when justice so requires)."),
    (P, "Preclusion is an affirmative defense that ordinarily is not raised by motion; it may support dismissal at the pleading stage only where its elements are established by the complaint and judicially noticeable materials with no disputed issue of material fact. Scott v. Kuhlmann, 746 F.2d 1377, 1378 (9th Cir. 1984) (per curiam). Plaintiff does not oppose notice of the existence, filing dates, and legal effect of the state-court filings. He opposes treating allegations and arguments in those papers as true, or treating grounds argued in a demurrer memorandum as findings made by the court. See Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988, 999 (9th Cir. 2018)."),
    (P, "The Court should therefore notice what Exhibit C actually does--and what it does not do. It sustains a demurrer; it does not dismiss the action, enter judgment, identify the ground adopted, or make a merits finding. Defendants may not transform their own advocacy in Exhibit B into findings absent from Exhibit C."),

    (H, "V. ARGUMENT"),
    (S, "A. Defendants Have Not Established Claim or Issue Preclusion."),
    (P, "California claim preclusion requires \"(1) the same cause of action (2) between the same parties or parties in privity with them (3) after a final judgment on the merits in the first suit.\" DKN Holdings LLC v. Faerber, 61 Cal. 4th 813, 824 (2015); see Boeken v. Philip Morris USA, Inc., 48 Cal. 4th 788, 797 (2010). The absence of a final judgment defeats claim preclusion as to both Defendants. The separate absence of party identity or established privity independently defeats the defense as to Smith. And because the order identifies no ground actually decided, it cannot establish issue preclusion."),
    (S, "1. Exhibit C is not a final judgment and therefore cannot preclude either Defendant."),
    (P, "Defendants attach no judgment. Exhibit C is titled as an order, directs that a demurrer be sustained without leave to amend, and contains no dismissal language. That distinction is dispositive. California requires a dismissal to be entered in writing as a judgment. Cal. Code Civ. Proc. § 581d. \"Until entry of judgment, a ruling on a demurrer is not res judicata and may be reconsidered and changed by the trial court.\" Valvo v. University of Southern California, 67 Cal. App. 3d 887, 892 n.3 (1977). Consistently, an order sustaining a demurrer without leave to amend is not appealable because it is not the final judgment. Berri v. Superior Court, 43 Cal. 2d 856, 860 (1955)."),
    (P, "The unusual form of Exhibit C reinforces rather than changes that result. \"PROPOSED\" was crossed out in the caption when the judge signed it, but each page still bears the proposed-order footer. The document also bears \"FILE BY FAX.\" Those features may show that the lodged proposal became an entered order; they do not convert the order into a judgment of dismissal. Nor does the May 22 proof of service establish service--or even existence--of a later judgment. On the materials Defendants presented, the state action never reached the final disposition required for claim preclusion."),
    (P, "This defect applies to both HOPE and Smith. Plaintiff does not argue that every demurrer ruling is forever incapable of preclusive effect. He argues the narrower point established by Defendants' packet: no ensuing judgment is before this Court."),
    (S, "2. The generic order establishes no issue that was actually and necessarily decided."),
    (P, "Issue preclusion requires a determination of the identical issue that was actually litigated, necessarily decided, final, and asserted against a party or privy. DKN Holdings, 61 Cal. 4th at 825. Exhibit C cannot satisfy those requirements. Defendants urged four grounds: causation, failure to exhaust, habeas as the asserted vehicle, and failure to state a claim. The order adopts none of them. It states only that the first amended complaint \"fails to allege facts sufficient to state any cause of action.\" It contains no finding about the truth of Plaintiff's allegations, Smith's conduct, the blanket policy, state action, or any federal element."),
    (P, "Goddard v. Security Title Insurance & Guarantee Co., 14 Cal. 2d 47 (1939), does not supply the missing finding. Goddard explains that the effect of a judgment following a general demurrer depends on the defect adjudicated: a judgment may reach the merits where the pleading establishes an absolute bar, but not where the defect is formal or curable by a different pleading. Id. at 52-53. Here, there is no judgment and no identified basis from which this Court could determine what issue, if any, the state court necessarily resolved."),
    (P, "Nor may Defendants select exhaustion from their own demurrer brief after the fact. If the state ruling rested on prematurity or a failure to satisfy a precondition, that would not adjudicate the underlying merits. Perez v. City of San Bruno, 27 Cal. 3d 875, 882-83 (1980). And state administrative exhaustion is not a prerequisite to a § 1983 action. Patsy v. Board of Regents, 457 U.S. 496, 516 (1982); see also Heath v. Cleary, 708 F.2d 1376, 1380 & n.4 (9th Cir. 1983) (a prior state disposition based on nonexhaustion did not decide the unadjudicated substantive federal claims). Those authorities are an alternative response if Defendants contend the state court adopted exhaustion--not an invitation to infer a ground the order does not state."),
    (P, "Defendants' \"could have been litigated\" argument does not cure the threshold problem. New legal labels generally do not avoid California claim preclusion where the same primary right was reduced to a final judgment. But without a final judgment, there is no claim preclusion to extend."),
    (S, "3. Defendants have not established that Smith is in privity with a state-court party for the conduct alleged here."),
    (P, "Smith was not a party to the state case. Defendants therefore must establish privity, which under California law requires more than a relationship label. It requires an identity or community of interest, adequate representation of the nonparty's interest in the first action, and circumstances making it fair to bind the nonparty. DKN Holdings, 61 Cal. 4th at 826. The California Supreme Court has cautioned that jointly liable actors are not automatically privies merely because a plaintiff previously sued one of them. Id. at 824-26."),
    (P, "Neither of Defendants' principal authorities establishes privity on these pleadings. In Scott, the prior and later defendants were federal employees who all participated in the same challenged agency inquiry; the Ninth Circuit described privity among officers of the same government with respect to the same issue. 746 F.2d at 1378. Here, the Complaint attributes distinct personal conduct to Smith: she allegedly possessed exclusive policy authority, approved and maintained the statewide rule, issued a September 2024 manual perpetuating it, personally assigned work to Plaintiff, received direct notice, and declined to correct the policy. ECF No. 1 ¶¶ 12, 42-44, 54."),
    (P, "Drawsand v. F.F. Properties, L.L.P., 866 F. Supp. 2d 1110 (N.D. Cal. 2011), is likewise distinguishable. Defendants cite page \"1227,\" but the pertinent discussion appears at page 1127. There, the earlier dismissal with prejudice was a final judgment, the employer and employees were sued over the same property and the same conduct, and the complaint itself alleged that the employees acted within the course and scope of employment. Id. at 1127. Here, the necessary final judgment is absent, and whether the prior HOPE defendants represented Smith's interests concerning her distinct, individual policy conduct is not established by the complaint or RJN."),
    (P, "At minimum, privity presents a fact question. It cannot be resolved against Plaintiff under the Scott standard where the relevant facts are disputed or undeveloped."),
    (S, "4. Defendants' own entity descriptions do not support dismissal."),
    (P, "The federal motion captions \"HOPE Program, A Licensed Clinical Social Worker Professional Corporation (sued and served as HOPE Psychotherapy, Inc.).\" The state-court caption in Exhibit C identifies \"HOPE PSYCHOTHERAPY, INC., d/b/a HOPE PROGRAM, a California corporation.\" Defendants cannot use the first formulation to suggest a distinct or misnamed federal entity while relying on the second to establish automatic party identity."),
    (P, "Plaintiff does not ask the Court to resolve corporate identity from captions alone. The narrower point is that Defendants must choose and prove a coherent theory. If the federal HOPE Defendant is the same corporation that appeared in state court, the \"sued and served as\" parenthetical is immaterial and the no-final-judgment defect still defeats preclusion. If Defendants contend it is a different corporation, party identity or privity cannot be assumed at the pleading stage."),
    (S, "5. The Complaint does not invoke In re Dwyer as binding precedent."),
    (P, "The motion attacks the Complaint's description of In re Dwyer. But the present claims do not depend on giving an unpublished trial-court order precedential or preclusive force. The Complaint pleads Dwyer principally as notice: HOPE personnel participated in that proceeding, a court criticized the same alleged blanket policy, and Smith allegedly continued the policy afterward. ECF No. 1 ¶¶ 2, 23-24, 44, 54. Whether Dwyer ultimately proves notice, knowledge, or intent is a merits question. Its pleaded use does not justify dismissal."),

    (S, "B. The Complaint Plausibly Alleges That Defendants Acted Under Color of State Law."),
    (S, "1. The inquiry concerns the specific challenged conduct, not HOPE's status in the abstract."),
    (P, "The question is not whether every act of a private treatment provider is state action. It is whether the conduct challenged here--jointly generating and using mandatory treatment-retention records that affected continued parole supervision--is fairly attributable to the State. Caviness v. Horizon Community Learning Center, Inc., 590 F.3d 806, 812 (9th Cir. 2010). State action may be established under any of several related approaches, including joint action and close nexus; the inquiry is necessarily fact-bound. Rawson v. Recovery Innovations, Inc., 975 F.3d 742, 747-48 (9th Cir. 2020)."),
    (P, "The Complaint alleges far more than a government contract:"),
    (L, "State law requires Plaintiff's participation and assigns the duration decision to the certified provider in consultation with the parole officer and with court approval. Cal. Penal Code § 3008(d)(2); ECF No. 1 ¶¶ 14-16, 18-19."),
    (L, "The implementing regulation requires a good-cause retention determination memorialized on a Form 3043 signed by the treatment provider and parole agent. 15 Cal. Code Regs. § 3574(f)(1)."),
    (L, "HOPE allegedly supplied the treatment-status content and recommendations that the containment team and CDCR used. ECF No. 1 ¶¶ 31-37."),
    (L, "A parole agent allegedly directed HOPE to record a no-show despite acknowledging the absence resulted from a technological error. Id. ¶ 34."),
    (L, "CDCR's discharge report expressly incorporated HOPE's assessment and recommendation before denying discharge. Id. ¶¶ 35-37."),
    (P, "Those allegations plausibly describe coordinated decision-making, not parallel private and public activity. A private person who is a willful participant in joint action with state officials acts under color of state law. Rawson v. Recovery Innovations, Inc., 975 F.3d 742, 747-48 (9th Cir. 2020); see also Franklin v. Fox, 312 F.3d 423, 445 (9th Cir. 2002). Professional judgment does not categorically break attribution; Rawson rejected that shortcut and required a close, fact-intensive assessment of the State's involvement in the challenged conduct. 975 F.3d at 753-54."),
    (P, "The alleged March 31 directive is particularly concrete. A state agent did not merely acquiesce in a private report; he allegedly instructed the private provider what false attendance result to record, with a supervisor copied. ECF No. 1 ¶ 34. The later CDCR decision allegedly relied on HOPE's treatment information. Id. ¶¶ 35-37. Those facts permit a reasonable inference of willful joint participation."),
    (P, "That the November 2025 discharge-review report also recites other supervision-related factors--including prior parole-violation history, employment status, time served on parole, and a stability assessment--does not defeat that inference. Those additional factors, even if judicially noticed for their existence, do not render HOPE's Form 3043 participation implausible as joint action; at most they raise a factual question of comparative causation unsuited to resolution on the pleadings, and they do not make amendment futile."),
    (S, "2. Defendants' published authorities are distinguishable on their own terms."),
    (P, "Caviness supports focusing on the conduct alleged. There, a charter school's public educational role did not make its post-employment statements state action because the complaint did not allege state involvement in those employment decisions. 590 F.3d at 812, 816. Here, the State allegedly participated in the challenged reporting and retention process itself: the provider and parole agent consult, sign the prescribed form, and feed the result into discharge review. ECF No. 1 ¶¶ 31-37."),
    (P, "Florer v. Congregation Pidyon Shevuyim, N.A., 639 F.3d 916 (9th Cir. 2011), arose from a contract chaplain's ecclesiastical decision that the plaintiff did not qualify for requested Jewish materials and services. The record contained no evidence that corrections officials wanted that result, jointly classified the plaintiff, or deprived him of prison-provided benefits because of it. Id. at 923-26. Here, no ecclesiastical or comparably private professional standard is at issue. The Complaint alleges an administrative, state-prescribed retention process; direct instructions from a parole agent; a jointly signed form; and actual use of HOPE's output in a discharge decision."),
    (P, "Rawson, not Florer, supplies the closer analytical model. Although the defendants in Rawson were nominally private and exercised medical judgment, the Ninth Circuit held that the totality of their integration into the State's involuntary-commitment process could make their conduct state action. 975 F.3d at 747-54. Plaintiff need not show identical facts. Rawson establishes the relevant point at this stage: professional discretion is not dispositive, no single fact controls, and the relationship must be assessed as a whole."),
    (P, "Defendants also overread Franklin. Its \"meeting of the minds\" formulation governs a conspiracy route to joint action. 312 F.3d at 445. Plaintiff also pleads direct willful participation and interdependence in a shared administrative process. He need not allege that CDCR and HOPE expressly agreed that their objective was to violate the Constitution. The allegations that they jointly generated the disputed inputs and used them to maintain mandatory treatment are enough to proceed to a factual record."),
    (S, "3. West reinforces the plausibility of attribution."),
    (P, "In West v. Atkins, 487 U.S. 42, 54-57 (1988), a contracted physician acted under color of law when providing care the State was obligated to furnish to a prisoner. Plaintiff relies on West as reinforcement, not as a categorical rule that every public contractor is a state actor. The pleaded circumstances matter: Plaintiff could not opt out of the program; the State designated the certified-provider/parole-agent process; HOPE allegedly occupied the only certified-provider role available in the region; and HOPE's reports were used in the State's exercise of supervisory authority. ECF No. 1 ¶¶ 17-19, 31-37. Taken together, those allegations plausibly show power made possible by state law and joint administration."),
    (S, "4. The Complaint alleges Smith's personal participation and HOPE's policy."),
    (P, "The motion treats Smith as though liability rested only on her title. It does not. The Complaint alleges that Smith alone could modify company policy, personally approved and maintained the blanket rule, directed the manual embodying it, personally assigned work to Plaintiff, received notice of the controversy, and failed to correct the policy. ECF No. 1 ¶¶ 12, 42-44, 54-55. Those are allegations of personal participation and deliberate indifference, not respondeat superior."),
    (P, "The claim against HOPE likewise identifies a policy and causal mechanism: the blanket retention policy, allegedly false treatment-status reporting, and retaliatory use of that reporting process. Id. ¶¶ 56-59. At the pleading stage, that is sufficient to identify the challenged policy and its alleged role in the injury."),

    (S, "C. The First Amendment Claim Alleges More Than Offensive Responsive Speech."),
    (P, "Defendants isolate Palacios's words and characterize the claim as criticism answered by criticism. The Complaint alleges a different sequence. Plaintiff complained about HOPE's retention policy, missing homework, clinician turnover, phase progression, and treatment completion. ECF No. 1 ¶ 38. At a containment-team meeting that affected parole conditions, Palacios allegedly called him \"disruptive,\" a \"ringleader,\" and \"abhorrent,\" and expressly linked those characterizations to his complaints: \"when you start complaining then the other guys chime in.\" Id. ¶¶ 39-40. The Complaint further alleges that HOPE's adverse reporting was used in treatment-retention and discharge decisions. Id. ¶¶ 31-41."),
    (P, "Thus, the alleged adverse action is not insult alone. It is the use of derogatory and allegedly false treatment characterizations within an official decision-making channel that could prolong mandatory treatment and supervision. A First Amendment retaliation claim requires protected activity, an adverse action that would chill a person of ordinary firmness, and causation. Arizona Students' Association v. Arizona Board of Regents, 824 F.3d 858, 867 (9th Cir. 2016). The explicit reference to Plaintiff's complaining supplies a plausible retaliatory nexus, and the alleged parole consequences supply injury beyond responsive speech. Whether the statements actually affected the outcome is a factual question; dismissal is not warranted merely because Defendants contest causation."),

    (S, "D. The Due-Process Claim Challenges a Systemic, Foreseeable Deprivation, Not Merely a Mistake Correctable by Grievance."),
    (P, "Plaintiff does not challenge his original conviction, the initial imposition of sex-offender treatment, or an abstract right to early discharge. He challenges the alleged use of a predetermined corporate policy and fabricated treatment inputs in a process governing the duration of mandatory treatment and continued supervision. ECF No. 1 ¶¶ 31-37, 50, 57-59."),
    (P, "Defendants' own cited provisions identify substantive and procedural constraints. Section 3008(d)(2) assigns the duration determination to an individualized consultation among the certified professional, parole officer, and court. Section 3574(f)(1) requires good cause, a written reason, and signatures from the provider and parole agent. The Complaint alleges those safeguards were hollowed out by a blanket rule and false factual inputs. It further alleges concrete restraints--GPS monitoring, curfew, mandatory attendance, and continued parole supervision--rather than stigma alone. Id. ¶¶ 37, 48-52. The Ninth Circuit recognizes a protected liberty interest in avoiding the stigmatizing sex-offender label coupled with a mandatory treatment program whose successful completion is a precondition to parole eligibility. Neal v. Shimoda, 131 F.3d 818, 830 (9th Cir. 1997). Greenholtz v. Inmates of Nebraska Penal & Correctional Complex, 442 U.S. 1 (1979), on which Defendants rely, concerns only the discretionary decision whether to grant release on parole; it does not govern the distinct liberty interest, recognized in Neal, that Plaintiff asserts here."),
    (P, "The availability of a grievance concerning mistakes in a discharge-review report does not defeat the claim on the face of the Complaint. First, Defendants identify a remedy for factual errors in the later Form 1502 report; the Complaint challenges an alleged corporate policy and false inputs originating in HOPE's treatment and Form 3043 process. Second, the random-and-unauthorized-act doctrine does not automatically make postdeprivation relief sufficient where the deprivation is foreseeable, predeprivation safeguards are practicable, and the challenged conduct occurs through an established process. Zinermon v. Burch, 494 U.S. 113, 132-39 (1990); see Logan v. Zimmerman Brush Co., 455 U.S. 422, 436 (1982). The alleged blanket policy and recurring reports fit that systemic theory."),
    (P, "Finally, Patsy means Plaintiff was not required to exhaust state administrative remedies before bringing § 1983 claims. 457 U.S. at 516. That rule does not itself prove the process inadequate; it forecloses Defendants' attempt to convert nonexhaustion into a jurisdictional or pleading bar. The adequacy of the specific procedures, and whether they could remedy the alleged policy-driven deprivation before it occurred, require a developed record."),

    (S, "E. The Bane Act Claim Pleads Coercion Beyond the Underlying Constitutional Violation."),
    (P, "The Bane Act applies whether or not the defendant acted under color of law. Cal. Civ. Code § 52.1. The Complaint alleges more than maintenance of a disputed policy. It alleges that Defendants used their gatekeeping role and adverse reporting power to compel continued participation under threat of parole consequences; that Plaintiff was threatened with parole violations for scheduling conflicts; and that Palacios used a containment-team meeting with parole officials to characterize Plaintiff adversely because he complained. ECF No. 1 ¶ 62."),
    (P, "Those allegations identify the means of coercion separately from the underlying rights: comply with the allegedly predetermined treatment regime and scheduling demands or risk adverse reports, continued restraints, or a parole violation. At minimum, whether that pressure was sufficiently coercive is fact-bound and should not be resolved by recasting the allegations as mere criticism."),
    (P, "Plaintiff does not rely on the $25,000 civil penalty in section 52.1(b), which is reserved to specified public enforcement actions. If necessary, he can remove that remedy from the prayer without dismissal of the cause of action."),

    (S, "F. The Fraud and Negligent-Misrepresentation Allegations Are Substantial; Any Particularity Gap Is Curable."),
    (P, "The motion is correct that Rule 9(b) requires the who, what, when, where, and how of fraud. Kearns v. Ford Motor Co., 567 F.3d 1120, 1124 (9th Cir. 2009). But the Complaint does not merely allege that \"Defendants\" lied at unspecified times. It identifies, among other things:"),
    (L, "a HOPE clinician's November 2022 representation that participants who completed assignments and complied could titrate and complete the program, ECF No. 1 ¶ 27;"),
    (L, "a similar representation during a January 2024 group session, id. ¶ 28;"),
    (L, "a June 2024 representation that none of Plaintiff's completed homework could be found, despite the allegation that HOPE had lost or mishandled it, id. ¶ 29;"),
    (L, "Form 3043 content transmitted to CDCR stating that Plaintiff only partially completed homework, id. ¶¶ 31-33; and"),
    (L, "the omission of an October 18, 2023 individualized plan allegedly placed in his file and sent to CDCR but never shown to him, id. ¶¶ 25(e), 65-66."),
    (P, "The Complaint also pleads direct reliance: Plaintiff remained enrolled, structured his commercial-driving work around HOPE's schedule, refrained from seeking another provider, and delayed seeking judicial relief because he believed completion remained achievable. Id. ¶¶ 26-30, 67. Those allegations answer Defendants' assertion that only CDCR relied."),
    (P, "The Court need not decide now whether every alleged communication satisfies Rule 9(b). If a speaker's name, transmission date, or medium needs greater precision, the defect is curable. Plaintiff can amend to separate each speaker and representation, identify the communication and recipient, explain why it was false when made, and plead reliance and resulting loss without group pleading. That is the paradigm case for leave to amend, not dismissal with prejudice."),

    (S, "G. The RICO Claim Should Not Be Dismissed With Prejudice."),
    (P, "The motion challenges the enterprise allegations and Rule 9(b) particularity. The Complaint alleges an association-in-fact with a common purpose, ongoing relationships, and longevity, and it identifies recurring mail and electronic transmissions of allegedly false treatment-status reports. ECF No. 1 ¶¶ 68-73. As to Smith, the required person-enterprise distinction is at least plausible because a natural person is legally distinct from the corporation and the broader association through which she allegedly acted. See Cedric Kushner Promotions, Ltd. v. King, 533 U.S. 158, 163 (2001)."),
    (P, "Plaintiff recognizes two pleading points that can be clarified if amendment is ordered. First, 18 U.S.C. § 1519 is not among the predicate offenses listed in 18 U.S.C. § 1961(1); Plaintiff therefore does not rely on paragraph 70(c) as a RICO predicate. The claim instead depends on sufficiently pleaded mail and wire fraud. Second, an amended complaint can identify each alleged mailing or wire by date, sender, recipient, document, false content, and role in the alleged scheme, and can clarify which Defendant is the RICO \"person\" and which persons and entities compose the enterprise."),
    (P, "Defendants' own authority demonstrates why prejudice is unwarranted. Schreiber Distributing Co. v. Serv-Well Furniture Co., 806 F.2d 1393, 1400-01 (9th Cir. 1986)--not 2004, as the motion states--reversed a RICO dismissal and directed that leave to amend be granted where the fraud allegations lacked particularity. If this Court finds the current mail- and wire-fraud allegations too general, the same remedy is appropriate here."),

    (S, "H. Any Dismissal Should Be With Leave to Amend."),
    (P, "Dismissal without leave is proper only when amendment could not cure the defect. Fed. R. Civ. P. 15(a)(2); Lopez, 203 F.3d at 1130-31. Plaintiff can cure any pleading deficiency identified by the Court. He can add a transaction-by-transaction fraud and RICO schedule; identify each speaker and recipient; allege the precise state-provider interactions supporting joint action; clarify the protected interest and unavailable predeprivation safeguard; separate Smith's individual acts from HOPE's policy; remove the nonpredicate § 1519 theory; and correct the Bane Act remedy."),
    (P, "None of those amendments would contradict the existing pleading. Defendants therefore cannot justify the extraordinary request to terminate every claim with prejudice at the first Rule 12 stage."),

    (H, "VI. CONCLUSION"),
    (P, "Plaintiff respectfully requests that the Court deny Defendants' motion. The state-court materials do not establish a final judgment, issue preclusion, or privity as to Smith. The Complaint plausibly alleges joint state action and constitutional injury. In the alternative, any dismissal should be with leave to amend."),
]


def signature_block() -> str:
    return (
        "Dated: September 21, 2026\n"
        "\n"
        "Respectfully submitted,\n"
        "\n"
        "\n"
        "___________________________________\n"
        "BRENDAN NGEHSI NEWANFORBI\n"
        "Plaintiff, In Pro Per"
    )


def is_toc_entry(ctype: str, text: str):
    """Roman section headers and lettered (A.-H.) argument subheads are the
    Table-of-Contents entries; the numbered sub-subheads are not listed."""
    if ctype == H:
        return ("roman", text)
    if ctype == S and re.match(r"^[A-H]\.\s", text):
        return ("letter", text)
    return None


def toc_row(d, label: str, page_str: str, bold: bool = False, indent: float = 0,
            num_reserve: float = 30) -> None:
    """Draw one TOC line: label (wrapped if long) + dot leader + right page no.
    The page number reserves a FIXED width so label wrapping -- and therefore
    the TOC's total line count -- is identical whether the number is 1 or 2
    digits. That stability is what makes the two-pass page numbers correct."""
    c = d.c
    fn = "Times-Bold" if bold else "Times-Roman"
    size = 12
    left_x = CONTENT_LEFT + indent
    right_x = CONTENT_RIGHT - 8   # small gap so page nos. don't kiss the right rule
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
        c.drawString(left_x, y, ln)
        if i == len(lines) - 1:
            c.setFont("Times-Roman", size)
            c.drawRightString(right_x, y, page_str)
            label_end = left_x + c.stringWidth(ln, fn, size) + 4
            num_w = c.stringWidth(page_str, "Times-Roman", size)
            leader_end = right_x - num_w - 4
            if leader_end > label_end:
                dw = c.stringWidth(". ", "Times-Roman", size)
                ndots = max(0, int((leader_end - label_end) / dw))
                c.drawString(label_end, y, ". " * ndots)
        d.current_line += 1


def render(out_path: Path, toc_pages: dict, capture: dict | None = None) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out_path), doc_title_footer=DOC_TITLE_FOOTER)

    c = d.c
    atty_y = d._line_y(0)
    atty_lh = 15
    for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
        c.setFont(font, size)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, text)
    d.current_line = 4
    d.blank_line()

    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()

    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()

    d.write_wrapped(
        "Hearing Date: October 20, 2026, at 10:30 a.m., in Courtroom G, 15th Floor, "
        "before the Honorable Lisa J. Cisneros, United States District Court for the "
        "Northern District of California.",
        first_indent=0,
    )
    d.blank_line()

    # --- TABLE OF CONTENTS (within the document, after the caption) ---
    d.ensure_space(4)
    d.write_line("TABLE OF CONTENTS", bold=True, center=True)
    d.blank_line()
    for ctype, text in CONTENT:
        te = is_toc_entry(ctype, text)
        if not te:
            continue
        level, label = te
        pg = str(toc_pages.get(label, "0"))
        toc_row(d, label, pg, bold=(level == "roman"),
                indent=(0 if level == "roman" else 18))
    d.blank_line()

    # --- BODY ---
    for c_type, text in CONTENT:
        if c_type == H:
            d.ensure_space(4)
            if capture is not None:
                capture[text] = d.page_num
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == S:
            d.ensure_space(6)
            if capture is not None and re.match(r"^[A-H]\.\s", text):
                capture[text] = d.page_num
            d.write_wrapped(f"<<b:{italicize_cases(text)}>>", first_indent=0)
            d.blank_line()
        elif c_type == P:
            d.write_wrapped(italicize_cases(text), first_indent=36)
            d.blank_line()
        elif c_type == L:
            d.write_wrapped("- " + italicize_cases(text), indent=36, first_indent=0)
            d.blank_line()

    d.ensure_space(9)
    for line in signature_block().split("\n"):
        if line.startswith("_") and os.path.isfile(SIGNATURE_PATH):
            d.draw_signature_image(
                SIGNATURE_PATH, SIG_IMG_W_PX, SIG_IMG_H_PX, line,
                width=SIG_WIDTH, right_margin_offset=SIG_RIGHT_OFFSET,
                height_scale=SIG_HEIGHT_SCALE,
            )
            d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)
        else:
            d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    d.blank_line()

    d.save()
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes, {d.page_num} pages)")
    return d.page_num


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    # Pass 1: capture the page each TOC entry lands on (TOC present w/ placeholders).
    capture: dict = {}
    tmp = SCRATCH_OUT.parent / "_toc_pass1.pdf"
    render(tmp, {}, capture=capture)
    try:
        tmp.unlink()
    except OSError:
        pass
    # Pass 2: render final with real TOC page numbers.
    for out in list(OUT_PATHS) + [SCRATCH_OUT]:
        render(out, capture)
    print("NOTE: not yet e-filed/served. Verify pins before filing (see review notes).")


if __name__ == "__main__":
    main()
