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
  recapPlainText,
} from "../../scripts/courtlistener/entries.mjs";
import { reconcileEntries } from "../../scripts/courtlistener/reconcile.mjs";
import { resolveMatter } from "../../scripts/courtlistener/resolve-dockets.mjs";
import { extractDocketHints, webhookSyncPlan } from "../../scripts/courtlistener/webhook.mjs";

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

  it("captures RECAP plain_text on the normalized entry without hashing it", () => {
    const normalized = normalizeDocketEntry(
      {
        id: 42,
        entry_number: 18,
        date_filed: "2026-08-26",
        description: "MOTION to Dismiss",
        recap_documents: [{ id: 9, plain_text: "  Defendants move to dismiss. Qualified immunity.  " }],
      },
      { matter: 24, docketId: 1, ingestedAt: "2026-08-26T12:00:00Z" },
    );
    expect(normalized.body).toBe("Defendants move to dismiss. Qualified immunity.");
    expect(recapPlainText({ recap_documents: [{ ocr_text: "OCR body" }] })).toBe("OCR body");
    const withoutText = normalizeDocketEntry(
      { id: 42, entry_number: 18, date_filed: "2026-08-26", description: "MOTION to Dismiss" },
      { matter: 24, docketId: 1, ingestedAt: "2026-08-26T12:00:00Z" },
    );
    expect(withoutText.hash).toBe(normalized.hash);
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

  it("reads remaining quota instead of hard-coding 125/day", () => {
    expect(remainingFromUsage({ daily_limit: 500, daily_used: 10 }).daily).toBe(490);
    expect(budgetAllows({ daily_remaining: 2 }).ok).toBe(false);
    expect(budgetAllows({ daily_remaining: 40 }).ok).toBe(true);
    expect(budgetAllows({ weird: true }).ok).toBe(true);
  });
});
