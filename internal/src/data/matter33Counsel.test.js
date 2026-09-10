import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");

describe("Matter 33 counsel lock", () => {
  it("keeps Fiel Dizon Tigno first on the motion-to-strike POS list", () => {
    const lib = readFileSync(
      path.join(ROOT, "internal/scripts/lib/matter33_counsel.py"),
      "utf8",
    );
    const script = readFileSync(
      path.join(ROOT, "internal/scripts/matter33-motion-to-strike-answer.py"),
      "utf8",
    );

    expect(lib).toContain('TIGNO_NAME = "Fiel Dizon Tigno"');
    expect(lib).toMatch(/Tigno is first on purpose/);
    expect(script).toContain("from matter33_counsel import counsel_pos_recipients");
    expect(script).toContain("SERVICE_RECIPIENTS = counsel_pos_recipients()");
    expect(script).not.toMatch(
      /SERVICE_RECIPIENTS = \[[^\]]*William J\. McMahon[^\]]*\]/s,
    );
  });
});
