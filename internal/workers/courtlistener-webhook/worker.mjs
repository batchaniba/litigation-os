// Cloudflare Worker: CourtListener webhook -> GitHub repository_dispatch adapter.
//
// CourtListener POSTs JSON events here whenever a subscribed docket gets new
// filings (DOCKET_ALERT), a search alert fires (SEARCH_ALERT), etc. This worker
// authenticates the request, then translates it into a repository_dispatch on
// newanforbi/interactive-litigation-portfolio so the CourtListener sync workflow
// runs on demand instead of on a fixed poll schedule.
//
// SECURITY NOTE — read before "improving" this: CourtListener's webhook system
// has NO signature/HMAC mechanism. Their official docs
// (https://www.courtlistener.com/help/api/webhooks/) state this explicitly and
// recommend (a) long, random, secret webhook URLs and (b) allow-listing their
// two egress IPs. This worker implements exactly that: a secret path component
// (WEBHOOK_PATH_SECRET) plus a source-IP check against the published egress
// IPs. Do NOT add HMAC verification against a made-up signing secret — there
// is nothing on CourtListener's side to verify it against.
//
// The sync workflow re-queries the CourtListener API for anything the event
// mentions; nothing from a webhook POST body is ever committed to the repo.

const REPO = "newanforbi/interactive-litigation-portfolio";
const DISPATCH_EVENT_TYPE = "courtlistener-webhook";

// Published CourtListener webhook egress IPs (docs: "Webhook Security").
const CL_EGRESS_IPS = new Set(["34.210.230.218", "54.189.59.91"]);

// webhook.event_type values from the docs.
const EVENT_TYPE_NAMES = {
  1: "DOCKET_ALERT",
  2: "SEARCH_ALERT",
  3: "RECAP_FETCH",
  4: "OLD_DOCKET_ALERTS_REPORT",
  5: "PRAY_AND_PAY",
};

const PATH_RE = /^\/wh\/([A-Za-z0-9_-]{32,})$/;

function timingSafeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) {
    return false;
  }
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

export default {
  async fetch(request, env, _ctx) {
    const url = new URL(request.url);

    if (request.method !== "POST") {
      return new Response("method not allowed", { status: 405 });
    }

    // 1. Secret URL path. 404 (not 401) so scanners learn nothing about the
    //    endpoint's existence.
    const pathMatch = PATH_RE.exec(url.pathname);
    if (!pathMatch || !timingSafeEqual(pathMatch[1], env.WEBHOOK_PATH_SECRET || "")) {
      return new Response("not found", { status: 404 });
    }

    // 2. Source-IP check against CourtListener's published egress IPs.
    //    SKIP_IP_CHECK exists only for local testing of the worker itself;
    //    never enable it in production.
    const clientIp = request.headers.get("cf-connecting-ip");
    if (env.SKIP_IP_CHECK !== "true" && !CL_EGRESS_IPS.has(clientIp)) {
      return new Response("forbidden", { status: 403 });
    }

    // 3. Parse and shape the event.
    let body;
    try {
      body = await request.json();
    } catch {
      return json({ ok: false, error: "invalid JSON" }, 400);
    }
    const webhookMeta = body && typeof body === "object" ? body.webhook || {} : {};
    const payload = body && typeof body === "object" ? body.payload || {} : {};
    const eventTypeId = Number(webhookMeta.event_type);
    const eventName = EVENT_TYPE_NAMES[eventTypeId] || `UNKNOWN_${webhookMeta.event_type}`;

    const dockets =
      eventTypeId === 1 && Array.isArray(payload.results)
        ? [
            ...new Set(
              payload.results.map((r) => r && r.docket).filter((d) => d !== undefined && d !== null),
            ),
          ].slice(0, 200)
        : [];

    const clientPayload = {
      courtlistener_event: eventName,
      webhook_version: webhookMeta.version ?? null,
      // CourtListener's Idempotency-Key: unique per event; the sync workflow's
      // ledger makes re-deliveries harmless.
      idempotency_key: request.headers.get("idempotency-key"),
      dockets,
      alert:
        payload.alert && typeof payload.alert === "object"
          ? { id: payload.alert.id ?? null, name: payload.alert.name ?? null }
          : null,
      received_at: new Date().toISOString(),
    };

    // 4. Translate into a GitHub repository_dispatch. We await it: on failure
    //    we return 5xx so CourtListener retries (exponential backoff, ~54h of
    //    retries before they disable the endpoint). Duplicate dispatches are
    //    harmless — the sync workflow is idempotent and serialized.
    //    Nothing secret is ever logged.
    let dispatchStatus = 0;
    try {
      const res = await fetch(`https://api.github.com/repos/${REPO}/dispatches`, {
        method: "POST",
        headers: {
          Accept: "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28",
          Authorization: `Bearer ${env.GITHUB_TOKEN}`,
          "Content-Type": "application/json",
          "User-Agent": "ilp-courtlistener-webhook",
        },
        body: JSON.stringify({ event_type: DISPATCH_EVENT_TYPE, client_payload: clientPayload }),
      });
      dispatchStatus = res.status;
      if (!res.ok) {
        const detail = await res.text().catch(() => "");
        console.log(
          `dispatch failed: http=${res.status} event=${eventName} ` +
            `idempotency=${clientPayload.idempotency_key} detail=${detail.slice(0, 200)}`,
        );
        return json({ ok: false, error: "dispatch failed" }, 502);
      }
    } catch (err) {
      console.log(
        `dispatch error: event=${eventName} idempotency=${clientPayload.idempotency_key} ` +
          `error=${String((err && err.message) || err).slice(0, 200)}`,
      );
      return json({ ok: false, error: "dispatch error" }, 502);
    }

    console.log(
      `dispatched: event=${eventName} dockets=${dockets.length} ` +
        `idempotency=${clientPayload.idempotency_key} github_http=${dispatchStatus}`,
    );
    return json({ ok: true }, 200);
  },
};
