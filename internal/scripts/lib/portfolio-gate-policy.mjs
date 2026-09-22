// Fail-closed local portfolio gate policy. Shared by
// `npm run gate` and `.githooks/pre-push` via portfolio-gate.mjs.
// Do not treat SKIP_PORTFOLIO_GATE=1 as a bypass.

export const ZERO_SHA = "0000000000000000000000000000000000000000";
export const EMERGENCY_BYPASS = "EMERGENCY";
export const MAIN_REF = "refs/heads/main";
export const DOCUMENTS_REF = "refs/heads/documents";

/** Same step list the pre-push hook has always run. Citation is required. */
export const GATE_STEPS = [
  { id: "lint", label: "lint", argv: ["npm", "run", "-s", "lint"] },
  { id: "typecheck", label: "typecheck", argv: ["npm", "run", "-s", "typecheck"] },
  {
    id: "validate-portfolio",
    label: "validate-portfolio",
    argv: ["node", "internal/scripts/validate-portfolio.mjs"],
  },
  {
    id: "doc-kind",
    label: "doc-kind",
    argv: ["node", "internal/scripts/check-doc-kind.mjs"],
  },
  {
    id: "golden-damages",
    label: "golden damages",
    argv: ["node", "internal/scripts/test-golden.mjs"],
  },
  {
    id: "unit-suite",
    label: "unit suite",
    argv: ["npx", "vitest", "run", "--reporter=dot"],
  },
  {
    id: "citation-gate",
    label: "citation gate",
    argv: ["python3", "internal/scripts/verify-citations.py", "--check"],
  },
];

export function parsePushLines(stdinText) {
  return String(stdinText ?? "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [localRef = "", localSha = "", remoteRef = "", remoteSha = ""] = line.split(/\s+/);
      return { localRef, localSha, remoteRef, remoteSha };
    });
}

export function isMainRef(ref) {
  return ref === MAIN_REF || ref === "main";
}

export function isDocumentsRef(ref) {
  return ref === DOCUMENTS_REF;
}

export function isDeleteSha(sha) {
  return sha === ZERO_SHA;
}

/** Branch deletes and the documents PDF-store ref are not code-gate pushes. */
export function shouldSkipRefUpdate({ localSha, remoteRef }) {
  return isDeleteSha(localSha) || isDocumentsRef(remoteRef);
}

export function shouldRunChecks(lines) {
  return lines.some((line) => !shouldSkipRefUpdate(line));
}

export function pushTouchesMain(lines) {
  return lines.some((line) => isMainRef(line.localRef) || isMainRef(line.remoteRef));
}

/**
 * Decide what the pre-push hook should do before running checks.
 * `npm run gate` does not call this — it always runs the steps.
 *
 * @returns {{ action: "skip" | "bypass" | "refuse" | "run", reason: string }}
 */
export function decideHookAction({ lines, skipValue }) {
  if (!shouldRunChecks(lines)) {
    return {
      action: "skip",
      reason: "no gated refs (branch delete or documents store only)",
    };
  }

  const emergency = skipValue === EMERGENCY_BYPASS;
  const touchesMain = pushTouchesMain(lines);

  if (emergency && touchesMain) {
    return {
      action: "refuse",
      reason:
        "SKIP_PORTFOLIO_GATE=EMERGENCY cannot bypass a push to main. Emergencies go through a feature branch and a pull request.",
    };
  }

  if (emergency) {
    return {
      action: "bypass",
      reason: "SKIP_PORTFOLIO_GATE=EMERGENCY accepted (not a push to main).",
    };
  }

  if (skipValue) {
    return {
      action: "run",
      reason: `SKIP_PORTFOLIO_GATE=${skipValue} is ignored; only SKIP_PORTFOLIO_GATE=EMERGENCY bypasses, and never on main.`,
    };
  }

  return { action: "run", reason: "gate required" };
}

/**
 * Lowest Node major that satisfies an `engines.node` range such as ">=22.22.0".
 * Returns null when the range cannot be read, so a malformed field degrades to
 * "do not enforce" rather than refusing every run.
 */
export function minimumNodeMajor(enginesRange) {
  const match = String(enginesRange ?? "").match(/(\d+)/);
  return match ? Number(match[1]) : null;
}

export function nodeMajor(version) {
  const match = String(version ?? "").match(/(\d+)/);
  return match ? Number(match[1]) : null;
}

/**
 * The unit suite runs in jsdom, which throws
 * `webidl.util.markAsUncloneable is not a function` on Node majors below the
 * declared engine. That surfaces as 52 unhandled errors and "no tests" — a
 * false catastrophic failure rather than an honest one. Refuse early instead.
 */
export function checkNodeVersion({ nodeVersion, enginesRange, nvmrcVersion }) {
  const required = minimumNodeMajor(enginesRange);
  const actual = nodeMajor(nodeVersion);
  if (required === null || actual === null || actual >= required) {
    return { ok: true, message: "" };
  }
  const pin = nvmrcVersion ? ` (.nvmrc pins ${nvmrcVersion})` : "";
  return {
    ok: false,
    message:
      `portfolio-gate: Node ${nodeVersion} does not satisfy engines.node ` +
      `"${enginesRange}"${pin}. The jsdom unit suite reports "no tests" plus ` +
      `unhandled webidl errors on older majors, so gate results would be ` +
      `misleading. Run \`nvm use\`, then npm run gate.`,
  };
}

export function checkPrerequisites({
  nodeModulesExists,
  python3Available,
  nodeVersion,
  enginesRange,
  nvmrcVersion,
}) {
  // Version first: a wrong Node major makes every later step untrustworthy.
  const node = checkNodeVersion({ nodeVersion, enginesRange, nvmrcVersion });
  if (!node.ok) {
    return node;
  }
  if (!nodeModulesExists) {
    return {
      ok: false,
      message: "portfolio-gate: node_modules missing — run npm install, then npm run gate.",
    };
  }
  if (!python3Available) {
    return {
      ok: false,
      message:
        "portfolio-gate: python3 not found — citation gate is required. Install python3, then npm run gate.",
    };
  }
  return { ok: true, message: "" };
}

/** Data-path mode, not a gate skip: validate against the committed manifest. */
export function shouldSkipDiskDocs(matterDirNames) {
  return !matterDirNames.some((name) => name.startsWith("matter-"));
}
