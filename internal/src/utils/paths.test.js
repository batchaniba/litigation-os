import { describe, expect, it } from "vitest";
import { withBase } from "./paths";

describe("withBase", () => {
  // BASE_URL is "/" under test and vite dev, and
  // "/interactive-litigation-portfolio/" on GitHub Pages. Both must produce a
  // single-slash join — the trailing slash is stripped before concatenating.
  it("joins the configured base without doubling the slash", () => {
    expect(withBase("/logo-dark.webp")).toBe("/logo-dark.webp");
    expect(withBase("/documents/matter-05/complaint.pdf")).toBe("/documents/matter-05/complaint.pdf");
  });

  it("leaves the path untouched apart from the prefix", () => {
    expect(withBase("/branding/slb-dark.webp")).toBe("/branding/slb-dark.webp");
    expect(withBase("/a b/c%20d.pdf")).toBe("/a b/c%20d.pdf");
  });

  it("never emits a double slash", () => {
    expect(withBase("/x")).not.toContain("//");
  });
});
