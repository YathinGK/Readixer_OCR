import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FeatureSection from "./components/FeatureSection";
import HandwritingPage from "./pages/HandwritingPage";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Home page with FeatureSection */}
        <Route path="/" element={<FeatureSection />} />

        {/* Handwriting Conversion Page */}
        <Route path="/handwriting" element={<HandwritingPage />} />
      </Routes>
    </Router>
  );
}
