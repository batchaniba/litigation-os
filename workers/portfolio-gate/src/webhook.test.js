import { describe, expect, it } from "vitest";
import { handleWebhook } from "./handler.mjs";
import { parseSignatureHeader, verifyGitHubSignature } from "./webhook.mjs";

const SECRET = "test-webhook-secret";

async function sign(body, secret = SECRET) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(body));
  const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return `sha256=${hex}`;
}

describe("verifyGitHubSignature", () => {
  it("accepts a matching X-Hub-Signature-256", async () => {
    const body = '{"zen":"ok"}';
    expect(await verifyGitHubSignature(body, await sign(body), SECRET)).toBe(true);
  });

  it("rejects a mismatch, missing header, or missing secret (fail-closed)", async () => {
    const body = '{"zen":"ok"}';
    const good = await sign(body);
    expect(await verifyGitHubSignature(body, good, "other-secret")).toBe(false);
    expect(await verifyGitHubSignature(body, "sha256=deadbeef", SECRET)).toBe(false);
    expect(await verifyGitHubSignature(body, null, SECRET)).toBe(false);
    expect(await verifyGitHubSignature(body, good, "")).toBe(false);
    expect(await verifyGitHubSignature(body, good, undefined)).toBe(false);
  });

  it("parses only sha256= hex headers", () => {
    expect(parseSignatureHeader("sha256=abc123")).toBe("abc123");
    expect(parseSignatureHeader("sha1=abc123")).toBeNull();
    expect(parseSignatureHeader("sha256=")).toBeNull();
  });
});

describe("handleWebhook fail-closed auth", () => {
  it("returns 401 and does not start a run when the signature is invalid", async () => {
    const waited = [];
    const res = await handleWebhook({
      rawBody: JSON.stringify({
        action: "opened",
        repository: { full_name: "newanforbi/interactive-litigation-portfolio" },
        pull_request: {
          number: 1,
          base: { ref: "main" },
          head: {
            sha: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            repo: { full_name: "newanforbi/interactive-litigation-portfolio" },
          },
        },
      }),
      signatureHeader: "sha256=00",
      eventName: "pull_request",
      env: { GITHUB_WEBHOOK_SECRET: SECRET, GITHUB_REPO: "newanforbi/interactive-litigation-portfolio" },
      ctx: { waitUntil: (p) => waited.push(p) },
    });
    expect(res.status).toBe(401);
    expect(waited).toEqual([]);
    expect(await res.json()).toMatchObject({ ok: false, error: "invalid signature" });
  });
});
