#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 35 â€” Verified Complaint for Damages and Injunctive and Declaratory Relief.

Ngwa Nforbi v. Ross Stores, Inc., et al.
Superior Court of California, County of Santa Clara.

Rendered on the shared California pleading-paper engine and signed with the
portfolio universal signature.

    python3 internal/scripts/matter35-verified-complaint.py [OUT_PDF]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pleading_paper import (  # noqa: E402
    CONTENT_LEFT,
    COURT_LINE1,
    PleadingPaper,
)
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-35"
    / "Verified Complaint - Ngwa Nforbi v Ross Stores Inc et al (Aug 26 2026).pdf"
)

DEFAULT_EXEC_DATE = "August 26, 2026"
COURT_LINE2 = "COUNTY OF SANTA CLARA"
FOOTER = (
    "VERIFIED COMPLAINT -- NGWA NFORBI v. ROSS STORES, INC., ET AL."
)

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
    ("ROSS STORES, INC., a Delaware", True, False),
    ("corporation; ROSS DRESS FOR LESS,", True, False),
    ("INC., a Virginia corporation;", True, False),
    ("DOE 1; DOE 2; and DOES 3 through", True, False),
    ("20, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. _________________", False, False),
    ("", False, False),
    ("VERIFIED COMPLAINT FOR", True, False),
    ("DAMAGES AND INJUNCTIVE", True, False),
    ("AND DECLARATORY RELIEF", True, False),
    ("", False, False),
    ("(1) Unruh Civil Rights Act", False, False),
    ("      (Civ. Code \u00a7\u00a7 51, 51.5, 52);", False, False),
    ("(2) False Imprisonment;", False, False),
    ("(3) Intentional Infliction of", False, False),
    ("      Emotional Distress;", False, False),
    ("(4) Negligent Hiring, Training,", False, False),
    ("      Retention & Supervision;", False, False),
    ("(5) Unfair Competition", False, False),
    ("      (Bus. & Prof. Code \u00a7 17200);", False, False),
    ("(6) Declaratory Relief", False, False),
    ("      (CCP \u00a7 1060)", False, False),
    ("", False, False),
    ("[Unlimited Civil \u2014 Amount", False, True),
    (" Exceeds $35,000]", False, True),
    ("[Jury Trial Demanded]", False, True),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

