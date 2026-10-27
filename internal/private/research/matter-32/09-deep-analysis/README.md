# Matter 32 Opposition Research Engine

This is an internal, decision-oriented research product for opposing ECF 22, not a filing-ready brief or an assurance that all six counts survive. It replaces the earlier workshop scaffold as the analytical starting point and integrates the Matter 20 production with the operative FAC, actual blood-warrant application, historical Chi Soo Kim recommendation, and favorable and adverse authority.

The separately authored [upstream controlling synthesis](../04-workshop/opposition-deep-research-analysis.md), added while this package was being finalized, is preserved unchanged and should be read alongside this package. The companion analysis adds particular emphasis to the 01:07:29 parole-log boundary, independent DMV/property causation, and Richards's qualification of a universal strict-but-for formulation.

## Read in this order

- **[Decision memorandum](opposition-decision-memorandum.md)**: The core synthesis, ranked opportunities, six claim modules, actual corrected-affidavit analysis, qualified-immunity divisions, historical comparison, damages causation, and recommended disposition.
- **[Evidence-to-claim matrix](evidence-to-claim-matrix.md)**: What each material proposition actually establishes, what it does not establish, its source locator, and its proper use at pleading, amendment, or proof.
- **[Authority treatment ledger](authority-treatment-ledger.md)**: Favorable, adverse, and mixed authorities, with primary-text links, limits, temporal eligibility, and research status.
- **[Amendment and proof proffer](amendment-and-proof-proffer.md)**: Concrete corrections to the operative paragraphs, conditional amendment options, and the records needed to support them.
- **[Red team and brief blueprint](red-team-and-brief-blueprint.md)**: The strongest defense version, issue allocation for a bounded brief, proposed argument language, and questions a skeptical judge is likely to ask.
- **[Research controls](research-controls.json)**: Machine-readable claim map and filing gates. Run `node internal/private/research/matter-32/09-deep-analysis/validate-deep-analysis.mjs` from the repository root to verify internal consistency and supplemental-source hashes.

## Important findings

- **The form-label theory requires correction.** The CHP 202 says “BREATH ODOR OF ALCOHOLIC BEVERAGE PRESENT,” not that an alcoholic drink was found. Source R195, PDF p. 2, AGO 000030, was inspected visually.
- **The toxicology was not negative for ethanol.** The report states 0.073 ± 0.004 grams %, released November 25, 2024. Source R195, PDF p. 6, AGO 000034, was inspected visually.
- **The warrant is a separate instrument.** Its narrative appears at R195, PDF pp. 20–21, AGO 000048–49. It does not expressly assert slurred speech or an alcoholic cup, and both pages were inspected visually.
- **The parole boundary matters.** The incident log records active-parole information at 01:07:29, after the alleged door opening and cup examination. Source R193 supplies the entry; it does not, by itself, conclusively establish when each officer first received the information.
- **The no-charges argument is not the end of the fabrication analysis.** Costanich recognizes a civil-proceeding fabrication theory in its particular setting, and the current model instruction expressly includes “other deprivation of liberty”; neither authority automatically establishes this DMV claim. ([Costanich](https://www.courtlistener.com/opinion/180346/costanich-v-dept-of-social-and-health-services/); [Ninth Circuit Instruction 9.38, revised June 2025](https://cdn.ca9.uscourts.gov/datastore/jury-instructions/civil/9-38-particular-rights-fourteenth-amendment-due-process-deliberate-fabrication-of-evidence.pdf))

## Scope and verification

The original room's 224 preserved assets and their original hash manifest remain unchanged. New authority captures have a separate `supplemental-source-manifest.json`; that manifest distinguishes downloaded originals from retrieval failures rather than silently substituting another document.

Record labels R001–R224 refer to the original room manifest, not court exhibit numbers. References to “FAC” mean R125, the conformed 21-page ECF 5 filed August 17, 2026; references to “MTD” mean R001, ECF 22 filed October 26, 2026, with printed memorandum page numbers unless stated otherwise.

The legal research was checked against accessible opinion text, not a commercial citator. Current docket status, subsequent treatment, original MP4 verification in this workspace, the precise DMV adjudicative basis, and the adopted/final status of historical recommendations remain explicit gates; no research conclusion changes a live deadline.

This branch is private research only. No court submission, deployment, R2 mutation, merger into `main`, or live matter/calendar update is authorized by this package.
