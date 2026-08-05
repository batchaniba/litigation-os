import { useState } from "react";
import { cases } from "../data/matters";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { isArchivedMatter } from "../utils/matterLifecycle";
import { SavedViews } from "./matters/SavedViews";
import { MatterCard } from "./matters/MatterCard";

const CLUSTER_LABELS = {
  1: "CHP",
  2: "Parole/HOPE",
  3: "Employment",
  4: "Writs",
  5: "Consumer Fraud",
};

export const MattersTab = ({ filteredCases, statusFilter, setStatusFilter, clusterFilter, setClusterFilter, typeFilter, setTypeFilter, searchQuery, setSearchQuery, sortKey, setSortKey }) => {
  const [expandedMatter, setExpandedMatter] = useState(null);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const activeCount = cases.filter(c => !isArchivedMatter(c)).length;
  const statusLabel = statusFilter === "active" ? `Active (${activeCount})` : statusFilter === "upcoming" ? "Upcoming" : statusFilter === "archived" ? "Archived" : "All";
  const clusterLabel = clusterFilter == null ? "All clusters" : CLUSTER_LABELS[clusterFilter];
  const typeLabel = typeFilter ?? "All courts";
  const filterSummary = `${statusLabel} · ${clusterLabel} · ${typeLabel}`;
  const chipStyle = (active) => ({
    padding: "8px 14px", borderRadius: 6,
    border: active ? `1px solid ${GOLD}` : "1px solid var(--filter-inactive-border)",
    background: active ? `${GOLD}18` : "var(--filter-inactive-bg)",
    color: active ? GOLD : "var(--filter-inactive-color)",
    fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600, cursor: "pointer",
  });

  return (
    <div>
      {/* Filters */}
      <div className="matters-filters">
        <div className="matters-filters-toolbar">
          <div className="matters-search-row">
            <input
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search matters…"
              aria-label="Search matters by caption, case number, or keywords"
              className="matters-search-input"
              style={{ border: "1px solid var(--card-border)", background: "var(--input-bg)", color: "var(--input-color)" }}
            />
            <span className="matters-search-endcap" aria-hidden="true" />
          </div>
          <button
            type="button"
            className="matters-filters-toggle"
            aria-expanded={filtersOpen}
            aria-controls="matters-filter-chips"
            onClick={() => setFiltersOpen((open) => !open)}
            style={{ border: `1px solid ${GOLD}55`, background: `${GOLD}12`, color: GOLD }}
          >
            <span aria-hidden="true">{filtersOpen ? "▴" : "▾"}</span>
            <span className="matters-filters-toggle-label">{filtersOpen ? "Hide filters" : "Filters"}</span>
            <span className="matters-filters-toggle-summary">{filterSummary}</span>
            <span className="matters-filters-count">{filteredCases.length} of {cases.length}</span>
          </button>
        </div>
        <div id="matters-filter-chips" className={`matters-filter-chips${filtersOpen ? " is-open" : ""}`}>
          {["active", "upcoming", "archived", "all"].map(s => (
            <button key={s} onClick={() => setStatusFilter(s)} aria-pressed={statusFilter === s} style={chipStyle(statusFilter === s)}>
              {s === "active" ? `Active (${activeCount})` : s === "upcoming" ? "Upcoming" : s === "archived" ? "Archived" : "All"}
            </button>
          ))}
          <span className="matters-filter-sep" style={{ color: "var(--subtle-text)" }}>|</span>
          {[null, 1, 2, 3, 4, 5].map(c => (
            <button key={c ?? "all"} onClick={() => setClusterFilter(c)} aria-pressed={clusterFilter === c} style={chipStyle(clusterFilter === c)}>
              {c === null ? "All" : CLUSTER_LABELS[c]}
            </button>
          ))}
          <span className="matters-filter-sep" style={{ color: "var(--subtle-text)" }}>|</span>
          {[null, "Federal", "State"].map(t => (
            <button key={t ?? "all"} onClick={() => setTypeFilter(t)} aria-pressed={typeFilter === t} style={chipStyle(typeFilter === t)}>
              {t ?? "All"}
            </button>
          ))}
          <span className="matters-filter-result-count" style={{ color: "var(--subtle-text)" }}>{filteredCases.length} of {cases.length}</span>
        </div>
      </div>

      <div className="matter-view-controls">
        <SavedViews
          current={{ status: statusFilter, cluster: clusterFilter, type: typeFilter, query: searchQuery, sort: sortKey }}
          onApply={(view) => { setStatusFilter(view.status); setClusterFilter(view.cluster); setTypeFilter(view.type); setSearchQuery(view.query); setSortKey(view.sort); }}
        />
        <label className="sort-control" style={{ color: "var(--subtle-text)" }}>Sort by
          <select value={sortKey} onChange={(event) => setSortKey(event.target.value)} style={{ background: "var(--input-bg)", borderColor: "var(--card-border)", color: "var(--input-color)" }}>
            <option value="number">Matter number</option><option value="filed">Newest filing</option><option value="deadline">Next deadline</option><option value="exposure">Moderate exposure</option><option value="court">Court</option><option value="status">Status</option>
          </select>
        </label>
      </div>

      <div className="matters-legend">
        Matters marked <strong className="matters-legend-abandoned">ABANDONED</strong> were voluntarily abandoned due to real, credible safety threats.
        Matters marked ⏳ <strong className="matters-legend-pending">PENDING</strong> are prepared but not yet filed, contingent on external timing.
      </div>

      {/* Matter Cards */}
      <div className="matter-card-list">
        {filteredCases.length === 0 ? (
          <div className="matters-empty-state">
            No matters match your current filters.{" "}
            <button
              onClick={() => { setStatusFilter("active"); setClusterFilter(null); setTypeFilter(null); setSearchQuery(""); setSortKey("number"); }}
              className="matters-clear-filters"
            >
              Clear all filters
            </button>
          </div>
        ) : (
          filteredCases.map(c => (
            <MatterCard
              key={c.number}
              matter={c}
              isOpen={expandedMatter === c.number}
              onToggle={() => setExpandedMatter(expandedMatter === c.number ? null : c.number)}
            />
          ))
        )}
      </div>
    </div>
  );
};