CONTENT = [
    ("PARA",
     "Plaintiff BRENDAN NGWA NFORBI (\"Plaintiff\") hereby alleges as follows:"),

    # I. INTRODUCTION
    ("HEADER", "I.\nINTRODUCTION"),
    ("PARA",
     "1. This is a case about who gets stopped. On August 25, 2026, Plaintiff\u2014a "
     "Black man\u2014walked into a Ross Dress for Less store in Sunnyvale, California, "
     "holding a Celsius energy drink he had purchased five minutes earlier at the "
     "Sprouts Farmers Market next door. He browsed the men's clothing section, found "
     "nothing he wanted, and walked toward the exit empty-handed. As he approached "
     "the door, a white female loss-prevention employee physically stepped in front "
     "of him, blocking his path, and demanded to know whether he had paid for the "
     "drink he was carrying. No one had seen him take anything. No theft had "
     "occurred. No alarm had sounded. The only reason for the stop was that "
     "Plaintiff is Black."),
    ("PARA",
     "2. This is not a case about a slur. It is a case about a retail practice known "
     "as \"consumer racial profiling\" or \"shopping while Black\"\u2014the selective "
     "detention of Black customers based on race rather than evidence. Defendants' "
     "loss-prevention employee did not ask Plaintiff for a receipt, did not search "
     "him, did not recover any stolen merchandise, and did not call the police, "
     "because there was no basis for any of those actions. She simply blocked his "
     "exit, accused him by implication, and asserted, \"I'm allowed to do that.\""),
    ("PARA",
     "3. The Unruh Civil Rights Act guarantees every person the right to enter a "
     "business establishment, decline to buy anything, and leave on the same terms "
     "as every other customer. Defendants violated that right. They denied Plaintiff "
     "the full and equal accommodations, advantages, facilities, privileges, and "
     "services of their store because of his race. They falsely imprisoned him. "
     "They intentionally inflicted emotional distress. And they did so pursuant to "
     "loss-prevention practices that have not been adequately trained, supervised, "
     "or corrected."),
    ("PARA",
     "4. Plaintiff brings this action to vindicate his civil rights, to obtain "
     "redress for the harm he suffered, and to secure injunctive relief requiring "
     "Defendants to abandon racially discriminatory loss-prevention practices at "
     "their Sunnyvale store and throughout California."),

    # II. PARTIES
    ("HEADER", "II.\nPARTIES"),
    ("PARA",
     "5. Plaintiff BRENDAN NGWA NFORBI is, and at all relevant times was, a resident "
     "of the State of California. Plaintiff is a Black man. Plaintiff may be "
     "contacted at telephone number (209) 801-4442 and email address "
     "bnn.cdl@gmail.com."),
    ("PARA",
     "6. Defendant ROSS STORES, INC. is a corporation organized under the laws of "
     "the State of Delaware, qualified to transact business in California, with "
     "principal executive offices at 5130 Hacienda Drive, Dublin, California 94568. "
     "Ross Stores, Inc. originally incorporated in California in 1957 and "
     "reincorporated in Delaware in 1989. Its California foreign-qualification "
     "record has been identified in public business-entity databases under "
     "California Secretary of State State ID 01642535."),
    ("PARA",
     "7. Defendant ROSS DRESS FOR LESS, INC. is a corporation organized under the "
     "laws of the Commonwealth of Virginia, qualified to transact business in "
     "California, with principal executive offices at 5130 Hacienda Drive, Dublin, "
     "California 94568. Public California business-entity records identify Ross "
     "Dress for Less, Inc. as a stock corporation formed in Virginia, California "
     "document number 2642531, filed March 15, 2004, status active. Ross Dress for "
     "Less, Inc. owns, operates, staffs, and/or controls the Sunnyvale Store."),
    ("PARA",
     "8. ROSS STORES, INC. and ROSS DRESS FOR LESS, INC. are referred to "
     "collectively as the \"Ross Defendants\" or the \"Corporate Defendants.\""),
    ("PARA",
     "9. On information and belief, the currently designated agent for service of "
     "process in California for one or both Corporate Defendants is C T Corporation "
     "System, 330 North Brand Boulevard, Suite 700, Glendale, California 91203. "
     "Plaintiff will serve each Corporate Defendant through the agent listed on the "
     "California Secretary of State record as of the date of service."),
    ("PARA",
     "10. Defendant DOE 1 is the individual who blocked Plaintiff's exit from the "
     "Sunnyvale Store on August 25, 2026. DOE 1 is a white woman of approximately "
     "55 years of age who was acting as loss-prevention or security personnel for "
     "the Ross Defendants at the Sunnyvale Store. Her true name is presently "
     "unknown to Plaintiff."),
    ("PARA",
     "11. Defendant DOE 2 is the cashier who was present during the detention. "
     "DOE 2 is a white woman who was wearing a Ross employee shirt and was working "
     "at the Sunnyvale Store on August 25, 2026. Her true name is presently "
     "unknown to Plaintiff."),
    ("PARA",
     "12. The true names and capacities, whether individual, corporate, associate, "
     "or otherwise, of Defendants DOES 1 through 20, inclusive, are unknown to "
     "Plaintiff, who therefore sues those Defendants by fictitious names pursuant "
     "to Code of Civil Procedure section 474. Plaintiff will seek leave of Court "
     "to amend this Complaint to allege their true names and capacities when "
     "ascertained."),
    ("PARA",
     "13. Plaintiff is informed and believes, and on that basis alleges, that each "
     "Defendant sued herein as a DOE is legally responsible in some manner for the "
     "events and occurrences alleged herein and proximately caused the injuries "
     "and damages alleged herein."),
    ("PARA",
     "14. Plaintiff is informed and believes, and on that basis alleges, that at "
     "all relevant times each Defendant was the agent, servant, employee, partner, "
     "joint venturer, co-conspirator, and/or representative of each of the "
     "remaining Defendants, and in doing the things alleged herein was acting "
     "within the course and scope of that relationship, and with the knowledge, "
     "permission, consent, authorization, and/or ratification of each of the "
     "remaining Defendants."),
    ("PARA",
     "15. Plaintiff is informed and believes, and on that basis alleges, that "
     "DOE 1 and DOE 2 were at all relevant times employees or agents of the "
     "Corporate Defendants, were on duty at the Sunnyvale Store, were performing "
     "the duties for which they were hired, and were acting within the course and "
     "scope of their employment or agency."),
    ("PARA",
     "16. The Corporate Defendants are therefore vicariously liable for the acts "
     "and omissions of DOE 1 and DOE 2 under the doctrine of respondeat superior."),
    ("PARA",
     "17. Plaintiff is further informed and believes, and on that basis alleges, "
     "that the Corporate Defendants authorized, directed, ratified, and/or adopted "
     "the conduct of DOE 1 and DOE 2 by promulgating, maintaining, tolerating, and "
     "failing to correct loss-prevention practices at the Sunnyvale Store that "
     "produce the race-based selection of customers for detention described "
     "herein."),
    ("PARA",
     "18. Plaintiff is informed and believes, and on that basis alleges, that "
     "ROSS STORES, INC. and ROSS DRESS FOR LESS, INC. operate as a single, "
     "integrated retail enterprise; that there exists such a unity of interest and "
     "ownership between them that separate personalities do not in reality exist "
     "with respect to the operation, staffing, and loss-prevention practices of "
     "the Sunnyvale Store; and that ROSS STORES, INC. establishes, approves, and "
     "controls the loss-prevention policies, training materials, and personnel "
     "practices applied at the Sunnyvale Store. Adherence to the fiction of "
     "separate corporate existence would sanction an inequitable result."),

    # III. JURISDICTION AND VENUE
    ("HEADER", "III.\nJURISDICTION AND VENUE"),
    ("PARA",
     "19. This Court has subject matter jurisdiction over this action pursuant to "
     "Article VI, section 10 of the California Constitution and Code of Civil "
     "Procedure section 410.10."),
    ("PARA",
     "20. This action is properly designated an unlimited civil case under Code of "
     "Civil Procedure sections 85 and 88 because the amount in controversy exceeds "
     "thirty-five thousand dollars ($35,000), exclusive of interest and costs. "
     "Plaintiff seeks actual damages, statutory damages and up to treble damages "
     "under Civil Code section 52(a), damages for emotional distress, punitive "
     "damages, injunctive and declaratory relief, and attorney's fees and costs."),
    ("PARA",
     "21. This Court has personal jurisdiction over the Corporate Defendants "
     "because they are qualified to do business in California, maintain principal "
     "executive offices in California, operate retail stores throughout California "
     "including the Sunnyvale Store, and committed the acts complained of in "
     "California."),
    ("PARA",
     "22. Venue is proper in the County of Santa Clara pursuant to Code of Civil "
     "Procedure sections 395 and 395.5 because the injury occurred in this County, "
     "the liabilities alleged arose in this County, and the Corporate Defendants "
     "conduct business in this County. The Sunnyvale Store is located at 119 E. El "
     "Camino Real, Sunnyvale, California 94087, within the County of Santa Clara."),

    # IV. FACTUAL ALLEGATIONS
    ("HEADER", "IV.\nFACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. Plaintiff Purchases a Beverage at Sprouts Farmers Market"),
    ("PARA",
     "23. On August 25, 2026, at approximately 8:45 p.m., Plaintiff entered "
     "Sprouts Farmers Market located at 111 E. El Camino Real, Sunnyvale, "
     "California 94087."),
    ("PARA",
     "24. Plaintiff selected a Celsius brand energy drink from the refrigerated "
     "section."),
    ("PARA",
     "25. Plaintiff proceeded to the checkout counter and paid for the beverage."),
    ("PARA",
     "26. Plaintiff received and retained the original register receipt. The "
     "receipt reflects a transaction time of 8:45 p.m. on August 25, 2026."),
    ("PARA",
     "27. Plaintiff will produce that receipt in this litigation. It may be "
     "attached as Exhibit A to an amended pleading or offered at trial. Plaintiff "
     "does not attach the original to this initial Complaint in order to preserve "
     "it."),
    ("PARA",
     "28. Sprouts Farmers Market is located immediately adjacent to the Sunnyvale "
     "Store at 119 E. El Camino Real, approximately 100 feet away. The two stores "
     "share a parking lot and are directly next to one another."),

    ("SUBHEAD", "B. Plaintiff Enters the Ross Store Holding the Beverage in Open View"),
    ("PARA",
     "29. At approximately 8:50 p.m. on August 25, 2026\u2014approximately five "
     "minutes after completing his purchase at Sprouts\u2014Plaintiff entered the "
     "Sunnyvale Store."),
    ("PARA",
     "30. Plaintiff entered the Sunnyvale Store already holding the Celsius drink "
     "in his right hand."),
    ("PARA",
     "31. The drink was in Plaintiff's open hand and in plain view at the moment "
     "he crossed the threshold of the Sunnyvale Store."),
    ("PARA",
     "32. The drink was a brightly colored can, easily visible from any angle."),
    ("PARA",
     "33. Plaintiff did not conceal the drink. He did not place it in a bag, a "
     "pocket, a purse, or any container."),
    ("PARA",
     "34. Plaintiff's possession of the beverage was therefore visible to any "
     "Ross employee positioned near the store entrance, including any "
     "loss-prevention personnel who may have been monitoring the entrance."),
    ("PARA",
     "35. Upon information and belief, Defendants maintain surveillance cameras "
     "at the entrance of the Sunnyvale Store that captured Plaintiff entering the "
     "store holding the beverage."),

    ("SUBHEAD", "C. Plaintiff Shops, Buys Nothing, and Takes Nothing"),
    ("PARA",
     "36. Once inside, Plaintiff walked through the store to the men's clothing "
     "section."),
    ("PARA",
     "37. Plaintiff looked at various items of men's clothing, including shirts, "
     "pants, and jackets."),
    ("PARA",
     "38. Plaintiff considered purchasing clothing but determined that the prices "
     "were higher than he was willing to pay."),
    ("PARA",
     "39. At no time did Plaintiff select any Ross merchandise for purchase or "
     "attempted purchase."),
    ("PARA",
     "40. At no time did Plaintiff conceal any Ross merchandise."),
    ("PARA",
     "41. At no time did Plaintiff remove any Ross merchandise from any shelf, "
     "rack, hanger, or display for the purpose of taking it."),
    ("PARA",
     "42. At no time did Plaintiff place any Ross merchandise in his pockets, in "
     "a bag, or on his person."),
    ("PARA",
     "43. Throughout his time in the Sunnyvale Store, the Celsius drink remained "
     "in Plaintiff's hand, in plain view."),
    ("PARA",
     "44. Plaintiff then decided to leave without making a purchase, as any "
     "customer is entitled to do."),

    ("SUBHEAD", "D. The Detention"),
    ("PARA",
     "45. At approximately 9:00 p.m., Plaintiff walked toward the exit of the "
     "Sunnyvale Store."),
    ("PARA",
     "46. As he approached the exit, DOE 1, a white female loss-prevention "
     "employee of approximately 55 years of age, physically stepped directly in "
     "front of Plaintiff."),
    ("PARA",
     "47. DOE 1 positioned her body directly in Plaintiff's path, blocking the "
     "exit."),
    ("PARA",
     "48. DOE 1 did not stand to the side and speak to Plaintiff. She did not "
     "gesture for him to stop. She physically interposed herself between Plaintiff "
     "and the only exit available to him."),
    ("PARA",
     "49. DOE 1's physical positioning prevented Plaintiff from leaving the "
     "store."),
    ("PARA",
     "50. DOE 1 did not touch Plaintiff. She did not need to. Her physical "
     "interposition between Plaintiff and the exit had the intended effect and "
     "actual effect of stopping him and preventing him from leaving."),
    ("PARA",
     "51. A reasonable person in Plaintiff's position would not have believed he "
     "was free to walk around DOE 1 and out the door."),
    ("PARA",
     "52. Plaintiff did not consent to being stopped or detained."),
    ("PARA",
     "53. Plaintiff was conscious of the confinement at the time it occurred."),
    ("PARA",
     "54. The detention lasted approximately three minutes."),

    ("SUBHEAD", "E. The Confrontation"),
    ("PARA",
     "55. DOE 1 asked Plaintiff: \"Did you pay for that drink?\""),
    ("PARA",
     "56. Plaintiff responded by asking: \"Do you people sell Celsius drinks "
     "here?\""),
    ("PARA",
     "57. DOE 1 answered: \"Yeah, sometimes.\""),
    ("PARA",
     "58. DOE 1's answer confirmed that the Sunnyvale Store does not reliably or "
     "ordinarily stock the item she was accusing Plaintiff of taking."),
    ("PARA",
     "59. Plaintiff then turned to DOE 2, a white woman wearing a Ross employee "
     "shirt who was working as a cashier and was standing approximately five feet "
     "away, and asked her the same question: \"Do you people sell Celsius drinks "
     "here?\""),
    ("PARA",
     "60. DOE 2 remained silent. She did not answer Plaintiff's question."),
    ("PARA",
     "61. DOE 2 did not correct DOE 1."),
    ("PARA",
     "62. DOE 2 did not intervene."),
    ("PARA",
     "63. DOE 2 did not confirm or deny that the store stocked the item."),
    ("PARA",
     "64. DOE 2 did not release Plaintiff from the detention."),
    ("PARA",
     "65. DOE 2's silence in that moment ratified and prolonged the detention."),
    ("PARA",
     "66. DOE 1 then stated: \"I'm allowed to do that.\""),
    ("PARA",
     "67. Plaintiff replied: \"You stopped me for no reason.\""),

    ("SUBHEAD", "F. What Did Not Happen"),
    ("PARA",
     "68. At no point during the detention was Plaintiff asked to produce a "
     "receipt for the beverage."),
    ("PARA",
     "69. Plaintiff had the receipt in his possession. He was never given the "
     "opportunity to present it, because he was never asked."),
    ("PARA",
     "70. Plaintiff was not searched."),
    ("PARA",
     "71. Plaintiff's person, pockets, and belongings were not inspected."),
    ("PARA",
     "72. Law enforcement was not summoned."),
    ("PARA",
     "73. No police report was made."),
    ("PARA",
     "74. Plaintiff was never accused of taking any clothing, apparel, footwear, "
     "housewares, or any other item of Ross merchandise."),
    ("PARA",
     "75. No Ross employee stated that any employee had observed Plaintiff take, "
     "conceal, or attempt to remove any Ross merchandise."),
    ("PARA",
     "76. No Ross merchandise was recovered from Plaintiff, because Plaintiff had "
     "none."),
    ("PARA",
     "77. No electronic article surveillance alarm sounded."),
    ("PARA",
     "78. The sole asserted basis for stopping Plaintiff was the beverage he had "
     "carried into the store in open view five minutes after buying it next door."),

    ("SUBHEAD", "G. Witnesses"),
    ("PARA",
     "79. DOE 2, the cashier, witnessed the detention from close proximity."),
    ("PARA",
     "80. An Indian couple standing behind Plaintiff at or near the exit observed "
     "the detention. The couple appeared to be in their 30s or 40s. Their "
     "identities are presently unknown to Plaintiff. Plaintiff will seek to "
     "identify these percipient witnesses through discovery."),
    ("PARA",
     "81. The detention occurred in the front area of the store, near the "
     "registers and the exit, where it was open and visible to employees and "
     "members of the public."),
    ("PARA",
     "82. Upon information and belief, Defendants' surveillance cameras captured "
     "the entire incident."),

    ("SUBHEAD", "H. Harm to Plaintiff"),
    ("PARA",
     "83. As a direct and proximate result of Defendants' conduct, Plaintiff "
     "suffered and continues to suffer emotional distress."),
    ("PARA",
     "84. Plaintiff was publicly treated as a thief, in front of Ross employees "
     "and other Ross patrons, because of the color of his skin."),
    ("PARA",
     "85. Plaintiff experienced humiliation and embarrassment in front of other "
     "customers who witnessed the detention, including the couple standing "
     "directly behind him."),
    ("PARA",
     "86. Plaintiff experienced, and continues to experience, anxiety, "
     "indignation, distress, shame, anger, and a persistent sense of being "
     "unwelcome and suspect in ordinary retail spaces."),
    ("PARA",
     "87. Plaintiff has suffered a loss of dignity."),
    ("PARA",
     "88. Plaintiff was denied the right to enter a business establishment open "
     "to the public, decline to purchase, and depart on the same terms available "
     "to other customers."),
    ("PARA",
     "89. Plaintiff now experiences anxiety when entering retail stores, "
     "particularly those with loss-prevention personnel. He is concerned that he "
     "will again be singled out for detention because of his race."),

    # V. RACIAL DISCRIMINATION
    ("HEADER", "V.\nALLEGATIONS REGARDING RACIAL DISCRIMINATION"),
    ("SUBHEAD", "A. Plaintiff Was Stopped Because He Is Black"),
    ("PARA", "90. Plaintiff is a Black man."),
    ("PARA", "91. DOE 1 is white."),
    ("PARA", "92. DOE 2 is white."),
    ("PARA",
     "93. The Sunnyvale Store is a retail business establishment open to the "
     "general public."),
    ("PARA",
     "94. Plaintiff alleges that Defendants' decision to intercept, stop, and "
     "detain him was motivated, at least in part, by his race."),
    ("PARA",
     "95. Plaintiff alleges that Defendants' loss-prevention practices at the "
     "Sunnyvale Store include the selection of customers for surveillance and "
     "investigatory detention on the basis of race, under the guise of theft "
     "prevention\u2014a practice commonly described as consumer racial profiling or "
     "\"shopping while Black.\""),

    ("SUBHEAD", "B. Circumstantial Evidence Supports the Inference of Discrimination"),
    ("PARA",
     "96. Direct evidence of discriminatory intent is rarely available. "
     "Discriminatory intent may be established by circumstantial evidence and by "
     "reasonable inferences drawn from the totality of the circumstances."),
    ("PARA",
     "97. The circumstances here support an inference of intentional race-based "
     "selection, including:"),
    ("LIST_ITEM",
     "a. Race of the parties: Plaintiff is Black, and the loss-prevention "
     "employee and cashier who participated in the detention are both white."),
    ("LIST_ITEM",
     "b. No observed theft: Plaintiff entered the store already holding the item "
     "in open view, so no employee could have observed him take it from a Ross "
     "shelf. He was seen entering with it."),
    ("LIST_ITEM",
     "c. No concealment: No employee observed, and no Defendant has claimed to "
     "have observed, any concealment of merchandise."),
    ("LIST_ITEM",
     "d. No Ross merchandise: No Ross merchandise was ever alleged to be missing "
     "or in Plaintiff's possession."),
    ("LIST_ITEM",
     "e. Admission of uncertainty: The only explanation DOE 1 offered for the "
     "item's provenance was that Ross sells the product \"sometimes\"\u2014an admission "
     "that the store does not reliably stock it and that she had no basis for "
     "believing it came from Ross."),
    ("LIST_ITEM",
     "f. Assertion of authority, not evidence: DOE 1's second and final "
     "explanation was not a factual basis at all, but an assertion of authority: "
     "\"I'm allowed to do that.\""),
    ("LIST_ITEM",
     "g. Silence of the cashier: DOE 2, a Ross employee positioned to resolve "
     "the question in seconds, remained silent rather than confirm or deny that "
     "the store carried the product. Her silence ratified the detention."),
    ("LIST_ITEM",
     "h. No receipt requested: Plaintiff was never asked for a receipt\u2014the "
     "single step that would have ended the encounter immediately. This is "
     "inconsistent with a good-faith inquiry into whether the item was paid for "
     "and suggests the real purpose of the stop was not to determine ownership of "
     "the drink."),
    ("LIST_ITEM",
     "i. Escalation to physical blocking: DOE 1 escalated directly to physically "
     "blocking a customer's exit, rather than making a non-obstructing inquiry. "
     "This suggests the stop was not a casual question but a deliberate "
     "detention."),
    ("LIST_ITEM",
     "j. Disparate treatment: On information and belief, similarly situated "
     "non-Black customers who enter and exit the Sunnyvale Store carrying "
     "beverages or other items purchased at neighboring businesses are not "
     "physically intercepted at the exit and questioned as suspected thieves."),
    ("LIST_ITEM",
     "k. Statistical evidence: On information and belief, Black customers are "
     "disproportionately stopped at the Sunnyvale Store compared to non-Black "
     "customers."),
    ("PARA",
     "98. Plaintiff alleges on information and belief that Defendants do not "
     "physically block the exits of white customers who leave the Sunnyvale Store "
     "holding an outside beverage."),
    ("PARA",
     "99. Plaintiff alleges on information and belief that Defendants' "
     "loss-prevention personnel at the Sunnyvale Store are not trained that a "
     "customer may lawfully enter a retail store carrying merchandise purchased "
     "elsewhere."),
    ("PARA",
     "100. Plaintiff alleges on information and belief that Defendants' "
     "loss-prevention personnel at the Sunnyvale Store are not trained that race, "
     "ethnicity, or apparent race may not be used as a factor in selecting which "
     "customers to surveil, approach, or detain."),

    ("SUBHEAD",
     "C. Generalized Theft Rates Do Not Supply Probable Cause and Do Not Excuse "
     "Profiling"),
    ("PARA",
     "101. Plaintiff acknowledges that retailers in the Greater Bay Area, "
     "including Defendants, face genuine losses from retail theft."),
    ("PARA",
     "102. Generalized concern about retail theft does not supply probable cause "
     "to detain any particular customer."),
    ("PARA",
     "103. Generalized concern about retail theft does not authorize a retailer "
     "to select which customers to detain on the basis of race."),
    ("PARA",
     "104. A statistical or industry-wide loss problem is not a defense to "
     "intentional discrimination against an individual customer. If it were, the "
     "Unruh Civil Rights Act would offer no protection in precisely the settings "
     "where it is most needed."),
    ("PARA",
     "105. Here, the ordinary indicia of probable cause were absent:"),
    ("LIST_ITEM", "\u2022 No employee saw Plaintiff take anything from Ross."),
    ("LIST_ITEM", "\u2022 Plaintiff entered holding the item."),
    ("LIST_ITEM", "\u2022 Nothing was concealed."),
    ("LIST_ITEM", "\u2022 Nothing was missing."),
    ("LIST_ITEM", "\u2022 Nothing was recovered."),
    ("PARA",
     "106. Penal Code section 490.5(f) permits a merchant to detain a person only "
     "when the merchant has probable cause to believe the person has unlawfully "
     "taken or is attempting to unlawfully take merchandise from the merchant's "
     "premises, and only for the limited purposes and in the limited manner "
     "specified by that statute."),
    ("PARA",
     "107. Defendants lacked probable cause to believe that Plaintiff had taken "
     "or was attempting to take any Ross merchandise."),
    ("PARA",
     "108. Because probable cause was absent, the merchant's privilege under "
     "Penal Code section 490.5(f) does not apply, and the detention of Plaintiff "
     "was unlawful."),
    ("PARA",
     "109. Separately, and independently, the detention exceeded the scope of any "
     "privilege because Defendants never conducted the limited inquiry the statute "
     "contemplates: they never requested a receipt, never asked Plaintiff to "
     "identify the item's source, and never conducted any recovery of merchandise, "
     "because there was none to recover."),

    # FIRST CAUSE OF ACTION
    ("HEADER", "VI.\nFIRST CAUSE OF ACTION"),
    ("SUBHEAD",
     "Violation of the Unruh Civil Rights Act\n"
     "(Civil Code \u00a7\u00a7 51, 51.5, 52)\n"
     "Against All Defendants"),
    ("PARA",
     "110. Plaintiff realleges and incorporates by reference each and every "
     "allegation contained in paragraphs 1 through 109, inclusive, as though fully "
     "set forth herein."),
    ("PARA",
     "111. Civil Code section 51(b) provides that all persons within the "
     "jurisdiction of this State are free and equal, and no matter what their "
     "race, color, ancestry, national origin, or other protected characteristic, "
     "are entitled to the full and equal accommodations, advantages, facilities, "
     "privileges, or services in all business establishments of every kind "
     "whatsoever."),
    ("PARA",
     "112. Civil Code section 51.5(a) provides that no business establishment of "
     "any kind whatsoever shall discriminate against, boycott or blacklist, or "
     "refuse to buy from, contract with, sell to, or trade with any person in this "
     "State because of the race, color, or other protected characteristic of that "
     "person."),
    ("PARA",
     "113. The Sunnyvale Store is a \"business establishment\" within the meaning "
     "of Civil Code sections 51 and 51.5. The term is construed in the broadest "
     "sense reasonably possible and plainly encompasses a retail store open to the "
     "general public."),
    ("PARA",
     "114. The Corporate Defendants own, operate, and/or control the Sunnyvale "
     "Store and are business establishments within the meaning of the Act."),
    ("PARA",
     "115. Plaintiff, as a customer who entered the Sunnyvale Store during "
     "business hours, was a member of the public entitled to the full and equal "
     "accommodations, advantages, facilities, privileges, and services of that "
     "business establishment."),
    ("PARA",
     "116. Among the privileges and services to which Plaintiff was entitled "
     "were:"),
    ("LIST_ITEM",
     "\u2022 The ability to browse merchandise without being singled out for "
     "surveillance because of his race."),
    ("LIST_ITEM", "\u2022 The ability to decline to purchase."),
    ("LIST_ITEM", "\u2022 The ability to walk to the exit unobstructed."),
    ("LIST_ITEM",
     "\u2022 The ability to leave the store without being physically intercepted "
     "and interrogated as a presumed thief."),
    ("PARA",
     "117. Defendants, acting through DOE 1 and DOE 2 and within the course and "
     "scope of their employment, denied Plaintiff those accommodations, "
     "advantages, facilities, privileges, and services."),
    ("PARA",
     "118. Defendants did so intentionally and because of Plaintiff's race."),
    ("PARA",
     "119. A violation of the Unruh Act requires intentional discrimination. "
     "Such intent need not be proven by direct evidence and may be established "
     "through circumstantial evidence and the reasonable inferences that flow from "
     "the surrounding facts."),
    ("PARA",
     "120. The circumstantial evidence of intentional race-based selection is set "
     "forth in paragraph 97 above and is incorporated here."),
    ("PARA",
     "121. Plaintiff further alleges that Defendants' conduct constituted the "
     "application of a facially neutral loss-prevention practice in an "
     "intentionally discriminatory manner: whatever Defendants' written policy may "
     "say about outside beverages, that practice was enforced against Plaintiff, a "
     "Black customer, in a manner in which it is not enforced against similarly "
     "situated non-Black customers."),
    ("PARA",
     "122. Race was a substantial motivating factor in Defendants' decision to "
     "intercept and detain Plaintiff."),
    ("PARA",
     "123. Defendants' asserted concern about retail theft is pretextual as "
     "applied to Plaintiff, and in any event does not justify the race-based "
     "selection of whom to detain."),
    ("PARA",
     "124. Defendants' conduct was a substantial factor in causing Plaintiff's "
     "harm."),
    ("PARA",
     "125. As a direct and proximate result of Defendants' violation of the Unruh "
     "Civil Rights Act, Plaintiff has suffered actual damages, including emotional "
     "distress, humiliation, embarrassment, anxiety, indignation, and loss of "
     "dignity, in an amount to be proven at trial and in excess of the "
     "jurisdictional minimum of this Court."),
    ("PARA",
     "126. Civil Code section 52(a) provides that whoever denies, aids or incites "
     "a denial, or makes any discrimination or distinction contrary to section 51 "
     "or 51.5 is liable for each and every offense for the actual damages, and any "
     "amount that may be determined by a jury, or a court sitting without a jury, "
     "up to a maximum of three times the amount of actual damage, but in no case "
     "less than four thousand dollars ($4,000), and any attorney's fees that may "
     "be determined by the court in addition thereto."),
    ("PARA",
     "127. Plaintiff is therefore entitled to recover his actual damages, up to "
     "three times his actual damages, and in no event less than the statutory "
     "minimum of four thousand dollars ($4,000) per offense, together with "
     "attorney's fees and costs."),
    ("PARA",
     "128. Plaintiff is further entitled to preventive and injunctive relief "
     "pursuant to Civil Code section 52(c)."),
    ("PARA",
     "129. Defendants' conduct was despicable and was carried out with a willful "
     "and conscious disregard of Plaintiff's rights, and constitutes malice and "
     "oppression within the meaning of Civil Code section 3294. Plaintiff is "
     "informed and believes and thereon alleges that an officer, director, or "
     "managing agent of the Corporate Defendants authorized or ratified the "
     "loss-prevention practices that produced this conduct, or acted with advance "
     "knowledge of the unfitness of the loss-prevention personnel employed at the "
     "Sunnyvale Store and employed them with a conscious disregard of the rights "
     "of others. Plaintiff is therefore entitled to punitive damages in an amount "
     "sufficient to punish and deter."),

    # SECOND CAUSE OF ACTION
    ("HEADER", "VII.\nSECOND CAUSE OF ACTION"),
    ("SUBHEAD", "False Imprisonment\nAgainst All Defendants"),
    ("PARA",
     "130. Plaintiff realleges and incorporates by reference each and every "
     "allegation contained in paragraphs 1 through 129, inclusive, as though fully "
     "set forth herein."),
    ("PARA",
     "131. Defendant DOE 1 intentionally deprived Plaintiff of his freedom of "
     "movement by physically stepping in front of him and blocking his path to the "
     "exit of the Sunnyvale Store."),
    ("PARA",
     "132. Confinement for purposes of false imprisonment may be effected by "
     "physical barriers or by any means that a reasonable person would understand "
     "to restrict freedom of movement. Physical touching is not required."),
    ("PARA",
     "133. DOE 1's conduct compelled Plaintiff to remain in the store for an "
     "appreciable period of time\u2014approximately three minutes\u2014against his will."),
    ("PARA",
     "134. Plaintiff did not consent to the confinement."),
    ("PARA",
     "135. Plaintiff was actually aware of the confinement at the time it "
     "occurred."),
    ("PARA",
     "136. DOE 2 participated in and prolonged the confinement by remaining "
     "present, remaining silent, and declining to answer the question that would "
     "have terminated the encounter."),
    ("PARA",
     "137. The confinement was not privileged."),
    ("PARA",
     "138. Penal Code section 490.5(f)(1) permits a merchant to detain a person "
     "for a reasonable time and in a reasonable manner only when the merchant has "
     "probable cause to believe the person to be detained is attempting to "
     "unlawfully take or has unlawfully taken merchandise from the merchant's "
     "premises."),
    ("PARA",
     "139. Defendants had no probable cause to believe that Plaintiff had taken "
     "or was attempting to take any merchandise from the Sunnyvale Store."),
    ("PARA",
     "140. No Defendant observed Plaintiff take merchandise. No Defendant "
     "observed Plaintiff conceal merchandise. Plaintiff entered the premises "
     "already holding the beverage in open view, and no Ross merchandise was ever "
     "identified as missing or in Plaintiff's possession."),
    ("PARA",
     "141. DOE 1's own statement that the store sells the beverage only "
     "\"sometimes\" further negates any reasonable belief that the item came from "
     "Ross shelves."),
    ("PARA",
     "142. Because Defendants lacked probable cause, the merchant's detention "
     "privilege under Penal Code section 490.5(f) does not apply."),
    ("PARA",
     "143. Alternatively, and in addition, the detention was not conducted in a "
     "reasonable manner or for a purpose authorized by the statute, in that "
     "Defendants never requested a receipt, never conducted any lawful inquiry "
     "designed to resolve ownership of the item, and instead detained Plaintiff "
     "for an investigatory purpose untethered to any observed act of theft."),
    ("PARA",
     "144. Defendants' conduct was a substantial factor in causing Plaintiff "
     "harm."),
    ("PARA",
     "145. As a direct and proximate result of the false imprisonment, Plaintiff "
     "suffered damages including emotional distress, humiliation, indignity, "
     "embarrassment, and anxiety, in an amount to be proven at trial and in excess "
     "of the jurisdictional minimum of this Court."),
    ("PARA",
     "146. The Corporate Defendants are liable for the false imprisonment under "
     "the doctrine of respondeat superior, because DOE 1 and DOE 2 were acting "
     "within the course and scope of their employment and were performing the very "
     "function\u2014loss prevention\u2014for which they were hired."),
    ("PARA",
     "147. Defendants' conduct was carried out with malice and oppression within "
     "the meaning of Civil Code section 3294, entitling Plaintiff to punitive "
     "damages."),

    # THIRD CAUSE OF ACTION
    ("HEADER", "VIII.\nTHIRD CAUSE OF ACTION"),
    ("SUBHEAD",
     "Intentional Infliction of Emotional Distress\nAgainst All Defendants"),
    ("PARA",
     "148. Plaintiff realleges and incorporates by reference each and every "
     "allegation contained in paragraphs 1 through 147, inclusive, as though fully "
     "set forth herein."),
    ("PARA",
     "149. Defendants' conduct was outrageous."),
    ("PARA",
     "150. It is outrageous for a retailer to physically block a customer's exit "
     "and publicly treat him as a thief because he is Black."),
    ("PARA",
     "151. The outrageousness of the conduct is heightened by the following "
     "circumstances:"),
    ("LIST_ITEM",
     "a. Defendants occupied a position of power over Plaintiff, controlling the "
     "premises, the exit, and the presence of security personnel."),
    ("LIST_ITEM",
     "b. The accusation was made publicly, near the registers and the exit, in "
     "the presence of Ross employees and other customers."),
    ("LIST_ITEM",
     "c. Defendants had no factual basis for the accusation."),
    ("LIST_ITEM",
     "d. When confronted with the absence of any basis, DOE 1 did not apologize "
     "or release Plaintiff, but instead asserted raw authority\u2014\"I'm allowed to "
     "do that.\""),
    ("LIST_ITEM",
     "e. DOE 2, who could have ended the encounter with a single word, chose "
     "silence."),
    ("LIST_ITEM",
     "f. The conduct was directed at Plaintiff because of a protected "
     "characteristic, and racial discrimination in a place of public accommodation "
     "is the kind of conduct that a civilized community does not tolerate."),
    ("PARA",
     "152. Defendants' conduct exceeded all bounds of that usually tolerated in a "
     "civilized community."),
    ("PARA",
     "153. Defendants acted with the intent to cause Plaintiff emotional "
     "distress, or in the alternative with reckless disregard of the probability "
     "that their conduct would cause Plaintiff to suffer emotional distress."),
    ("PARA",
     "154. Defendants knew or should have known that publicly accusing a Black "
     "customer of theft without basis, and physically preventing him from leaving, "
     "would cause humiliation and distress."),
    ("PARA",
     "155. Plaintiff in fact suffered emotional distress, as alleged in "
     "paragraphs 83 through 89 above."),
    ("PARA",
     "156. Defendants' outrageous conduct was a substantial factor in causing "
     "Plaintiff's emotional distress."),
    ("PARA",
     "157. The Corporate Defendants are liable for the conduct of DOE 1 and "
     "DOE 2 under the doctrine of respondeat superior and by reason of their "
     "ratification of that conduct."),
    ("PARA",
     "158. As a direct and proximate result, Plaintiff has suffered general "
     "damages in an amount to be proven at trial and in excess of the "
     "jurisdictional minimum of this Court."),
    ("PARA",
     "159. Defendants' conduct was despicable and was carried out with a willful "
     "and conscious disregard of Plaintiff's rights, constituting malice and "
     "oppression under Civil Code section 3294, entitling Plaintiff to punitive "
     "damages."),

    # FOURTH CAUSE OF ACTION
    ("HEADER", "IX.\nFOURTH CAUSE OF ACTION"),
    ("SUBHEAD",
     "Negligent Hiring, Training, Retention, and Supervision\n"
     "Against the Corporate Defendants and Does 3\u201320"),
    ("PARA",
     "160. Plaintiff realleges and incorporates by reference each and every "
     "allegation contained in paragraphs 1 through 159, inclusive, as though fully "
     "set forth herein."),
    ("PARA",
     "161. This cause of action is pleaded in the alternative to the intentional "
     "torts alleged above."),
    ("PARA",
     "162. The Corporate Defendants owed a duty of reasonable care to members of "
     "the public, including Plaintiff, who entered the Sunnyvale Store as "
     "invitees."),
    ("PARA",
     "163. That duty included the duty to exercise reasonable care in the hiring, "
     "training, retention, and supervision of loss-prevention and security "
     "personnel who are authorized to stop, question, and detain customers."),
    ("PARA",
     "164. A retailer that empowers employees to physically detain members of the "
     "public assumes a heightened obligation to ensure those employees are "
     "competent to exercise that power lawfully and without regard to race."),
    ("PARA",
     "165. The Corporate Defendants breached that duty in one or more of the "
     "following respects:"),
    ("LIST_ITEM",
     "a. Failing to train loss-prevention personnel that a customer's race is "
     "not, and may never be, a factor in deciding whom to surveil, approach, or "
     "detain."),
    ("LIST_ITEM",
     "b. Failing to train loss-prevention personnel that a customer may lawfully "
     "enter a Ross store carrying food, beverages, or merchandise purchased at a "
     "neighboring business."),
    ("LIST_ITEM",
     "c. Failing to train loss-prevention personnel on the probable-cause "
     "requirement of Penal Code section 490.5(f) and the limits of the merchant's "
     "detention privilege."),
    ("LIST_ITEM",
     "d. Failing to train loss-prevention personnel to make a non-obstructing "
     "inquiry, including a simple request for a receipt, before physically "
     "blocking a customer's egress."),
    ("LIST_ITEM",
     "e. Failing to train store employees, including cashiers, on their "
     "obligation to intervene or provide information that would terminate an "
     "unfounded detention."),
    ("LIST_ITEM",
     "f. Failing to adopt, implement, monitor, and enforce policies prohibiting "
     "consumer racial profiling at the Sunnyvale Store."),
    ("LIST_ITEM",
     "g. Failing to audit or track the demographics of customers stopped by "
     "loss-prevention personnel at the Sunnyvale Store, or failing to act on such "
     "data."),
    ("LIST_ITEM",
     "h. Hiring and retaining DOE 1 in a loss-prevention role notwithstanding "
     "her unfitness to exercise detention authority lawfully."),
    ("LIST_ITEM",
     "i. Failing to supervise DOE 1 and DOE 2 in the performance of their "
     "loss-prevention duties."),
    ("PARA",
     "166. It was reasonably foreseeable that the failure to train and supervise "
     "loss-prevention personnel in these respects would result in customers being "
     "detained without probable cause, and would result in the race-based "
     "selection of customers for detention."),
    ("PARA",
     "167. The Corporate Defendants' breach was a substantial factor in causing "
     "the detention of Plaintiff and the harm he suffered."),
    ("PARA",
     "168. As a direct and proximate result, Plaintiff has suffered damages in an "
     "amount to be proven at trial and in excess of the jurisdictional minimum of "
     "this Court."),

    # FIFTH CAUSE OF ACTION
    ("HEADER", "X.\nFIFTH CAUSE OF ACTION"),
    ("SUBHEAD",
     "Unlawful and Unfair Business Practices\n"
     "(Business & Professions Code \u00a7 17200 et seq.)\n"
     "Against the Corporate Defendants and Does 3\u201320"),
    ("PARA",
     "169. Plaintiff realleges and incorporates by reference each and every "
     "allegation contained in paragraphs 1 through 168, inclusive, as though fully "
     "set forth herein."),
    ("PARA",
     "170. Business and Professions Code section 17200 defines unfair competition "
     "to include any unlawful, unfair, or fraudulent business act or practice."),
    ("PARA",
     "171. Defendants' conduct constitutes an unlawful business practice "
     "because:"),
    ("LIST_ITEM",
     "a. It violates Civil Code sections 51 and 51.5 (the Unruh Civil Rights "
     "Act)."),
    ("LIST_ITEM",
     "b. It constitutes detention without the probable cause required by Penal "
     "Code section 490.5(f)."),
    ("LIST_ITEM",
     "c. It constitutes the common-law torts of false imprisonment and "
     "intentional infliction of emotional distress."),
    ("PARA",
     "172. Defendants' conduct constitutes an unfair business practice because:"),
    ("LIST_ITEM",
     "a. The practice of selecting customers for investigatory detention on the "
     "basis of race is immoral, unethical, oppressive, unscrupulous, and "
     "substantially injurious to consumers."),
    ("LIST_ITEM",
     "b. It offends a legislatively declared public policy embodied in the Unruh "
     "Civil Rights Act."),
    ("LIST_ITEM",
     "c. The harm it causes to consumers outweighs any utility it may have to "
     "Defendants, particularly where the practice does not actually detect theft, "
     "as this incident demonstrates."),
    ("PARA",
     "173. Defendants' business practices at issue include:"),
    ("LIST_ITEM",
     "a. Selecting customers for loss-prevention surveillance and detention on "
     "the basis of race."),
    ("LIST_ITEM",
     "b. Detaining customers without probable cause."),
    ("LIST_ITEM",
     "c. Physically obstructing customers' egress as a loss-prevention "
     "technique."),
    ("LIST_ITEM",
     "d. Failing to train and supervise loss-prevention personnel regarding the "
     "legal limits on customer detention."),
    ("PARA",
     "174. These are ongoing business practices, not isolated acts, and on "
     "information and belief they continue at the Sunnyvale Store and at other "
     "Ross locations."),
    ("PARA",
     "175. Plaintiff has suffered injury in fact as a result of Defendants' "
     "unfair competition, including the deprivation of his liberty of movement "
     "and the denial of equal access to a place of public accommodation. Plaintiff "
     "seeks only equitable relief on this cause of action."),
    ("PARA",
     "176. Plaintiff seeks injunctive relief pursuant to Business and "
     "Professions Code section 17203, including an order requiring Defendants "
     "to:"),
    ("LIST_ITEM",
     "a. Adopt and implement a written policy prohibiting the use of race as a "
     "factor in loss-prevention decisions."),
    ("LIST_ITEM",
     "b. Train all loss-prevention personnel and store employees at the "
     "Sunnyvale Store on that policy and on the probable-cause requirements of "
     "Penal Code section 490.5."),
    ("LIST_ITEM",
     "c. Train all loss-prevention personnel that customers may enter carrying "
     "items purchased elsewhere."),
    ("LIST_ITEM",
     "d. Implement a documented procedure requiring a non-obstructing inquiry "
     "and a request for a receipt before any physical detention."),
    ("LIST_ITEM",
     "e. Audit and track the demographics of customers stopped at the Sunnyvale "
     "Store and report the results to the Court."),
    ("PARA",
     "177. Plaintiff acknowledges that damages are not recoverable under "
     "Business and Professions Code section 17200, and this cause of action seeks "
     "equitable relief only."),

    # SIXTH CAUSE OF ACTION
    ("HEADER", "XI.\nSIXTH CAUSE OF ACTION"),
    ("SUBHEAD",
     "Declaratory Relief\n"
     "(Code of Civil Procedure \u00a7 1060)\n"
     "Against All Defendants"),
    ("PARA",
     "178. Plaintiff realleges and incorporates by reference each and every "
     "allegation contained in paragraphs 1 through 177, inclusive, as though fully "
     "set forth herein."),
    ("PARA",
     "179. An actual and present controversy has arisen between Plaintiff and "
     "Defendants concerning their respective rights and duties."),
    ("PARA",
     "180. Plaintiff contends that Defendants' interception and detention of him "
     "on August 25, 2026 violated the Unruh Civil Rights Act; that Defendants "
     "lacked probable cause under Penal Code section 490.5(f); and that "
     "generalized concerns about retail theft in the Greater Bay Area do not "
     "authorize a retailer to select customers for detention on the basis of "
     "race."),
    ("PARA",
     "181. Plaintiff is informed and believes, and on that basis alleges, that "
     "Defendants contend to the contrary\u2014as reflected in DOE 1's contemporaneous "
     "assertion, \"I'm allowed to do that.\""),
    ("PARA",
     "182. A judicial declaration is necessary and appropriate at this time so "
     "that the parties may ascertain their rights and duties, and so that "
     "Plaintiff may shop at Defendants' stores without being subjected to "
     "race-based detention."),
    ("PARA",
     "183. Plaintiff seeks a declaration that:"),
    ("LIST_ITEM",
     "a. Defendants' stop and detention of Plaintiff on August 25, 2026 violated "
     "Civil Code sections 51 and 51.5."),
    ("LIST_ITEM",
     "b. Defendants lacked probable cause within the meaning of Penal Code "
     "section 490.5(f), and the merchant's detention privilege did not apply."),
    ("LIST_ITEM",
     "c. Generalized retail-theft conditions do not authorize or excuse the "
     "selection of customers for detention on the basis of race."),

    # PRAYER
    ("HEADER", "XII.\nPRAYER FOR RELIEF"),
    ("PARA",
     "WHEREFORE, Plaintiff BRENDAN NGWA NFORBI prays for judgment against "
     "Defendants, and each of them, as follows:"),
    ("SUBHEAD", "On the First Cause of Action (Unruh Civil Rights Act):"),
    ("LIST_ITEM", "1. For actual damages according to proof at trial;"),
    ("LIST_ITEM",
     "2. For statutory damages pursuant to Civil Code section 52(a) in an amount "
     "up to three times actual damages, but in no event less than four thousand "
     "dollars ($4,000) for each and every offense;"),
    ("LIST_ITEM",
     "3. For attorney's fees pursuant to Civil Code section 52(a) and Code of "
     "Civil Procedure section 1021.5, as applicable;"),
    ("LIST_ITEM",
     "4. For preventive and injunctive relief pursuant to Civil Code section "
     "52(c);"),
    ("SUBHEAD", "On the Second Cause of Action (False Imprisonment):"),
    ("LIST_ITEM", "5. For general and special damages according to proof at trial;"),
    ("SUBHEAD",
     "On the Third Cause of Action (Intentional Infliction of Emotional "
     "Distress):"),
    ("LIST_ITEM",
     "6. For general damages for emotional distress according to proof at "
     "trial;"),
    ("SUBHEAD",
     "On the Fourth Cause of Action (Negligent Hiring, Training, Retention, and "
     "Supervision):"),
    ("LIST_ITEM", "7. For general and special damages according to proof at trial;"),
    ("SUBHEAD", "On the Fifth Cause of Action (Unfair Competition Law):"),
    ("LIST_ITEM",
     "8. For injunctive relief pursuant to Business and Professions Code section "
     "17203, including the relief described in paragraph 176 above;"),
    ("SUBHEAD", "On the Sixth Cause of Action (Declaratory Relief):"),
    ("LIST_ITEM",
     "9. For a judicial declaration as set forth in paragraph 183 above;"),
    ("SUBHEAD", "On All Causes of Action:"),
    ("LIST_ITEM",
     "10. For exemplary and punitive damages pursuant to Civil Code section 3294 "
     "in an amount sufficient to punish Defendants and deter similar conduct, "
     "according to proof;"),
    ("LIST_ITEM",
     "11. For prejudgment and post-judgment interest as permitted by law;"),
    ("LIST_ITEM", "12. For costs of suit incurred herein; and"),
    ("LIST_ITEM",
     "13. For such other and further relief as the Court deems just and "
     "proper."),
    ("PARA",
     "Plaintiff alleges that the total amount in controversy exceeds thirty-five "
     "thousand dollars ($35,000), exclusive of interest and costs, and that this "
     "action is properly classified as an unlimited civil case."),

    # JURY DEMAND
    ("HEADER", "XIII.\nDEMAND FOR JURY TRIAL"),
    ("PARA",
     "184. Plaintiff hereby demands a trial by jury on all causes of action and "
     "issues so triable."),
]


