import { describe, expect, it } from "vitest";
import { formatMatterRefs, matterRefsInclude, parseMatterRefs } from "./matterRefs.js";

describe("matterRefs", () => {
  it("normalizes number arrays and CSV strings", () => {
    expect(parseMatterRefs([1, 2, 7])).toEqual({ all: false, numbers: [1, 2, 7], label: "1, 2, 7" });
    expect(parseMatterRefs("1, 2, 7")).toEqual({ all: false, numbers: [1, 2, 7], label: "1, 2, 7" });
  });

  it("keeps portfolio sentinels", () => {
    expect(parseMatterRefs("All").all).toBe(true);
    expect(formatMatterRefs("All CDCR")).toBe("All CDCR");
  });

  it("matches matter membership without treating All as every matter by default", () => {
    expect(matterRefsInclude([20, 24], 20)).toBe(true);
    expect(matterRefsInclude([20, 24], 1)).toBe(false);
    expect(matterRefsInclude("All", 1)).toBe(false);
    expect(matterRefsInclude("All", 1, { includeAll: true })).toBe(true);
  });
});
