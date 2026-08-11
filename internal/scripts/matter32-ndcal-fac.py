# ==========================================================
# NGWA NFORBI v. MEZA-GONZALEZ and MELANO -- FIRST AMENDED COMPLAINT
# USDC N.D. Cal. (Matter 32)
#
# Source of record for this filing. The PDF under
# internal/public/documents/matter-32/ndcal/ is generated from this
# script -- edit the CONTENT below and re-run, never hand-patch the PDF.
#
#   python3 internal/scripts/matter32-ndcal-fac.py [OUT_PDF]
# ==========================================================
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import PleadingPaper, CONTENT_LEFT

DOC_TITLE_FOOTER = 'FIRST AMENDED COMPLAINT FOR DAMAGES -- NGWA NFORBI v. MEZA-GONZALEZ, ET AL. (N.D. Cal.)'

DEFAULT_OUT = os.path.join(
    SCRIPT_DIR, "..", "public", "documents", 'matter-32', "ndcal", 'FAC Ngwa Nforbi v Meza-Gonzalez and Melano NDCal (Aug 11 2026).pdf'
)

ATTORNEY_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

# (text, bold, italic) -- blank strings are spacer rows
CAPTION_LEFT = [
    ('BRENDAN NGWA NFORBI,', True, False),
    ('', False, False),
    ('                          Plaintiff,', False, False),
    ('', False, False),
    ('       v.', False, False),
    ('', False, False),
    ('SANTIAGO MEZA-GONZALEZ', True, False),
    ('(CHP Badge #023295), in his individual', True, False),
    ('capacity; JOSE MELANO (CHP Badge', True, False),
    ('#023054), in his individual capacity;', True, False),
    ('and DOES 1 through 10, inclusive,', True, False),
    ('', False, False),
    ('                          Defendants.', False, False),
]

CAPTION_RIGHT = [
    ('Case No. __________________', False, False),
    ('', False, False),
    ('FIRST AMENDED COMPLAINT', True, False),
    ('FOR DAMAGES', True, False),
    ('', False, False),
    ('(42 U.S.C. § 1983)', False, False),
    ('', False, False),
    ('(1) 4th Amend. -- Judicial', False, False),
    ('       Deception;', False, False),
    ('(2) 14th Amend. -- Fabrication of', False, False),
    ('       Evidence;', False, False),
    ('(3) 4th Amend. -- Unlawful Arrest;', False, False),
    ('(4) 4th Amend. -- Unlawful Entry;', False, False),
    ('(5) 4th Amend. -- Unlawful Search;', False, False),
    ('(6) 1st Amend. -- Retaliation.', False, False),
    ('', False, False),
    ('[DEMAND FOR JURY TRIAL]', True, False),
]

