import { describe, expect, it } from "vitest";
import { budgetAllows, remainingFromUsage, readCourtListenerToken } from "../../scripts/courtlistener/client.mjs";
import { courtIdFromCourt, isFederalMatter } from "../../scripts/courtlistener/courts.mjs";
import {
  formatDocketNumber,
  officeVariants,
  parseFederalDocket,
} from "../../scripts/courtlistener/docket-number.mjs";
import {
  buildTimelineEvent,
  detectDeadlineCandidate,
  entryHash,
  formatTimelineDate,
  inferFactActor,
  inferFactType,
  normalizeDocketEntry,
} from "../../scripts/courtlistener/entries.mjs";
import { reconcileEntries } from "../../scripts/courtlistener/reconcile.mjs";
import {
  BOOTSTRAP_MATTERS,
  parseArgs,
  selectSyncTargets,
} from "../../scripts/courtlistener/sync-dockets.mjs";
import { resolveMatter } from "../../scripts/courtlistener/resolve-dockets.mjs";
import { extractDocketHints, webhookSyncPlan } from "../../scripts/courtlistener/webhook.mjs";
import apiUsageFixture from "./courtlistener/fixtures/api-usage.json";

describe("docket number + court binding", () => {
  it("strips judge initials and (PC) from PACER numbers", () => {
    expect(parseFederalDocket("3:26-cv-07504-LJC")).toEqual({
      office: "3",
      year: "26",
      nature: "cv",
      number: "07504",
    });
    expect(formatDocketNumber(parseFederalDocket("2:26-cv-00191-DJC-CSK (PC)"))).toBe("2:26-cv-00191");
  });

  it("tries the other N.D. Cal. office when the case was reassigned", () => {
    const parsed = parseFederalDocket("4:26-cv-09249-ASK");
    expect(officeVariants(parsed, "cand")).toEqual(["4:26-cv-09249", "3:26-cv-09249", "5:26-cv-09249"]);
  });

  it("maps portfolio court strings onto CourtListener ids", () => {
    expect(courtIdFromCourt("USDC N.D. Cal. (Oakland; formerly 3:26-cv-09249-ASK)")).toBe("cand");
    expect(courtIdFromCourt("USDC E.D. Cal. (Sacramento Div.)")).toBe("caed");
    expect(isFederalMatter({ type: "Federal", proceeding: "federal_civil" })).toBe(true);
    expect(isFederalMatter({ type: "State", proceeding: "state_civil" })).toBe(false);
  });
});

describe("resolveMatter", () => {
  it("does not rediscover a bound docket by caption", async function boundSkip() {
    const searches = [];
    const client = {
      searchDockets: async (query) => {
        searches.push(query);
        return [{ docket_id: 1, docket_absolute_url: "/docket/1/x/", court_id: "cand" }];
      },
    };
    const result = await resolveMatter(
      {
        number: 28,
        case_no: "3:26-cv-07504-LJC",
        court: "USDC N.D. Cal.",
        courtlistener: { court_id: "cand", docket_id: 73646240, docket_url: "/docket/73646240/ngehsi-newanforbi-v-smith/" },
      },
      client,
    );
    expect(result.status).toBe("bound");
    expect(searches).toEqual([]);
    expect(result.binding.docket_id).toBe(73646240);
  });

  it("retries the other office prefix instead of searching by caption", async function officeFallback() {
    const searched = [];
    const client = {
      searchDockets: async ({ docketNumber }) => {
        searched.push(docketNumber);
        if (docketNumber === "3:26-cv-09249") {
          return [
            {
              docket_id: 74725653,
              docket_absolute_url: "/docket/74725653/newanforbi-v-amazoncom-services-llc/",
              court_id: "cand",
            },
          ];
        }
        return [];
      },
    };
    const result = await resolveMatter(
      {
        number: 29,
        case_no: "4:26-cv-09249-ASK",
        court: "USDC N.D. Cal.",
      },
      client,
    );
    expect(searched[0]).toBe("4:26-cv-09249");
    expect(searched).toContain("3:26-cv-09249");
    expect(result.status).toBe("resolved");
    expect(result.binding.docket_id).toBe(74725653);
  });
});

