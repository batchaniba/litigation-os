import { useEffect, useState } from "react";

/** Bumped to v2 so the v1 value (often an accidental OS-light sticky) is ignored. */
export const THEME_STORAGE_KEY = "newanforbi.theme.v2";

/** Resolve the initial theme the same way the inline script in index.html does:
 *  an explicit stored choice wins; otherwise dark. The portfolio is dark-first —
 *  we do not follow prefers-color-scheme, which was sticky-writing "light" for
 *  first-time visitors on light OS themes and breaking the expected first paint.
 *  Keeping the two in agreement is what avoids a flash of the wrong theme. */
export function preferredDarkMode(): boolean {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    if (stored === "light") return false;
    if (stored === "dark") return true;
  } catch {
    // Private browsing or a blocked origin — fall through to the dark default.
  }
  return true;
}

/**
 * Dark-mode state that survives a reload once the user has chosen.
 * Mirrors the choice onto <html data-theme> so the page background is painted
 * correctly before React mounts.
 */
export function useThemePreference() {
  const [darkMode, setDarkMode] = useState(preferredDarkMode);

  useEffect(() => {
    document.documentElement.dataset.theme = darkMode ? "dark" : "light";
    try {
      localStorage.setItem(THEME_STORAGE_KEY, darkMode ? "dark" : "light");
    } catch {
      // Persisting is a convenience; the session still works without it.
    }
  }, [darkMode]);

  return [darkMode, setDarkMode] as const;
}
