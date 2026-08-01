import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props { children: ReactNode }
interface State { error: Error | null }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Portfolio rendering error", error, info);
  }

  render() {
    if (!this.state.error) return this.props.children;
    return (
      <main className="error-state">
        <div>
          <h1>This section could not be displayed.</h1>
          <p>{this.state.error.message}</p>
          <button onClick={() => window.location.reload()}>Reload portfolio</button>
        </div>
      </main>
    );
  }
}
