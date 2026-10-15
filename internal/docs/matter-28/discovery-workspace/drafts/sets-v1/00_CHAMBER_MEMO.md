# CHAMBER MEMO: Matter 28 Discovery Sets v1 (INTERNAL, NOT FOR SERVICE)

Assumption: Dkt 15 is denied except as to fraud and RICO. Those theories are dropped. Compensation and incentive
requests are kept only for Monell motive and custom, and for punitive damages against Smith. Nothing has been served.
PDFs are in `pdf/`; signatures are blank. Re-render with `--stamp-signature --date "…"` only at service. The
generator is `internal/scripts/matter28-discovery-sets-v1.py` and the data lives in `matter28_sets_v1_data.py`.

**Counts.**
- HOPE ROGs: 21 numbered, counted conservatively as 22. No. 15 (Dwyer plus the regulation) may count as two. 3 reserved.
- Smith ROGs: 21, 4 reserved (No. 21, delegation, added Oct 14).
- RFAs: HOPE Set One 41 (Nos. 33-41 added Oct 14); HOPE Set Two 20 (HOLD); Smith Set One 17 (Nos. 16-17 added Oct 14); Smith Set Two 2 (HOLD).
- RFPs: HOPE 46 (Nos. 42-46 added Oct 14 as section K; RFP instructions 9-11 added); Smith 15.
- Subpart discipline follows Kendall, 174 F.R.D. at 685–86, as adopted in Safeco, 181 F.R.D. 441: one primary
  question each, with subsumed details only. There are no "and identify all documents" tails; RFPs carry that load.

## Claim map (request numbers)
| Claim / issue | HOPE ROG | HOPE RFA (Set 1 / Set 2 HOLD) | HOPE RFP | Smith ROG | Smith RFA (Set 1 / Set 2 HOLD) | Smith RFP |
|---|---|---|---|---|---|---|
| §1983 Monell / policy (HOPE) | 1-5,8,10,15-17 | 6,8-13,25-26,28-29 / - | 1-4,16-19,22-25,27-33,40-41,45 | 2-3,8-9,17 | 2,12 / - | 4-8,15 |
| Color of state law (both) | 2,4-7 | 1-5,7,9,22,27,29,35-36,38,40 / - | 1-2,7-9,14,17-21,25,39,41-43,46 | 6,11 | 8 / - | 3,13 |
| First Amendment retaliation | 11-13,18 | 17-20,23,33-34,41 / - | 1-2,5-6,11-12,14-15,26,32,41-42,44,46 | 5,7 | - / 2 | 1 |
| Due process | 1-3,8-10,15 | 2,5-6,11,14-16,27,33,35-40 / - | 1-5,7-10,19,29,40-43,46 | - | 5 / - | - |
| Smith individual / supervisory | 1,16-17 | 28 / - | 1-2,15-16,24,26,31,41,44-45 | 1-9,12,21 | 1-7,12-13,16-17 / 1-2 | 1-8,14 |
| Bane Act §52.1 | 12,14 | 18-19,21-22,41 / - | 1-2,5,12-14,41 | 13 | 7 / - | - |
| Preclusion / privity defense (Smith) | - | - / - | 1-2,41 | 10 | 9-11 / - | 12 |
| Insurance | 21 | - / - | 1-2,34-35,41 | 16 | - / - | 11 |
| ESI / preservation | 18-20 | 23-24 / - | 1-2,4,36-38,41 | 14-15 | 14-15 / - | 9-10 |
| Damages / punitive | - | 32 / - | 1-2,13,33,41 | 17-18 | 16 / - | 15 |
| Matter 5 contradictions | - | 30-32 / - | 1-2,41 | - | - / - | - |

HOPE RFA Set Two (HOLD) = authenticity and business-records foundation for HOPE_000001–542 (Nos. 1–3), plus admissions
built on HOPE_000294, 295, 334–335, 348–349, 189, 538–542, 143/197–199 and 159–161. Smith RFA Set Two (HOLD) = notice
via HOPE_000189.

## Serving order and timing
1. **Now (by about Oct 16–20):**
   - **HOPE RFP Set One.** No. 1 (re-production) is the protective-order fix. Nos. 5–6 (videos) and 4 (EHR audit
     trail) are the perishable items.
   - **HOPE RFA Set One.** It uses no San Joaquin production content.
   - Pair both with the preservation letter (`../PRESERVATION_AND_DEFICIENCY_LETTER.md`).
   - Responses come due about Nov 16–19. Discovery is open (26(f) was held 9/29) and the MTD does not stay it
     (*Gray*, 133 F.R.D. 39).