describe("entry normalization and deadlines", () => {
  it("hashes stably so a second sync cannot duplicate the row", () => {
    const a = entryHash({
      docketId: 1,
      entryId: 99,
      entryNumber: 15,
      dateFiled: "2026-09-11",
      description: "MOTION TO DISMISS",
    });
    const b = entryHash({
      docketId: 1,
      entryId: 99,
      entryNumber: 15,
      dateFiled: "2026-09-11",
      description: "MOTION TO DISMISS",
    });
    expect(a).toBe(b);
    expect(a).toHaveLength(64);
  });

  it("formats portfolio timeline dates as Mon. D, YYYY", () => {
    expect(formatTimelineDate("2026-09-11")).toBe("Sep. 11, 2026");
    expect(formatTimelineDate("2026-06-02")).toBe("Jun. 2, 2026");
  });

  it("treats an MTD as an opposing filing, not a deadline", () => {
    const normalized = normalizeDocketEntry(
      {
        id: 99887766,
        entry_number: 15,
        date_filed: "2026-09-11",
        description: "MOTION TO DISMISS filed by Defendant Shannon Smith",
      },
      { matter: 28, docketId: 73646240, ingestedAt: "2026-09-11T08:00:00Z" },
    );
    expect(inferFactType(normalized.description)).toBe("filing");
    expect(inferFactActor(normalized.description)).toBe("opposing");
    expect(detectDeadlineCandidate(normalized.description, normalized.date_filed)).toBeNull();
    const event = buildTimelineEvent(normalized);
    expect(event.upcoming).toBe(false);
    expect(event.external.docket_entry_id).toBe(99887766);
    expect(event.event).toContain("Dkt. 15");
  });

  it("parks an amended-complaint clock in review, not on the timeline as upcoming", () => {
    const text = "ORDER. Plaintiff shall file an amended complaint within 21 days.";
    const candidate = detectDeadlineCandidate(text, "2026-09-11");
    expect(candidate).toMatchObject({
      candidate_type: "deadline",
      proposed_date: "2026-10-02",
      confidence: 0.7,
    });
  });
});

