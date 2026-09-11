import { describe, expect, it } from "vitest";
import { intelligenceCatalog } from "../data/intelligence/catalog";
import { cases } from "../data/matters";
import { activateIssue, deriveTwin } from "./twin";
import { applyOrderToDependencies, resolveDeadlines, resolveRecipe } from "./deadlines";
import { diffArguments, diffsForMatter } from "./argumentDiff";
import { contradictionsForMatter, flagContradiction } from "./contradictions";
import { classifyDocketText, eventFromNormalizedEntry, issuesMentioned } from "./classify";
import { eventFromNormalizedEntry as emitFromNormalized } from "../../scripts/intelligence/emit-events.mjs";
import { publish, publishedEvents, resetEventBus, subscribe } from "./eventBus";
import { buildKnowledgeGraph } from "./graph";
import { assembleIntelligence, commandCenter } from "./index";
import { timeline } from "../data/timeline";
import { qiRadar, sharedCounsel } from "./queries";
import { matchFingerprint } from "./fingerprints";
import { recapAdvice } from "./recap";
import { auditCitation } from "./citeProof";
import { shockwaveFromOpinion } from "./shockwave";
import { simulateDomino, systemicImportance } from "./systemic";
import { buildWarRoom } from "./warRoom";
import { claimCoverage, weakestElement } from "./coverage";
import { overnightBrief } from "./overnight";
import type { LitigationEvent } from "./types";

const summaries = cases.filter((row) => [24, 26, 28, 29, 32, 33].includes(row.number));

