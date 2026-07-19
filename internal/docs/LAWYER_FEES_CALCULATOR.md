# Granular Litigation Fee Calculator
## Brendan Ngehsi Newanforbi — 24 Matters Portfolio
### Analysis Date: July 11, 2026 (full revision of the May 29, 2026 draft)

---

## What changed in this revision

The May 29, 2026 draft estimated document lengths by description ("664-page complaint," "712-page CASOMB complaint," "396-page DS2044 discovery"). Those figures do not match the files actually sitting in `public/documents/matter-XX/`. This revision:

1. Ran `pdfinfo` (poppler-utils) against every one of the **203 real PDF files** across all 24 matter folders to get exact page counts — no filename-based guessing.
2. Dispatched five parallel analysis passes (one per case cluster) to classify each real file by document type (complaint, motion/opposition/reply, discovery, writ/habeas, declaration, administrative, evidence) and price it against the rate methodology below.
3. Added the 3 matters that didn't exist in the prior draft (Matters 22, 23, 24) and corrected status for 8 matters voluntarily dismissed since May 29 (Matters 4, 11, 13, 16, 17, 18, 21, plus Matter 6 dismissed without prejudice and Matter 22 now **settled**, July 11, 2026).

**Net effect: the portfolio-wide estimate drops from $1.44M–$2.23M (mid $1.83M) to $646K–$1.04M (mid $845K).** The single biggest driver is that several "signature" documents referenced by description in the old draft (Matter 3's 664-page complaint, Matter 5's 712-page complaint) simply are not among the uploaded PDFs — the real complaints in those matters run well under 100 pages each.

---

## Methodology

**Hourly Billing Rates (Realistic Market Rates):**
- **Senior Partner/Complex Litigation:** $350–$450/hr (motion practice, appeals)
- **Associate/Mid-Level:** $250–$350/hr (pleadings, discovery, trial prep)
- **Paralegal/Support:** $150–$200/hr (document review, organization)
- **Blended average used throughout:** $280/hr

**Billing principles applied by every analysis pass:**
- Opposing counsel's own filings (their MTDs, demurrers, replies) are billed only at a light review rate, never at drafting rate — a lawyer hired by the plaintiff drafts the plaintiff's filings, not the defendant's.
- Near-duplicate/re-filed copies of the same document (e.g., two identical scanned copies of a writ petition) are billed once at full rate, with only incremental hours for the duplicate.
- Large PDFs that are discovery dumps, exhibit compilations, or scanned evidence bundles are billed at a lighter review/compilation rate (~0.3–0.5 hr/page), never at complaint-drafting rate, regardless of raw page count.
- Writ of mandate and habeas corpus petitions are billed as flat specialized-practice blocks (40–80 hrs) rather than per page.
- Matters with no uploaded PDFs (4, 11, 13, 17, 18) are estimated conservatively from `matters.js` status/procedural-history text — not assumed to be zero-cost, since a complaint was in fact filed in each.

**Work Unit Conversions:**
- **Complaint/major pleading:** ~2–3 hrs per page (research, drafting, revisions, filing)
- **Motion briefing (MTD/demurrer/M4L, opposition, reply):** ~0.6–1.2 hrs per page, or 40–80 hr flat blocks for large integrated filings
- **Discovery responses:** ~0.3–0.5 hrs per page
- **Declarations/short filings:** ~1–2 hrs per document (not per page)
- **Writ petitions / habeas corpus:** 40–80 hrs flat (specialized administrative/procedural law)
- **Administrative/notices/case-management filings:** 0.5–2 hrs per document, not per page
- **Evidence/exhibit compilation:** ~0.3–0.5 hrs/page

---

## Per-Matter Estimates (ground-truth page counts)

