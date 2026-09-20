import { describe, expect, it } from "vitest";
import {
  buildCheckOutput,
  CHECK_NAME,
  failClosedConclusion,
  truncateLog,
} from "./check.mjs";

describe("CHECK_NAME", () => {
  it("is exactly portfolio-gate", () => {
    expect(CHECK_NAME).toBe("portfolio-gate");
  });
});

describe("fail-closed conclusions", () => {
  it("never returns neutral", () => {
    expect(failClosedConclusion("timeout")).toBe("failure");
    expect(failClosedConclusion("container could not start")).toBe("failure");
    expect(failClosedConclusion("invalid signature")).toBe("failure");
  });
});

describe("buildCheckOutput / truncateLog", () => {
  it("titles success and failure with the locked check name", () => {
    expect(buildCheckOutput({ ok: true, sha: "a".repeat(40) }).title).toBe("portfolio-gate passed");
    expect(buildCheckOutput({ ok: false, sha: "b".repeat(40), reason: "boom" }).title).toBe(
      "portfolio-gate failed",
    );
  });

  it("mentions the timeout when the reason is a timeout", () => {
    const out = buildCheckOutput({
      ok: false,
      reason: "No result within 1500000ms",
      timeoutMs: 1_500_000,
      sha: "c".repeat(40),
    });
    expect(out.summary).toMatch(/1500s/);
    expect(out.summary).toMatch(/Fail-closed/);
  });

  it("truncates long logs", () => {
    const text = truncateLog("x".repeat(100), 20);
    expect(text.startsWith("x".repeat(20))).toBe(true);
    expect(text).toMatch(/truncated/);
  });
});
