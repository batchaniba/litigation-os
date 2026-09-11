import type { ArgumentDiff, ArgumentSnapshot } from "./types";

export function diffArguments(prior: ArgumentSnapshot, current: ArgumentSnapshot): ArgumentDiff {
  const priorArgs = new Set(prior.arguments);
  const currentArgs = new Set(current.arguments);
  const added = current.arguments.filter((item) => !priorArgs.has(item));
  const abandoned = prior.arguments.filter((item) => !currentArgs.has(item));
  const kept = current.arguments.filter((item) => priorArgs.has(item));
  const priorAuth = new Set(prior.authorities);
  const currentAuth = new Set(current.authorities);
  const priorAdmit = new Set(prior.admissions);
  return {
    matter: current.matter,
    prior: prior.filing,
    current: current.filing,
    added,
    abandoned,
    modified: added.length + abandoned.length > 0 ? kept : [],
    newAuthorities: current.authorities.filter((item) => !priorAuth.has(item)),
    droppedAuthorities: prior.authorities.filter((item) => !currentAuth.has(item)),
    factualAdmissions: current.admissions.filter((item) => !priorAdmit.has(item)),
  };
}

export function diffsForMatter(snapshots: ArgumentSnapshot[], matter: number): ArgumentDiff[] {
  const ordered = snapshots.filter((row) => row.matter === matter).sort((a, b) => a.date.localeCompare(b.date));
  const diffs: ArgumentDiff[] = [];
  for (let i = 1; i < ordered.length; i += 1) diffs.push(diffArguments(ordered[i - 1], ordered[i]));
  return diffs;
}