| # | Caption | Court | Docs | Real Pages | Hours (low–high) | Cost Low | Cost Mid | Cost High |
|---|---|---|---|---|---|---|---|---|
| 1 | Newanforbi v. CHP et al. | USDC E.D. Cal. | 23 | 108 | 48–85 | $13,552 | $18,704 | $23,856 |
| 2 | Newanforbi v. Meza-Gonzalez et al. | Alameda Sup. Ct. | 16 | 111 | 68–117 | $19,152 | $25,900 | $32,648 |
| 3 | Newanforbi v. Derrick et al. | USDC E.D. Cal. | 26 | 290 | 191–352 | $53,424 | $75,936 | $98,448 |
| 4 | Newanforbi v. Derrick et al. (State Mirror) | San Joaquin Sup. Ct. | 0* | 0* | 42–94 | $11,620 | $18,970 | $26,320 |
| 5 | Newanforbi v. Palacios et al. | San Joaquin Sup. Ct. | 33 | 821 | 420–683 | $117,628 | $154,406 | $191,184 |
| 6 | Newanforbi v. HOPE et al. | USDC E.D. Cal. | 4 | 101 | 193–292 | $54,040 | $67,900 | $81,760 |
| 7 | Newanforbi v. Candelaria | USDC E.D. Cal. | 16 | 181 | 185–288 | $51,688 | $66,150 | $80,612 |
| 8 | Newanforbi v. Candelaria, et al. | Sacramento Sup. Ct. | 2 | 88 | 51–81 | $14,140 | $18,410 | $22,680 |
| 9 | Newanforbi v. Macomber (Writ) | Sacramento Sup. Ct. | 9 | 179 | 65–116 | $18,200 | $25,340 | $32,480 |
| 10 | Newanforbi v. Macomber (Habeas) | Santa Clara Sup. Ct. | 2 | 3 | 41–72 | $11,340 | $15,750 | $20,160 |
| 11 | Newanforbi v. Macomber (Federal) | USDC E.D. Cal. | 0* | 0* | 31–76 | $8,540 | $14,910 | $21,280 |
| 12 | Ngwa Nforbi v. Diamond Truck Sales | San Joaquin Sup. Ct. | 17 | 131 | 136–220 | $38,080 | $49,840 | $61,600 |
| 13 | Newanforbi v. Urrea et al. (Federal) | USDC E.D. Cal. | 0* | 0* | 31–76 | $8,540 | $14,910 | $21,280 |
| 14 | Newanforbi v. Urrea et al. (State) | San Joaquin Sup. Ct. | 1 | 28 | 70–95 | $19,600 | $23,100 | $26,600 |
| 15 | Newanforbi v. CDCR, et al. | San Joaquin Sup. Ct. | 17 | 445 | 300–418 | $84,000 | $100,520 | $117,040 |
| 16 | Newanforbi v. Rojo | San Joaquin Sup. Ct. | 1 | 32 | 64–80 | $17,920 | $20,160 | $22,400 |
| 17 | Newanforbi v. Maloney et al. | USDC E.D. Cal. | 0* | 0* | 56–80 | $15,680 | $19,040 | $22,400 |
| 18 | Newanforbi v. Barocio | USDC E.D. Cal. | 0* | 0* | 55–75 | $15,400 | $18,200 | $21,000 |
| 19 | Newanforbi v. Macomber (Habeas, Discharge) | Santa Clara Sup. Ct. | 2 | 69 | 41–72 | $11,340 | $15,750 | $20,160 |
| 20 | Newanforbi v. CHP (Writ of Mandate) | Alameda Sup. Ct. | 18 | 390 | 81–138 | $22,624 | $30,618 | $38,612 |
| 21 | Newanforbi v. Rojo et al. (Federal) | USDC E.D. Cal. | 1 | 9 | 28–41 | $7,840 | $9,660 | $11,480 |
| 22 | Newanforbi v. Pilot Travel Centers LLC | San Joaquin Sup. Ct. | 7 | 47 | 62–102 | $17,360 | $22,960 | $28,560 |
| 23 | Newanforbi v. Macy's Inc. et al. | San Joaquin Sup. Ct. | 2 | 11 | 4–8 | $1,120 | $1,680 | $2,240 |
| 24 | Newanforbi v. Serrato | USDC N.D. Cal. | 6 | 58 | 47–72 | $13,020 | $16,590 | $20,160 |

\* No documents folder exists in `public/documents/` for this matter — a complaint was filed and later voluntarily dismissed, but was never uploaded to the portfolio site. Estimated from `matters.js` status/procedural-history text.

---

## Aggregate Cost Summary

### By Cluster

| Cluster | Matters | Low | Mid | High |
|---|---|---|---|---|
| **CHP / DUI / DMV** | 1, 2, 7, 8, 20, 24 | $134,176 | $176,372 | $218,568 |
| **Parole Retaliation / HOPE** | 3, 4, 5, 6, 11, 13, 14, 15, 16, 17, 18, 21 | $414,232 | $537,712 | $661,192 |
| **Consumer Fraud / Employment** | 12, 22, 23 | $56,560 | $74,480 | $92,400 |
| **Administrative Writs & Habeas** | 9, 10, 19 | $40,880 | $56,840 | $72,800 |

