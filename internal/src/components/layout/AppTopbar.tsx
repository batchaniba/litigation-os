export function AppTopbar({ darkMode, onMenu, onSearch, onToggleTheme, theme }: { darkMode: boolean; onMenu: () => void; onSearch: () => void; onToggleTheme: () => void; theme: any }) {
  return (
    <header className="app-topbar" style={{ background: theme.cardBg, borderColor: theme.cardBorder }}>
      <button className="icon-button menu-button" onClick={onMenu} aria-controls="portfolio-navigation" aria-label="Open navigation">☰</button>
      <button className="global-search-trigger" onClick={onSearch} style={{ background: theme.inputBg, borderColor: theme.cardBorder, color: theme.subtleText }} aria-keyshortcuts="Control+K Meta+K /">
        <span>Search the portfolio</span><kbd>⌘ K</kbd>
      </button>
      <button className="icon-button" onClick={onToggleTheme} aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}>{darkMode ? "☀" : "🌙"}</button>
    </header>
  );
}