describe("litigation intelligence OS", () => {
  it("builds a queryable graph: QI matters, supporting authority, and counsel who raise it", () => {
    const graph = buildKnowledgeGraph(summaries, intelligenceCatalog);
    const radar = qiRadar(graph, intelligenceCatalog);
    expect(radar.matters).toEqual(expect.arrayContaining([24, 28, 32]));
    expect(radar.supporting.map((row) => row.id)).toEqual(expect.arrayContaining(["wyatt", "richardson", "shanks"]));
    expect(radar.attorneys).toEqual(expect.arrayContaining(["Haiyang A. Li", "Blaze Van Dine"]));
    expect(sharedCounsel(intelligenceCatalog, 24, 32)).toContain("Haiyang A. Li");
  });

  it("turns anticipated QI into an active twin issue when the MTD lands", () => {
    const serrato = cases.find((row) => row.number === 24)!;
    const before = deriveTwin(serrato, intelligenceCatalog, [], []);
    expect(before.open_issues.find((issue) => issue.id === "qualified_immunity")?.status).toBe("active");
    const hope = cases.find((row) => row.number === 28)!;
    const anticipated = deriveTwin(hope, intelligenceCatalog, [], []);
    expect(anticipated.open_issues.find((issue) => issue.id === "qualified_immunity")?.status).toBe("anticipated");
    const filing: LitigationEvent = {
      id: "test-mtd",
      type: "MOTION_FILED",
      at: "Sep. 21, 2026",
      matter: 28,
      summary: "Defendant files MTD invoking qualified immunity",
      issues: ["qualified_immunity"],
    };
    const afterMotion = deriveTwin(hope, intelligenceCatalog, [filing], []);
    expect(afterMotion.open_issues.find((issue) => issue.id === "qualified_immunity")?.status).toBe("active");
    const mutated = activateIssue(anticipated, "qualified_immunity", "Dkt. 17 MTD");
    expect(mutated.controlling_questions).toContain("qualified_immunity");
    expect(mutated.live_motions.some((motion) => motion.issues.includes("qualified_immunity"))).toBe(true);
  });

  it("keeps the Serrato CMC as a dependency until the MTD final order fires", () => {
    const waiting = resolveDeadlines(intelligenceCatalog, []);
    expect(waiting.every((clock) => clock.status === "waiting_on_trigger")).toBe(true);
    expect(waiting.map((clock) => clock.id)).toEqual(expect.arrayContaining(["m24-cmc-after-mtd", "m24-jcms", "m24-adr"]));
    const firedCatalog = applyOrderToDependencies(intelligenceCatalog, 24, "m24-dkt18-final", "2026-09-14");
    const fired = resolveRecipe(firedCatalog.dependencies[0]);
    const cmc = fired.find((clock) => clock.id === "m24-cmc-after-mtd");
    const jcms = fired.find((clock) => clock.id === "m24-jcms");
    expect(cmc?.status).toBe("fired");
    expect(cmc?.displayDate).toBe("Sep. 28, 2026");
    expect(jcms?.displayDate).toBe("Sep. 21, 2026");
    const continuance: LitigationEvent = {
      id: "dkt25",
      type: "ORDER_ENTERED",
      at: "Sep. 9, 2026",
      matter: 24,
      summary:
        "ORDER — Dkt. 25 continued the CMC to fourteen (14) days after the final order on Defendant's motion to dismiss (Dkt. 18).",
    };
    expect(resolveDeadlines(intelligenceCatalog, [continuance]).every((clock) => clock.status === "waiting_on_trigger")).toBe(true);
    const disposition: LitigationEvent = {
      id: "dkt18-final",
      type: "ORDER_ENTERED",
      at: "2026-09-14",
      matter: 24,
      summary: "Order granting in part and denying in part Dkt. 18",
      payload: { triggerId: "m24-dkt18-final" },
    };
    expect(resolveDeadlines(intelligenceCatalog, [disposition]).find((clock) => clock.id === "m24-cmc-after-mtd")?.displayDate).toBe(
      "Sep. 28, 2026",
    );
  });

  it("shockwaves a new QI opinion onto the matters that actually depend on that issue", () => {
    const report = shockwaveFromOpinion(
      {
        title: "Example v. County",
        court: "CA9",
        issues: ["qualified_immunity"],
        holdings: "Narrows the clearly-established-law inquiry.",
      },
      intelligenceCatalog,
    );
    const matters = report.hits.map((hit) => hit.matter);
    expect(matters).toEqual(expect.arrayContaining([24, 28]));
    expect(report.hits.find((hit) => hit.matter === 24)?.impact).toBe("HIGH");
  });

  it("diffs defense positions: new arguments, abandoned ones, and new authorities", () => {
    const diffs = diffsForMatter(intelligenceCatalog.arguments, 26);
    expect(diffs).toHaveLength(1);
    expect(diffs[0].added).toContain("fcra_icraa");
    expect(diffs[0].newAuthorities).toContain("lerma");
    const serrato = diffsForMatter(intelligenceCatalog.arguments, 24)[0];
    expect(serrato.added).toContain("first_amendment_retaliation");
    expect(diffArguments(intelligenceCatalog.arguments[0], intelligenceCatalog.arguments[1]).abandoned).toEqual([]);
  });

  it("flags factual contradictions with the sources that still support the proposition", () => {
    const hits = contradictionsForMatter(intelligenceCatalog, 24);
    expect(hits[0]?.id).toBe("serrato-thorough-review");
    expect(hits[0]?.sources.length).toBeGreaterThan(0);
    const next = flagContradiction(hits[0], "MTD p. 11");
    expect(next.contradicted_by).toContain("MTD p. 11");
  });

  it("publishes docket events on a bus so agents can subscribe without bloating sync", () => {
    resetEventBus();
    const seen: string[] = [];
    const stop = subscribe("MOTION_FILED", (event) => {
      seen.push(event.id);
    });
    publish({
      id: "bus-1",
      type: "MOTION_FILED",
      at: "2026-09-11",
      matter: 28,
      summary: "MTD",
    });
    publish({
      id: "bus-2",
      type: "ORDER_ENTERED",
      at: "2026-09-11",
      matter: 24,
      summary: "order",
    });
    expect(seen).toEqual(["bus-1"]);
    expect(publishedEvents()).toHaveLength(2);
    stop();
  });

  it("ranks systemic importance and simulates a Matter 24 MTD-survival domino", () => {
    const graph = buildKnowledgeGraph(cases, intelligenceCatalog);
    const ranking = systemicImportance(cases, graph, intelligenceCatalog);
    expect(ranking[0].matter).toBeGreaterThan(0);
    expect(ranking.find((row) => row.matter === 24)?.score).toBeGreaterThan(50);
    const domino = simulateDomino({ kind: "survives_mtd", matter: 24 }, graph, intelligenceCatalog);
    expect(domino.effects.some((effect) => [32, 33, 20, 1].includes(effect.matter))).toBe(true);
  });

  it("opens a war room when a Rule 12 motion hits a live matter", () => {
    const room = buildWarRoom(
      {
        id: "wr",
        type: "MOTION_FILED",
        at: "Aug. 26, 2026",
        matter: 24,
        docket: 18,
        summary: "Rule 12(b)(6) motion filed invoking qualified immunity",
        issues: ["qualified_immunity", "u_visa_certification"],
      },
      intelligenceCatalog,
    );
    expect(room?.immediate).toMatch(/Opposition clock/);
    expect(room?.crossMatters.length).toBeGreaterThan(0);
    expect(room?.sequence[0]).toMatch(/Read/);
  });

  it("uses RECAP as a cost gate: retrieve what is already free, skip low-value PACER buys", () => {
    const already = recapAdvice(intelligenceCatalog.recap.find((row) => row.id === "m24-dkt18-already")!);
    const skip = recapAdvice(intelligenceCatalog.recap.find((row) => row.id === "low-value-minutiae")!);
    const buy = recapAdvice(intelligenceCatalog.recap.find((row) => row.id === "m26-dkt12-reply-pdf")!);
    expect(already.action).toBe("retrieve");
    expect(already.reason).toMatch(/do not repurchase/i);
    expect(skip.action).toBe("skip");
    expect(buy.action).toBe("retrieve");
  });

  it("audits citations for existence, bindingness, and overstated parentheticals", () => {
    const lerma = intelligenceCatalog.authorities.find((row) => row.id === "lerma")!;
    const audit = auditCitation(lerma, intelligenceCatalog);
    expect(audit.exists).toBe(true);
    expect(audit.binding).toBe(false);
    expect(audit.parentheticalOverstates).toBe(true);
    expect(audit.notes.join(" ")).toMatch(/Fair Chance/);
  });

  it("fingerprints a filing against known defense patterns", () => {
    const profile = intelligenceCatalog.fingerprints.find((row) => row.id === "haiyang-li")!;
    const filing = intelligenceCatalog.arguments.find((row) => row.id === "m24-dkt18")!;
    const match = matchFingerprint(profile, filing);
    expect(match.score).toBeGreaterThan(50);
    expect(match.resembled).toEqual(expect.arrayContaining(["qualified_immunity"]));
  });

  it("classifies docket text and maps QI language onto the issue catalog", () => {
    expect(classifyDocketText("Defendant's Motion to Dismiss under Rule 12(b)(6)")).toBe("MOTION_FILED");
    expect(classifyDocketText("ORDER continuing the CMC")).toBe("ORDER_ENTERED");
    expect(issuesMentioned("qualified immunity and Monell policy", intelligenceCatalog)).toEqual(
      expect.arrayContaining(["qualified_immunity", "monell_policy"]),
    );
  });

  it("reports claim-element coverage without pretending the percentages are win rates", () => {
    const matrix = intelligenceCatalog.matrices.find((row) => row.claim_id === "m28-monell")!;
    const rico = weakestElement(matrix.elements);
    expect(rico?.id).toBe("m28-rico");
    expect(rico?.next_evidence).toMatch(/CDCR payment/);
    expect(claimCoverage(matrix)).toBeGreaterThan(0.5);
    expect(claimCoverage(matrix)).toBeLessThan(1);
  });

  it("assembles a command-center snapshot and an overnight brief", () => {
    const os = assembleIntelligence({ summaries, timeline: [], catalog: intelligenceCatalog, asOf: "Sep. 11, 2026" });
    expect(os.disclaimer).toMatch(/not the probability/);
    expect(os.twins.find((twin) => twin.matter === 28)?.controlling_questions).toEqual(
      expect.arrayContaining(["state_actor", "qualified_immunity"]),
    );
    const brief = overnightBrief({
      asOf: "Sep. 11, 2026",
      twins: os.twins,
      events: [
        {
          id: "n1",
          type: "MOTION_FILED",
          at: "Sep. 10, 2026",
          matter: 29,
          summary: "Accurate filed MTD.",
        },
      ],
      catalog: intelligenceCatalog,
    });
    expect(brief.highestPriority).toMatch(/Matter/);
    expect(brief.docketChanges[0]).toMatch(/Matter 29/);
    const center = commandCenter(24, os);
    expect(center.twin?.matter).toBe(24);
    expect(center.clocks.some((clock) => clock.id === "m24-cmc-after-mtd")).toBe(true);
    expect(recapAdvice({
      id: "prayer",
      label: "watched PDF",
      inRecap: false,
      prayerPending: true,
      strategicValue: "HIGH",
      why: "clock",
    }).action).toBe("wait");
  });
});