def _signature_block(d: PleadingPaper, exec_date: str, *, respectfully: bool) -> None:
    # Signature ink extends ~1.5–2 pleading lines above the underscore; reserve
    # blanks so clear space remains under the preceding text.
    d.ensure_space(12)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    if respectfully:
        d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)
    d.blank_line()
    d.write_line("Telephone: (209) 801-4442", right=True, right_margin_offset=20)
    d.write_line("Email: bnn.cdl@gmail.com", right=True, right_margin_offset=20)


def _verification(d: PleadingPaper, exec_date: str) -> None:
    d.start_new_page()
    d.write_line("VERIFICATION", bold=True, center=True)
    d.blank_line()
    d.write_line("STATE OF CALIFORNIA, COUNTY OF SANTA CLARA", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "I, BRENDAN NGWA NFORBI, am the Plaintiff in the above-entitled action.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "I have read the foregoing VERIFIED COMPLAINT FOR DAMAGES AND INJUNCTIVE "
        "AND DECLARATORY RELIEF and know its contents.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "The matters stated therein are true of my own knowledge, except as to "
        "those matters stated on information and belief, and as to those matters "
        "I believe them to be true.",
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
        f"Executed on {exec_date}, in the County of Santa Clara, State of "
        "California.",
        first_indent=36,
    )
    d.ensure_space(10)
    # Signature ink extends ~1.5–2 pleading lines above the underscore; reserve
    # blanks so clear space remains under the execution sentence.
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)


def build(out: Path, exec_date: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
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

    for kind, text in CONTENT:
        if kind == "HEADER":
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
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")

    _signature_block(d, exec_date, respectfully=True)
    _verification(d, exec_date)
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--date", default=DEFAULT_EXEC_DATE,
                    help="Execution / verification date printed on the filing")
    args = ap.parse_args()
    path = build(Path(args.out).resolve(), args.date)
    print(f"Generated: {path}")


if __name__ == "__main__":
    main()
