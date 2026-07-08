export const damages_table = [
    { category: "Lost Wages / Economic Harm", matters: "1, 2, 3, 5, 7, 15, 22", conservative: 275000, moderate: 580000, aggressive: 935000 },
    { category: "False Imprisonment", matters: "1, 2, 15", conservative: 65000, moderate: 165000, aggressive: 325000 },
    { category: "Emotional Distress", matters: "1, 2, 3, 5, 7, 15, 22, 24", conservative: 85000, moderate: 240000, aggressive: 535000 },
    { category: "Bane Act / Treble", matters: "1, 2, 5", conservative: 75000, moderate: 200000, aggressive: 450000 },
    { category: "Punitive Damages", matters: "1, 2, 3, 5, 7, 15, 22, 24", conservative: 165000, moderate: 595000, aggressive: 1500000 },
    { category: "Consumer Fraud", matters: "12", conservative: 40000, moderate: 75000, aggressive: 150000 },
    { category: "Attorneys' Fees", matters: "1, 3, 5, 7, 22, 24", conservative: 50000, moderate: 110000, aggressive: 260000 },
    { category: "PC §290.46(j) Violation + Wrongful Termination (Matter 22)", matters: "22", conservative: 220000, moderate: 525000, aggressive: 1000000 },
    { category: "42 USC §1983 — Arbitrary U Visa Certification Denial & Retaliation (Matter 24)", matters: "24", conservative: 75000, moderate: 200000, aggressive: 450000 }
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
        status: "Demurrer hearing July 15, 2026; discovery ongoing",
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
        settlement_note: "Default against Diamond may resolve fastest; Dakota Financial LLC service pending",
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
    }
];
