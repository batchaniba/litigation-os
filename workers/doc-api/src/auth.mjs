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

import { HttpError, pathsForSha } from "./data.mjs";
import { verifyAccessToken } from "./oauth.mjs";

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
    } else {
      // OAuth access tokens (e.g. ChatGPT native MCP): same scope model —
      // "write" in the granted scopes means rw. Only active while API_KEYS
      // is configured (no writable-but-unauthenticated API).
      const grant = await verifyAccessToken(env, token);
      if (grant) {
        scope = grant.scope.split(/\s+/).includes("write") ? "rw" : "r";
        actor = `oauth:${grant.label}`;
      }
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

// --- Confidential files ------------------------------------------------------
// "Undo everything except for file marked Confidential": reads are open to
// anonymous callers for every document EXCEPT files marked Confidential.
// A path counts as Confidential when it belongs to a confidential production
// (the HOPE Bates set, filed under "HOPE Discovery") or its filename says so
// (e.g. "Confidential Settlement Agreement ..."). Token holders (any scope,
// API key or OAuth) bypass this gate — it only affects anonymous reads.
// Writes are untouched: they still require an "rw" token.
//
// PUBLIC_READ=false remains the global panic button: when set, every read
// needs a token again, exactly like the 2026-10-04 lockdown.

export function isConfidentialPath(path) {
  let p = String(path ?? "");
  try {
    p = decodeURIComponent(p);
  } catch {
    // keep the raw form
  }
  // "HOPE Discovery", "hope-discovery", "hope_discovery" — separator varies
  // across the matter-05 and matter-28 filings of the same Bates set.
  return /hope[\s_-]*discovery/i.test(p) || /confidential/i.test(p);
}

// True when the operator has pulled the panic button: all reads need a token.
export function readLockdown(env) {
  return !!env.API_KEYS && env.PUBLIC_READ === "false";
}

// Throw HttpError(401) unless this document may be served to this caller.
// `ref` is { sha } and/or { path }; access comes from resolveAccess().
// Only a VALID TOKEN (any scope, API key or OAuth) bypasses the per-file
// gate — PUBLIC_READ=true opens non-confidential reads but never the
// Confidential set. Fail-closed: when no path can be resolved for the sha,
// anonymous callers are denied. Every known path is checked, because one
// confidential filing path is enough to deny (the same bytes live under
// both matter-05/hope-discovery and matter-28/HOPE Discovery).
export async function assertDocReadable(env, ref = {}, access) {
  if (access && access.scope) return; // token holder: full read access
  if (readLockdown(env)) throw new HttpError(401, { error: "unauthorized" });
  const paths = ref.path ? [ref.path] : ref.sha ? await pathsForSha(env, ref.sha) : [];
  if (!paths.length || paths.some(isConfidentialPath))
    throw new HttpError(401, { error: "unauthorized" });
}

