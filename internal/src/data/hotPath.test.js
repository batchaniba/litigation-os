import { describe, expect, it } from "vitest";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const srcRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function read(rel) {
  return fs.readFileSync(path.join(srcRoot, rel), "utf8");
}

describe("hot-path modules stay off the full docket log and document registry", () => {
  it("matters/index.ts does not import the registry or timeline", () => {
    const src = read("data/matters/index.ts");
    expect(src).not.toMatch(/from ["'].*documents["']/);
    expect(src).not.toMatch(/timeline\.json/);
    expect(src).toMatch(/summaries\.json/);
  });

  it("useNextActions reads upcoming.json, not timeline.json", () => {
    const src = read("hooks/useNextActions.js");
    expect(src).toMatch(/from ["'].*upcoming\.json["']/);
    expect(src).not.toMatch(/from ["'].*timeline\.json["']/);
  });

  it("statusLabel.ts does not import matterTimeline", () => {
    const src = read("utils/statusLabel.ts");
    expect(src).not.toMatch(/matterTimeline/);
    expect(src).not.toMatch(/timeline\.json/);
  });

  it("the shell deadline clock uses upcoming.json", () => {
    const src = read("components/layout/ShellLayout.tsx");
    expect(src).toMatch(/upcoming\.json/);
    expect(src).not.toMatch(/timeline\.json/);
  });
});
