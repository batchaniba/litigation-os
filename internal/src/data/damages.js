import { withMatterIdentity } from "./matterIdentity.js";

// Category rollup + per-matter bottoms-up. Matter identity (caption / court /
// status) is joined from summaries at read time — do not duplicate those fields
// on matter_damages rows. `claims` here is a short damages-tab label and may
// differ from the matter JSON claims string by design.
export const damages_table = [
    { category: "Lost Wages / Economic Harm", matters: [1, 2, 7, 22], conservative: 20000, moderate: 130000, aggressive: 334000 },
    { category: "False Imprisonment", matters: [1, 2], conservative: 40000, moderate: 85000, aggressive: 215000 },
    { category: "Emotional Distress", matters: [1, 2, 5, 7, 22, 24], conservative: 0, moderate: 20000, aggressive: 115000 },
    { category: "Bane Act / Treble", matters: [1, 2], conservative: 15000, moderate: 50000, aggressive: 70000 },
    { category: "Punitive Damages", matters: [1, 2, 7, 22, 24], conservative: 30000, moderate: 120000, aggressive: 450000 },
    { category: "Consumer Fraud", matters: [12], conservative: 78672, moderate: 110072, aggressive: 200272 },
    { category: "Attorneys' Fees", matters: [1, 7, 22, 24], conservative: 28000, moderate: 45000, aggressive: 70000 },
    { category: "PC §290.46(j) Violation + Wrongful Termination (Matter 22)", matters: [22], conservative: 220000, moderate: 525000, aggressive: 1000000 },
    { category: "42 USC §1983 — Arbitrary U Visa Certification Denial & Retaliation (Matter 24)", matters: [24], conservative: 75000, moderate: 200000, aggressive: 450000 },
    { category: "PC §290.46(j) Failure to Hire — FedEx / UPS (Matters 25, 26)", matters: [25, 26], conservative: 75000, moderate: 180000, aggressive: 420000 },
    { category: "PC §290.46(j) — Wrongful Termination / Failure to Employ — Randstad / RK Logistics (Matter 27)", matters: [27], conservative: 180000, moderate: 437000, aggressive: 835000 },
    { category: "§1983 Monell / Individual + Bane Act + RICO — Shannon Smith / HOPE (Matter 28)", matters: [28], conservative: 249000, moderate: 666000, aggressive: 1510000 },
    { category: "PC §290.46(j) Failure to Hire — Amazon (Matter 29)", matters: [29], conservative: 30000, moderate: 75000, aggressive: 180000 },
    { category: "§1983 Retaliation, Due Process, Bane Act & IIED — Moua (Matter 30)", matters: [30], conservative: 90000, moderate: 225000, aggressive: 525000 },
    { category: "FCRA / ICRAA Vendor Liability — First Advantage LLC (Matter 31)", matters: [31], conservative: 30000, moderate: 89000, aggressive: 205000 },
    { category: "N.D. Cal. §1983 Meza-Gonzalez (Matter 32) — pleaded >$214k; $0 here to avoid double-count w/ M1/M2", matters: [32], conservative: 0, moderate: 0, aggressive: 0 },
    { category: "N.D. Cal. §1983 Nforbi v. Candelaria et al. (Matter 33, 3:26-cv-08272-LJC) — pleaded >$214k; $0 here to avoid double-count w/ M7", matters: [33], conservative: 0, moderate: 0, aggressive: 0 },
    { category: "§1983 Monell / Individual + Bane Act — Counseling & Psychotherapy Center (Matter 34)", matters: [34], conservative: 0, moderate: 0, aggressive: 0 }
];
// Matters 3, 5, and 15 are excluded/reduced above (abandoned/dismissed Jul. 2026):
// - Matter 3 (Derrick, ABANDONED): its Lost Income, Emotional Distress, Punitive, and Fees
//   components subtracted from the matching rows; no False Imprisonment/Bane Act component existed for it.
// - Matter 5 (Palacios, DISMISSED): its Lost CDL Wages, Bane Act/Treble, Punitive, and Fees
//   components subtracted; Matter 5 has no dedicated Emotional Distress component in its own
//   breakdown, so its (unquantified) share of that row was left in place rather than guessed at.
// - Matter 15 (CDCR/Dodd/Noguchi, ABANDONED — voluntary dismissal with prejudice, Jul. 24, 2026):
//   its Lost CDL Wages, Liberty Deprivation (False Imprisonment), Emotional Distress, and Punitive
//   components subtracted. Its Out-of-Pocket Compliance Costs ($20K/$40K/$60K) and Retaliatory
//   Transfer Losses ($15K/$30K/$64K) components have no matching category row and were never
//   captured here at all. Emotional Distress conservative would have gone negative after this
//   subtraction (row already reduced by Matter 3's share) — floored at $0 rather than shown negative.
// - Matter 30 (Moua) is NOT abandoned — it's a pending, pre-complaint matter whose filing is
//   contingent on Plaintiff's parole discharge timing (see matters.js status field). Its dedicated
//   row above was restored accordingly; it had previously been removed here on a mistaken
//   "abandoned" premise that the litigant has since corrected.
// - Matters 1, 2, and 7 (CHP cluster) were voluntarily dismissed without prejudice Aug. 15, 2026.
//   Unlike Matters 3/5/15 above, Matters 1's and 7's claims were refiled as successor N.D. Cal.
//   dockets (Matter 32 and Matter 33, respectively) rather than extinguished, so their category-row
//   dollar contributions are intentionally NOT subtracted here — Matter 32/33 already carry $0
//   placeholder rows below specifically to avoid double-counting against 1/7. Matter 2's claims
//   (False Imprisonment / Battery / Bane Act rows) have NO successor docket as of this writing —
//   see Matter 2's own flagged risk and the "matter2-state-claims-gap" crossMatter.json exposure —
//   and remain included here pending confirmation of whether they were abandoned; if so confirmed,
//   subtract Matter 2's share of the False Imprisonment, Bane Act/Treble, and Emotional Distress
//   rows following the pattern above.

