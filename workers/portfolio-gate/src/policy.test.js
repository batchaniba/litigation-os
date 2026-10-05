import { describe, expect, it } from "vitest";
import { handleWebhook } from "./handler.mjs";
import { CHECK_NAME } from "./constants.mjs";
import { decideWebhookAction } from "./policy.mjs";

const REPO = "newanforbi/interactive-litigation-portfolio";
const SHA = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
const PREV = "cccccccccccccccccccccccccccccccccccccccc";

function prPayload({ action = "opened", base = "main", headRepo = REPO, sha = SHA, before } = {}) {
  return {
    action,
    number: 42,
    before,
    repository: { full_name: REPO },
    installation: { id: 99 },
    pull_request: {
      number: 42,
      base: { ref: base },
      head: { sha, repo: { full_name: headRepo } },
    },
  };
}

describe("decideWebhookAction — main-only PRs", () => {
  it("runs opened/synchronize/reopened PRs targeting main", () => {
    for (const action of ["opened", "synchronize", "reopened"]) {
      const decision = decideWebhookAction("pull_request", prPayload({ action, before: PREV }));
      expect(decision.action).toBe("run");
      expect(decision.job.sha).toBe(SHA);
      expect(decision.job.prNumber).toBe(42);
    }
  });

  it("is a no-op when the PR base is not main", () => {
    const decision = decideWebhookAction("pull_request", prPayload({ base: "develop" }));
    expect(decision.action).toBe("ignore");
    expect(decision.reason).toMatch(/base is not main/);
  });

  it("ignores other pull_request actions and other events", () => {
    expect(decideWebhookAction("pull_request", prPayload({ action: "closed" })).action).toBe(
      "ignore",
    );
    expect(decideWebhookAction("push", { repository: { full_name: REPO } }).action).toBe("ignore");
    expect(decideWebhookAction("ping", {}).action).toBe("pong");
  });

  it("refuses fork heads (fail, do not start a clone)", () => {
    const decision = decideWebhookAction(
      "pull_request",
      prPayload({ headRepo: "someone/fork" }),
    );
    expect(decision.action).toBe("fail");
    expect(decision.reason).toMatch(/fork/);
    expect(decision.job.sha).toBe(SHA);
  });

  it("records the previous SHA on synchronize so older runs can be cancelled", () => {
    const decision = decideWebhookAction(
      "pull_request",
      prPayload({ action: "synchronize", before: PREV }),
    );
    expect(decision.job.beforeSha).toBe(PREV);
  });

  it("handles check_run rerequest only for portfolio-gate on a main PR", () => {
    const ok = decideWebhookAction("check_run", {
      action: "rerequested",
      repository: { full_name: REPO },
      check_run: {
        name: CHECK_NAME,
        head_sha: SHA,
        pull_requests: [{ number: 7, base: { ref: "main" } }],
      },
    });
    expect(ok.action).toBe("run");
    expect(ok.job.sha).toBe(SHA);

    const otherBase = decideWebhookAction("check_run", {
      action: "rerequested",
      repository: { full_name: REPO },
      check_run: {
        name: CHECK_NAME,
        head_sha: SHA,
        pull_requests: [{ number: 7, base: { ref: "develop" } }],
      },
    });
    expect(otherBase.action).toBe("ignore");

    const otherName = decideWebhookAction("check_run", {
      action: "rerequested",
      repository: { full_name: REPO },
      check_run: { name: "something-else", head_sha: SHA, pull_requests: [] },
    });
    expect(otherName.action).toBe("ignore");
  });
});

describe("handleWebhook — PR not targeting main is a no-op", () => {
  it("returns 200 ignored and does not queue a container", async () => {
    const body = JSON.stringify(prPayload({ base: "feature" }));
    const secret = "s";
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign"],
    );
    const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(body));
    const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
    const queued = [];
    const res = await handleWebhook({
      rawBody: body,
      signatureHeader: `sha256=${hex}`,
      eventName: "pull_request",
      env: { GITHUB_WEBHOOK_SECRET: secret, GITHUB_REPO: REPO },
      enqueue: async (j) => { queued.push(j); },
    });
    expect(res.status).toBe(200);
    expect(queued).toEqual([]);
    expect(await res.json()).toMatchObject({ ok: true, ignored: true });
  });
});

async function signed(body, secret) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(body));
  return `sha256=${[...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("")}`;
}

describe("handleWebhook — queues instead of running under waitUntil", () => {
  it("queues a PR to main with the timeout and answers 202", async () => {
    const body = JSON.stringify(prPayload());
    const queued = [];
    const res = await handleWebhook({
      rawBody: body,
      signatureHeader: await signed(body, "s"),
      eventName: "pull_request",
      env: { GITHUB_WEBHOOK_SECRET: "s", GITHUB_REPO: REPO, GATE_TIMEOUT_MS: "720000" },
      enqueue: async (j) => {
        queued.push(j);
      },
    });
    expect(res.status).toBe(202);
    expect(queued).toHaveLength(1);
    expect(queued[0]).toMatchObject({ sha: SHA, timeoutMs: 720000 });
    expect(queued[0].refusal).toBeUndefined();
  });

  it("queues a fork PR as a refusal so it still gets a failing check", async () => {
    const body = JSON.stringify(prPayload({ headRepo: "someone/fork" }));
    const queued = [];
    const res = await handleWebhook({
      rawBody: body,
      signatureHeader: await signed(body, "s"),
      eventName: "pull_request",
      env: { GITHUB_WEBHOOK_SECRET: "s", GITHUB_REPO: REPO },
      enqueue: async (j) => {
        queued.push(j);
      },
    });
    expect(res.status).toBe(202);
    expect(queued[0].refusal).toBeTruthy();
  });

  it("answers 500 when the job cannot be queued", async () => {
    const body = JSON.stringify(prPayload());
    const res = await handleWebhook({
      rawBody: body,
      signatureHeader: await signed(body, "s"),
      eventName: "pull_request",
      env: { GITHUB_WEBHOOK_SECRET: "s", GITHUB_REPO: REPO },
      enqueue: async () => {
        throw new Error("durable object unavailable");
      },
    });
    expect(res.status).toBe(500);
  });
});
