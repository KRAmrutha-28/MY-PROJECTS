import ReactMarkdown from "react-markdown";
import API from "../services/api";

function ResearchPanel({
  query,
  setQuery,
  generateReport,
  loading,
  report
}) {

  const downloadFile = async (
    endpoint,
    filename
  ) => {

    try {

      const response = await API.post(
        endpoint,
        {
          report
        },
        {
          responseType: "blob"
        }
      );

      const url =
        window.URL.createObjectURL(
          new Blob([response.data])
        );

      const link =
        document.createElement("a");

      link.href = url;

      link.download = filename;

      document.body.appendChild(link);

      link.click();

      link.remove();

    } catch (error) {

      console.error(error);

      alert(
        `Failed to download ${filename}`
      );

    }

  };

  const downloadPDF = () =>
    downloadFile(
      "/reports/download-pdf/",
      "Research_Report.pdf"
    );

  const downloadHTML = () =>
    downloadFile(
      "/reports/download-html/",
      "Research_Report.html"
    );

  const downloadDOCX = () =>
    downloadFile(
      "/reports/download-docx/",
      "Research_Report.docx"
    );

  const downloadPPTX = () =>
    downloadFile(
      "/reports/download-pptx/",
      "Research_Report.pptx"
    );

  const downloadXLSX = () =>
    downloadFile(
      "/reports/download-xlsx/",
      "Research_Report.xlsx"
    );

  return (

    <div className="research-panel">

      <div className="search-box">

        <input
          type="text"
          placeholder="Ask a research question..."
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
        />

        <button
          onClick={generateReport}
        >
          {
            loading
              ? "Generating..."
              : "Generate Report"
          }
        </button>

      </div>

      {report && (

        <div className="report-card">

          <div
            style={{
              display: "flex",
              justifyContent:
                "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "10px",
              marginBottom: "20px"
            }}
          >

            <h2>
              📄 Generated Research Report
            </h2>

            <div
              style={{
                display: "flex",
                gap: "10px",
                flexWrap: "wrap"
              }}
            >

              <button
                onClick={downloadPDF}
                className="export-btn"
              >
                PDF
              </button>

              <button
                onClick={downloadDOCX}
                className="export-btn"
              >
                DOCX
              </button>

              <button
                onClick={downloadHTML}
                className="export-btn"
              >
                HTML
              </button>

              <button
                onClick={downloadPPTX}
                className="export-btn"
              >
                PPTX
              </button>

              <button
                onClick={downloadXLSX}
                className="export-btn"
              >
                XLSX
              </button>

            </div>

          </div>

          <ReactMarkdown>
            {report}
          </ReactMarkdown>

        </div>

      )}

    </div>

  );
}

export default ResearchPanel;