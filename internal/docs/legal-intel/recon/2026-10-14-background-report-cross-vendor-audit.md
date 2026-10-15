# Matter 29 - Cross-Vendor Background-Report Factual Audit

**Prepared:** October 14, 2026  
**Scope:** Compare Brendan Ngwa Nforbi's Amazon/Accurate report with independently generated employment-screening reports in the portfolio. This is an evidence audit, not a damages calculation or a pleading.

## Executive finding

Accurate reported `NATIONAL SEX OFFENDER DATABASE SEARCH - NO RECORD FOUND` on July 7, 2026 and retained that result when the report was updated on October 14, 2026. Seven distinct comparator reports found the California registry record before or after Accurate's search. The comparator reports match the subject through combinations of name, date of birth, address, aliases, and, in InfoMart, physical description.

The clean factual discrepancy is therefore the registry-search outcome. The comparison does not establish that Accurate's separately reported Santa Clara conviction data is false.

## Canonical source inventory

| Vendor | Requestor | Report/search date | Portfolio path | SHA-256 |
|---|---|---:|---|---|
| Accurate Background | Amazon HVH | searched Jul. 7, 2026; updated Oct. 14, 2026 | `documents/matter-29/Accurate Background - Consumer Report (Amazon HVH, Ref 496623722, updated Oct 14 2026).pdf` | `fcbcdbcfd1e2de374f486881d082068729ced5ad608ba37119e9899649ae83ee` |
| First Advantage | UPS | completed Jul. 18, 2024 | `documents/matter-26/Dkt 07 Exhibit A - First Advantage Background Report (Filed Aug 26 2026).pdf` | `1ea3acae35f459791145b5fc32948c3fdf0e5cc91e4cf3d5b699b3cb9995a5a1` |
| Checkr | Pilot Travel Centers | completed Dec. 23, 2025 | `documents/matter-22/Checkr - Pilot Travel Centers - Background Check Report (Completed Dec 23 2025).pdf` | `76d27191d49e6d2bbbab4ebbf3dc471262f90a8fb3bb985ed2ce0957502f5af9` |
| Checkr | Next Chapter Project | completed Mar. 27, 2026 | `documents/matter-29/Checkr Consumer Report - Next Chapter Project (Report 2998b72edcf19a05d25ab058, Completed Mar 27 2026).pdf` | `bebf538d733961c8c86f3b0897f214b8e3eb25954ed56bdeb40a7bbb671b0ebf` |
| HireRight | Macy's | requested May 28, 2026; registry verified May 29, 2026 | `documents/matter-23/HireRight - Macy's - Background Check Report (Requested May 28 2026).pdf` | `df0a80a14aed3dae08515de362abeacc0f181614f3934fcc0e4848c196dd4b48` |
| InfoMart | RK Logistics | completed Jul. 13, 2026 | `documents/matter-27/InfoMart - RK Logistics - Background Check Report (Order 15780719, Completed Jul 13 2026).pdf` | `d8a2b75750f56a2760d2650a56ca668ece4424e576e03fe877641a2fe94d16f3` |
| Checkr | Next Chapter Project | completed Aug. 7, 2026 | `documents/matter-29/Checkr Consumer Report - Next Chapter Project (Report d1eb77b8c7c4e1cf783dfa24, Completed Aug 7 2026).pdf` | `6472486fc9f8fe23017e87fdf91ab88e86bb35a3f15a65b8d93bf1c05858f624` |
| Checkr | Nuro | completed Oct. 6, 2026 | `documents/matter-29/Checkr Consumer Report - Nuro (Report fdd27d50df88c6073f30aecc, Completed Oct 6 2026).pdf` | `49fd1b2e8e1c6e1737b3c2a7bd8bec8cdf3f4fa7be2efd34d08aa578a8b10ad8` |

The second uploaded Pilot/Checkr PDF was byte-for-byte identical to the canonical Pilot report and is not separately committed.

## Registry-result chronology

| Date | Vendor | Recorded result |
|---|---|---|
| Jul. 18, 2024 | First Advantage | `Record Found`; source identified as `CALIFORNIA SEX OFFENDER REGISTRY` |
| Dec. 16-23, 2025 | Checkr / Pilot | `CA SEX OFFENDER REGISTRY`; full-name and DOB match |
| Mar. 26-27, 2026 | Checkr / Next Chapter | `CA SEX OFFENDER REGISTRY`; full-name and DOB match |
| May 29, 2026 | HireRight / Macy's | Applicant listed in California; verified using AKA, DOB, and address |
| Jul. 7, 2026 | Accurate / Amazon | `NO RECORD FOUND` |
| Jul. 13, 2026 | InfoMart / RK Logistics | California sex-offender `Record`; matching name, DOB, aliases, and physical description |
| Aug. 5-7, 2026 | Checkr / Next Chapter | `CA SEX OFFENDER REGISTRY`; full-name and DOB match |
| Sep. 23-Oct. 6, 2026 | Checkr / Nuro | `CA SEX OFFENDER REGISTRY`; full-name and DOB match |
| Oct. 14, 2026 | Accurate / Amazon | Updated report still carries the Jul. 7 `NO RECORD FOUND` result |

## Findings

### 1. Accurate's registry result conflicts with every comparator

The surrounding chronology rules out a newly created record as an explanation. First Advantage, Checkr, and HireRight found the California registry record before Accurate's July 7 search; InfoMart found it six days later; later Checkr reports continued to find it.

### 2. The comparator match is identity-specific

The comparator reports do not rely on name alone. They use consistent name variants, the same date of birth, address or alias verification, and, in InfoMart, a matching physical description. This supports discovery directed to Accurate's search inputs, name parsing, source coverage, match thresholds, quality-control review, and any October reinvestigation or package-review activity.

### 3. Accurate carries an unsupported name variant

Accurate lists `NGWA NFORBI, NEWANSORBI` and labels it applicant-provided. The comparator reports instead use recognizable variants including `NEWANFORBI`, `NGWANFORBI`, `NGWA-NFORBI`, and `NFORBI`. No comparator supports the spelling `NEWANSORBI`. The Accurate entry also appears to transpose name fields.

### 4. Court and registry results must remain separate

Several comparator reports returned clear or no-record county results while separately returning a positive registry record. Accurate later found Santa Clara County case C1761642 while reporting a negative registry result. A county-court result does not validate or cure the contrary registry-search result, and a comparator's clear county result does not prove that the conviction does not exist.

## Limits of the comparison

- The comparator reports do not independently verify Accurate's filing date, disposition date, restitution figures, costs, sentence credits, or statutory charge coding.
- Those fields require comparison against the certified Santa Clara docket, minute order, abstract of judgment, and sentencing records.
- The registry false negative demonstrates a reporting inconsistency and likely search, coverage, or matching failure. Causation must still be tied to the information Amazon actually used.

## Recommended discovery targets

1. Accurate's raw query inputs and parsed name fields for every component search.
2. The vendor/database used for Search ID 496623723 and its California coverage on July 7, 2026.
3. Match thresholds, suppression rules, alias logic, and exception or error logs.
4. Audit history for the October 13 package review and October 14 update/notification.
5. All communications and result transmissions to Amazon, including component-level result changes.
6. Documents showing how `NEWANSORBI` entered the file and why it was attributed to the applicant.
7. Any reinvestigation notes generated after Accurate obtained the Santa Clara record.