### TOTAL PORTFOLIO COST (24 matters, 203 documents, 3,102 real pages)

**Conservative (Low End):** **$645,848** (2,307 hrs)

**Mid-Point:** **$845,404** (3,019 hrs)

**Aggressive (High End):** **$1,044,960** (3,732 hrs)

---

## Comparison to Damages Claimed

Current portfolio-level damages exposure (per `src/data/damages.js`, deduplicated for shared economic events):

| Exposure Level | Damages Claim | Estimated Lawyer Fees (Mid) | Ratio (Fees/Damages) |
|---|---|---|---|
| Conservative | $1,050,000 | $845,404 | 81% |
| Moderate | $2,690,000 | $845,404 | 31% |
| Aggressive | $5,605,000 | $845,404 | 15% |

At the conservative exposure level, hiring counsel would have consumed roughly **four out of every five dollars** ultimately recoverable. At moderate exposure, fees drop to about **31%** of recovery — still a substantial bite, but far less severe than the prior draft's 66% figure (which was inflated by overstated page counts).

---

## Pro Se Savings Analysis

| Scenario | Low | Mid | High |
|---|---|---|---|
| Actual cost paid (pro se) | $0 | $0 | $0 |
| Cost if hired counsel | $645,848 | $845,404 | $1,044,960 |
| Savings ignoring the litigant's own time | **$645,848** | **$845,404** | **$1,044,960** |
| Litigant's own time (3,019 hrs @ $300/hr opportunity cost) | $905,790 | $905,790 | $905,790 |
| **Net savings after opportunity cost** | **–$259,942** | **–$60,386** | **$139,170** |

**Honest reading:** once the litigant's own time is valued at a professional's opportunity-cost rate ($300/hr), the ground-truth analysis shows the pro se path is roughly a wash against hiring counsel at a blended $280/hr rate — not the large net win the May 29 draft implied. The real advantage of proceeding pro se here is less about raw dollar savings and more about **preserving 100% of any eventual recovery** (no contingency cut) and retaining full control over 24 simultaneously active matters that a single retained firm would likely have had to triage or decline.

---

## Risk & Quality Factors

**Risks of Pro Se Representation:**
1. Motion practice execution — MTD/demurrer oppositions are competent but lack the polish of experienced litigation counsel on close procedural questions (qualified immunity, exhaustion).
2. Discovery completeness on the larger matters (Matter 5's 377 pages of bilateral discovery, Matter 15's evolving complaint record).
3. Damages quantification lacks expert affidavits (emotional distress multipliers, HOPE billing-structure experts).
4. Eight matters were voluntarily dismissed since the May 29 draft (Matters 4, 11, 13, 16, 17, 18, 21, and 6 without prejudice) — a real cost of pro se triage under caseload pressure that a funded firm might have avoided by not filing marginal matters in the first place.

**Strengths of Pro Se Approach:**
1. Factual mastery across a genuinely interconnected 24-matter record.
2. No contingency or hourly fee erodes any eventual recovery.
3. Matter 22 (Pilot Travel Centers) settled in under six weeks pro se, before service was even completed — a result that speaks for itself.

---

## Conclusion

Ground-truth document analysis (pdfinfo page counts + document-type classification across all 203 uploaded PDFs) puts the realistic cost of retained counsel for this 24-matter portfolio at **$646K–$1.04M, mid-point $845K** — a substantial revision downward from the May 29, 2026 draft's $1.44M–$2.23M estimate, because several of that draft's page counts for "signature" filings (Matter 3's complaint, Matter 5's complaint) do not correspond to any file actually in the repository.

Once the litigant's own time is priced at a professional opportunity-cost rate, the net savings from proceeding pro se are close to break-even at the mid-point — the real value of the pro se path lies in retaining full recovery and control over a caseload no single retained firm could realistically carry at this scale, not in a dramatic fee-avoidance windfall.

---

*Report prepared: July 11, 2026*
*Methodology: pdfinfo (poppler-utils) real page-count extraction across 203 PDFs in `public/documents/`, five parallel document-classification and fee-estimation passes (one per case cluster), hourly billing benchmarks, federal/state litigation standards.*
