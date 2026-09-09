---
name: stipulation-defense
description: Review, redline, or draft any stipulation, continuance, extension, tolling agreement, or proposed order so it favors Plaintiff — especially on timelines. Use whenever opposing counsel sends a stipulation or proposed order, asks for an extension or continuance, asks to move a hearing/CMC/deadline, asks for e-signature authority, or when the user is drafting one. Also use before signing anything captioned "Stipulation," "Joint," or "[Proposed] Order." Portfolio-wide default, not matter-specific.
---

# Stipulation defense

Plaintiff's standing posture on every stipulation in this portfolio.

**The rule: time runs against Plaintiff.** Evidence degrades, custodians leave, retention windows close, damages accrue without remedy, and delay favors whoever holds the documents — which is almost always the defense. Never agree to a continuance reflexively, never extend more than asked, and never let a stipulation drift longer in Plaintiff's hands than it arrived.

## Non-negotiables

1. **Offer to draft.** Whoever drafts sets the defaults. If the defense drafts, their draft is an opening offer, not a form.
2. **Continue the event, not the deadlines.** Moving a conference must not silently move disclosures, ADR certification, Rule 26(f), or expert dates. Enumerate what moves and what expressly does not.
3. **Dates certain only.** Never "reset to run from the continued conference date" or any floating anchor. Put a calendar date on every obligation.
4. **Never broaden what they asked for.** If the defense asks to move one date, move one date. Adding relief they did not request is a gift.
5. **Price every extension.** A continuance the defense wants is currency. Charge for it.
6. **Never grant blanket e-signature authority.** Authorize one identified final version you have read, in writing, per document.
7. **Reserve rights expressly.** Silence gets read as agreement later.

Model language for every rule below is in `CLAUSES.md` in this directory. Use it verbatim where it fits.

## Before signing — run this

- [ ] What is the stated reason? Is it still true on the day you sign?
- [ ] What deadlines chain off the event being moved? Check the scheduling order and local rules, not just the stipulation.
- [ ] Does any date approach something unrecoverable — Rule 4(m) service, limitations, appeal window, amendment as of right? Stop if so.
- [ ] Does this stipulation touch discovery? Say expressly that it is not a stay.
- [ ] Does it affect a pending motion, its briefing, or its hearing?
- [ ] **Parallel proceedings:** is the same claim or primary right pending elsewhere? Slowing the federal case raises preclusion exposure if the state case reaches judgment first. Check both calendars before agreeing.
- [ ] Is the benefit reciprocal, or one-way?
- [ ] Read the **[Proposed] Order** separately. The order binds; the stipulation only recites.
- [ ] Does the caption, case number, and party description match this action?

## What to trade for

Never give a continuance for free. Ask for one of these in exchange:

- A date certain for the defense's Rule 26(a)(1) disclosures
- Production of a named category of documents by a date
- Agreement to accept service on an unserved defendant
- Stipulation to authenticity of the agency's own records
- "No further extensions absent order of the Court"
- A matching extension on one of Plaintiff's own obligations
- Agreement that the continuance does not stay discovery

## Red flags

| Language | Problem |
|---|---|
| "and all related deadlines shall be reset accordingly" | Floating anchor; sweeps in dates nobody discussed |
| "the parties agree to meet and confer regarding a schedule after…" | Produces no schedule and no clock |
| "following discovery" | Puts an obligation behind a gate that may never open |
| "you can give me authority to sign with your electronic signature" | Blanket authority; sign it yourself or authorize one named file |
| "premature" / "at this time" | Defense reserving delay without a date |
| No end date on a stay or extension | Open-ended |

## Case study — Serrato Dkt. 22 (Sept. 3, 2026)

DAG Li drafted a stipulation to continue the initial CMC. Plaintiff signed it **and added** a second request item vacating the September 8 deadlines for Rule 26(a)(1) disclosures, the Joint CMC Statement, and ADR certification, resetting them to run from the continued conference date.

The edit was tidy drafting and substantively backwards: **Plaintiff asked for more delay than the defendant did**, on a floating anchor, and got nothing in return. When Plaintiff later wanted to keep the September 15 date, he had no standing to object to his own expanded stipulation.

What should have happened: continue the conference only; hold the September 8 dates or move them to a date certain; and charge for it — a date certain for Defendant's disclosures, or agreement that the continuance does not defer discovery.

## Signature and filing hygiene

- Sign the document yourself; do not delegate the signature block.
- When opposing counsel files, authorize **one named file** in writing: *"You are authorized to file [exact filename] with my electronic signature."*
- Require the Civil L.R. 5-1(i)(3) attestation from the filer.
- **Diff the filed version against what you signed.** Ask for the conformed copy and compare.
- Nothing is filed until it is clerk-stamped. Do not treat a mailed or emailed document as on the docket.

## Log it

Record every stipulation in `internal/src/data/timeline.json` with: who drafted, what moved, what was expressly preserved, what was obtained in exchange, and whether the proposed order was signed. An unsigned proposed order is not an order — the old dates stay live.
