// OAuth 2.0 / 2.1 authorization server for the litigation-doc-api Worker.
//
// Why this exists: some MCP clients — notably ChatGPT's "Create MCP App"
// flow — cannot send a static `Authorization: Bearer <token>` header. They
// only speak OAuth (or no auth). This module lets the Worker act as its own
// authorization server so those clients can obtain a scoped token with the
// owner's approval, landing in the same scope model as API_KEYS
// (auth.mjs: "r" read, "rw" read+write) and the same audit trail.
//
// Single-owner design: there is exactly one resource owner (the portfolio
// owner). The authorize step authenticates him with a pre-shared owner key
// (the OAUTH_OWNER_KEY Worker secret) typed into a consent page. There are
// no user accounts and no password database.
//
// Endpoints (wired in index.mjs):
//   GET /.well-known/oauth-authorization-server[/mcp] -> AS metadata (RFC 8414)
//   GET /.well-known/oauth-protected-resource[/mcp]   -> resource metadata (RFC 9728)
//   POST /oauth/register  -> Dynamic Client Registration (RFC 7591)
//   GET  /oauth/authorize -> consent page (owner key + scope approval)
//   POST /oauth/authorize -> verify owner key, issue code, redirect to client
//   POST /oauth/token     -> authorization_code exchange / refresh_token rotation
//
// Security properties:
//   * Fail-closed: every endpoint 503s when D1 is absent, the oauth_* tables
//     are not provisioned, or OAUTH_OWNER_KEY is not configured.
//   * Only token *hashes* are stored (same philosophy as API_KEYS).
//   * Authorization codes: 10-minute TTL, single use, bound to client_id +
//     redirect_uri + PKCE S256 challenge.
//   * PKCE S256 is REQUIRED (OAuth 2.1); the token endpoint also requires
//     client authentication (client_secret_basic or client_secret_post).
//   * redirect_uris are exact-match validated at authorize, token, and DCR.
//   * Refresh tokens rotate on every use (old one is deleted).
//   * OAuth grants only take effect when API_KEYS is configured on the
//     Worker (see auth.mjs): you cannot get a writable-but-unauthenticated
//     API by enabling OAuth alone.

import { HttpError } from "./data.mjs";
import { sha256Hex } from "./auth.mjs";

const SCOPES = ["read", "write"];
const CODE_TTL = 600; // authorization codes: 10 minutes, single use
const ACCESS_TTL = 86400; // access tokens: 24 hours
const REFRESH_TTL = 90 * 86400; // refresh tokens: 90 days, rotated on use

const nowSec = () => Math.floor(Date.now() / 1000);

function randHex(bytes) {
  const b = new Uint8Array(bytes);
  crypto.getRandomValues(b);
  return [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
}

function b64url(buf) {
  const bin = String.fromCharCode(...new Uint8Array(buf));
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function pkceS256(verifier) {
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(verifier),
  );
  return b64url(digest);
}

// Constant-time comparison for the owner key (length leak is acceptable;
// content is not).
function timingSafeEqual(a, b) {
  const ab = new TextEncoder().encode(a);
  const bb = new TextEncoder().encode(b);
  if (ab.length !== bb.length) return false;
  let diff = 0;
  for (let i = 0; i < ab.length; i++) diff |= ab[i] ^ bb[i];
  return diff === 0;
}

const esc = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]),
  );

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });

const oauthError = (status, error, description) =>
  json({ error, ...(description ? { error_description: description } : {}) }, status);

// Fail-closed: D1 absent or oauth tables not provisioned -> 503.
async function needOAuthTables(env) {
  if (!env.DB) throw new HttpError(503, { error: "oauth_not_configured" });
  try {
    await env.DB.prepare("SELECT client_id FROM oauth_clients LIMIT 0").run();
  } catch {
    throw new HttpError(503, { error: "oauth_not_configured" });
  }
}

function needOwnerKey(env) {
  if (!env.OAUTH_OWNER_KEY) throw new HttpError(503, { error: "oauth_not_configured" });
}

