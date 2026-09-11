// CourtListener webhooks are a hint to look, not a payload to commit.
// Their POSTs are not cryptographically signed; treat the body as untrusted.

export const COURTLISTENER_WEBHOOK_IPS = Object.freeze(["34.210.230.218", "54.189.59.91"]);

export function isCourtListenerWebhookIp(ip) {
  const value = String(ip ?? "").trim();
  return COURTLISTENER_WEBHOOK_IPS.includes(value);
}

function asId(value) {
  if (typeof value === "number" && Number.isInteger(value) && value > 0) return value;
  if (typeof value === "string" && /^\d+$/.test(value)) return Number(value);
  const match = String(value ?? "").match(/\/(?:docket|dockets)\/(\d+)\b/);
  return match ? Number(match[1]) : null;
}

function pushId(into, value) {
  const id = asId(value);
  if (id) into.add(id);
}

/** Pull docket IDs out of a webhook body. Never returns docket entries to apply. */
export function extractDocketHints(body) {
  const ids = new Set();
  if (!body || typeof body !== "object") return [];
  const payload = body.payload && typeof body.payload === "object" ? body.payload : body;
  pushId(ids, payload.docket);
  pushId(ids, payload.docket_id);
  const results = Array.isArray(payload.results) ? payload.results : [];
  // results[] on a docket_alert are docket *entries*. Their `id` is not a docket id.
  if (!results.length) pushId(ids, payload.id);
  for (const row of results) {
    if (!row || typeof row !== "object") continue;
    pushId(ids, row.docket);
    pushId(ids, row.docket_id);
  }
  return [...ids];
}

/**
 * Decide what an incoming webhook is allowed to trigger.
 * `applyPayloadEntries` is always false — the receiver must re-query the API.
 */
export function webhookSyncPlan(body, { idempotencyKey, sourceIp } = {}) {
  if (sourceIp && !isCourtListenerWebhookIp(sourceIp)) {
    return {
      action: "reject",
      reason: "ip_not_allowlisted",
      docketIds: [],
      applyPayloadEntries: false,
    };
  }
  const docketIds = extractDocketHints(body);
  if (!docketIds.length) {
    return {
      action: "ignore",
      reason: "no_docket_hint",
      docketIds: [],
      applyPayloadEntries: false,
      idempotencyKey: idempotencyKey ?? null,
    };
  }
  return {
    action: "requery",
    reason: "webhook_is_a_hint",
    docketIds,
    applyPayloadEntries: false,
    idempotencyKey: idempotencyKey ?? null,
  };
}