// Per-matter bottoms-up breakdown — individual case ceilings before deduplication
// Portfolio view above avoids double-counting shared economic events (e.g., same CDL
// wage loss underlying Matters 1, 2, 7, 15). Per-matter view is for individual
// settlement negotiations where each defendant pays independently.
const matter_damages_raw = [
  {
    number: 1,
    claims: "4th / 14th Amend. §1983 — officers individually",
    risk: "DISMISSED without prejudice Aug. 15, 2026 (mooted the pending MTD/F&R); claims refiled in Matter 32. Historical QI risk note: Monell/punitive conceded in opposition.",
    settlement_note: "Superseded by Matter 32 (N.D. Cal.) — use Matter 32 for live settlement packaging; CHP/State through AG; EPLI carrier drives resolution",
    conservative: 100000,
    moderate: 225000,
    aggressive: 425000,
    components: [
      {
        label: "Lost CDL Wages (~15 months)",
        conservative: 50000,
        moderate: 90000,
        aggressive: 150000
      },
      {
        label: "False Imprisonment (5-day hold)",
        conservative: 12000,
        moderate: 30000,
        aggressive: 60000
      },
      {
        label: "Emotional Distress",
        conservative: 18000,
        moderate: 55000,
        aggressive: 100000
      },
      {
        label: "Punitive (officers individually)",
        conservative: 12000,
        moderate: 35000,
        aggressive: 75000
      },
      {
        label: "Fees — 42 USC §1988",
        conservative: 8000,
        moderate: 15000,
        aggressive: 40000
      }
    ]
  },
  {
    number: 2,
    claims: "False Imprisonment, Battery, Bane Act",
    risk: "DISMISSED without prejudice Aug. 15, 2026 — no successor docket. Matter 32 (N.D. Cal.) does not plead these state-law theories or name State of California/CHP; confirm intentional abandonment or amend/refile before the Nov. 1, 2026 CCP §335.1 backstop.",
    settlement_note: "No live vehicle as of Aug. 15, 2026 dismissal — do not package with Matter 32 without first amending it (28 U.S.C. §1367) or refiling in state court to carry these claims forward",
    conservative: 100000,
    moderate: 175000,
    aggressive: 350000,
    components: [
      {
        label: "False Imprisonment",
        conservative: 25000,
        moderate: 50000,
        aggressive: 75000
      },
      {
        label: "Battery / Unlawful Search",
        conservative: 15000,
        moderate: 25000,
        aggressive: 50000
      },
      {
        label: "Bane Act Statutory + Treble",
        conservative: 40000,
        moderate: 75000,
        aggressive: 175000
      },
      {
        label: "Emotional Distress",
        conservative: 20000,
        moderate: 25000,
        aggressive: 50000
      }
    ]
  },
  {
    number: 3,
    claims: "1A Retaliation, Equal Protection, Due Process",
    risk: "QI rebutted by on-record speech suppression + sworn comparator declarations",
    settlement_note: "SLB rejected $85K global (Matters 3+5); trial leverage grows with discovery",
    conservative: 112000,
    moderate: 300000,
    aggressive: 625000,
    components: [
      {
        label: "Lost Income (FedEx + ongoing suppression)",
        conservative: 55000,
        moderate: 90000,
        aggressive: 130000
      },
      {
        label: "Emotional Distress / 1A Chilling Effect",
        conservative: 25000,
        moderate: 70000,
        aggressive: 120000
      },
      {
        label: "Punitive (Derrick, Noguchi)",
        conservative: 20000,
        moderate: 100000,
        aggressive: 250000
      },
      {
        label: "Fees — 42 USC §1988",
        conservative: 12000,
        moderate: 40000,
        aggressive: 125000
      }
    ]
  },
  {
    number: 5,
    claims: "Fraud, Negligence Per Se, IIED, IIEPEA, Bane Act, UCL",
    risk: "Favorable — private defendants, no immunity; Palacios video admission near-dispositive on fraud scienter",
    settlement_note: "Strongest single-matter liability in portfolio; HOPE financial motive documented ($10,600/yr per retained parolee)",
    conservative: 225000,
    moderate: 575000,
    aggressive: 1150000,
    components: [
      {
        label: "Lost CDL Wages ($109K doc + continuing)",
        conservative: 110000,
        moderate: 210000,
        aggressive: 255000
      },
      {
        label: "Bane Act Statutory + Treble (10+ CTM cycles)",
        conservative: 60000,
        moderate: 150000,
        aggressive: 380000
      },
      {
        label: "Punitive (HOPE corp + Palacios managing agent)",
        conservative: 40000,
        moderate: 175000,
        aggressive: 400000
      },
      {
        label: "UCL Restitution",
        conservative: 5000,
        moderate: 15000,
        aggressive: 50000
      },
      {
        label: "Fees — §52.1(i) + CCP §1021.5",
        conservative: 10000,
        moderate: 25000,
        aggressive: 65000
      }
    ]
  },
  {
    number: 7,
    claims: "14th Amend. Structural Bias §1983 — DMV APS",
    risk: "DISMISSED without prejudice Aug. 15, 2026 (mooted the pending F&R/Objections); claims refiled in Matter 33. Historical QI note: rebutted by 6 independent clearly-established-law findings; structural error = no prejudice showing required.",
    settlement_note: "Superseded by Matter 33 (N.D. Cal.) — use Matter 33 for live settlement packaging; DMV Director Gordon (official capacity) creates policy-change settlement pressure; Candelaria personally signed void decision",
    conservative: 275000,
    moderate: 475000,
    aggressive: 700000,
    components: [
      {
        label: "Economic (wages + benefits + out-of-pocket)",
        conservative: 130000,
        moderate: 180000,
        aggressive: 220000
      },
      {
        label: "Non-Economic (emotional distress + dignitary harm)",
        conservative: 75000,
        moderate: 130000,
        aggressive: 200000
      },
      {
        label: "Punitive (Candelaria individually)",
        conservative: 40000,
        moderate: 100000,
        aggressive: 200000
      },
      {
        label: "Fees — 42 USC §1988",
        conservative: 30000,
        moderate: 65000,
        aggressive: 80000
      }
    ]
  },
  {
    number: 12,
    claims: "Fraud, Negligent Misrepresentation, Breach of Contract, UCL",
    risk: "Strong on liability — prior owner's disclosure to Diamond establishes actual knowledge; defect objectively documented",
    settlement_note: "Default against Diamond already requested (Jun. 15, 2026); default against Alpine imminent (response deadline Jul. 31, 2026); CMC Aug. 12, 2026 is the prove-up entry point",
    conservative: 78672,
    moderate: 110072,
    aggressive: 200272,
    components: [
      {
        label: "Documented Out-of-Pocket (deposit $12,345.10, GAP $1,895, DMV $3,442, Brannon Tire $1,197.34, Mobile Will's $740, Golden Empire Towing $562.50, Western Truck Center $36.71)",
        conservative: 20219,
        moderate: 20219,
        aggressive: 20219
      },
      {
        label: "Undocumented Out-of-Pocket, sworn testimony (Commercial Towing $750 + Almaraz Diesel $5,000)",
        conservative: 5750,
        moderate: 5750,
        aggressive: 5750
      },
      {
        label: "Lost Commercial Hauling Income (18 wks × $1,300/wk conservative; Amazon Relay carrier agreement; FAC pleads $46,800+ to date)",
        conservative: 23400,
        moderate: 46800,
        aggressive: 100000
      },
      {
        label: "Prejudgment Interest (Civ. Code §3287(a); 7% × ~3.04 yrs on documented losses)",
        conservative: 4303,
        moderate: 4303,
        aggressive: 4303
      },
      {
        label: "Punitive Damages (Civ. Code §3294; fraudulent concealment + intentional misrepresentation; Diamond→Alpine rebrand as consciousness-of-liability badge)",
        conservative: 25000,
        moderate: 33000,
        aggressive: 70000
      }
    ]
  },
  {
    number: 15,
    claims: "Negligence, False Imprisonment, IIED, Breach of Mandatory Duty",
    risk: "Favorable — §820.2 immunity inapplicable to ministerial/clerical acts; 'Eagan' copy-paste is uniquely powerful (Noguchi authored wrong name)",
    settlement_note: "Highest uncapped potential in portfolio; July 2 retaliatory transfer is additional punitive evidence; accruing daily",
    conservative: 300000,
    moderate: 650000,
    aggressive: 1150000,
    components: [
      {
        label: "Lost CDL Wages (accruing from Nov. 19, 2025)",
        conservative: 90000,
        moderate: 150000,
        aggressive: 216000
      },
      {
        label: "Liberty Deprivation ($100/day, continuing tort)",
        conservative: 25000,
        moderate: 80000,
        aggressive: 110000
      },
      {
        label: "Out-of-Pocket Compliance Costs",
        conservative: 20000,
        moderate: 40000,
        aggressive: 60000
      },
      {
        label: "Emotional Distress (GPS on void instrument)",
        conservative: 75000,
        moderate: 150000,
        aggressive: 300000
      },
      {
        label: "Punitive (Dodd, Noguchi, Rojo individually)",
        conservative: 75000,
        moderate: 200000,
        aggressive: 400000
      },
      {
        label: "Retaliatory Transfer Losses (housing + employment)",
        conservative: 15000,
        moderate: 30000,
        aggressive: 64000
      }
    ]
  },
  {
    number: 22,
    claims: "PC §290.46(j), Wrongful Termination, FCRA, ICRAA, UCL, IIED",
    risk: "Extremely favorable — Post-Adverse Action Notice is written admission citing registry as sole basis; no criminal convictions in any jurisdiction",
    settlement_note: "EPLI carrier involved; policy correction at all CA Pilot locations adds non-monetary leverage; Checkr statutory warning confirms willfulness",
    conservative: 220000,
    moderate: 525000,
    aggressive: 1000000,
    components: [
      {
        label: "Economic (wages + benefits)",
        conservative: 85000,
        moderate: 155000,
        aggressive: 265000
      },
      {
        label: "PC §290.46(l) Treble Add-On",
        conservative: 60000,
        moderate: 200000,
        aggressive: 400000
      },
      {
        label: "Emotional Distress / IIED",
        conservative: 40000,
        moderate: 100000,
        aggressive: 200000
      },
      {
        label: "FCRA / ICRAA Statutory",
        conservative: 10000,
        moderate: 20000,
        aggressive: 40000
      },
      {
        label: "Civil Penalty §290.46(k)",
        conservative: 10000,
        moderate: 20000,
        aggressive: 25000
      },
      {
        label: "Punitive",
        conservative: 15000,
        moderate: 30000,
        aggressive: 70000
      }
    ]
  },
  {
    number: 24,
    claims: "14th Amend. Due Process, 1A Retaliation §1983 — U Visa Denial",
    risk: "Favorable — no QI for arbitrary denial of mandatory statutory duty; retaliation claim strong (3/26 complaint → 4/20 denial, same incident Serrato defending)",
    settlement_note: "U Visa certification itself is the primary non-monetary win; money damages against Serrato personally create personal settlement pressure",
    conservative: 75000,
    moderate: 200000,
    aggressive: 450000,
    components: [
      {
        label: "Immigration Access Harm (U Visa deprivation)",
        conservative: 20000,
        moderate: 60000,
        aggressive: 120000
      },
      {
        label: "Emotional Distress",
        conservative: 20000,
        moderate: 60000,
        aggressive: 100000
      },
      {
        label: "Punitive (Serrato individually)",
        conservative: 20000,
        moderate: 55000,
        aggressive: 150000
      },
      {
        label: "Fees — 42 USC §1988",
        conservative: 15000,
        moderate: 25000,
        aggressive: 80000
      }
    ]
  },
  {
    number: 25,
    claims: "PC §290.46(j), Wrongful Failure to Hire, ICRAA, Invasion of Privacy, Negligence Per Se, UCL",
    risk: "Favorable on the law but pled on information and belief — no admitted-basis letter or recovered background report, unlike Matters 22/23; strongest evidence is the application-to-denial notice trail (2 pre-adverse notices, 5 reminders)",
    settlement_note: "No wage documentation (never employed) caps economic damages relative to Matter 22; statutory penalty and fee-shifting are the main leverage points",
    conservative: 40000,
    moderate: 95000,
    aggressive: 220000,
    components: [
      {
        label: "PC §290.46(j)(4)(A) Statutory Penalty",
        conservative: 25000,
        moderate: 40000,
        aggressive: 75000
      },
      {
        label: "Emotional Distress / Lost Opportunity",
        conservative: 8000,
        moderate: 25000,
        aggressive: 60000
      },
      {
        label: "ICRAA Statutory + Punitive",
        conservative: 2000,
        moderate: 5000,
        aggressive: 10000
      },
      {
        label: "Punitive (Civ. Code §3294)",
        conservative: 0,
        moderate: 10000,
        aggressive: 45000
      },
      {
        label: "Fees — PC §290.46(j)(4)(A) / ICRAA",
        conservative: 5000,
        moderate: 15000,
        aggressive: 30000
      }
    ]
  },
  {
    number: 26,
    claims: "PC §290.46(j), Wrongful Failure to Hire, ICRAA, Invasion of Privacy, Negligence Per Se, UCL",
    risk: "Favorable on the law but pled on information and belief, as with Matter 25; limitations period preserved by July 15, 2026 filing (16 days ahead of the July 31, 2026 two-year cutoff from the July 31, 2024 adverse action)",
    settlement_note: "Limitations period risk eliminated by timely filing; no wage documentation (never employed) caps economic damages relative to Matter 22; statutory penalty and fee-shifting are the main leverage points",
    conservative: 35000,
    moderate: 85000,
    aggressive: 200000,
    components: [
      {
        label: "PC §290.46(j)(4)(A) Statutory Penalty",
        conservative: 25000,
        moderate: 35000,
        aggressive: 65000
      },
      {
        label: "Emotional Distress / Lost Opportunity",
        conservative: 5000,
        moderate: 20000,
        aggressive: 55000
      },
      {
        label: "ICRAA Statutory + Punitive",
        conservative: 2000,
        moderate: 5000,
        aggressive: 10000
      },
      {
        label: "Punitive (Civ. Code §3294)",
        conservative: 0,
        moderate: 10000,
        aggressive: 40000
      },
      {
        label: "Fees — PC §290.46(j)(4)(A) / ICRAA",
        conservative: 3000,
        moderate: 15000,
        aggressive: 30000
      }
    ]
  },
  {
    number: 27,
    claims: "PC §290.46(j), Wrongful Termination / Failure to Employ (Tameny), FCRA, ICRAA, UCL",
    risk: "Extremely favorable — Plaintiff holds the actual InfoMart BGC report (Order No. 15780719): all 7 county/state criminal searches and federal criminal returned No Record; registry is the only flagged item; Billing Code 'RK LOGISTICS' and Client Package 'RK Logistics' in report header prove RK Logistics configured the criteria triggering 'NEEDS APPROVAL, PER CLIENT CRITERIA.' Rehire email establishes employment relationship existed at time of BGC — stronger Tameny posture than the pure failure-to-hire cases in Matters 25/26. Wage rate confirmed at $28.50/hr, 42.5 hrs/week (Mon–Fri 2:30 PM–11:00 PM), generating overtime each week; actual lost wages eclipse the §290.46(j)(4)(A) $25,000 statutory floor within approximately 6.5 months, making actual-damages the operative measure. RK Logistics denied liability Jul. 21, 2026 on two grounds — neither disturbs this posture: its employer-status argument reaches only the Tameny claim (not the other five causes of action) and is undercut by its own Transportation Manager's written rejection email; its MVR-based defense cites a commercial (Class A) disqualification inapplicable to the non-commercial Class C position at issue, predating Plaintiff's Jun. 11, 2026 Class C reissue. Randstad's own exposure — the FCRA waiting-period violation — is untouched by either defense and remains unanswered.",
    settlement_note: "Fifth PC §290.46(j) matter in portfolio; pattern evidence across five employers strengthens willfulness showing on all. Two-defendant structure (Randstad US, LLC as employer of record + RK Logistics Group, Inc. as criteria-setting end client) creates cross-pressure: each defendant is incentivized to attribute the adverse decision to the other. Punitive exposure is amplified by both defendants' substantial net worth — Randstad is a subsidiary of a global staffing company; RK Logistics serves the semiconductor and EV supply chain. Rehire posture + documented wage rate produces back pay and front pay exposure not present in Matters 25/26.",
    conservative: 179838,
    moderate: 437095,
    aggressive: 834352,
    components: [
      {
        label: "Lost Wages — Back Pay ($28.50/hr × 42.5 hrs/wk incl. weekly OT at 1.5x; $1,246.88/wk: conservative 12 mo. / moderate 18 mo. / aggressive 24 mo.)",
        conservative: 64838,
        moderate: 97257,
        aggressive: 129676
      },
      {
        label: "Front Pay — Future Lost Earnings (conservative: none / moderate: 12 additional mo. / aggressive: 24 additional mo.)",
        conservative: 0,
        moderate: 64838,
        aggressive: 129676
      },
      {
        label: "Emotional Distress — Wrongful rescission of accepted rehire position; fifth cumulative §290.46(j) employment denial compounds distress narrative",
        conservative: 25000,
        moderate: 50000,
        aggressive: 75000
      },
      {
        label: "FCRA / ICRAA Statutory + Punitive (willful noncompliance; InfoMart report itself contains FCRA Summary of Rights and CA ICRA Notice — parties had constructive notice of the statutory framework at the moment of use)",
        conservative: 15000,
        moderate: 25000,
        aggressive: 50000
      },
      {
        label: "Punitive (Civ. Code §3294) — Two corporate defendants with independent net worth exposure; fifth repeat §290.46(j) violation supports willfulness finding; 'NEEDS APPROVAL, PER CLIENT CRITERIA' shows deliberate criteria configuration, not inadvertent use",
        conservative: 50000,
        moderate: 150000,
        aggressive: 350000
      },
      {
        label: "Attorney Fees — PC §290.46(j)(4)(A) mandatory fee-shifting + FCRA + ICRAA",
        conservative: 25000,
        moderate: 50000,
        aggressive: 100000
      }
    ]
  },
  {
    number: 28,
    claims: "42 U.S.C. §1983 Monell + Individual Capacity; Bane Act §52.1; Fraud/Negligent Misrepresentation; RICO §1962(c)-(d)",
    risk: "Favorable on state-actor theory (West v. Atkins); Monell supported by In re Dwyer condemnation of HOPE's blanket retention policy and HOPE's own Clinical Operational Manual; RICO carries dismissal risk but is pleaded as aggressive multiplier; Philadelphia Indemnity insurance ($1M per-incident / $5M aggregate) creates realistic settlement floor",
    settlement_note: "Shannon Smith's individual-capacity exposure creates personal settlement pressure independent of HOPE's corporate insurance. 542 pages of discovery already in hand from dismissed state case. RICO treble exposure ($249K–$1.51M range) and §1988 fee shifting give Plaintiff substantial leverage. Insurance floor anchors realistic resolution in the $500K–$1M range on moderate facts.",
    conservative: 249000,
    moderate: 666000,
    aggressive: 1510000,
    components: [
      {
        label: "Lost CDL Wages — Economic Harm (documented W-2s: $109,408+ over 2022–2024; $72K/yr but-for CDL career rate; conservative: 2 yr / moderate: 3 yr / aggressive: 5 yr)",
        conservative: 144000,
        moderate: 216000,
        aggressive: 360000
      },
      {
        label: "§1983 Compensatory Damages — Constitutional deprivation, liberty-interest violation, emotional distress (Monell against HOPE + individual capacity against Smith)",
        conservative: 30000,
        moderate: 100000,
        aggressive: 200000
      },
      {
        label: "Bane Act §52.1 — Coercive interference with constitutional rights ($25,000 statutory minimum per violation; multiple violations alleged)",
        conservative: 25000,
        moderate: 75000,
        aggressive: 150000
      },
      {
        label: "RICO §1964(c) — Treble damages for enterprise conduct (fraudulent billing to CDCR; false adverse reporting to parole agents); conservative: $0 (dismissal risk) / moderate: $150K / aggressive: $450K",
        conservative: 0,
        moderate: 150000,
        aggressive: 450000
      },
      {
        label: "Punitive Damages — §1983 against Shannon Smith individually; Bane Act treble exposure; deliberate policy of retaliatory reporting",
        conservative: 25000,
        moderate: 75000,
        aggressive: 200000
      },
      {
        label: "Attorney Fees — 42 U.S.C. §1988 (§1983 / Bane Act); RICO fee shifting",
        conservative: 25000,
        moderate: 50000,
        aggressive: 150000
      }
    ]
  },
  {
    number: 29,
    claims: "PC §290.46(j)(2)(E) Violation, FCRA, ICRAA, Invasion of Privacy, UCL §17200, IIED",
    risk: "Extremely favorable on liability if the anticipated adverse action occurs — PC §290.46(j)(2)(E) categorically prohibits registry use; BGC delay is consistent with registry-flag review; a pattern across the four confirmed prior instances (22, 25, 26, 27) compounds willfulness; Amazon's size and documented hiring pipeline maximize punitive and fee exposure",
    settlement_note: "Would be the fifth confirmed PC §290.46(j) adverse action in the portfolio (after 22, 25, 26, 27) if the pending BGC results in one; post-Lerma settlement (Sept. 29, 2023) willfulness is the dominant settlement driver — Amazon and Accurate Background cannot claim good faith after settling an identical class action; Amazon's $500B+ net worth and Accurate Background's role as repeat defendant create substantial punitive exposure; pre-adverse notice once issued triggers FCRA 5-business-day waiting period before adverse action. Lerma v. Amazon.com Services, LLC et al., No. 8:22-cv-01727 (C.D. Cal.) is the key analogous settlement.",
    conservative: 30000,
    moderate: 75000,
    aggressive: 180000,
    components: [
      {
        label: "PC §290.46(j)(4)(A) Statutory Penalty (per-violation minimum $25,000; post-Lerma willfulness eliminates any reduction below statutory floor)",
        conservative: 25000,
        moderate: 30000,
        aggressive: 50000
      },
      {
        label: "Emotional Distress — fifth confirmed cumulative PC §290.46(j) employment denial if this one occurs; compounding dignitary harm narrative across Randstad, FedEx, UPS, Pilot; IIED claim supported by ongoing pattern",
        conservative: 3000,
        moderate: 20000,
        aggressive: 50000
      },
      {
        label: "ICRAA Statutory (Accurate Background as reporting agency; failure to follow proper notice/disclosure procedures; Accurate Background named defendant in Lerma — post-settlement repeat violation supports willful noncompliance finding)",
        conservative: 1000,
        moderate: 5000,
        aggressive: 10000
      },
      {
        label: "Punitive Damages (Civ. Code §3294 — post-Lerma willfulness: Amazon and Accurate Background settled identical §290.46(j) claim Sept. 2023 and continued the same BGC practice; three-year post-settlement repetition is strongest possible willfulness predicate; Amazon's market capitalization supports meaningful punitive multiplier)",
        conservative: 0,
        moderate: 15000,
        aggressive: 60000
      },
      {
        label: "Attorney Fees — PC §290.46(j)(4)(A) mandatory fee-shifting; FCRA; ICRAA",
        conservative: 1000,
        moderate: 5000,
        aggressive: 10000
      }
    ]
  },
  {
    number: 30,
    claims: "42 U.S.C. §1983 First Amendment Retaliation, §1983 Due Process, Bane Act Cal. Civ. Code §52.1, IIED",
    risk: "Very strong on liability — three independent retaliation vectors each independently actionable; fabricated telehealth violation contradicted by contemporaneous text records; 18-day interval between CDCR lawsuit service and retaliatory transfer is direct evidence of retaliatory motive; punitive damages strongly supported against Moua personally for fabricated parole violation",
    settlement_note: "Primary settlement drivers: (1) fabricated parole violation documented in real-time text evidence (Moua never sent access code; BNN asked twice; violation submitted anyway); (2) 18-day temporal proximity between CDCR lawsuit service and retaliatory transfer is nearly impossible to explain as coincidental; (3) Bane Act §52.1 exposes individual defendants to statutory penalties plus 3× compensatory; (4) punitive exposure against Moua personally for knowing fabrication of violation; (5) Macy's employment destruction directly traceable to transfer with no legitimate administrative basis.",
    conservative: 90000,
    moderate: 225000,
    aggressive: 525000,
    components: [
      {
        label: "§1983 Compensatory — First Amendment Retaliation (two-step documented retaliation: Derrick suit → file transfer; CDCR suit service → retaliatory transfer within 18 days; emotional distress from unconstitutional parole supervision)",
        conservative: 25000,
        moderate: 75000,
        aggressive: 175000
      },
      {
        label: "§1983 Compensatory — Fourteenth Amendment Due Process (fabricated 'failure to attend treatment' violation based on access code Moua never provided; administrative record harm; ongoing parole conditions impacted by manufactured pretext)",
        conservative: 15000,
        moderate: 40000,
        aggressive: 100000
      },
      {
        label: "Lost Wages — Macy's Captain Selling & Support ($21.50/hr × ~30 hrs/wk; last shift Jul. 2, 2026; LOA through Aug. 12 preferred return; lost employment opportunity attributable entirely to retaliatory transfer from Stockton to Santa Clara GPS Unit)",
        conservative: 5000,
        moderate: 20000,
        aggressive: 50000
      },
      {
        label: "Bane Act Cal. Civ. Code §52.1(b) — minimum $4,000 statutory civil penalty per violation plus up to 3× actual damages plus mandatory attorney fees; coercive use of fabricated violation and retaliatory transfer to suppress First Amendment petition activity",
        conservative: 12000,
        moderate: 35000,
        aggressive: 75000
      },
      {
        label: "IIED — fabricated parole violation; forced housing/employment displacement from Stockton to Santa Clara GPS jurisdiction; employment destruction; sex offender registration completed under duress of third-strike automatic life sentence (Pen. Code §667(e)(2)(A)) during active housing displacement",
        conservative: 15000,
        moderate: 30000,
        aggressive: 75000
      },
      {
        label: "Punitive Damages — Moua personally (knowing fabrication of parole violation by withholding access code then submitting non-attendance as willful non-compliance; retaliatory transfer executed within 18 days of lawsuit service)",
        conservative: 0,
        moderate: 15000,
        aggressive: 25000
      },
      {
        label: "Attorney Fees — 42 U.S.C. §1988 (§1983 fee-shifting); Bane Act mandatory fee award",
        conservative: 18000,
        moderate: 10000,
        aggressive: 25000
      }
    ]
  },
  {
    number: 31,
    claims: "FCRA §1681b(b), FCRA §1681e(b), ICRAA, Negligence Per Se, UCL §17200",
    risk: "Favorable pattern (same vendor, two registry-flagged reports, two employers, 8 months apart) but untested theory in this portfolio — reaches the CRA rather than the employer that used the report; still constrained by the same information-and-belief gap affecting Matters 25/26 pending discovery of the underlying reports",
    settlement_note: "Deliberately excludes Emotional Distress / Lost Opportunity — already claimed against FedEx (Matter 25) and UPS (Matter 26) for these same two denials; this matter's exposure is additive (vendor-specific ICRAA/FCRA statutory penalties), not a duplicate of the employer-side claims",
    conservative: 30000,
    moderate: 89000,
    aggressive: 205000,
    components: [
      {
        label: "ICRAA Statutory Damages (Civ. Code §1786.50(a)(1) — not less than $10,000 per willful violation; two independent furnishing events, UPS Jul. 2024 and FedEx Mar. 2025)",
        conservative: 20000,
        moderate: 30000,
        aggressive: 50000
      },
      {
        label: "FCRA Statutory Damages (15 U.S.C. §1681n — willful noncompliance, $100–$1,000 per violation per report furnished; two reports)",
        conservative: 2000,
        moderate: 4000,
        aggressive: 10000
      },
      {
        label: "FCRA §1681e(b) Reasonable-Procedures Failure — Actual Damages (failure to exclude/flag categorically prohibited registry information despite First Advantage's own statutory disclaimer already printed on its notices)",
        conservative: 0,
        moderate: 15000,
        aggressive: 40000
      },
      {
        label: "Punitive Damages (Civ. Code §3294 / ICRAA willfulness — same vendor, two separate adverse actions eight months apart, evidencing a systemic practice rather than an isolated error)",
        conservative: 0,
        moderate: 20000,
        aggressive: 60000
      },
      {
        label: "Attorney Fees (ICRAA Civ. Code §1786.50(a)(2) mandatory fee-shifting + FCRA §1681n/o)",
        conservative: 8000,
        moderate: 20000,
        aggressive: 45000
      }
    ]
  },
  {
    number: 32,
    claims: "§1983 — six causes (unlawful entry/search/arrest, Franks, fabrication, 1A retaliation)",
    risk: "Matters 1 and 2 confirmed dismissed Aug. 15, 2026 — this is now the live vehicle for Matter 1's federal claims. [FLAGGED: Matter 2's state-law claims (False Imprisonment, Battery, Bane Act) and the State/CHP defendant are NOT pled here and have no other successor — confirm intentional abandonment or amend before Nov. 1, 2026.] Also watch potential FRCP 41(a)(1)(B) two-dismissal exposure from Matter 13's prior notice dismissal of the overlapping five-day-hold claim — see internal/docs/MATTER_01_FORUM_TRANSFER_ANALYSIS.md §3.2. Overlaps Matter 24 (related N.D. Cal.) — manage claim-splitting.",
    settlement_note: "Operative complaint pleads >$214,000 compensatory. Portfolio row stays $0 so the shared Nov. 1 / CDL wage-loss period is not double-counted against Matters 1 and 2; use Matter 32's pleaded figure in N.D. Cal. negotiations.",
    conservative: 0,
    moderate: 0,
    aggressive: 0,
    components: [
      {
        label: "Reserved — pleaded >$214k in N.D. Cal.; portfolio $0 avoids double-count with Matters 1/2",
        conservative: 0,
        moderate: 0,
        aggressive: 0
      }
    ]
  },
  {
    number: 33,
    claims: "§1983 APS structural bias / fair hearing / vacatur vs Candelaria & Gordon",
    risk: "Matter 7 confirmed dismissed Aug. 15, 2026 — this is now the live vehicle for those claims. Coordinate with Matter 32 and Serrato related-case notice.",
    settlement_note: "Operative complaint pleads >$214,000 compensatory / $250,000 JS-44 min. Portfolio row stays $0 so the APS / CDL wage-loss period is not double-counted against Matter 7; use Matter 33's pleaded figure in N.D. Cal. negotiations.",
    conservative: 0,
    moderate: 0,
    aggressive: 0,
    components: [
      {
        label: "Reserved — pleaded >$214k in N.D. Cal.; portfolio $0 avoids double-count with Matter 7",
        conservative: 0,
        moderate: 0,
        aggressive: 0
      }
    ]
  },
  {
    number: 34,
    claims: "42 U.S.C. §1983 Monell + Individual; Bane Act §52.1; Fraud/Misrepresentation; UCL §17200",
    risk: "Pre-filing / intake stage: state-actor status established under West v. Atkins; liability contingent on discovery of CPC treatment agreements, intake orientation representations, and whether CPC maintains an unlawful blanket-retention policy analogous to In re Dwyer",
    settlement_note: "Prospective companion/successor to Matter 28 following July 2, 2026 Santa Clara transfer. Pre-filing valuation contingent on intake documentation and treatment progress reporting. Avoid double-counting prior CDL wage losses with Matter 28/Matter 5.",
    conservative: 0,
    moderate: 0,
    aggressive: 0,
    components: [
      {
        label: "Reserved — pre-filing intake / compliance monitoring stage; valuation contingent on intake disclosures and treatment progress reporting",
        conservative: 0,
        moderate: 0,
        aggressive: 0
      }
    ]
  },
  {
    number: 35,
    claims: "Unruh §§51/51.5/52; False Imprisonment; IIED; Negligent Supervision; UCL §17200; Declaratory Relief",
    risk: "Intentional-discrimination proof is circumstantial; Ross will assert Pen. Code §490.5(f) merchant privilege — negated here by no observed theft, open-view outside beverage, and no Ross merchandise. Preserve receipt and demand store video early.",
    settlement_note: "Standalone public-accommodation stop; no damages overlap with employment or CHP clusters. Statutory Unruh floor ($4,000/offense) plus treble/ED/punitive and fee-shifting drive settlement pressure once video and demographics are in discovery.",
    conservative: 25000,
    moderate: 75000,
    aggressive: 250000,
    components: [
      {
        label: "Unruh Civ. Code §52(a) — actual + up to treble / $4,000 statutory floor + fees",
        conservative: 12000,
        moderate: 35000,
        aggressive: 100000
      },
      {
        label: "False Imprisonment + IIED general damages (public racial accusation)",
        conservative: 8000,
        moderate: 25000,
        aggressive: 75000
      },
      {
        label: "Civ. Code §3294 punitive damages (managing-agent ratification pleaded)",
        conservative: 5000,
        moderate: 15000,
        aggressive: 75000
      }
    ]
  }
];

export const matter_damages = matter_damages_raw.map((row) => withMatterIdentity(row));
