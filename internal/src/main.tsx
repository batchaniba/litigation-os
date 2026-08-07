import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, HashRouter } from "react-router";
import App from "./App";
import { ErrorBoundary } from "./components/ui/ErrorBoundary";
import "./styles/app.css";

const root = document.getElementById("root");

if (!root) throw new Error("Application root element was not found");

const basename = import.meta.env.BASE_URL.replace(/\/$/, "") || undefined;
const Router = basename ? HashRouter : BrowserRouter;

createRoot(root).render(
  <StrictMode>
    <ErrorBoundary>
      <Router>
        <App />
      </Router>
    </ErrorBoundary>
  </StrictMode>,
);
