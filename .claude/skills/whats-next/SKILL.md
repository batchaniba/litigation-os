---
name: whats-next
description: Answer "what's next on the list for me to do?" and every variation of it — "what's next", "what do I need to do", "what's on my plate", "what am I working on next", "what's due", "what's coming up", "anything overdue?", "where do I stand", "what should I file next", "what's my next deadline", "give me my to-do list", "next action", "what's on deck this week". Runs the portfolio's next-actions monitor over clocks.json and matters/summaries.json and reports the ranked queue: overdue items first, then this week, then the horizon. Use whenever the user asks what they should be doing next in this litigation portfolio, or asks about upcoming deadlines, hearings, or filings without naming a specific matter.
---

# What's next

The portfolio already knows what's due. Never answer this question from memory,
from the README, or by reading `clocks.json` by eye — the README tables and
`upcoming.json` are generated snapshots, and reading dates by hand is how a
deadline gets missed. Run the monitor.

## Run it

```bash
npm run next                  # default: 30-day horizon
npm run next -- --days 7      # just this week
npm run next -- --all         # everything still flagged upcoming
npm run next -- --mine        # drop opposing-party and court/agency clocks
npm run next -- --matter 20   # one matter
npm run next -- --json        # machine-readable, same ranking
```

Pick the horizon from how the question was asked:

| They asked | Run |
|---|---|
| "what's next", "what do I do next" | `npm run next` |
| "this week", "next few days" | `npm run next -- --days 7` |
| "everything", "full list", "rest of the year" | `npm run next -- --all` |
| "what's next on Matter 20" | `npm run next -- --matter 20` |

## How the queue is ranked

1. **PAST DUE** — dated before today but still live in `clocks.json`.
   Either the obligation was missed or the clock was never satisfied/vacated
   after it was done. Both are worth saying out loud.
2. **Next 3 days**, **This week**, then the rest of the horizon.
3. Inside each band, the user's own obligations come before clocks that run
   against someone else.

Every row carries an actor tag. Untagged rows are the user's to do. Rows marked
`[opposing party's clock]` or `[court/agency clock]` are dates to *watch*, not
tasks to work — an AG reply deadline is not a task on this desk. Those tags are
inferred from the event text unless the timeline entry pins an `actor` field, so
the output labels them `inferred — verify`. Repeat that caveat when it matters.

Two sections sit below the bands:

- **Not on one calendar day** — entries dated by month or by range, which can't
  be counted down to. Mention them if the horizon is wide.
- **Active matters with no dated next step** — active or pre-filing matters with
  nothing scheduled at all. This is the coverage gap, and it is usually the most
  useful part of the answer: those matters are drifting.

## How to answer

Lead with the single most urgent thing, then give the short list. Concretely:

- Open with anything past due, named, with how many days it has been sitting.
- Then 3–6 items, each as: date, days out, matter number and caption, and what
  the day actually demands (file / appear / meet & confer / serve).
- Close with the no-next-step matters if there are any.
- Keep it to what the data says. Do not invent a deadline, do not compute a new
  one, and do not upgrade an inferred actor tag into a certainty.
- End with the standing caveat: these are the dates as recorded in the
  portfolio; confirm against the docket before relying on one.

If the user then asks about one item, drill in with `--matter N` and read the
matter's own record at `internal/src/data/matters/NN.json` for context.

## When something looks wrong

If a past-due item is actually complete, the fix is in the data, not the script:
drop `"upcoming": true` from that entry in `internal/src/data/timeline.json`, then
run `npm run sync:upcoming && npm run generate:readme` so the SPA bundle and the
README table follow. Offer that when a past-due row is stale. The monitor also
skips upcoming flags that only touch archived/closed matters (and prints a count
of those skips) — clear those flags too so validate-portfolio stays green.

To pin an actor instead of relying on inference, add `"actor": "you" | "opposing"
| "agency"` to the timeline entry. The script prefers the explicit value and
drops the "inferred" caveat.
