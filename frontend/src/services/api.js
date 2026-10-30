import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000,
});

export const analyzeCode = async (payload) => {
  const response = await api.post('/api/analyze', payload);
  return response.data;
};

export const getDashboardStats = async () => {
  const response = await api.get('/api/dashboard');
  return response.data;
};

export const getReviews = async (params = {}) => {
  const response = await api.get('/api/reviews', { params });
  return response.data;
};

export const getReviewDetail = async (id) => {
  const response = await api.get(`/api/reviews/${id}`);
  return response.data;
};

export const deleteReview = async (id) => {
  const response = await api.delete(`/api/reviews/${id}`);
  return response.data;
};

export const getSamples = async () => {
  const response = await api.get('/api/samples');
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export const getDownloadReportUrl = (id, format = 'markdown') => {
  return `/api/reviews/${id}/report?format=${format}`;
};

export default api;
