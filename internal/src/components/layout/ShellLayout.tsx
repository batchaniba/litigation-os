import { useEffect, useMemo, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { timeline } from "../../data/timeline";
import { ThemeContext, THEMES } from "../../ThemeContext";
import { useDeadlineClock } from "../../hooks/useDeadlineClock";
import { PortfolioUIContext, type PortfolioUIValue } from "../../context/PortfolioUIContext";
import { getPDTMidnight, parseEventDatePDT } from "../../utils/dateUtils";
import { DeadlineBanner } from "./DeadlineBanner";
import { PortfolioHeader } from "./PortfolioHeader";

export function ShellLayout() {
  const [darkMode, setDarkMode] = useState(true);
  const [damagesView, setDamagesView] = useState("moderate");
  const [showPastEvents, setShowPastEvents] = useState(false);
  const [showClock, setShowClock] = useState(false);
  const location = useLocation();
  const theme = THEMES[darkMode ? "dark" : "light"];

  const upcomingEvents = useMemo(() => {
    const today = getPDTMidnight();
    return timeline
      .filter((event) => event.upcoming && parseEventDatePDT(event.date) >= today)
      .sort((a, b) => +parseEventDatePDT(a.date) - +parseEventDatePDT(b.date));
  }, []);
  const timeLeft = useDeadlineClock(upcomingEvents);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "auto" });
  }, [location.pathname]);

  const ui = useMemo<PortfolioUIValue>(() => ({
    darkMode, setDarkMode,
    damagesView, setDamagesView, showPastEvents, setShowPastEvents,
    showClock, setShowClock, upcomingEvents, timeLeft,
  }), [darkMode, damagesView, showPastEvents, showClock, upcomingEvents, timeLeft]);

  return (
    <ThemeContext.Provider value={theme}>
      <PortfolioUIContext.Provider value={ui}>
        <div style={{ minHeight: "100vh", background: theme.bg, color: theme.text }}>
          <PortfolioHeader darkMode={darkMode} onToggleTheme={() => setDarkMode((value) => !value)} theme={theme} />
          <DeadlineBanner timeLeft={timeLeft} showClock={showClock} onToggle={() => setShowClock((value) => !value)} theme={theme} />
          <main className="app-container app-main"><Outlet /></main>
          <footer className="app-footer" style={{ borderColor: theme.footerBorder, color: theme.footerText }}>
            <div className="app-container">Interactive Litigation Portfolio</div>
          </footer>
        </div>
      </PortfolioUIContext.Provider>
    </ThemeContext.Provider>
  );
}
