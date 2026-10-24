import { useEffect, useState } from "react";
import API from "../services/api";

function ReportHistory() {

  const [reports, setReports] = useState([]);

  useEffect(() => {

    loadReports();

  }, []);

  const loadReports = async () => {

    try {

      const response =
        await API.get(
          "/reports/history/"
        );

      setReports(response.data);

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <div className="documents-panel">

      <h2>📜 Recent Reports</h2>

      <div className="document-list">

        {reports.map((report) => (

          <div
            key={report.report_id}
            className="document-item"
          >

            {report.title}

          </div>

        ))}

      </div>

    </div>

  );
}

export default ReportHistory;