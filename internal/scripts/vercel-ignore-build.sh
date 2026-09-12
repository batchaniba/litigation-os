#!/usr/bin/env bash
# ==========================================================
# Vercel "Ignored Build Step".
#
# Dashboard: Project -> Settings -> Git -> Ignored Build Step -> Custom:
#   bash internal/scripts/vercel-ignore-build.sh
#
# Vercel's convention is inverted from Unix: exit 0 = SKIP the build,
# exit 1 = BUILD. It runs in the build container after the shallow
# (--depth=10) clone and before `npm ci`, so a skip costs seconds.
#
# Decisions, in order:
#   1. Not `main`            -> skip. PR branches get no preview builds.
#   2. No previous deploy    -> build (first run after enabling, or after
#                               the project is reconnected).
#   3. Nothing under a path that feeds `vite build` changed since the
#      last successful production deploy -> skip. Intel memos, counsel
#      dossiers, Python generators, workflows, and agent rules do not
#      change a byte of dist/.
#
# If the previous SHA is outside the shallow clone, `git diff` exits 128
# and we build. That is the safe direction: an extra build, never a
# missed one. `git fetch --deepen` below is best-effort to widen the
# window; failure is ignored.
#
# Deploy-hook builds (see internal/workers/vercel-deploy-cron/) arrive
# with VERCEL_GIT_COMMIT_REF=main and the same PREVIOUS_SHA, so rule 3
# also skips a scheduled deploy when main has not moved in a way that
# matters. Requires "Automatically expose System Environment Variables".
#
# Test locally against any two commits:
#   VERCEL_GIT_COMMIT_REF=main VERCEL_GIT_PREVIOUS_SHA=HEAD~3 \
#     bash internal/scripts/vercel-ignore-build.sh; echo "exit=$?"
# ==========================================================
set -u

PRODUCTION_BRANCH="${VERCEL_PRODUCTION_BRANCH:-main}"

# Everything `npm run build` reads. Keep in step with vite.config.js,
# the prebuild `sync:derived` scripts, and their imports under lib/.
BUILD_INPUTS=(
  internal/src
  internal/public
  internal/scripts/lib
  internal/scripts/load-matters.mjs
  internal/scripts/sync-matter-summaries.mjs
  internal/scripts/sync-upcoming.mjs
  internal/scripts/sync-short-links.mjs
  internal/scripts/vercel-ignore-build.sh
  index.html
  vite.config.js
  tsconfig.json
  package.json
  package-lock.json
  vercel.json
)

ref="${VERCEL_GIT_COMMIT_REF:-}"
prev="${VERCEL_GIT_PREVIOUS_SHA:-}"
echo "vercel-ignore-build: ref=${ref:-<unset>} previous=${prev:-<none>} head=$(git rev-parse --short HEAD 2>/dev/null || echo '?')"

if [ "$ref" != "$PRODUCTION_BRANCH" ]; then
  echo "vercel-ignore-build: not ${PRODUCTION_BRANCH} — skip"
  exit 0
fi

if [ -z "$prev" ]; then
  echo "vercel-ignore-build: no previous production deploy recorded — build"
  exit 1
fi

if ! git cat-file -e "${prev}^{commit}" 2>/dev/null; then
  git fetch --quiet --deepen=200 origin "$PRODUCTION_BRANCH" 2>/dev/null || true
fi

git diff --quiet "$prev" HEAD -- "${BUILD_INPUTS[@]}" 2>/dev/null
rc=$?
case "$rc" in
  0)
    echo "vercel-ignore-build: no build-input changes since ${prev} — skip"
    exit 0
    ;;
  1)
    echo "vercel-ignore-build: build inputs changed since ${prev} — build"
    ;;
  *)
    echo "vercel-ignore-build: cannot diff against ${prev} (git exit ${rc}) — build"
    ;;
esac
exit 1