// --- discovery metadata -----------------------------------------------------

export function authorizationServerMetadata(origin) {
  return {
    issuer: origin,
    authorization_endpoint: `${origin}/oauth/authorize`,
    token_endpoint: `${origin}/oauth/token`,
    registration_endpoint: `${origin}/oauth/register`,
    response_types_supported: ["code"],
    grant_types_supported: ["authorization_code", "refresh_token"],
    code_challenge_methods_supported: ["S256"],
    scopes_supported: SCOPES,
    token_endpoint_auth_methods_supported: ["client_secret_basic", "client_secret_post"],
  };
}

export function protectedResourceMetadata(origin) {
  return {
    resource: `${origin}/mcp`,
    authorization_servers: [origin],
    scopes_supported: SCOPES,
    bearer_methods_supported: ["header"],
  };
}

// --- Dynamic Client Registration (RFC 7591) ---------------------------------

function validRedirectUri(u) {
  let parsed;
  try {
    parsed = new URL(u);
  } catch {
    return false;
  }
  if (parsed.hash) return false; // fragments are never sent to the server
  if (parsed.protocol === "https:") return true;
  // http is allowed only for loopback (native apps), per RFC 8252.
  return (
    parsed.protocol === "http:" &&
    (parsed.hostname === "localhost" || parsed.hostname === "127.0.0.1")
  );
}

export async function handleRegister(request, env) {
  try {
    await needOAuthTables(env);
  } catch (e) {
    return json(e.body, e.status);
  }
  if ((request.headers.get("content-type") || "").includes("application/json") === false)
    return oauthError(400, "invalid_request", "content-type must be application/json");
  let body;
  try {
    body = await request.json();
  } catch {
    return oauthError(400, "invalid_request", "body must be valid JSON");
  }
  const redirectUris = body?.redirect_uris;
  if (!Array.isArray(redirectUris) || redirectUris.length === 0)
    return oauthError(400, "invalid_redirect_uri", "redirect_uris must be a non-empty array");
  for (const u of redirectUris) {
    if (typeof u !== "string" || !validRedirectUri(u))
      return oauthError(400, "invalid_redirect_uri", `bad redirect_uri: ${u}`);
  }
  const clientId = `cli_${randHex(12)}`;
  const clientSecret = randHex(32);
  const name = typeof body?.client_name === "string" ? body.client_name.slice(0, 120) : null;
  await env.DB.prepare(
    `INSERT INTO oauth_clients (client_id, client_secret_hash, redirect_uris, client_name)
     VALUES (?, ?, ?, ?)`,
  )
    .bind(clientId, await sha256Hex(clientSecret), JSON.stringify(redirectUris), name)
    .run();
  return json(
    {
      client_id: clientId,
      client_secret: clientSecret,
      redirect_uris: redirectUris,
      client_name: name,
      token_endpoint_auth_method: "client_secret_post",
      grant_types: ["authorization_code", "refresh_token"],
      response_types: ["code"],
    },
    201,
  );
}

async function getClient(env, clientId) {
  const row = await env.DB.prepare(
    `SELECT client_id, client_secret_hash, redirect_uris, client_name
     FROM oauth_clients WHERE client_id = ?`,
  )
    .bind(clientId)
    .first();
  if (!row) return null;
  let uris = [];
  try {
    uris = JSON.parse(row.redirect_uris);
  } catch {
    uris = [];
  }
  return { ...row, redirect_uris: Array.isArray(uris) ? uris : [] };
}

function parseScope(raw) {
  const parts = String(raw ?? "")
    .split(/\s+/)
    .filter(Boolean);
  const ok = [...new Set(parts.filter((p) => SCOPES.includes(p)))];
  return ok.length ? ok : ["read"]; // conservative default
}

// --- authorize: consent page -------------------------------------------------

