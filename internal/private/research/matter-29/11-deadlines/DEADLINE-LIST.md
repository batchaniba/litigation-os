# Matter 29 — Deadline list (research)

**Live truth is `internal/src/data/matters/29/clocks.json`.** This list is a working extract as of the 2026-10-28 snapshot plus the Oct. 28 letter. It is not a clock mutation. Confirm against the docket before relying on a date.

Actor tags follow the snapshot. Untagged or `you` = Plaintiff's side. `opposing` / `agency` = watch.

Types: **court** (Dkt. 9 or noticed hearing) · **statutory** · **computed** · **optional** · **internal**.

## Past in the snapshot (still marked open — do not ignore)

| Date | Clock id | Item | Status in snapshot | Note |
|---|---|---|---|---|
| 2026-09-30 | `29-deadline-6` | 28 U.S.C. § 1447(c) remand window (computed from removal) | `open` | Date has passed. Research: not recommending remand (FCRA on the face). Graph cleanup is a **separate** edit |
| 2026-10-14 | `29-crd-right-to-sue-watch` | WATCH — CRD / right-to-sue gap for Claim 2 | `open` | Not a hard missed filing; a coverage gap. Outer CRD limit 3 years from July 2026 acts as cited in the clock |

## Next (from Oct. 28)

| Date | Time PT | Clock / source | Item | Type | Actor |
|---|---|---|---|---|---|
| **Fri Nov 6** | 1:00–1:30 p.m. | `29-rule26f-meet-confer` | Rule 26(f) conference (Teams) with Brown, Frederick, Drury, Stanzick | court (scheduled conference) | you |
| **Tue Nov 10** | all day | `29-deadline-3` | ADR Certification (ADR L.R. 3) **and** 26(f) meet-and-confer deadline (Dkt. 9). Nov. 6 call, if held, satisfies the meet-and-confer | court | you |
| Wed Nov 11 | — | calendar | Veterans Day — court closed | record | — |
| **Fri Nov 13** | all day | `29-accurate-reinvestigation` | WATCH — Accurate § 1681i / § 1786.24 reinvestigation due 30 days from Oct. 14 dispute | statutory | opposing |
| Fri Nov 13 | all day | `29-zoom-request-mtd` | OPTIONAL last day to request Zoom for Nov. 18 MTD (3 business days; good cause). Default: **in person** | optional | you |
| **Wed Nov 18** | 1:30 p.m. | `29-hearing-mtd` | Hearing on Dkt. 19 (Claims 5–7), Courtroom 4, 3rd Floor, Oakland | court | you |
| **Tue Nov 24** | all day | `29-deadline-2` | Initial disclosures **and** Joint CMC Statement | court | you |
| Tue Nov 24 | all day | `29-cmc-inperson-request` | OPTIONAL request that Dec. 1 CMC be in person | optional | you |
| Thu–Fri Nov 26–27 | — | calendar | Thanksgiving — court closed | record | — |
| Sat Nov 28 | all day | `29-ccpa-amazon` | WATCH — Amazon CCPA request-to-know 45 days from Oct. 14 letter through counsel; receipt **UNVERIFIED**; Saturday | statutory | opposing |
| Mon Nov 30 | — | standing order as cited in 60-day calendar | If phone/Zoom participant invite needed for CMC: contact CRD Kim Means one business day before — **UNVERIFIED** in this room | optional | you |
| **Tue Dec 1** | 1:30 p.m. | `29-hearing-1` | Initial CMC, Zoom default (`cand.uscourts.gov/ask`) | court | agency |
| Sun Dec 7 | — | FRCP 34(b)(2)(A) **if** early RFPs deemed served Nov. 6 | Illustrative Rule 34 response date. **Not a stored clock.** Oct. 14 calendar used Dec. 10 because it assumed a Nov. 10 conference | computed | opposing |
| Jul 27, 2028 | — | `29-sol-fcra-icraa` | OUTER BOUND FCRA/ICRAA limitations (conservative, computed from Jul. 27, 2026 shift removal) | statutory computed | you |

## Oct. 28 letter vs. the Nov. 13 reinvestigation clock

Accurate's letter is dated **October 28, 2026** and states reinvestigation of the two disputed items is complete. That is **new evidence** that the § 1681i watch may be **satisfied as to those two items**. This research room does **not** edit `clocks.json`.

Still watch:

- Complete-file request (§ 1681g / § 1786.10) — not clearly produced.
- Procedure description — available on request, not enclosed as a narrative of what they did.
- Amazon receipt of the revised report — letter assertion only.

## Satisfied / contingent (snapshot)

| Date | Clock | Item | Status |
|---|---|---|---|
| 2026-09-22 | `29-deadline-4`, `29-deadline-5` | Responsive pleadings | satisfied |
| 2026-10-06 | `29-deadline-mtd-opposition` | Opposition to Dkt. 19 | satisfied (served Sep. 23) |
| 2026-10-13 | `29-deadline-mtd-reply` | Reply | satisfied |
| 2026-10-20 | `29-lr73d-objection` | 7-3(d) new-reply-evidence objection | contingent — **not needed** (reply had no declarations/exhibits) |

## Internal targets (not court deadlines)

From the Oct. 14 sixty-day calendar snapshot, still useful:

- Hash/freeze the Oct. 28 PDF — **done in this room** (`08-audit/SHA256SUMS`).
- Native .eml of Oct. 14 5:06 a.m. Amazon Jobs email.
- Certified Santa Clara docket C1761642.
- Damages ledger (lost wages, distress log, costs) — categories only until settlement-guard is run.
- Hearing binder for Nov. 18.
- Circulate JCMS draft ~Nov. 16–17.

## Other-matter collisions (from the Oct. 14 calendar snapshot — verify live)

The snapshot listed M33 CMC Nov. 12, M24 appearance email Nov. 16 / MTD Nov. 20, M28 items around Nov. 13. **UNVERIFIED** as of Oct. 28 against those matters' live clocks. Check `npm run next -- --days 30` before blocking the week of Nov. 10–20.
