import { useEffect, useState } from "react";
import API from "../services/api";
import FileUpload from "./FileUpload";

function DocumentsPanel() {

  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {

    try {

      const response = await API.get(
        "/documents/list/"
      );

      setDocuments(response.data);

    } catch (error) {

      console.error(
        "Error fetching documents:",
        error
      );

    }

  };

  const handleDelete = async (
    documentId
  ) => {

    const confirmDelete =
      window.confirm(
        "Are you sure you want to delete this document?"
      );

    if (!confirmDelete) {
      return;
    }

    try {

      await API.delete(
        `/documents/delete/${documentId}/`
      );

      alert(
        "Document deleted successfully"
      );

      fetchDocuments();

    } catch (error) {

      console.error(
        "Delete error:",
        error
      );

      alert(
        "Failed to delete document"
      );

    }

  };

  return (

    <div className="documents-panel">

      <h2>📂 Documents</h2>

      <FileUpload />

      <div className="document-list">

        {documents.length === 0 ? (

          <p>No documents uploaded</p>

        ) : (

          documents.map((doc) => (

            <div
              key={doc.document_id}
              className="document-item"
            >

              <div className="doc-title">
                📄 {doc.title}
              </div>

              <div className="doc-meta">

                <span>
                  {doc.file_type?.toUpperCase()}
                </span>

                <span>
                  {doc.total_chunks} chunks
                </span>

              </div>

              <div
                className={
                  doc.processing_status ===
                  "COMPLETED"
                    ? "status-completed"
                    : "status-failed"
                }
              >
                {doc.processing_status}
              </div>

              <button
                className="delete-btn"
                onClick={() =>
                  handleDelete(
                    doc.document_id
                  )
                }
              >
                🗑 Delete
              </button>

            </div>

          ))

        )}

      </div>

    </div>

  );

}

export default DocumentsPanel;