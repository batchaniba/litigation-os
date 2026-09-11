// CourtListener REST/Search client. Token stays in process env — never VITE_*.

export const CL_BASE = "https://www.courtlistener.com/api/rest/v4";
export const CL_SITE = "https://www.courtlistener.com";
export const CL_UA =
  "litigation-portfolio-courtlistener-bridge/0.1 (+https://github.com/newanforbi/interactive-litigation-portfolio)";

export function readCourtListenerToken(env = process.env) {
  for (const key of Object.keys(env)) {
    if (key.startsWith("VITE_") && /COURTLISTENER/i.test(`${key}=${env[key] ?? ""}`)) {
      throw new Error(
        "COURTLISTENER_TOKEN must not live in a VITE_* variable — that would ship it to the browser.",
      );
    }
  }
  const token = String(env.COURTLISTENER_TOKEN ?? "").trim();
  return token || null;
}

export function remainingFromUsage(usage) {
  if (!usage || typeof usage !== "object") return { daily: null, hourly: null, minute: null, unknown: true };
  const pick = (...candidates) => {
    for (const value of candidates) {
      if (Number.isFinite(value)) return value;
    }
    return null;
  };
  const daily = pick(
    usage.daily_remaining,
    usage.remaining,
    Number.isFinite(usage.daily_limit) && Number.isFinite(usage.daily_used)
      ? usage.daily_limit - usage.daily_used
      : null,
    Number.isFinite(usage.limits?.requests?.per_day) && Number.isFinite(usage.usage?.requests?.per_day)
      ? usage.limits.requests.per_day - usage.usage.requests.per_day
      : null,
  );
  const hourly = pick(
    usage.hourly_remaining,
    Number.isFinite(usage.limits?.requests?.per_hour) && Number.isFinite(usage.usage?.requests?.per_hour)
      ? usage.limits.requests.per_hour - usage.usage.requests.per_hour
      : null,
  );
  const minute = pick(
    usage.minute_remaining,
    Number.isFinite(usage.limits?.requests?.per_minute) && Number.isFinite(usage.usage?.requests?.per_minute)
      ? usage.limits.requests.per_minute - usage.usage.requests.per_minute
      : null,
  );
  return {
    daily,
    hourly,
    minute,
    unknown: daily == null && hourly == null && minute == null,
  };
}

export function budgetAllows(usage, { minDaily = 8 } = {}) {
  const remaining = remainingFromUsage(usage);
  if (remaining.unknown) return { ok: true, remaining, reason: "usage_shape_unknown" };
  if (remaining.daily != null && remaining.daily < minDaily) {
    return { ok: false, remaining, reason: `daily remaining ${remaining.daily} < ${minDaily}` };
  }
  if (remaining.hourly != null && remaining.hourly < 2) {
    return { ok: false, remaining, reason: `hourly remaining ${remaining.hourly} < 2` };
  }
  return { ok: true, remaining, reason: "ok" };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function createClient({
  fetchImpl = globalThis.fetch,
  token = readCourtListenerToken(),
  minIntervalMs = 250,
} = {}) {
  let lastAt = 0;

  async function request(url, { auth = false, retries = 3 } = {}) {
    const wait = minIntervalMs - (Date.now() - lastAt);
    if (wait > 0) await sleep(wait);
    const headers = { Accept: "application/json", "User-Agent": CL_UA };
    if (auth) {
      if (!token) {
        const error = new Error("COURTLISTENER_TOKEN is required for this CourtListener endpoint.");
        error.code = "CL_TOKEN_REQUIRED";
        throw error;
      }
      headers.Authorization = `Token ${token}`;
    }
    let lastError;
    for (let attempt = 0; attempt < retries; attempt += 1) {
      lastAt = Date.now();
      let response;
      try {
        response = await fetchImpl(url, { headers });
      } catch (err) {
        lastError = err;
        await sleep(500 * (attempt + 1));
        continue;
      }
      if (response.status === 429 || response.status >= 500) {
        await sleep(1000 * (attempt + 1));
        lastError = new Error(`CourtListener HTTP ${response.status} for ${url}`);
        continue;
      }
      const text = await response.text();
      let data;
      try {
        data = text ? JSON.parse(text) : null;
      } catch {
        data = { raw: text };
      }
      if (!response.ok) {
        const error = new Error(data?.detail || `CourtListener HTTP ${response.status} for ${url}`);
        error.status = response.status;
        error.body = data;
        throw error;
      }
      return data;
    }
    throw lastError ?? new Error(`CourtListener request failed for ${url}`);
  }

  async function searchDockets({ docketNumber, courtId }) {
    const params = new URLSearchParams({ type: "d", docket_number: docketNumber });
    if (courtId) params.set("court", courtId);
    const data = await request(`${CL_BASE}/search/?${params}`);
    return Array.isArray(data?.results) ? data.results : [];
  }

  async function getApiUsage() {
    return request(`${CL_BASE}/api-usage/`, { auth: true });
  }

  async function listDocketEntries({ docketId, afterEntryId = null, afterEntryNumber = null }) {
    const params = new URLSearchParams({
      docket: String(docketId),
      order_by: "id",
    });
    if (afterEntryId != null) params.set("id__gt", String(afterEntryId));
    else if (afterEntryNumber != null) params.set("entry_number__gt", String(afterEntryNumber));
    const entries = [];
    let url = `${CL_BASE}/docket-entries/?${params}`;
    while (url) {
      const page = await request(url, { auth: true });
      const rows = Array.isArray(page?.results) ? page.results : [];
      for (const row of rows) {
        if (afterEntryId != null && Number(row.id) <= Number(afterEntryId)) continue;
        if (afterEntryNumber != null && Number(row.entry_number) <= Number(afterEntryNumber)) continue;
        entries.push(row);
      }
      url = page?.next || null;
    }
    return entries;
  }

  return {
    token,
    request,
    searchDockets,
    getApiUsage,
    listDocketEntries,
  };
}
