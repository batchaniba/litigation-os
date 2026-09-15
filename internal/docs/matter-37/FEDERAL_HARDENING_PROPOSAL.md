# Matter 37 (Home Depot) — E.D. Cal. federal-hardening proposal

Three pleading-craft additions to `internal/scripts/matter37-edca-complaint.py`
(the **federal** Home Depot draft on PR #795, branch
`matter37-edca-federal-redraft-v2`). Staged here on
`claude/home-depot-revamp-thoughts-qo89re` so #795's branch stays untouched —
other agents are working that branch.

**No new factual allegations.** Every addition rests on facts already pleaded.
Home Depot has **no wage rate in the record**, so the standing paragraph pleads
lost compensation "according to proof" and invents no hourly figure.

The San Joaquin state generator (`matter37-home-depot-complaint.py`) is LOCKED
historical work product. AT&T/Home Depot are federal now; the earlier edits to
that state generator have been reverted.

Apply with:

```
git checkout matter37-edca-federal-redraft-v2
git apply internal/docs/matter-37/matter37-edca-federal-hardening.patch
python3 internal/scripts/matter37-edca-complaint.py   # rebuilds the review draft; exits 0
```

The patch applies cleanly on the current #795 head (50 insertions, 1 deletion)
and the edited draft regenerates without error.

---

## 1. New ¶10A — Article III standing (*TransUnion v. Ramirez*)

The federal draft pleaded subject-matter jurisdiction (¶¶8–12) but had no
dedicated Article III standing paragraph (only a passing "Article III" mention
in the §290 preventive-relief reservation). After *TransUnion LLC v. Ramirez*,
594 U.S. 413 (2021), a bare §1681b(b)(3)(A) procedural violation is not by
itself concrete injury. ¶10A ties concreteness to the lost accepted Tracy job
(compensation according to proof — no invented rate) and the deprivation of the
pre-adverse review-and-response opportunity. Covers all three counts.

**Placement.** After ¶10 (diversity), before ¶11 (venue); numbered 10A.

## 2. New ¶78A — *Lerma* distinction + judicial-notice inoculation

The federal draft did not distinguish *Lerma* at all. Because *Lerma v. Amazon*
is a C.D. Cal. federal decision, Home Depot will cite it directly and pair a
12(b)(6) with a request for judicial notice of the public conviction records.
¶78A closes it.

**Placement.** Inside the Third Cause of Action (§290 count), after ¶78,
before ¶79.

## 3. Sharpened ¶63 — *Safeco v. Burr* reckless-disregard willfulness

¶63 was already strong (Home Depot's own Ford-form pre-adverse language +
*Harris v. Home Depot*). Adding the *Safeco Ins. Co. of America v. Burr*, 551
U.S. 47 (2007) reckless-disregard standard firms up the §1681n statutory +
punitive hook.

**Placement.** Edits ¶63 in place; no renumbering.

---

## Authorities added (all real; verify in the citation funnel before filing)

- *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021)
- *Lerma v. Amazon.com Services, LLC*, No. 8:22-cv-01727 (C.D. Cal.)
- *Safeco Ins. Co. of America v. Burr*, 551 U.S. 47 (2007)

*Harris v. Home Depot U.S.A., Inc.*, 114 F. Supp. 3d 868 (N.D. Cal. 2015), is
already cited in ¶63 on the branch and is untouched.
