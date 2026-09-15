# Matter 39 (Best Buy) — E.D. Cal. federal-hardening proposal

Three pleading-craft additions to `internal/scripts/matter39-edca-complaint.py`,
proposed **for PR #799** but staged here on `claude/home-depot-revamp-thoughts-qo89re`
so the cursor branch stays untouched. They are the federal analogs of the Home
Depot (Matter 37) edits, translated from California demurrer law to the federal
Rule 12(b)(6) / Article III standard.

**No new factual allegations.** Every addition rests on facts already pleaded,
consistent with the filing-gate "hostile audit of every I&B allegation."

Apply with:

```
git checkout cursor/matter39-edca-federal-redraft-4b59
git apply internal/docs/matter-39/matter39-federal-hardening.patch
python3 internal/scripts/matter39-edca-complaint.py   # rebuilds the review draft; exits 0
```

The patch (`matter39-federal-hardening.patch`) applies cleanly on the current
#799 head (58 insertions, 8 deletions) and the draft regenerates without error.

---

## 1. New ¶9A — Article III standing (*TransUnion v. Ramirez*)

**Why.** This is the single biggest way the case gets dismissed at the pleading
stage. After *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021), a bare
§ 1681b(b)(3)(A) *procedural* violation is not by itself concrete injury — "no
concrete harm, no standing." As drafted, standing appears only as a stray phrase
at ¶39 and a passing mention at ¶81; the JURISDICTION section (¶¶7–10) pleads
subject-matter jurisdiction but never pleads Article III standing. The Ninth
Circuit (*Dutta v. State Farm*) wants the plaintiff to show the missing
information would have mattered — which ¶38 already supplies. ¶9A frames those
facts as injury-in-fact.

**Placement.** Inserted after ¶9 (diversity), before ¶10 (venue), inside
JURISDICTION AND VENUE. Numbered 9A so no other paragraph renumbers; it falls
inside every "1 through …" reallegation range automatically.

## 2. New ¶55A — *Lerma* distinction + judicial-notice inoculation

**Why.** The Home Depot #1 move, and it bites harder here because *Lerma v.
Amazon* is itself a C.D. Cal. federal decision — Best Buy will cite it directly
and pair a 12(b)(6) with a request for judicial notice of the public conviction
records to argue lawful court-record sourcing. ¶¶54–55 gesture at "that's a
merits defense" but never address judicial notice or *Lerma*. ¶55A states that
judicial notice of the existence of court records establishes neither the source
nor the contents of Best Buy's unproduced First Advantage report, that a 12(b)(6)
cannot resolve which source Best Buy used, and that *Lerma* turned on a report
that was in the record — which this one is not.

**Placement.** Inserted after ¶55, before the FIRST CAUSE OF ACTION header, at
the end of subhead G. Numbered 55A. Count Three's reallegation (¶72) is widened
from "48 through 55" to "48 through 55A" so the count incorporates it.

## 3. Sharpened ¶63 — *Safeco* reckless-disregard willfulness

**Why.** ¶63 grounded willfulness only in Best Buy naming First Advantage. Under
*Safeco Ins. Co. of America v. Burr*, 551 U.S. 47 (2007), "willful" under
§ 1681n reaches reckless disregard — an objectively unreasonable reading of the
statute. The sharpened paragraph adds Best Buy's sophistication/scale and the
settled, unambiguous character of the pre-adverse-notice duty, which is what
unlocks § 1681n statutory + punitive damages.

**Placement.** Edits ¶63 in place; no renumbering.

---

## Authorities added (all real; verify in the citation funnel before filing)

- *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021)
- *Lerma v. Amazon.com Services, LLC*, No. 8:22-cv-01727 (C.D. Cal.) — already
  relied on in the Matter 37 (Home Depot) complaint
- *Safeco Ins. Co. of America v. Burr*, 551 U.S. 47 (2007)

## Still outside this proposal (unchanged filing gates)

- Confirm the May 29, 2026 FCRA/ICRAA discovery date.
- File Count Three before **October 17, 2026** (CCP § 338(a), three years from
  the October 2023 use).
- Confirm Best Buy's current California SOS agent; do not serve 6653 Hopkins Road.
- Plaintiff signature; no `/s/`.
