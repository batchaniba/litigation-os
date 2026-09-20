#!/bin/bash
# Clone the PR head SHA and run the same bar as `.githooks/pre-push`.
# Prefer `npm run gate` (PR #904). If that script is absent on an older
# head, fall back to the documented six-step suite.
#
# Env (set by server.mjs; never log GITHUB_TOKEN):
#   GATE_SHA, GATE_CLONE_URL, GITHUB_TOKEN, WORKDIR
set -euo pipefail

SHA="${GATE_SHA:?GATE_SHA required}"
CLONE_URL="${GATE_CLONE_URL:?GATE_CLONE_URL required}"
WORKDIR="${WORKDIR:-/tmp/portfolio-gate/${SHA}}"

export PORTFOLIO_SKIP_DISK_DOCS=1
export VITE_COPY_DOCUMENTS=0
unset SKIP_PORTFOLIO_GATE || true

echo "portfolio-gate: fetching ${SHA}"

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  git_url="$(GATE_CLONE_URL="$CLONE_URL" python3 -c '
import os, urllib.parse
u = urllib.parse.urlsplit(os.environ["GATE_CLONE_URL"])
token = urllib.parse.quote(os.environ["GITHUB_TOKEN"], safe="")
host = u.hostname or ""
if u.port:
    host = f"{host}:{u.port}"
print(urllib.parse.urlunsplit((u.scheme, f"x-access-token:{token}@{host}", u.path, u.query, u.fragment)))
')"
else
  git_url="$CLONE_URL"
fi

git init -q
git remote add origin "$git_url"
# Depth-1 fetch of the exact commit. GitHub accepts a SHA as a ref here.
git fetch --depth 1 --no-tags origin "$SHA"
git -c advice.detachedHead=false checkout --detach FETCH_HEAD

echo "portfolio-gate: npm ci"
npm ci --no-audit --no-fund

if python3 -c 'import json; p=json.load(open("package.json")); raise SystemExit(0 if p.get("scripts", {}).get("gate") else 1)'; then
  echo "portfolio-gate: npm run gate"
  npm run gate
else
  echo "portfolio-gate: npm run gate missing — six-step fallback"
  npm run -s lint
  npm run -s typecheck
  node internal/scripts/validate-portfolio.mjs
  node internal/scripts/test-golden.mjs
  npx vitest run --reporter=dot
  python3 internal/scripts/verify-citations.py --check
fi

echo "portfolio-gate: gate passed"