function authorizeErrorPage(message) {
  return new Response(
    `<!doctype html><html><head><meta charset="utf-8"><title>Authorization error</title></head>` +
      `<body style="font-family:system-ui;max-width:34rem;margin:3rem auto;padding:0 1rem">` +
      `<h1>Authorization error</h1><p>${esc(message)}</p></body></html>`,
    { status: 400, headers: { "content-type": "text/html; charset=utf-8" } },
  );
}

function consentPage({ clientName, requestedScope, state, clientId, redirectUri, codeChallenge, error }) {
  const scopeDesc = {
    read: "View matters, deadline clocks, and documents",
    write: "Create, update, and delete matters, clocks, and document entries",
  };
  const scopeLabels = requestedScope.map((s) => `${s} — ${scopeDesc[s]}`).join("<br>");
  const hidden = { client_id: clientId, redirect_uri: redirectUri, state: state ?? "", code_challenge: codeChallenge, requested_scope: requestedScope.join(" ") };
  const hiddenInputs = Object.entries(hidden)
    .map(([k, v]) => `<input type="hidden" name="${k}" value="${esc(v)}">`)
    .join("\n");
  return new Response(
    `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">` +
      `<title>Authorize ${esc(clientName)}</title></head>` +
      `<body style="font-family:system-ui;max-width:34rem;margin:3rem auto;padding:0 1rem">` +
      `<h1>Authorize ${esc(clientName)}</h1>` +
      `<p>This app is requesting access to your litigation document API:</p>` +
      `<p>${scopeLabels}</p>` +
      (error ? `<p style="color:#b00020"><strong>${esc(error)}</strong></p>` : "") +
      `<form method="post" action="/oauth/authorize">` +
      hiddenInputs +
      `<p><label>Grant<br>` +
      `<label><input type="radio" name="approved_scope" value="read" checked> read only</label><br>` +
      `<label><input type="radio" name="approved_scope" value="read write"> read + write</label>` +
      `</label></p>` +
      `<p><label>Owner key<br><input type="password" name="owner_key" autocomplete="off" style="width:100%;padding:.5rem"></label></p>` +
      `<p><button type="submit" name="decision" value="approve" style="padding:.6rem 1.2rem">Approve</button> ` +
      `<button type="submit" name="decision" value="deny" style="padding:.6rem 1.2rem">Deny</button></p>` +
      `</form></body></html>`,
    { status: error ? 401 : 200, headers: { "content-type": "text/html; charset=utf-8" } },
  );
}

function redirectWithError(redirectUri, state, error) {
  const u = new URL(redirectUri);
  u.searchParams.set("error", error);
  if (state) u.searchParams.set("state", state);
  return Response.redirect(u.toString(), 302);
}

export async function handleAuthorizeGet(request, env, url) {
  try {
    await needOAuthTables(env);
    needOwnerKey(env);
  } catch (e) {
    return json(e.body, e.status);
  }
  const p = url.searchParams;
  const clientId = p.get("client_id");
  const redirectUri = p.get("redirect_uri");
  const responseType = p.get("response_type");
  const challenge = p.get("code_challenge");
  const method = p.get("code_challenge_method");
  const state = p.get("state");

  if (responseType !== "code")
    return authorizeErrorPage("response_type must be code");
  const client = clientId ? await getClient(env, clientId) : null;
  if (!client) return authorizeErrorPage("unknown client_id — register with POST /oauth/register first");
  if (!redirectUri || !client.redirect_uris.includes(redirectUri))
    return authorizeErrorPage("redirect_uri does not match a registered value");
  if (!challenge || method !== "S256")
    return redirectWithError(redirectUri, state, "invalid_request"); // PKCE is mandatory
  const scope = parseScope(p.get("scope"));
  return consentPage({
    clientName: client.client_name || client.client_id,
    requestedScope: scope,
    state,
    clientId,
    redirectUri,
    codeChallenge: challenge,
  });
}

