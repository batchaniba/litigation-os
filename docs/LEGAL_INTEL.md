# Legal Intelligence

CourtListener-powered intelligence for the portfolio, beyond docket syncing.

## Opposing counsel dossiers (v1)

`npm run intel:counsel` builds a profile of opposing counsel:

    npm run intel:counsel -- --matter 28              # auto-discover from bound docket parties
    npm run intel:counsel -- --matter 28 --link       # also record on the matter
    npm run intel:counsel -- --name "Jane Smith" --matter 28
    npm run intel:counsel -- --attorney-id 12345 --matter 28
    npm run intel:counsel -- --name "Jane Smith" --firm "Big Law LLP"

What a dossier contains:

- **Identity** - name, CourtListener attorney ID when resolvable, firm.
- **Docket history** - RECAP search across their cases: volume, courts, date
  range, and a 25-case sample. Capped at ~60 most recent dockets.
- **Motion patterns against you** - their filings in *your* matters, classified
  from locally synced docket entries (motion to dismiss, summary judgment,
  discovery, settlement signals, voluntary dismissals). Zero API cost.

Output: `internal/docs/legal-intel/counsel/<slug>.json` (data) and
`<slug>.md` (readable summary). A run costs fewer than 10 API calls;
run on demand, not on a schedule.

Counsel discovery matches docket parties against the matter's `defendants`
field. It auto-resolves only on a unique best match (>= 2 token hits,
score >= 0.5); otherwise it prints ranked candidates and asks for
`--attorney-id` or `--name`. Use `--link` to persist
`opposing_counsel: [{ name, attorney_id, firm, dossier }]` on the matter
record (validated by the matter schema).

Caveats, stated in every dossier:

- Name-based RECAP search can conflate common names; pin `--attorney-id`
  when ambiguous.
- History is a sample, not an exhaustive record.
- Settlement/dismissal mentions are directional signals, not adjudicated outcomes.

## Roadmap

- **Ninth Circuit precedent radar** - weekly `court:ca9` published-opinion scan
  filtered by per-matter issue keywords; hits ranked by engagement with the
  brief bank's authorities.
- **Supporting authority engine** - `cites:` searches over the citation index
  for newer cases applying the same rules, plus gap analysis on thin issues.
- **Draft pleading citation gate** - eyecite extraction + CourtListener
  citation-lookup + name matching before a pleading is finalized.
- **Quote verification** - fuzzy-match block quotes against opinion text.
- **Playbook extraction** - RECAP brief downloads to surface the authorities
  opposing counsel actually leans on.

