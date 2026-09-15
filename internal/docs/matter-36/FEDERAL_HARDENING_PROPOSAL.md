# Matter 36 (AT&T) — E.D. Cal. federal-hardening proposal

Three pleading-craft additions to `internal/scripts/matter36-edca-complaint.py`
(the **federal** AT&T draft on PR #802, branch
`cursor/matter36-edca-federal-redraft-4b59`). Staged here on
`claude/home-depot-revamp-thoughts-qo89re` so #802's branch stays untouched.
These are the same Rule 12(b)(6) / Article III hardening moves applied to
Best Buy (Matter 39), adapted to AT&T's facts.

**No new factual allegations.** Every addition rests on facts already pleaded.

The San Joaquin state packet (`matter36-att-complaint.py`) is historical /
never clerk-filed — AT&T is federal now. This proposal does not touch it, and
the two edits briefly made to that state generator have been reverted.

Apply with:

```
git checkout cursor/matter36-edca-federal-redraft-4b59
git apply internal/docs/matter-36/matter36-edca-federal-hardening.patch
python3 internal/scripts/matter36-edca-complaint.py   # rebuilds the review draft; exits 0
```

The patch applies cleanly on the current #802 head (55 insertions, 6 deletions)
and the edited draft regenerates without error.

---

## 1. New ¶12A — Article III standing (*TransUnion v. Ramirez*)

The load-bearing federal add. After *TransUnion LLC v. Ramirez*, 594 U.S. 413
(2021), a bare § 1681b(b)(3)(A) procedural violation is not by itself concrete
injury. The JURISDICTION section (¶¶9–13) pleaded subject-matter jurisdiction
but never pleaded Article III standing. ¶12A ties concreteness to (a) the lost
accepted $24.95/hr Lodi position and (b) the deprivation of the pre-adverse
review-and-response opportunity that would have let Plaintiff flag the registry
use before the 12:23 p.m. rescission. Covers all counts, including the state
claims that still need Article III standing in federal court.

**Placement.** After ¶12 (venue), before ¶13; numbered 12A, inside every
"1 through 51" reallegation range.

## 2. New ¶70A — *Lerma* distinction + judicial-notice inoculation

The federal draft did not distinguish *Lerma* at all. Because *Lerma v. Amazon*
is a C.D. Cal. federal decision, AT&T will cite it directly and pair a 12(b)(6)
with a request for judicial notice of the public conviction records. ¶70A states
that the abstract availability of a court-record source does not establish AT&T
used one, that judicial notice of the records' existence proves neither source
nor contents of AT&T's unproduced First Advantage report, and that *Lerma*
turned on a report that was in the record — which this one is not.

**Placement.** Inside the Third Cause of Action (§ 290 count), after ¶70,
before ¶71; numbered 70A.

## 3. Sharpened ¶58 — *Safeco v. Burr* reckless-disregard willfulness

¶58 grounded FCRA willfulness only in AT&T's 10:19 a.m. First Advantage task.
Sharpened to the *Safeco Ins. Co. of America v. Burr*, 551 U.S. 47 (2007)
standard (willful = knowing **or reckless disregard**), adding AT&T's
sophistication/scale and the settled, unambiguous character of the
pre-adverse-notice duty — which unlocks § 1681n statutory + punitive damages.

**Placement.** Edits ¶58 in place; no renumbering.

---

## Authorities added (all real; verify in the citation funnel before filing)

- *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021)
- *Lerma v. Amazon.com Services, LLC*, No. 8:22-cv-01727 (C.D. Cal.)
- *Safeco Ins. Co. of America v. Burr*, 551 U.S. 47 (2007)

## Unchanged filing gates (per PR #802)

- § 290 Count Three is CCP § 338(a), timely from the May 28, 2026 use → May 28, 2029.
- Confirm AT&T Mobility Services LLC's current California SOS agent; do not serve the Lodi store.
- Plaintiff signature; no `/s/`.