export async function handleAuthorizePost(request, env) {
  try {
    await needOAuthTables(env);
    needOwnerKey(env);
  } catch (e) {
    return json(e.body, e.status);
  }
  const form = await request.formData().catch(() => null);
  if (!form) return authorizeErrorPage("form body required");
  const f = (k) => String(form.get(k) ?? "");
  const clientId = f("client_id");
  const redirectUri = f("redirect_uri");
  const state = f("state");
  const challenge = f("code_challenge");
  const requestedScope = parseScope(f("requested_scope"));

  const client = clientId ? await getClient(env, clientId) : null;
  if (!client || !client.redirect_uris.includes(redirectUri) || !challenge)
    return authorizeErrorPage("invalid authorization request — start over");
  if (f("decision") !== "approve") return redirectWithError(redirectUri, state, "access_denied");

  if (!timingSafeEqual(f("owner_key"), env.OAUTH_OWNER_KEY)) {
    return consentPage({
      clientName: client.client_name || client.client_id,
      requestedScope,
      state,
      clientId,
      redirectUri,
      codeChallenge: challenge,
      error: "Owner key incorrect.",
    });
  }

  // The owner is the resource owner: the radio choice (read, or read+write)
  // is authoritative as long as it stays within the known scopes.
  let approved = parseScope(f("approved_scope"));
  approved = approved.filter((s) => SCOPES.includes(s));
  if (!approved.length) approved = ["read"];

  const code = randHex(32);
  await env.DB.prepare(
    `INSERT INTO oauth_codes (code_hash, client_id, redirect_uri, code_challenge, scope, expires_at)
     VALUES (?, ?, ?, ?, ?, ?)`,
  )
    .bind(
      await sha256Hex(code),
      clientId,
      redirectUri,
      challenge,
      approved.join(" "),
      nowSec() + CODE_TTL,
    )
    .run();
  const u = new URL(redirectUri);
  u.searchParams.set("code", code);
  if (state) u.searchParams.set("state", state);
  return Response.redirect(u.toString(), 302);
}

// --- token endpoint ----------------------------------------------------------

async function clientAuth(request, env, form) {
  // client_secret_basic preferred; client_secret_post also accepted.
  const hdr = request.headers.get("authorization") || "";
  let id = null;
  let secret = null;
  const m = hdr.match(/^Basic\s+(.+)$/i);
  if (m) {
    try {
      const decoded = atob(m[1]);
      const i = decoded.indexOf(":");
      if (i > 0) {
        id = decoded.slice(0, i);
        secret = decoded.slice(i + 1);
      }
    } catch {
      /* fall through to post */
    }
  }
  if (!id) {
    id = String(form.get("client_id") ?? "");
    secret = String(form.get("client_secret") ?? "");
  }
  if (!id || !secret) return null;
  const client = await getClient(env, id);
  if (!client) return null;
  if (!(await timingSafeEqual(await sha256Hex(secret), client.client_secret_hash))) return null;
  return client;
}

async function issueTokenPair(env, client, scope) {
  const access = randHex(32);
  const refresh = randHex(32);
  const now = nowSec();
  const label = client.client_name || client.client_id;
  await env.DB.batch([
    env.DB.prepare(
      `INSERT INTO oauth_tokens (token_hash, kind, client_id, label, scope, expires_at)
       VALUES (?, 'access', ?, ?, ?, ?)`,
    ).bind(await sha256Hex(access), client.client_id, label, scope.join(" "), now + ACCESS_TTL),
    env.DB.prepare(
      `INSERT INTO oauth_tokens (token_hash, kind, client_id, label, scope, expires_at)
       VALUES (?, 'refresh', ?, ?, ?, ?)`,
    ).bind(await sha256Hex(refresh), client.client_id, label, scope.join(" "), now + REFRESH_TTL),
  ]);
  return {
    access_token: access,
    token_type: "Bearer",
    expires_in: ACCESS_TTL,
    refresh_token: refresh,
    scope: scope.join(" "),
  };
}

