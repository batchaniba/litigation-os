import { afterEach, describe, expect, it, vi } from "vitest";
import { coverageSection, crossMatterSection, downloadMatterSummary, matterMarkdown } from "./exportMatter";
import { clusterForMatter } from "./crossMatter";
import { coverageForMatter } from "../data/coverage";
import type { Matter, TimelineEvent } from "../types/portfolio";

const baseMatter = {
  number: 99,
  caption: "Newanforbi v. Example",
  case_no: "CV-2026-0099",
  court: "San Joaquin Sup. Ct.",
  status: "Active",
  judge: "Hon. Example Judge",
  filed: "Jan. 5, 2026",
  claims: "Retaliation and negligence.",
  causes: ["Bane Act", "Negligence"],
  key_facts: "Facts of the matter.",
  procedural_status: "Answer due.",
  damages: "$250,000",
  risk: "Comparative fault argument.",
  documents: [{ label: "Original Complaint", path: "/documents/matter-99/complaint.pdf" }],
} as unknown as Matter;

const event = (date: string, text: string) => ({ date, event: text, matters: [99], type: "filing" }) as unknown as TimelineEvent;

describe("matterMarkdown", () => {
  it("leads with the caption and the docket identifiers", () => {
    const markdown = matterMarkdown(baseMatter);
    expect(markdown).toContain("# Matter 99: Newanforbi v. Example");
    expect(markdown).toContain("**Case number:** CV-2026-0099");
    expect(markdown).toContain("**Court:** San Joaquin Sup. Ct.");
  });

  it("renders causes and documents as lists", () => {
    const markdown = matterMarkdown(baseMatter);
    expect(markdown).toContain("- Bane Act");
    expect(markdown).toContain("- Negligence");
    expect(markdown).toContain("- Original Complaint");
  });

  it("states plainly when there is no next action or recent development", () => {
    const markdown = matterMarkdown(baseMatter);
    expect(markdown).toContain("**Next action:** No upcoming action recorded");
    expect(markdown).toContain("**Next deadline:** None recorded");
    expect(markdown).toContain("**Recent development:** None recorded");
  });

  it("uses the supplied next and recent events when present", () => {
    const markdown = matterMarkdown(
      baseMatter,
      event("Sep. 1, 2026", "Case management conference"),
      event("Jul. 4, 2026", "Answer filed"),
    );
    expect(markdown).toContain("**Next action:** Case management conference");
    expect(markdown).toContain("**Next deadline:** Sep. 1, 2026");
    expect(markdown).toContain("Jul. 4, 2026 — Answer filed");
  });

  it("says so when no documents are linked", () => {
    expect(matterMarkdown({ ...baseMatter, documents: [] })).toContain("No documents linked.");
    expect(matterMarkdown({ ...baseMatter, documents: undefined } as Matter)).toContain("No documents linked.");
  });
});

describe("coverageSection and crossMatterSection", () => {
  it("are omitted for a matter with neither", () => {
    expect(coverageSection(baseMatter)).toBe("");
    expect(crossMatterSection(baseMatter)).toBe("");
  });

  it("renders insurance limits for a matter that has them", () => {
    const insured = [...Array(40).keys()].map((n) => n + 1).find((n) => coverageForMatter(n));
    expect(insured, "portfolio should have at least one insured matter").toBeDefined();
    const section = coverageSection({ ...baseMatter, number: insured! });
    expect(section).toContain("## Insurance coverage on file");
    expect(section).toContain("per incident");
    expect(section).toContain("**Carrier:**");
  });

  it("renders cluster context for a matter in the cross-matter graph", () => {
    const clustered = [...Array(40).keys()].map((n) => n + 1).find((n) => clusterForMatter(n));
    expect(clustered, "portfolio should have at least one clustered matter").toBeDefined();
    const section = crossMatterSection({ ...baseMatter, number: clustered! });
    expect(section).toContain("## Cross-matter significance");
    expect(section).toContain("**Cluster:**");
  });
});

describe("downloadMatterSummary", () => {
  afterEach(() => vi.restoreAllMocks());

  it("names the file by zero-padded matter number and defers the revoke", () => {
    const createObjectURL = vi.fn().mockReturnValue("blob:fake");
    const revokeObjectURL = vi.fn();
    vi.stubGlobal("URL", { ...URL, createObjectURL, revokeObjectURL });
    const click = vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});
    const anchors: HTMLAnchorElement[] = [];
    const createElement = document.createElement.bind(document);
    vi.spyOn(document, "createElement").mockImplementation((tag: string) => {
      const node = createElement(tag);
      if (tag === "a") anchors.push(node as HTMLAnchorElement);
      return node;
    });
    vi.useFakeTimers();

    try {
      downloadMatterSummary({ ...baseMatter, number: 7 }, "# body");
      expect(click).toHaveBeenCalledOnce();
      expect(anchors[0].download).toBe("matter-07-summary.md");
      // The regression: revoking on the same tick races the download in Safari.
      expect(revokeObjectURL).not.toHaveBeenCalled();
      vi.runAllTimers();
      expect(revokeObjectURL).toHaveBeenCalledWith("blob:fake");
    } finally {
      vi.useRealTimers();
      vi.unstubAllGlobals();
    }
  });
});
