# Matter 32 MTD Opposition Workshop

Private, branch-only research room for Nforbi v. Meza-Gonzalez and Melano, N.D. Cal. 4:26-cv-08271-ASK. Created October 26, 2026 to workshop the strongest supportable opposition to ECF 22, not to recycle every historical allegation or file an unverified brief.

## Start here

- **Controlling synthesis:** `04-workshop/opposition-deep-research-analysis.md` converts the record into claim triage, corrected-affidavit analysis, a conduct-specific immunity map, an adversarial-leakage audit, amendment proffer, page budget, and ranked completion plan.
- **Companion research engine:** [Opposition Research Engine](09-deep-analysis/README.md) adds a 5,000+ word decision memorandum, corrected FAC map, evidence matrix, authority treatment, amendment proffer, and red-team brief architecture. Read it with the controlling synthesis, especially for pre-parole timing, the distinct DMV/property theory, and the Richards causation qualification.
- **Supersession notice:** The original seven `04-workshop` scaffolds and the earlier `5b306800` analysis remain as historical drafts. Some use obsolete FAC paragraph anchors or incomplete no-charges, toxicology, protected-activity, or two-dismissal analysis; use the two research syntheses above instead.
- **Third synthesis, ECF 5-keyed (Oct. 27):** `04-workshop/opposition-deep-research-v2-2026-10-27.md` was written in parallel with the two above. It reaches the same core calls (toxicology and affidavit stay internal; correct the form-label error; lead with entry; no Rule 41 in the brief). It adds line-pinned MTD errors, per-authority verification tags, the Romberg timer gap (eyes open 01:08:40 vs. timer stop 01:08:45), Meza's sworn knock-then-door sequence for the amendment, Lingo damages scope, and repo data corrections. It differs in recommending non-opposition with leave on Counts 2 and 6. Reconcile that choice before drafting.
- **Decision memo:** `04-workshop/strategy-and-risk.md` identifies the strongest lanes and the factual concessions that improve credibility.
- **Response map:** `04-workshop/mtd-response-matrix.md` tracks every numbered defense argument.
- **Historical comparison:** `04-workshop/chi-soo-kim-to-current-fac.md` confronts the April 2026 adverse reasoning and distinguishes procedural history from merits.
- **Working brief:** `04-workshop/opposition-working-draft.md` supplies editable advocacy language, with unresolved portions expressly blocked.
- **Warrant workbench:** `04-workshop/corrected-affidavit-workbench.md` keeps the actual affidavit, alleged corrections, remaining facts, and materiality analysis separate.
- **Filing gates:** `04-workshop/verification-and-filing-gates.md` covers docket, briefing clock, source, video, authority, and amendment checks.
- **Authority status:** `04-workshop/authority-ledger.md` separates verified holdings from research leads and adverse authority.
- **Source inventory:** `08-audit/inventory.md` and `08-audit/manifest.json` provide hashes, original paths, retrieval methods, source commits, duplicate occurrences, and missing assets.
- **Verification results:** `08-audit/verification-results.md` distinguishes successful room checks from unchanged baseline whole-portfolio validation failures.

## What is preserved

- **Current input:** ECF 22, the 19-page motion filed October 26, 2026; ECF 23, defendants' one-page magistrate-jurisdiction DECLINATION. The original attachment filenames are preserved, but the second attachment is not an MTD.
- **Portfolio record:** Current FAC, earlier complaints and motion papers, plaintiff's objections to Kim's recommendation, prior dismissal papers, ND Cal service history, and related screening material.
- **Incident and production:** Arrest materials, transcript, incident log, CHP 415 declarations, laboratory and DMV records, and the produced CHP 202 / DS 367 / warrant-affidavit packet from the Matter 20 research branch.
- **Historical context:** Matter 01, 02, 20, 24, 32, and 33 graph snapshots, labeled as snapshots rather than live docket verification.
- **External verification:** Primary appellate authorities and a retrieved public text reproduction of Kim's April 20, 2026 recommendation. A public text reproduction is not the stamped original recommendation PDF.

## Nonnegotiable corrections

- **Form label:** Produced CHP 202 p. 2, AGO 000030, says “BREATH ODOR OF ALCOHOLIC BEVERAGE PRESENT.” It does not say an alcoholic beverage was physically present. DS 367 p. 1, AGO 000040, says “Odor of alcoholic beverage.” Do not perpetuate the FAC's beverage-checkbox characterization.
- **Odor evidence:** A recording cannot directly establish whether an odor existed. Absence of an audible odor statement is not proof of fabrication.
- **Warrant:** Produced affidavit is in Exhibit 5, PDF pp. 20–21, AGO 000048–000049. It is not identical to the CHP 202 or DS 367.
- **Judicial officer:** The warrant copy identifies Judge Amy Sekany. Do not conflate the blood-draw warrant with the separate Whitman probable-cause/custody review.
- **Video:** Preserved transcript is plaintiff-created, contains speaker/name and pagination anomalies, and is not a substitute for watching the original recording.
- **Rule 12:** Do not use this evidence collection to insert unpleaded facts into the FAC through an opposition.

## Boundary of this branch

This follows the Matter 20 research-room pattern: source preservation, extracted text, adverse-evidence analysis, and explicit filing gates. It does not change `main`, the live matter graph, procedural clocks, public site, Cloudflare deployment, R2 objects, or D1 records. It does not merge the Matter 20 branch into this branch.

No filing, service, court communication, public deployment, or live docket certification is authorized or performed. Research judgments are provisional; original records and independently checked law control.

## Quick checks

```sh
cd internal/private/research/matter-32
sha256sum -c 08-audit/SHA256SUMS
node 08-audit/validate-workshop.mjs
```

The source manifest records exact bytes and deduplication. The workshop deliberately retains selected retrieval gaps, unresolved factual conflicts, and authority-update tasks instead of claiming a complete or filing-ready record.
