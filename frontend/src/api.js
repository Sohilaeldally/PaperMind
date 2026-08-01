import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE_URL}/documents/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

export const getDocuments = async () => {
  const response = await axios.get(`${API_BASE_URL}/documents/`);
  return response.data;
};

export const getDocumentById = async (documentId) => {
  const response = await axios.get(`${API_BASE_URL}/documents/${documentId}`);
  return response.data;
};

export const askQuestion = async (query, documentId, topK = 5) => {
  const response = await axios.post(`${API_BASE_URL}/search/ask`, {
    query,
    document_id: documentId,
    top_k: topK,
  });
  return response.data;
};