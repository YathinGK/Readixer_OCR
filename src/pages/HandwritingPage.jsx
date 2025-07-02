import React, { useState } from "react";
import axios from "axios";

export default function HandwritingPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleConvert = async () => {
    if (!selectedFile) return alert("Please select an image!");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
      });

      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "converted_notes.pdf";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert("Error converting file: " + (error.response?.data?.error || error.message));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-8 text-center text-gray-800 dark:text-white font-[Cambria]">
      <h2 className="text-4xl font-bold text-purple-700 dark:text-purple-400 mb-8">Handwriting to Digital Text</h2>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-6 p-2 border rounded bg-white text-gray-900"
      />

      {preview && (
        <div className="mb-6">
          <p className="mb-2 font-semibold">Preview:</p>
          <img src={preview} alt="Preview" className="max-w-md mx-auto rounded shadow" />
        </div>
      )}

      <button
        onClick={handleConvert}
        className="bg-purple-600 text-white px-6 py-3 rounded hover:bg-purple-700 transition"
      >
        Convert to PDF
      </button>
    </div>
  );
}
