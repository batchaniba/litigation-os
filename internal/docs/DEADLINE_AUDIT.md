# Deadline & Statute-of-Limitations Sweep
## Brendan Ngehsi Newanforbi — 24 Matters Portfolio
### Analysis Date: July 14, 2026

---

## Purpose and methodology

The app's Deadline Clock is driven entirely by `src/data/timeline.js` entries flagged `upcoming: true`. If any of those are wrong, or if a real deadline exists in the court record but was never entered, the litigant could miss a filing or a hearing without warning. This sweep pulled every deadline actually stated inside the real PDFs — scheduling orders, notices of hearing, discovery proofs of service, demurrers, complaints — and diffed it against what the app currently shows.

Five parallel analysis passes read the source documents (not just `timeline.js` summaries) for the same five matter groupings used in the prior audits, and cross-checked every date against the applicable statute-of-limitations rule where relevant (Gov. Code §911.2/§945.6 government-claims deadlines, CCP §335.1 general tort SOL, CCP §338(d) fraud SOL, 42 U.S.C. §1983's 2-year borrowed period).

**154 timeline.js entries reviewed. 77 individual findings logged across all five groups: 31 CONFIRMED clean, 14 STALE, 16 WRONG_DATE, 16 MISSING.**

---

## Part 1 — Act now

These are live, near-term items, ranked by how soon they matter.

**1. The litigant has his own discovery response deadline in ~6 days that isn't tracked anywhere.** (Matter 5) Defendants Palacios/HOPE propounded Requests for Admission, Requests for Production, and Special Interrogatories (Set One) on the litigant himself, served June 18, 2026. Response is due **on or about July 20, 2026**. The existing `timeline.js` entry for June 18 has the direction backwards — it describes the litigant as the propounding party, when the actual documents show Defendants propounded on him. This is likely why his own deadline was never captured. Missing this risks waived objections and a motion to compel/sanctions.

> RFA/RFP/SROGS to Pl (061826).pdf captions: *"PROPOUNDING PARTY: Defendants KATIE PALACIOS and HOPE PROGRAM ... RESPONDING PARTY: Plaintiff"*

**2. Defendants' own discovery response deadline, ~3 days out, also untracked.** (Matter 5) The litigant propounded Special Interrogatories, Set Two, on HOPE and Palacios on June 17, 2026 — their response is due **on or about July 17, 2026**. Not in `timeline.js` at all. Worth tracking so any follow-up meet-and-confer or motion-to-compel deadline isn't missed either.

**3. Matter 8's fee-waiver hearing, listed for July 17 (3 days out), could not be independently verified.** The agent searched the reviewed portion of an 86-page combined filing and could not locate source text for either the May 19, 2026 FW-003 order or the July 17 hearing date. **Confirm this directly against the Sacramento Superior Court docket before relying on the app's calendar.**

---

## Part 2 — Confirmed correct (the good news)

- **Matter 5's demurrer hearing, tomorrow, July 15, 2026, 9:00 a.m., Dept. 10A** — independently confirmed across three separate filings (the demurrer notice, the litigant's opposition, and defendants' July 7 reply). All agree exactly.
- **Matter 15's responsive-pleading deadline, July 22, 2026** — confirmed exactly against the sheriff's proof of service (both CDCR and Keely Dodd personally served June 22, 2026; 30 days lands precisely on July 22). No extension or demurrer on file that would change this.
- **Matter 12's CMC (Aug. 12, 2026) and CMS-due (Jul. 28, 2026) dates** — confirmed against the court's own Notice of Case Assignment. The "not yet confirmed against a court-issued notice" caveat already in `timeline.js` is itself now stale — the confirming document is already in the case file.
- **Matter 20's entire deadline set** (CMC, demurrer hearing, opposition service) — fully confirmed accurate, correct `upcoming` flags, no issues.
- **Matter 24's federal scheduling order dates** (CMC Sept. 15, ADR/Rule 26(f) Aug. 25, initial disclosures Sept. 8) — all confirmed exact matches.

---

## Part 3 — Missing case-ending events (the most consequential gaps)

These aren't calendar-entry bugs — they're major docket developments with zero representation in the app at all.

**Matter 7 — a federal magistrate judge has recommended dismissing the entire case, and none of it is tracked.** Findings & Recommendations filed June 15, 2026 recommend the FAC be dismissed *without leave to amend* and the case closed (quasi-judicial immunity for Candelaria; Eleventh Amendment/standing issues for Gordon). The litigant timely filed Objections (~June 29 deadline, met). The case now awaits the District Judge's de novo ruling — completely invisible in `timeline.js`, which jumps straight from the April 27 FAC-filing entry to unrelated government-claim entries.

**Matter 9 — the case was dismissed six weeks ago, and there's nothing in the app about it.** The AG's demurrer to the writ petition was **sustained without leave to amend on May 29, 2026** (tentative ruling became final under the department's Local Rule 1.06(B) procedure — no oral argument was requested). This is presumptively the final order disposing of the entire case. It likely also starts a 60-day appellate clock from entry/service of judgment — a deadline that doesn't exist anywhere yet because no one is tracking whether judgment has been entered. **Check the Sacramento docket immediately.**

**Matter 10 — habeas petition denied without prejudice in April; the app still shows only the filing.** Denied April 27, 2026 for failure to exhaust administrative remedies. `timeline.js`'s only Matter 10 entry is the February filing — no resolution was ever added. (Separately: this order file is saved with a `.pdf` extension but is actually plain text — worth checking whether other files in the portfolio are similarly mislabeled, since a broken PDF could silently hide a real order from anyone just skimming file names.)

**Matter 19 — the only "upcoming" item in the whole matter is a stale, unresolved OSC date with no outcome document anywhere.** "OSC anticipated — June 5, 2026" is still flagged `upcoming: true`, five-plus weeks after the fact, and the folder contains no order, return, or ruling to show what actually happened. This is the exact failure mode this audit exists to catch. **Check the Santa Clara docket immediately.**

---

## Part 4 — Systemic bug: the live Deadline Clock is full of stale entries

Every single group found the same pattern independently — `upcoming: true` on events that have already happened, in some cases six-plus weeks ago. This isn't a handful of typos; it's a maintenance gap where entries never get flipped to `false` after the event passes.

**Affected entries (all confirmed accurate on their face — the only defect is the stale `upcoming` flag):**

| Matter(s) | Entry | How stale |
|---|---|---|
| 2 | Jun. 3 CM-110 deadline | ~6 weeks (also wrong date — see Part 5) |
| 2 | Jun. 18 U-Visa certification hearing | ~4 weeks |
| 2 | Jul. 6 CMC | 8 days |
| 8, 22 (+4) | May 29 "Complaints filed" | ~6 weeks |
| 4 | May 29 "Complaints filed"; Jun. 1 Gov. claim accrual | ~6 weeks each |
| 5 | Jun. 24 Supplemental Discovery Responses Deadline | ~3 weeks |
| 11, 13, 17, 18, 21 | Jun. 29 Voluntary Dismissal With Prejudice | 15 days |
| 12 | Jun. 15 Default Judgment request submitted | ~1 month |
| 14 | Jun. 1 Gov. claim accrual; Jun. 27 deemed rejected; Jun. 30 filing | 14–44 days |
| 15 | Jun. 7 deemed rejected; Jun. 11 Complaint filed | 5–6 weeks |
| 16 | Jul. 3 deemed rejected; Jul. 7 Complaint filed | 7–11 days |
| 19 | Jun. 5 OSC anticipated | 5+ weeks (also no outcome doc — see Part 3) |

**Recommendation: a one-time pass flipping every past-dated entry to `upcoming: false` would fix the majority of this audit's findings by itself**, independent of any content corrections below.

---

## Part 5 — Wrong dates and wrong statutory citations

- **Matter 2**: CM-110 deadline computed wrong — the Notice of CMC requires filing "at least 15 calendar days before" the July 6 CMC, which is **June 21**, not the June 3 currently listed.
- **Matter 2**: The April 14, 2026 entry claims the Alameda action was "STAYED in its entirety — all discovery and deadlines suspended," but a U-Visa certification motion was fully briefed and heard June 18, 2026, nearly two months later — the stay's actual scope appears narrower than described, and the "may be superseded by the stay" notes on the CM-110/CMC entries are likely incorrect assumptions.
- **Matter 7**: FAC filing date off by two days — `timeline.js` says April 27; the court's own Findings & Recommendations states April 29.
- **Matter 2**: Original service deadline off by one day (April 7 vs. the actual April 6 per the source document).
- **Matter 14 & 16 (recurring pattern)**: Both cite Gov. Code §945.6(a)(1) — the 6-month suit-filing deadline that applies only when *actual written notice* of claim rejection was given. Both claims were instead deemed rejected by the agency's silence after 45 days (Gov. Code §912.4(c)), which triggers the **2-year** period under §945.6(a)(2) instead — as the litigant's own Rojo complaint (page 5, ¶9) correctly states elsewhere. Not a missed-deadline risk (the true deadline is later, not earlier, and both suits were already filed before either date), but the entries misstate the legal basis and should be corrected or marked superseded.
- **Matter 14**: The "Jun. 1, 2026 Gov. claim accrual deadline" entry cites a Dec. 1, 2025 accrual date that doesn't match the Urrea complaint (which pleads Nov. 1–6, 2024) — appears to conflate Matter 4's facts with Matter 14's.
- **Matter 15**: A parallel §945.6(a)(1)-vs-(a)(2) question exists for the *first* government claim too (Nov. 5, 2026 entry) — worth confirming whether actual written rejection notice was ever served, since if not, the real deadline is roughly two years later than currently listed. This doesn't create urgency; if anything it removes some.
- **Matter 12**: The April 10, 2026 response-deadline entry is based on the *original* complaint, which was superseded by a First Amended Complaint (filed May 11, personally served May 12). The real, sworn-to deadline that actually triggered the default judgment request was **June 11, 2026** — a different date than what's currently shown.

---

## Part 6 — Statute-of-limitations exposure worth flagging (not calendar bugs)

- **Matter 14**: Government Claim was presented roughly 18 months after the pleaded Nov. 2024 accrual — well past the 6-month §911.2 presentation window. The complaint relies on a continuing-violation theory to bridge this; it's a real risk to be aware of, not a data-entry error.
- **Matter 5**: The FAC pleads specific misrepresentations dating to March 2021 and November 2022, against a complaint filed February 2026. The negligence, IIED, and Bane Act causes of action (2-year SOL under CCP §335.1) would presumptively bar conduct predating February 2024 absent a successful continuing-violation or delayed-discovery argument. The fraud cause of action (3-year discovery-rule SOL under CCP §338(d)) is on firmer footing. Defendants' pending demurrer (hearing tomorrow) does not currently raise this — worth the litigant's awareness regardless of how that hearing goes.

---

## Part 7 — Missing historical entries (informational, no live-clock risk)

- Matter 21's Jan. 22, 2026 federal complaint filing has no `timeline.js` entry at all — the shared "4 federal complaints" entry omits this fifth companion filing.
- Matter 12's First Amended Complaint (filed May 11, 2026, adding a new alter-ego defendant) and its service on Diamond (May 12, 2026) are both missing — these are the events that actually reset the response clock leading to the default judgment.
- Matter 24's federal magistrate-judge Consent/Declination deadline (~July 1, 2026) isn't tracked; already past, but worth confirming it was actually filed.
- Matter 9's First Amended Petition (filed Feb. 2, 2026) has no entry.
- Matter 15's CRC 3.724 ADR meet-and-confer obligation (due ~Nov. 9, 2026, printed directly on the court's Notice of Case Assignment) isn't tracked yet — low urgency given the lead time, but should be added now so it isn't missed later.

---

## Priority ranking

1. **Confirm the Matter 5 discovery deadlines** (own response due ~July 20; opposing response due ~July 17) — these are the only genuinely new, near-term, real obligations this audit surfaced that aren't already reflected anywhere.
2. **Verify Matter 8's July 17 fee-waiver hearing directly with the court** — the audit couldn't confirm it from the documents on file.
3. **Check the Sacramento and Santa Clara dockets for Matters 9, 10, and 19** — all three have case-ending or case-resolving events that happened weeks to months ago with zero record in the app.
4. **Run a bulk pass flipping stale `upcoming: true` entries to `false`** — this single fix addresses the majority of findings in this report.

---

*Report prepared: July 14, 2026*
*Methodology: five parallel deadline-extraction and cross-verification passes across the litigant's court documents (scheduling orders, notices of hearing, proofs of service, demurrers, complaints) in 18 of 24 matters with uploaded pleadings, diffed against every `src/data/timeline.js` entry tagged to those matters, with SOL/government-claims calculations checked against current California statutory deadlines.*
