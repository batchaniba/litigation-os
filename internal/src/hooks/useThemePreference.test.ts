import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { THEME_STORAGE_KEY, preferredDarkMode, useThemePreference } from "./useThemePreference";

const mockPrefersLight = (prefersLight: boolean) =>
  vi.stubGlobal("matchMedia", vi.fn().mockReturnValue({ matches: prefersLight }));

describe("useThemePreference", () => {
  beforeEach(() => {
    localStorage.clear();
    delete document.documentElement.dataset.theme;
    mockPrefersLight(false);
  });
  afterEach(() => vi.unstubAllGlobals());

  it("defaults to dark when nothing is stored", () => {
    expect(preferredDarkMode()).toBe(true);
  });

  it("stays dark even when the OS prefers light", () => {
    mockPrefersLight(true);
    expect(preferredDarkMode()).toBe(true);
  });

  it("honors an explicit stored light choice over the dark default", () => {
    mockPrefersLight(false);
    localStorage.setItem(THEME_STORAGE_KEY, "light");
    expect(preferredDarkMode()).toBe(false);
  });

  it("honors an explicit stored dark choice", () => {
    mockPrefersLight(true);
    localStorage.setItem(THEME_STORAGE_KEY, "dark");
    expect(preferredDarkMode()).toBe(true);
  });

  it("ignores the retired v1 storage key so an OS-sticky light does not return", () => {
    mockPrefersLight(true);
    localStorage.setItem("newanforbi.theme.v1", "light");
    expect(preferredDarkMode()).toBe(true);
  });

  it("persists a toggle and survives a remount", () => {
    const { result, unmount } = renderHook(() => useThemePreference());
    expect(result.current[0]).toBe(true);

    act(() => result.current[1](false));
    expect(localStorage.getItem(THEME_STORAGE_KEY)).toBe("light");
    unmount();

    const remounted = renderHook(() => useThemePreference());
    expect(remounted.result.current[0]).toBe(false);
  });

  it("mirrors the choice onto <html data-theme> for the pre-mount paint", () => {
    const { result } = renderHook(() => useThemePreference());
    expect(document.documentElement.dataset.theme).toBe("dark");
    act(() => result.current[1](false));
    expect(document.documentElement.dataset.theme).toBe("light");
  });

  it("still resolves a theme when storage throws", () => {
    const getItem = vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new Error("storage disabled");
    });
    expect(preferredDarkMode()).toBe(true);
    getItem.mockRestore();
  });
});
