# Crawl

`internal/src/data/index/matters.json` is the front door. Then fetch only the sibling you need from `internal/src/data/matters/NN/` (`matter.json`, `docket.json`, `clocks.json`, `events.jsonl`, …). Legacy `NN.json` stays canonical until split — split it when you touch that matter (`node internal/scripts/split-matter.mjs NN --replace`).

`events.jsonl` is append-only. Do not rewrite it. Do not move the log into `procedural_status`.

Never invent a docket number. If `dkt` is null, say so. `{filed: true, dkt: 18}` is on file; a draft is not.

PDFs live on the `documents` branch. This branch has `.txt` / `.meta.json` sidecars. A PDF without a sidecar is not searchable here.

Schema (shape, not a speed limit): `internal/src/data/index/schema.json`.
