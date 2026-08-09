import { describe, expect, it } from "vitest";
import { NAV_ITEMS, ROUTES } from "./routes";
import { PREFETCHABLE_ROUTES, prefetchRoute } from "./routePrefetch";

describe("routePrefetch", () => {
  // The map is keyed by path string, so a renamed route would silently stop
  // prefetching rather than fail. These are the checks that catch that.
  it("has a chunk for every route in ROUTES", () => {
    for (const path of Object.values(ROUTES)) {
      expect(PREFETCHABLE_ROUTES, `${path} has no prefetch loader`).toContain(path);
    }
  });

  it("has a chunk for every link in the nav", () => {
    for (const item of NAV_ITEMS) {
      expect(PREFETCHABLE_ROUTES, `${item.label} is in the nav but has no prefetch loader`).toContain(item.path);
    }
  });

  it("is a no-op for a path with no chunk, and never throws", () => {
    expect(() => prefetchRoute("/not-a-route")).not.toThrow();
    expect(() => prefetchRoute("")).not.toThrow();
  });

  it("is safe to call repeatedly for the same route", () => {
    expect(() => {
      prefetchRoute(ROUTES.outcomes);
      prefetchRoute(ROUTES.outcomes);
      prefetchRoute(ROUTES.outcomes);
    }).not.toThrow();
  });
});
