import { useMemo, useState } from "react";
import { Link } from "react-router";
import { cases } from "../data/matters";
import { CLUSTERS, CLUSTER_LABELS } from "../data/clusters";
import { jurisdictions } from "../data/portfolioMeta";
import { outcomes } from "../data/outcomes";
import { useNextActions } from "../hooks/useNextActions";
import syncState from "../data/courtlistener/sync-state.json";
import indexMeta from "../data/index/matters.json";
import { countCourts } from "../utils/portfolioStats";
import {
  agendaCounts,
  agendaWeeks,
  DASHBOARD_HORIZON_DAYS,
  horizonEndKey,
  monthStrip,
  weeksToCover,
  needsAttention,
  nextCourtDate,
  shortCourt,
  shortDate,
  stageBoard,
  syncAgeDays,
} from "./dashboard/dashboardModel";

// Static, data-derived figures (no clock dependency).
const CLUSTER_COLOR = Object.fromEntries(CLUSTERS.map((cl) => [cl.n, cl.color]));
const clusterCounts = CLUSTERS.map((cl) => ({
  ...cl,
  count: cases.filter((c) => c.cluster === cl.n).length,
}));
const courtCounts = countCourts(cases, jurisdictions);
const openCounts = {
  inCourt: cases.filter((c) => c.lifecycle === "active" && !c.archived).length,
  preFiling: cases.filter((c) => c.lifecycle === "pre_filing" && !c.archived).length,
  settled: cases.filter((c) => c.lifecycle === "settled").length,
};
openCounts.total = openCounts.inCourt + openCounts.preFiling + openCounts.settled;
const closedCounts = {
  dismissed: cases.filter((c) => c.lifecycle === "dismissed").length,
  abandoned: cases.filter((c) => c.lifecycle === "abandoned").length,
  closed: cases.filter((c) => c.lifecycle === "closed").length,
};
closedCounts.total = closedCounts.dismissed + closedCounts.abandoned + closedCounts.closed;

const settlements = (outcomes.realized ?? []).filter((r) => r.type === "settlement");
const settledCaptions = settlements.map((r) => {
  const m = cases.find((c) => Number(c.number) === Number(r.matter));
  return { matter: r.matter, date: r.date, name: m ? m.caption.replace(/^.*?\sv\.\s+/, "").split(",")[0] : `Matter ${r.matter}` };
});
const highlightRulings = (outcomes.judicial_opinions ?? [])
  .filter((j) => j.dashboard_headline)
  .slice(0, 2);

const TONE_CLASS = { task: "task", court: "court", confer: "confer", theirs: "theirs" };
const FILTERS = [
  { key: "all", label: "Everything" },
  { key: "mine", label: "My moves" },
  { key: "court", label: "Court dates" },
];

function MatterChip({ label }) {
  return <span className="dash-mchip">{label}</span>;
}

function VerbChip({ verb }) {
  return <span className={`dash-verb ${TONE_CLASS[verb.tone] ?? "task"}`}>{verb.label}</span>;
}

function matterHref(item) {
  return item.matters?.length ? `/matters/${item.matters[0]}` : "/matters";
}

