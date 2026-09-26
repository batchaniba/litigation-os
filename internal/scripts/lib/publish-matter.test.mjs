import { describe, expect, it } from "vitest";
import {
  collectDeniedKeyPaths,
  collectPublishStripIssues,
  collectSettlementLeakIssues,
  isCourtFacingClock,
  publishMatter,
  sanitizePublicText,
} from "./publish-matter.mjs";

const SECRET_FACTS =
  "SECRET KEY FACTS NOVEL — the demand strategy is to open at $2.4 million and settle for housing plus a confidential figure after the recruiter cell is used.";
const PERSONAL_EMAIL = "jane.secret@gmail.com";

function fixture(over = {}) {
  const { matter: matterOver, ...rest } = over;
  return {
    matter: {
      number: 99,
      caption: "Test v. Example",
      case_no: "1:26-cv-00099",
      court: "USDC N.D. Cal.",
      judge: "Hon. Example Judge",
      lifecycle: "active",
      proceeding: "federal_civil",
      phase: "pleadings",
      cluster: 5,
      status_label: "Answer pending",
      type: "Federal",
      filed: "Sep. 1, 2026",
      archived: false,
      defendants: "Example LLC",
      claims: "FCRA",
      causes: ["FCRA §1681"],
      status: "Long narrative that must not ship.",
      key_facts: SECRET_FACTS,
      procedural_status: "See clocks — demand strategy memo stays here.",
      damages: "MODERATE: $2,400,000 settlement posture.",
      risk: "Settlement note: take $50k if they blink.",
      policy_limits: "$1M / $5M",
      note: "Internal InfoMart ID 998877.",
      same_incident: "RJ68845",
      ...matterOver,
    },
    docket: [
      {
        dkt: 1,
        filed: true,
        title: "Complaint",
        path: "/documents/matter-99/complaint.pdf",
        date: "2026-09-01",
      },
      {
        dkt: null,
        filed: false,
        title: "Unfiled draft demand strategy",
        path: "/documents/matter-99/draft-demand.pdf",
      },
    ],
    clocks: [
      {
        date: "2026-10-01",
        kind: "hearing",
        status: "set",
        actor: "court",
        source_dkt: 12,
        title: "Motion to dismiss hearing",
      },
      {
        date: "2026-10-02",
        kind: "deadline",
        status: "open",
        actor: "you",
        source_dkt: null,
        title: "WATCH — demand strategy settlement posture; do not serve yet",
      },
    ],
    documents: [
      { path: "/documents/matter-99/complaint.pdf", filed: true },
      { path: "/documents/matter-99/draft-demand.pdf", filed: false },
      { path: "/documents/matter-99/tap.pdf", filed: false },
      { path: "/documents/matter-99/notes.docx", filed: true },
    ],
    counsel: {
      appearances: [
        {
          name: "Jane Doe",
          firm: "Law LLP",
          attorney_id: 123,
          email: PERSONAL_EMAIL,
          dossier: "internal/docs/counsel/jane-doe-playbook.md",
        },
      ],
    },
    phoneTapPaths: new Set(["/documents/matter-99/tap.pdf"]),
    ...rest,
  };
}

