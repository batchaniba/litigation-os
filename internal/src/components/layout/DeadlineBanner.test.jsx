import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, act } from "@testing-library/react";
import { DeadlineBanner } from "./DeadlineBanner";

const EVENTS = [{ date: "Dec. 10, 2026", event: "Case management conference", matters: [5], type: "hearing", upcoming: true }];

const advanceSeconds = (n) => {
  // One act() per tick — batching a whole span into a single act would collapse
  // every interval callback into one render and hide what this is measuring.
  for (let i = 0; i < n; i++) act(() => { vi.advanceTimersByTime(1000); });
};

describe("DeadlineBanner", () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ["setInterval", "clearInterval", "setTimeout", "clearTimeout", "Date"] });
    vi.setSystemTime(new Date("2026-08-08T12:00:00-07:00"));
  });
  afterEach(() => vi.useRealTimers());

  it("starts collapsed and does not re-render every second while collapsed", () => {
    let renders = 0;
    function Probe() { renders++; return <DeadlineBanner upcomingEvents={EVENTS} />; }

    render(<Probe />);
    expect(screen.getByRole("button", { name: /show/i })).toBeInTheDocument();
    expect(document.getElementById("deadline-clock-display")).toBeNull();

    const baseline = renders;
    advanceSeconds(10);
    // The regression this guards: a hidden countdown used to drive a 1 Hz render
    // loop through the shell's context value, re-rendering every active route.
    expect(renders).toBe(baseline);
  });

  it("ticks once a second once the countdown is shown", async () => {
    render(<DeadlineBanner upcomingEvents={EVENTS} />);
    await act(async () => { screen.getByRole("button", { name: /show/i }).click(); });

    expect(document.getElementById("deadline-clock-display")).not.toBeNull();
    const before = document.querySelector(".legacy-clock-units").textContent;
    advanceSeconds(3);
    expect(document.querySelector(".legacy-clock-units").textContent).not.toBe(before);
  });

  it("stops ticking again when the countdown is collapsed", async () => {
    render(<DeadlineBanner upcomingEvents={EVENTS} />);
    await act(async () => { screen.getByRole("button", { name: /show/i }).click(); });
    await act(async () => { screen.getByRole("button", { name: /hide/i }).click(); });

    expect(document.getElementById("deadline-clock-display")).toBeNull();
    expect(screen.getByRole("button", { name: /show/i })).toBeInTheDocument();
  });
});
