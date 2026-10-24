import { useEffect, useState } from "react";
import API from "../services/api";

import {
  FaFileAlt,
  FaDatabase,
  FaChartBar,
  FaRobot
} from "react-icons/fa";

function StatsCards() {

  const [stats, setStats] = useState({
    documents: 0,
    chunks: 0,
    reports: 0
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {

    try {

      const response =
        await API.get("/dashboard/stats/");

      setStats(response.data);

    } catch (error) {

      console.error(
        "Failed to load stats",
        error
      );

    }
  };

  return (

    <div className="stats-row">

      <div className="metric-card">

        <div className="metric-icon">
          <FaFileAlt />
        </div>

        <h2>{stats.documents}</h2>

        <p>Documents</p>

      </div>

      <div className="metric-card">

        <div className="metric-icon">
          <FaDatabase />
        </div>

        <h2>{stats.chunks}</h2>

        <p>Chunks Indexed</p>

      </div>

      <div className="metric-card">

        <div className="metric-icon">
          <FaChartBar />
        </div>

        <h2>{stats.reports}</h2>

        <p>Reports Generated</p>

      </div>

      <div className="metric-card">

        <div className="metric-icon">
          <FaRobot />
        </div>

        <h2>Gemini</h2>

        <p>AI Engine</p>

      </div>

    </div>

  );
}

export default StatsCards;