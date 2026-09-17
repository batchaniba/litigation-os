import { describe, expect, it } from "vitest";
import {
  classifyNpm,
  formatReport,
  groupFor,
  parseRequirementsTxt,
  pipStale,
} from "./deps-outdated.mjs";

describe("groupFor", () => {
  it("keeps the old Dependabot peer groups", () => {
    expect(groupFor("eslint", "patch")).toBe("dev-tooling");
    expect(groupFor("@vitejs/plugin-react", "patch")).toBe("build-tooling");
    expect(groupFor("react-router", "patch")).toBe("react-ecosystem");
    expect(groupFor("vitest", "major")).toBe("vitest-stack");
    expect(groupFor("vitest", "patch")).toBe("vitest-stack");
    expect(groupFor("@vitest/coverage-v8", "patch")).toBe("vitest-stack");
    expect(groupFor("react", "major")).toBe("react-stack");
    expect(groupFor("left-pad", "patch")).toBe("other");
  });
});

describe("classifyNpm", () => {
  it("splits in-range from majors and ignores typescript majors", () => {
    const { inRange, major, ignoredMajor } = classifyNpm({
      vite: { current: "8.2.2", wanted: "8.2.3", latest: "8.2.3", type: "devDependencies" },
      react: { current: "19.2.8", wanted: "19.2.8", latest: "20.0.0", type: "dependencies" },
      typescript: { current: "5.9.3", wanted: "5.9.3", latest: "7.0.0", type: "devDependencies" },
    });
    expect(inRange.map((r) => r.name)).toEqual(["vite"]);
    expect(major.map((r) => r.name)).toEqual(["react"]);
    expect(ignoredMajor.map((r) => r.name)).toEqual(["typescript"]);
    expect(inRange[0].group).toBe("build-tooling");
    expect(major[0].group).toBe("react-stack");
  });

  it("does not call a newer line a major when the latest dist-tag lags", () => {
    const { major } = classifyNpm({
      jsdom: { current: "30.0.1", wanted: "30.1.0", latest: "29.1.1", type: "devDependencies" },
      "react-router": { current: "8.3.1", wanted: "8.4.0", latest: "7.18.4", type: "dependencies" },
    });
    expect(major).toEqual([]);
  });
});

describe("parseRequirementsTxt / pipStale", () => {
  it("reads >= floors and skips comments", () => {
    const rows = parseRequirementsTxt(
      "# hi\nreportlab>=5.0.1\npypdf>=6.14.2  # merge\n\nnot-a-pin\n",
    );
    expect(rows).toEqual([
      { name: "reportlab", floor: "5.0.1" },
      { name: "pypdf", floor: "6.14.2" },
    ]);
    expect(pipStale(rows, new Map([["reportlab", "5.4.0"], ["pypdf", "6.14.2"]]))).toEqual([
      { name: "reportlab", floor: "5.0.1", latest: "5.4.0" },
    ]);
  });
});

describe("formatReport", () => {
  it("says current when nothing is stale", () => {
    const text = formatReport({
      npm: { inRange: [], major: [], ignoredMajor: [] },
      pip: { stale: [] },
    });
    expect(text).toContain("lockfile matches");
    expect(text).toContain("every floor is already the latest");
  });
});
