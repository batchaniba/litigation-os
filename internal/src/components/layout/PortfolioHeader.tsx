import { useEffect, useId, useState } from "react";
import { NavLink, useLocation } from "react-router";
import { GOLD } from "../../constants";
import { NAV_ITEMS } from "../../routes";
import { withBase } from "../../utils/paths";
import { CoverageTower } from "../CoverageTower";
import { headline_coverage } from "../../data/coverage";

export function PortfolioHeader({
  darkMode,
  onSearch,
  onToggleTheme,
}: {
  darkMode: boolean;
  onSearch: () => void;
  onToggleTheme: () => void;
}) {
  const location = useLocation();
  const navId = useId();
  const [menuOpen, setMenuOpen] = useState(false);
  const [menuPath, setMenuPath] = useState(location.pathname);
  const activeLabel = NAV_ITEMS.find((item) =>
    item.end ? location.pathname === item.path : location.pathname === item.path || location.pathname.startsWith(`${item.path}/`)
  )?.label ?? "Dashboard";

  // Close the mobile section menu on navigation without an effect round-trip
  // (eslint-plugin-react-hooks@7 set-state-in-effect).
  if (menuPath !== location.pathname) {
    setMenuPath(location.pathname);
    if (menuOpen) setMenuOpen(false);
  }

  useEffect(() => {
    const onResize = () => {
      if (window.matchMedia("(min-width: 761px)").matches) setMenuOpen(false);
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  return (
    <header className="legacy-header" style={{ background: "var(--header-bg)", borderBottom: `2px solid ${GOLD}` }}>
      <div className="legacy-header-inner">
        <img
          className="legacy-brand-logo"
          src={withBase(darkMode ? "/logo-dark.png" : "/logo-light.png")}
          alt="Newanforbi — In Propria Persona"
        />

        <span className="legacy-versus" aria-hidden="true">
          <span className="legacy-versus-letter">V</span>
          <span className="legacy-versus-dot">.</span>
        </span>
        <span className="sr-only">versus</span>

        <div className="legacy-header-main">
          <div className="legacy-westlaw">
            <div className="legacy-westlaw-label">📚 Westlaw-Indexed</div>
            <div className="legacy-westlaw-quote">
              “In this regard, it appears from a search of Westlaw that Plaintiff filed two other lawsuits in federal court that have resulted in opinions available on Westlaw.”
            </div>
            <div className="legacy-westlaw-cite">
              2026 WL 1067541 · 2026 WL 1389969
            </div>
            <div className="legacy-westlaw-attribution">
              — Blaze Van Dine, Esq. · Sims, Lawrence &amp; Broghammer
            </div>
            <div className="legacy-westlaw-source">
              Palacios Demurrer (Matter 5)
            </div>
          </div>

          {headline_coverage && <CoverageTower record={headline_coverage} variant="header" />}

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
                {[
                  "Haiyang A. Li",
                  "Erick Rhoan",
                  "Vanessa Ing",
                  "Mark Beckington",
                  "Judith S. Gronna",
                  "Anthony Hakl",
                ].map((name) => <div key={name}>{name}</div>)}
                <div className="firm-external-hint">Visit site ↗</div>
              </div>
              <img className="firm-logo legacy-dag-logo" src={withBase(darkMode ? "/branding/dag-dark.jpg" : "/branding/dag-light.jpg")} alt="California Department of Justice, Office of the Attorney General" />
            </a>
          </div>
        </div>

        <div className="legacy-header-controls">
          <div className="legacy-header-actions">
            <button
              className="legacy-search-trigger"
              onClick={onSearch}
              style={{ background: "var(--input-bg)", borderColor: "var(--card-border)", color: "var(--subtle-text)" }}
              aria-keyshortcuts="Control+K Meta+K /"
            >
              <span>Search the portfolio</span><kbd>⌘ K</kbd>
            </button>
            <button className="legacy-theme-toggle" onClick={onToggleTheme} aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"} title={darkMode ? "Light mode" : "Dark mode"}>
              {darkMode ? "☀" : "🌙"}
            </button>
          </div>
          <button
            type="button"
            className="legacy-nav-menu-toggle"
            aria-expanded={menuOpen}
            aria-controls={navId}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <span aria-hidden="true">{menuOpen ? "▴" : "▾"}</span>
            <span>{menuOpen ? "Hide sections" : `Sections · ${activeLabel}`}</span>
          </button>
          <nav id={navId} className={`legacy-navigation${menuOpen ? " is-open" : ""}`} aria-label="Portfolio sections">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.end}
                className="legacy-nav-link"
                style={({ isActive }) => ({
                  border: isActive ? "var(--tab-active-border)" : "var(--tab-inactive-border)",
                  background: isActive ? "var(--tab-active-bg)" : "var(--tab-inactive-bg)",
                  color: isActive ? "var(--tab-active-color)" : "var(--tab-inactive-color)",
                })}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
