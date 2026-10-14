// Repository-root cleanliness policy, shared by validate-portfolio.mjs and its tests.
//
// History: checkRepoRootIsClean() used to allow *any* .pdf or .docx at the root
// unconditionally, on the theory that they were transient upload artifacts.
// They were not transient. 41 tracked files / 161.6 MB accumulated there,
// including live discovery responses and demurrer briefing for matters 05 and
// 06, plus 8 files that are registered in the document manifest but whose bytes
// R2 never received.
//
// The blanket bypass is gone. In its place, root-quarantine.json is an explicit
// allowlist of the known backlog: anything at the root that is not listed fails
// the gate immediately, so the pile cannot grow while it is being drained.
//
// Removing an entry is the intended direction of travel and needs no ceremony.
// Adding one requires editing a committed ledger inside a pull request, where a
// reviewer sees it.

/**
 * Identity is checked by size rather than sha256 on purpose: the ledger covers
 * 161.6 MB and the gate runs on every push. Size alone still catches a
 * different file parked under an allowlisted name, which is the case that
 * matters.
 */
export function classifyRootEntries({ entries, allowedFiles, quarantine }) {
  const errors = [];
  const warnings = [];
  const ledger = new Map((quarantine?.files ?? []).map((file) => [file.name, file]));
  const seen = new Set();

  for (const entry of entries) {
    if (!entry.isFile) continue;
    if (entry.name.startsWith(".")) continue;
    if (allowedFiles.has(entry.name)) continue;

    const listed = ledger.get(entry.name);
    if (!listed) {
      errors.push(
        `repository root has stray file "${entry.name}" — move it into ` +
          `documents/matter-NN/ (or internal/assets/). ` +
          `Document-store files are pushed to R2, not committed here.`,
      );
      continue;
    }

    seen.add(entry.name);
    if (typeof entry.size === "number" && entry.size !== listed.size) {
      errors.push(
        `repository root file "${entry.name}" is quarantined at ${listed.size} bytes ` +
          `but is now ${entry.size} bytes — a different file is parked under a ` +
          `quarantined name. Update internal/src/data/index/root-quarantine.json.`,
      );
    }
  }

  const drained = [...ledger.keys()].filter((name) => !seen.has(name));
  if (drained.length > 0) {
    warnings.push(
      `root-quarantine.json lists ${drained.length} file(s) no longer at the ` +
        `repository root — drop them from the ledger: ${drained.slice(0, 5).join(", ")}` +
        `${drained.length > 5 ? ", …" : ""}`,
    );
  }

  if (seen.size > 0) {
    const bytes = [...seen].reduce((sum, name) => sum + (ledger.get(name)?.size ?? 0), 0);
    warnings.push(
      `repository root still holds ${seen.size} quarantined document(s) ` +
        `(${(bytes / 1e6).toFixed(1)} MB). File them under ` +
        `documents/, run npm run sync:manifest and ` +
        `npm run documents:push, then remove them here and from the ledger.`,
    );
  }

  return { errors, warnings, remaining: seen.size };
}