const SERRATO_DKT25 =
  "ORDER — Dkt. 25 in Newanforbi v. Serrato (4:26-cv-05953-ASK). Mag. Krishnan signed the Dkt. 22 stipulation. CMC continued from September 15, 2026 to fourteen (14) days after the final order on Defendant's motion to dismiss (Dkt. 18; hearing remains Sep. 30 per Dkt. 21).";

const SERRATO_DKT21 =
  "FILED — Clerk's Notice Resetting Hearing on Motion to Dismiss (Dkt. 21) in Newanforbi v. Serrato (4:26-cv-05953-ASK). The hearing on Defendant's Motion to Dismiss the FAC (Dkt. 18) is reset to September 30, 2026, 1:30 p.m.";

const VAN_DINE_MTD_BODY = `MOTION to Dismiss Plaintiff's Complaint

Defendants HOPE Psychotherapy, Inc. and Shannon Smith hereby move to dismiss under Fed. R. Civ. P. 12(b)(6).

Qualified immunity bars the individual-capacity claims because the rights were not clearly established under Harlow v. Fitzgerald.
HOPE is not a state actor under West v. Atkins, 487 U.S. 42 (1988).
Monell liability fails because there is no official policy or custom.
Claim preclusion and res judicata bar relitigation of the state-court action.
The RICO claim fails for lack of continuity and enterprise.
Defendants do not dispute that HOPE contracted with CDCR.`;

