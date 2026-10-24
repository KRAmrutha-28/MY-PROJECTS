import { useState } from "react";
import API from "../services/api";

function FileUpload() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a document");
      return;
    }

    const formData = new FormData();

    formData.append("title", file.name);
    formData.append("file", file);

    try {
      const response = await API.post(
        "/documents/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert("✅ " + response.data.message);

      console.log(response.data);

    } catch (error) {
      console.error(error);

      if (error.response) {
        console.log(error.response.data);

        alert(
          JSON.stringify(
            error.response.data,
            null,
            2
          )
        );
      } else {
        alert("Upload failed");
      }
    }
  };

  return (
    <div className="upload-container">

      <label className="file-label">
        📂 Select Document

        <input
          type="file"
          accept=".pdf,.docx,.txt,.csv,.pptx,.xlsx"
          hidden
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>

      <button
        onClick={uploadFile}
        className="upload-btn"
      >
        🚀 Upload Document
      </button>

      {file && (
        <p className="file-name">
          📄 {file.name}
        </p>
      )}

    </div>
  );
}

export default FileUpload;