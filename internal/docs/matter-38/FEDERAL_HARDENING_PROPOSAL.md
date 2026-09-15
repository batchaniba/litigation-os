# Matter 38 (Swift) — E.D. Cal. federal-hardening proposal

Two pleading-craft additions to `internal/scripts/matter38-edca-complaint.py`
(the **federal** Swift draft on PR #803, branch
`cursor/matter38-swift-filing-redraft-4b59`). Staged here on
`claude/home-depot-revamp-thoughts-qo89re` so #803's branch stays untouched.

**No new factual allegations.** Every addition rests on facts already pleaded.

**Only two of the three sibling edits apply here.** Swift pleads **no FCRA
count** (the § 1681p clock closed), and jurisdiction is **diversity (§ 1332) +
§ 1367**, not federal question — so the *Safeco v. Burr* FCRA-willfulness edit
used in Matters 36/37/39 does **not** apply and is omitted.

Apply with:

```
git checkout cursor/matter38-swift-filing-redraft-4b59
git apply internal/docs/matter-38/matter38-edca-federal-hardening.patch
python3 internal/scripts/matter38-edca-complaint.py   # rebuilds the review draft; exits 0
```

The patch applies cleanly on the current #803 head (42 insertions) and the
edited draft regenerates without error.

---

## 1. New ¶12A — Article III standing (*TransUnion v. Ramirez*)

Even on diversity jurisdiction, a federal court requires Article III standing,
and after *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021), a bare statutory
violation is not by itself concrete injury. The most exposed count is the
**ICRAA § 1786.40 notice-omission (Count Two)** — a classic "procedural"
claim. ¶12A anchors concreteness to the denied Class A Driver opportunity
(tangible economic harm) and ties the § 1786.40 omission to a concrete
downstream deprivation (no timely chance to learn a report existed, inspect and
dispute it, and respond before the October 5, 2023 decision became final).

**Placement.** After ¶12 (supplemental jurisdiction), before ¶13; numbered 12A.

## 2. New ¶57A — *Lerma* distinction + judicial-notice inoculation (§ 290 count)

Kept deliberately honest to this record. The draft candidly concedes (¶¶2, 56)
that the furnished packet shows **no completed NSOPW hit and no "SOURCE OF
RECORD: CALIFORNIA SEX OFFENDER REGISTRY,"** and that the NSOPW component was
still "Processing." ¶57A does not overclaim a completed California-registry
source. Instead it holds the pleading-stage line: Swift's screening records are
in Swift's exclusive possession and not before the Court; judicial notice of
conviction records establishes neither the source nor the use; and *Lerma*
turned on a **produced completed** report, which this record does not contain —
so a *Lerma* analysis cannot be performed on the pleadings.

**Placement.** Inside the First Cause of Action (§ 290 count), after ¶57,
before ¶58.

---

## Candid caveat (not something these edits fix)

The § 290.46(j) count is the **weakest of the four screening matters** on the
merits, because the record concedes no completed California-registry hit and the
NSOPW component never finished. ¶57A improves the **pleading-stage** posture
(surviving a 12(b)(6) + judicial-notice attack), but the underlying **source /
use proof problem is real** and turns entirely on what discovery of Swift's
vendor adjudication logs shows. This is worth weighing before making the § 290
count load-bearing.

## Authorities added (verify in the citation funnel before filing)

- *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021)
- *Lerma v. Amazon.com Services, LLC*, No. 8:22-cv-01727 (C.D. Cal.)
