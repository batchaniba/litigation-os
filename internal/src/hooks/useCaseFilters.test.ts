import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { useCaseFilters } from "./useCaseFilters";
import { cases } from "../data/matters";

describe("useCaseFilters", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it("defaults to active matters", () => {
    const { result } = renderHook(() => useCaseFilters());
    expect(result.current.statusFilter).toBe("active");
    expect(result.current.filteredCases.length).toBeGreaterThan(0);
    expect(result.current.filteredCases.length).toBeLessThan(cases.length);
  });

  it("holds the filter pass until typing settles, without lagging the input", () => {
    const { result } = renderHook(() => useCaseFilters({ status: "all" }));
    const unfiltered = result.current.filteredCases.length;

    act(() => result.current.setSearchQuery("zzz-no-such-matter"));
    // The controlled value updates immediately so the field stays responsive...
    expect(result.current.searchQuery).toBe("zzz-no-such-matter");
    // ...while the expensive filter + status-label pass has not run yet.
    expect(result.current.filteredCases.length).toBe(unfiltered);

    act(() => void vi.advanceTimersByTime(200));
    expect(result.current.filteredCases).toHaveLength(0);
  });

  it("collapses a burst of keystrokes into a single filter pass", () => {
    const { result } = renderHook(() => useCaseFilters({ status: "all" }));
    const unfiltered = result.current.filteredCases.length;

    for (const query of ["c", "ch", "chp"]) {
      act(() => result.current.setSearchQuery(query));
      act(() => void vi.advanceTimersByTime(150)); // each keystroke resets the timer
    }
    expect(result.current.filteredCases.length).toBe(unfiltered);

    act(() => void vi.advanceTimersByTime(200));
    expect(result.current.filteredCases.length).toBeLessThan(unfiltered);
  });

  it("applies cluster and court filters immediately", () => {
    const { result } = renderHook(() => useCaseFilters({ status: "all" }));
    act(() => result.current.setClusterFilter(1));
    expect(result.current.filteredCases.every((matter) => matter.cluster === 1)).toBe(true);

    act(() => result.current.setTypeFilter("Federal"));
    expect(result.current.filteredCases.every((matter) => matter.type === "Federal")).toBe(true);
  });

  it("sorts by matter number by default and by court on request", () => {
    const { result } = renderHook(() => useCaseFilters({ status: "all" }));
    const numbers = result.current.filteredCases.map((matter) => matter.number);
    expect(numbers).toEqual([...numbers].sort((a, b) => a - b));

    act(() => result.current.setSortKey("court"));
    const courts = result.current.filteredCases.map((matter) => matter.court);
    expect(courts).toEqual([...courts].sort((a, b) => a.localeCompare(b)));
  });

  it("never mutates the shared cases array", () => {
    const original = cases.map((matter) => matter.number);
    const { result } = renderHook(() => useCaseFilters({ status: "all", sort: "court" }));
    expect(result.current.filteredCases.length).toBe(cases.length);
    expect(cases.map((matter) => matter.number)).toEqual(original);
  });
});
