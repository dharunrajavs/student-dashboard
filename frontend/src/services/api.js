import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 (Unauthorized) and 422 (Invalid token format)
    if (error.response?.status === 401 || error.response?.status === 422) {
      const isAuthEndpoint = error.config?.url?.includes('/auth/');
      if (!isAuthEndpoint && window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        // Check if user was previously authenticated
        const hadToken = localStorage.getItem('token');
        if (hadToken) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          // Only redirect on non-auth endpoints
          if (!error.config?.url?.includes('/auth/me')) {
            window.location.href = '/login';
          }
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
  changePassword: (passwords) => api.post('/auth/change-password', passwords),
};

// Students API
export const studentsAPI = {
  getProfile: (studentId) => api.get(`/students/profile/${studentId}`),
  updateProfile: (studentId, data) => api.put(`/students/profile/${studentId}`, data),
  getPerformance: (studentId, params) => api.get(`/students/performance/${studentId}`, { params }),
  addPerformance: (data) => api.post('/students/performance', data),
  listStudents: (params) => api.get('/students/list', { params }),
};

// Predictions API
export const predictionsAPI = {
  predictGPA: (data) => api.post('/predict/gpa', data),
  predictScholarship: (data) => api.post('/predict/scholarship', data),
  recommendCareer: (data) => api.post('/predict/career', data),
  calculateRiskScore: (studentId) => api.get(`/predict/risk-score/${studentId}`),
  getHistory: (studentId, type) => api.get(`/predict/history/${studentId}`, { params: { type } }),
};

// Chatbot API
export const chatbotAPI = {
  sendMessage: (data) => api.post('/chatbot/message', data),
  getHistory: (studentId, limit) => api.get(`/chatbot/history/${studentId}`, { params: { limit } }),
  getStudyPlan: (studentId) => api.get(`/chatbot/study-plan/${studentId}`),
  clearHistory: (studentId) => api.delete(`/chatbot/clear-history/${studentId}`),
};

// Analytics API
export const analyticsAPI = {
  getHeatmap: (studentId) => api.get(`/analytics/heatmap/${studentId}`),
  getTrends: (studentId) => api.get(`/analytics/trends/${studentId}`),
  getLeaderboard: (params) => api.get('/analytics/leaderboard', { params }),
  getComparison: (studentId) => api.get(`/analytics/comparison/${studentId}`),
};

// Admin API
export const adminAPI = {
  getDashboard: () => api.get('/admin/dashboard'),
  getAtRiskStudents: (threshold) => api.get('/admin/students/at-risk', { params: { threshold } }),
  getEligibleStudents: () => api.get('/admin/scholarships/eligible'),
  exportEligible: () => api.get('/admin/scholarships/export', { responseType: 'blob' }),
  createAlert: (data) => api.post('/admin/alerts/create', data),
  deactivateStudent: (studentId) => api.post(`/admin/students/${studentId}/deactivate`),
};

// Reports API
export const reportsAPI = {
  generatePDF: () => api.post('/reports/generate-pdf', {}, { responseType: 'blob' }),
  emailReport: () => api.post('/reports/email-report'),
  sendAlert: (data) => api.post('/reports/send-alert', data),
};

export default api;
