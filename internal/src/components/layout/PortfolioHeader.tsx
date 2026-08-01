import { NavLink } from "react-router-dom";
import { GOLD } from "../../constants";
import { NAV_ITEMS } from "../../routes";
import { withBase } from "../../utils/paths";

export function PortfolioHeader({ darkMode, onToggleTheme, theme }: { darkMode: boolean; onToggleTheme: () => void; theme: any }) {
  return (
    <header className="app-header" style={{ background: theme.headerBg }}>
      <div className="app-container app-header-row">
        <div className="app-brand">
          <img className="app-logo" src={withBase(darkMode ? "/logo-dark.png" : "/logo-light.png")} alt="Newanforbi — In Propria Persona" />
          <div>
            <div className="app-kicker">Interactive case command</div>
            <h1 className="app-title" style={{ color: theme.heading }}>Litigation Portfolio</h1>
            <div style={{ color: GOLD, fontFamily: "var(--font-sans)", fontSize: 10, marginTop: 5 }}>2026 WL 1067541 · 2026 WL 1389969</div>
          </div>
        </div>
        <button className="theme-toggle" onClick={onToggleTheme} aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}>{darkMode ? "☀" : "🌙"}</button>
        <nav className="app-nav" aria-label="Portfolio sections">
          {NAV_ITEMS.map((item) => (
            <NavLink key={item.path} to={item.path} end={item.end} className={({ isActive }) => `app-nav-link${isActive ? " active" : ""}`} style={({ isActive }) => ({ color: isActive ? GOLD : theme.subtleText })}>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
