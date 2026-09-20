// GitHub App authentication + Checks API. Secrets stay on the Worker
// (wrangler secret). The container receives only a short-lived installation
// token for `git fetch` of the installation repo.

import {
  CHECK_NAME,
  GITHUB_API,
  GITHUB_API_VERSION,
  UA,
} from "./constants.mjs";

function concatBytes(...parts) {
  const len = parts.reduce((n, p) => n + p.length, 0);
  const out = new Uint8Array(len);
  let offset = 0;
  for (const part of parts) {
    out.set(part, offset);
    offset += part.length;
  }
  return out;
}

function derLength(n) {
  if (n < 128) return Uint8Array.of(n);
  if (n < 256) return Uint8Array.of(0x81, n);
  if (n < 65536) return Uint8Array.of(0x82, (n >> 8) & 0xff, n & 0xff);
  throw new Error("DER length too large");
}

function tlv(tag, content) {
  return concatBytes(Uint8Array.of(tag), derLength(content.length), content);
}

// rsaEncryption AlgorithmIdentifier (RFC 8017 Appendix A.1).
const RSA_ALG_ID = Uint8Array.from([
  0x30, 0x0d, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86, 0xf7, 0x0d, 0x01, 0x01, 0x01, 0x05,
  0x00,
]);

export function pkcs1DerToPkcs8Der(pkcs1) {
  const version = Uint8Array.from([0x02, 0x01, 0x00]);
  return tlv(0x30, concatBytes(version, RSA_ALG_ID, tlv(0x04, pkcs1)));
}

export function pemToPkcs8Der(pem) {
  const match = /-----BEGIN ([A-Z ]+)-----([\s\S]+?)-----END \1-----/.exec(String(pem || ""));
  if (!match) throw new Error("GITHUB_APP_PRIVATE_KEY is not a PEM private key");
  const label = match[1];
  const der = Uint8Array.from(atob(match[2].replace(/\s+/g, "")), (c) => c.charCodeAt(0));
  if (label === "PRIVATE KEY") return der;
  if (label === "RSA PRIVATE KEY") return pkcs1DerToPkcs8Der(der);
  throw new Error(`unsupported PEM label: ${label}`);
}

export function base64UrlEncode(data) {
  const bytes = typeof data === "string" ? new TextEncoder().encode(data) : new Uint8Array(data);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

export async function createAppJwt({
  appId,
  privateKeyPem,
  nowSec = Math.floor(Date.now() / 1000),
}) {
  const id = String(appId || "").trim();
  if (!id) throw new Error("GITHUB_APP_ID is not set");
  const header = base64UrlEncode(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const payload = base64UrlEncode(
    JSON.stringify({
      iat: nowSec - 60,
      exp: nowSec + 540,
      iss: /^\d+$/.test(id) ? Number(id) : id,
    }),
  );
  const key = await crypto.subtle.importKey(
    "pkcs8",
    pemToPkcs8Der(privateKeyPem),
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign(
    "RSASSA-PKCS1-v1_5",
    key,
    new TextEncoder().encode(`${header}.${payload}`),
  );
  return `${header}.${payload}.${base64UrlEncode(sig)}`;
}

function apiHeaders(token, extra = {}) {
  return {
    accept: "application/vnd.github+json",
    authorization: `Bearer ${token}`,
    "user-agent": UA,
    "x-github-api-version": GITHUB_API_VERSION,
    ...extra,
  };
}

export async function githubRequest(path, { token, method = "GET", body } = {}) {
  const res = await fetch(`${GITHUB_API}${path}`, {
    method,
    headers: apiHeaders(token, body ? { "content-type": "application/json" } : {}),
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = null;
  }
  if (!res.ok) {
    const err = new Error(`GitHub ${method} ${path} → ${res.status}`);
    err.status = res.status;
    err.detail = (json && (json.message || json.error)) || text.slice(0, 240);
    throw err;
  }
  return json;
}

export async function getInstallationToken(env, installationId) {
  const id = installationId || env.GITHUB_APP_INSTALLATION_ID;
  if (!id) throw new Error("GitHub App installation id is missing");
  const jwt = await createAppJwt({
    appId: env.GITHUB_APP_ID,
    privateKeyPem: env.GITHUB_APP_PRIVATE_KEY,
  });
  const data = await githubRequest(`/app/installations/${id}/access_tokens`, {
    token: jwt,
    method: "POST",
  });
  if (!data?.token) throw new Error("GitHub App installation token missing from response");
  return data.token;
}

export function createGitHubClient({ token, repo }) {
  const [owner, name] = String(repo).split("/");
  if (!owner || !name) throw new Error("GITHUB_REPO must be owner/name");

  return {
    async createCheckRun({ sha, title, summary, status = "in_progress" }) {
      return githubRequest(`/repos/${owner}/${name}/check-runs`, {
        token,
        method: "POST",
        body: {
          name: CHECK_NAME,
          head_sha: sha,
          status,
          started_at: new Date().toISOString(),
          output: { title: title || CHECK_NAME, summary: summary || `${CHECK_NAME} started` },
        },
      });
    },

    async completeCheckRun({ id, conclusion, output }) {
      return githubRequest(`/repos/${owner}/${name}/check-runs/${id}`, {
        token,
        method: "PATCH",
        body: {
          status: "completed",
          conclusion,
          completed_at: new Date().toISOString(),
          output,
        },
      });
    },

    async cancelPendingChecks(sha, summary) {
      if (!sha) return [];
      const data = await githubRequest(
        `/repos/${owner}/${name}/commits/${sha}/check-runs?check_name=${encodeURIComponent(CHECK_NAME)}&per_page=20`,
        { token },
      );
      const runs = Array.isArray(data?.check_runs) ? data.check_runs : [];
      const cancelled = [];
      for (const run of runs) {
        if (run.name !== CHECK_NAME) continue;
        if (run.status !== "queued" && run.status !== "in_progress") continue;
        await githubRequest(`/repos/${owner}/${name}/check-runs/${run.id}`, {
          token,
          method: "PATCH",
          body: {
            status: "completed",
            conclusion: "cancelled",
            completed_at: new Date().toISOString(),
            output: {
              title: `${CHECK_NAME} cancelled`,
              summary: summary || "superseded by a newer push",
            },
          },
        });
        cancelled.push(run.id);
      }
      return cancelled;
    },
  };
}