describe("reconcileEntries", () => {
  const mtd = normalizeDocketEntry(
    {
      id: 99887766,
      entry_number: 15,
      date_filed: "2026-09-11",
      description: "MOTION TO DISMISS filed by Defendant",
    },
    { matter: 28, docketId: 123, ingestedAt: "2026-09-11T08:00:00Z" },
  );
  const order = normalizeDocketEntry(
    {
      id: 17,
      entry_number: 17,
      date_filed: "2026-09-11",
      description: "ORDER. Plaintiff shall file an amended complaint within 21 days.",
    },
    { matter: 28, docketId: 123, ingestedAt: "2026-09-11T08:00:00Z" },
  );

  it("inserts a fact once and is a no-op the second time", () => {
    const first = reconcileEntries({ timeline: [], normalizedEntries: [mtd] });
    expect(first.stats.factsAdded).toBe(1);
    expect(first.timeline[0].upcoming).toBe(false);
    const second = reconcileEntries({
      timeline: first.timeline,
      ledger: first.ledger,
      review: first.review,
      normalizedEntries: [mtd],
    });
    expect(second.stats.skipped).toBe(1);
    expect(second.stats.factsAdded).toBe(0);
    expect(second.timeline).toHaveLength(1);
  });

  it("attaches provenance to an existing Dkt. N instead of duplicating it", () => {
    const timeline = [
      {
        date: "Sep. 3, 2026",
        event: "FILED — Dkt. 13 Proof of Service in Newanforbi v. Smith",
        matters: [28],
        type: "filing",
        upcoming: false,
      },
    ];
    const pos = normalizeDocketEntry(
      { id: 555, entry_number: 13, date_filed: "2026-09-03", description: "PROOF OF SERVICE" },
      { matter: 28, docketId: 123, ingestedAt: "2026-09-11T08:00:00Z" },
    );
    const result = reconcileEntries({ timeline, normalizedEntries: [pos] });
    expect(result.stats.factsAdded).toBe(0);
    expect(result.stats.provenanceAttached).toBe(1);
    expect(result.timeline).toHaveLength(1);
    expect(result.timeline[0].external.docket_entry_id).toBe(555);
    expect(result.timeline[0].event).toContain("Proof of Service");
  });

  it("does not attach Dkt. N provenance when another row only mentions that docket", () => {
    const timeline = [
      {
        date: "Aug. 26, 2026",
        event: "FILED — Dkt. 18 Motion to Dismiss FAC in Newanforbi v. Serrato",
        matters: [24],
        type: "filing",
        upcoming: false,
      },
      {
        date: "Sep. 30, 2026",
        event: "Hearing on Defendant Serrato's Motion to Dismiss FAC (Dkt. 18)",
        matters: [24],
        type: "hearing",
        upcoming: true,
      },
    ];
    const mtd = normalizeDocketEntry(
      { id: 1800, entry_number: 18, date_filed: "2026-08-26", description: "MOTION to Dismiss the FAC" },
      { matter: 24, docketId: 1, ingestedAt: "2026-09-11T08:00:00Z" },
    );
    const result = reconcileEntries({ timeline, normalizedEntries: [mtd] });
    expect(result.stats.factsAdded).toBe(0);
    expect(result.stats.provenanceAttached).toBe(1);
    expect(result.timeline[0].external.docket_entry_id).toBe(1800);
    expect(result.timeline[1].external).toBeUndefined();
  });

  it("parks an ambiguous same-date Dkt. N collision in review instead of guessing", () => {
    const timeline = [
      {
        date: "Aug. 26, 2026",
        event: "FILED — Dkt. 18 Motion to Dismiss FAC",
        matters: [24],
        type: "filing",
        upcoming: false,
      },
      {
        date: "Aug. 26, 2026",
        event: "SET — Dkt. 18 hearing on the motion to dismiss FAC",
        matters: [24],
        type: "hearing",
        upcoming: false,
      },
    ];
    const mtd = normalizeDocketEntry(
      { id: 1800, entry_number: 18, date_filed: "2026-08-26", description: "MOTION to Dismiss" },
      { matter: 24, docketId: 1, ingestedAt: "2026-09-11T08:00:00Z" },
    );
    const result = reconcileEntries({ timeline, normalizedEntries: [mtd] });
    expect(result.stats.factsAdded).toBe(0);
    expect(result.stats.provenanceAttached).toBe(0);
    expect(result.stats.ambiguousQueued).toBe(1);
    expect(result.timeline).toHaveLength(2);
    expect(result.timeline.every((event) => !event.external?.docket_entry_id)).toBe(true);
    expect(result.review.candidates[0]).toMatchObject({
      matter: 24,
      candidate_type: "ambiguous_timeline_match",
      trigger_entry: 18,
      status: "pending",
    });
  });

  it("never flips a deadline candidate onto upcoming: true", () => {
    const result = reconcileEntries({ timeline: [], normalizedEntries: [order] });
    expect(result.stats.factsAdded).toBe(1);
    expect(result.timeline[0].upcoming).toBe(false);
    expect(result.timeline[0].type).toBe("order");
    expect(result.review.candidates).toHaveLength(1);
    expect(result.review.candidates[0]).toMatchObject({
      matter: 28,
      candidate_type: "deadline",
      trigger_entry: 17,
      proposed_date: "2026-10-02",
      status: "pending",
    });
    expect(result.timeline.some((event) => event.upcoming === true)).toBe(false);
  });
});

