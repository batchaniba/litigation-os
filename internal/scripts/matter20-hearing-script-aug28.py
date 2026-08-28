#!/usr/bin/env python3
"""Matter 20 — speaker script for the August 28, 2026 CHP demurrer hearing.

Not a filing. Large-type oral-argument crib for Dept. 25 (Whitman).
Regenerate:
    python3 internal/scripts/matter20-hearing-script-aug28.py
"""

from __future__ import annotations

import os
import sys

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_PDF = os.path.join(
    REPO_ROOT,
    "internal/public/documents/matter-32/from-20",
    "Oral Argument Script - CHP Demurrer Hearing (Aug 28 2026).pdf",
)
OUT_TXT = os.path.join(
    REPO_ROOT,
    "internal/docs",
    "Matter 20 - Oral Argument Script - CHP Demurrer Hearing (Aug 28 2026).txt",
)


def P(text, style):
    return Paragraph(text, style)


def bullets(items, style, bullet="•"):
    return ListFlowable(
        [ListItem(Paragraph(it, style), leftIndent=12, bulletColor="black") for it in items],
        bulletType="bullet",
        start=bullet,
        leftIndent=18,
        bulletFontName="Times-Bold",
        bulletFontSize=12,
        spaceBefore=2,
        spaceAfter=8,
    )