describe("publishMatter", () => {
  it("keeps filing-safe identity, docket, court clocks, and pleading counsel", () => {
    const published = publishMatter(fixture());
    expect(published.number).toBe(99);
    expect(published.caption).toBe("Test v. Example");
    expect(published.case_no).toBe("1:26-cv-00099");
    expect(published.court).toBe("USDC N.D. Cal.");
    expect(published.judge).toBe("Hon. Example Judge");
    expect(published.lifecycle).toBe("active");
    expect(published.proceeding).toBe("federal_civil");
    expect(published.phase).toBe("pleadings");
    expect(published.cluster).toBe(5);
    expect(published.status_label).toBe("Answer pending");
    expect(published.docket).toEqual([
      {
        dkt: 1,
        filed: true,
        title: "Complaint",
        path: "/documents/matter-99/complaint.pdf",
        date: "2026-09-01",
      },
    ]);
    expect(published.clocks).toEqual([
      {
        date: "2026-10-01",
        kind: "hearing",
        status: "set",
        title: "Motion to dismiss hearing",
        actor: "court",
      },
    ]);
    expect(published.documents.map((d) => d.path).sort()).toEqual([
      "/documents/matter-99/complaint.pdf",
      "/documents/matter-99/tap.pdf",
    ]);
    expect(published.people).toEqual([
      { name: "Jane Doe", kind: "counsel", firm: "Law LLP", attorney_id: 123 },
      { name: "Hon. Example Judge", kind: "judge" },
    ]);
  });

  it("does not emit key_facts, personal email, or settlement strategy", () => {
    const published = publishMatter(fixture());
    const json = JSON.stringify(published);
    expect(published).not.toHaveProperty("key_facts");
    expect(published).not.toHaveProperty("damages");
    expect(published).not.toHaveProperty("risk");
    expect(published).not.toHaveProperty("procedural_status");
    expect(published).not.toHaveProperty("status");
    expect(published).not.toHaveProperty("policy_limits");
    expect(published).not.toHaveProperty("same_incident");
    expect(published).not.toHaveProperty("note");
    expect(json).not.toContain("key_facts");
    expect(json).not.toContain(SECRET_FACTS);
    expect(json).not.toContain(PERSONAL_EMAIL);
    expect(json).not.toContain("settlement posture");
    expect(json).not.toContain("draft-demand");
    expect(json).not.toContain("playbook");
    expect(json).not.toContain("WATCH");
    expect(json).not.toContain(".docx");
    expect(collectDeniedKeyPaths(published)).toEqual([]);
    expect(collectPublishStripIssues({ published, sourceMatter: fixture().matter })).toEqual([]);
  });

  it("drops settlement figures from status_label", () => {
    const published = publishMatter(
      fixture({ matter: { status_label: "Settled Jul. 14, 2026 ($35,000)" } }),
    );
    expect(published.status_label).toBeUndefined();
    expect(JSON.stringify(published)).not.toContain("$35,000");
  });
});

describe("isCourtFacingClock", () => {
  it("fails closed on computed strategy clocks without a docket number", () => {
    expect(
      isCourtFacingClock({
        date: "2026-11-01",
        kind: "deadline",
        source_dkt: null,
        title: "Computed SOL backstop",
      }),
    ).toBe(false);
    expect(
      isCourtFacingClock({
        date: "2026-11-20",
        kind: "hearing",
        source_dkt: null,
        title: "MTD hearing",
      }),
    ).toBe(true);
    expect(
      isCourtFacingClock({
        date: "2026-12-17",
        kind: "deadline",
        source_dkt: null,
        title: "Case Management Conference, Dept. 20",
      }),
    ).toBe(true);
  });
});

describe("sanitizePublicText", () => {
  it("redacts personal email and phone", () => {
    expect(sanitizePublicText(`Serve ${PERSONAL_EMAIL} at (209) 801-4442`)).toBe(
      "Serve [redacted] at [redacted]",
    );
  });
});

describe("collectPublishStripIssues", () => {
  it("fails when a denylisted field is smuggled onto the publish object", () => {
    const poisoned = { ...publishMatter(fixture()), key_facts: SECRET_FACTS };
    const issues = collectPublishStripIssues({ published: poisoned });
    expect(issues.some((row) => row.includes("key_facts"))).toBe(true);
  });
});

describe("settlement figures stay internal", () => {
  it("does not publish private or settlement-mechanics clocks", () => {
    const base = { date: "2026-10-26", kind: "deadline", actor: "opposing" };
    expect(isCourtFacingClock({ ...base, title: "Response deadline for Randstad" })).toBe(true);
    expect(isCourtFacingClock({ ...base, title: "Response deadline for Randstad", private: true })).toBe(false);
    expect(isCourtFacingClock({ ...base, title: "Response due; settlement payment outside date" })).toBe(false);
  });

  it("flags settlement dollar figures and amount fields", () => {
    const hit = (text) => collectSettlementLeakIssues("t", text).length > 0;
    expect(hit("Pilot settled for $35,000")).toBe(true);
    expect(hit("$85,000 global settlement offer rejected")).toBe(true);
    expect(hit('type: "settlement", status: "SETTLED", amount: 35000')).toBe(true);
    expect(hit("demand_amount: 55000")).toBe(true);
    expect(hit("Agreement in principle reached")).toBe(true);
  });

  it("leaves ordinary text alone", () => {
    const hit = (text) => collectSettlementLeakIssues("t", text).length > 0;
    expect(hit("Matter 22 settled July 14, 2026. Matters 32 and 33 plead damages exceeding $214,000")).toBe(false);
    expect(hit("meet and confer regarding early settlement, ADR process selection")).toBe(false);
    expect(hit('type: "settlement", amount: 0, confidential: true')).toBe(false);
  });
});
