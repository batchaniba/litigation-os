#!/usr/bin/env python3
"""Matter 33 -- Plaintiff's Motion to Strike Defendants' Answer (ECF No. 11).

Nforbi v. Candelaria et al., USDC N.D. Cal. No. 3:26-cv-08272-LJC.
Hearing: November 12, 2026, 1:30 p.m., Videoconference (Zoom) (Hon. Lisa J. Cisneros).

This script builds:
  1. Plaintiff's Notice of Motion and Motion to Strike Defendants' Answer (ECF No. 11)
     Pursuant to Fed. R. Civ. P. 12(f); or, in the Alternative, to Strike Affirmative
     Defenses; Memorandum of Points and Authorities in Support.
  2. [Proposed] Order Granting Plaintiff's Motion to Strike.
  3. Rule 5 Proof of Service.
  4. Assembles the filing packet and copies to the short-link location.

Usage:
    python3 internal/scripts/matter33-motion-to-strike-answer.py \\
        [--date "September 5, 2026"] [--mailed-from "San Jose, California"]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from matter33_counsel import counsel_pos_recipients  # noqa: E402
from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]

# Primary filing output: Motion + Memo of P&As + attached Proof of Service
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-33/ndcal"
    / "Plaintiff Motion to Strike Answer (N.D. Cal. 3-26-cv-08272-LJC) (Sep 5 2026).pdf"
)

# Standalone Proposed Order
DEFAULT_ORDER_OUT = (
    ROOT
    / "internal/public/documents/matter-33/ndcal"
    / "Proposed Order Granting Motion to Strike Answer (N.D. Cal. 3-26-cv-08272-LJC) (Sep 5 2026).pdf"
)

# Standalone Proof of Service
DEFAULT_POS_OUT = (
    ROOT
    / "internal/public/documents/matter-33/ndcal"
    / "Proof of Service - Motion to Strike Answer (N.D. Cal. 3-26-cv-08272-LJC) (Sep 5 2026).pdf"
)

# Combined packet with Proposed Order included
DEFAULT_PACKET_OUT = (
    ROOT
    / "internal/public/documents/matter-33/ndcal"
    / "Plaintiff Motion to Strike Answer Packet with Proposed Order (N.D. Cal. 3-26-cv-08272-LJC) (Sep 5 2026).pdf"
)

DEFAULT_EXEC_DATE = "September 5, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
SHORT_LINK_SLUG = "cand-strike"
PACKET_SLUG = "cand-strike-packet"

FOOTER = (
    "PLAINTIFF'S MOTION TO STRIKE ANSWER (ECF NO. 11) -- "
    "NFORBI v. CANDELARIA ET AL."
)
ORDER_FOOTER = (
    "[PROPOSED] ORDER GRANTING MOTION TO STRIKE -- "
    "NFORBI v. CANDELARIA ET AL."
)

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("DIANA CANDELARIA, in her", True, False),
    ("individual capacity; STEVE", True, False),
    ("GORDON, in his official", True, False),
    ("capacity; and DOES 1-10,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
    ("", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 3:26-cv-08272-LJC", False, False),
    ("", False, False),
    ("PLAINTIFF'S NOTICE OF MOTION", True, False),
    ("AND MOTION TO STRIKE", True, False),
    ("DEFENDANTS' ANSWER (ECF NO. 11)", True, False),
    ("PURSUANT TO FED. R. CIV. P. 12(f);", True, False),
    ("OR, IN THE ALTERNATIVE, TO", True, False),
    ("STRIKE AFFIRMATIVE DEFENSES;", True, False),
    ("MEMORANDUM OF POINTS AND", True, False),
    ("AUTHORITIES IN SUPPORT", True, False),
    ("", False, False),
    ("Date: November 12, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: Videoconference (Zoom)", False, False),
    ("Judge: Hon. Lisa J. Cisneros", False, False),
    ("", False, False),
    ("Action Filed: August 10, 2026", False, False),
    ("Operative FAC: August 17, 2026", False, False),
]

ORDER_CAPTION_RIGHT = [
    ("Case No. 3:26-cv-08272-LJC", False, False),
    ("", False, False),
    ("[PROPOSED] ORDER GRANTING", True, False),
    ("PLAINTIFF'S MOTION TO STRIKE", True, False),
    ("DEFENDANTS' ANSWER (ECF NO. 11)", True, False),
    ("PURSUANT TO FED. R. CIV. P. 12(f)", True, False),
    ("", False, False),
    ("Date: November 12, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: Videoconference (Zoom)", False, False),
    ("Judge: Hon. Lisa J. Cisneros", False, False),
    ("", False, False),
    ("Action Filed: August 10, 2026", False, False),
    ("Operative FAC: August 17, 2026", False, False),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

# Tigno is PACER lead / attorney to be noticed. Do not omit him.
SERVICE_RECIPIENTS = counsel_pos_recipients()

# Body content for the Notice of Motion and Memorandum of Points and Authorities
CONTENT: list[tuple[str, str]] = [
    (
        "HEADER",
        "PLAINTIFF'S NOTICE OF MOTION AND MOTION TO STRIKE\n"
        "DEFENDANTS' ANSWER (ECF NO. 11) PURSUANT TO FED. R. CIV. P. 12(f);\n"
        "OR, IN THE ALTERNATIVE, TO STRIKE AFFIRMATIVE DEFENSES",
    ),
    (
        "PARA",
        "TO ALL PARTIES AND THEIR ATTORNEYS OF RECORD:",
    ),
    (
        "PARA",
        "PLEASE TAKE NOTICE that Plaintiff notices this Motion for hearing at the Initial Case "
        "Management Conference already set by the Court's Dkt. 4 order for November 12, 2026, at 1:30 p.m., "
        "or as soon thereafter as the matter may be heard, or on such other date as the Court may set, "
        "before the Honorable Lisa J. Cisneros, United States Magistrate Judge, United States District Court "
        "for the Northern District of California, appearing via Zoom videoconference "
        "(https://cand.uscourts.gov/ljc) or in such courtroom as the Court may designate. "
        "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, will and hereby does move this Court, "
        "pursuant to Federal Rule of Civil Procedure 12(f), for an order:",
    ),
    (
        "LIST_ITEM",
        "1. Striking in its entirety the Answer filed by Defendants Diana Candelaria and Steve Gordon "
        "on September 4, 2026 (ECF No. 11), on the ground that it is directed solely to Plaintiff's "
        "original Complaint (Dkt. 1) filed August 10, 2026, which was superseded in full on August 17, 2026 "
        "by Plaintiff's First Amended Complaint (Dkt. 6), rendering the Answer a procedural nullity that is "
        "redundant, immaterial, and impertinent under Rule 12(f);",
    ),
    (
        "LIST_ITEM",
        "2. In the alternative, if the Answer is not stricken in its entirety, striking all thirty-three (33) "
        "Affirmative Defenses asserted in Defendants' Answer (ECF No. 11 at 32:20-35:20), or specific subsets "
        "thereof, on the grounds that they are legally insufficient, impertinent, redundant, immaterial, fail "
        "to satisfy the pleading standards of Federal Rules of Civil Procedure 8 and 12(f), and consist of bare "
        "boilerplate legal conclusions devoid of factual support, raw template drafting placeholders ('xxx'), "
        "inapplicable state-law tort immunities that cannot bar federal civil rights claims under 42 U.S.C. "
        "§ 1983, irrelevant employment discrimination statutes of limitations, and legally untenable defenses "
        "contrary to binding Supreme Court and Ninth Circuit precedent;",
    ),
    (
        "LIST_ITEM",
        "3. Ordering Defendants to file and serve an answer addressing the operative First Amended Complaint "
        "(Dkt. 6) within fourteen (14) days of the Court's order, and instructing Defendants that any such "
        "answer must strictly conform to Federal Rule of Civil Procedure 8(b) without evasive boilerplate "
        "asserting that 'the law speaks for itself'; and",
    ),
    (
        "LIST_ITEM",
        "4. Granting such other and further relief as the Court deems just and proper.",
    ),
    (
        "PARA",
        "This Motion is based upon this Notice of Motion, the attached Memorandum of Points and "
        "Authorities, the Court's records and files in this action (including Dkt. 1, Dkt. 4, Dkt. 5, "
        "Dkt. 6, Dkt. 8, and ECF No. 11), the attached Proof of Service, and such further argument or "
        "evidence as may be presented at or before the hearing.",
    ),
    (
        "PARA",
        "Pursuant to Civil Local Rule 7-3(a), any opposition must be filed and served not more than "
        "fourteen (14) days after this Motion is filed. Any reply must be filed and served not more than "
        "seven (7) days after the opposition is filed. Civil L.R. 7-3(c). This Notice is given more than "
        "thirty-five (35) days before the noticed hearing. Civil L.R. 7-2(a).",
    ),
    (
        "HEADER",
        "MEMORANDUM OF POINTS AND AUTHORITIES",
    ),
    (
        "HEADER",
        "TABLE OF CONTENTS",
    ),
    (
        "LIST_ITEM",
        "Issues to Be Decided",
    ),
    (
        "LIST_ITEM",
        "I. Introduction",
    ),
    (
        "LIST_ITEM",
        "II. Relevant Procedural Background",
    ),
    (
        "LIST_ITEM",
        "III. Legal Standard Under Fed. R. Civ. P. 12(f)",
    ),
    (
        "LIST_ITEM",
        "IV. Argument",
    ),
    (
        "LIST_ITEM",
        "    A. The Entire Answer Must Be Stricken",
    ),
    (
        "LIST_ITEM",
        "    B. The Thirty-Three Affirmative Defenses Must Be Stricken",
    ),
    (
        "LIST_ITEM",
        "    C. Systematic Evasive Denials Violate Rule 8(b)",
    ),
    (
        "LIST_ITEM",
        "V. Conclusion",
    ),
    (
        "HEADER",
        "TABLE OF AUTHORITIES",
    ),
    (
        "SUBHEAD",
        "Cases",
    ),
    (
        "LIST_ITEM",
        "<<i:Ashcroft v. Iqbal>>, 556 U.S. 662 (2009)",
    ),
    (
        "LIST_ITEM",
        "<<i:Barnes v. AT&T Pension Benefit Plan>>, 718 F. Supp. 2d 1167 (N.D. Cal. 2010)",
    ),
    (
        "LIST_ITEM",
        "<<i:Bell Atl. Corp. v. Twombly>>, 550 U.S. 544 (2007)",
    ),
    (
        "LIST_ITEM",
        "<<i:Butz v. Economou>>, 438 U.S. 478 (1978)",
    ),
    (
        "LIST_ITEM",
        "<<i:Cleavinger v. Saxner>>, 474 U.S. 193 (1985)",
    ),
    (
        "LIST_ITEM",
        "<<i:Ex parte Young>>, 209 U.S. 123 (1908)",
    ),
    (
        "LIST_ITEM",
        "<<i:Felder v. Casey>>, 487 U.S. 131 (1988)",
    ),
    (
        "LIST_ITEM",
        "<<i:Ferdik v. Bonzelet>>, 963 F.2d 1258 (9th Cir. 1992)",
    ),
    (
        "LIST_ITEM",
        "<<i:Hafer v. Melo>>, 502 U.S. 21 (1991)",
    ),
    (
        "LIST_ITEM",
        "<<i:Hal Roach Studios, Inc. v. Richard Feiner & Co.>>, 896 F.2d 1542 (9th Cir. 1990)",
    ),
    (
        "LIST_ITEM",
        "<<i:Lacey v. Maricopa County>>, 693 F.3d 896 (9th Cir. 2012) (en banc)",
    ),
    (
        "LIST_ITEM",
        "<<i:Martinez v. California>>, 444 U.S. 277 (1980)",
    ),
    (
        "LIST_ITEM",
        "<<i:Patsy v. Bd. of Regents>>, 457 U.S. 496 (1982)",
    ),
    (
        "LIST_ITEM",
        "<<i:Pennhurst State Sch. & Hosp. v. Halderman>>, 465 U.S. 89 (1984)",
    ),
    (
        "LIST_ITEM",
        "<<i:Ramirez v. County of San Bernardino>>, 806 F.3d 1002 (9th Cir. 2015)",
    ),
    (
        "LIST_ITEM",
        "<<i:Whittlestone, Inc. v. Handi-Craft Co.>>, 618 F.3d 970 (9th Cir. 2010)",
    ),
    (
        "LIST_ITEM",
        "<<i:Will v. Michigan Dept. of State Police>>, 491 U.S. 58 (1989)",
    ),
    (
        "LIST_ITEM",
        "<<i:Wyshak v. City Nat'l Bank>>, 607 F.2d 824 (9th Cir. 1979)",
    ),
    (
        "SUBHEAD",
        "Statutes and Rules",
    ),
    (
        "LIST_ITEM",
        "Fed. R. Civ. P. 8, 12(f), 15",
    ),
    (
        "LIST_ITEM",
        "42 U.S.C. § 1983",
    ),
    (
        "LIST_ITEM",
        "N.D. Cal. Civil L.R. 7-2, 7-3, 7-4",
    ),
    (
        "HEADER",
        "ISSUES TO BE DECIDED",
    ),
    (
        "LIST_ITEM",
        "1. Whether Defendants' Answer (ECF No. 11) must be stricken under Rule 12(f) because it "
        "responds solely to the superseded original Complaint (Dkt. 1) rather than the operative "
        "First Amended Complaint (Dkt. 6).",
    ),
    (
        "LIST_ITEM",
        "2. In the alternative, whether Defendants' thirty-three affirmative defenses must be stricken "
        "as legally insufficient, impertinent, or boilerplate under Rules 8 and 12(f).",
    ),
    (
        "LIST_ITEM",
        "3. Whether Defendants should be ordered to answer Dkt. 6 within fourteen days in conformity "
        "with Rule 8(b).",
    ),
    (
        "HEADER",
        "I. INTRODUCTION",
    ),
    (
        "PARA",
        "On September 4, 2026, Defendants Diana Candelaria and Steve Gordon filed a 37-page Answer "
        "(ECF No. 11). On the face of page 1, Defendants expressly state that they are answering "
        "\"Plaintiff Brendan Ngwa Nforbi's COMPLAINT FOR DAMAGES AND FOR DECLARATORY AND INJUNCTIVE "
        "RELIEF ('Complaint') (Document 1) filed on August 10, 2026.\" (ECF No. 11 at 1:26-28.) "
        "The Answer then proceeds paragraph by paragraph through the 136 paragraphs of that original August 10 "
        "pleading, concluding with 33 boilerplate affirmative defenses.",
    ),
    (
        "PARA",
        "There is a fatal procedural defect in Defendants' filing: Plaintiff's original Complaint (Dkt. 1) "
        "has not been the operative pleading in this case for weeks. On August 17, 2026, Plaintiff filed his "
        "conforming First Amended Complaint (\"FAC\") (Dkt. 6). On August 21, 2026, Plaintiff served that "
        "operative FAC on both Defendants by first-class mail at the California Department of Motor Vehicles "
        "Legal Affairs Division. On August 24, 2026, Plaintiff filed a formal Notice Identifying Operative "
        "First Amended Complaint (Dkt. 8), specifically alerting the Court and all parties that Dkt. 6 is the "
        "sole operative pleading of record and that the earlier complaints were superseded in full under "
        "Federal Rule of Civil Procedure 15(a) and <<i:Lacey v. Maricopa County>>, 693 F.3d 896, 927 (9th Cir. "
        "2012) (en banc).",
    ),
    (
        "PARA",
        "Under bedrock Ninth Circuit law, an amended complaint supersedes the original complaint in its entirety, "
        "and the original complaint is treated thereafter as non-existent. <<i:Ramirez v. County of San "
        "Bernardino>>, 806 F.3d 1002, 1008 (9th Cir. 2015); <<i:Hal Roach Studios, Inc. v. Richard Feiner & "
        "Co.>>, 896 F.2d 1542, 1546 (9th Cir. 1990). An answer directed to a superseded complaint is a "
        "procedural nullity: it fails to join issue on the operative claims, responds to allegations that no "
        "longer control, and leaves the actual operative pleading unanswered. Federal courts routinely strike "
        "answers responding to superseded pleadings pursuant to Federal Rule of Civil Procedure 12(f).",
    ),
    (
        "PARA",
        "Even if the Answer were not stricken in its entirety, each of Defendants' thirty-three (33) Affirmative "
        "Defenses must be stricken. Defendants' affirmative defenses represent the worst form of boilerplate "
        "pleading. They consist of one-sentence legal slogans devoid of a single supporting fact; negative "
        "defenses that merely dispute Plaintiff's prima facie burden; state-law tort immunities that have zero "
        "application to federal civil rights claims under 42 U.S.C. § 1983; an irrelevant Title VII employment "
        "discrimination statute of limitations; unsupportable claims of quasi-judicial absolute immunity for DMV "
        "hearing officers; an invalid 'reservation of rights' to amend; and raw, unedited internal drafting "
        "placeholders ('xxx' and 'xx') that confirm counsel copied an unvetted template without reading the "
        "operative complaint.",
    ),
    (
        "PARA",
        "Finally, Defendants' pervasive refusal to admit or deny factual allegations—relying on the canned "
        "evasion that allegations 'purport to be conclusions of law' and 'the law speaks for itself'—violates "
        "Federal Rule of Civil Procedure 8(b). Plaintiff respectfully requests that the Court strike the "
        "Answer in its entirety with leave to answer the operative FAC (Dkt. 6) within fourteen (14) days, "
        "or, in the alternative, strike the thirty-three affirmative defenses and direct compliance with Rule 8(b).",
    ),
    (
        "HEADER",
        "II. RELEVANT PROCEDURAL BACKGROUND",
    ),
    (
        "PARA",
        "On August 10, 2026, Plaintiff filed his original Complaint for Damages and for Declaratory and "
        "Injunctive Relief under 42 U.S.C. § 1983 and 28 U.S.C. §§ 2201-2202 (Dkt. 1). Summonses were issued "
        "the same day as to Defendant Diana Candelaria, individually, and Defendant Steve Gordon, Director of "
        "the California DMV, in his official capacity (Dkt. 2).",
    ),
    (
        "PARA",
        "On August 14, 2026, the Sacramento County Sheriff personally served both Defendants with the summons "
        "at the DMV Legal Affairs Division in Sacramento. That same day, Plaintiff filed a First Amended Complaint "
        "(Dkt. 5).",
    ),
    (
        "PARA",
        "On August 17, 2026, Plaintiff filed a conforming First Amended Complaint (Dkt. 6), which omitted an "
        "unverified citation and constitutes the operative complaint of record in this action. (See Matter 33 "
        "Docket, Dkt. 6.)",
    ),
    (
        "PARA",
        "On August 21, 2026, Plaintiff served a copy of the operative First Amended Complaint (Dkt. 6) on both "
        "Defendant Candelaria and Defendant Gordon by United States first-class mail deposited at San Jose, "
        "California, addressed to each Defendant at the DMV Legal Affairs Division, Mail Station C128, 2415 First "
        "Avenue, Sacramento, CA 95818. A formal Proof of Service certifying this service was executed on August "
        "21, 2026. (See Proof of Service, Dkt. 6 Mailed to Candelaria and Gordon, Aug. 21, 2026.)",
    ),
    (
        "PARA",
        "On August 24, 2026, to ensure that the docket clearly reflected which pleading was operative before any "
        "responsive pleading or motion was due, Plaintiff filed and served a formal 'Notice Identifying Operative "
        "First Amended Complaint' (Dkt. 8). That Notice expressly advised the Court and all parties that:",
    ),
    (
        "LIST_ITEM",
        "'3. The operative pleading of record is the First Amended Complaint filed August 17, 2026 as Dkt. 6. "
        "The earlier First Amended Complaint filed August 14, 2026 as Dkt. 5 is superseded in full and is of no "
        "further force or effect. See Fed. R. Civ. P. 15(a); Lacey v. Maricopa County, 693 F.3d 896, 927 (9th "
        "Cir. 2012) (en banc). 4. This Notice does not amend, supplement, or withdraw any allegation in Dkt. 6. "
        "It is filed only to identify the operative pleading clearly on the face of the docket before any responsive "
        "pleading or Rule 12 motion.' (Dkt. 8 at 1-2.)",
    ),
    (
        "PARA",
        "On September 4, 2026, Defendants filed their Answer (ECF No. 11). Despite having been served with the "
        "FAC two weeks earlier, and despite the explicit August 24 Notice on the docket, Defendants answered the "
        "superseded August 10 Complaint (Dkt. 1). Paragraph 1 of the Answer states unequivocally:",
    ),
    (
        "LIST_ITEM",
        "'Defendants DIANA CANDELARIA, in her individual capacity, and STEVE GORDON, Director of the California "
        "Department of Motor Vehicles, in his official capacity (collectively referred to as \"Defendants\"), "
        "answer Plaintiff Brendan Ngwa Nforbi's COMPLAINT FOR DAMAGES AND FOR DECLARATORY AND INJUNCTIVE RELIEF "
        "(\"Complaint\") (Document 1) filed on August 10, 2026, as set forth below.' (ECF No. 11 at 1:26-28.)",
    ),
    (
        "PARA",
        "Defendants did not answer the operative First Amended Complaint (Dkt. 6). Plaintiff now timely moves "
        "to strike the Answer pursuant to Federal Rule of Civil Procedure 12(f).",
    ),
    (
        "HEADER",
        "III. LEGAL STANDARD UNDER FED. R. CIV. P. 12(f)",
    ),
    (
        "PARA",
        "Federal Rule of Civil Procedure 12(f) provides that the court 'may strike from a pleading an insufficient "
        "defense or any redundant, immaterial, impertinent, or scandalous matter.' Fed. R. Civ. P. 12(f). The "
        "purpose of a motion to strike under Rule 12(f) is to 'avoid the expenditure of time and money that must "
        "arise from litigating spurious issues by dispensing with those issues prior to trial.' <<i:Whittlestone, "
        "Inc. v. Handi-Craft Co.>>, 618 F.3d 970, 973 (9th Cir. 2010); <<i:Fantasy, Inc. v. Fogerty>>, 984 F.2d "
        "1524, 1527 (9th Cir. 1993), rev'd on other grounds, 510 U.S. 517 (1994).",
    ),
    (
        "PARA",
        "Matter is 'immaterial' if it has no essential or important relationship to the claim for relief or the "
        "defenses being pleaded, and 'impertinent' if it consists of statements that do not pertain, and are not "
        "necessary, to the issues in question. <<i:Fantasy, Inc.>>, 984 F.2d at 1527. An affirmative defense is "
        "'insufficient' if it fails as a matter of law or fails to satisfy federal pleading standards. <<i:Barnes "
        "v. AT&T Pension Benefit Plan>>, 718 F. Supp. 2d 1167, 1171 (N.D. Cal. 2010).",
    ),
    (
        "PARA",
        "Under Rule 12(f)(2), a party must make a motion to strike 'within 21 days after being served with the "
        "pleading.' Here, Defendants served their Answer electronically on September 4, 2026. This Motion is filed "
        "on September 5, 2026, well within the 21-day statutory window.",
    ),
    (
        "HEADER",
        "IV. ARGUMENT",
    ),
    (
        "SUBHEAD",
        "A. The Entire Answer Must Be Stricken Because It Responds to a Superseded\n"
        "Complaint and Is a Procedural Nullity",
    ),
    (
        "PARA",
        "It is black-letter law in the Ninth Circuit that 'an amended complaint supersedes the original, the latter "
        "being treated thereafter as non-existent.' <<i:Ramirez v. County of San Bernardino>>, 806 F.3d 1002, 1008 "
        "(9th Cir. 2015); accord <<i:Hal Roach Studios, Inc. v. Richard Feiner & Co.>>, 896 F.2d 1542, 1546 (9th "
        "Cir. 1990); <<i:Lacey v. Maricopa County>>, 693 F.3d 896, 927 (9th Cir. 2012) (en banc) ('the general rule "
        "is that an amended complaint supersedes the original complaint and renders it without legal effect'); "
        "<<i:Ferdik v. Bonzelet>>, 963 F.2d 1258, 1262 (9th Cir. 1992).",
    ),
    (
        "PARA",
        "When an amended complaint is filed, the original complaint becomes <<i:functus officio>>—it ceases to "
        "perform any function in the case. As a direct consequence, an answer directed to a superseded complaint "
        "responds to a legal nullity. It fails to join issue on the operative complaint as mandated by Federal Rule "
        "of Civil Procedure 8(b), addresses factual allegations and legal theories that may have been altered or "
        "superseded, and leaves the operative First Amended Complaint completely unanswered.",
    ),
    (
        "PARA",
        "Because an amended complaint renders the original non-existent, an answer directed only to the "
        "superseded pleading fails to join issue on the operative claims. The Ninth Circuit's supersession "
        "rule in <<i:Ramirez>>, <<i:Hal Roach Studios>>, <<i:Lacey>>, and <<i:Ferdik>> leaves no room for an "
        "answer that, on its face, addresses only Dkt. 1. That answer is redundant of a pleading that no longer "
        "exists, immaterial to the operative controversy, and properly stricken under Rule 12(f).",
    ),
    (
        "PARA",
        "Here, Defendants' Answer explicitly states on page 1 that it answers the 'Complaint (Document 1) filed on "
        "August 10, 2026.' (ECF No. 11 at 1:28.) It responds to paragraphs 1 through 136 of Dkt. 1. But Dkt. 1 was "
        "superseded on August 17, 2026 by Dkt. 6. Defendants were served with Dkt. 6 on August 21, 2026, and "
        "Plaintiff filed a formal Notice of Operative FAC on August 24, 2026 (Dkt. 8). There is no ambiguity on the "
        "docket. Defendants simply answered the wrong pleading.",
    ),
    (
        "PARA",
        "Allowing an answer to a superseded complaint to stand creates severe confusion, clutter, and prejudice. "
        "The parties cannot conduct discovery or frame pretrial motions on an answer responding to non-operative "
        "allegations. The entire Answer should be stricken under Rule 12(f) as redundant, immaterial, and "
        "procedurally improper, with leave granted for Defendants to file an answer addressing the operative First "
        "Amended Complaint (Dkt. 6) within fourteen (14) days.",
    ),
    (
        "SUBHEAD",
        "B. In the Alternative, Defendants' Thirty-Three Affirmative Defenses Must Be Stricken",
    ),
    (
        "PARA",
        "Should the Court decline to strike the Answer in its entirety, Plaintiff moves in the alternative to strike "
        "all thirty-three (33) Affirmative Defenses asserted in the Answer (ECF No. 11 at 32:20-35:20). Every single "
        "defense is fatally defective under governing law.",
    ),
    (
        "SUBHEAD",
        "1. The Pleading Standard for Affirmative Defenses in the Northern District of California",
    ),
    (
        "PARA",
        "In the Northern District of California, courts overwhelmingly apply the plausibility standard of <<i:Bell "
        "Atl. Corp. v. Twombly>>, 550 U.S. 544 (2007), and <<i:Ashcroft v. Iqbal>>, 556 U.S. 662 (2009), to affirmative "
        "defenses. See, e.g., <<i:Barnes v. AT&T Pension Benefit Plan>>, 718 F. Supp. 2d 1167, 1171-72 (N.D. Cal. "
        "2010) (Patel, J.) ('While neither the Ninth Circuit nor the Supreme Court has addressed whether the "
        "Twombly-Iqbal standard applies to affirmative defenses, the vast majority of courts in this district have "
        "held that the Twombly-Iqbal standard does apply.'); <<i:Perez v. Gordon & Wong Law Group, P.C.>>, 2012 WL "
        "1029425, at *6-8 (N.D. Cal. Mar. 26, 2012) (Koh, J.) (applying <<i:Twombly>> and <<i:Iqbal>> to strike "
        "boilerplate affirmative defenses); <<i:CTF Dev., Inc. v. Penta Hospitality, LLC>>, 2009 WL 3517617, at *7-8 "
        "(N.D. Cal. Oct. 26, 2009) (Alsup, J.) ('Under Twombly and Iqbal, an affirmative defense must contain "
        "sufficient factual matter to state a defense that is plausible on its face.').",
    ),
    (
        "PARA",
        "Under this standard, a defendant must plead sufficient factual content to make the defense plausible, "
        "providing fair notice of the factual grounds upon which it rests. Even under the older 'fair notice' test "
        "articulated in <<i:Wyshak v. City Nat'l Bank>>, 607 F.2d 824, 827 (9th Cir. 1979), fair notice requires "
        "pointing to the specific facts connecting the defense to the claims, not merely reciting the legal title "
        "of a defense. Naked legal conclusions and bare statutory citations do not survive under either standard.",
    ),
    (
        "SUBHEAD",
        "2. Negative Defenses and Denials Disguised as Affirmative Defenses\n"
        "(Defenses 1, 2, 3, 4, 7, 25, 26)",
    ),
    (
        "PARA",
        "A defense that points out a defect in the plaintiff's prima facie case is not an affirmative defense. "
        "<<i:Zivkovic v. S. Cal. Edison Co.>>, 302 F.3d 1080, 1088 (9th Cir. 2002); <<i:Barnes>>, 718 F. Supp. 2d at "
        "1173-74. An affirmative defense admits the allegations of the complaint but avoids liability by asserting an "
        "independent legal excuse. See <<i:Gomez v. Toledo>>, 446 U.S. 635, 640 (1980).",
    ),
    (
        "PARA",
        "Defenses 1 (lack of standing), 2 (lack of subject matter jurisdiction), 3 (failure to state sufficient "
        "facts), 4 (failure to state a claim), and 7 (ripeness / lack of justiciable controversy) assert defects in "
        "Plaintiff's prima facie case, not affirmative defenses. They belong in a Rule 12(b) motion or operate as "
        "general denials. As Judge Patel explained in <<i:Barnes>>, 'Failure to state a claim is not a proper "
        "affirmative defense but, rather, asserts a defect in [plaintiff's] prima facie case.' 718 F. Supp. 2d at "
        "1174. Similarly, Defenses 25 (damages not caused by Defendants / breach of Plaintiff's duty) and 26 (causation "
        "by third parties) merely negate the causation element of Plaintiff's Section 1983 claim. They are negative "
        "defenses and should be stricken.",
    ),
    (
        "SUBHEAD",
        "3. State Tort Immunities and Government Claims Act Provisions Cannot Bar\n"
        "Federal § 1983 Claims (Defenses 9, 10, 14, 28)",
    ),
    (
        "PARA",
        "Defenses 9 and 10 allege failure to exhaust administrative remedies under the California Government Claims "
        "Act and failure to state claims presented to the Department of General Services (each trailing off with the "
        "uncompleted placeholder 'xxx'). Under binding Supreme Court precedent, state notice-of-claim and government "
        "claims presentation requirements DO NOT APPLY to federal civil rights claims under 42 U.S.C. § 1983. "
        "<<i:Felder v. Casey>>, 487 U.S. 131, 140-41 (1988) ('a state law that condition[s] the right of recovery upon "
        "compliance with a notice-of-claim requirement cannot be applied to an action brought under § 1983'). "
        "Plaintiff asserts federal claims under Section 1983, not state-law tort claims. These defenses are legally "
        "insufficient as a matter of law.",
    ),
    (
        "PARA",
        "Defense 14 asserts a kitchen-sink recitation of California Government Code immunities (Gov. Code §§ 815, "
        "815.2(b), 815.3, 818, 818.2, 818.8, 820, 820.2, 820.4, 820.6, 820.8, 821, 821.6, 822.2, 950.2, and Civil "
        "Code § 47). It is elementary that state statutory immunities cannot shield state officials from liability "
        "for violations of federal constitutional rights under 42 U.S.C. § 1983. <<i:Martinez v. California>>, 444 "
        "U.S. 277, 284 n.8 (1980) ('Conduct by persons acting under color of state law which is wrongful under 42 "
        "U.S.C. § 1983... cannot be immunized by state law.'); <<i:Wallis v. Spencer>>, 202 F.3d 1126, 1144 (9th Cir. "
        "2000) ('State immunity laws do not shield the defendants from § 1983 claims.'). Because Plaintiff asserts "
        "federal Section 1983 claims, state tort immunity statutes are entirely impertinent.",
    ),
    (
        "PARA",
        "Defense 28 asserts that violations of the California Constitution do not support damages claims under "
        "<<i:Katzberg v. Regents of Univ. of Cal.>>, 29 Cal. 4th 300 (2002). Plaintiff does not seek damages under the "
        "California Constitution. Plaintiff's damages claims arise exclusively under 42 U.S.C. § 1983 for violations "
        "of the Due Process Clause of the Fourteenth Amendment to the United States Constitution. Defense 28 is "
        "immaterial and impertinent.",
    ),
    (
        "SUBHEAD",
        "4. Factually and Legally Contradicted Constitutional Defenses (Defenses 11, 12, 13)",
    ),
    (
        "PARA",
        "Defense 12 claims that 'Plaintiff has no cause of action directly under the United States Constitution.' "
        "Plaintiff did not bring a direct cause of action under the Constitution; Plaintiff brought his claims under "
        "42 U.S.C. § 1983, the congressionally enacted vehicle for enforcing constitutional violations. Defense 12 "
        "is a straw man.",
    ),
    (
        "PARA",
        "Defense 13 asserts that state officials sued in their official capacity for damages are not 'persons' under "
        "§ 1983, citing <<i:Will v. Michigan Dept. of State Police>>, 491 U.S. 58 (1989). But Plaintiff DID NOT sue "
        "Director Steve Gordon for damages in his official capacity. Director Gordon is sued strictly in his official "
        "capacity for prospective declaratory and injunctive relief under <<i:Ex parte Young>>, 209 U.S. 123 (1908). "
        "The Supreme Court in <<i:Will>> explicitly reaffirmed that 'a state official in his or her official capacity, "
        "when sued for injunctive relief, would be a person under § 1983 because official-capacity actions for "
        "prospective relief are not treated as actions against the State.' 491 U.S. at 71 n.10. And Defendant Diana "
        "Candelaria is sued for damages in her INDIVIDUAL capacity, where <<i:Will>> does not apply. <<i:Hafer v. "
        "Melo>>, 502 U.S. 21, 31 (1991) ('state officials, sued in their individual capacities, are \"persons\" "
        "within the meaning of § 1983'). Defense 13 is legally meritless and mischaracterizes the complaint.",
    ),
    (
        "PARA",
        "Defense 11 asserts Eleventh Amendment immunity. Under <<i:Ex parte Young>>, 209 U.S. at 159-60, and "
        "<<i:Pennhurst State Sch. & Hosp. v. Halderman>>, 465 U.S. 89, 102-03 (1984), the Eleventh Amendment does "
        "not bar suits against state officials in their official capacity seeking prospective equitable relief to end "
        "a continuing violation of federal law. Nor does the Eleventh Amendment bar Section 1983 individual-capacity "
        "damages actions against state officers. <<i:Hafer>>, 502 U.S. at 30-31. Defense 11 is insufficient as a "
        "matter of law.",
    ),
    (
        "SUBHEAD",
        "5. DMV Driver Safety Hearing Officers Lack Quasi-Judicial Absolute\n"
        "Immunity (Defense 31)",
    ),
    (
        "PARA",
        "Defense 31 claims that Defendants are entitled to absolute quasi-judicial immunity under <<i:Butz v. "
        "Economou>>, 438 U.S. 478 (1978). Under <<i:Butz>> and its progeny, absolute immunity extends only to "
        "administrative officials whose role is functionally comparable to that of a judge and who operate within a "
        "system featuring comprehensive institutional safeguards against bias and agency control. <<i:Cleavinger v. "
        "Saxner>>, 474 U.S. 193, 201-02 (1985).",
    ),
    (
        "PARA",
        "California DMV Driver Safety Hearing Officers are executive branch civil-service employees who lack the "
        "independence of Article III judges or administrative law judges under the Administrative Procedure Act. Under "
        "California Vehicle Code §§ 14100 et seq., DMV hearing officers combine investigatory, prosecutorial, and "
        "adjudicative roles: they collect the DMV's enforcement evidence, introduce it at the hearing, rule on their "
        "own objections, cross-examine the licensee, and render the decision. They are subordinate employees of the "
        "very enforcement agency whose administrative action is at issue. That combined investigatory, prosecutorial, "
        "and adjudicative role is not the functionally comparable judicial office <<i:Butz>> and <<i:Cleavinger>> "
        "require. Executive hearing officers are shielded, at most, by qualified immunity, not absolute "
        "quasi-judicial immunity. Defense 31 is legally insufficient.",
    ),
    (
        "SUBHEAD",
        "6. Irrelevant Employment Discrimination Statute of Limitations (Defense 16)",
    ),
    (
        "PARA",
        "Defense 16 asserts that Plaintiff's claims are barred by 'the applicable statute of limitations, including but "
        "not limited to, 42 U.S.C. § 2000e-5(f)(1), and sections 335.1 and 342 of the California Code of Civil Procedure. "
        "xx' (ECF No. 11 at 33:23-26).",
    ),
    (
        "PARA",
        "42 U.S.C. § 2000e-5(f)(1) is the statute of limitations for Title VII employment discrimination claims. This "
        "is an administrative driver's license suspension case under 42 U.S.C. § 1983; there are no Title VII claims "
        "in this action. Citing Title VII illustrates reckless copy-pasting of boilerplate defenses. Furthermore, the "
        "applicable statute of limitations for Section 1983 actions arising in California is two years. Cal. Code Civ. "
        "Proc. § 335.1. The underlying APS hearing occurred on January 24, 2025, and Defendant Candelaria's decision "
        "issued on February 11, 2025. This action was filed on August 10, 2026, roughly eighteen months later—well "
        "within the two-year period. Defense 16 is legally baseless.",
    ),
    (
        "SUBHEAD",
        "7. Improper 'Reservation of Rights' (Defense 33)",
    ),
    (
        "PARA",
        "Defense 33 purports to 'reserve the right to amend this answer to assert additional defenses and/or supplement, "
        "alter, and/or change this answer as may be warranted by the revelation of information during discovery.' (ECF "
        "No. 11 at 35:17-20.)",
    ),
    (
        "PARA",
        "A reservation of rights is not a valid affirmative defense. Under Federal Rule of Civil Procedure 15, a party "
        "may amend its pleading only by leave of court or with the opposing party's written consent. A party cannot "
        "circumvent Rule 15 by reserving rights in an answer. This District strikes such reservations. "
        "<<i:Perez>>, 2012 WL 1029425, at *11 (Koh, J.) (striking a reservation of rights to add affirmative "
        "defenses). Defense 33 must be stricken.",
    ),
    (
        "SUBHEAD",
        "8. Pure Boilerplate Lacking Any Factual Allegations\n"
        "(Defenses 5, 6, 8, 15, 17, 18, 19, 20, 21, 22, 23, 24, 27, 29, 30, 32)",
    ),
    (
        "PARA",
        "The remaining defenses are one-sentence legal conclusions devoid of any factual content, in blatant violation "
        "of <<i:Twombly>>, <<i:Iqbal>>, and <<i:Barnes>>. For example:",
    ),
    (
        "LIST_ITEM",
        "- Defense 8 asserts that 'Venue does not lie in this Court.' Defendants provide zero facts explaining why venue "
        "is improper in the Northern District of California. The underlying events occurred on Interstate 580 in "
        "Livermore, Alameda County, which is located squarely within the Northern District of California. 28 U.S.C. "
        "§ 1391(b)(2); Civil L.R. 3-2(d). Venue is manifestly proper.",
    ),
    (
        "LIST_ITEM",
        "- Defense 23 asserts 'res judicata and/or collateral estoppel because Plaintiff failed to exhaust available "
        "judicial remedies.' Defendants do not identify any prior judgment, any issue preclusion, or any unexhausted "
        "remedy. In any event, exhaustion of state judicial remedies is not a prerequisite to a Section 1983 claim. "
        "<<i:Patsy v. Bd. of Regents>>, 457 U.S. 496, 516 (1982).",
    ),
    (
        "LIST_ITEM",
        "- Defenses 5 (laches), 6 (unclean hands), 15 (good faith / discretion), 17 (after-acquired evidence), 18 "
        "(required by law), 19 (failure to mitigate / speculative), 20 (comparative fault), 21 (estoppel and waiver), "
        "22 (judicial estoppel), 24 (consent), 27 (indispensable parties), 29 (adequate remedy at law), 30 "
        "(impossibility), and 32 (qualified immunity) each consist of a single sentence reciting the title of a doctrine "
        "without a syllable of supporting factual narrative.",
    ),
    (
        "PARA",
        "Pleading in this fashion forces Plaintiff and the Court to guess what facts, if any, Defendants believe support "
        "these thirty-three defenses. Under <<i:Barnes>>, 718 F. Supp. 2d at 1172, and <<i:Perez>>, 2012 WL 1029425, "
        "at *8, these unadorned legal boilerplate defenses must be stricken.",
    ),
    (
        "SUBHEAD",
        "9. Glaring Drafting Artifacts ('xxx', 'xx') Confirm Unvetted Template Pleading",
    ),
    (
        "PARA",
        "The unvetted, assembly-line nature of Defendants' affirmative defenses is laid bare on the face of the pleading "
        "itself:",
    ),
    (
        "LIST_ITEM",
        "- Defense 9: '...because Plaintiff failed to exhaust appropriate administrative remedies under California's "
        "Government Claims Act and xxx' (ECF No. 11 at 32:27-33:1).",
    ),
    (
        "LIST_ITEM",
        "- Defense 10: '...stated in the administrative claims filed with the California Government Claims Program in "
        "the Department of General Services. xxx' (ECF No. 11 at 33:4-7).",
    ),
    (
        "LIST_ITEM",
        "- Defense 16: '...sections 335.1 and 342 of the California Code of Civil Procedure. xx' (ECF No. 11 at 33:25-26).",
    ),
    (
        "PARA",
        "The presence of literal template placeholders ('xxx' and 'xx') demonstrates beyond debate that counsel copied "
        "a stock template, failed to finish drafting, and filed the document without even proofreading it. Such careless "
        "pleading degrades the integrity of court filings and underscores why the affirmative defenses should be stricken.",
    ),
    (
        "SUBHEAD",
        "C. Defendants' Systematic Evasive Denials Violate Fed. R. Civ. P. 8(b)",
    ),
    (
        "PARA",
        "Throughout paragraphs 1 through 136 of the Answer, Defendants deploy a canned, evasive formula:",
    ),
    (
        "LIST_ITEM",
        "'Paragraph [X] contains allegations to which no response is required because the allegations purport to be "
        "statements, summaries, or conclusions of law; or characterizations of Plaintiff's legal contentions based on "
        "those statements, summaries, or conclusions of law. To the extent that a response to those allegations is "
        "required, Defendants deny those allegations on the basis that the law speaks for itself and is the best evidence "
        "of its content. Defendants deny all other factual allegations in paragraph [X] not expressly admitted here.' "
        "(See, e.g., ECF No. 11 at ¶¶ 1, 2, 4-136.)",
    ),
    (
        "PARA",
        "Under Federal Rule of Civil Procedure 8(b)(1)(B), a party responding to a pleading must 'admit or deny the "
        "allegations asserted against it by an opposing party.' Rule 8(b) provides only three permissible responses: "
        "(1) an admission, (2) a denial, or (3) a statement that the party lacks knowledge or information sufficient "
        "to form a belief. Responding that an allegation 'purports to be a conclusion of law' or that 'the law speaks for "
        "itself' is an improper evasion that violates Rule 8(b). See <<i:State Farm Mut. Auto. Ins. Co. v. "
        "Riley>>, 199 F.R.D. 276, 278 (N.D. Ill. 2001) (explaining that responses stating 'the document speaks for "
        "itself' or claiming an allegation is a 'legal conclusion' are improper evasions under Rule 8(b)); <<i:Barnes>>, "
        "718 F. Supp. 2d at 1170. When Defendants are ordered to answer the operative FAC (Dkt. 6), the Court should "
        "direct them to comply strictly with Rule 8(b).",
    ),
    (
        "HEADER",
        "V. CONCLUSION",
    ),
    (
        "PARA",
        "For the foregoing reasons, Plaintiff respectfully requests that the Court:",
    ),
    (
        "LIST_ITEM",
        "1. Grant this Motion and strike Defendants' Answer (ECF No. 11) in its entirety pursuant to Federal Rule of "
        "Civil Procedure 12(f);",
    ),
    (
        "LIST_ITEM",
        "2. In the alternative, strike all thirty-three (33) Affirmative Defenses asserted in Defendants' Answer, or "
        "such defenses as the Court finds legally insufficient;",
    ),
    (
        "LIST_ITEM",
        "3. Order Defendants to file and serve an answer addressing the operative First Amended Complaint (Dkt. 6) "
        "within fourteen (14) days, in strict conformity with Federal Rule of Civil Procedure 8(b); and",
    ),
    (
        "LIST_ITEM",
        "4. Grant such other and further relief as the Court deems just and proper.",
    ),
]

ORDER_CONTENT: list[tuple[str, str]] = [
    (
        "HEADER",
        "[PROPOSED] ORDER GRANTING PLAINTIFF'S MOTION TO STRIKE\n"
        "DEFENDANTS' ANSWER (ECF NO. 11) PURSUANT TO FED. R. CIV. P. 12(f)",
    ),
    (
        "PARA",
        "Plaintiff Brendan Ngwa Nforbi's Motion to Strike Defendants' Answer (ECF No. 11) Pursuant to "
        "Federal Rule of Civil Procedure 12(f); or, in the Alternative, to Strike Affirmative Defenses, "
        "came on regularly for hearing before this Court.",
    ),
    (
        "PARA",
        "Having considered Plaintiff's Motion, the Memorandum of Points and Authorities, the Court's "
        "records and files in this action, and the arguments of the parties, and good cause appearing therefor, "
        "THE COURT FINDS AND ORDERS AS FOLLOWS:",
    ),
    (
        "LIST_ITEM",
        "1. Plaintiff's Motion to Strike is GRANTED.",
    ),
    (
        "LIST_ITEM",
        "2. Defendants Diana Candelaria and Steve Gordon's Answer (ECF No. 11), filed on September 4, 2026, "
        "is hereby STRICKEN in its entirety pursuant to Federal Rule of Civil Procedure 12(f), on the ground "
        "that it responds solely to Plaintiff's superseded original Complaint (Dkt. 1) rather than Plaintiff's "
        "operative First Amended Complaint (Dkt. 6), rendering it a procedural nullity, redundant, immaterial, "
        "and impertinent.",
    ),
    (
        "LIST_ITEM",
        "3. In the alternative, Defendants' thirty-three (33) Affirmative Defenses (ECF No. 11 at 32-35) "
        "are hereby STRICKEN as legally insufficient, impertinent, and failing to state plausible defenses "
        "under Federal Rules of Civil Procedure 8 and 12(f).",
    ),
    (
        "LIST_ITEM",
        "4. Defendants shall file and serve an answer addressing the operative First Amended Complaint "
        "(Dkt. 6) within fourteen (14) days of the date of this Order.",
    ),
    (
        "LIST_ITEM",
        "5. Any answer filed by Defendants shall strictly conform to Federal Rule of Civil Procedure 8(b), "
        "admitting or denying each allegation or stating lack of knowledge or information sufficient to form "
        "a belief, and shall not assert evasive boilerplate denials stating that 'the law speaks for itself.'",
    ),
    (
        "PARA",
        "IT IS SO ORDERED.",
    ),
]


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
    d.draw_caption_block(
        CAPTION_LEFT, right_caption, caption_size=9.5, tight_lh=12.5, boxed=True
    )
    d.blank_line()


def _signature(d: PleadingPaper, exec_date: str) -> None:
    d.ensure_space(6)
    d.write_line(f"Dated: {exec_date}")
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


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_wrapped(line, bold=True, first_indent=0, indent=0)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")


def motion_pos_fields(exec_date: str, mailed_from: str) -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGWA NFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "DIANA CANDELARIA, individually;",
            "STEVE GORDON, officially; and DOES 1-10",
        ],
        defendant_role="Defendants",
        case_number="3:26-cv-08272-LJC",
        title="PROOF OF SERVICE",
        service_date=exec_date,
        document_title=(
            "Plaintiff's Notice of Motion and Motion to Strike Defendants' Answer (ECF No. 11) "
            "Pursuant to Fed. R. Civ. P. 12(f); Memorandum of Points and Authorities; [Proposed] Order"
        ),
        mailing_location=mailed_from,
        recipients=SERVICE_RECIPIENTS,
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
        district_line=DISTRICT_NDCAL,
        signature_on_second_page=True,
    )


def append_pdfs(front: Path, back: Path, out: Path | None = None) -> Path:
    target = out or front
    assemble([front, back], target)
    return target


def build_motion_document(out: Path, exec_date: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    _header_block(d, CAPTION_RIGHT)
    _render_body(d, CONTENT)
    _signature(d, exec_date)
    d.save()
    return out


def build_proposed_order(out: Path, exec_date: str) -> Path:
    # exec_date kept for CLI parity with the motion; the order is signed only by the Court.
    _ = exec_date
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=ORDER_FOOTER)
    _header_block(d, ORDER_CAPTION_RIGHT)
    _render_body(d, ORDER_CONTENT)
    d.ensure_space(5)
    d.write_line("Dated: _______________, 2026")
    d.blank_line()
    d.write_line("___________________________________________")
    d.write_line("HON. LISA J. CISNEROS")
    d.write_line("United States Magistrate Judge")
    d.save()
    return out


def build_motion_proof_of_service(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    return build_proof_of_service(out, motion_pos_fields(exec_date, mailed_from))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date", default=DEFAULT_EXEC_DATE, help="Execution date for signature and POS"
    )
    parser.add_argument(
        "--mailed-from",
        default=DEFAULT_MAILED_FROM,
        help="City, State from which mail is deposited",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Destination path for primary motion PDF (with POS appended)",
    )
    parser.add_argument(
        "--order-out",
        type=Path,
        default=DEFAULT_ORDER_OUT,
        help="Destination path for standalone Proposed Order PDF",
    )
    parser.add_argument(
        "--pos-out",
        type=Path,
        default=DEFAULT_POS_OUT,
        help="Destination path for standalone Proof of Service PDF",
    )
    parser.add_argument(
        "--packet-out",
        type=Path,
        default=DEFAULT_PACKET_OUT,
        help="Destination path for full packet PDF (Motion + Proposed Order + POS)",
    )
    args = parser.parse_args()

    print(f"Building Motion to Strike for Matter 33 (Date: {args.date})...")

    # 1. Build the standalone Proof of Service PDF
    build_motion_proof_of_service(args.pos_out, args.date, args.mailed_from)
    print(f"  [+] Wrote Proof of Service: {args.pos_out}")

    # 2. Build the standalone Proposed Order PDF
    build_proposed_order(args.order_out, args.date)
    print(f"  [+] Wrote Proposed Order: {args.order_out}")

    # 3. Build the Motion (Notice + Memo of P&As) temporary PDF
    temp_motion_raw = args.out.with_name("tmp_motion_raw.pdf")
    build_motion_document(temp_motion_raw, args.date)
    print(f"  [+] Wrote Motion document: {temp_motion_raw}")

    # 4. Assemble primary filing: Motion + Proof of Service
    assemble([temp_motion_raw, args.pos_out], args.out)
    print(f"  [+] Wrote Primary Motion PDF with POS: {args.out}")

    # 5. Assemble full packet: Motion + Proposed Order + Proof of Service (Order placed before POS)
    assemble([temp_motion_raw, args.order_out, args.pos_out], args.packet_out)
    if temp_motion_raw.exists():
        temp_motion_raw.unlink()
    print(f"  [+] Wrote Full Filing Packet PDF: {args.packet_out}")

    # 6. Publish to short link
    pub = publish_short_link(args.out, SHORT_LINK_SLUG)
    print(f"  [+] Published short-link PDF to: {pub}")
    packet_pub = publish_short_link(args.packet_out, PACKET_SLUG)
    print(f"  [+] Published packet short-link PDF to: {packet_pub}")


if __name__ == "__main__":
    main()
