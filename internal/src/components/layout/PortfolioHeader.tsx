import { NavLink } from "react-router-dom";
import { BODY_GRAY, GOLD } from "../../constants";
import { NAV_ITEMS } from "../../routes";
import { withBase } from "../../utils/paths";

export function PortfolioHeader({ darkMode, onToggleTheme, theme }: { darkMode: boolean; onToggleTheme: () => void; theme: any }) {
  return (
    <header className="legacy-header" style={{ background: theme.headerBg, borderBottom: `2px solid ${GOLD}` }}>
      <div className="legacy-header-inner">
        <img
          className="legacy-brand-logo"
          src={withBase(darkMode ? "/logo-dark.png" : "/logo-light.png")}
          alt="Newanforbi — In Propria Persona"
        />

        <div className="legacy-header-main">
          <div className="legacy-westlaw">
            <div style={{ fontSize: 9, fontFamily: "'DM Sans', sans-serif", fontWeight: 700, letterSpacing: 3, color: GOLD, textTransform: "uppercase", marginBottom: 6 }}>
              📚 Westlaw-Indexed
            </div>
            <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontStyle: "italic", color: BODY_GRAY, lineHeight: 1.6, marginBottom: 6, maxWidth: 380 }}>
              “In this regard, it appears from a search of Westlaw that Plaintiff filed two other lawsuits in federal court that have resulted in opinions available on Westlaw.”
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

          <div className="legacy-opposing-counsel">
            <a href="https://www.sims-law.net/" target="_blank" rel="noopener noreferrer" title="Visit Sims, Lawrence & Broghammer (sims-law.net) ↗" className="firm-link">
              <div className="legacy-counsel-names">
                <div>Bryan Malone</div>
                <div>Blaze Van Dine</div>
                <div className="firm-external-hint">Visit site ↗</div>
              </div>
              <img className="firm-logo" src={withBase(darkMode ? "/branding/slb-dark.png" : "/branding/slb-light.png")} alt="Sims, Lawrence & Broghammer" style={{ height: darkMode ? 62 : 42, width: "auto" }} />
            </a>
            <a href="https://www.garciagurney.com/" target="_blank" rel="noopener noreferrer" title="Visit Garcia & Gurney, A Law Corporation (garciagurney.com) ↗" className="firm-link">
              <div className="legacy-counsel-names">
                <div>Melinda Garcia</div>
                <div className="firm-external-hint">Visit site ↗</div>
              </div>
              <img className="firm-logo legacy-garcia-logo" src={withBase(darkMode ? "/branding/garcia-gurney-dark.png" : "/branding/garcia-gurney.png")} alt="Garcia & Gurney, A Law Corporation" />
            </a>
            <a href="https://oag.ca.gov/dag-recruitment" target="_blank" rel="noopener noreferrer" title="Visit California Attorney General's Office — Deputy Attorney General recruitment (oag.ca.gov) ↗" className="firm-link">
              <div className="legacy-counsel-names">
                {["Haiyang A. Li", "Erick Rhoan", "Vanessa Ing", "Mark Beckington", "Judith S. Gronna", "Anthony Hakl"].map((name) => <div key={name}>{name}</div>)}
                <div className="firm-external-hint">Visit site ↗</div>
              </div>
              <img className="firm-logo legacy-dag-logo" src={withBase(darkMode ? "/branding/dag-dark.jpg" : "/branding/dag-light.jpg")} alt="California Department of Justice, Office of the Attorney General" />
            </a>
          </div>
        </div>

        <div className="legacy-header-controls">
          <button className="legacy-theme-toggle" onClick={onToggleTheme} aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"} title={darkMode ? "Light mode" : "Dark mode"}>
            {darkMode ? "☀" : "🌙"}
          </button>
          <nav className="legacy-navigation" aria-label="Portfolio sections">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.end}
                className="legacy-nav-link"
                style={({ isActive }) => ({
                  border: isActive ? theme.tabActive.border : theme.tabInactive.border,
                  background: isActive ? theme.tabActive.bg : theme.tabInactive.bg,
                  color: isActive ? theme.tabActive.color : theme.tabInactive.color,
                })}
              >
                {item.path === "/outcomes" ? "Profit" : item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