describe("docket text fires Serrato clocks and mutates the Matter 28 twin", () => {
  it("sets m24-dkt18-final from a merits order on Dkt. 18 without a pre-set triggerId", () => {
    const grant = eventFromNormalizedEntry(
      {
        matter: 24,
        description: "ORDER GRANTING IN PART AND DENYING IN PART Defendant's Motion to Dismiss (Dkt. 18)",
        date_filed: "2026-09-14",
        entry_number: 27,
        courtlistener_entry_id: 27001,
      },
      intelligenceCatalog,
    );
    expect(grant.type).toBe("ORDER_ENTERED");
    expect(grant.payload?.triggerId).toBe("m24-dkt18-final");
    expect(resolveDeadlines(intelligenceCatalog, [grant]).find((clock) => clock.id === "m24-cmc-after-mtd")?.displayDate).toBe(
      "Sep. 28, 2026",
    );

    const shortGrant = eventFromNormalizedEntry(
      {
        matter: 24,
        description: "ORDER GRANTING Dkt. 18",
        date_filed: "2026-09-14",
        entry_number: 27,
      },
      intelligenceCatalog,
    );
    expect(shortGrant.payload?.triggerId).toBe("m24-dkt18-final");

    const denied = eventFromNormalizedEntry(
      {
        matter: 24,
        description: "MINUTE ORDER: Dkt. 18 DENIED",
        date_filed: "2026-09-14",
        entry_number: 27,
      },
      intelligenceCatalog,
    );
    expect(denied.payload?.triggerId).toBe("m24-dkt18-final");
  });

  it("does not treat Dkt. 25, the Dkt. 21 hearing reset, or a grant of the continuance stipulation as the MTD order", () => {
    const noise = [
      SERRATO_DKT25,
      SERRATO_DKT21,
      "ORDER GRANTING stipulation to continue the hearing on Dkt. 18",
    ].map((description, index) =>
      eventFromNormalizedEntry(
        {
          matter: 24,
          description,
          date_filed: "2026-09-09",
          entry_number: index === 1 ? 21 : 25,
        },
        intelligenceCatalog,
      ),
    );
    expect(noise.every((event) => event.payload?.triggerId == null)).toBe(true);
    expect(resolveDeadlines(intelligenceCatalog, noise).every((clock) => clock.status === "waiting_on_trigger")).toBe(true);

    const liveRows = timeline.filter(
      (event) =>
        event.event.includes("Dkt. 25 in Newanforbi v. Serrato") ||
        event.event.includes("Clerk's Notice Resetting Hearing on Motion to Dismiss (Dkt. 21)"),
    );
    const fromTimeline = assembleIntelligence({
      summaries,
      timeline: liveRows,
      catalog: intelligenceCatalog,
    });
    expect(fromTimeline.clocks.filter((clock) => clock.matter === 24).every((clock) => clock.status === "waiting_on_trigger")).toBe(
      true,
    );
  });

  it("assembling the live portfolio leaves Serrato waiting and HOPE QI anticipated", () => {
    const os = assembleIntelligence({ summaries, catalog: intelligenceCatalog, asOf: "Sep. 11, 2026" });
    const serrato = os.clocks.filter((clock) => ["m24-cmc-after-mtd", "m24-jcms", "m24-adr"].includes(clock.id));
    expect(serrato.length).toBe(3);
    expect(serrato.every((clock) => clock.status === "waiting_on_trigger")).toBe(true);
    expect(os.twins.find((twin) => twin.matter === 28)?.open_issues.find((issue) => issue.id === "qualified_immunity")?.status).toBe(
      "anticipated",
    );
  });

  it("mutates Matter 28 from Van Dine MTD text without editing the catalog", () => {
    const filing = eventFromNormalizedEntry(
      {
        matter: 28,
        description: "MOTION to Dismiss",
        body: VAN_DINE_MTD_BODY,
        date_filed: "2026-09-21",
        entry_number: 15,
        courtlistener_entry_id: 15001,
      },
      intelligenceCatalog,
    );
    expect(filing.type).toBe("MOTION_FILED");
    expect(filing.issues).toEqual(
      expect.arrayContaining(["qualified_immunity", "state_actor", "monell_policy", "claim_preclusion", "rico_continuity"]),
    );
    expect(filing.payload?.authorities).toEqual(expect.arrayContaining(["west-atkins", "harlow"]));
    const admissions = filing.payload?.admissions as string[] | undefined;
    expect(admissions?.[0]).toMatch(/do not dispute that HOPE contracted/i);

    const preview = eventFromNormalizedEntry(
      {
        matter: 28,
        description: "Gmail: Van Dine previewed a Rule 12(b)(6) and asked to confer",
        date_filed: "2026-09-03",
      },
      intelligenceCatalog,
    );
    expect(preview.type).not.toBe("MOTION_FILED");

    const os = assembleIntelligence({
      summaries,
      timeline: [],
      catalog: intelligenceCatalog,
      events: [filing],
      asOf: "Sep. 21, 2026",
    });
    const twin = os.twins.find((row) => row.matter === 28);
    expect(twin?.open_issues.find((issue) => issue.id === "qualified_immunity")?.status).toBe("active");
    expect(twin?.live_motions.some((motion) => motion.status === "live" && motion.issues.includes("qualified_immunity"))).toBe(true);
    expect(twin?.live_motions.some((motion) => motion.status === "anticipated")).toBe(false);
    expect(os.clocks.some((clock) => clock.matter === 28 && /Opposition/.test(clock.label) && clock.status === "date_certain")).toBe(
      true,
    );
    expect(os.warRooms.some((room) => room.matter === 28)).toBe(true);
    const center = commandCenter(28, os);
    expect(center.diffs[0]?.prior).toMatch(/preview/i);
    expect(center.diffs[0]?.newAuthorities).toEqual(expect.arrayContaining(["west-atkins", "harlow"]));
    expect(center.diffs[0]?.factualAdmissions[0]).toMatch(/HOPE contracted/i);
  });

  it("court:sync classifier attaches the same triggerId and MTD extraction", () => {
    const order = emitFromNormalized({
      matter: 24,
      description: "ORDER GRANTING IN PART AND DENYING IN PART Defendant's Motion to Dismiss (Dkt. 18)",
      date_filed: "2026-09-14",
      entry_number: 27,
      courtlistener_entry_id: 27001,
    });
    expect(order.type).toBe("ORDER_ENTERED");
    expect(order.payload.triggerId).toBe("m24-dkt18-final");

    const motion = emitFromNormalized({
      matter: 28,
      description: "MOTION to Dismiss",
      body: VAN_DINE_MTD_BODY,
      date_filed: "2026-09-21",
      entry_number: 15,
      courtlistener_entry_id: 15001,
    });
    expect(motion.type).toBe("MOTION_FILED");
    expect(motion.issues).toContain("qualified_immunity");
    expect(motion.payload.authorities).toContain("west-atkins");
  });
});
