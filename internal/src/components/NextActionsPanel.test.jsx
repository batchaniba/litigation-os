import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
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

const renderPanel = (queue, mineOnly = false) => {
  const onMineOnlyChange = () => undefined;
  return render(
    <MemoryRouter>
      <NextActionsPanel queue={queue} mineOnly={mineOnly} onMineOnlyChange={onMineOnlyChange} />
    </MemoryRouter>,
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
    undated: [],
    gaps: [
      { number: 31, caption: "Newanforbi v. First Advantage LLC", case_no: null, status_label: "Pre-filing" },
    ],
  };

  it("leads with the ranked queue and keeps opposing clocks visible", () => {
    renderPanel(queue);
    expect(screen.getByRole("heading", { name: "What’s next" })).toBeTruthy();
    expect(screen.getByText("Next 3 days")).toBeTruthy();
    expect(screen.getByText(/Initial disclosures/)).toBeTruthy();
    expect(screen.getByText(/UPS reply deadline/)).toBeTruthy();
    expect(screen.getByText("opposing")).toBeTruthy();
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
      <MemoryRouter>
        <NextActionsPanel queue={queue} mineOnly={false} onMineOnlyChange={(value) => seen.push(value)} />
      </MemoryRouter>,
    );
    await user.click(screen.getByLabelText("My desk only"));
    expect(seen).toEqual([true]);
  });
});
