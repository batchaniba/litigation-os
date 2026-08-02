import { useLayoutEffect } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { SiteFooter } from "./components/SiteFooter";
import { SiteHeader } from "./components/SiteHeader";
import { BookPage } from "./pages/BookPage";
import { CalculatorPage } from "./pages/CalculatorPage";
import { FitPage } from "./pages/FitPage";
import { HomePage } from "./pages/HomePage";
import { DisclosuresPage, PrivacyPage, TermsPage } from "./pages/LegalPages";
import { WhyBitcoinPage } from "./pages/WhyBitcoinPage";

function ScrollToHash() {
  const { pathname, hash } = useLocation();

  useLayoutEffect(() => {
    if (hash) {
      const id = hash.slice(1);
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }
    }
    window.scrollTo({ top: 0, behavior: "auto" });
  }, [pathname, hash]);

  return null;
}

export default function App() {
  return (
    <>
      <SiteHeader />
      <ScrollToHash />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/calculator" element={<CalculatorPage />} />
        <Route path="/fit" element={<FitPage />} />
        <Route path="/why-bitcoin" element={<WhyBitcoinPage />} />
        <Route path="/book" element={<BookPage />} />
        <Route path="/terms" element={<TermsPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route path="/disclosures" element={<DisclosuresPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <SiteFooter />
    </>
  );
}
