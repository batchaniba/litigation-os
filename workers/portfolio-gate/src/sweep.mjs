// Fail-closed backstop for lost runs. A Check Run left `in_progress` past the
// gate timeout means its runner died without reporting (eviction, deploy,
// container host move). Conclude it `failure` so the PR shows a real result
// instead of spinning forever; "Re-run" on the check starts a fresh attempt.

import { CHECK_NAME } from "./constants.mjs";

export async function sweepStaleChecks({ github, now = Date.now(), maxAgeMs }) {
  const swept = [];
  for (const pr of await github.listOpenPulls()) {
    if (pr?.base?.ref !== "main" || !pr?.head?.sha) continue;
    for (const run of await github.listCheckRuns(pr.head.sha)) {
      if (run.name !== CHECK_NAME) continue;
      if (run.status !== "queued" && run.status !== "in_progress") continue;
      const started = Date.parse(run.started_at || "");
      if (Number.isFinite(started) && now - started < maxAgeMs) continue;
      await github.completeCheckRun({
        id: run.id,
        conclusion: "failure",
        output: {
          title: `${CHECK_NAME} lost its runner`,
          summary:
            `No result within ${Math.round(maxAgeMs / 60000)} minutes of start on ` +
            `${pr.head.sha.slice(0, 12)}. The runner stopped without reporting. ` +
            "Re-run this check to try again.",
        },
      });
      swept.push({ pr: pr.number, checkRunId: run.id });
    }
  }
  return swept;
}
