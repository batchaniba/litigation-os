import { useEffect, useState } from "react";

export const THEME_STORAGE_KEY = "newanforbi.theme.v1";

/** Resolve the initial theme the same way the inline script in index.html does:
 *  an explicit stored choice wins, otherwise follow the OS, otherwise dark.
 *  Keeping the two in agreement is what avoids a flash of the wrong theme. */
export function preferredDarkMode(): boolean {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    if (stored === "dark") return true;
    if (stored === "light") return false;
  } catch {
    // Private browsing or a blocked origin — fall through to the OS preference.
  }
  return !window.matchMedia?.("(prefers-color-scheme: light)").matches;
}

/**
 * Dark-mode state that survives a reload and follows the OS when the user has
 * not chosen. Mirrors the choice onto <html data-theme> so the page background
 * is painted correctly before React mounts.
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
