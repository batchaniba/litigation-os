import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { usePortfolioToday } from "./usePortfolioToday";

describe("usePortfolioToday", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it("reads the viewer's America/Los_Angeles civil date, not UTC", () => {
    vi.useFakeTimers();
    // 01:00 UTC Nov 2 is still Nov 1 in California (PST).
    vi.setSystemTime(new Date("2026-11-02T01:00:00.000Z"));
    const { result } = renderHook(() => usePortfolioToday());
    expect(result.current).toBe("2026-11-01");
  });

  it("rolls to the next PT day at Pacific midnight", () => {
    vi.useFakeTimers();
    // 23:59:00 PDT on Wednesday Oct 28, 2026.
    vi.setSystemTime(new Date("2026-10-29T06:59:00.000Z"));
    const { result } = renderHook(() => usePortfolioToday());
    expect(result.current).toBe("2026-10-28");

    act(() => {
      vi.advanceTimersByTime(70_000);
    });
    expect(result.current).toBe("2026-10-29");
  });

  it("recomputes when the tab becomes visible after the PT date has changed", () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-10-28T18:00:00.000Z"));
    const { result } = renderHook(() => usePortfolioToday());
    expect(result.current).toBe("2026-10-28");

    act(() => {
      vi.setSystemTime(new Date("2026-10-29T18:00:00.000Z"));
      document.dispatchEvent(new Event("visibilitychange"));
    });
    expect(result.current).toBe("2026-10-29");
  });

  it("recomputes on window focus", () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-10-28T18:00:00.000Z"));
    const { result } = renderHook(() => usePortfolioToday());

    act(() => {
      vi.setSystemTime(new Date("2026-10-30T18:00:00.000Z"));
      window.dispatchEvent(new Event("focus"));
    });
    expect(result.current).toBe("2026-10-30");
  });
});
