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
  const token = String(env.COURTLISTENER_TOKEN || env.COURTLISTENER_API_TOKEN || "").trim();
  return token || null;
}

function windowKind(row) {
  const seconds = Number(row?.window_seconds);
  const rate = String(row?.rate ?? "");
  if (seconds === 86400 || /\/day$/i.test(rate)) return "daily";
  if (seconds === 3600 || /\/hour$/i.test(rate)) return "hourly";
  if (seconds === 60 || /\/min$/i.test(rate)) return "minute";
  return null;
}

function remainingOf(row) {
  if (Number.isFinite(row?.remaining)) return Number(row.remaining);
  if (Number.isFinite(row?.limit) && Number.isFinite(row?.used)) {
    return Math.max(0, Number(row.limit) - Number(row.used));
  }
  return null;
}

/** Parse /api-usage/. Prefer documented current_usage rows (scope=user). */
export function remainingFromUsage(usage) {
  if (!usage || typeof usage !== "object") {
    return { daily: null, hourly: null, minute: null, unknown: true, rows: [] };
  }
  const rows = Array.isArray(usage.current_usage) ? usage.current_usage : [];
  const userRows = rows.filter((row) => row?.scope === "user");
  if (userRows.length) {
    const pick = (kind) => remainingOf(userRows.find((row) => windowKind(row) === kind));
    const daily = pick("daily");
    const hourly = pick("hourly");
    const minute = pick("minute");
    return {
      daily,
      hourly,
      minute,
      unknown: daily == null && hourly == null && minute == null,
      rows: userRows,
      blocked: userRows.some((row) => row.blocked === true || Number(row.limit) === 0),
    };
  }
  const pickLegacy = (...candidates) => {
    for (const value of candidates) {
      if (Number.isFinite(value)) return value;
    }
    return null;
  };
  const daily = pickLegacy(
    usage.daily_remaining,
    Number.isFinite(usage.daily_limit) && Number.isFinite(usage.daily_used)
      ? usage.daily_limit - usage.daily_used
      : null,
  );
  const hourly = pickLegacy(usage.hourly_remaining);
  const minute = pickLegacy(usage.minute_remaining);
  return {
    daily,
    hourly,
    minute,
    unknown: daily == null && hourly == null && minute == null,
    rows: [],
    blocked: false,
  };
}

export function budgetAllows(usage, { minDaily = 8, minHourly = 2, minMinute = 1 } = {}) {
  const remaining = remainingFromUsage(usage);
  if (remaining.blocked) {
    return { ok: false, remaining, reason: "user scope blocked" };
  }
  if (remaining.unknown) {
    return { ok: false, remaining, reason: "usage_shape_unknown" };
  }
  if (remaining.daily != null && remaining.daily < minDaily) {
    return { ok: false, remaining, reason: `daily remaining ${remaining.daily} < ${minDaily}` };
  }
  if (remaining.hourly != null && remaining.hourly < minHourly) {
    return { ok: false, remaining, reason: `hourly remaining ${remaining.hourly} < ${minHourly}` };
  }
  if (remaining.minute != null && remaining.minute < minMinute) {
    return { ok: false, remaining, reason: `minute remaining ${remaining.minute} < ${minMinute}` };
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

  async function listDocketEntries({
    docketId,
    afterEntryId = null,
    afterEntryNumber = null,
    dateFiledGte = null,
  } = {}) {
    const params = new URLSearchParams({
      docket: String(docketId),
      order_by: "id",
    });
    if (afterEntryId != null) params.set("id__gt", String(afterEntryId));
    else if (afterEntryNumber != null) params.set("entry_number__gt", String(afterEntryNumber));
    if (dateFiledGte) params.set("date_filed__gte", String(dateFiledGte));
    const entries = [];
    let url = `${CL_BASE}/docket-entries/?${params}`;
    while (url) {
      const page = await request(url, { auth: true });
      const rows = Array.isArray(page?.results) ? page.results : [];
      for (const row of rows) {
        if (afterEntryId != null && Number(row.id) <= Number(afterEntryId)) continue;
        if (afterEntryNumber != null && Number(row.entry_number) <= Number(afterEntryNumber)) continue;
        const filed = String(row.date_filed ?? row.entry_date_filed ?? "").slice(0, 10);
        if (dateFiledGte && filed && filed < dateFiledGte) continue;
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