CONTENT = [
    ('PARA', 'Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, files this First Amended Complaint against Defendants SANTIAGO MEZA-GONZALEZ and JOSE MELANO, in their individual capacities, and alleges as follows:'),
    ('HEADER', 'INTRODUCTION'),
    ('PARA', "1. This is a civil rights action under 42 U.S.C. section 1983 arising from an arrest on November 1, 2024, on the shoulder of Interstate 580 East in Livermore, Alameda County, California. Plaintiff Brendan Ngwa Nforbi, a commercial truck driver holding a Class A Commercial Driver's License (No. F7953179), was parked and asleep in his vehicle when California Highway Patrol Officers Santiago Meza-Gonzalez and Jose Melano approached. Over the course of two hours -- captured in their entirety on the officers' own dashcam recording (CHP Case No. RJ68845) -- the officers opened the vehicle without consent or warrant, identified the only cup in the vehicle as containing urine, continued the investigation after the basis for their initial suspicion had dissipated, arrested Plaintiff within eighteen seconds of his exercise of the statutory right to decline a voluntary preliminary alcohol screening test, and then generated sworn statements containing material representations that are contradicted by the same recording in the CHP's own custody."),
    ('PARA', '2. After the arrest, Officer Meza-Gonzalez executed under penalty of perjury a DS-367 Officer\'s Statement and a CHP Arrest-Investigation Report, both of which were used to obtain a blood-draw warrant from a magistrate, to initiate a one-year administrative suspension of Plaintiff\'s commercial driving privileges, and to refer criminal charges to the Alameda County District Attorney. The DS-367 and arrest report contain at least four representations that are materially contradicted by the dashcam recording: a claimed "strong distinct odor of an alcoholic beverage" that neither officer ever verbalizes on the recording; a characterization of Plaintiff\'s speech as "slurred" when the recording captures extended coherent conversation; a claim that Plaintiff was "very confused and disoriented" when the recording shows him correctly identifying his location and reading distant signage; and a checked box for "Beverage Present: Yes" when the only liquid the officers found was, in Officer Melano\'s own contemporaneous words on the recording, "piss." Four days later, CHP itself issued a Penal Code section 851.6 Detention Certificate reclassifying the event as "a detention only, not an arrest" for "insufficient grounds." The Alameda County District Attorney declined to file any charges.'),
    ('PARA', "3. Plaintiff brings six claims against Defendants in their individual capacities: judicial deception in support of a blood-draw warrant; deliberate fabrication of evidence; unlawful arrest without probable cause; unlawful warrantless entry into a private vehicle; unlawful search; and First Amendment retaliation for exercising the statutory right to refuse a voluntary preliminary alcohol screening test. Plaintiff seeks compensatory and punitive damages and reasonable attorney's fees under 42 U.S.C. section 1988."),
    ('HEADER', 'JURISDICTION AND VENUE'),
    ('PARA', '4. This Court has original subject-matter jurisdiction under 28 U.S.C. section 1331 (federal question) and 28 U.S.C. section 1343(a)(3) and (a)(4) (civil rights). The claims arise under the First, Fourth, and Fourteenth Amendments to the United States Constitution, as enforced through 42 U.S.C. section 1983.'),
    ('PARA', '5. Venue is proper in the Northern District of California under 28 U.S.C. section 1391(b)(2). All events giving rise to this action occurred in Livermore and Dublin, Alameda County, California, within this District.'),
    ('PARA', '6. Under Civil Local Rule 3-2(c) and (d), this action arose in Alameda County and is appropriately assigned to the San Francisco Division or the Oakland Division.'),
    ('HEADER', 'PARTIES'),
    ('PARA', "7. Plaintiff BRENDAN NGWA NFORBI is a natural person and a resident of the County of San Joaquin, State of California. At all relevant times, he held a valid California Class A Commercial Driver's License (No. F7953179) with endorsements for doubles/triples and tank vehicles."),
    ('PARA', '8. Defendant SANTIAGO MEZA-GONZALEZ (CHP Badge #023295) is a sworn peace officer employed by the California Highway Patrol, assigned to the CHP Dublin Area. He was acting under color of state law at all relevant times. He is sued in his individual capacity only.'),
    ('PARA', '9. Defendant JOSE MELANO (CHP Badge #023054) is a sworn peace officer employed by the California Highway Patrol, assigned to the CHP Dublin Area. He was acting under color of state law at all relevant times. He is sued in his individual capacity only.'),
    ('PARA', '10. The true names of Defendants DOES 1 through 10 are presently unknown. On information and belief, each participated in, approved, or acquiesced in the conduct alleged herein. Each is sued in his or her individual capacity. Plaintiff will seek leave to amend when their identities are ascertained.'),
    ('HEADER', 'FACTUAL ALLEGATIONS'),
    ('SUBHEAD', 'A. Plaintiff Was Lawfully Parked and Asleep'),
    ('PARA', "11. On the evening of October 31, 2024, and into the early hours of November 1, 2024, Plaintiff was driving a rented gray Tesla Model Y eastbound on Interstate 580. Feeling fatigued, he exited active travel lanes and parked on the right shoulder just west of the Isabel Avenue exit in Livermore, Alameda County. He then rested in the driver's seat. He was not driving. No officer observed him in volitional movement of the vehicle."),
    ('PARA', "12. Plaintiff is a professional commercial truck driver. Pulling off the road to rest when fatigued is consistent with federal Hours-of-Service principles and with CHP's own public safety guidance to drowsy motorists."),
    ('SUBHEAD', "B. The Officers' Pre-Contact Hypothesis"),
    ('PARA', "13. At approximately 00:54:36, the CHP patrol vehicle's dashcam recording activated as it came to a stop behind Plaintiff's parked Tesla. The recording ran continuously through approximately 01:57:10, capturing the entirety of the encounter."),
    ('PARA', '14. At 00:55:53, before either officer had approached the vehicle, Officer Melano remarked on the recording: "It\'s a rental. Huh." At 00:56:05, both officers approached and peered through the windows with flashlights while Plaintiff remained asleep inside. At 00:56:07, Melano stated: "It wasn\'t here earlier when we passed by."'),
    ('PARA', '15. At 00:56:09 -- before either officer had spoken a word to Plaintiff, before Plaintiff was awake, and before any welfare observation had been made -- Officer Melano stated on the recording: "I think it\'s booze." That statement, directed at a cup visible through the vehicle window, was formed before any contact with Plaintiff and before any observation of his condition.'),
    ('SUBHEAD', 'C. Warrantless Entry'),
    ('PARA', "16. At 00:56:43, Officer Melano opened the front passenger-side door of Plaintiff's vehicle. Plaintiff was still asleep. He had not consented to entry. No warrant had been obtained. No exigent circumstance -- no medical emergency, no ongoing crime, no fire, no destruction of evidence, no hot pursuit -- was present or articulated. No other basis for the entry was articulated on the recording."),
    ('SUBHEAD', 'D. The Cup Is Identified as Urine;\nthe Initial Suspicion Dissipates'),
    ('PARA', '17. Between 00:58:49 and 00:59:07, Officer Melano seized the cup from the vehicle interior, smelled it, and identified its contents on the recording:'),
    ('PARA', 'Melano: "Is it water? No this is piss. This is pee."'),
    ('PARA', 'Plaintiff: "I don\'t know what that is."'),
    ('PARA', 'Melano: "I\'m telling you it\'s piss. It smells like piss."'),
    ('PARA', "18. Officer Melano's own contemporaneous identification of the cup's contents as urine is inconsistent with his earlier hypothesis that the cup contained alcohol. Whatever investigative suspicion the cup had generated dissipated at the moment the officer handling it identified it as something other than an alcoholic beverage and said so aloud."),
    ('SUBHEAD', 'E. Continued Detention, Field Sobriety Exercises,\nand PAS Advisement'),
    ('PARA', '19. The officers did not terminate the encounter. They ordered Plaintiff out of the vehicle onto uneven ground and administered field sobriety exercises. Officer Melano acknowledged on the recording that the ground conditions were not suitable for reliable FST administration and declined to perform certain balance-dependent exercises for that reason.'),
    ('PARA', '20. Throughout the encounter, Plaintiff spoke coherently and articulately. The dashcam audio captures him spelling his surname on request, discussing the alternator design of the rental Tesla, explaining CDL fatigue protocols, and correctly identifying his location as Livermore. At no point in over two hours of continuous recording does either officer verbalize any observation of an alcohol odor emanating from Plaintiff.'),
    ('PARA', '21. At 01:10:54, Officer Meza-Gonzalez advised Plaintiff that the preliminary alcohol screening ("PAS") test was voluntary: "You\'re not required to do this." That advisement is legally accurate. Under California Vehicle Code section 23612(i), a PAS is a preliminary investigative tool, and a driver not on DUI probation may lawfully decline it.'),
    ('PARA', '22. At 01:11:03, Officer Meza-Gonzalez stated on the recording: "If you choose to not consent to it, then it\'ll be up to my discretion whether I put you under arrest for DUI or not." That statement, captured on the officers\' own recording, expressly conditioned the arrest decision on whether Plaintiff consented to or refused the voluntary test.'),
    ('SUBHEAD', 'F. PAS Refusal and Immediate Arrest'),
    ('PARA', '23. Plaintiff declined the PAS test.'),
    ('PARA', '24. At 01:11:15 through 01:11:33 -- eighteen seconds after the refusal -- Officer Meza-Gonzalez placed Plaintiff under arrest. No new observation or piece of evidence intervened between the refusal and the arrest. The temporal sequence is captured on the recording.'),
    ('SUBHEAD', 'G. The DS-367 and Arrest Report:\nFour Material Contradictions with the Dashcam'),
    ('PARA', "25. Following the arrest, Defendant Meza-Gonzalez prepared, executed under penalty of perjury, and submitted to DMV, to the reviewing magistrate, and to the Alameda County District Attorney: (a) a DS-367 Age 21 and Older Officer's Statement; and (b) a CHP Arrest-Investigation Report (Case No. RJ68845)."),
    ('PARA', '26. Each document contains representations that are materially contradicted by the dashcam recording:'),
    ('LIST_ITEM', '(a) Odor. The DS-367 and arrest report state Meza-Gonzalez detected a "strong distinct odor of an alcoholic beverage" from Plaintiff. In over two hours of continuous dashcam audio, neither officer verbalizes any observation of an alcohol odor at any point. Officers routinely narrate significant observations on dashcam -- Melano narrates his cup hypothesis (00:56:09), his urine identification (00:58:49-00:59:07), and vehicle details (00:55:53) -- but neither officer narrates detecting an alcohol odor.'),
    ('LIST_ITEM', '(b) Speech. The DS-367 characterizes Plaintiff\'s speech as "slurred." The recording captures Plaintiff in extended coherent conversation, including spelling his surname letter-by-letter and discussing mechanical details of the rental vehicle.'),
    ('LIST_ITEM', '(c) Orientation. The arrest report states Plaintiff "seemed very confused and disoriented." The recording captures Plaintiff correctly identifying his location as Livermore and reading distant highway signage.'),
    ('LIST_ITEM', '(d) Beverage. The DS-367 contains a checked box for "Beverage Present: Yes." The only liquid the officers found and discussed on the recording was identified by Officer Melano as urine, not a beverage.'),
    ('PARA', '27. The arrest report also omits material facts: that the suspected alcohol in the cup was identified on the recording as urine; that Officer Melano declined to administer certain FSTs due to ground conditions; that Officer Meza-Gonzalez expressly advised Plaintiff the PAS was voluntary; and that no officer had observed Plaintiff driving or in volitional control of the vehicle.'),
    ('PARA', '28. Of the four contradictions, the "Beverage Present" entry is the most objectively verifiable: the officers\' own contemporaneous words on their own recording identify the only liquid as urine, and the DS-367 checkbox characterizes it as a beverage. The odor, speech, and orientation entries are experiential observations that were not verbalized on the recording; Plaintiff alleges they are materially contradicted by the objective record, and their truth or falsity is a question the recording can help resolve.'),
    ('SUBHEAD', 'H. The Blood-Draw Warrant and Forced Extraction'),
    ('PARA', "29. Based on the DS-367 and arrest report, a magistrate authorized a warrant for the involuntary extraction of Plaintiff's blood. Plaintiff was transported to the CHP Dublin Area office, where a blood sample was forcibly drawn pursuant to that warrant. A compelled blood draw is a significant bodily intrusion within the meaning of the Fourth Amendment. Missouri v. McNeely, 569 U.S. 141, 148 (2013)."),
    ('PARA', '30. If the four contradicted representations identified in paragraph 26 are set aside, and if the omitted facts identified in paragraph 27 are restored, the warrant application would have reflected: a commercial driver parked and asleep on a highway shoulder; a cup identified by the investigating officer as urine; coherent, oriented conversation; no verbalized alcohol odor; and refusal of a test the officer had just described as voluntary. Whether those facts, standing alone, would have supported probable cause for a blood-draw warrant is a question that should be resolved on a developed record, not on the pleadings.'),
    ('SUBHEAD', 'I. Booking and Extended Detention'),
    ('PARA', "31. Following the blood extraction, Plaintiff was transported to and booked at Santa Rita Jail in Dublin, California. A parole hold was placed based on the arrest report, extending Plaintiff's custodial confinement beyond the initial arrest."),
    ('SUBHEAD', "J. CHP's Subsequent Reclassification:\nThe Penal Code Section 851.6 Detention Certificate"),
    ('PARA', '32. On November 5, 2024, the Dublin CHP issued a Detention Certificate under California Penal Code section 851.6, referencing CHP Case No. RJ68845. The Certificate states that Plaintiff\'s taking into custody "was a detention only, not an arrest" and that he was released under Penal Code section 849(b)(1) for "insufficient grounds for making a criminal complaint." By operation of Penal Code sections 849(c) and 849.5, the encounter is thereafter not deemed an arrest but a detention only.'),
    ('PARA', "33. The Detention Certificate is a subsequent official reclassification by the arresting agency itself. It does not, standing alone, establish that the arrest violated the Fourth Amendment at the moment it occurred. It does, however, constitute contemporaneous evidence from the agency best positioned to evaluate the encounter -- evidence consistent with and corroborative of Plaintiff's allegation that the arrest lacked probable cause."),
    ('SUBHEAD', "K. The District Attorney's Declination"),
    ('PARA', '34. CHP referred charges to the Alameda County District Attorney under Vehicle Code sections 23152(a), 23152(b), and 23578. The District Attorney declined to file any accusatory pleading. No criminal case was initiated.'),
    ('SUBHEAD', 'L. Alias Note, Related Actions, and Prior Proceedings'),
    ('PARA', '35. Plaintiff has appeared in prior court and administrative proceedings arising from this incident under the name variant "Brendan Ngehsi Newanforbi." That is the same individual as Plaintiff in this action. This Complaint uses "Brendan Ngwa Nforbi" throughout except where quoting from a prior record. In a related action in this District, N.D. Cal. Case No. 4:26-cv-05953-ASK, United States Magistrate Judge Ajay S. Krishnan screened a complaint resting on a substantially overlapping factual record and found it sufficient to proceed under 28 U.S.C. section 1915(e). A prior action arising from the same November 1, 2024 incident, filed in the Eastern District of California, has been voluntarily dismissed without prejudice. This action is not duplicative of any pending proceeding.'),
    ('SUBHEAD', 'M. Damages'),
    ('PARA', "36. As a direct and proximate result of Defendants' conduct, Plaintiff has suffered:"),
    ('LIST_ITEM', '(a) Loss of liberty from custodial confinement at the roadside, at the CHP Dublin Area office, and at Santa Rita Jail, including extended confinement under a parole hold predicated on the arrest report;'),
    ('PARA', '(b) A compelled blood extraction at the CHP Dublin Area office;'),
    ('LIST_ITEM', "(c) Loss of employment and earning capacity as a Class A commercial driver. At the time of the November 1, 2024 incident, Plaintiff had just commenced a dedicated route assignment with Lily Transportation (Toyota Dedicated, San Ramon, California) through Centerline Drivers, a staffing company, at a regular rate of $33.35 per hour and a premium/overtime rate of $50.03 per hour, as reflected in the contemporaneous Centerline wage notice dated October 31, 2024. Using a conservative schedule of forty regular hours and twenty overtime hours per week -- consistent with dedicated regional truck driving work -- Plaintiff's lost earnings from November 1, 2024 through the filing of this Complaint (approximately 92 weeks) exceed $214,000. This figure does not include lost employment benefits, future impairment of earning capacity, or other consequential economic losses;"),
    ('LIST_ITEM', "(d) A one-year administrative-per-se suspension of Plaintiff's Class A Commercial Driver's License (Feb. 20, 2025 through Feb. 19, 2026), with an accompanying one-year commercial disqualification, together with a three-year SR-22 financial-responsibility requirement (annual premiums of $281.28), for which Plaintiff's filing became effective May 18, 2026 and whose maintenance period therefore extends through approximately May 2029, and a $125.00 CDL reissue fee;"),
    ('PARA', '(e) Vehicle towing and impound fees; and'),
    ('LIST_ITEM', "(f) Emotional distress, anxiety, humiliation, sleep disturbance, and reputational injury from having his professional reputation damaged by sworn statements that are materially contradicted by the officers' own contemporaneous recording."),
    ('PARA', '37. The DS-367 was a material statutory and evidentiary basis for initiation and adjudication of the APS proceeding. Plaintiff alleges that the materially false representations in the DS-367 foreseeably caused or materially contributed to the resulting suspension of his commercial driving privileges. The wage loss is a direct and foreseeable consequence of that suspension. The total economic damages, including lost wages, benefits, and out-of-pocket expenses, exceed $250,000, excluding emotional distress and punitive damages to be proven at trial.'),
    ('HEADER', 'FIRST CAUSE OF ACTION'),
    ('SUBHEAD', 'Fourth Amendment -- Judicial Deception and Unlawful\nBodily Intrusion Under a Warrant Obtained Through\nMaterially False or Misleading Statements\n(42 U.S.C. § 1983 -- Against Defendant Meza-Gonzalez and DOES 1-10)'),
    ('PARA', '38. Plaintiff re-alleges paragraphs 1 through 37.'),
    ('PARA', '39. An officer violates the Fourth Amendment by submitting a warrant application containing statements that are deliberately or recklessly false, or that omit material facts, if the application -- stripped of the false statements and supplemented with the omitted facts -- would not support probable cause. Franks v. Delaware, 438 U.S. 154, 155-56 (1978); Chism v. Washington State, 661 F.3d 380, 386 (9th Cir. 2011).'),
    ('PARA', '40. On information and belief, Defendant Meza-Gonzalez executed the DS-367 and arrest report under penalty of perjury and submitted them, or caused them to be submitted, to the reviewing magistrate as the evidentiary basis for the blood-draw warrant application. The challenged representations identified in paragraph 26 were material to the probable-cause determination. When those representations are set aside and the omitted facts identified in paragraph 27 are restored, the remaining application does not plausibly support probable cause to believe Plaintiff was driving under the influence. Benavidez v. County of San Diego, 993 F.3d 1134, 1146-47 (9th Cir. 2021) (applying Franks corrected-affidavit test).'),
    ('PARA', '41. Defendant Meza-Gonzalez acted with at least reckless disregard for the truth. An officer who executes a sworn statement while a contemporaneous recording of the same encounter -- stored on his own patrol vehicle -- contains information materially inconsistent with that sworn statement acts with reckless disregard, at minimum. The right to be free from a warrant obtained through materially false or misleading statements was clearly established before November 1, 2024. Franks, 438 U.S. at 155-56; Chism, 661 F.3d at 386; Galbraith v. County of Santa Clara, 307 F.3d 1119, 1126 (9th Cir. 2002).'),
    ('PARA', '42. As a direct and proximate result, Plaintiff suffered a compelled blood extraction without valid probable cause, and the further damages alleged in paragraphs 36-37.'),
    ('HEADER', 'SECOND CAUSE OF ACTION'),
    ('SUBHEAD', 'Fourteenth Amendment -- Deliberate Fabrication of Evidence\n(42 U.S.C. § 1983 -- Against Defendant Meza-Gonzalez and DOES 1-10)'),
    ('PARA', '43. Plaintiff re-alleges paragraphs 1 through 37.'),
    ('PARA', "44. The Fourteenth Amendment prohibits state actors from deliberately fabricating evidence and using it to bring about deprivations of liberty or property. Devereaux v. Abbey, 263 F.3d 1070, 1076 (9th Cir. 2001) (en banc). Qualified immunity is not available to officers who deliberately fabricate evidence. Costanich v. Dep't of Social & Health Servs., 627 F.3d 1101, 1115-16 (9th Cir. 2010)."),
    ('PARA', "45. Defendant Meza-Gonzalez executed sworn statements containing the four materially contradicted representations identified in paragraph 26. Those statements were used to obtain the blood-draw warrant, to sustain custodial confinement (including under a parole hold), to initiate and sustain the DMV administrative-per-se suspension of Plaintiff's Class A CDL, and to refer charges to the District Attorney."),
    ('PARA', "46. Defendant Meza-Gonzalez personally participated in the encounter the dashcam recorded. He personally heard Plaintiff's speech. He personally observed Plaintiff's demeanor and orientation. He was present when Officer Melano identified the cup's contents as urine. He personally administered the PAS advisement and effected the arrest. He then executed sworn statements containing representations materially inconsistent with what he had personally observed and what his own agency's recording captured. An officer who knowingly and deliberately includes materially false representations in sworn investigative documents violates the Fourteenth Amendment. Spencer v. Peters, 857 F.3d 789, 798 (9th Cir. 2017) (deliberate mischaracterization of evidence in investigative reports); Devereaux, 263 F.3d at 1076."),
    ('PARA', '47. As a direct and proximate result, Plaintiff has suffered the damages alleged in paragraphs 36-37.'),
    ('HEADER', 'THIRD CAUSE OF ACTION'),
    ('SUBHEAD', 'Fourth Amendment -- Unlawful Arrest and Detention\n(42 U.S.C. § 1983 -- Against Both Defendants and DOES 1-10)'),
    ('PARA', '48. Plaintiff re-alleges paragraphs 1 through 37.'),
    ('PARA', '49. The Fourth Amendment requires probable cause for a warrantless arrest. Probable cause exists when the facts and circumstances known to the officer at the time are sufficient for a prudent person to believe that the suspect has committed a crime. Devenpeck v. Alford, 543 U.S. 146, 152 (2004).'),
    ('PARA', '50. At the moment of arrest (01:11:15-01:11:33), the facts known to the officers, as reflected on the recording, included: Plaintiff was parked and asleep when contacted; the only suspected "beverage" had been identified as urine; Plaintiff had spoken coherently and identified his location; no officer had verbalized an alcohol odor; Officer Melano had declined to administer certain FSTs due to ground conditions; and Plaintiff had exercised his statutory right under Vehicle Code section 23612(i) to decline a voluntary PAS test. No new observation or evidence intervened between the PAS refusal and the arrest. Plaintiff\'s exercise of the statutory right to refuse the PAS test could not itself supply the probable cause that was otherwise absent. Thomas v. Dillard, 818 F.3d 864, 884-85 (9th Cir. 2016) (refusal to consent to a search cannot create reasonable suspicion or establish probable cause). Moreover, officers evaluating probable cause may not disregard facts tending to dissipate it. Sialoi v. City of San Diego, 823 F.3d 1223, 1233 (9th Cir. 2016) (continued seizure unlawful after officers learned that suspected weapon was a toy; applying United States v. Lopez, 482 F.3d 1067 (9th Cir. 2007)). Here, Officer Melano\'s contemporaneous identification of the cup\'s contents as urine was a fact tending to dissipate the suspicion that had prompted the investigation, and Defendants disregarded it.'),
    ('PARA', '51. CHP\'s subsequent issuance of the Penal Code section 851.6 Detention Certificate -- reclassifying the event as a detention for "insufficient grounds" -- and the Alameda County District Attorney\'s declination to file charges are consistent with and corroborative of Plaintiff\'s allegation that the arrest lacked probable cause.'),
    ('PARA', '52. The right to be free from arrest without probable cause was clearly established well before November 1, 2024. Beck v. Ohio, 379 U.S. 89 (1964); Devenpeck, 543 U.S. at 152.'),
    ('PARA', '53. Defendant Meza-Gonzalez personally effected the arrest. Defendant Melano was an integral participant: he conducted the initial vehicle entry and search, administered the field sobriety exercises, communicated his investigative findings to Meza-Gonzalez throughout the encounter, and remained present and actively engaged in the joint investigation up to and through the moment of arrest without objection or intervention. The arrest was the culmination of a joint investigation in which both officers participated and to which both officers contributed. As a direct and proximate result, Plaintiff was subjected to custodial confinement, including loss of liberty at the roadside, at the CHP Dublin Area office, and at Santa Rita Jail.'),
    ('HEADER', 'FOURTH CAUSE OF ACTION'),
    ('SUBHEAD', 'Fourth Amendment -- Unlawful Warrantless Entry\n(42 U.S.C. § 1983 -- Against Defendant Melano and DOES 1-10)'),
    ('PARA', '54. Plaintiff re-alleges paragraphs 1 through 37.'),
    ('PARA', '55. Opening the door of a private vehicle and entering or reaching into its interior constitutes a Fourth Amendment search. United States v. Ngumezi, 980 F.3d 1285, 1289 (9th Cir. 2020) (officer who opened passenger door, leaned inside, and questioned driver conducted a Fourth Amendment search). A warrantless search is presumptively unreasonable absent consent or a recognized exception.'),
    ('PARA', '56. At 00:56:43, Defendant Melano opened the front passenger-side door of Plaintiff\'s vehicle while Plaintiff was asleep. No consent was given. No warrant existed. No objectively observable facts indicated that Plaintiff required immediate medical assistance: the dashcam shows a vehicle parked intact on the shoulder with no visible damage, no smoke or fire, no crash debris, and an occupant in a normal resting posture. The officers\' own words on the recording preceding the entry ("It\'s a rental," "It wasn\'t here earlier," "I think it\'s booze") reflect investigative interest, not a response to an observed emergency. Ngumezi, 980 F.3d at 1289.'),
    ('PARA', '57. The right to be free from warrantless entry into a vehicle absent consent, exigency, or an applicable exception was clearly established before November 1, 2024. Ngumezi, 980 F.3d at 1289.'),
    ('PARA', "58. Defendant Melano personally opened the door. Defendant Meza-Gonzalez was present and did not intervene. As a direct and proximate result of the warrantless entry, Plaintiff's constitutionally protected privacy interest in his vehicle was violated, and the entry initiated the chain of events leading to the subsequent search, prolonged detention, arrest, and forced blood extraction."),
    ('HEADER', 'FIFTH CAUSE OF ACTION'),
    ('SUBHEAD', 'Fourth Amendment -- Unlawful Search\n(42 U.S.C. § 1983 -- Against Both Defendants and DOES 1-10)'),
    ('PARA', '59. Plaintiff re-alleges paragraphs 1 through 37.'),
    ('PARA', "60. Following the warrantless entry, Defendant Melano reached into the vehicle, seized the cup from the center console area, smelled it, and examined its contents. Defendant Meza-Gonzalez directed Plaintiff's attention and movements during the encounter while Melano conducted the physical search. No consent was given. No warrant existed. No exigent circumstance was present."),
    ('PARA', "61. To the extent probable cause to search arose from Melano's observation of the cup, any such basis was materially undermined when Melano personally seized, smelled, and identified the liquid as urine (00:58:49-00:59:07). The continuing warrantless search of the vehicle thereafter required some independent lawful justification. None was present. Ngumezi, 980 F.3d at 1289."),
    ('PARA', '62. The right to be free from a warrantless vehicle search absent probable cause, consent, or an applicable exception was clearly established before November 1, 2024. Ngumezi, 980 F.3d at 1289.'),
    ('PARA', "63. As a direct and proximate result of the unlawful search, evidence obtained from Plaintiff's vehicle was used to prolong the detention and to support the investigation that culminated in the arrest and forced blood extraction."),
    ('HEADER', 'SIXTH CAUSE OF ACTION'),
    ('SUBHEAD', 'First Amendment -- Retaliation for Exercise of\nStatutory Right to Refuse a Voluntary\nPreliminary Alcohol Screening Test\n(42 U.S.C. § 1983 -- Against Both Defendants and DOES 1-10)'),
    ('PARA', '64. Plaintiff re-alleges paragraphs 1 through 37.'),
    ('PARA', '65. To state a First Amendment retaliation claim, a plaintiff must allege (i) constitutionally protected activity; (ii) an adverse action; and (iii) a causal connection. Nieves v. Bartlett, 587 U.S. 391, 398-99 (2019); Ballentine v. Tucker, 28 F.4th 54, 62 (9th Cir. 2022).'),
    ('PARA', '66. Plaintiff engaged in protected activity. Under California Vehicle Code section 23612(i), a PAS test is a voluntary investigative tool for drivers not on DUI probation. Refusal carries no statutory consequence. Officer Meza-Gonzalez confirmed its voluntary nature at timestamp 01:10:54: "You\'re not required to do this." The exercise of a statutory right to refuse a voluntary investigative procedure is constitutionally protected conduct. Ballentine, 28 F.4th at 62; Camara v. Municipal Court, 387 U.S. 523, 528-33 (1967).'),
    ('PARA', '67. Defendants took an adverse action. At timestamp 01:11:15, Plaintiff declined the PAS test. Eighteen seconds later, at timestamp 01:11:33, Officer Meza-Gonzalez placed Plaintiff under arrest. No new evidence of impairment was observed or articulated between the refusal and the arrest.'),
    ('PARA', '68. The arrest was causally connected to the refusal. The temporal proximity -- eighteen seconds -- supports an inference of causation. That inference is reinforced by Officer Meza-Gonzalez\'s own statement at timestamp 01:11:03, captured on the dashcam recording: "If you choose to not consent to it, then it\'ll be up to my discretion whether I put you under arrest for DUI or not." That statement, made moments before the refusal and arrest, expressly conditioned the arrest decision on whether Plaintiff consented to or refused the voluntary test.'),
    ('PARA', '69. Nieves does not bar this claim. Under Nieves, a retaliatory-arrest claim survives even if probable cause existed if the plaintiff provides objective evidence that similarly situated individuals who did not engage in the same protected conduct were not arrested. 587 U.S. at 407; see also Gonzalez v. Trevino, 602 U.S. 653 (2024) (plaintiff need not identify virtually identical comparator but must provide objective evidence of differential treatment). Here, the PAS test is statutorily voluntary under section 23612(i) and refusal carries no statutory penalty; drivers who comply with a PAS request are not subjected to immediate custodial arrest solely on that basis when, as here, the remaining objective indicia of impairment are absent. In the alternative, as alleged in the Third Cause of Action, no probable cause existed for the arrest. The right to be free from retaliatory arrest for exercising a statutory right was clearly established before November 1, 2024. Ballentine, 28 F.4th at 62; Nieves, 587 U.S. at 398-99.'),
    ('PARA', '70. As a direct and proximate result, Plaintiff has suffered the damages alleged in paragraphs 36-37.'),
    ('HEADER', 'PRAYER FOR RELIEF'),
    ('PARA', 'WHEREFORE, Plaintiff BRENDAN NGWA NFORBI respectfully prays for judgment against Defendants SANTIAGO MEZA-GONZALEZ and JOSE MELANO, in their individual capacities, as follows:'),
    ('LIST_ITEM', "A. Compensatory damages against each Defendant in an amount according to proof at trial, including but not limited to: loss of liberty and physical and emotional suffering from the unlawful detention, arrest, and compelled blood extraction; lost wages and lost earning capacity exceeding $214,000 from November 1, 2024 through the present, calculated from Plaintiff's contemporaneous rate of $33.35 regular and $50.03 premium; continuing impairment of future earning capacity as a Class A commercial driver; out-of-pocket expenses including SR-22 premiums, CDL reissue fee, and vehicle towing and impound costs; and emotional distress, humiliation, and reputational injury;"),
    ('PARA', 'B. Punitive damages against each Defendant in an amount sufficient to punish and deter;'),
    ('LIST_ITEM', "C. Taxable costs as permitted by law, and reasonable attorney's fees under 42 U.S.C. section 1988 to the extent recoverable;"),
    ('PARA', 'D. Pre- and post-judgment interest; and'),
    ('PARA', 'E. Such other and further relief as this Court deems just and proper.'),
    ('HEADER', 'DEMAND FOR JURY TRIAL'),
    ('PARA', 'Pursuant to Rule 38 of the Federal Rules of Civil Procedure and the Seventh Amendment to the United States Constitution, Plaintiff demands a trial by jury on all issues so triable.'),
]

# Rendered as a unit after CONTENT so a page break cannot separate the date from
# the signature. "" rows are blank pleading lines, reproducing the spacing of
# the filed original.
SIGNATURE_BLOCK = [
    ('', ''),
    ('left', 'Dated: August 11, 2026'),
    ('', ''),
    ('right', 'Respectfully submitted,'),
    ('', ''),
    ('', ''),
    ('right', '___________________________________'),
    ('right', 'BRENDAN NGWA NFORBI'),
    ('right', 'Plaintiff, In Pro Per'),
]


def main():
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)
    d = PleadingPaper(out, doc_title_footer=DOC_TITLE_FOOTER)

    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTORNEY_BLOCK):
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
            d.ensure_space(len(lines) + 3)
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

    d.ensure_space(len(SIGNATURE_BLOCK))
    for align, text in SIGNATURE_BLOCK:
        if align == "":
            d.blank_line()
        elif align == "left":
            d.write_line(text)
        elif align == "right":
            d.write_line(text, right=True, right_margin_offset=20)
        else:
            raise ValueError(f"unknown signature alignment {align!r}")

    d.save()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
