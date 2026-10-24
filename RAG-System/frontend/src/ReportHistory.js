import { useEffect, useState } from "react";
import API from "../services/api";

function ReportHistory() {

const [reports, setReports] = useState([]);

useEffect(() => {
fetchReports();
}, []);

const fetchReports = async () => {

```
try {

  const response =
    await API.get(
      "/reports/history/"
    );

  setReports(response.data);

} catch (error) {

  console.error(error);

}
```

};

return (

```
<div className="report-history">

  <h2>
    📊 Report History
  </h2>

  {
    reports.length === 0
    ? (
        <p>
          No reports generated yet
        </p>
      )
    : (
        reports.map((report) => (

          <div
            key={report.report_id}
            className="history-card"
          >

            <h4>
              {report.title}
            </h4>

            <p>
              {new Date(
                report.created_at
              ).toLocaleString()}
            </p>

            <span>
              {report.status}
            </span>

          </div>

        ))
      )
  }

</div>
```

);

}

export default ReportHistory;
