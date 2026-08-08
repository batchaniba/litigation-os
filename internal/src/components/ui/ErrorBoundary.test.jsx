import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { ErrorBoundary } from "./ErrorBoundary";

function Boom({ throws }) {
  if (throws) throw new Error("matter 31 exploded");
  return <div>section content</div>;
}

describe("ErrorBoundary", () => {
  // React logs caught errors to console.error; silence it so the run stays readable.
  beforeEach(() => vi.spyOn(console, "error").mockImplementation(() => {}));
  afterEach(() => vi.restoreAllMocks());

  it("renders children when nothing throws", () => {
    render(<ErrorBoundary><Boom throws={false} /></ErrorBoundary>);
    expect(screen.getByText("section content")).toBeInTheDocument();
  });

  it("shows the failure and its message when a child throws", () => {
    render(<ErrorBoundary><Boom throws /></ErrorBoundary>);
    expect(screen.getByText(/could not be displayed/i)).toBeInTheDocument();
    expect(screen.getByText("matter 31 exploded")).toBeInTheDocument();
  });

  it("uses a caller-supplied fallback when given one", () => {
    render(
      <ErrorBoundary fallback={(error) => <p>inline: {error.message}</p>}>
        <Boom throws />
      </ErrorBoundary>,
    );
    expect(screen.getByText(/inline: matter 31 exploded/)).toBeInTheDocument();
  });

  // The regression this guards: the only boundary sat above the router with no
  // reset path, so one bad route replaced the whole portfolio until a reload.
  it("clears the error when resetKey changes", () => {
    const { rerender } = render(
      <ErrorBoundary resetKey="/matters/31"><Boom throws /></ErrorBoundary>,
    );
    expect(screen.getByText(/could not be displayed/i)).toBeInTheDocument();

    rerender(<ErrorBoundary resetKey="/dashboard"><Boom throws={false} /></ErrorBoundary>);
    expect(screen.getByText("section content")).toBeInTheDocument();
  });

  it("keeps the error while resetKey is unchanged", () => {
    const { rerender } = render(
      <ErrorBoundary resetKey="/matters/31"><Boom throws /></ErrorBoundary>,
    );
    rerender(<ErrorBoundary resetKey="/matters/31"><Boom throws={false} /></ErrorBoundary>);
    expect(screen.getByText(/could not be displayed/i)).toBeInTheDocument();
  });
});
