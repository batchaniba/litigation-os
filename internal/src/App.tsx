import { lazy, Suspense } from "react";
import { Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { ShellLayout } from "./components/layout/ShellLayout";
import { RouteLoading } from "./components/ui/AsyncState";
import { usePortfolioUI } from "./context/PortfolioUIContext";
import { ROUTES } from "./routes";

const DashboardTab = lazy(() => import("./components/DashboardTab").then((m) => ({ default: m.DashboardTab })));
const CensusRoute = lazy(() => import("./pages/CensusRoute"));
const CalendarTab = lazy(() => import("./components/CalendarTab").then((m) => ({ default: m.CalendarTab })));
const MattersRoute = lazy(() => import("./pages/MattersRoute"));
const TimelineTab = lazy(() => import("./components/TimelineTab").then((m) => ({ default: m.TimelineTab })));
const DamagesTab = lazy(() => import("./components/DamagesTab").then((m) => ({ default: m.DamagesTab })));
const TheoriesTab = lazy(() => import("./components/TheoriesTab").then((m) => ({ default: m.TheoriesTab })));
const CostOfCounselTab = lazy(() => import("./components/CostOfCounselTab").then((m) => ({ default: m.CostOfCounselTab })));
const OutcomesTab = lazy(() => import("./components/OutcomesTab").then((m) => ({ default: m.OutcomesTab })));
const JudicialOpinionsTab = lazy(() => import("./components/JudicialOpinionsTab").then((m) => ({ default: m.JudicialOpinionsTab })));
const NotableQuotesTab = lazy(() => import("./components/NotableQuotesTab").then((m) => ({ default: m.NotableQuotesTab })));
const MatterDetailPage = lazy(() => import("./pages/MatterDetailPage").then((m) => ({ default: m.MatterDetailPage })));

function DashboardRoute() {
  const ui = usePortfolioUI();
  const navigate = useNavigate();
  return <DashboardTab upcomingEvents={ui.upcomingEvents} setClusterFilter={(cluster: number) => navigate(`${ROUTES.matters}?cluster=${cluster}`)} setActiveTab={() => undefined} />;
}

function TimelineRoute() {
  const ui = usePortfolioUI();
  return <TimelineTab showPastEvents={ui.showPastEvents} setShowPastEvents={ui.setShowPastEvents} />;
}

function DamagesRoute() {
  const ui = usePortfolioUI();
  return <DamagesTab damagesView={ui.damagesView} setDamagesView={ui.setDamagesView} />;
}

export default function App() {
  return (
    <Suspense fallback={<RouteLoading label="Loading portfolio section" />}>
      <Routes>
        <Route element={<ShellLayout />}>
          <Route index element={<DashboardRoute />} />
          <Route path="census" element={<CensusRoute />} />
          <Route path="calendar" element={<CalendarTab />} />
          <Route path="matters" element={<MattersRoute />} />
          <Route path="matters/:matterNumber" element={<MatterDetailPage />} />
          <Route path="timeline" element={<TimelineRoute />} />
          <Route path="damages" element={<DamagesRoute />} />
          <Route path="theories" element={<TheoriesTab />} />
          <Route path="cost-of-counsel" element={<CostOfCounselTab />} />
          <Route path="outcomes" element={<OutcomesTab />} />
          <Route path="judicial-opinions" element={<JudicialOpinionsTab />} />
          <Route path="notable-quotes" element={<NotableQuotesTab />} />
          <Route path="*" element={<Navigate to={ROUTES.dashboard} replace />} />
        </Route>
      </Routes>
    </Suspense>
  );
}
