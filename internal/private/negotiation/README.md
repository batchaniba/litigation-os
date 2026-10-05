# Negotiation ledgers (private)

One file per matter, `NN.jsonl`, one move per line, oldest first. Every
settlement figure, withdrawal, unsent draft, defense response, and Plaintiff's
private walk-away goes here, so `npm run negotiate:check` can test the next
move against the hard rules in
[`internal/docs/settlement/SETTLEMENT_REANCHOR_MEMO.md`](../../docs/settlement/SETTLEMENT_REANCHOR_MEMO.md) § 3.

**Private.** Like everything under `internal/private/`, these files never go
into the public SPA, the Worker/D1 store, a filing, a demand letter, or an
email to counsel. Walk-aways are reservation points, never disclosed.

## Line format

```json
{"date":"2026-09-12","side":"plaintiff","kind":"demand","amount":25000,"scope":"global","note":"..."}
```

| Field | Values |
|---|---|
| `side` | `plaintiff` or `defense` |
| `kind` (plaintiff) | `demand` (sent), `draft` (prepared, not sent), `withdraw`, `walkaway` (private), `override` (sent despite a block, with the reason), `term`, `note` |
| `kind` (defense) | `counter`, `offer`, `accept` (these carry a **number**); `request_time`, `conferring`, `reject` (these do **not**: they are never counters); `term`, `note` |
| `scope` | `global`, or a defendant slug such as `randstad`, `rk`. Figures are compared within a scope; a global figure is also compared against single-defendant figures. |
| `buys` | what a lower figure bought: `defense_number`, `document`, `held_clock`, `narrower_release`, `prompt_payment`, `non_cash_relief` |
| `event` | the ruling, report, admission, discovery result, coverage fact, or trial date behind a reprice |

Record **drafts that were not sent** too: a higher unsent draft is exactly
what Rule 6 checks for.

## Valuation files (`NN.valuation.json`)

The proof map behind the numbers: each key record with its pin and a verbatim
quote, which claim element it proves, which defense it answers, whether the
defense has seen it, whether it is held in reserve or must never be cited, and
each damages line with the evidence behind it and Plaintiff's probability of
proving it. `npm run valuation -- --matter NN` prints the sheet. Reprice by
editing the probabilities or evidence status when an event lands, then rerun.
FedEx (`25.valuation.json`) is the model.

## Use

```bash
npm run negotiate:check -- --matter 27 --history
npm run negotiate:check -- --matter 25 --amount 195000 --scope global
npm run negotiate:check -- --matter 25 --amount 150000 --buys defense_number --event "FedEx countered $60,000 on Oct. 9"
npm run negotiate:check -- --matter 25 --amount 150000 ... --record          # after Plaintiff sends it
npm run negotiate:check -- --matter 25 --amount 90000 --override "why" --record   # deliberate exception, kept on record
```

Exit 1 means at least one hard rule is broken; each is named with the reason.
Add a walk-away line (`"kind":"walkaway"`) before the first number in a matter.
