# Repository Instructions

## Skip GitHub PR #666

Do not work on, review, comment on, update, rebase, merge, close, re-open, label, or push to **PR #666** (`https://github.com/newanforbi/interactive-litigation-portfolio/pull/666`). If assigned it or pointed at it, say it is skipped by standing instruction and stop. This skip is only #666.

## Stipulations — plaintiff-first, with discretion

When the work is actually a stipulation or defense agreement (extra time, a stay, a waiver, expanded relief, or his signature on their paper), read and follow [Stipulation Defense](internal/docs/STIPULATION_DEFENSE.md). Draft terms most favorable to Plaintiff. Maintain or shorten defense timelines when supported and advantageous; preserve Plaintiff's preparation time and favorable hearing dates. Require an explicit deadline comparison and concession audit. Identify concrete Plaintiff benefit for exceptions; do not silently grant defense time, waive rights, expand defense options, or authorize Plaintiff's signature.

Do not import that voice into ordinary Plaintiff papers (status reports, oppositions, complaints, hearing notes). Do not recite "this is not a stipulation" on those papers. Use discretion among actual stipulations: be firm on extra time, stays, waivers, and counsel's `/s/`; treat authenticity, a name correction he already wants, and a court-asked magistrate-settlement yes as ordinary.

Verify rules and sources before case-specific deadline conclusions. Proposed agreements do not automatically change operative calendar dates. Preserve existing court orders and executed agreements as historical facts.

For project structure and existing development workflows, consult README.md and internal/docs/SUPERCYCLE_INSTRUCTIONS.md.

## Email ending

Outgoing emails close with:

```
Brendan Ngwa Nforbi
Plaintiff, In Propria Persona
```

No phone, no email address, no "In Pro Per" on the close.

## Counsel dossiers

Opposing-counsel identity/role research lives under `internal/docs/counsel/`. Seeded: Kabat Chapman & Ozmer (Williams / Chapman) at [`internal/docs/counsel/kcoz/`](internal/docs/counsel/kcoz/). Append PACER pulls there. Those dockets are not related cases. Do not email counsel about the research.

## No GitHub to outsiders

Never put a GitHub, `raw.githubusercontent.com`, git-repo, or document-store
URL in anything Plaintiff will send or file. Attach the file. A download
link in the agent chat for him is fine. It does not go in the email.

## No CI — the gate is local

There is no GitHub Actions CI. The only workflows left are the CourtListener
ones (`courtlistener-sync`, `counsel-dossier`, `intel-fetch-briefs`); do not
add others. The checks the old CI job ran now run in the `pre-push` hook
(installed by `npm run prepare`): lint, typecheck, `validate-portfolio`,
golden damages math, the unit suite, and the fabricated-citation gate.
Before opening a PR, run `npm run validate` yourself and say so in the PR
body. Production deploys are scheduled, not per-push; see
`internal/docs/VERCEL_DEPLOYS.md`.

## Runtime boundary: Python vs Node

`internal/scripts/` contains two runtimes. Do not mix them.

**Node (.mjs)** — the build/validation/sync pipeline. These run in the git
hooks and `npm run` scripts:
- `validate-portfolio.mjs` — data validation (pre-push gate)
- `sync-*.mjs` — derived data generation (registry, manifest, summaries, upcoming, short-links)
- `load-matters.mjs`, `lib/matter-schema.mjs` — shared loaders and schemas
- `courtlistener/*.mjs` — docket sync

**Python (.py)** — one-off document generation and filling. These are
matter-specific utilities (e.g. `fill-matter-12-*.py`, `build-citation-index.py`)
run manually by Aliko. They are **not** part of the build, the hooks, or any npm script.

Rules:
- New automation that runs in the hooks or `npm run` must be Node (.mjs).
- Python scripts must not be added to `package.json` scripts or workflow steps.
- Shared logic (matter loading, validation) lives in Node; do not duplicate it in Python.
