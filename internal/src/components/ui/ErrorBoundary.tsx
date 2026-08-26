import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
  /** Change this to clear a caught error — the route boundary passes the current
   *  path, so navigating away from a broken section recovers without a reload. */
  resetKey?: string;
  /** Rendered instead of the default full-page card. Used by the route-level
   *  boundary, which sits inside the shell and must not claim the whole page. */
  fallback?: (error: Error) => ReactNode;
}
interface State { error: Error | null; resetKey?: string }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null, resetKey: this.props.resetKey };

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { error };
  }

  static getDerivedStateFromProps(props: Props, state: State): Partial<State> | null {
    if (props.resetKey === state.resetKey) return null;
    return { error: null, resetKey: props.resetKey };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Portfolio rendering error", error, info);
  }

  render() {
    const { error } = this.state;
    if (!error) return this.props.children;
    if (this.props.fallback) return this.props.fallback(error);
    return (
      <main className="error-state">
        <div>
          <h1>This section could not be displayed.</h1>
          <p>{error.message}</p>
          <button onClick={() => window.location.reload()}>Reload portfolio</button>
        </div>
      </main>
    );
  }
}
