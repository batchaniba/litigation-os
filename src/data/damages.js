export const damages_table = [
    { category: "Lost Wages / Economic Harm", matters: "1, 2, 3, 5, 7, 15, 22", conservative: 275000, moderate: 580000, aggressive: 935000 },
    { category: "False Imprisonment", matters: "1, 2, 15", conservative: 65000, moderate: 165000, aggressive: 325000 },
    { category: "Emotional Distress", matters: "1, 2, 3, 5, 7, 15, 22, 24", conservative: 85000, moderate: 240000, aggressive: 535000 },
    { category: "Bane Act / Treble", matters: "1, 2, 5", conservative: 75000, moderate: 200000, aggressive: 450000 },
    { category: "Punitive Damages", matters: "1, 2, 3, 5, 7, 15, 22, 24", conservative: 165000, moderate: 595000, aggressive: 1500000 },
    { category: "Consumer Fraud", matters: "12", conservative: 40000, moderate: 75000, aggressive: 150000 },
    { category: "Attorneys' Fees", matters: "1, 3, 5, 7, 22, 24", conservative: 50000, moderate: 110000, aggressive: 260000 },
    { category: "PC §290.46(j) Violation + Wrongful Termination (Matter 22)", matters: "22", conservative: 220000, moderate: 525000, aggressive: 1000000 },
    { category: "42 USC §1983 — Arbitrary U Visa Certification Denial & Retaliation (Matter 24)", matters: "24", conservative: 75000, moderate: 200000, aggressive: 450000 },
    { category: "PC §290.46(j) Failure to Hire — FedEx / UPS (Matters 25, 26)", matters: "25, 26", conservative: 75000, moderate: 180000, aggressive: 420000 },
    { category: "PC §290.46(j) — Wrongful Termination / Failure to Employ — Randstad / RK Logistics (Matter 27)", matters: "27", conservative: 180000, moderate: 437000, aggressive: 835000 },
    { category: "§1983 Monell / Individual + Bane Act + RICO — Shannon Smith / HOPE (Matter 28)", matters: "28", conservative: 249000, moderate: 666000, aggressive: 1510000 }
];

