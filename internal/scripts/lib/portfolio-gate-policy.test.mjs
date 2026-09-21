import { describe, expect, it } from "vitest";
import { runPortfolioGate } from "../portfolio-gate.mjs";
import {
  checkNodeVersion,
  checkPrerequisites,
  decideHookAction,
  EMERGENCY_BYPASS,
  GATE_STEPS,
  parsePushLines,
  pushTouchesMain,
  shouldRunChecks,
  shouldSkipDiskDocs,
  shouldSkipRefUpdate,
  ZERO_SHA,
} from "./portfolio-gate-policy.mjs";

const FEATURE = "refs/heads/cursor/example";
const MAIN = "refs/heads/main";
const DOCUMENTS = "refs/heads/documents";
const SHA = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

function line({ localRef = FEATURE, localSha = SHA, remoteRef = FEATURE, remoteSha = SHA } = {}) {
  return { localRef, localSha, remoteRef, remoteSha };
}

describe("GATE_STEPS", () => {
  it("keeps the pre-push step list including the citation gate", () => {
    expect(GATE_STEPS.map((step) => step.id)).toEqual([
      "lint",
      "typecheck",
      "validate-portfolio",
      "golden-damages",
      "unit-suite",
      "citation-gate",
    ]);
    expect(GATE_STEPS.at(-1).argv).toEqual([
      "python3",
      "internal/scripts/verify-citations.py",
      "--check",
    ]);
  });
});

describe("parsePushLines / skip refs", () => {
  it("parses git pre-push stdin", () => {
    const text = `${FEATURE} ${SHA} ${MAIN} ${ZERO_SHA}\n`;
    expect(parsePushLines(text)).toEqual([
      {
        localRef: FEATURE,
        localSha: SHA,
        remoteRef: MAIN,
        remoteSha: ZERO_SHA,
      },
    ]);
  });

  it("skips branch deletes and the documents store", () => {
    expect(shouldSkipRefUpdate(line({ localSha: ZERO_SHA, remoteRef: FEATURE }))).toBe(true);
    expect(shouldSkipRefUpdate(line({ remoteRef: DOCUMENTS }))).toBe(true);
    expect(shouldSkipRefUpdate(line({ remoteRef: FEATURE }))).toBe(false);
  });

  it("runs the gate when any line is a code-branch update", () => {
    expect(shouldRunChecks([line({ localSha: ZERO_SHA }), line({ remoteRef: FEATURE })])).toBe(
      true,
    );
    expect(shouldRunChecks([line({ localSha: ZERO_SHA }), line({ remoteRef: DOCUMENTS })])).toBe(
      false,
    );
  });

  it("treats local or remote main as touching main", () => {
    expect(pushTouchesMain([line({ localRef: MAIN, remoteRef: FEATURE })])).toBe(true);
    expect(pushTouchesMain([line({ localRef: FEATURE, remoteRef: MAIN })])).toBe(true);
    expect(pushTouchesMain([line({ remoteRef: FEATURE })])).toBe(false);
  });
});

describe("decideHookAction bypass policy", () => {
  it("skips deletes and documents-only pushes without a bypass", () => {
    expect(
      decideHookAction({
        lines: [line({ localSha: ZERO_SHA }), line({ remoteRef: DOCUMENTS })],
        skipValue: undefined,
      }).action,
    ).toBe("skip");
  });

  it("does not treat SKIP_PORTFOLIO_GATE=1 as a bypass", () => {
    const decision = decideHookAction({
      lines: [line()],
      skipValue: "1",
    });
    expect(decision.action).toBe("run");
    expect(decision.reason).toMatch(/ignored/);
  });

  it("accepts EMERGENCY only off main", () => {
    const decision = decideHookAction({
      lines: [line({ remoteRef: FEATURE })],
      skipValue: EMERGENCY_BYPASS,
    });
    expect(decision.action).toBe("bypass");
  });

  it("refuses EMERGENCY when the push updates main (local or remote)", () => {
    expect(
      decideHookAction({
        lines: [line({ remoteRef: MAIN })],
        skipValue: EMERGENCY_BYPASS,
      }).action,
    ).toBe("refuse");
    expect(
      decideHookAction({
        lines: [line({ localRef: MAIN, remoteRef: FEATURE })],
        skipValue: EMERGENCY_BYPASS,
      }).action,
    ).toBe("refuse");
  });

  it("runs the gate when no bypass is set", () => {
    expect(decideHookAction({ lines: [line()], skipValue: undefined }).action).toBe("run");
  });
});

