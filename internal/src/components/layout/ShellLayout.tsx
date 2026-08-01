import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import upcoming from "../../data/upcoming.json";
import { ThemeContext, THEMES } from "../../ThemeContext";
import { useDeadlineClock } from "../../hooks/useDeadlineClock";
import { PortfolioUIContext, type PortfolioUIValue } from "../../context/PortfolioUIContext";
import type { TimelineEvent } from "../../types/portfolio";
import { getPDTMidnight, parseEventDatePDT } from "../../utils/dateUtils";
import { DeadlineBanner } from "./DeadlineBanner";
import { Breadcrumbs } from "./Breadcrumbs";
import { PortfolioHeader } from "./PortfolioHeader";
import { RouteLoading } from "../ui/AsyncState";

const GlobalSearchDialog = lazy(() => import("../search/GlobalSearchDialog"));

export function ShellLayout() {
  const [darkMode, setDarkMode] = useState(true);
  const [damagesView, setDamagesView] = useState("moderate");
  const [showPastEvents, setShowPastEvents] = useState(false);
  const [showClock, setShowClock] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const location = useLocation();
  const mainRef = useRef<HTMLElement>(null);
  const searchOpenerRef = useRef<HTMLElement | null>(null);
  const theme = THEMES[darkMode ? "dark" : "light"];

  const openSearch = useCallback(() => {
    searchOpenerRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    setSearchOpen(true);
  }, []);
  const closeSearch = useCallback(() => {
    setSearchOpen(false);
    window.requestAnimationFrame(() => searchOpenerRef.current?.focus());
  }, []);

  const upcomingEvents = useMemo(() => {
    const today = getPDTMidnight();
    return (upcoming as TimelineEvent[])
      .filter((event) => parseEventDatePDT(event.date) >= today)
      .sort((a, b) => +parseEventDatePDT(a.date) - +parseEventDatePDT(b.date));
  }, []);
  const timeLeft = useDeadlineClock(upcomingEvents);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "auto" });
    mainRef.current?.focus({ preventScroll: true });
  }, [location.pathname]);

  useEffect(() => {
    const shortcuts = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement;
      const isTyping = /INPUT|TEXTAREA|SELECT/.test(target.tagName) || target.isContentEditable;
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); openSearch(); }
      if (!isTyping && event.key === "/") { event.preventDefault(); openSearch(); }
    };
    document.addEventListener("keydown", shortcuts);
    return () => document.removeEventListener("keydown", shortcuts);
  }, [openSearch]);

  const ui = useMemo<PortfolioUIValue>(() => ({
    darkMode, setDarkMode,
    damagesView, setDamagesView, showPastEvents, setShowPastEvents,
    showClock, setShowClock, upcomingEvents, timeLeft,
  }), [darkMode, damagesView, showPastEvents, showClock, upcomingEvents, timeLeft]);

  return (
    <ThemeContext.Provider value={theme}>
      <PortfolioUIContext.Provider value={ui}>
        <div className="app-shell" style={{ minHeight: "100vh", background: theme.bg, color: theme.text }}>
          <a className="skip-link" href="#main-content">Skip to content</a>
          <div className="app-workspace">
            <PortfolioHeader darkMode={darkMode} onSearch={openSearch} onToggleTheme={() => setDarkMode((value) => !value)} theme={theme} />
            <DeadlineBanner timeLeft={timeLeft} showClock={showClock} onToggle={() => setShowClock((value) => !value)} theme={theme} />
            <div className="app-container"><Breadcrumbs theme={theme} /></div>
            <main id="main-content" ref={mainRef} tabIndex={-1} className="app-container app-main"><Outlet /></main>
            <footer className="app-footer" style={{ borderColor: theme.footerBorder, color: theme.footerText }}><div className="app-container">Interactive Litigation Portfolio</div></footer>
          </div>
          {searchOpen && <Suspense fallback={<RouteLoading label="Loading search" />}><GlobalSearchDialog onClose={closeSearch} /></Suspense>}
        </div>
      </PortfolioUIContext.Provider>
    </ThemeContext.Provider>
  );
}
