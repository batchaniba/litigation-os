import { useMemo, useState } from "react";
import { GOLD } from "../constants";
import {
  FEDERAL_COURTS,
  RECIPE_META,
  STATE_COURTS,
  computeDeadlinesFromEvent,
  type CourtKey,
  type RecipeId,
  type ServiceMethod,
} from "../utils/deadlineMath";

const RECIPE_ORDER: RecipeId[] = [
  "ca_demurrer_hearing",
  "ca_motion_hearing",
  "ca_summons_service",
  "ca_demurrer_meet_confer",
  "ca_crc_service_deadline",
  "ca_cmc_statement",
  "federal_motion_hearing",
  "federal_answer_after_service",
  "federal_response_after_mail_service",
  "edcal_lr230c_opposition",
  "edcal_lr230d_reply",
];

const SERVICE_OPTIONS: { value: ServiceMethod; label: string }[] = [
  { value: "personal", label: "Personal service" },
  { value: "mail_ca", label: "Mail within California (+5 calendar days)" },
  { value: "mail_out_of_state", label: "Mail out of state (+10 calendar days)" },
  { value: "overnight", label: "Overnight / fax / express (+2 calendar days)" },
  { value: "electronic", label: "Electronic service (baseline + note)" },
  { value: "mail_out_of_country", label: "Mail outside U.S. (+20 calendar days)" },
];

function todayIsoLocal(): string {
  const now = new Date();
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Los_Angeles",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(now);
  const y = parts.find((p) => p.type === "year")?.value;
  const m = parts.find((p) => p.type === "month")?.value;
  const d = parts.find((p) => p.type === "day")?.value;
  return `${y}-${m}-${d}`;
}

export function DeadlineCalculatorTab() {
  const [recipe, setRecipe] = useState<RecipeId>("ca_demurrer_hearing");
  const [anchorDate, setAnchorDate] = useState("2026-08-28");
  const [court, setCourt] = useState<CourtKey>("Alameda Sup. Ct.");
  const [serviceMethod, setServiceMethod] = useState<ServiceMethod>("mail_ca");

  const meta = RECIPE_META[recipe];
  const courts = meta.forum === "federal" ? FEDERAL_COURTS : STATE_COURTS;
  const showService = recipe === "ca_motion_hearing" || recipe === "ca_demurrer_hearing";

  const { result, error } = useMemo(() => {
    try {
      return {
        result: computeDeadlinesFromEvent({
          recipe,
          anchorDate,
          court,
          serviceMethod: showService ? serviceMethod : undefined,
        }),
        error: null as string | null,
      };
    } catch (err) {
      return {
        result: null,
        error: err instanceof Error ? err.message : "Unable to compute deadlines.",
      };
    }
  }, [recipe, anchorDate, court, serviceMethod, showService]);

  const onRecipeChange = (next: RecipeId) => {
    setRecipe(next);
    const nextForum = RECIPE_META[next].forum;
    if (nextForum === "federal" && !FEDERAL_COURTS.includes(court)) {
      setCourt("USDC E.D. Cal.");
    }
    if (nextForum === "california" && !STATE_COURTS.includes(court)) {
      setCourt("San Joaquin Sup. Ct.");
    }
  };

  return (
    <article className="dl-tab">
      <header className="dl-tab-header">
        <h1 className="tab-title">Deadline Math</h1>
        <p className="detail-copy detail-copy-secondary">
          Derive opposition, reply, answer, and service deadlines from the triggering event — not from
          dates typed by hand. Counts follow CCP §§12 / 12a / 12c / 1005, FRCP 6, and E.D. Cal. L.R.
          230, against published holiday calendars for the six courts in this portfolio.
        </p>
      </header>

      <section className="dl-form" aria-label="Deadline inputs">
        <label className="dl-field">
          <span className="dl-label">Triggering event</span>
          <select
            value={recipe}
            onChange={(e) => onRecipeChange(e.target.value as RecipeId)}
            className="dl-input"
          >
            {RECIPE_ORDER.map((id) => (
              <option key={id} value={id}>
                {RECIPE_META[id].label}
              </option>
            ))}
          </select>
          <span className="dl-help">{meta.description}</span>
        </label>

        <label className="dl-field">
          <span className="dl-label">{meta.anchorLabel}</span>
          <input
            type="date"
            value={anchorDate}
            onChange={(e) => setAnchorDate(e.target.value || todayIsoLocal())}
            className="dl-input"
          />
        </label>

        <label className="dl-field">
          <span className="dl-label">Court</span>
          <select
            value={court}
            onChange={(e) => setCourt(e.target.value as CourtKey)}
            className="dl-input"
          >
            {courts.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>

        {showService && (
          <label className="dl-field">
            <span className="dl-label">Service method (moving papers)</span>
            <select
              value={serviceMethod}
              onChange={(e) => setServiceMethod(e.target.value as ServiceMethod)}
              className="dl-input"
            >
              {SERVICE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </label>
        )}
      </section>

      {error && (
        <p className="dl-error" role="alert">
          {error}
        </p>
      )}

      {result && (
        <>
          <section className="dl-results" aria-live="polite">
            <div className="dl-results-head">
              <h2 className="dl-results-title">Computed deadlines</h2>
              <p className="detail-copy detail-copy-muted">
                Anchor: {result.anchorDisplay} · {result.court}
              </p>
            </div>
            <ol className="dl-deadline-list">
              {result.deadlines.map((d, index) => (
                <li
                  key={d.id}
                  className="dl-deadline"
                  style={{ animationDelay: `${index * 60}ms` }}
                >
                  <div className="dl-deadline-top">
                    <div>
                      <div className="dl-deadline-label">{d.label}</div>
                      <div className="dl-deadline-date" style={{ color: GOLD }}>
                        {d.displayDate}
                      </div>
                    </div>
                    {d.rolled && <span className="dl-rolled">Weekend / holiday roll</span>}
                  </div>
                  <p className="dl-deadline-explain">{d.explanation}</p>
                  <ul className="dl-cites">
                    {d.citations.map((c) => (
                      <li key={`${d.id}-${c.id}`}>
                        <a href={c.url} target="_blank" rel="noopener noreferrer">
                          {c.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                </li>
              ))}
            </ol>
          </section>

          <section className="dl-sources">
            <h2 className="dl-subhead">Official sources used</h2>
            <ul className="dl-source-list">
              {result.sources.map((s) => (
                <li key={s.id}>
                  <a href={s.url} target="_blank" rel="noopener noreferrer">
                    {s.label}
                  </a>
                  {s.note && <span className="dl-source-note"> — {s.note}</span>}
                </li>
              ))}
            </ul>
            <p className="dl-disclaimer">{result.disclaimer}</p>
          </section>
        </>
      )}
    </article>
  );
}

export default DeadlineCalculatorTab;
