import { useState } from "react";
import axios from "axios";

function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const token = localStorage.getItem("token");

      await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert("File uploaded successfully!");

      setFile(null);

      if (onUploadSuccess) {
        onUploadSuccess();
      }

    } catch (error) {
      console.error(error);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button type="submit" disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
    </form>
  );
}

export default UploadForm;