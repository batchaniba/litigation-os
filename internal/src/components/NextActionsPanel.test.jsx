import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { ThemeContext, THEMES } from "../ThemeContext";
import { NextActionsPanel } from "./NextActionsPanel";
import { clipEvent, daysLabel } from "../utils/nextActionsView";

const item = (over = {}) => ({
  date: "Sep. 8, 2026",
  dateKey: "2026-09-08",
  daysOut: 3,
  urgency: "critical",
  event: "Deadline — Initial disclosures (FRCP 26(a)(1)) and Joint Case Management Statement — Newanforbi v. Serrato",
  matters: [24],
  action: "file",
  actor: "you",
  actorSource: "inferred",
  ...over,
});

const renderPanel = (queue, mineOnly = false, theme = THEMES.dark) => {
  const onMineOnlyChange = () => undefined;
  return render(
    <ThemeContext.Provider value={theme}>
      <MemoryRouter>
        <NextActionsPanel queue={queue} mineOnly={mineOnly} onMineOnlyChange={onMineOnlyChange} />
      </MemoryRouter>
    </ThemeContext.Provider>,
  );
};

describe("clipEvent / daysLabel", () => {
  it("clips long event text and labels days", () => {
    expect(clipEvent("short")).toBe("short");
    expect(clipEvent("x".repeat(200)).endsWith("…")).toBe(true);
    expect(daysLabel(-2)).toBe("2d overdue");
    expect(daysLabel(0)).toBe("today");
    expect(daysLabel(3)).toBe("in 3d");
  });
});

describe("NextActionsPanel", () => {
  const queue = {
    horizonDays: 30,
    items: [
      item(),
      item({
        date: "Sep. 8, 2026",
        event: "UPS reply deadline — this is UPS's clock",
        matters: [26],
        action: "file",
        actor: "opposing",
        actorSource: "explicit",
        urgency: "critical",
      }),
      item({
        date: "Sep. 10, 2026",
        dateKey: "2026-09-10",
        daysOut: 5,
        urgency: "soon",
        event: "Meet-and-confer date Van Dine requested",
        matters: [28],
        action: "meet & confer",
      }),
    ],
    undated: [
      {
        date: "Oct. 2026",
        event: "Month-only service window",
        matters: [12],
        action: "serve",
        actor: "you",
        actorSource: "inferred",
      },
    ],
    gaps: [
      { number: 31, caption: "Newanforbi v. First Advantage LLC", case_no: null, status_label: "Pre-filing" },
    ],
  };

  it("leads with the ranked queue and keeps opposing clocks visible", () => {
    renderPanel(queue);
    expect(screen.getByRole("heading", { name: "What’s next" })).toBeTruthy();
    expect(screen.getAllByText("Next 3 days").length).toBeGreaterThan(0);
    expect(screen.getByText(/Initial disclosures/)).toBeTruthy();
    expect(screen.getByText(/UPS reply deadline/)).toBeTruthy();
    expect(screen.getByText(/opposing/i)).toBeTruthy();
    expect(screen.getByRole("link", { name: "Matter 24" })).toHaveAttribute("href", "/matters/24");
  });

  it("My desk only hides opposing clocks and still shows coverage gaps", () => {
    renderPanel(queue, true);
    expect(screen.queryByText(/UPS reply deadline/)).toBeNull();
    expect(screen.getByText(/Initial disclosures/)).toBeTruthy();
    expect(screen.getByText(/First Advantage/)).toBeTruthy();
    expect(screen.getByText(/Dates as recorded in the portfolio/)).toBeTruthy();
  });

  it("the filter checkbox reports the toggle", async () => {
    const user = userEvent.setup();
    const seen = [];
    render(
      <ThemeContext.Provider value={THEMES.dark}>
        <MemoryRouter>
          <NextActionsPanel queue={queue} mineOnly={false} onMineOnlyChange={(value) => seen.push(value)} />
        </MemoryRouter>
      </ThemeContext.Provider>,
    );
    await user.click(screen.getByLabelText("My desk only"));
    expect(seen).toEqual([true]);
  });

  it("empty state when nothing is dated, undated, or drifting", () => {
    renderPanel({ horizonDays: 30, items: [], undated: [], gaps: [] });
    expect(screen.getByText("Nothing dated in the next 30 days.")).toBeTruthy();
    expect(screen.queryByText(/First Advantage/)).toBeNull();
  });

  it("keeps undated rows and expands a card without hiding the event", async () => {
    const user = userEvent.setup();
    renderPanel(queue);
    expect(screen.getByText("Not on one calendar day")).toBeTruthy();
    expect(screen.getByText(/Month-only service window/)).toBeTruthy();

    const toggle = screen.getByRole("button", { name: /Initial disclosures/ });
    expect(toggle).toHaveAttribute("aria-expanded", "false");
    await user.click(toggle);
    expect(toggle).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByText("Inferred from the event text — verify.")).toBeTruthy();
  });

  it("renders under the light theme tokens", () => {
    renderPanel(queue, false, THEMES.light);
    expect(screen.getByRole("heading", { name: "What’s next" })).toBeTruthy();
    expect(screen.getByLabelText("My desk only")).toBeTruthy();
  });
});