describe("webhook is a hint", () => {
  const body = {
    webhook: { event_type: 1 },
    payload: {
      docket: 73646240,
      results: [{ id: 99, docket: 73646240, description: "MOTION TO DISMISS" }],
    },
  };

  it("does not treat docket-entry result ids as docket ids", () => {
    expect(extractDocketHints(body)).not.toContain(99);
  });

  it("extracts docket ids and refuses to apply payload entries", () => {
    expect(extractDocketHints(body)).toEqual([73646240]);
    const plan = webhookSyncPlan(body, {
      idempotencyKey: "abc",
      sourceIp: "34.210.230.218",
    });
    expect(plan.action).toBe("requery");
    expect(plan.applyPayloadEntries).toBe(false);
    expect(plan.docketIds).toEqual([73646240]);
  });

  it("rejects posts that are not from CourtListener's published IPs", () => {
    const plan = webhookSyncPlan(body, { sourceIp: "1.2.3.4" });
    expect(plan.action).toBe("reject");
    expect(plan.applyPayloadEntries).toBe(false);
  });
});

describe("token leakage and budget", () => {
  it("refuses a VITE_* CourtListener token", () => {
    expect(() => readCourtListenerToken({ VITE_COURTLISTENER_TOKEN: "secret" })).toThrow(/VITE_/);
  });

  it("accepts COURTLISTENER_TOKEN and the COURTLISTENER_API_TOKEN alias", () => {
    expect(readCourtListenerToken({ COURTLISTENER_TOKEN: "abc" })).toBe("abc");
    expect(readCourtListenerToken({ COURTLISTENER_API_TOKEN: "alias" })).toBe("alias");
    expect(readCourtListenerToken({ COURTLISTENER_TOKEN: "primary", COURTLISTENER_API_TOKEN: "alias" })).toBe(
      "primary",
    );
  });

  it("parses the documented /api-usage/ current_usage rows", () => {
    const remaining = remainingFromUsage(apiUsageFixture);
    expect(remaining.unknown).toBe(false);
    expect(remaining.daily).toBe(62);
    expect(remaining.hourly).toBe(32);
    expect(remaining.minute).toBe(3);
    expect(budgetAllows(apiUsageFixture).ok).toBe(true);
  });

  it("fails closed when the usage body is not the documented shape", () => {
    expect(budgetAllows({ weird: true }).ok).toBe(false);
    expect(budgetAllows({ weird: true }).reason).toBe("usage_shape_unknown");
    expect(budgetAllows({ daily_remaining: 2 }).ok).toBe(false);
    expect(budgetAllows({ daily_remaining: 40 }).ok).toBe(true);
    expect(remainingFromUsage({ daily_limit: 500, daily_used: 10 }).daily).toBe(490);
  });
});

describe("sync target selection", () => {
  const matters = [
    { number: 1, type: "Federal", proceeding: "federal_civil", lifecycle: "dismissed", courtlistener: { docket_id: 1 } },
    { number: 24, type: "Federal", proceeding: "federal_civil", lifecycle: "active", courtlistener: { docket_id: 24 } },
    { number: 28, type: "Federal", proceeding: "federal_civil", lifecycle: "active", courtlistener: { docket_id: 28 } },
    { number: 7, type: "Federal", proceeding: "federal_civil", lifecycle: "dismissed", courtlistener: { docket_id: 7 } },
  ];

  it("refuses a first sync of every bound docket when cursors are empty", () => {
    expect(() => selectSyncTargets(matters, {}, { matters: {} })).toThrow(/Refusing a full historical backfill/);
  });

  it("bootstraps only the live seven", () => {
    expect(BOOTSTRAP_MATTERS).toEqual([24, 25, 26, 28, 29, 32, 33]);
    expect(selectSyncTargets(matters, { bootstrap: true }).map((row) => row.number)).toEqual([24, 28]);
  });

  it("parses --bootstrap --since and --active-only", () => {
    expect(parseArgs(["--bootstrap", "--since", "2026-07-01", "--dry-run"])).toMatchObject({
      bootstrap: true,
      since: "2026-07-01",
      dryRun: true,
    });
    expect(parseArgs(["--active-only"]).activeOnly).toBe(true);
    expect(() => parseArgs(["--since", "07/01/2026"])).toThrow(/YYYY-MM-DD/);
  });
});