// Per-matter bottoms-up breakdown — individual case ceilings before deduplication
// Portfolio view above avoids double-counting shared economic events (e.g., same CDL
// wage loss underlying Matters 1, 2, 7, 15). Per-matter view is for individual
// settlement negotiations where each defendant pays independently.
export const matter_damages = [
    {
        number: 1,
        caption: "Newanforbi v. CHP et al.",
        court: "USDC E.D. Cal.",
        claims: "4th / 14th Amend. §1983 — officers individually",
        status: "MTD under submission",
        risk: "Significant QI risk — MTD pending; Monell/punitive conceded in opposition",
        settlement_note: "Package with Matter 2; CHP/State through AG; EPLI carrier drives resolution",
        conservative: 100000, moderate: 225000, aggressive: 425000,
        components: [
            { label: "Lost CDL Wages (~15 months)", conservative: 50000, moderate: 90000, aggressive: 150000 },
            { label: "False Imprisonment (5-day hold)", conservative: 12000, moderate: 30000, aggressive: 60000 },
            { label: "Emotional Distress", conservative: 18000, moderate: 55000, aggressive: 100000 },
            { label: "Punitive (officers individually)", conservative: 12000, moderate: 35000, aggressive: 75000 },
            { label: "Fees — 42 USC §1988", conservative: 8000, moderate: 15000, aggressive: 40000 }
        ]
    },
    {
        number: 2,
        caption: "Newanforbi v. Meza-Gonzalez et al.",
        court: "Alameda Sup. Ct. (STAYED)",
        claims: "False Imprisonment, Battery, Bane Act",
        status: "Stayed pending federal MTD in Matter 1",
        risk: "Favorable — no QI in state court; U-Visa certification motion adds leverage",
        settlement_note: "Package with Matter 1; state tort claims survive federal outcome regardless",
        conservative: 100000, moderate: 175000, aggressive: 350000,
        components: [
            { label: "False Imprisonment", conservative: 25000, moderate: 50000, aggressive: 75000 },
            { label: "Battery / Unlawful Search", conservative: 15000, moderate: 25000, aggressive: 50000 },
            { label: "Bane Act Statutory + Treble", conservative: 40000, moderate: 75000, aggressive: 175000 },
            { label: "Emotional Distress", conservative: 20000, moderate: 25000, aggressive: 50000 }
        ]
    },
    {
        number: 3,
        caption: "Newanforbi v. Derrick et al.",
        court: "USDC E.D. Cal.",
        claims: "1A Retaliation, Equal Protection, Due Process",
        status: "MTD under submission; Palacios MTD briefed",
        risk: "QI rebutted by on-record speech suppression + sworn comparator declarations",
        settlement_note: "SLB rejected $85K global (Matters 3+5); trial leverage grows with discovery",
        conservative: 112000, moderate: 300000, aggressive: 625000,
        components: [
            { label: "Lost Income (FedEx + ongoing suppression)", conservative: 55000, moderate: 90000, aggressive: 130000 },
            { label: "Emotional Distress / 1A Chilling Effect", conservative: 25000, moderate: 70000, aggressive: 120000 },
            { label: "Punitive (Derrick, Noguchi)", conservative: 20000, moderate: 100000, aggressive: 250000 },
            { label: "Fees — 42 USC §1988", conservative: 12000, moderate: 40000, aggressive: 125000 }
        ]
    },
    {
        number: 5,
        caption: "Newanforbi v. Palacios et al.",
        court: "San Joaquin Sup. Ct.",
        claims: "Fraud, Negligence Per Se, IIED, IIEPEA, Bane Act, UCL",
        status: "Reply filed 07/07/2026; demurrer hearing July 15, 2026 — IMMINENT",
        risk: "Favorable — private defendants, no immunity; Palacios video admission near-dispositive on fraud scienter",
        settlement_note: "Strongest single-matter liability in portfolio; HOPE financial motive documented ($10,600/yr per retained parolee)",
        conservative: 225000, moderate: 575000, aggressive: 1150000,
        components: [
            { label: "Lost CDL Wages ($109K doc + continuing)", conservative: 110000, moderate: 210000, aggressive: 255000 },
            { label: "Bane Act Statutory + Treble (10+ CTM cycles)", conservative: 60000, moderate: 150000, aggressive: 380000 },
            { label: "Punitive (HOPE corp + Palacios managing agent)", conservative: 40000, moderate: 175000, aggressive: 400000 },
            { label: "UCL Restitution", conservative: 5000, moderate: 15000, aggressive: 50000 },
            { label: "Fees — §52.1(i) + CCP §1021.5", conservative: 10000, moderate: 25000, aggressive: 65000 }
        ]
    },
    {
        number: 7,
        caption: "Newanforbi v. Candelaria",
        court: "USDC E.D. Cal.",
        claims: "14th Amend. Structural Bias §1983 — DMV APS",
        status: "FAC filed; F&R pending from Mag. Kim",
        risk: "Favorable — QI rebutted by 6 independent clearly-established-law findings; structural error = no prejudice showing required",
        settlement_note: "DMV Director Gordon (official capacity) creates policy-change settlement pressure; Candelaria personally signed void decision",
        conservative: 275000, moderate: 475000, aggressive: 700000,
        components: [
            { label: "Economic (wages + benefits + out-of-pocket)", conservative: 130000, moderate: 180000, aggressive: 220000 },
            { label: "Non-Economic (emotional distress + dignitary harm)", conservative: 75000, moderate: 130000, aggressive: 200000 },
            { label: "Punitive (Candelaria individually)", conservative: 40000, moderate: 100000, aggressive: 200000 },
            { label: "Fees — 42 USC §1988", conservative: 30000, moderate: 65000, aggressive: 80000 }
        ]
    },
    {
        number: 12,
        caption: "Diamond Truck Sales, Inc.",
        court: "San Joaquin Sup. Ct.",
        claims: "Fraud, Negligent Misrepresentation, Breach of Contract, UCL",
        status: "Default judgment request submitted 06/15/2026; CMC 08/12/2026",
        risk: "Strong on liability — prior owner's disclosure to Diamond establishes actual knowledge; defect objectively documented",
        settlement_note: "Default against Diamond already requested (Jun. 15, 2026); default against Alpine imminent (response deadline Jul. 31, 2026); CMC Aug. 12, 2026 is the prove-up entry point",
        conservative: 57000, moderate: 100000, aggressive: 200000,
        components: [
            { label: "Direct Economic Losses (deposit, GAP, DMV, towing)", conservative: 25130, moderate: 25130, aggressive: 25130 },
            { label: "Lost Commercial Income", conservative: 20000, moderate: 50000, aggressive: 100000 },
            { label: "Fraud Punitive + UCL Restitution", conservative: 11870, moderate: 24870, aggressive: 74870 }
        ]
    },
    {
        number: 15,
        caption: "Newanforbi v. CDCR / Dodd / Noguchi",
        court: "San Joaquin Sup. Ct.",
        claims: "Negligence, False Imprisonment, IIED, Breach of Mandatory Duty",
        status: "Filed June 11, 2026; CMC December 9, 2026",
        risk: "Favorable — §820.2 immunity inapplicable to ministerial/clerical acts; 'Eagan' copy-paste is uniquely powerful (Noguchi authored wrong name)",
        settlement_note: "Highest uncapped potential in portfolio; July 2 retaliatory transfer is additional punitive evidence; accruing daily",
        conservative: 300000, moderate: 650000, aggressive: 1150000,
        components: [
            { label: "Lost CDL Wages (accruing from Nov. 19, 2025)", conservative: 90000, moderate: 150000, aggressive: 216000 },
            { label: "Liberty Deprivation ($100/day, continuing tort)", conservative: 25000, moderate: 80000, aggressive: 110000 },
            { label: "Out-of-Pocket Compliance Costs", conservative: 20000, moderate: 40000, aggressive: 60000 },
            { label: "Emotional Distress (GPS on void instrument)", conservative: 75000, moderate: 150000, aggressive: 300000 },
            { label: "Punitive (Dodd, Noguchi, Rojo individually)", conservative: 75000, moderate: 200000, aggressive: 400000 },
            { label: "Retaliatory Transfer Losses (housing + employment)", conservative: 15000, moderate: 30000, aggressive: 64000 }
        ]
    },
    {
        number: 22,
        caption: "Newanforbi v. Pilot Travel Centers LLC",
        court: "San Joaquin Sup. Ct.",
        claims: "PC §290.46(j), Wrongful Termination, FCRA, ICRAA, UCL, IIED",
        status: "Filed May 29, 2026; demand pending",
        risk: "Extremely favorable — Post-Adverse Action Notice is written admission citing registry as sole basis; no criminal convictions in any jurisdiction",
        settlement_note: "EPLI carrier involved; policy correction at all CA Pilot locations adds non-monetary leverage; Checkr statutory warning confirms willfulness",
        conservative: 220000, moderate: 525000, aggressive: 1000000,
        components: [
            { label: "Economic (wages + benefits)", conservative: 85000, moderate: 155000, aggressive: 265000 },
            { label: "PC §290.46(l) Treble Add-On", conservative: 60000, moderate: 200000, aggressive: 400000 },
            { label: "Emotional Distress / IIED", conservative: 40000, moderate: 100000, aggressive: 200000 },
            { label: "FCRA / ICRAA Statutory", conservative: 10000, moderate: 20000, aggressive: 40000 },
            { label: "Civil Penalty §290.46(k)", conservative: 10000, moderate: 20000, aggressive: 25000 },
            { label: "Punitive", conservative: 15000, moderate: 30000, aggressive: 70000 }
        ]
    },
    {
        number: 24,
        caption: "Newanforbi v. Serrato",
        court: "USDC N.D. Cal.",
        claims: "14th Amend. Due Process, 1A Retaliation §1983 — U Visa Denial",
        status: "Filed June 17, 2026; CMC September 15, 2026",
        risk: "Favorable — no QI for arbitrary denial of mandatory statutory duty; retaliation claim strong (3/26 complaint → 4/20 denial, same incident Serrato defending)",
        settlement_note: "U Visa certification itself is the primary non-monetary win; money damages against Serrato personally create personal settlement pressure",
        conservative: 75000, moderate: 200000, aggressive: 450000,
        components: [
            { label: "Immigration Access Harm (U Visa deprivation)", conservative: 20000, moderate: 60000, aggressive: 120000 },
            { label: "Emotional Distress", conservative: 20000, moderate: 60000, aggressive: 100000 },
            { label: "Punitive (Serrato individually)", conservative: 20000, moderate: 55000, aggressive: 150000 },
            { label: "Fees — 42 USC §1988", conservative: 15000, moderate: 25000, aggressive: 80000 }
        ]
    },
    {
        number: 25,
        caption: "Newanforbi v. Federal Express Corporation",
        court: "San Joaquin Sup. Ct.",
        claims: "PC §290.46(j), Wrongful Failure to Hire, ICRAA, Invasion of Privacy, Negligence Per Se, UCL",
        status: "Complaint drafted/verified July 15, 2026; not yet filed",
        risk: "Favorable on the law but pled on information and belief — no admitted-basis letter or recovered background report, unlike Matters 22/23; strongest evidence is the application-to-denial notice trail (2 pre-adverse notices, 5 reminders)",
        settlement_note: "No wage documentation (never employed) caps economic damages relative to Matter 22; statutory penalty and fee-shifting are the main leverage points",
        conservative: 40000, moderate: 95000, aggressive: 220000,
        components: [
            { label: "PC §290.46(j)(4)(A) Statutory Penalty", conservative: 25000, moderate: 40000, aggressive: 75000 },
            { label: "Emotional Distress / Lost Opportunity", conservative: 8000, moderate: 25000, aggressive: 60000 },
            { label: "ICRAA Statutory + Punitive", conservative: 2000, moderate: 5000, aggressive: 10000 },
            { label: "Punitive (Civ. Code §3294)", conservative: 0, moderate: 10000, aggressive: 45000 },
            { label: "Fees — PC §290.46(j)(4)(A) / ICRAA", conservative: 5000, moderate: 15000, aggressive: 30000 }
        ]
    },
    {
        number: 26,
        caption: "Newanforbi v. United Parcel Service, Inc.",
        court: "San Joaquin Sup. Ct.",
        claims: "PC §290.46(j), Wrongful Failure to Hire, ICRAA, Invasion of Privacy, Negligence Per Se, UCL",
        status: "Complaint drafted/verified July 15, 2026; not yet filed — TIME-SENSITIVE (adverse action July 31, 2024)",
        risk: "Favorable on the law but pled on information and belief, as with Matter 25; principal risk is procedural — several causes carry 2-year limitations periods running from the July 31, 2024 adverse action",
        settlement_note: "Filing urgency is the dominant near-term issue; no wage documentation (never employed) caps economic damages relative to Matter 22",
        conservative: 35000, moderate: 85000, aggressive: 200000,
        components: [
            { label: "PC §290.46(j)(4)(A) Statutory Penalty", conservative: 25000, moderate: 35000, aggressive: 65000 },
            { label: "Emotional Distress / Lost Opportunity", conservative: 5000, moderate: 20000, aggressive: 55000 },
            { label: "ICRAA Statutory + Punitive", conservative: 2000, moderate: 5000, aggressive: 10000 },
            { label: "Punitive (Civ. Code §3294)", conservative: 0, moderate: 10000, aggressive: 40000 },
            { label: "Fees — PC §290.46(j)(4)(A) / ICRAA", conservative: 3000, moderate: 15000, aggressive: 30000 }
        ]
    },
    {
        number: 27,
        caption: "Newanforbi v. Randstad, et al.",
        court: "San Joaquin Sup. Ct.",
        claims: "PC §290.46(j), Wrongful Termination / Failure to Employ (Tameny), FCRA, ICRAA, UCL",
        status: "Pre-adverse notice received Jul. 13, 2026; adverse action expected on or after Jul. 21, 2026; complaint not yet filed",
        risk: "Extremely favorable — Plaintiff holds the actual InfoMart BGC report (Order No. 15780719): all 7 county/state criminal searches and federal criminal returned No Record; registry is the only flagged item; Billing Code 'RK LOGISTICS' and Client Package 'RK Logistics' in report header prove RK Logistics configured the criteria triggering 'NEEDS APPROVAL, PER CLIENT CRITERIA.' Rehire email establishes employment relationship existed at time of BGC — stronger Tameny posture than the pure failure-to-hire cases in Matters 25/26. Wage rate confirmed at $28.50/hr, 42.5 hrs/week (Mon–Fri 2:30 PM–11:00 PM), generating overtime each week; actual lost wages eclipse the §290.46(j)(4)(A) $25,000 statutory floor within approximately 6.5 months, making actual-damages the operative measure.",
        settlement_note: "Fifth PC §290.46(j) matter in portfolio; pattern evidence across five employers strengthens willfulness showing on all. Two-defendant structure (Randstad US, LLC as employer of record + RK Logistics Group, Inc. as criteria-setting end client) creates cross-pressure: each defendant is incentivized to attribute the adverse decision to the other. Punitive exposure is amplified by both defendants' substantial net worth — Randstad is a subsidiary of a global staffing company; RK Logistics serves the semiconductor and EV supply chain. Rehire posture + documented wage rate produces back pay and front pay exposure not present in Matters 25/26.",
        conservative: 179838, moderate: 437095, aggressive: 834352,
        components: [
            { label: "Lost Wages — Back Pay ($28.50/hr × 42.5 hrs/wk incl. weekly OT at 1.5x; $1,246.88/wk: conservative 12 mo. / moderate 18 mo. / aggressive 24 mo.)", conservative: 64838, moderate: 97257, aggressive: 129676 },
            { label: "Front Pay — Future Lost Earnings (conservative: none / moderate: 12 additional mo. / aggressive: 24 additional mo.)", conservative: 0, moderate: 64838, aggressive: 129676 },
            { label: "Emotional Distress — Wrongful rescission of accepted rehire position; fifth cumulative §290.46(j) employment denial compounds distress narrative", conservative: 25000, moderate: 50000, aggressive: 75000 },
            { label: "FCRA / ICRAA Statutory + Punitive (willful noncompliance; InfoMart report itself contains FCRA Summary of Rights and CA ICRA Notice — parties had constructive notice of the statutory framework at the moment of use)", conservative: 15000, moderate: 25000, aggressive: 50000 },
            { label: "Punitive (Civ. Code §3294) — Two corporate defendants with independent net worth exposure; fifth repeat §290.46(j) violation supports willfulness finding; 'NEEDS APPROVAL, PER CLIENT CRITERIA' shows deliberate criteria configuration, not inadvertent use", conservative: 50000, moderate: 150000, aggressive: 350000 },
            { label: "Attorney Fees — PC §290.46(j)(4)(A) mandatory fee-shifting + FCRA + ICRAA", conservative: 25000, moderate: 50000, aggressive: 100000 }
        ]
    },
    {
        number: 28,
        caption: "Newanforbi v. Shannon Smith, LCSW, CEO, et al.",
        court: "USDC N.D. Cal.",
        claims: "42 U.S.C. §1983 Monell + Individual Capacity; Bane Act §52.1; Fraud/Negligent Misrepresentation; RICO §1962(c)-(d)",
        status: "Complaint mailed Jul. 16, 2026; anticipated receipt Jul. 20, 2026",
        risk: "Favorable on state-actor theory (West v. Atkins); Monell supported by In re Dwyer condemnation of HOPE's blanket retention policy and HOPE's own Clinical Operational Manual; RICO carries dismissal risk but is pleaded as aggressive multiplier; Philadelphia Indemnity insurance ($1M per-incident / $5M aggregate) creates realistic settlement floor",
        settlement_note: "Shannon Smith's individual-capacity exposure creates personal settlement pressure independent of HOPE's corporate insurance. 542 pages of discovery already in hand from dismissed state case. RICO treble exposure ($249K–$1.51M range) and §1988 fee shifting give Plaintiff substantial leverage. Insurance floor anchors realistic resolution in the $500K–$1M range on moderate facts.",
        conservative: 249000, moderate: 666000, aggressive: 1510000,
        components: [
            { label: "Lost CDL Wages — Economic Harm (documented W-2s: $109,408+ over 2022–2024; $72K/yr but-for CDL career rate; conservative: 2 yr / moderate: 3 yr / aggressive: 5 yr)", conservative: 144000, moderate: 216000, aggressive: 360000 },
            { label: "§1983 Compensatory Damages — Constitutional deprivation, liberty-interest violation, emotional distress (Monell against HOPE + individual capacity against Smith)", conservative: 30000, moderate: 100000, aggressive: 200000 },
            { label: "Bane Act §52.1 — Coercive interference with constitutional rights ($25,000 statutory minimum per violation; multiple violations alleged)", conservative: 25000, moderate: 75000, aggressive: 150000 },
            { label: "RICO §1964(c) — Treble damages for enterprise conduct (fraudulent billing to CDCR; false adverse reporting to parole agents); conservative: $0 (dismissal risk) / moderate: $150K / aggressive: $450K", conservative: 0, moderate: 150000, aggressive: 450000 },
            { label: "Punitive Damages — §1983 against Shannon Smith individually; Bane Act treble exposure; deliberate policy of retaliatory reporting", conservative: 25000, moderate: 75000, aggressive: 200000 },
            { label: "Attorney Fees — 42 U.S.C. §1988 (§1983 / Bane Act); RICO fee shifting", conservative: 25000, moderate: 50000, aggressive: 150000 }
        ]
    }
];