describe("checkPrerequisites / disk-docs mode", () => {
  it("fails closed when node_modules or python3 is missing", () => {
    expect(checkPrerequisites({ nodeModulesExists: false, python3Available: true }).ok).toBe(
      false,
    );
    expect(checkPrerequisites({ nodeModulesExists: true, python3Available: false }).ok).toBe(
      false,
    );
    expect(checkPrerequisites({ nodeModulesExists: true, python3Available: true }).ok).toBe(true);
  });

  it("points missing node_modules at npm install then npm run gate", () => {
    const { message } = checkPrerequisites({
      nodeModulesExists: false,
      python3Available: true,
    });
    expect(message).toMatch(/npm install/);
    expect(message).toMatch(/npm run gate/);
  });

  it("refuses a Node major below engines.node before any step runs", () => {
    const { ok, message } = checkPrerequisites({
      nodeModulesExists: true,
      python3Available: true,
      nodeVersion: "20.20.1",
      enginesRange: ">=22.22.0",
      nvmrcVersion: "22.22.2",
    });
    expect(ok).toBe(false);
    expect(message).toMatch(/20\.20\.1/);
    expect(message).toMatch(/22\.22\.0/);
    expect(message).toMatch(/nvm use/);
  });

  it("wins over node_modules so a wrong Node is reported first", () => {
    const { message } = checkPrerequisites({
      nodeModulesExists: false,
      python3Available: true,
      nodeVersion: "20.20.1",
      enginesRange: ">=22.22.0",
    });
    expect(message).toMatch(/engines\.node/);
    expect(message).not.toMatch(/npm install/);
  });

  it("accepts the declared major and anything newer", () => {
    for (const nodeVersion of ["22.22.0", "22.22.2", "24.0.0"]) {
      expect(checkNodeVersion({ nodeVersion, enginesRange: ">=22.22.0" }).ok).toBe(true);
    }
  });

  it("does not enforce when the range or version is unreadable", () => {
    expect(checkNodeVersion({ nodeVersion: "20.20.1", enginesRange: undefined }).ok).toBe(true);
    expect(checkNodeVersion({ nodeVersion: undefined, enginesRange: ">=22.22.0" }).ok).toBe(true);
    expect(checkPrerequisites({ nodeModulesExists: true, python3Available: true }).ok).toBe(true);
  });

  it("auto-selects manifest mode when no matter-* PDF tree is present", () => {
    expect(shouldSkipDiskDocs([])).toBe(true);
    expect(shouldSkipDiskDocs(["_form-library"])).toBe(true);
    expect(shouldSkipDiskDocs(["matter-01"])).toBe(false);
  });
});

describe("runPortfolioGate", () => {
  function run(over = {}) {
    const ran = [];
    const errs = [];
    const logs = [];
    const env = { ...(over.env ?? {}) };
    const { env: _env, runStep: customStep, ...rest } = over;
    const code = runPortfolioGate({
      hookMode: false,
      nodeModulesExists: true,
      python3Available: true,
      matterDirNames: [],
      log: (msg) => logs.push(msg),
      logErr: (msg) => errs.push(msg),
      ...rest,
      env,
      runStep:
        customStep ??
        ((step) => {
          ran.push(step.id);
          return 0;
        }),
    });
    return { code, ran, errs, logs, env };
  }

  it("refuses missing node_modules without running steps", () => {
    const { code, ran, errs } = run({ nodeModulesExists: false });
    expect(code).toBe(1);
    expect(ran).toEqual([]);
    expect(errs[0]).toMatch(/npm install/);
  });

  it("refuses missing python3 without running steps", () => {
    const { code, ran, errs } = run({ python3Available: false });
    expect(code).toBe(1);
    expect(ran).toEqual([]);
    expect(errs[0]).toMatch(/citation gate is required/);
  });

  it("sets PORTFOLIO_SKIP_DISK_DOCS when the PDF tree is missing", () => {
    const { code, env } = run({ matterDirNames: [] });
    expect(code).toBe(0);
    expect(env.PORTFOLIO_SKIP_DISK_DOCS).toBe("1");
    expect(env.VITE_COPY_DOCUMENTS).toBe("0");
  });

  it("runs every gate step including citation", () => {
    const { code, ran, logs } = run({ matterDirNames: ["matter-01"] });
    expect(code).toBe(0);
    expect(ran).toEqual(GATE_STEPS.map((step) => step.id));
    expect(logs.at(-1)).toMatch(/gate passed/);
  });

  it("skips hook work for documents-only or delete-only pushes", () => {
    const stdin = `${FEATURE} ${ZERO_SHA} ${FEATURE} ${SHA}\n`;
    const { code, ran } = run({
      hookMode: true,
      stdinText: stdin,
    });
    expect(code).toBe(0);
    expect(ran).toEqual([]);
  });

  it("refuses EMERGENCY bypass on a push to main", () => {
    const stdin = `${FEATURE} ${SHA} ${MAIN} ${SHA}\n`;
    const { code, ran, errs } = run({
      hookMode: true,
      stdinText: stdin,
      env: { SKIP_PORTFOLIO_GATE: "EMERGENCY" },
    });
    expect(code).toBe(1);
    expect(ran).toEqual([]);
    expect(errs[0]).toMatch(/cannot bypass a push to main/);
  });

  it("allows EMERGENCY bypass on a feature branch only", () => {
    const stdin = `${FEATURE} ${SHA} ${FEATURE} ${SHA}\n`;
    const { code, ran } = run({
      hookMode: true,
      stdinText: stdin,
      env: { SKIP_PORTFOLIO_GATE: "EMERGENCY" },
    });
    expect(code).toBe(0);
    expect(ran).toEqual([]);
  });

  it("does not let SKIP_PORTFOLIO_GATE=1 skip the hook", () => {
    const stdin = `${FEATURE} ${SHA} ${FEATURE} ${SHA}\n`;
    const { code, ran, errs } = run({
      hookMode: true,
      stdinText: stdin,
      env: { SKIP_PORTFOLIO_GATE: "1" },
    });
    expect(code).toBe(0);
    expect(ran).toEqual(GATE_STEPS.map((step) => step.id));
    expect(errs[0]).toMatch(/ignored/);
  });
});