export const DashboardTab = ({ setClusterFilter, setActiveTab }) => {
  const { queue, today } = useNextActions(DASHBOARD_HORIZON_DAYS);
  const [filter, setFilter] = useState("all");

  const attention = useMemo(() => needsAttention(queue, cases), [queue]);
  const horizonDays = DASHBOARD_HORIZON_DAYS;
  const horizonEnd = shortDate(horizonEndKey(today, horizonDays));
  const stripWeeks = weeksToCover(today, horizonDays);
  const weeks = useMemo(() => agendaWeeks(queue, cases, { filter, horizonDays }), [queue, filter, horizonDays]);
  const counts = useMemo(() => agendaCounts(queue, horizonDays), [queue, horizonDays]);
  const strip = useMemo(() => monthStrip(queue, stripWeeks), [queue, stripWeeks]);
  const board = useMemo(() => stageBoard(cases, queue), [queue]);
  const court = useMemo(() => nextCourtDate(queue, cases), [queue]);

  const clLast = Object.values(syncState?.matters ?? {})
    .map((row) => row?.last_synced_at)
    .filter(Boolean)
    .sort()
    .at(-1);
  const clLastDay = typeof clLast === "string" ? clLast.slice(0, 10) : null;
  const syncAge = syncAgeDays(clLastDay, today);
  const asOf = indexMeta?.today ?? null;
  const longToday = new Date(`${today}T12:00:00Z`).toLocaleDateString("en-US", {
    weekday: "long", month: "long", day: "numeric", year: "numeric", timeZone: "UTC",
  });

  const pickCluster = (n) => {
    setClusterFilter(n);
    setActiveTab?.("Matters");
  };

  const attnSummary = [
    attention.overdue ? `${attention.overdue} past due` : null,
    attention.soon ? `${attention.soon} in the next 3 days` : null,
    attention.opposingOverdue ? `${attention.opposingOverdue} overdue on their side` : null,
  ].filter(Boolean).join(" · ");

  return (
    <div className="dash">
      {/* Title row */}
      <section className="dash-head">
        <div>
          <div className="dash-eyebrow">{longToday}</div>
          <h1 className="dash-title">Docket at a glance</h1>
          <p className="dash-lede">
            What is due, where each case stands, and what the record shows — {openCounts.total} open matters, all pro se.
          </p>
        </div>
        <div className="dash-chips" role="status">
          <span className={`dash-chip ${asOf ? "ok" : "warn"}`}>
            {asOf ? `Clocks verified ${shortDate(asOf)}` : "Clock date unknown"}
          </span>
          <span className={`dash-chip ${syncAge != null && syncAge <= 14 ? "ok" : "warn"}`}>
            {syncAge == null
              ? "Docket sync not run"
              : syncAge === 0
                ? "Docket synced today"
                : `Docket sync ${syncAge} ${syncAge === 1 ? "day" : "days"} old (${shortDate(clLastDay)})`}
          </span>
        </div>
      </section>

      {/* Needs attention + pulse */}
      <section className="dash-row">
        <div className="dash-card dash-attn">
          <div className="dash-card-head">
            <h2 className="dash-h2">Needs attention</h2>
            <span className="dash-meta">{attnSummary || "Nothing past due"}</span>
          </div>
          {attention.items.length === 0 ? (
            <p className="dash-empty">Nothing on your desk is past due or due in the next three days.</p>
          ) : (
            <ul className="dash-attn-list">
              {attention.items.map((item) => (
                <li key={item.key}>
                  <Link to={matterHref(item)} className="dash-attn-row">
                    <span className="dash-attn-when">
                      <span className={`dash-attn-rel ${item.tone}`}>{item.relative}</span>
                      <span className="dash-meta">{shortDate(item.dateKey)}</span>
                    </span>
                    <MatterChip label={item.matterLabel} />
                    <span className="dash-attn-body">
                      <span className="dash-attn-title">{item.title}</span>
                      <span className="dash-meta">{item.verb.label} · {item.meta}</span>
                    </span>
                    <svg className="dash-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="dash-pulse">
          <div className="dash-card dash-pulse-wide">
            <div className="dash-card-head">
              <span className="dash-label">Open matters</span>
              <Link to="/matters?status=all" className="dash-link">All {cases.length} →</Link>
            </div>
            <div className="dash-big">{openCounts.total}</div>
            <div className="dash-stack" aria-hidden="true">
              <span style={{ flex: openCounts.inCourt }} className="in-court" />
              <span style={{ flex: openCounts.preFiling }} className="pre-filing" />
              <span style={{ flex: openCounts.settled }} className="settled" />
            </div>
            <div className="dash-legend">
              <span><i className="in-court" />{openCounts.inCourt} in court</span>
              <span><i className="pre-filing" />{openCounts.preFiling} pre-filing</span>
              <span><i className="settled" />{openCounts.settled} settled</span>
            </div>
          </div>
          <div className="dash-card">
            <span className="dash-label">Next court date</span>
            <div className="dash-mid">{court ? shortDate(court.dateKey) : "—"}</div>
            <div className="dash-meta dash-stat-sub">
              {court ? `${court.title.split(" — ")[0]} · ${court.matterLabel}${court.meta ? ` · ${court.meta.split(" · ").slice(1).join(" · ")}` : ""}` : "None on the calendar"}
            </div>
          </div>
          <div className="dash-card">
            <span className="dash-label">Recoveries</span>
            <div className="dash-mid">{settlements.length} settled</div>
            <div className="dash-meta dash-stat-sub">
              {settlements.length
                ? `Matters ${settlements.map((s) => s.matter).join(" and ")} · terms confidential`
                : "None yet"}
            </div>
          </div>
        </div>
      </section>

      {/* Look-ahead through the horizon end */}
      <section className="dash-section">
        <div className="dash-section-head">
          <h2 className="dash-h2 lg">Through {horizonEnd}</h2>
          <div className="dash-filters" role="group" aria-label="Filter the agenda">
            {FILTERS.map((f) => (
              <button
                key={f.key}
                type="button"
                aria-pressed={filter === f.key}
                className={`dash-filter${filter === f.key ? " on" : ""}`}
                onClick={() => setFilter(f.key)}
              >
                {f.label} · {counts[f.key]}
              </button>
            ))}
          </div>
        </div>

        <div className="dash-row top">
          <div className="dash-card dash-month">
            <div className="dash-card-head">
              <span className="dash-month-label">{strip.label}</span>
              <span className="dash-meta">{stripWeeks} weeks</span>
            </div>
            <div className="dash-month-dow" aria-hidden="true">
              {["S", "M", "T", "W", "T", "F", "S"].map((d, i) => <span key={i}>{d}</span>)}
            </div>
            <div className="dash-month-grid">
              {strip.days.map((d) => (
                <div
                  key={d.key}
                  className={`dash-day${d.today ? " today" : ""}${d.past ? " past" : ""}`}
                  aria-label={`${shortDate(d.key)}${d.tones.length ? `, ${d.tones.length} item${d.tones.length === 1 ? "" : "s"}` : ""}`}
                >
                  <span className="dash-day-n">{d.label}</span>
                  <span className="dash-dots">
                    {d.tones.map((t, i) => <i key={i} className={t} />)}
                  </span>
                </div>
              ))}
            </div>
            <div className="dash-legend small">
              <span><i className="dot task" />File / serve</span>
              <span><i className="dot court" />Court date</span>
              <span><i className="dot confer" />Meet &amp; confer</span>
              <span><i className="dot theirs" />Their move</span>
            </div>
          </div>

          <div className="dash-card dash-agenda">
            {weeks.length === 0 ? (
              <p className="dash-empty">Nothing through {horizonEnd} for this filter.</p>
            ) : weeks.map((w) => (
              <div key={w.start} className="dash-week">
                <div className="dash-week-head">
                  <span className="dash-eyebrow sm">{w.label}</span>
                  {w.range ? <span className="dash-meta">{w.range}</span> : null}
                </div>
                <ul>
                  {w.rows.map((r) => (
                    <li key={r.key} className={`dash-agenda-row${r.verb.tone === "theirs" ? " theirs" : ""}`}>
                      <span className="dash-agenda-date">
                        <span className="dow">{r.when.dow}</span>
                        <span className="md">{r.when.label.split(" ").slice(1).join(" ")}</span>
                      </span>
                      <span className="dash-agenda-chips">
                        <MatterChip label={r.matterLabel} />
                        <VerbChip verb={r.verb} />
                      </span>
                      <Link to={matterHref(r)} className="dash-agenda-title">{r.title}</Link>
                      <span className="dash-agenda-meta">{r.meta}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stage board */}
      <section className="dash-section">
        <div className="dash-section-head">
          <h2 className="dash-h2 lg">Where every case stands</h2>
          <span className="dash-meta">{board.total} open matters by stage · amber means nothing dated on the calendar</span>
        </div>
        <div className="dash-board" role="list" style={{ "--lanes": board.lanes.length }}>
          {board.lanes.map((lane) => (
            <div key={lane.key} className="dash-lane" role="listitem">
              <div className="dash-lane-head">
                <span>{lane.name}</span>
                <span className="dash-meta">{lane.items.length}</span>
              </div>
              <div className="dash-lane-items">
                {lane.items.map((c) => (
                  <Link key={c.number} to={`/matters/${c.number}`} className="dash-mcard">
                    <span className="dash-mcard-top">
                      <i style={{ background: CLUSTER_COLOR[c.cluster] ?? "#94a3b8" }} aria-hidden="true" />
                      <span className="num">M{c.number}</span>
                    </span>
                    <span className="dash-mcard-name">{c.name}</span>
                    <span className={`dash-mcard-line ${c.tone}`}>{c.line}</span>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="dash-board-foot">
          <div className="dash-legend small">
            {CLUSTERS.map((cl) => (
              <span key={cl.n}><i style={{ background: cl.color }} />{CLUSTER_LABELS[cl.n] ?? cl.label}</span>
            ))}
          </div>
          <Link to="/matters?status=archived" className="dash-link">
            {closedCounts.total} closed matters — {closedCounts.dismissed} dismissed · {closedCounts.abandoned} abandoned · {closedCounts.closed} closed →
          </Link>
        </div>
      </section>

      {/* Record + mix */}
      <section className="dash-row">
        <div className="dash-record">
          <h2 className="dash-h2 lg">The record so far</h2>
          <div className="dash-record-tiles">
            <div className="dash-card dash-tile">
              <span className="dash-label green">Settled</span>
              <div className="dash-mid">{settlements.length} {settlements.length === 1 ? "matter" : "matters"}</div>
              <p className="dash-tile-copy">
                {settledCaptions.map((s) => `${s.name} (M${s.matter}), ${s.date}`).join(". ")}. Terms confidential.
              </p>
            </div>
            {highlightRulings.map((j) => {
              const m = cases.find((c) => Number(c.number) === Number(j.matter));
              return (
                <Link key={`${j.matter}-${j.date}`} to={`/matters/${j.matter}`} className="dash-card dash-tile">
                  <span className="dash-label blue">{j.dashboard_label}</span>
                  <div className="dash-mid">{m ? m.caption.replace(/^.*?\sv\.\s+/, "").split(",")[0] : `Matter ${j.matter}`}</div>
                  <p className="dash-tile-copy">{j.dashboard_headline} (M{j.matter})</p>
                </Link>
              );
            })}
          </div>
        </div>

        <div className="dash-mix">
          <h2 className="dash-h2 lg">Portfolio mix</h2>
          <div className="dash-card">
            <div className="dash-card-head">
              <span className="dash-meta">{cases.length} matters by cluster — select one to filter</span>
            </div>
            <div className="dash-clusterbar">
              {clusterCounts.map((cl) => (
                <button
                  key={cl.n}
                  type="button"
                  style={{ flex: Math.max(cl.count, 0.5), background: cl.color }}
                  onClick={() => pickCluster(cl.n)}
                  aria-label={`Filter matters by cluster: ${cl.label} (${cl.count})`}
                  title={`${cl.label} — ${cl.count}`}
                />
              ))}
            </div>
            <div className="dash-cluster-list">
              {clusterCounts.map((cl) => (
                <button key={cl.n} type="button" className="dash-cluster-btn" onClick={() => pickCluster(cl.n)} title={cl.label}>
                  <i style={{ background: cl.color }} aria-hidden="true" />
                  <span>{CLUSTER_LABELS[cl.n] ?? cl.label}</span>
                  <span className="dash-meta">{cl.count}</span>
                </button>
              ))}
            </div>
            <div className="dash-courts">
              {jurisdictions.map((j) => (
                <div key={j} className="dash-court">
                  <span className="dash-court-n">{courtCounts[j] || 0}</span>
                  <span className="dash-meta">{shortCourt(j)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <footer className="dash-foot">
        <span>Dates as recorded in the portfolio. Confirm against the docket before relying on a date.</span>
        <details>
          <summary>How dates are counted</summary>
          <p>
            Dates come from each matter&apos;s live calendar, bucketed from today&apos;s Pacific date. The week runs Sunday through
            Saturday. Vacated, satisfied, settled, and archived items are left out. A date the other side owes is marked
            &ldquo;Their move.&rdquo; Matters with nothing dated show their latest status in amber on the stage board.
          </p>
        </details>
      </footer>
    </div>
  );
};
