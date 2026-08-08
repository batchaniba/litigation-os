import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, Outlet, useLocation } from "react-router";
import upcoming from "../../data/upcoming.json";
import { ThemeContext, THEMES } from "../../ThemeContext";
import { useThemePreference } from "../../hooks/useThemePreference";
import { PortfolioUIContext, type PortfolioUIValue } from "../../context/PortfolioUIContext";
import type { TimelineEvent } from "../../types/portfolio";
import { getPDTMidnight, parseEventDatePDT } from "../../utils/dateUtils";
import { DeadlineBanner } from "./DeadlineBanner";
import { Breadcrumbs } from "./Breadcrumbs";
import { PortfolioHeader } from "./PortfolioHeader";
import { EmptyState, RouteLoading } from "../ui/AsyncState";
import { ErrorBoundary } from "../ui/ErrorBoundary";
import { ROUTES } from "../../routes";

const GlobalSearchDialog = lazy(() => import("../search/GlobalSearchDialog"));

export function ShellLayout() {
  const [darkMode, setDarkMode] = useThemePreference();
  const [damagesView, setDamagesView] = useState("moderate");
  const [showPastEvents, setShowPastEvents] = useState(false);
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
    upcomingEvents,
    // setDarkMode comes from a custom hook, so the linter cannot see that it is a
    // stable useState setter; listing it costs nothing and keeps the rule honest.
  }), [darkMode, setDarkMode, damagesView, showPastEvents, upcomingEvents]);

  return (
    <ThemeContext.Provider value={theme}>
      <PortfolioUIContext.Provider value={ui}>
        <div className={`app-shell${darkMode ? "" : " light"}`} style={{ background: "var(--bg)", color: "var(--text)" }}>
          <a className="skip-link" href="#main-content">Skip to content</a>
          <div className="app-workspace">
            <PortfolioHeader darkMode={darkMode} onSearch={openSearch} onToggleTheme={() => setDarkMode((value) => !value)} />
            <DeadlineBanner upcomingEvents={upcomingEvents} />
            <div className="app-container"><Breadcrumbs /></div>
            <main id="main-content" ref={mainRef} tabIndex={-1} className="app-container app-main">
              {/* Keyed on the path so navigating away from a broken section clears
                  the error. The outer boundary in main.tsx sits above the router
                  and can only offer a reload; this one keeps the chrome alive. */}
              <ErrorBoundary
                resetKey={location.pathname}
                fallback={(error) => (
                  <EmptyState
                    title="This section could not be displayed."
                    detail={error.message}
                    action={<Link className="back-link" to={ROUTES.dashboard}>Back to the dashboard</Link>}
                  />
                )}
              >
                <Outlet />
              </ErrorBoundary>
            </main>
            <footer className="app-footer" style={{ borderColor: "var(--footer-border)", color: "var(--footer-text)" }}><div className="app-container">Interactive Litigation Portfolio</div></footer>
          </div>
          {searchOpen && <Suspense fallback={<RouteLoading label="Loading search" />}><GlobalSearchDialog onClose={closeSearch} /></Suspense>}
        </div>
      </PortfolioUIContext.Provider>
    </ThemeContext.Provider>
  );
}
