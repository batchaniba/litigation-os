import React from "react";
import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CollapsibleProse, COLLAPSE_THRESHOLD } from "./CollapsibleProse";

const long = "word ".repeat(200).trim();

describe("CollapsibleProse", () => {
  it("renders short prose plainly, with no toggle", () => {
    render(<CollapsibleProse text="A short procedural note." label="key facts" />);
    expect(screen.getByText("A short procedural note.")).toBeInTheDocument();
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("renders nothing for empty prose", () => {
    const { container } = render(<CollapsibleProse text="   " label="key facts" />);
    expect(container).toBeEmptyDOMElement();
  });

  it("clamps long prose behind a labelled toggle", async () => {
    render(<CollapsibleProse text={long} label="key facts" />);
    const toggle = screen.getByRole("button", { name: /show full key facts/i });
    expect(toggle).toHaveAttribute("aria-expanded", "false");
    expect(screen.getByText(long)).toHaveClass("is-clamped");

    await userEvent.click(toggle);
    expect(toggle).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByText(long)).not.toHaveClass("is-clamped");
    expect(screen.getByRole("button", { name: /show less/i })).toBeInTheDocument();
  });

  it("keeps the full text in the DOM while collapsed, so print and find-in-page work", () => {
    render(<CollapsibleProse text={long} label="key facts" />);
    expect(screen.getByText(long).textContent).toBe(long);
  });

  it("honours the threshold boundary", () => {
    const atThreshold = "x".repeat(COLLAPSE_THRESHOLD);
    render(<CollapsibleProse text={atThreshold} label="key facts" />);
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("keeps caller classes and styles on the paragraph", () => {
    render(<CollapsibleProse text={long} label="risk notes" className="detail-copy-muted" />);
    const paragraph = screen.getByText(long);
    expect(paragraph).toHaveClass("detail-copy");
    expect(paragraph).toHaveClass("detail-copy-muted");
  });
});
