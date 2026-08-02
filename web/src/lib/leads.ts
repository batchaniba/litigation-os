import { CALENDLY, isCalendlyConfigured } from "../config/site";

export type LeadPayload = {
  source: "equity-iq" | "orientation-form";
  name?: string;
  email?: string;
  phone?: string;
  notes?: string;
  quizAnswers?: Record<string, string>;
  quizBand?: string;
  quizScore?: number;
  createdAt: string;
};

const STORAGE_KEY = "e2b_lead_draft";

export function saveLeadDraft(payload: Partial<LeadPayload>) {
  const existing = loadLeadDraft();
  const next = { ...existing, ...payload, createdAt: new Date().toISOString() };
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  return next;
}

export function loadLeadDraft(): Partial<LeadPayload> {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as Partial<LeadPayload>) : {};
  } catch {
    return {};
  }
}

export async function submitLead(payload: LeadPayload): Promise<{ ok: boolean; mode: "webhook" | "local" }> {
  const webhook = import.meta.env.VITE_LEAD_WEBHOOK_URL as string | undefined;
  saveLeadDraft(payload);

  if (webhook) {
    const res = await fetch(webhook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return { ok: res.ok, mode: "webhook" };
  }

  console.info("[Equity2Bitcoin lead]", payload);
  return { ok: true, mode: "local" };
}

export function getCalendlyUrl(): string {
  const url = CALENDLY.orientationUrl;
  return isCalendlyConfigured(url) ? url : "";
}

export function calendlyUrlWithPrefill(base: string, draft: Partial<LeadPayload>): string {
  if (!base) return "";
  const url = new URL(base);
  url.searchParams.set("hide_gdpr_banner", "1");
  if (draft.name) url.searchParams.set("name", draft.name);
  if (draft.email) url.searchParams.set("email", draft.email);
  if (draft.quizBand) {
    url.searchParams.set(
      "a1",
      `Equity IQ: ${draft.quizBand}${draft.quizScore != null ? ` (${draft.quizScore})` : ""}`,
    );
  }
  return url.toString();
}
