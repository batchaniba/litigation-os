# Portfolio API — Operation Catalog (B1)

The portfolio's agents currently operate by reading and hand-editing JSON
files. Every agent must therefore carry the full schema, the crawl order,
and every invariant in its working memory — and every one of them can
corrupt those invariants. PR #826 ("retire 3 duplicate/superseded timeline
events") was cleanup of exactly that failure class: duplicate `upcoming`
events and superseded clocks introduced by well-meaning direct edits.

The API boundary ends that. Agents stop touching files. They call typed
operations; the operations know the invariants. The file layout becomes an
implementation detail — which is what lets timeline sharding (#827), the
SQLite query layer, and future restructures happen without breaking a
single agent.

Principles:

1. **Reads first.** Read operations change no behavior and teach us the real
   query surface. They ship in Stage 1.
2. **JSON stays canonical.** The boundary reads and writes the same JSON
   source of truth. Derived stores (SQLite, fuse board, README tables) are
   built from it, never written through.
3. **Invariants live at the boundary, not in prompts.** If a rule can be
   checked by a machine, the operation checks it. Prompt folklore becomes
   code.
4. **Versioned.** Operations are versioned (`v1.*`). File layout changes
   must not change operation signatures.

## Stage 1 — CLI (`npm run q <op> [args]`)

Thin wrappers over the scripts that already exist. No new infrastructure.

## Stage 2 — MCP server

The same operations, new transport. Agents that speak MCP call the
portfolio directly instead of shelling out.

---

## Read operations

| Operation | Signature | Source today | Status |
|---|---|---|---|
| `getMatter` | `(n) -> identity + layout + files[]` | `load-matters.mjs` | wrap |
| `listMatters` | `({lifecycle?, phase?, cluster?}) -> index entries` | `index/matters.json` | wrap |
| `upcomingDeadlines` | `({days=14, matter?}) -> ranked clocks` | `check-deadlines.mjs`, `next-actions.mjs` | wrap |
| `getTimeline` | `({matter?, since?, upcomingOnly?}) -> events` | `timeline.json` / `events.jsonl` | wrap |
| `getFuseBoard` | `() -> Fuse/Wait/Parked` | `generate-fuse-board.mjs` | wrap |
| `fetchDocument` | `(sha256) -> pdf bytes (hash-verified)` | `fetch-doc.mjs` (PR #828) | wrap |
| `searchDocuments` | `(query) -> .txt sidecar hits` | `search-documents.py` | wrap |
| `getCounselDossier` | `(name) -> dossier` | `internal/docs/legal-intel/counsel/` | new |
| `getJudgeDossier` | `(name) -> dossier` | `internal/docs/legal-intel/judges/` | new |
| `getClusters` | `() -> cluster map` | `index/clusters.json` | wrap |
| `getMatterDocs` | `(n) -> manifest entries for matter` | `documents/manifest.json` | new |

Notes:

- `upcomingDeadlines` reads the **index `next_clock`** (which already folds
  `clocks.json` for split matters and the timeline for legacy ones) — never
  raw prose. This is the "clocks win" rule as an operation.
- `getTimeline` for a split matter reads `events.jsonl`; for legacy,
  `timeline.json` filtered by matter. Callers never branch on layout.
- `fetchDocument` re-hashes client-side and refuses mismatches; the key is
  `sha256/<first2>/<rest>.pdf`, deterministic from the manifest.

## Write operations

Writes are staged **after** reads, and only where agents have demonstrably
corrupted state. Each operation validates its invariants and refuses the
write with a machine-readable reason when they fail.

| Operation | Signature | Invariants enforced |
|---|---|---|
| `recordTimelineEvent` | `({date, type, actor, matters[], title, source?, upcoming}) -> event id` | date parses; `upcoming:true` requires `source`; no duplicate `(date, type, matters)` upcoming event exists (the #826 rule); `last_updated` bumped on touched matters |
| `retireUpcomingEvent` | `({eventId, reason}) -> ok` | flips `upcoming` true→false only; records `superseded_by` / `retired_reason`; never deletes |
| `setNextClock` | `({matter, clock}) -> ok` | split matters write `clocks.json`, never timeline prose; legacy write timeline; exactly one open clock per kind per matter |
| `updateMatterIdentity` | `({n, patch}) -> ok` | schema-validated; `matter.json` stays ≤80 lines / 8KB; `last_updated` = today |
| `catalogDocument` | `({matter, path, sha256, size}) -> ok` | manifest + registry updated together (the #762 lesson: one without the other fails CI); R2 key derived, never supplied |
| `scaffoldMatter` | `({n, caption}) -> paths` | wraps `scaffold-matter.mjs`; `n` unused; layout recorded in index |
| `splitMatter` | `({n}) -> paths` | wraps `split-matter.mjs`; refuses if already split |

`recordTimelineEvent` is first because timeline corruption is the observed
failure mode. `catalogDocument` is second (manifest/registry skew broke a
PR check before).

## Policy (not validation)

Some rules cannot be checked by a machine but must still bind every agent.
The boundary **surfaces** them — every write response includes the policy
reminder relevant to its operation, and agents acknowledge policy in their
output:

- Settlement framing is user-drawn and exact: Matter 27 communications are
  "final demands," AG-office communications are "offers." The boundary never
  generates settlement language on its own.
- Never sign anything on the user's behalf. No operation produces a
  signature, agreement, or "I agree."
- Review/merge separation: operations propose; only the user merges.

These live here (versioned, in the repo) instead of in any single agent's
prompt, so every present and future agent loads the same law.

## Adding an operation

1. Name the agent question it answers (from real usage, not speculation).
2. Specify signature, sources, and invariants in this catalog first.
3. Implement as a Stage 1 CLI op with the invariants as executable checks.
4. Promote to the MCP server unchanged.

No operation exists without its catalog entry. The catalog is the contract;
the code is the implementation.
