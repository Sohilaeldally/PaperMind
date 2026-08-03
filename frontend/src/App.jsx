import { useState, useEffect, useRef } from "react";
import { getDocuments, uploadDocument, askQuestion, getDocumentById } from "./api";
import "./App.css";

const ACTIVE_STATUSES = ["uploaded", "parsing", "parsed", "chunking", "chunked", "embedding"];

function App() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadError, setUploadError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const [selectedDocumentId, setSelectedDocumentId] = useState(null);
  const [query, setQuery] = useState("");
  const [asking, setAsking] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [askError, setAskError] = useState(null);

  const fileInputRef = useRef(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  useEffect(() => {
    const hasActiveDocuments = documents.some((doc) =>
      ACTIVE_STATUSES.includes(doc.status)
    );

    if (!hasActiveDocuments) return;

    const interval = setInterval(async () => {
      const activeDocs = documents.filter((doc) =>
        ACTIVE_STATUSES.includes(doc.status)
      );

      const updates = await Promise.all(
        activeDocs.map((doc) => getDocumentById(doc.id).catch(() => null))
      );

      setDocuments((prevDocs) =>
        prevDocs.map((doc) => {
          const updated = updates.find((u) => u && u.id === doc.id);
          return updated ? { ...doc, ...updated } : doc;
        })
      );
    }, 2000);

    return () => clearInterval(interval);
  }, [documents]);

  const loadDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error("Failed to load documents:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelected = (file) => {
    setSelectedFile(file);
    setUploadError(null);
  };

  const handleInputChange = (event) => {
    if (event.target.files[0]) {
      handleFileSelected(event.target.files[0]);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    if (event.dataTransfer.files[0]) {
      handleFileSelected(event.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setUploadError(null);

    try {
      await uploadDocument(selectedFile);
      setSelectedFile(null);
      await loadDocuments();
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadError(
        error.response?.data?.detail || "Upload failed. Please try again."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleSelectDocument = (documentId) => {
    setSelectedDocumentId(documentId);
    setAnswer(null);
    setAskError(null);
  };

  const handleAsk = async () => {
    if (!query.trim() || !selectedDocumentId) return;

    setAsking(true);
    setAskError(null);
    setAnswer(null);

    try {
      const result = await askQuestion(query, selectedDocumentId);
      setAnswer(result);
    } catch (error) {
      console.error("Ask failed:", error);
      setAskError(
        error.response?.data?.detail || "Something went wrong. Please try again."
      );
    } finally {
      setAsking(false);
    }
  };

  const selectedDocument = documents.find((doc) => doc.id === selectedDocumentId);

  return (
    <div className="app">
      <h1>PaperMind 📄🤖</h1>

      <section className="upload-section">
        <h2>Upload a Paper</h2>

        <div
          className={`dropzone ${isDragging ? "dragging" : ""}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleInputChange}
            ref={fileInputRef}
            style={{ display: "none" }}
          />

          {selectedFile ? (
            <p>📄 {selectedFile.name}</p>
          ) : (
            <p>Drag & drop a file here, or click to browse</p>
          )}
        </div>

        <button onClick={handleUpload} disabled={!selectedFile || uploading}>
          {uploading ? "Uploading..." : "Upload"}
        </button>
        {uploadError && <p className="error">{uploadError}</p>}
      </section>

      <section>
        <h2>Uploaded Papers</h2>
        {loading ? (
          <p>Loading...</p>
        ) : documents.length === 0 ? (
          <p>No papers uploaded yet.</p>
        ) : (
          <ul className="document-list">
            {documents.map((doc) => {
              const isReady = doc.status === "completed";
              const isFailed = doc.status === "failed";
              const isSelectable = isReady;

              return (
                <li
                  key={doc.id}
                  className={[
                    doc.id === selectedDocumentId ? "selected" : "",
                    isFailed ? "failed" : "",
                    !isSelectable ? "disabled" : "",
                  ].join(" ")}
                  onClick={() => isSelectable && handleSelectDocument(doc.id)}
                >
                  <div className="document-info">
                    <span>{doc.original_name}</span>
                    {isFailed && (
                      <span className="failed-hint">
                        Something went wrong while processing this file. Please try uploading it again.
                      </span>
                    )}
                  </div>

                  <span
                    className={`status-badge ${
                      isReady ? "status-ready" : isFailed ? "status-failed" : "status-processing"
                    }`}
                  >
                    {isReady ? "Ready" : isFailed ? "Failed" : "Processing..."}
                  </span>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      <section className="ask-section">
        <h2>Ask a Question</h2>

        {selectedDocument ? (
          <p>
            Asking about: <strong>{selectedDocument.original_name}</strong>
          </p>
        ) : (
          <p className="hint">Select a paper above first.</p>
        )}

        <input
          type="text"
          placeholder="What is the main contribution of this paper?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={!selectedDocumentId}
        />
        <button
          onClick={handleAsk}
          disabled={!selectedDocumentId || !query.trim() || asking}
        >
          {asking ? "Thinking..." : "Ask"}
        </button>

        {askError && <p className="error">{askError}</p>}

        {answer && (
          <div className="answer-box">
            <h3>Answer</h3>
            <p>{answer.answer}</p>

            <h4>Sources</h4>
            <ul>
              {[...new Set(answer.sources.map((s) => s.section_name || "General content"))].map(
                (sectionName) => (
                  <li key={sectionName}>📍 {sectionName}</li>
                )
              )}
            </ul>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;