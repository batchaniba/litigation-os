// Family 3 extraction: single loader for the docket-interpretation rule
// file. The interpretation scripts under this directory (and
// split-matter.mjs) are dumb renderers over these rules — the strategy
// (patterns, thresholds, weights, confidences) lives in
// internal/src/data/rules/docket-interpretation.json and is compiled here.
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const RULES_PATH = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../src/data/rules/docket-interpretation.json",
);

export function compilePattern(pattern, flags) {
  return new RegExp(pattern, flags || "");
}

// Compile a rule list into first-match-wins rules with compiled regexes.
// Rules carry: pattern (string|null), flags, input ("raw"|"lowercase"),
// optional notPattern/notFlags, and optional gating keys (whenFiled, whenDkt).
function compileRules(list) {
  return list.map((rule) => ({
    ...rule,
    re: rule.pattern == null ? null : compilePattern(rule.pattern, rule.flags),
    notRe:
      rule.notPattern == null
        ? null
        : compilePattern(rule.notPattern, rule.notFlags),
  }));
}

// First-match-wins over a compiled rule list. A rule with re == null is the
// default and always matches (subject to its gating keys). Returns the rule
// or null.
export function matchFirstRule(rules, value, extra = {}) {
  for (const rule of rules) {
    if (rule.whenFiled !== undefined && rule.whenFiled !== extra.filed) continue;
    if (rule.whenDkt !== undefined && rule.whenDkt !== extra.dkt) continue;
    if (rule.re == null) return rule;
    const text =
      rule.input === "lowercase"
        ? String(value ?? "").toLowerCase()
        : String(value ?? "");
    if (!rule.re.test(text)) continue;
    if (rule.notRe != null && rule.notRe.test(text)) continue;
    return rule;
  }
  return null;
}

let cache = null;

export function loadDocketRules() {
  if (!cache) {
    const raw = JSON.parse(readFileSync(RULES_PATH, "utf8"));
    cache = {
      ...raw,
      factTypeRules: compileRules(raw.factTypeRules),
      factActorRules: compileRules(raw.factActorRules),
      filerRules: compileRules(raw.filerRules),
      docTypeRules: compileRules(raw.docTypeRules),
      packetRules: compileRules(raw.packetRules),
      deadlineCandidates: {
        explicitDate: {
          ...raw.deadlineCandidates.explicitDate,
          re: compilePattern(
            raw.deadlineCandidates.explicitDate.pattern,
            raw.deadlineCandidates.explicitDate.flags,
          ),
        },
        withinDays: {
          ...raw.deadlineCandidates.withinDays,
          re: compilePattern(
            raw.deadlineCandidates.withinDays.pattern,
            raw.deadlineCandidates.withinDays.flags,
          ),
          requiredAny: raw.deadlineCandidates.withinDays.requiredAny.map((p) =>
            compilePattern(p, raw.deadlineCandidates.withinDays.requiredAnyFlags),
          ),
        },
      },
    };
  }
  return cache;
}
