import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get('/api/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Process natural language query
  processQuery: async (queryText) => {
    try {
      const response = await api.post('/api/query', { query: queryText });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Process voice input
  processVoice: async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.wav');
      
      const response = await api.post('/api/voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get database schema
  getDatabaseSchema: async () => {
    try {
      const response = await api.get('/api/schema');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Execute direct SQL query
  executeSQL: async (sqlQuery) => {
    try {
      const response = await api.post('/api/sql', { sql: sqlQuery });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get example queries
  getExamples: async () => {
    try {
      const response = await api.get('/api/examples');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default apiService;
