import { useState } from "react";
import API from "./services/api";

import Navbar from "./components/Navbar";
import StatsCards from "./components/StatsCards";
import DocumentsPanel from "./components/DocumentsPanel";
import ResearchPanel from "./components/ResearchPanel";
import ReportHistory from "./components/ReportHistory";

import "./App.css";

function App() {

  const [query, setQuery] = useState("");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const generateReport = async () => {

    if (!query.trim()) {
      alert("Please enter a query");
      return;
    }

    try {

      setLoading(true);

      const response =
        await API.post(
          "/reports/generate/",
          { query }
        );

      setReport(response.data.report);

    } catch (error) {

      console.error(error);

      alert(
        "Failed to generate report"
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="dashboard">

      <Navbar />

      <div className="hero-banner">

        <h1>
          Enterprise Research Intelligence Platform
        </h1>

        <p>
          Generate AI-powered research reports
          using ChromaDB, Sentence Transformers
          and Gemini AI.
        </p>

      </div>

      <StatsCards />

      <div className="workspace">

  <div>
    <DocumentsPanel />
    <ReportHistory />
  </div>

  <ResearchPanel
    query={query}
    setQuery={setQuery}
    generateReport={generateReport}
    loading={loading}
    report={report}
  />

</div>

    </div>
    
  );
}

export default App;