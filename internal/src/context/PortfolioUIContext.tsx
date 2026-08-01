import { createContext, useContext } from "react";
import type { Dispatch, SetStateAction } from "react";
import type { TimelineEvent } from "../types/portfolio";

export interface PortfolioUIValue {
  darkMode: boolean;
  setDarkMode: Dispatch<SetStateAction<boolean>>;
  damagesView: string;
  setDamagesView: Dispatch<SetStateAction<string>>;
  showPastEvents: boolean;
  setShowPastEvents: Dispatch<SetStateAction<boolean>>;
  showClock: boolean;
  setShowClock: Dispatch<SetStateAction<boolean>>;
  upcomingEvents: TimelineEvent[];
  timeLeft: { label: string; days: number; hours: number; mins: number; secs: number; urgent: boolean; frozen: boolean };
}

export const PortfolioUIContext = createContext<PortfolioUIValue | null>(null);

export function usePortfolioUI() {
  const value = useContext(PortfolioUIContext);
  if (!value) throw new Error("usePortfolioUI must be used inside ShellLayout");
  return value;
}
