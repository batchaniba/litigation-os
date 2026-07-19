import { useState } from "react";
import { GOLD, BODY_GRAY } from "./constants";
import { getPDTMidnight, parseEventDatePDT } from "./utils/dateUtils";
import { useDeadlineClock } from "./hooks/useDeadlineClock";
import { useCaseFilters } from "./hooks/useCaseFilters";
import { PORTFOLIO } from "./data";
import { DashboardTab } from "./components/DashboardTab";
import { MattersTab } from "./components/MattersTab";
import { TimelineTab } from "./components/TimelineTab";
import { DamagesTab } from "./components/DamagesTab";
import { TheoriesTab } from "./components/TheoriesTab";
import { CostOfCounselTab } from "./components/CostOfCounselTab";
import { OutcomesTab } from "./components/OutcomesTab";
import { JudicialOpinionsTab } from "./components/JudicialOpinionsTab";
import { ThemeContext, THEMES } from "./ThemeContext";

const tabs = ["Dashboard", "Matters", "Timeline", "Damages", "Theories", "Cost of Counsel", "Outcomes", "Judicial Opinions"];

export default function LitigationPortfolio() {
  const [darkMode, setDarkMode] = useState(true);
  const theme = THEMES[darkMode ? "dark" : "light"];
  const [activeTab, setActiveTab] = useState("Dashboard");
  const { clusterFilter, setClusterFilter, typeFilter, setTypeFilter, searchQuery, setSearchQuery, filteredCases } = useCaseFilters();
  const [damagesView, setDamagesView] = useState("moderate");
  const [showPastEvents, setShowPastEvents] = useState(false);
  const [showClock, setShowClock] = useState(false);

  const today = getPDTMidnight();
  const upcomingEvents = PORTFOLIO.timeline
    .filter(t => t.upcoming && parseEventDatePDT(t.date) >= today)
    .sort((a, b) => parseEventDatePDT(a.date) - parseEventDatePDT(b.date));

  const timeLeft = useDeadlineClock(upcomingEvents);

  return (
    <ThemeContext.Provider value={theme}>
    <div style={{ minHeight: "100vh", background: theme.bg, color: theme.text, fontFamily: "'Cormorant Garamond', 'Georgia', serif" }}>
      <style>{`@keyframes clockPulse { 0%,100%{opacity:1} 50%{opacity:0.25} }`}</style>

      {/* Header */}
      <div style={{ background: theme.headerBg, borderBottom: `2px solid ${GOLD}` }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "20px 24px 20px", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 16 }}>
          {/* Logo */}
          <img
            src={darkMode ? "/logo-dark.png" : "/logo-light.png"}
            alt="Newanforbi — In Propria Persona"
            style={{ height: 90, width: 90, objectFit: "contain", flexShrink: 0 }}
          />
          <div>
            <div style={{ color: GOLD, fontSize: 11, fontFamily: "'DM Sans', sans-serif", fontWeight: 700, letterSpacing: 4, textTransform: "uppercase", marginBottom: 6 }}>Litigation Portfolio</div>
            <h1 style={{ fontSize: 32, fontWeight: 700, color: theme.headerText, margin: 0, lineHeight: 1.1 }}>Brendan Ngehsi Newanforbi</h1>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: BODY_GRAY, marginTop: 6 }}>Pro Se / In Propria Persona · Prepared {PORTFOLIO.prepared_date}</div>
          </div>
          {/* Westlaw Accolade */}
          <div style={{ flex: 1, display: "flex", alignItems: "flex-end", justifyContent: "flex-start", paddingLeft: 28, minWidth: 0 }}>
            <div>
              <div style={{ fontSize: 9, fontFamily: "'DM Sans', sans-serif", fontWeight: 700, letterSpacing: 3, color: GOLD, textTransform: "uppercase", marginBottom: 6 }}>
                📚 Westlaw-Indexed
              </div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontStyle: "italic", color: BODY_GRAY, lineHeight: 1.6, marginBottom: 6, maxWidth: 380 }}>
                "In this regard, it appears from a search of Westlaw that Plaintiff filed two other lawsuits in federal court that have resulted in opinions available on Westlaw."
              </div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700, color: GOLD, letterSpacing: 0.5, marginBottom: 4 }}>
                2026 WL 1067541 · 2026 WL 1389969
              </div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 9, color: BODY_GRAY, opacity: 0.8, lineHeight: 1.5 }}>
                — Blaze Van Dine, Esq. · Sims, Lawrence &amp; Broghammer
              </div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 9, color: BODY_GRAY, opacity: 0.6 }}>
                Palacios Demurrer (Matter 5)
              </div>
            </div>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
              {tabs.map(t => (
                <button key={t} onClick={() => setActiveTab(t)} aria-current={activeTab === t ? "page" : undefined} style={{
                  padding: "8px 18px", borderRadius: 6,
                  border: activeTab === t ? theme.tabActive.border : theme.tabInactive.border,
                  background: activeTab === t ? theme.tabActive.bg : theme.tabInactive.bg,
                  color: activeTab === t ? theme.tabActive.color : theme.tabInactive.color,
                  fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, cursor: "pointer", transition: "all 0.2s",
                  letterSpacing: 0.5
                }}>{t}</button>
              ))}
            </div>
            <button
              onClick={() => setDarkMode(v => !v)}
              aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
              title={darkMode ? "Light mode" : "Dark mode"}
              style={{
                padding: "7px 10px", borderRadius: 6, border: `1px solid ${GOLD}44`,
                background: "transparent", color: GOLD, fontSize: 16, cursor: "pointer",
                lineHeight: 1, transition: "all 0.2s", flexShrink: 0,
              }}
            >
              {darkMode ? "☀" : "🌙"}
            </button>
          </div>
        </div>
      </div>

      {/* Deadline Clock Banner */}
      <div style={{
        background: theme.bannerBg,
        borderBottom: `1px solid ${timeLeft.urgent ? "#EF444440" : GOLD + "30"}`,
      }}>
      <div style={{
        maxWidth: 1200, margin: "0 auto", padding: "10px 24px",
        display: "flex", alignItems: "center", justifyContent: "center", gap: 28, flexWrap: "wrap",
        position: "relative"
      }}>
        <div style={{ color: GOLD, fontSize: 10, fontFamily: "'DM Sans', sans-serif", fontWeight: 700, letterSpacing: 3, textTransform: "uppercase", whiteSpace: "nowrap" }}>
          ⚖ Deadline Clock
        </div>
        {/* Screen-reader announcement for clock (updates every minute is sufficient) */}
        <div aria-live="polite" aria-atomic="true" style={{ position: "absolute", width: 1, height: 1, overflow: "hidden", clip: "rect(0,0,0,0)", whiteSpace: "nowrap" }}>
          {showClock && timeLeft.label ? `Deadline: ${timeLeft.label}. ${timeLeft.days} days, ${timeLeft.hours} hours, ${timeLeft.mins} minutes remaining.` : ""}
        </div>
        {showClock && <>
          <div aria-hidden="true" style={{ display: "flex", gap: 4, alignItems: "center" }}>
            {[{ v: timeLeft.days, l: "Days" }, { v: timeLeft.hours, l: "Hrs" }, { v: timeLeft.mins, l: "Min" }, { v: timeLeft.secs, l: "Sec" }].map(({ v, l }, i) => (
              <div key={l} style={{ display: "flex", alignItems: "center", gap: 4 }}>
                {i > 0 && <span style={{ color: "#334155", fontSize: 18, lineHeight: 1, paddingBottom: 10 }}>:</span>}
                <div style={{ textAlign: "center", minWidth: 36 }}>
                  <div style={{ fontSize: 22, fontWeight: 700, color: timeLeft.frozen ? "#EF4444" : timeLeft.urgent ? "#EF4444" : "white", fontFamily: "'DM Sans', sans-serif", lineHeight: 1, animation: timeLeft.frozen ? "clockPulse 2.8s ease-in-out infinite" : "none" }}>
                    {String(v).padStart(2, "0")}
                  </div>
                  <div style={{ fontSize: 9, color: "#475569", fontFamily: "'DM Sans', sans-serif", letterSpacing: 1.5, textTransform: "uppercase", marginTop: 2 }}>{l}</div>
                </div>
              </div>
            ))}
          </div>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: "#94A3B8", maxWidth: 380, textAlign: "center", lineHeight: 1.4 }}>
            {timeLeft.label}
          </div>
        </>}
        <button onClick={() => setShowClock(v => !v)} aria-expanded={showClock} aria-controls="deadline-clock-display" style={{
          position: "absolute", right: 16, top: "50%", transform: "translateY(-50%)",
          padding: "4px 10px", borderRadius: 5,
          border: theme.clockBtn.border,
          background: "transparent", color: theme.clockBtn.color, fontFamily: "'DM Sans', sans-serif",
          fontSize: 10, fontWeight: 600, cursor: "pointer", letterSpacing: 0.5, textTransform: "uppercase"
        }}>
          {showClock ? "Hide" : "Show"}
        </button>
      </div>
      </div>

      {/* Tab content */}
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "24px 24px 60px" }}>
        {activeTab === "Dashboard" && <DashboardTab upcomingEvents={upcomingEvents} setClusterFilter={setClusterFilter} setActiveTab={setActiveTab} />}
        {activeTab === "Matters"   && <MattersTab filteredCases={filteredCases} clusterFilter={clusterFilter} setClusterFilter={setClusterFilter} typeFilter={typeFilter} setTypeFilter={setTypeFilter} searchQuery={searchQuery} setSearchQuery={setSearchQuery} />}
        {activeTab === "Timeline"  && <TimelineTab showPastEvents={showPastEvents} setShowPastEvents={setShowPastEvents} />}
        {activeTab === "Damages"   && <DamagesTab damagesView={damagesView} setDamagesView={setDamagesView} />}
        {activeTab === "Theories"  && <TheoriesTab />}
        {activeTab === "Cost of Counsel" && <CostOfCounselTab />}
        {activeTab === "Outcomes" && <OutcomesTab />}
        {activeTab === "Judicial Opinions" && <JudicialOpinionsTab />}
      </div>

      {/* Footer */}
      <div style={{ borderTop: `1px solid ${theme.footerBorder}` }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "16px 24px", fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.footerText }}>
          <span>Confidential — Attorney Work Product</span>
        </div>
      </div>
    </div>
    </ThemeContext.Provider>
  );
}
