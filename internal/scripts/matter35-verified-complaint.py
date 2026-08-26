#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 35 — Verified Complaint for Damages and Injunctive Relief (v9).

Ngwa Nforbi v. Ross Stores, Inc., et al.
Superior Court of California, County of Santa Clara.

Rendered from the v9 draft on the shared California pleading-paper engine
and signed with the portfolio universal signature.

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
    ("DOE 1; and DOES 2 through 20,", True, False),
    ("inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. _________________", False, False),
    ("", False, False),
    ("VERIFIED COMPLAINT FOR", True, False),
    ("DAMAGES AND INJUNCTIVE", True, False),
    ("RELIEF", True, False),
    ("", False, False),
    ("(1) Unruh Civil Rights Act", False, False),
    ("      (Civ. Code \u00a7\u00a7 51, 51.5, 52);", False, False),
    ("(2) False Imprisonment;", False, False),
    ("(3) Negligent Training and", False, False),
    ("      Supervision", False, False),
    ("", False, False),
    ("[Unlimited Civil -- Amount", False, True),
    (" Exceeds $35,000]", False, True),
    ("[Jury Trial Demanded]", False, True),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

CONTENT = [
    ("PARA", 'Plaintiff BRENDAN NGWA NFORBI ("Plaintiff") alleges as follows:'),
    ("HEADER", 'I.\nINTRODUCTION'),
    ("PARA", "1. This is a case about who gets stopped. On August 25, 2026, Plaintiff -- a Black man -- walked into a Ross Dress for Less store in Sunnyvale, California, holding a Celsius energy drink he had purchased five minutes earlier at the Sprouts Farmers Market next door. He browsed the men's clothing section, found nothing he wanted, and walked toward the exit empty-handed. As he approached the door, a white female loss-prevention employee physically stepped in front of him, blocking his path, and demanded to know whether he had paid for the drink he was carrying. Plaintiff had taken no Ross merchandise and had concealed nothing, and no employee identified any observed act of taking or concealment during the encounter. No Ross merchandise was identified to Plaintiff as missing. No alarm sounded."),
    ("PARA", '2. This is not a case about a slur. It is a case about a retail practice known as consumer racial profiling, or "shopping while Black" -- the selective detention of Black customers on the basis of race rather than evidence. Defendants\' loss-prevention employee did not ask Plaintiff for a receipt, did not search him, did not recover any merchandise, and did not summon law enforcement, because there was no basis for any of those actions. She blocked his exit, accused him by implication, and asserted: "I\'m allowed to do that."'),
    ("PARA", '3. The Unruh Civil Rights Act guarantees every person the right to enter a business establishment, decline to buy anything, and leave on the same terms as every other customer. Defendants denied Plaintiff that right because of his race.'),
    ("PARA", "4. Plaintiff's claims rest on two independent legal wrongs. First, Defendants denied Plaintiff the full and equal accommodations, advantages, facilities, privileges, and services of a business establishment because of his race, in violation of Civil Code sections 51 and 51.5. Second, and independent of motive, Defendants confined Plaintiff without the probable cause that the merchant's detention privilege of Penal Code section 490.5(f) requires. Either wrong, standing alone, entitles Plaintiff to relief."),
    ("PARA", '5. Plaintiff brings this action to vindicate his civil rights, to obtain redress for the harm he suffered, and to secure injunctive relief requiring Defendants to abandon racially discriminatory loss-prevention practices at their Sunnyvale store.'),
    ("HEADER", 'II.\nPARTIES'),
    ("PARA", '6. Plaintiff BRENDAN NGWA NFORBI is, and at all relevant times was, a resident of the State of California. Plaintiff is a Black man.'),
    ("PARA", '7. Defendant ROSS STORES, INC. is a corporation organized under the laws of the State of Delaware, qualified to transact business in California, with principal executive offices at 5130 Hacienda Drive, Dublin, California 94568.'),
    ("PARA", '8. Defendant ROSS DRESS FOR LESS, INC. is a corporation organized under the laws of the Commonwealth of Virginia, qualified to transact business in California, with principal executive offices at 5130 Hacienda Drive, Dublin, California 94568. California business-entity records identify Ross Dress for Less, Inc. as a stock corporation formed in Virginia, California document number 2642531, filed March 15, 2004, status active.'),
    ("PARA", '9. ROSS STORES, INC. and ROSS DRESS FOR LESS, INC. are referred to collectively as the "Corporate Defendants." The retail store located at 119 E. El Camino Real, Sunnyvale, California 94087 is referred to as the "Sunnyvale Store."'),
    ("PARA", "10. Plaintiff is informed and believes, and on that basis alleges, that one or both of the Corporate Defendants own, operate, staff, and control the Sunnyvale Store; establish and approve the loss-prevention policies, training materials, and personnel practices applied at that store; and employed DOE 1 at the time of the events alleged herein. The precise allocation of those functions between the two entities is presently within Defendants' exclusive knowledge. Plaintiff will amend this Complaint to conform to proof once the employing and operating entity is ascertained."),
    ("PARA", '11. On information and belief, the designated agent for service of process in California for one or both Corporate Defendants is C T Corporation System, 330 North Brand Boulevard, Suite 700, Glendale, California 91203. Plaintiff will serve each Corporate Defendant through the agent listed on the California Secretary of State record as of the date of service.'),
    ("PARA", "12. Defendant DOE 1 is the individual who blocked Plaintiff's exit from the Sunnyvale Store on August 25, 2026. DOE 1 is a white woman of approximately 55 years of age who was acting as loss-prevention or security personnel for the Corporate Defendants at the Sunnyvale Store. Her true name is presently unknown to Plaintiff and is known to Defendants."),
    ("PARA", '13. The true names and capacities, whether individual, corporate, associate, or otherwise, of Defendants DOES 2 through 20, inclusive, are unknown to Plaintiff, who therefore sues those Defendants by fictitious names pursuant to Code of Civil Procedure section 474. Plaintiff will seek leave of Court to amend this Complaint to allege their true names and capacities when ascertained.'),
    ("PARA", '14. Plaintiff is informed and believes, and on that basis alleges, that each Defendant sued herein as a DOE is legally responsible in some manner for the events and occurrences alleged herein and proximately caused the injuries and damages alleged herein.'),
    ("PARA", '15. Plaintiff is informed and believes, and on that basis alleges, that at all relevant times DOE 1 was an employee or agent of the Corporate Defendants, was on duty at the Sunnyvale Store, was performing the very duties for which she was hired, and was acting within the course and scope of her employment or agency.'),
    ("PARA", '16. The Corporate Defendants are therefore vicariously liable for the acts and omissions of DOE 1 under the doctrine of respondeat superior.'),
    ("PARA", "17. In stopping Plaintiff, DOE 1 was performing the loss-prevention responsibilities assigned to her by her employer, and not acting on a frolic of her own. The extent to which her conduct conformed to or departed from the Corporate Defendants' written loss-prevention policies, training, and supervisory practices is presently unknown to Plaintiff and is a matter for discovery. Plaintiff does not at this time allege that any officer, director, or managing agent of the Corporate Defendants authorized or ratified her conduct, and no such allegation is necessary to the vicarious liability alleged in paragraph 16 above."),
    ("HEADER", 'III.\nJURISDICTION AND VENUE'),
    ("PARA", '18. This Court has subject matter jurisdiction over this action pursuant to article VI, section 10 of the California Constitution and Code of Civil Procedure section 410.10.'),
    ("PARA", '19. This action is properly designated an unlimited civil case under Code of Civil Procedure sections 85 and 88 because the amount in controversy exceeds thirty-five thousand dollars ($35,000), exclusive of interest and costs.'),
    ("PARA", '20. This Court has personal jurisdiction over the Corporate Defendants because they are qualified to do business in California, maintain principal executive offices in California, operate retail stores throughout California including the Sunnyvale Store, and committed the acts complained of in California.'),
    ("PARA", '21. Venue is proper in the County of Santa Clara pursuant to Code of Civil Procedure sections 395 and 395.5 because the injury occurred in this County, the liabilities alleged arose in this County, and the Corporate Defendants conduct business in this County. The Sunnyvale Store is located within this County.'),
    ("HEADER", 'IV.\nFACTUAL ALLEGATIONS'),
    ("SUBHEAD", 'A. Plaintiff Purchases a Beverage at the Store Next Door'),
    ("PARA", '22. On August 25, 2026, at approximately 8:45 p.m., Plaintiff entered Sprouts Farmers Market located at 111 E. El Camino Real, Sunnyvale, California 94087.'),
    ("PARA", '23. Plaintiff selected a Celsius brand energy drink from the refrigerated section, proceeded to the checkout counter, and paid for the beverage.'),
    ("PARA", '24. Plaintiff received and retained the original register receipt. The receipt reflects a transaction time of 8:45 p.m. on August 25, 2026. Plaintiff does not attach the original to this initial pleading in order to preserve it, and will produce it in this litigation.'),
    ("PARA", '25. Sprouts Farmers Market is located immediately adjacent to the Sunnyvale Store, approximately 100 feet away. The two stores share a parking lot and are directly next to one another.'),
    ("SUBHEAD", 'B. Plaintiff Enters the Ross Store Holding the Beverage in Open View'),
    ("PARA", '26. At approximately 8:50 p.m. on August 25, 2026 -- approximately five minutes after completing his purchase at Sprouts -- Plaintiff entered the Sunnyvale Store.'),
    ("PARA", '27. Plaintiff entered the Sunnyvale Store already holding the Celsius drink in his right hand.'),
    ("PARA", "28. The drink was in Plaintiff's open hand and in plain view at the moment he crossed the threshold of the Sunnyvale Store. It was a brightly colored can, easily visible from any angle."),
    ("PARA", '29. Plaintiff did not conceal the drink. He did not place it in a bag, a pocket, or any container.'),
    ("PARA", "30. Plaintiff's possession of the beverage was therefore visible to any Ross employee positioned near the store entrance, including any loss-prevention personnel monitoring the entrance."),
    ("PARA", '31. Upon information and belief, Defendants maintain surveillance cameras covering the entrance and the front of the Sunnyvale Store, and those cameras recorded Plaintiff entering the store holding the beverage in open view.'),
    ("SUBHEAD", 'C. Plaintiff Shops, Buys Nothing, and Takes Nothing'),
    ("PARA", "32. Once inside, Plaintiff walked through the store to the men's clothing section and looked at various items of men's clothing, including shirts, pants, and jackets."),
    ("PARA", '33. Plaintiff considered purchasing clothing but determined that the prices were higher than he was willing to pay.'),
    ("PARA", '34. At no time did Plaintiff select, conceal, pocket, bag, or place on his person any Ross merchandise, or remove any Ross merchandise from any shelf, rack, hanger, or display for the purpose of taking it.'),
    ("PARA", "35. Throughout his time in the Sunnyvale Store, the Celsius drink remained in Plaintiff's hand, in plain view. The can was open, and Plaintiff drank from it openly while browsing in the men's clothing section. By the time Plaintiff walked toward the exit, the can had been opened and partially consumed."),
    ("PARA", '36. Plaintiff then decided to leave without making a purchase, as any customer is entitled to do.'),
    ("SUBHEAD", 'D. The Detention'),
    ("PARA", '37. At approximately 9:00 p.m., Plaintiff walked toward the exit of the Sunnyvale Store.'),
    ("PARA", '38. As he approached the exit, DOE 1 physically stepped directly in front of Plaintiff and positioned her body in his path, blocking the exit.'),
    ("PARA", '39. DOE 1 did not stand to the side and speak to Plaintiff. She did not gesture for him to stop. She physically interposed herself between Plaintiff and the only exit available to him.'),
    ("PARA", "40. DOE 1's physical positioning prevented Plaintiff from leaving the store."),
    ("PARA", '41. DOE 1 did not touch Plaintiff. She did not need to. Her physical interposition between Plaintiff and the exit had the intended and actual effect of stopping him and preventing him from leaving.'),
    ("PARA", "42. A reasonable person in Plaintiff's position would not have believed he was free to walk around DOE 1 and out the door."),
    ("PARA", '43. Plaintiff did not consent to being stopped or detained, and was conscious of the confinement at the time it occurred.'),
    ("PARA", '44. The detention lasted approximately three minutes.'),
    ("SUBHEAD", 'E. The Confrontation'),
    ("PARA", '45. DOE 1 asked Plaintiff: "Did you pay for that drink?"'),
    ("PARA", '46. Plaintiff responded by asking: "Do you people sell Celsius drinks here?"'),
    ("PARA", '47. DOE 1 answered: "Yeah, sometimes." Her answer expressed uncertainty rather than knowledge. She did not state that the Sunnyvale Store stocked the product on that date, that the product was displayed anywhere Plaintiff had been, or that any such product was missing.'),
    ("PARA", '48. Plaintiff then turned to a white female Ross employee wearing a Ross employee shirt, who was working as a cashier and standing approximately five feet away (the "Cashier"), and asked her the same question: "Do you people sell Celsius drinks here?" The Cashier did not answer, did not confirm or deny that the store stocked the item, and did not correct DOE 1. The Cashier is a percipient witness. Plaintiff does not presently name her as a defendant, and reserves the right to seek leave to amend should discovery establish her active participation in the detention.'),
    ("PARA", '49. DOE 1 then stated: "I\'m allowed to do that."'),
    ("PARA", '50. Plaintiff replied: "You stopped me for no reason."'),
    ("SUBHEAD", 'F. What Did Not Happen'),
    ("PARA", '51. At no point during the detention was Plaintiff asked to produce a receipt for the beverage. Plaintiff had the receipt in his possession. He was never given the opportunity to present it, because he was never asked.'),
    ("PARA", '52. Plaintiff was not searched. His person, pockets, and belongings were not inspected.'),
    ("PARA", '53. Law enforcement was not summoned, and no police report was made.'),
    ("PARA", '54. Plaintiff was never accused of taking any clothing, apparel, footwear, housewares, or any other item of Ross merchandise.'),
    ("PARA", '55. No Ross employee stated that any employee had observed Plaintiff take, conceal, or attempt to remove any Ross merchandise.'),
    ("PARA", '56. No Ross merchandise was recovered from Plaintiff, because Plaintiff had none. No electronic article surveillance alarm sounded.'),
    ("PARA", '57. The sole asserted basis for stopping Plaintiff was the beverage he had carried into the store in open view five minutes after buying it next door.'),
    ("SUBHEAD", 'G. Witnesses and Recorded Evidence'),
    ("PARA", '58. The Cashier witnessed the detention from close proximity.'),
    ("PARA", '59. A couple standing behind Plaintiff at or near the exit, who appeared to be of South Asian descent and in their thirties or forties, observed the detention. Their identities are presently unknown to Plaintiff, who will seek to identify these percipient witnesses through discovery.'),
    ("PARA", '60. The detention occurred in the front area of the store, near the registers and the exit, where it was open and visible to employees and members of the public.'),
    ("PARA", "61. Upon information and belief, Defendants' surveillance cameras captured the entire incident, including Plaintiff's entry into the store holding the beverage, his time in the men's clothing section, and DOE 1's interception of him at the exit."),
    ("SUBHEAD", 'H. Harm to Plaintiff'),
    ("PARA", "62. As a direct and proximate result of Defendants' conduct, Plaintiff suffered and continues to suffer emotional distress."),
    ("PARA", '63. Plaintiff was publicly treated as a thief, in front of Ross employees and other Ross patrons, because of the color of his skin.'),
    ("PARA", '64. Plaintiff experienced humiliation and embarrassment in front of other customers who witnessed the detention, including the couple standing directly behind him.'),
    ("PARA", '65. Plaintiff experienced, and continues to experience, anxiety, indignation, distress, shame, anger, and a persistent sense of being unwelcome and suspect in ordinary retail spaces. Plaintiff has suffered a loss of dignity.'),
    ("PARA", '66. Plaintiff was denied the right to enter a business establishment open to the public, decline to purchase, and depart on the same terms available to other customers.'),
    ("PARA", '67. Plaintiff now experiences anxiety when entering retail stores, particularly those with loss-prevention personnel, and is concerned that he will again be singled out for detention because of his race.'),
    ("PARA", "68. Plaintiff wishes and intends to shop at Ross stores in the future, including the Sunnyvale Store, which is located in a shopping center Plaintiff patronizes. Plaintiff is presently deterred from doing so by Defendants' loss-prevention practices and by the reasonable apprehension that he will again be selected for surveillance and detention on account of his race. Plaintiff will return to the Sunnyvale Store as a customer if those practices are corrected. On information and belief, the practices alleged herein remain in effect and unchanged, and absent preventive relief Plaintiff faces a real and continuing threat of being subjected to them again."),
    ("HEADER", 'V.\nALLEGATIONS OF RACE-BASED SELECTION'),
    ("PARA", '69. Plaintiff is a Black man. DOE 1 is white. The Sunnyvale Store is a retail business establishment open to the general public.'),
    ("PARA", "70. Plaintiff alleges that Defendants' decision to intercept, stop, and detain him was motivated, at least in part, by his race."),
    ("PARA", '71. Plaintiff is informed and believes, and on that basis alleges, that loss-prevention practices at the Sunnyvale Store include the selection of customers for surveillance and investigatory detention on the basis of race, under the guise of theft prevention -- a practice commonly described as consumer racial profiling.'),
    ("PARA", '72. Direct evidence of discriminatory intent is rarely available. Discriminatory intent may be established by circumstantial evidence and by reasonable inferences drawn from the totality of the circumstances.'),
    ("PARA", '73. The circumstances here support an inference of intentional race-based selection, including:'),
    ("LIST_ITEM", 'a. Race of the parties. Plaintiff is Black; the loss-prevention employee who detained him is white.'),
    ("LIST_ITEM", "b. No taking to observe. Plaintiff entered the store already holding the beverage openly in his hand, and drank from it openly while browsing. Plaintiff did not take the beverage from a Ross shelf, and no employee identified to Plaintiff any observed act of taking. Whether DOE 1 personally observed Plaintiff's entry, and what Defendants' cameras recorded, are matters presently within Defendants' knowledge and the subject of discovery."),
    ("LIST_ITEM", 'c. No concealment. Plaintiff concealed nothing, and no Defendant claimed during the encounter to have observed any concealment of merchandise.'),
    ("LIST_ITEM", "d. No Ross merchandise. No Ross merchandise was ever alleged to be missing or in Plaintiff's possession."),
    ("LIST_ITEM", 'e. Expression of uncertainty. The only explanation DOE 1 offered for the item\'s provenance was that Ross sells the product "sometimes." Even assuming the Sunnyvale Store does sometimes sell Celsius beverages, the fact that a retailer sometimes carries a product supplies no reason to believe that a particular can, carried openly into the store by a customer and openly consumed, came from that retailer\'s shelves.'),
    ("LIST_ITEM", 'f. Assertion of authority rather than evidence. DOE 1\'s second and final explanation was not a factual basis at all, but an assertion of authority: "I\'m allowed to do that."'),
    ("LIST_ITEM", 'g. No receipt requested. Plaintiff was never asked for a receipt -- the single step that would have ended the encounter immediately. That omission is inconsistent with a good-faith inquiry into whether the item was paid for, and supports the inference that determining ownership of the drink was not the real purpose of the stop.'),
    ("LIST_ITEM", "h. Immediate escalation to physical blocking. DOE 1 escalated directly to physically obstructing a customer's exit rather than making a non-obstructing inquiry, indicating a deliberate detention rather than a casual question."),
    ("LIST_ITEM", "i. Disparate treatment. On information and belief, similarly situated non-Black customers who enter and exit the Sunnyvale Store carrying beverages or other items purchased at neighboring businesses are not physically intercepted at the exit and questioned as suspected thieves. The identity of such comparator customers, and the records reflecting whom Defendants' loss-prevention personnel stop, are within Defendants' exclusive possession and control and are the proper subject of discovery."),
    ("PARA", '74. Plaintiff alleges on information and belief that Defendants do not physically block the exits of white customers who leave the Sunnyvale Store holding an outside beverage.'),
    ("PARA", "75. Plaintiff alleges on information and belief that Defendants' loss-prevention personnel at the Sunnyvale Store are not trained that a customer may lawfully enter a retail store carrying merchandise purchased elsewhere."),
    ("PARA", "76. Plaintiff alleges on information and belief that Defendants' loss-prevention personnel at the Sunnyvale Store are not trained that race, ethnicity, or apparent race may not be used as a factor in selecting which customers to surveil, approach, or detain."),
    ("HEADER", "VI.\nTHE MERCHANT'S PRIVILEGE DOES NOT APPLY"),
    ("PARA", '77. Plaintiff acknowledges that retailers in the Greater Bay Area, including Defendants, face genuine losses from retail theft.'),
    ("PARA", '78. Generalized concern about retail theft does not supply probable cause to detain any particular customer, and does not authorize a retailer to select which customers to detain on the basis of race.'),
    ("PARA", '79. A statistical or industry-wide loss problem is not a defense to discrimination against an individual customer. If it were, the Unruh Civil Rights Act would offer no protection in precisely the settings where it is most needed.'),
    ("PARA", '80. Here, the ordinary indicia of probable cause were absent: Plaintiff did not take or conceal any Ross merchandise, and no employee identified to Plaintiff any observed act of taking or concealment; Plaintiff entered holding the item openly; no Ross merchandise was identified to Plaintiff as missing; nothing was recovered; and no alarm sounded.'),
    ("PARA", "81. Penal Code section 490.5(f)(1) permits a merchant to detain a person for a reasonable time and in a reasonable manner only when the merchant has probable cause to believe the person to be detained is attempting unlawfully to take, or has unlawfully taken, merchandise from the merchant's premises."),
    ("PARA", "82. Defendants lacked probable cause to believe that Plaintiff had taken or was attempting to take any Ross merchandise. Because probable cause was absent, the merchant's privilege does not apply and the detention was unlawful."),
    ("PARA", "83. Separately and independently, the detention was not conducted in a reasonable manner or for a purpose authorized by the statute. Having initiated the detention, DOE 1 did not meaningfully investigate the suspicion she had asserted. She did not request the receipt, did not ask where the beverage had been purchased, did not verify whether the Sunnyvale Store stocked that product that evening, did not identify any missing merchandise, and did not articulate any observed act connecting the beverage to Ross. No merchandise was recovered, because there was none to recover. Whether a merchant's detention was reasonable in scope and manner is ordinarily a question of fact. (See Fermino v. Fedco, Inc. (1994) 7 Cal.4th 701.)"),
    ("HEADER", 'VII.\nPRESERVATION OF EVIDENCE'),
    ("PARA", '84. The surveillance recordings described above are central to the issues in this action. They will show whether Plaintiff entered the Sunnyvale Store carrying the beverage in open view, whether any employee observed him handle Ross merchandise, and how DOE 1 positioned herself at the exit.'),
    ("PARA", '85. By the filing and service of this Complaint, and by separate written notice, Plaintiff demands that Defendants preserve, and refrain from deleting, overwriting, recycling, or otherwise destroying, all surveillance video from every camera covering the entrance, sales floor, register area, and exit of the Sunnyvale Store for August 25, 2026, from 8:30 p.m. through 9:30 p.m.; all loss-prevention incident reports, stop logs, apprehension records, and shrink reports for that store; all loss-prevention policies, training materials, and outside-merchandise policies in effect on that date; and all personnel and complaint records concerning DOE 1.'),
    ("PARA", '86. Defendants are on notice that this evidence is relevant to pending litigation and that they are under a duty to preserve it.'),
    ("HEADER", 'VIII.\nFIRST CAUSE OF ACTION'),
    ("SUBHEAD", 'Violation of the Unruh Civil Rights Act (Civil Code sections 51, 51.5, and 52) (Against All Defendants)'),
    ("PARA", '87. Plaintiff realleges and incorporates by reference paragraphs 1 through 86, inclusive, as though fully set forth herein.'),
    ("PARA", '88. Civil Code section 51(b) provides that all persons within the jurisdiction of this State are free and equal, and no matter what their race, color, ancestry, national origin, or other protected characteristic, are entitled to the full and equal accommodations, advantages, facilities, privileges, or services in all business establishments of every kind whatsoever.'),
    ("PARA", '89. Civil Code section 51.5(a) provides that no business establishment of any kind whatsoever shall discriminate against any person in this State because of the race, color, or other protected characteristic of that person.'),
    ("PARA", '90. The Sunnyvale Store is a "business establishment" within the meaning of Civil Code sections 51 and 51.5. That term is construed in the broadest sense reasonably possible and plainly encompasses a retail store open to the general public.'),
    ("PARA", '91. The Corporate Defendants own, operate, and/or control the Sunnyvale Store and are business establishments within the meaning of the Act.'),
    ("PARA", '92. Plaintiff, as a customer who entered the Sunnyvale Store during business hours, was a member of the public entitled to the full and equal accommodations, advantages, facilities, privileges, and services of that business establishment.'),
    ("PARA", '93. Among the privileges and services to which Plaintiff was entitled were:'),
    ("LIST_ITEM", 'a. The ability to browse merchandise without being singled out for surveillance because of his race;'),
    ("LIST_ITEM", 'b. The ability to decline to purchase;'),
    ("LIST_ITEM", 'c. The ability to walk to the exit unobstructed; and'),
    ("LIST_ITEM", 'd. The ability to leave the store without being physically intercepted and interrogated as a presumed thief.'),
    ("PARA", '94. Defendants, acting through DOE 1 within the course and scope of her employment, denied Plaintiff those accommodations, advantages, facilities, privileges, and services.'),
    ("PARA", "95. Defendants did so intentionally and because of Plaintiff's race."),
    ("PARA", '96. A violation of the Unruh Act requires intentional discrimination. Such intent need not be proven by direct evidence and may be established through circumstantial evidence and the reasonable inferences that flow from the surrounding facts. The circumstantial evidence of intentional race-based selection is set forth in paragraph 73 above and is incorporated here.'),
    ("PARA", "97. Plaintiff further alleges that Defendants' conduct constituted the application of a facially neutral loss-prevention practice in an intentionally discriminatory manner: whatever Defendants' written policy may say about outside beverages, that practice was enforced against Plaintiff, a Black customer, in a manner in which it is not enforced against similarly situated non-Black customers."),
    ("PARA", "98. Race was a substantial motivating factor in Defendants' decision to intercept and detain Plaintiff. Defendants' asserted concern about retail theft is pretextual as applied to Plaintiff and, in any event, does not justify the race-based selection of whom to detain."),
    ("PARA", "99. Defendants' conduct was a substantial factor in causing Plaintiff's harm."),
    ("PARA", "100. As a direct and proximate result of Defendants' violation of the Unruh Civil Rights Act, Plaintiff has suffered actual damages, including emotional distress, humiliation, embarrassment, anxiety, indignation, and loss of dignity, in an amount to be proven at trial."),
    ("PARA", "101. Civil Code section 52(a) provides that whoever denies, aids or incites a denial, or makes any discrimination or distinction contrary to section 51 or 51.5 is liable for each and every offense for the actual damages, and any amount that may be determined by a jury, or a court sitting without a jury, up to a maximum of three times the amount of actual damage, but in no case less than four thousand dollars ($4,000), and any attorney's fees that may be determined by the court in addition thereto."),
    ("PARA", "102. Plaintiff is therefore entitled to recover his actual damages, up to three times his actual damages, and in no event less than four thousand dollars ($4,000) per offense, together with costs and any attorney's fees allowed by law."),
    ("PARA", '103. As alleged in paragraph 68 above, Plaintiff intends to patronize the Sunnyvale Store but is presently deterred by the practices alleged herein, and therefore faces a likelihood of future injury. Plaintiff is entitled to preventive relief pursuant to Civil Code section 52(c), and seeks an order requiring Defendants to:'),
    ("LIST_ITEM", 'a. Adopt, implement, and maintain a written policy prohibiting the use of race as a factor in loss-prevention surveillance, approach, and detention decisions;'),
    ("LIST_ITEM", 'b. Train all loss-prevention personnel and store employees at the Sunnyvale Store on that policy and on the probable-cause requirements of Penal Code section 490.5;'),
    ("LIST_ITEM", 'c. Train all loss-prevention personnel that customers may lawfully enter the store carrying food, beverages, or merchandise purchased elsewhere;'),
    ("LIST_ITEM", 'd. Adopt reasonable, nondiscriminatory loss-prevention procedures consistent with Penal Code section 490.5, including appropriate verification of ownership where the suspected item could have originated outside the store; and'),
    ("LIST_ITEM", 'e. Record and retain the date, asserted basis, and outcome of each loss-prevention stop at the Sunnyvale Store.'),
    ("PARA", "104. The conduct of DOE 1 was despicable and was carried out with a willful and conscious disregard of Plaintiff's rights, constituting malice and oppression within the meaning of Civil Code section 3294. Plaintiff is therefore entitled to punitive damages against DOE 1 in an amount sufficient to punish and deter. Plaintiff does not presently seek punitive damages against the Corporate Defendants, and will seek leave to amend to do so if discovery establishes that an officer, director, or managing agent authorized or ratified the conduct or the practices that produced it within the meaning of Civil Code section 3294(b)."),
    ("HEADER", 'IX.\nSECOND CAUSE OF ACTION'),
    ("SUBHEAD", 'False Imprisonment (Against All Defendants)'),
    ("PARA", '105. Plaintiff realleges and incorporates by reference paragraphs 1 through 104, inclusive, as though fully set forth herein.'),
    ("PARA", '106. DOE 1 intentionally deprived Plaintiff of his freedom of movement by physically stepping in front of him and blocking his path to the exit of the Sunnyvale Store.'),
    ("PARA", '107. Confinement for purposes of false imprisonment may be effected by physical barriers or by any means that a reasonable person would understand to restrict freedom of movement. Physical touching is not required.'),
    ("PARA", "108. DOE 1's conduct compelled Plaintiff to remain in the store for an appreciable period of time -- approximately three minutes -- against his will."),
    ("PARA", '109. Plaintiff did not consent to the confinement and was actually aware of it at the time it occurred.'),
    ("PARA", "110. The confinement was not privileged. Penal Code section 490.5(f)(1) permits a merchant to detain a person for a reasonable time and in a reasonable manner only when the merchant has probable cause to believe the person detained is attempting unlawfully to take, or has unlawfully taken, merchandise from the merchant's premises."),
    ("PARA", "111. Defendants had no probable cause to believe that Plaintiff had taken or was attempting to take any merchandise from the Sunnyvale Store. Plaintiff did not take or conceal any Ross merchandise, and no Defendant identified to Plaintiff any observed act of taking or concealment. Plaintiff entered the premises already holding the beverage in open view, and no Ross merchandise was ever identified as missing or in Plaintiff's possession."),
    ("PARA", '112. DOE 1\'s own statement that the store sells the beverage "sometimes" reflected uncertainty rather than knowledge. Even if the Sunnyvale Store does sometimes stock Celsius beverages, that a product is sometimes carried does not, absent an observed taking or concealment, supply probable cause to believe that this particular can was Ross merchandise unlawfully taken from the premises.'),
    ("PARA", "113. Because Defendants lacked probable cause, the merchant's detention privilege under Penal Code section 490.5(f) does not apply."),
    ("PARA", '114. Alternatively and in addition, and as alleged in paragraph 83 above, the detention was not conducted in a reasonable manner or for a purpose authorized by the statute, and therefore exceeded the scope of any privilege that might otherwise have existed.'),
    ("PARA", "115. Defendants' conduct was a substantial factor in causing Plaintiff harm."),
    ("PARA", '116. As a direct and proximate result of the false imprisonment, Plaintiff suffered damages including emotional distress, humiliation, indignity, embarrassment, and anxiety, in an amount to be proven at trial.'),
    ("PARA", '117. The Corporate Defendants are liable for the false imprisonment under the doctrine of respondeat superior, because DOE 1 was acting within the course and scope of her employment and was performing the very function -- loss prevention -- for which she was hired.'),
    ("PARA", '118. The conduct of DOE 1 was carried out with malice and oppression within the meaning of Civil Code section 3294, entitling Plaintiff to punitive damages against her, subject to the same reservation stated in paragraph 104 above.'),
    ("HEADER", 'X.\nTHIRD CAUSE OF ACTION'),
    ("SUBHEAD", 'Negligent Training and Supervision (Against the Corporate Defendants and Does 2 through 20)'),
    ("PARA", '119. Plaintiff realleges and incorporates by reference paragraphs 1 through 118, inclusive, as though fully set forth herein.'),
    ("PARA", '120. This cause of action is pleaded in the alternative to the intentional torts alleged above and does not depend on proof of discriminatory intent. Even if DOE 1 acted without racial motivation, the Corporate Defendants remain answerable for their own failure to exercise reasonable care in training and supervising the exercise of detention authority.'),
    ("PARA", '121. Civil Code section 1714(a) establishes the general duty of every person to exercise ordinary care in the management of his or her property and in his or her own conduct. The Corporate Defendants owed a duty of reasonable care to members of the public, including Plaintiff, who entered the Sunnyvale Store as a business invitee. That duty included the duty to exercise reasonable care in the training, supervision, and monitoring of loss-prevention personnel authorized to stop, question, and detain customers on the premises.'),
    ("PARA", '122. The Corporate Defendants entrusted loss-prevention personnel, including DOE 1, with authority to stop and detain customers. A merchant who delegates that authority to store-level personnel must take reasonable steps to see that it is exercised only on probable cause, only for the purposes Penal Code section 490.5 permits, and only in a reasonable manner.'),
    ("PARA", "123. Plaintiff pleads the following in the alternative. If DOE 1's conduct conformed to the loss-prevention practices the Corporate Defendants established and maintained at the Sunnyvale Store, then those practices were themselves unreasonable and the Corporate Defendants were negligent in adopting and maintaining them. If, on the other hand, DOE 1's conduct departed from the Corporate Defendants' written policies, then the Corporate Defendants were negligent in failing to train, supervise, monitor, and enforce those policies so as to make them effective in practice. Which of these is the case is presently within Defendants' exclusive knowledge."),
    ("PARA", '124. Plaintiff is informed and believes, and on that basis alleges, that the Corporate Defendants breached that duty in one or more of the following respects:'),
    ("LIST_ITEM", "a. Failing to train loss-prevention personnel on the probable-cause requirement of Penal Code section 490.5(f) and the limits of the merchant's detention privilege;"),
    ("LIST_ITEM", 'b. Failing to train loss-prevention personnel that a customer may lawfully enter the store carrying food, beverages, or merchandise purchased at a neighboring business;'),
    ("LIST_ITEM", "c. Failing to train loss-prevention personnel to make a non-obstructing inquiry, including a simple request for a receipt, before physically blocking a customer's egress;"),
    ("LIST_ITEM", "d. Failing to train loss-prevention personnel that a customer's race is not, and may never be, a factor in deciding whom to surveil, approach, or detain; and"),
    ("LIST_ITEM", 'e. Failing to supervise loss-prevention personnel at the Sunnyvale Store in the performance of these duties;'),
    ("LIST_ITEM", 'f. Failing to monitor, review, or audit customer stops made by loss-prevention personnel at the Sunnyvale Store, or to maintain any record from which an unreasonable or discriminatory pattern of stops could be detected and corrected; and'),
    ("LIST_ITEM", 'g. Failing to enforce whatever written loss-prevention policies the Corporate Defendants may have adopted, such that those policies did not govern conduct on the sales floor.'),
    ("PARA", "125. The content of Defendants' loss-prevention training materials, policies, and supervisory practices is within Defendants' exclusive possession and control. Plaintiff pleads these breaches on information and belief and will amend to conform to proof."),
    ("PARA", "126. It was reasonably foreseeable that the failures alleged above would result in customers being detained without probable cause and in a manner exceeding the merchant's privilege. The detention of Plaintiff is precisely the kind of harm that reasonable training and supervision are designed to prevent."),
    ("PARA", "127. The Corporate Defendants' breach was a substantial factor in causing the detention of Plaintiff and the harm he suffered."),
    ("PARA", '128. As a direct and proximate result, Plaintiff has suffered damages in an amount to be proven at trial.'),
    ("HEADER", 'XI.\nPRAYER FOR RELIEF'),
    ("PARA", 'WHEREFORE, Plaintiff BRENDAN NGWA NFORBI prays for judgment against Defendants, and each of them, as follows:'),
    ("SUBHEAD", 'On the First Cause of Action (Unruh Civil Rights Act)'),
    ("LIST_ITEM", '1. For actual damages according to proof at trial;'),
    ("LIST_ITEM", '2. For damages pursuant to Civil Code section 52(a) in an amount up to three times actual damages, but in no event less than four thousand dollars ($4,000) for each and every offense;'),
    ("LIST_ITEM", '3. For preventive relief pursuant to Civil Code section 52(c), including the relief described in paragraph 103 above;'),
    ("SUBHEAD", 'On the Second Cause of Action (False Imprisonment)'),
    ("LIST_ITEM", '4. For general and special damages according to proof at trial;'),
    ("SUBHEAD", 'On the Third Cause of Action (Negligent Training and Supervision)'),
    ("LIST_ITEM", '5. For general and special damages according to proof at trial;'),
    ("SUBHEAD", 'On All Causes of Action'),
    ("LIST_ITEM", '6. For exemplary and punitive damages against DOE 1 pursuant to Civil Code section 3294, in an amount sufficient to punish and deter, according to proof;'),
    ("LIST_ITEM", "7. For attorney's fees pursuant to Civil Code section 52(a) and Code of Civil Procedure section 1021.5, to the extent Plaintiff is represented by counsel at any stage of this action;"),
    ("LIST_ITEM", '8. For prejudgment and post-judgment interest as permitted by law;'),
    ("LIST_ITEM", '9. For costs of suit incurred herein; and'),
    ("LIST_ITEM", '10. For such other and further relief as the Court deems just and proper.'),
    ("PARA", 'Plaintiff alleges that the total amount in controversy exceeds thirty-five thousand dollars ($35,000), exclusive of interest and costs, and that this action is properly classified as an unlimited civil case.'),
    ("HEADER", 'XII.\nDEMAND FOR JURY TRIAL'),
    ("PARA", '129. Plaintiff hereby demands a trial by jury on all causes of action and issues so triable.'),
]


def _signature_block(d: PleadingPaper, exec_date: str, *, respectfully: bool) -> None:
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
    d.write_wrapped("I, BRENDAN NGWA NFORBI, declare:", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in the above-entitled action. I have read the foregoing "
        "VERIFIED COMPLAINT FOR DAMAGES AND INJUNCTIVE RELIEF and know its contents. "
        "The matters stated therein are true of my own knowledge, except as to those "
        "matters stated on information and belief, and as to those matters I believe "
        "them to be true.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the State of California "
        "that the foregoing is true and correct.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        f"Executed on {exec_date}, at Sunnyvale, California.",
        first_indent=36,
    )
    d.ensure_space(10)
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
