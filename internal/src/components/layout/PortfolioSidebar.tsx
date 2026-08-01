import { NavLink } from "react-router-dom";
import { NAV_ITEMS } from "../../routes";
import { withBase } from "../../utils/paths";

export function PortfolioSidebar({ darkMode, open, onNavigate, theme }: { darkMode: boolean; open: boolean; onNavigate: () => void; theme: any }) {
  const groups = [...new Set(NAV_ITEMS.map((item) => item.group))];
  return (
    <aside id="portfolio-navigation" className={`app-sidebar${open ? " open" : ""}`} style={{ background: theme.headerBg, borderColor: theme.cardBorder }} aria-label="Portfolio navigation">
      <div className="sidebar-brand">
        <img className="sidebar-logo" src={withBase(darkMode ? "/logo-dark.png" : "/logo-light.png")} alt="Newanforbi — In Propria Persona" />
        <div><div className="app-kicker">Case command</div><div className="sidebar-title" style={{ color: theme.heading }}>Litigation Portfolio</div></div>
      </div>
      <nav className="sidebar-nav">
        {groups.map((group) => (
          <section key={group} aria-labelledby={`nav-${group.toLowerCase()}`}>
            <h2 id={`nav-${group.toLowerCase()}`} className="sidebar-group">{group}</h2>
            {NAV_ITEMS.filter((item) => item.group === group).map((item) => (
              <NavLink key={item.path} to={item.path} end={item.end} onClick={onNavigate} className={({ isActive }) => `sidebar-link${isActive ? " active" : ""}`} style={({ isActive }) => ({ color: isActive ? "var(--gold)" : theme.secondaryText, background: isActive ? "rgb(200 168 75 / 10%)" : "transparent" })}>
                <span className="sidebar-icon" aria-hidden="true">{item.icon}</span><span>{item.label}</span>
              </NavLink>
            ))}
          </section>
        ))}
      </nav>
      <div className="sidebar-footer" style={{ color: theme.subtleText }}>2026 WL 1067541<br />2026 WL 1389969</div>
    </aside>
  );
}
