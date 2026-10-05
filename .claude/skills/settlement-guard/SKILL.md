---
name: settlement-guard
description: >
  Run before drafting, revising, recommending, or sending any settlement
  number, demand, counter, withdrawal, response to an offer, "final" or
  expiring demand, Rule 68 decision, or term sheet, in any matter. Triggers
  on: demand, counter, offer, settle, settlement, "what should I ask",
  "should I lower", "they want more time", "final number", walk-away,
  global deal. Checks the move against the offer ledger and the hard rules
  in SETTLEMENT_REANCHOR_MEMO.md § 3 so Plaintiff does not negotiate
  against himself (Randstad, Matter 27). Not for stipulations about time
  alone: that is stipulation-defense.
---

# Settlement guard

Randstad (Matter 27) went $85,000 → $55,000 → withdrawn → $25,000 global without
one defense number, while higher drafts ($250,000, then $40,000) sat unsent. The
rules that would have stopped it were in a memo nobody was made to run. This
skill makes them a step you cannot skip.

## Every time

1. **Read the ledger:** `npm run negotiate:check -- --matter NN --history`.
   If the matter has no ledger, create `internal/private/negotiation/NN.jsonl`
   from the matter's `events.jsonl` (sent figures, unsent drafts, every defense
   response) before anything else. Format: `internal/private/negotiation/README.md`.
2. **Run the valuation** if the matter has `internal/private/negotiation/NN.valuation.json`:
   `npm run valuation -- --matter NN`. It shows what is proven (with pins), each
   damages line × Plaintiff's probability, the bracket the evidence supports, which
   defenses discount it, and which records may be cited in a letter, held in
   reserve, or never cited. Every figure you propose must trace to a line there.
   No valuation file yet: build one before proposing a number (FedEx, Matter 25,
   is the model).
3. **Read** `internal/docs/settlement/SETTLEMENT_REANCHOR_MEMO.md` § 3 (rules),
   § 4 (this track's bracket), § 4A (opening engine), § 9 (deal terms).
4. **Run the check on the exact move** before drafting the letter:

   ```bash
   npm run negotiate:check -- --matter NN --amount 60000 --scope global \
     --buys defense_number --event "what happened"   # add --gives-time / --trades / --withdraw as true
   ```

   Report the output to Plaintiff verbatim: CLEAR or BLOCKED, each rule, and
   the § 5 checklist.

## Using evidence in the letter

- Cite only what the valuation lists under "Cite in a letter". Quote it; do not
  characterize it (memo Rule 12).
- Items "in reserve" are for mediation or for answering a specific defense.
  Do not spend them in the opening.
- Never cite: the defense's own removal math or declarations (memo § 4A).
- Any item with a use restriction (protective order, sealed record) stays out
  until the restriction is cleared in writing.
- Never threaten criminal reporting, regulatory complaints, or publicity in
  exchange for money. For a party without a lawyer that can be extortion
  (Pen. Code §§ 518–519). Ask for money for the claims; nothing else.

## If it is BLOCKED

- **Do not draft the blocked figure.** Offer the compliant move instead:
  hold the figure, ask for their number, reprice on a named event, or send the
  higher unsent draft.
- "They asked for more time", "they're conferring", "the deadline is close",
  and "I need the money" are not counters or events. Say so plainly.
- Only Plaintiff can override, in his own words, for a stated reason. Then:
  `--override "his reason" --record`. The override is kept in the ledger and
  surfaces in the next debrief.

## After anything goes out or comes in

Record it the same day: Plaintiff's sends with `--record`; defense responses
(with or without a number), unsent drafts, and the walk-away by appending a
line to the ledger. A missing defense line makes the next check wrong.

## Never

- Put a ledger figure, walk-away, or this check's output in a letter, email,
  filing, or anything defense counsel sees.
- Cite one matter's settlement as a benchmark for another (memo § 2).
- Pair a lower figure with extra defense time.
