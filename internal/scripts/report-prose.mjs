#!/usr/bin/env node
// Advisory word-count / docket-log report. Not a validate fail.
// Split matters: score prose.json when present (identity files are slim on purpose).
import fs from "node:fs";
import path from "node:path";
import { loadMatters } from "./load-matters.mjs";
import { docketLogIssues, proseBudgetIssues } from "./prose-budget.mjs";

const matters = loadMatters();
let findings = 0;

function withProse(matter) {
  if (matter.__layout !== "split" || !matter.__sourceDir) return matter;
  const prosePath = path.join(matter.__sourceDir, "prose.json");
  if (!fs.existsSync(prosePath)) return matter;
  return { ...matter, ...JSON.parse(fs.readFileSync(prosePath, "utf8")) };
}

for (const raw of matters) {
  const matter = withProse(raw);
  const tag = `Matter ${matter.number} (${matter.caption})`;
  for (const issue of proseBudgetIssues(matter)) {
    findings += 1;
    const kind = issue.level === "over-ceiling" ? "over ceiling" : "over target";
    console.log(`${tag}: ${issue.field} ${issue.words}w ${kind} (target ${issue.target}, ceiling ${issue.ceiling})`);
  }
  for (const issue of docketLogIssues(matter)) {
    findings += 1;
    console.log(
      `${tag}: ${issue.field} looks like a docket log (${issue.hits.join(", ")}; ${issue.words}w)`,
    );
  }
}

if (!findings) {
  console.log("No prose-budget or docket-log findings.");
} else {
  console.log(`\n${findings} finding(s). Advisory only — this is not a schema fail.`);
}
process.exit(0);
