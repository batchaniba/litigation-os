import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router";
import { MattersTab } from "./MattersTab";
import { cases } from "../data/matters";

const noop = () => undefined;

const renderList = (overrides = {}) => {
  const props = {
    filteredCases: cases.slice(0, 6),
    statusFilter: "active", setStatusFilter: noop,
    clusterFilter: null, setClusterFilter: noop,
    typeFilter: null, setTypeFilter: noop,
    searchQuery: "", setSearchQuery: noop,
    sortKey: "number", setSortKey: noop,
    ...overrides,
  };
  return render(<MemoryRouter><MattersTab {...props} /></MemoryRouter>);
};

describe("MattersTab", () => {
  it("renders one card per filtered matter", () => {
    renderList();
    expect(screen.getAllByRole("button", { expanded: false }).filter((b) => b.className === "matter-card-header")).toHaveLength(6);
  });

  it("expands only the card that was clicked", async () => {
    const user = userEvent.setup();
    renderList();
    const headers = screen.getAllByRole("button", { expanded: false }).filter((b) => b.className === "matter-card-header");

    await user.click(headers[0]);
    expect(headers[0]).toHaveAttribute("aria-expanded", "true");
    expect(headers[1]).toHaveAttribute("aria-expanded", "false");

    await user.click(headers[0]);
    expect(headers[0]).toHaveAttribute("aria-expanded", "false");
  });

  it("moves the open card when a different one is clicked", async () => {
    const user = userEvent.setup();
    renderList();
    const headers = screen.getAllByRole("button", { expanded: false }).filter((b) => b.className === "matter-card-header");

    await user.click(headers[0]);
    await user.click(headers[2]);
    expect(headers[0]).toHaveAttribute("aria-expanded", "false");
    expect(headers[2]).toHaveAttribute("aria-expanded", "true");
  });

  it("reports the filtered count against the portfolio total", () => {
    renderList();
    expect(screen.getAllByText(`6 of ${cases.length}`).length).toBeGreaterThan(0);
  });

  it("offers a reset when nothing matches", () => {
    renderList({ filteredCases: [] });
    expect(screen.getByText(/no matters match your current filters/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /clear all filters/i })).toBeInTheDocument();
  });
});
