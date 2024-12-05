import axios from "axios";

const BASE_URL = "http://localhost:8000/api/documents";

// Create an Axios instance for the API
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 10000, // Set a timeout for requests (10 seconds)
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request and response interceptors
apiClient.interceptors.request.use(
  (config) => {
    // Modify the config (e.g., add an Authorization header if needed)
    // config.headers['Authorization'] = `Bearer ${token}`;
    return config;
  },
  (error) => {
    console.error("Request error:", error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error("Response error:", error.response || error.message);
    return Promise.reject(error.response || error.message);
  }
);

// API Methods
const documentsApi = {
  getDocumentById: async (fileId) => {
    try {
      const response = await apiClient.get(`/get/${fileId}`);
      return {
        ...response,
        url: `${BASE_URL}/get/${fileId}`, // Add URL to response
      };
    } catch (error) {
      console.error("Error fetching document by ID:", error);
      throw error;
    }
  },

  deleteDocument: async (fileId) => {
    try {
      return await apiClient.delete(`/delete/${fileId}`);
    } catch (error) {
      console.error("Error deleting document:", error);
      throw error;
    }
  },

  uploadDocument: async (formData) => {
    try {
      return await apiClient.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    } catch (error) {
      console.error("Error uploading document:", error);
      throw error;
    }
  },

  updateDocument: async (formData) => {
    try {
      return await apiClient.put("/update", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    } catch (error) {
      console.error("Error updating document:", error);
      throw error;
    }
  },
};

export default documentsApi;