def build_pdf():
    title = ParagraphStyle(
        "title", fontName="Times-Bold", fontSize=14, leading=18,
        alignment=TA_CENTER, spaceAfter=4,
    )
    sub = ParagraphStyle(
        "sub", fontName="Times-Italic", fontSize=11, leading=14,
        alignment=TA_CENTER, spaceAfter=12,
    )
    h = ParagraphStyle(
        "h", fontName="Times-Bold", fontSize=12, leading=16,
        alignment=TA_LEFT, spaceBefore=10, spaceAfter=6,
    )
    body = ParagraphStyle(
        "body", fontName="Times-Roman", fontSize=11.5, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=8,
    )
    speak = ParagraphStyle(
        "speak", fontName="Times-Roman", fontSize=12, leading=17,
        alignment=TA_JUSTIFY, spaceAfter=8, leftIndent=12, rightIndent=6,
    )
    note = ParagraphStyle(
        "note", fontName="Times-Italic", fontSize=10.5, leading=14,
        alignment=TA_LEFT, spaceAfter=8,
    )
    card = ParagraphStyle(
        "card", fontName="Times-Roman", fontSize=11, leading=15,
        alignment=TA_LEFT, spaceAfter=4,
    )
    plain = ParagraphStyle(
        "plain", fontName="Times-Roman", fontSize=11.5, leading=15,
        alignment=TA_LEFT, spaceAfter=2,
    )

    story = []
    story.append(P("ORAL ARGUMENT SCRIPT", title))
    story.append(P("Do not file. Speaker crib only.", sub))
    story.append(P("<b>Newanforbi v. California Highway Patrol, et al.</b>", sub))
    story.append(P("Alameda Super. Ct. No. 26CV191136 — August 28, 2026", sub))

    story.append(P("1. Appearance card", h))
    story.append(P(
        "<b>When / where:</b> 10:30 a.m. (not 9:00 — late tentative). "
        "Hon. Jenna M. Whitman, Dept. 25, Rene C. Davidson Courthouse, "
        "1221 Oak Street, Oakland. Zoom 161 8066 1142 / passcode 5805. "
        "CRS 811363998599.",
        card,
    ))
    story.append(P(
        "<b>Who you are:</b> Brendan Ngehsi Newanforbi, Petitioner, in propria persona.",
        card,
    ))
    story.append(P(
        "<b>Who they are:</b> Deputy Attorney General Vanessa Ing, for CHP and "
        "for Serrato, Paul, and Dutra.",
        card,
    ))
    story.append(P(
        "<b>What is on calendar:</b> CHP demurrer to the Petition for Writ of Mandate. "
        "The individual respondents joined. A joint stipulation to advance their "
        "October 16/23 dates to today has been filed; it is not yet entered. "
        "Be ready to argue all of them.",
        card,
    ))

    story.append(P("2. The tentative — memorize this table", h))
    story.append(P(
        "<b>First cause of action</b> (ministerial duty / qualifying crime under "
        "Penal Code section 679.10) — <b>OVERRULED</b>. Classic factual dispute "
        "on probable cause. Court credits the no-odor / no-impairment / false-report "
        "allegations at this stage.",
        card,
    ))
    story.append(P(
        "<b>Second</b> (reason-giving, section 679.10(i)(2)) — "
        "<b>SUSTAINED WITHOUT LEAVE</b>. Specificity required only for "
        "non-cooperation denials; this denial was “no qualifying crime.”",
        card,
    ))
    story.append(P(
        "<b>Third</b> (helpfulness presumption, section 679.10(h)) — "
        "<b>SUSTAINED WITHOUT LEAVE</b>. Presumption never triggered because "
        "CHP denied on qualifying-crime grounds.",
        card,
    ))
    story.append(P(
        "<b>Fourth</b> (declaratory relief) — <b>OVERRULED</b>. Cumulative theories "
        "are allowed at the pleading stage.",
        card,
    ))
    story.append(P(
        "The case lives on counts one and four. Do not spend argument defending "
        "two and three unless the Court asks.",
        note,
    ))

    story.append(P("3. Rules of engagement", h))
    story.append(bullets([
        "Submit on the tentative as to one and four. Do not relitigate a win.",
        "This is a demurrer. You are not proving the stop was unlawful today. You are keeping the claim alive for the writ hearing.",
        "Do not ask the Court, on demurrer, to order Form I-918 Supplement B signed.",
        "Do not correct the Court’s typos (Serrano/Serrato, APPICLABLE, WTIHOUT).",
        "Do not mention the Northern District IFP screening order unless the Court raises it. The Attorney General already attacked it; the tentative does not rely on it.",
        "Do not argue other cases (Serrato federal, Diamond, Randstad, CHP habeas).",
        "If you do not know, say so and offer to file a short supplemental letter. Do not guess.",
        "Do not use count four to relitigate reason-giving or the helpfulness presumption. Lead with section 679.10(k) and no election of remedies.",
    ], card))

    story.append(P("4. Opening — read this if the Court invites argument first", h))
    story.append(P(
        "Good morning, Your Honor. Brendan Newanforbi, Petitioner, appearing for myself.",
        speak,
    ))
    story.append(P(
        "I submit on the Court’s tentative as to the first and fourth causes of action, "
        "and I ask the Court to adopt it. The tentative is correct that this is a classic "
        "factual dispute that cannot be resolved on demurrer. Penal Code section 679.10, "
        "subdivision (g)(1), uses the word “shall”: a certifying official shall certify "
        "victim helpfulness on Form I-918 Supplement B when the victim was a victim of "
        "qualifying criminal activity and has been helpful. Whether those conditions are "
        "met turns on disputed facts. That is a merits question, not a pleading question.",
        speak,
    ))
    story.append(P(
        "I am not asking the Court today to order the Form B signed. I am asking the "
        "Court to overrule the demurrer on counts one and four so the Petition can "
        "proceed to an answer and a hearing on the merits.",
        speak,
    ))

    story.append(P("5. If the Attorney General contests count one — three points", h))
    story.append(P("<b>Point A — Demurrer cannot weigh the dashcam against the arrest report.</b>", body))
    story.append(P(
        "Your Honor, the Attorney General asks the Court to treat the dashcam transcript "
        "and the empty can as establishing probable cause as a matter of law. The tentative "
        "already rejects that. The Court must assume the truth of the properly pleaded "
        "facts. That is <i>Blank v. Kirwan</i> (1985) 39 Cal.3d 311, at 318, which both "
        "sides cite, and it is the standard the tentative applies from <i>Redfearn v. "
        "Trader Joe’s Co.</i> (2018) 20 Cal.App.5th 989.",
        speak,
    ))
    story.append(P(
        "The Petition alleges, and Exhibit 5 supports, that there was no odor of alcohol, "
        "no slurred speech, no confusion or disorientation, and that the arrest report "
        "says otherwise. Exhibit 6 is that report. Exhibit 7 is CHP’s own Penal Code "
        "section 851.6 detention certificate, issued November 5, 2024: detention only, "
        "not an arrest, insufficient grounds for making a criminal complaint. No charges "
        "were ever filed. Those are CHP’s documents. They create a conflict. They do not "
        "knock the Petition out.",
        speak,
    ))
    story.append(P("<b>Point B — Open container plus PAS refusal is not probable cause as a matter of law.</b>", body))
    story.append(P(
        "The tentative cites <i>People v. Thompson</i> (2006) 38 Cal.4th 811 for the "
        "probable-cause standard, and then holds that under the facts I have pleaded, "
        "a finder of fact could find probable cause lacking, citing <i>People v. Wolterman</i> "
        "(1992) 11 Cal.App.4th Supp. 15 and <i>Espinoza v. Shiomoto</i> (2017) 10 Cal.App.5th 85. "
        "I rest on that. An empty can in a parked car, and a declined preliminary alcohol "
        "screening test that the officer told me I was not required to take, do not as a "
        "matter of law establish driving under the influence. If they did, the Court could "
        "sustain the demurrer. The tentative says they do not.",
        speak,
    ))
    story.append(P("<b>Point C — Qualifying crime is pleaded; I do not have to prove it today.</b>", body))
    story.append(P(
        "The Petition alleges false imprisonment, unlawful criminal restraint, felonious "
        "assault, obstruction of justice, and perjury — all enumerated in 8 U.S.C. "
        "section 1101(a)(15)(U)(iii), which section 679.10 incorporates. If there was no "
        "probable cause, the restraint was not a lawful arrest. Whether that is true is "
        "for the writ hearing. On demurrer it is enough that it is alleged, supported by "
        "CHP’s own exhibits, and not contradicted as a matter of law. Penal Code section "
        "679.10 does not require a charge, a prosecution, or a conviction.",
        speak,
    ))

    story.append(P("6. If they say certification is “discretionary” so mandamus cannot lie", h))
    story.append(P(
        "Your Honor, mandamus does not lie to compel an agency to exercise discretion "
        "in a particular way. I said that in the opposition. But section 679.10, "
        "subdivision (g)(1), is not framed as open-ended discretion. It says the "
        "certifying official “shall certify” when the two statutory conditions are met. "
        "The dispute is whether those conditions are met. That is a factual dispute. "
        "The tentative treats it that way. Mandamus can compel an agency to apply the "
        "correct legal standard, and it can compel performance of a duty the Legislature "
        "made mandatory. I am not asking for a particular Form B signature on the "
        "pleadings. I am asking that count one survive so that question can be tried.",
        speak,
    ))

    story.append(P("7. If the Attorney General contests count four — declaratory relief", h))
    story.append(P(
        "Your Honor, I also submit on the tentative as to the fourth cause of action. "
        "Count four is Code of Civil Procedure section 1060. It asks the Court to declare "
        "the parties’ rights under Penal Code section 679.10. It does not ask the Court "
        "to declare that the November 1, 2024 stop was qualifying criminal activity. "
        "Paragraph 94 of the Petition says that expressly.",
        speak,
    ))
    story.append(P(
        "The Attorney General calls the claim duplicative and retrospective. The "
        "tentative already answers that. The claim may later become duplicative of the "
        "surviving first cause of action. The Court cannot make that determination on "
        "demurrer. I may plead cumulative theories, even inconsistent ones. There is no "
        "election of remedies at the pleading stage.",
        speak,
    ))
    story.append(P(
        "Count four is not a rerun of counts two and three. One of the live controversies "
        "is Penal Code section 679.10, subdivision (k): whether the absence of charges or "
        "a prosecution is a legitimate basis for denial. That question travels with count "
        "one. It is an actual controversy about how this still-pending request must be "
        "decided, and how CHP must apply the statute on reconsideration. That is "
        "prospective. <i>Griset v. Fair Political Practices Commission</i> (2001) 25 Cal.4th 688 "
        "held that declaratory relief was resolved after the writ claims were adjudicated. "
        "We are at demurrer. <i>Griset</i> does not require dismissal now.",
        speak,
    ))
    story.append(P(
        "Do not argue count four as a way to restore the reason-giving or helpfulness "
        "writ claims. The Court just sustained those without leave. If you lead with "
        "“the letter was too conclusory,” you invite the Court to reverse itself on "
        "count four. Lead with section 679.10(k) and no election of remedies.",
        note,
    ))

    story.append(P("8. Individual respondents — Serrato, Paul, Dutra", h))
    story.append(P(
        "Your Honor, the individual respondents joined CHP’s demurrer. Their joinders "
        "rise and fall with CHP on counts one and four. Captain Serrato signed the "
        "April 20, 2026 denial letter. His own memorandum acknowledges that the Petition "
        "alleges he is a certifying official and attaches that letter. He is a proper "
        "respondent under Penal Code section 679.10, subdivision (b).",
        speak,
    ))
    story.append(P(
        "Lieutenant Paul acknowledged the request on April 10, 2026 and is named in the "
        "denial letter as the contact person. Sergeant Dutra was the assigned investigator "
        "and the designated recipient of the Supplement B. The Petition alleges, in the "
        "statute’s words, that each is a certifying official. Those allegations are "
        "accepted as true on demurrer. If the Court finds any gap as to Paul or Dutra, "
        "I ask leave to amend to plead the designation more specifically. That is a "
        "curable pleading point, not a reason to dismiss them without leave.",
        speak,
    ))
    story.append(P(
        "If the Court asks whether their demurrers are actually on calendar today: "
        "The parties stipulated to advance the October 16 and October 23 dates to today. "
        "The stipulation has been filed. If it has not yet been entered, I am prepared "
        "to argue the joinders with CHP’s demurrer, or to have them heard on the "
        "stipulated date once the order is signed. I do not want a split calendar.",
        note,
    ))

    story.append(P("9. Only if the Court asks about counts two and three", h))
    story.append(P(
        "Your Honor, I submit on the tentative as to the second and third causes of "
        "action so the Court can reach the surviving claim. I will not belabor them.",
        speak,
    ))
    story.append(P(
        "<i>If, and only if, the Court invites a response on leave to amend:</i> "
        "If the Court is inclined to sustain, I respectfully ask that it be with leave "
        "to amend. This is the first challenge to the pleading. The first sentence of "
        "section 679.10(i)(2) still requires a written explanation for any denial, and "
        "the Legislative Counsel’s Digest of Assembly Bill 1261 described that duty "
        "without limiting it to non-cooperation. I can amend to plead a process claim "
        "tied to the surviving first cause of action. I will not take the Court’s time "
        "on that unless the Court wants it.",
        note,
    ))

    story.append(P("10. Closing ask — read this", h))
    story.append(P(
        "Your Honor, I ask the Court to adopt the tentative: overrule the demurrer as "
        "to the first and fourth causes of action, including as to the individual "
        "respondents on those claims, and set a deadline for an answer. The case "
        "management conference is September 2. I am prepared to proceed.",
        speak,
    ))
    story.append(P(
        "Thank you.",
        speak,
    ))

    story.append(PageBreak())
    story.append(P("11. Q&amp;A cards — short answers only", h))

    qa = [
        (
            "“The transcript shows you were parked on the shoulder with an empty can and you refused the PAS. Isn’t that probable cause?”",
            "That is a merits inference. The Petition alleges no odor, no impairment, and a false report. CHP’s own section 851.6 certificate said insufficient grounds for a complaint. The tentative holds that conflict cannot be resolved on demurrer. I rest on that.",
        ),
        (
            "“You prepared the transcript yourself.”",
            "I did, from CHP’s recording. It is Exhibit 5 to the Petition. On demurrer the Court accepts the exhibits as part of the pleading. If CHP disputes accuracy, that is for the merits, not a reason to sustain a demurrer.",
        ),
        (
            "“You were not driving a truck.”",
            "Correct. I was in a rented Tesla, parked, tired, on my way home to Stockton. That does not create probable cause for DUI, and it does not defeat a false-imprisonment theory if the arrest lacked probable cause.",
        ),
        (
            "“No charges were filed, so there is no qualifying crime.”",
            "Section 679.10 does not require a charge or a conviction. The qualifying activity is the crime against the victim. CHP’s own detention certificate is evidence that it lacked grounds for a complaint. That supports the claim; it does not defeat it.",
        ),
        (
            "“This is a federal U-visa question. Why are we here?”",
            "I am not asking this Court to grant a U visa. USCIS does that. I am asking this Court to enforce California Penal Code section 679.10 — a state-law duty the Legislature placed on certifying entities, including CHP.",
        ),
        (
            "“Are you asking me to order them to sign the form today?”",
            "No, Your Honor. Not on demurrer. Overrule counts one and four. At the merits hearing I will ask the Court to compel certification if the record shows the statutory conditions are met, or at minimum to vacate the denial and remand for a new determination under the correct standard.",
        ),
        (
            "“Serrato / Paul / Dutra are not certifying officials.”",
            "Serrato signed the denial. Paul processed the request. Dutra was the assigned investigator and designated recipient. Each is alleged, in the statute’s words, to be a certifying official. If any allegation is thin, grant leave to amend. Do not dismiss them without leave.",
        ),
        (
            "“Declaratory relief is duplicative / retrospective.”",
            "The tentative already holds the claim may later become duplicative of the surviving first cause of action, and that I need not elect remedies on demurrer. Count four also presents section 679.10(k): whether the absence of charges is a legitimate basis for denial. That controversy is live with count one. Griset resolved declaratory relief after the writ was adjudicated. We are at demurrer.",
        ),
        (
            "“Count four just repeats the reason-giving and helpfulness claims I already sustained.”",
            "I am not asking the Court to restore counts two and three through a declaration. Paragraph 94 does not seek a declaration on qualifying crime. The live declaration is how section 679.10, including subdivision (k), governs this still-pending request. That is why the tentative overruled count four.",
        ),
        (
            "“The Northern District already screened a related complaint.”",
            "That order is not before this Court and I do not rely on it. This Petition stands on its own exhibits and on California mandate law.",
        ),
        (
            "“Why shouldn’t I sustain without leave on everything?”",
            "Because the first cause of action turns on contested facts the Court has already identified. Sustaining without leave would decide the merits on a demurrer. The tentative does not do that, and it should not.",
        ),
    ]
    for q, a in qa:
        story.append(P(f"<b>Q. {q}</b>", card))
        story.append(P(f"A. {a}", speak))

    story.append(P("12. Do not say", h))
    story.append(bullets([
        "Do not say “the tentative is a win” or “I already won.” Say “I submit on the tentative as to one and four.”",
        "Do not argue that CHP officers are criminals as a personal attack. Stay on the exhibits: report versus dashcam versus the 851.6 certificate.",
        "Do not quote damages, lost CDL wages, or immigration consequences as a reason to overrule a demurrer. Those are not pleading-stage issues.",
        "Do not volunteer counts two and three. If asked, submit.",
        "Do not use count four to restore reason-giving or the helpfulness presumption. Lead with section 679.10(k).",
        "Do not correct the Court. If the Court says “Serrano,” let it go.",
        "Do not interrupt the Attorney General. Take notes. Answer the Court’s questions, not opposing counsel’s speeches.",
    ], card))

    story.append(P("13. After the hearing", h))
    story.append(P(
        "Write down the ruling word for word, including any answer deadline and whether "
        "the individual demurrers were ruled on or continued. The September 2, 2026 "
        "case management conference remains on calendar unless the Court says otherwise. "
        "Do not email the Attorney General a “confirmation” of what you think was said. "
        "Wait for the minute order.",
        body,
    ))
    story.append(Spacer(1, 8))
    story.append(P(
        "Authorities used in this crib are limited to the tentative, the filed opposition, "
        "and the Penal Code. <i>Blank v. Kirwan</i> (1985) 39 Cal.3d 311; "
        "<i>Redfearn v. Trader Joe’s Co.</i> (2018) 20 Cal.App.5th 989; "
        "<i>People v. Thompson</i> (2006) 38 Cal.4th 811; "
        "<i>People v. Wolterman</i> (1992) 11 Cal.App.4th Supp. 15; "
        "<i>Espinoza v. Shiomoto</i> (2017) 10 Cal.App.5th 85; "
        "Penal Code sections 679.10 and 851.6; "
        "<i>Griset v. Fair Political Practices Commission</i> (2001) 25 Cal.4th 688 "
        "(only if the Attorney General cites it).",
        note,
    ))

    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="Oral Argument Script — CHP Demurrer Hearing (August 28, 2026)",
        author="Brendan Ngehsi Newanforbi",
    )
    doc.build(story)
    return OUT_PDF