2. **After the Oct 27 ruling (about Oct 28–Nov 4):**
   - HOPE ROGs and all Smith sets. Smith's sets depend on her surviving the preclusion and privity argument.
   - Smith ROG 20 (affirmative defenses) only after an answer is filed.
   - Smith ROG 18 (net worth) could be held until a punitive-damages showing; it is a candidate for the reserve.
3. **After re-production or the PO paragraph:** HOPE RFA Set Two and Smith RFA Set Two (HOLD).
4. **Before service:**
   - Confirm that HOPE's San Joaquin SROG responses (cited in HOPE RFA 29–31) were verified and not designated
     Confidential.
   - ~~Verify the current text of 15 CCR §3574 (RFA 27).~~ Done Oct 14; RFA 27 and 30 corrected (PR #1003).
   - Confirm with Brendan that no LS/CMI score of 11+ was recorded after Apr 17, 2025 (RFA 40).
   - Confirm the signature-name question (caption name vs. AGENTS.md email signature).

## Anticipated objections and pre-drafted responses
| Objection | Response (verified authority) |
|---|---|
| Boilerplate "overbroad, burdensome, not relevant" | Objections must be specific and supported; boilerplate is improper. *A. Farber & Partners v. Garber*, 234 F.R.D. 186, 188 (C.D. Cal. 2006); Rule 34(b)(2)(B)–(C); Rule 33(b)(4) |
| Privilege asserted without a log | Boilerplate privilege assertions are insufficient; waiver turns on a holistic test with a 30-day default. *Burlington N. & Santa Fe Ry. v. U.S. Dist. Ct.*, 408 F.3d 1142, 1149 (9th Cir. 2005) |
| Cal. constitutional privacy / state-law privileges | Federal privilege law governs federal-question cases with pendent claims. *Agster*, 422 F.3d 836. Personnel-file privacy is balanced and handled by a PO. *Soto v. City of Concord*, 162 F.R.D. 603 (N.D. Cal. 1995) |
| Other clients' records / psychotherapist privilege | Requests are de-identified counts only (RFP 31–32; ROG 10), so no patient communications are sought (*Jaffee*, 518 U.S. 1). If PHI is still claimed, a qualified protective order under 45 C.F.R. §164.512(e)(1)(ii)(B) and (v) answers it |
| "Not in our possession" (Smith's personal phone; contractor-hosted policies and EHR) | "Control" means the legal right to obtain on demand, which includes HOPE's vendor contracts and work data on employees' devices. *In re Citric Acid Litig.*, 191 F.3d 1090, 1107 (9th Cir. 1999). RFP 38 (contractor agreement) tests this |
| Too many ROGs / discrete subparts | Each ROG asks one primary question; details are subsumed. *Kendall*, 174 F.R.D. at 685–86; *Safeco*, 181 F.R.D. 441. The count is kept at ≤22 for HOPE |
| Premature contention ROGs | Rule 33(a)(2) allows contention interrogatories; the court may defer them, not bar them. They are aimed at defenses already argued in Dkt 15/30 (color of law, individualized judgment, adequate process, privity) |
| Stay pending MTD | *Gray*, 133 F.R.D. 39 (N.D. Cal. 1990): a pending 12(b)(6) motion does not ordinarily justify a stay |
| Insurance / ROR not discoverable | The policies are mandatory under 26(a)(1)(A)(iv). For the ROR letter, relevance to coverage and settlement is argued from the facts; **no case cited (split, UNVERIFIED)** |
| Qualified immunity bars discovery (Smith) | Private actors generally can't claim qualified immunity. *Richardson v. McKnight*, 521 U.S. 399 (1997) (private prison guards). Citation verified; the holding is well known but was not re-read for this memo. Confirm the Ninth Circuit application before briefing |
| "Document speaks for itself" (RFA Set Two) | Not a proper Rule 36(a)(4) response; HOPE must admit, deny, or explain. (No case added; the rule text controls) |
| San Joaquin PO bars use (Set Two) | That's why it is on HOLD. Re-production under RFP 1 or the prior-production paragraph cures it (see `../PO_STRATEGY_AND_ADDENDUM.md`; *Foltz*, 331 F.3d 1122) |

Meet-and-confer prerequisite: Civil L.R. 37-1. Also check Judge Cisneros's discovery standing order (joint-letter
procedure; UNVERIFIED) before any motion.
