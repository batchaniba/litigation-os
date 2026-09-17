// Token auth + scope resolution for the litigation-doc-api Worker.
//
// The read surface shipped open (no auth). This adds *scoped bearer tokens*
// without breaking that: tokens live only as SHA-256 hashes inside the
// `API_KEYS` Worker secret, never in this repo. The secret is a JSON map of
//
//     { "<sha256-hex-of-token>": { "name": "cursor", "scope": "rw" }, ... }
//
// so the plaintext tokens exist only where they were minted. Scope is "r"
// (read) or "rw" (read + write); "rw" implies "r".
//
// Rollout is fail-safe in both directions:
//   * API_KEYS unset  -> reads stay OPEN (unchanged behavior); writes are
//                        hard-refused (503 auth_not_configured). You cannot
//                        accidentally get a writable-but-unauthenticated API.
//   * API_KEYS set     -> writes require an "rw" token. Reads require any
//                        valid token UNLESS PUBLIC_READ === "true", which
//                        keeps reads open while gating writes (recommended
//                        first step, so existing read clients don't break).
//
// No keys, tokens, or secrets live in this file — only the logic that checks
// a hash against the injected secret.

import { HttpError } from "./data.mjs";

export async function sha256Hex(input) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(String(input)));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function bearer(request) {
  const a = request.headers.get("authorization") || "";
  const m = a.match(/^Bearer\s+(.+)$/i);
  return m ? m[1].trim() : null;
}

function parseKeys(raw) {
  try {
    const o = JSON.parse(raw);
    return o && typeof o === "object" ? o : {};
  } catch {
    return {};
  }
}

// Resolve what the caller is allowed to do. Never throws — callers gate with
// requireRead / requireWrite so each surface returns its own error shape.
export async function resolveAccess(request, env) {
  const token = bearer(request);
  const configured = !!env.API_KEYS;
  let scope = null; // null | "r" | "rw"
  let actor = null;

  if (configured && token) {
    const rec = parseKeys(env.API_KEYS)[await sha256Hex(token)];
    if (rec) {
      scope = rec.scope === "rw" ? "rw" : "r";
      actor = typeof rec.name === "string" && rec.name ? rec.name : "key";
    }
  }

  const publicRead = configured ? env.PUBLIC_READ === "true" : true;
  return {
    configured,
    hasToken: !!token,
    scope,
    actor: actor ?? (token ? "unknown-token" : "anon"),
    canRead: scope !== null || publicRead,
    canWrite: scope === "rw",
  };
}

export function requireRead(access) {
  if (!access.canRead) throw new HttpError(401, { error: "unauthorized" });
}

export function requireWrite(access) {
  if (!access.configured) throw new HttpError(503, { error: "auth_not_configured" });
  if (!access.canWrite)
    throw new HttpError(access.hasToken ? 403 : 401, {
      error: access.hasToken ? "forbidden" : "unauthorized",
    });
}