TXT = r"""ORAL ARGUMENT SCRIPT — DO NOT FILE
Newanforbi v. California Highway Patrol, et al.
Alameda Super. Ct. No. 26CV191136
Hon. Jenna M. Whitman, Dept. 25 — August 28, 2026, 10:30 a.m. (not 9:00)
Zoom: 161 8066 1142 / passcode 5805     CRS: 811363998599

You: Brendan Ngehsi Newanforbi, Petitioner, in propria persona.
Them: Deputy Attorney General Vanessa Ing (CHP + Serrato / Paul / Dutra).


================================================================================
TENTATIVE (issued August 27, 2026) — memorize this
================================================================================
1st COA  ministerial duty / qualifying crime     OVERRULED
2nd COA  reason-giving (§679.10(i)(2))           SUSTAINED WITHOUT LEAVE
3rd COA  helpfulness presumption (§679.10(h))    SUSTAINED WITHOUT LEAVE
4th COA  declaratory relief                      OVERRULED

The case lives on counts one and four. Do not spend argument defending two and
three unless the Court asks.


================================================================================
RULES
================================================================================
- Submit on the tentative as to one and four. Do not relitigate a win.
- This is a demurrer. You are not proving the stop was unlawful today.
- Do not ask the Court, on demurrer, to order Form I-918 Supplement B signed.
- Do not correct the Court's typos (Serrano/Serrato, APPICLABLE, WTIHOUT).
- Do not mention the Northern District IFP order unless the Court raises it.
- Do not argue other cases. If you do not know, say so. Do not guess.
- Do not use count four to relitigate reason-giving or the helpfulness
  presumption. Lead with section 679.10(k) and no election of remedies.


================================================================================
OPENING — read this
================================================================================
Good morning, Your Honor. Brendan Newanforbi, Petitioner, appearing for myself.

I submit on the Court's tentative as to the first and fourth causes of action,
and I ask the Court to adopt it. The tentative is correct that this is a classic
factual dispute that cannot be resolved on demurrer. Penal Code section 679.10,
subdivision (g)(1), uses the word "shall": a certifying official shall certify
victim helpfulness on Form I-918 Supplement B when the victim was a victim of
qualifying criminal activity and has been helpful. Whether those conditions are
met turns on disputed facts. That is a merits question, not a pleading question.

I am not asking the Court today to order the Form B signed. I am asking the
Court to overrule the demurrer on counts one and four so the Petition can
proceed to an answer and a hearing on the merits.


================================================================================
IF THE ATTORNEY GENERAL CONTESTS COUNT ONE — three points
================================================================================
POINT A — Demurrer cannot weigh the dashcam against the arrest report.

Your Honor, the Attorney General asks the Court to treat the dashcam transcript
and the empty can as establishing probable cause as a matter of law. The
tentative already rejects that. The Court must assume the truth of the properly
pleaded facts. That is Blank v. Kirwan (1985) 39 Cal.3d 311, at 318, which both
sides cite, and it is the standard the tentative applies from Redfearn v. Trader
Joe's Co. (2018) 20 Cal.App.5th 989.

The Petition alleges, and Exhibit 5 supports, that there was no odor of alcohol,
no slurred speech, no confusion or disorientation, and that the arrest report
says otherwise. Exhibit 6 is that report. Exhibit 7 is CHP's own Penal Code
section 851.6 detention certificate, issued November 5, 2024: detention only,
not an arrest, insufficient grounds for making a criminal complaint. No charges
were ever filed. Those are CHP's documents. They create a conflict. They do not
knock the Petition out.

POINT B — Open container plus PAS refusal is not probable cause as a matter of law.

The tentative cites People v. Thompson (2006) 38 Cal.4th 811 for the
probable-cause standard, and then holds that under the facts I have pleaded, a
finder of fact could find probable cause lacking, citing People v. Wolterman
(1992) 11 Cal.App.4th Supp. 15 and Espinoza v. Shiomoto (2017) 10 Cal.App.5th 85.
I rest on that. An empty can in a parked car, and a declined preliminary alcohol
screening test that the officer told me I was not required to take, do not as a
matter of law establish driving under the influence. If they did, the Court
could sustain the demurrer. The tentative says they do not.

POINT C — Qualifying crime is pleaded; I do not have to prove it today.

The Petition alleges false imprisonment, unlawful criminal restraint, felonious
assault, obstruction of justice, and perjury — all enumerated in 8 U.S.C.
section 1101(a)(15)(U)(iii), which section 679.10 incorporates. If there was no
probable cause, the restraint was not a lawful arrest. Whether that is true is
for the writ hearing. On demurrer it is enough that it is alleged, supported by
CHP's own exhibits, and not contradicted as a matter of law. Penal Code section
679.10 does not require a charge, a prosecution, or a conviction.


================================================================================
IF THEY SAY CERTIFICATION IS "DISCRETIONARY"
================================================================================
Your Honor, mandamus does not lie to compel an agency to exercise discretion in
a particular way. I said that in the opposition. But section 679.10, subdivision
(g)(1), is not framed as open-ended discretion. It says the certifying official
"shall certify" when the two statutory conditions are met. The dispute is
whether those conditions are met. That is a factual dispute. The tentative
treats it that way. Mandamus can compel an agency to apply the correct legal
standard, and it can compel performance of a duty the Legislature made
mandatory. I am not asking for a particular Form B signature on the pleadings.
I am asking that count one survive so that question can be tried.


================================================================================
IF THE ATTORNEY GENERAL CONTESTS COUNT FOUR
================================================================================
Your Honor, I also submit on the Court's tentative as to the fourth cause of
action. Count four is Code of Civil Procedure section 1060. It asks the Court
to declare the parties' rights under Penal Code section 679.10. It does not
ask the Court to declare that the November 1, 2024 stop was qualifying criminal
activity. Paragraph 94 of the Petition says that expressly.

The Attorney General calls the claim duplicative and retrospective. The
tentative already answers that. The claim may later become duplicative of the
surviving first cause of action. The Court cannot make that determination on
demurrer. I may plead cumulative theories, even inconsistent ones. There is
no election of remedies at the pleading stage.

Count four is not a rerun of counts two and three. One of the live
controversies is Penal Code section 679.10, subdivision (k): whether the
absence of charges or a prosecution is a legitimate basis for denial. That
question travels with count one. It is an actual controversy about how this
still-pending request must be decided, and how CHP must apply the statute on
reconsideration. That is prospective. Griset v. Fair Political Practices
Commission (2001) 25 Cal.4th 688 held that declaratory relief was resolved
after the writ claims were adjudicated. We are at demurrer. Griset does not
require dismissal now.

Do not argue count four as a way to restore the reason-giving or helpfulness
writ claims. If you lead with "the letter was too conclusory," you invite the
Court to reverse itself on count four. Lead with section 679.10(k) and no
election of remedies.


================================================================================
INDIVIDUAL RESPONDENTS
================================================================================
Your Honor, the individual respondents joined CHP's demurrer. Their joinders
rise and fall with CHP on counts one and four. Captain Serrato signed the
April 20, 2026 denial letter. His own memorandum acknowledges that the Petition
alleges he is a certifying official and attaches that letter. He is a proper
respondent under Penal Code section 679.10, subdivision (b).

Lieutenant Paul acknowledged the request on April 10, 2026 and is named in the
denial letter as the contact person. Sergeant Dutra was the assigned investigator
and the designated recipient of the Supplement B. The Petition alleges, in the
statute's words, that each is a certifying official. Those allegations are
accepted as true on demurrer. If the Court finds any gap as to Paul or Dutra, I
ask leave to amend to plead the designation more specifically. That is a curable
pleading point, not a reason to dismiss them without leave.

If asked whether their demurrers are on calendar: The parties stipulated to
advance the October 16 and October 23 dates to today. The stipulation has been
filed. If it has not yet been entered, I am prepared to argue the joinders with
CHP's demurrer, or to have them heard on the stipulated date once the order is
signed. I do not want a split calendar.


================================================================================
ONLY IF THE COURT ASKS ABOUT COUNTS TWO AND THREE
================================================================================
Your Honor, I submit on the tentative as to the second and third causes of
action so the Court can reach the surviving claim. I will not belabor them.

Only if the Court invites a response on leave to amend:
If the Court is inclined to sustain, I respectfully ask that it be with leave to
amend. This is the first challenge to the pleading. The first sentence of
section 679.10(i)(2) still requires a written explanation for any denial, and
the Legislative Counsel's Digest of Assembly Bill 1261 described that duty
without limiting it to non-cooperation. I can amend to plead a process claim
tied to the surviving first cause of action. I will not take the Court's time
on that unless the Court wants it.


================================================================================
CLOSING ASK — read this
================================================================================
Your Honor, I ask the Court to adopt the tentative: overrule the demurrer as to
the first and fourth causes of action, including as to the individual respondents
on those claims, and set a deadline for an answer. The case management conference
is September 2. I am prepared to proceed.

Thank you.


================================================================================
Q&A CARDS
================================================================================
Q. The transcript shows you were parked on the shoulder with an empty can and
   you refused the PAS. Isn't that probable cause?
A. That is a merits inference. The Petition alleges no odor, no impairment, and
   a false report. CHP's own section 851.6 certificate said insufficient grounds
   for a complaint. The tentative holds that conflict cannot be resolved on
   demurrer. I rest on that.

Q. You prepared the transcript yourself.
A. I did, from CHP's recording. It is Exhibit 5 to the Petition. On demurrer the
   Court accepts the exhibits as part of the pleading. If CHP disputes accuracy,
   that is for the merits, not a reason to sustain a demurrer.

Q. You were not driving a truck.
A. Correct. I was in a rented Tesla, parked, tired, on my way home to Stockton.
   That does not create probable cause for DUI, and it does not defeat a
   false-imprisonment theory if the arrest lacked probable cause.

Q. No charges were filed, so there is no qualifying crime.
A. Section 679.10 does not require a charge or a conviction. The qualifying
   activity is the crime against the victim. CHP's own detention certificate is
   evidence that it lacked grounds for a complaint. That supports the claim; it
   does not defeat it.

Q. This is a federal U-visa question. Why are we here?
A. I am not asking this Court to grant a U visa. USCIS does that. I am asking
   this Court to enforce California Penal Code section 679.10 — a state-law duty
   the Legislature placed on certifying entities, including CHP.

Q. Are you asking me to order them to sign the form today?
A. No, Your Honor. Not on demurrer. Overrule counts one and four. At the merits
   hearing I will ask the Court to compel certification if the record shows the
   statutory conditions are met, or at minimum to vacate the denial and remand
   for a new determination under the correct standard.

Q. Serrato / Paul / Dutra are not certifying officials.
A. Serrato signed the denial. Paul processed the request. Dutra was the assigned
   investigator and designated recipient. Each is alleged, in the statute's
   words, to be a certifying official. If any allegation is thin, grant leave to
   amend. Do not dismiss them without leave.

Q. Declaratory relief is duplicative / retrospective.
A. The tentative already holds the claim may later become duplicative of the
   surviving first cause of action, and that I need not elect remedies on
   demurrer. Count four also presents section 679.10(k): whether the absence
   of charges is a legitimate basis for denial. That controversy is live with
   count one. Griset resolved declaratory relief after the writ was
   adjudicated. We are at demurrer.

Q. Count four just repeats the reason-giving and helpfulness claims I already
   sustained.
A. I am not asking the Court to restore counts two and three through a
   declaration. Paragraph 94 does not seek a declaration on qualifying crime.
   The live declaration is how section 679.10, including subdivision (k),
   governs this still-pending request. That is why the tentative overruled
   count four.

Q. The Northern District already screened a related complaint.
A. That order is not before this Court and I do not rely on it. This Petition
   stands on its own exhibits and on California mandate law.

Q. Why shouldn't I sustain without leave on everything?
A. Because the first cause of action turns on contested facts the Court has
   already identified. Sustaining without leave would decide the merits on a
   demurrer. The tentative does not do that, and it should not.


================================================================================
DO NOT SAY
================================================================================
- "The tentative is a win" / "I already won." Say: "I submit on the tentative
  as to one and four."
- Do not personally attack the officers. Stay on the exhibits.
- Do not quote damages, lost CDL wages, or immigration consequences.
- Do not volunteer counts two and three.
- Do not use count four to restore reason-giving or the helpfulness
  presumption. Lead with section 679.10(k).
- Do not correct the Court. If the Court says "Serrano," let it go.
- Do not interrupt the Attorney General.


================================================================================
AFTER THE HEARING
================================================================================
Write down the ruling word for word, including any answer deadline and whether
the individual demurrers were ruled on or continued. The September 2, 2026 case
management conference remains on calendar unless the Court says otherwise. Do
not email the Attorney General a "confirmation" of what you think was said.
Wait for the minute order.

Authorities in this crib: Blank v. Kirwan (1985) 39 Cal.3d 311; Redfearn v.
Trader Joe's Co. (2018) 20 Cal.App.5th 989; People v. Thompson (2006) 38 Cal.4th
811; People v. Wolterman (1992) 11 Cal.App.4th Supp. 15; Espinoza v. Shiomoto
(2017) 10 Cal.App.5th 85; Penal Code sections 679.10 and 851.6; Griset v. Fair
Political Practices Commission (2001) 25 Cal.4th 688 (only if the Attorney
General cites it).
"""


def main() -> None:
    os.makedirs(os.path.dirname(OUT_TXT), exist_ok=True)
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write(TXT.lstrip("\n"))
        if not TXT.endswith("\n"):
            f.write("\n")
    pdf = build_pdf()
    print(f"Wrote {OUT_TXT}")
    print(f"Wrote {pdf}")


if __name__ == "__main__":
    main()