export async function handleToken(request, env) {
  try {
    await needOAuthTables(env);
  } catch (e) {
    return json(e.body, e.status);
  }
  const ct = request.headers.get("content-type") || "";
  if (!ct.includes("application/x-www-form-urlencoded"))
    return oauthError(400, "invalid_request", "content-type must be application/x-www-form-urlencoded");
  const raw = await request.text();
  const form = new URLSearchParams(raw);
  const grant = form.get("grant_type");

  if (grant === "authorization_code") {
    const code = String(form.get("code") ?? "");
    const redirectUri = String(form.get("redirect_uri") ?? "");
    const verifier = String(form.get("code_verifier") ?? "");
    if (!code || !redirectUri || !verifier)
      return oauthError(400, "invalid_request", "code, redirect_uri, and code_verifier are required");
    const client = await clientAuth(request, env, form);
    if (!client) return oauthError(401, "invalid_client", "client authentication failed");

    // Single-use: fetch then delete in the same beat.
    const row = await env.DB.prepare(`SELECT * FROM oauth_codes WHERE code_hash = ?`)
      .bind(await sha256Hex(code))
      .first();
    if (row) {
      await env.DB.prepare(`DELETE FROM oauth_codes WHERE code_hash = ?`)
        .bind(await sha256Hex(code))
        .run();
    }
    if (!row) return oauthError(400, "invalid_grant", "code not found or already used");
    if (row.expires_at <= nowSec()) return oauthError(400, "invalid_grant", "code expired");
    if (row.client_id !== client.client_id || row.redirect_uri !== redirectUri)
      return oauthError(400, "invalid_grant", "code was issued to a different client or redirect_uri");
    if ((await pkceS256(verifier)) !== row.code_challenge)
      return oauthError(400, "invalid_grant", "PKCE verification failed");

    const scope = parseScope(row.scope);
    return json(await issueTokenPair(env, client, scope));
  }

  if (grant === "refresh_token") {
    const rt = String(form.get("refresh_token") ?? "");
    if (!rt) return oauthError(400, "invalid_request", "refresh_token is required");
    const client = await clientAuth(request, env, form);
    if (!client) return oauthError(401, "invalid_client", "client authentication failed");
    const row = await env.DB.prepare(
      `SELECT * FROM oauth_tokens WHERE token_hash = ? AND kind = 'refresh'`,
    )
      .bind(await sha256Hex(rt))
      .first();
    if (row) {
      // Rotation: the presented refresh token is consumed.
      await env.DB.prepare(`DELETE FROM oauth_tokens WHERE token_hash = ?`)
        .bind(await sha256Hex(rt))
        .run();
    }
    if (!row) return oauthError(400, "invalid_grant", "refresh token not found or already used");
    if (row.expires_at <= nowSec()) return oauthError(400, "invalid_grant", "refresh token expired");
    if (row.client_id !== client.client_id)
      return oauthError(400, "invalid_grant", "refresh token belongs to a different client");
    const scope = parseScope(row.scope);
    return json(await issueTokenPair(env, client, scope));
  }

  return oauthError(400, "unsupported_grant_type", "grant_type must be authorization_code or refresh_token");
}

// --- token verification (used by auth.mjs) -----------------------------------
// Returns { scope, label } for a live access token, else null. Never throws:
// a missing table or D1 just means "no OAuth grants".
export async function verifyAccessToken(env, token) {
  try {
    if (!env.DB) return null;
    const row = await env.DB.prepare(
      `SELECT scope, label, expires_at FROM oauth_tokens
       WHERE token_hash = ? AND kind = 'access'`,
    )
      .bind(await sha256Hex(token))
      .first();
    if (!row || row.expires_at <= nowSec()) return null;
    return { scope: String(row.scope || ""), label: row.label || "oauth-client" };
  } catch {
    return null;
  }
}

export function wwwAuthenticate(origin) {
  return `Bearer resource_metadata="${origin}/.well-known/oauth-protected-resource"`;
}
