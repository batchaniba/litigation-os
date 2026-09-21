---
doc_kind: derived
retired: true
source: internal/src/data/matters/*/clocks.json
as_of: 2026-09-21
---

# Deadline audit — retired

This file is not the live calendar.

The July 2026 prose sweep described a smaller portfolio against `src/data/timeline.js`, which is no longer the clock store. Do not reconstruct deadlines, SOLs, or "act now" items from that snapshot or from any other `internal/docs/` table.

**Source of truth:** each matter's `internal/src/data/matters/NN/clocks.json`, plus `internal/src/data/index/matters.json` `next_clock`. Clock `status` is `open | set | contingent | vacated | satisfied`. `overdue` is derived at read time. Query with `npm run q upcomingDeadlines` or `npm run next`.

The old sweep remains in git history. `deadline_audit.json` is a companion fossil; do not treat it as current either.
