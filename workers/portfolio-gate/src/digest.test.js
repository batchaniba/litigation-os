import { describe, expect, it, vi } from "vitest";
import {
  buildDigest,
  clockRows,
  composeDigest,
  deliverDigest,
  loadMainClocks,
  pacificDay,
} from "./digest.mjs";

const SOURCE = { sha: "b16c3ef83479086daca00565202df2c0f32bfe44", committedAt: "2026-10-03T19:03:48-07:00" };

function rows() {
  return [
    ...clockRows(28, [
      { id: "28-a", date: "2026-10-01", status: "open", actor: "you", title: "FILE ADR Certification" },
      { id: "28-b", date: "2026-10-13", status: "open", actor: "opposing", title: "Reply deadline on Dkt. 15" },
      { id: "28-c", date: "2026-10-05", status: "satisfied", actor: "you", title: "Opposition to Dkt. 15" },
    ]),
    ...clockRows(29, {
      clocks: [{ id: "29-a", date: "2026-10-13", status: "open", actor: "you", title: "Opposition due on Dkt. 19" }],
    }),
    ...clockRows(26, [{ id: "26-a", date: "2026-10-07", status: "vacated", actor: "you", title: "HEARING" }]),
    ...clockRows(25, [{ id: "25-a", date: "2026-10-29", status: "contingent", actor: "you", title: "FedEx responses" }]),
    ...clockRows(27, [{ id: "27-a", date: "2026-10-09", status: "open", actor: "you", title: "secret terms", private: true }]),
    ...clockRows(1, [{ id: "1-a", date: "2026-11-01", status: "open", actor: "you", title: "CCP 335.1 SOL backstop" }]),
    ...clockRows(30, [{ id: "30-a", date: null, status: "open", actor: "you", title: "undated" }]),
  ];
}

describe("buildDigest", () => {
  it("lists every live clock in the window, past-due open ones, and skips closed ones", () => {
    const d = buildDigest({ rows: rows(), today: "2026-10-05", weekday: "Tue", source: SOURCE });
    expect(d.needs_disposition.map((r) => r.id)).toEqual(["28-a"]);
    // Both Oct. 13 deadlines appear: the old digest showed one next_clock per matter.
    expect(d.clocks.map((r) => r.id)).toEqual(["27-a", "28-b", "29-a"]);
    expect(d.text).toContain("main @ b16c3ef");
    expect(d.text).toContain("1 need disposition · 3 in next 14 days");
    expect(d.text).toContain("Oct 13 (8d) · M29 · YOU · Opposition due on Dkt. 19");
    expect(d.text).not.toContain("HEARING");
    expect(d.text).toContain("1 live clock(s) have no date.");
  });

  it("masks private titles in both the text and the rows", () => {
    const d = buildDigest({ rows: rows(), today: "2026-10-05", weekday: "Tue", source: SOURCE });
    expect(d.text).not.toContain("secret terms");
    expect(d.text).toContain("M27 · YOU · Private clock — see the repo");
    expect(d.clocks.find((r) => r.id === "27-a").title).toBeNull();
  });

  it("adds a 60-day horizon on Mondays, including dismissed-matter SOL backstops", () => {
    const d = buildDigest({ rows: rows(), today: "2026-10-05", weekday: "Mon", source: SOURCE });
    expect(d.horizon.map((r) => r.id)).toEqual(["25-a", "1-a"]);
    expect(d.text).toContain("(contingent) FedEx responses");
    expect(buildDigest({ rows: rows(), today: "2026-10-05", weekday: "Tue", source: SOURCE }).horizon).toEqual([]);
  });

  it("still sends a message when nothing is due", () => {
    const d = buildDigest({ rows: [], today: "2026-10-05", weekday: "Tue", source: SOURCE });
    expect(d.text).toContain("Nothing dated in the window.");
  });
});

describe("pacificDay", () => {
  it("uses Pacific time, not UTC", () => {
    expect(pacificDay(new Date("2026-10-06T03:00:00Z"))).toEqual({ date: "2026-10-05", weekday: "Mon" });
  });
});

function fakeGithub(files) {
  return {
    getBranchHead: vi.fn(async () => ({ sha: SOURCE.sha, committedAt: SOURCE.committedAt })),
    getTree: vi.fn(async () => Object.keys(files).map((path) => ({ path, type: "blob" }))),
    getFileText: vi.fn(async (path) => {
      if (!(path in files)) throw new Error(`404 ${path}`);
      return files[path];
    }),
  };
}

describe("loadMainClocks / composeDigest", () => {
  it("reads every matters/NN/clocks.json at the head of main", async () => {
    const gh = fakeGithub({
      "internal/src/data/matters/28/clocks.json": JSON.stringify([{ date: "2026-10-13", status: "open", title: "x" }]),
      "internal/src/data/matters/29/clocks.json": JSON.stringify([{ date: "2026-10-13", status: "open", title: "y" }]),
      "internal/src/data/matters/29/matter.json": "{}",
      "internal/src/data/index/matters.json": JSON.stringify({ matters: [{ number: 29, caption: "v. Amazon" }] }),
    });
    const loaded = await loadMainClocks(gh);
    expect(loaded.files).toBe(2);
    expect(loaded.rows.map((r) => r.matter)).toEqual([28, 29]);
    expect(loaded.captions[29]).toBe("v. Amazon");
  });

  it("sends a failure notice instead of throwing when main cannot be read", async () => {
    const gh = fakeGithub({});
    gh.getBranchHead = vi.fn(async () => {
      throw new Error("GitHub GET /repos/x/commits/main → 401");
    });
    const d = await composeDigest({ github: gh, now: new Date("2026-10-05T15:08:00Z") });
    expect(d.type).toBe("deadline_digest_error");
    expect(d.text).toContain("Today's deadlines were NOT checked.");
  });

  it("fails loudly on a malformed clocks.json instead of skipping that matter", async () => {
    const gh = fakeGithub({ "internal/src/data/matters/28/clocks.json": "{not json" });
    const d = await composeDigest({ github: gh, now: new Date("2026-10-05T15:08:00Z") });
    expect(d.type).toBe("deadline_digest_error");
    expect(d.error).toContain("28/clocks.json");
  });
});

describe("deliverDigest", () => {
  it("posts JSON to ALERT_WEBHOOK", async () => {
    const fetchImpl = vi.fn(async () => new Response("ok"));
    const r = await deliverDigest({ ALERT_WEBHOOK: "https://hook.example/x" }, { text: "hi" }, fetchImpl);
    expect(r.delivered).toBe(true);
    expect(JSON.parse(fetchImpl.mock.calls[0][1].body)).toEqual({ text: "hi" });
  });

  it("reports when no webhook is configured", async () => {
    const log = vi.spyOn(console, "log").mockImplementation(() => {});
    const r = await deliverDigest({}, { text: "hi" });
    expect(r).toMatchObject({ delivered: false, reason: "ALERT_WEBHOOK unset" });
    log.mockRestore();
  });
});
