import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await axios.post(`${API_URL}/auth/login`, formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return response.data;
};

export const register = async (userData) => {
  const response = await axios.post(`${API_URL}/auth/register`, userData);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/users/me');
  return response.data;
};

// Sessions
export const getSessions = async (params = {}) => {
  const response = await api.get('/sessions', { params });
  return response.data;
};

export const getSession = async (id) => {
  const response = await api.get(`/sessions/${id}`);
  return response.data;
};

export const createSession = async (sessionData) => {
  const response = await api.post('/sessions', sessionData);
  return response.data;
};

export const updateSession = async (id, sessionData) => {
  const response = await api.put(`/sessions/${id}`, sessionData);
  return response.data;
};

export const deleteSession = async (id) => {
  const response = await api.delete(`/sessions/${id}`);
  return response.data;
};

// Exercises
export const getExercises = async () => {
  const response = await api.get('/exercises');
  return response.data;
};

export const createExercise = async (exerciseData) => {
  const response = await api.post('/exercises', exerciseData);
  return response.data;
};

// Stats
export const getStats = async (startDate, endDate) => {
  const response = await api.get('/stats', {
    params: { start_date: startDate, end_date: endDate },
  });
  return response.data;
};

// Programs
export const getPrograms = async () => {
  const response = await api.get('/programs');
  return response.data;
};

export const createProgram = async (programData) => {
  const response = await api.post('/programs', programData);
  return response.data;
};

// Goals
export const getGoals = async () => {
  const response = await api.get('/goals');
  return response.data;
};

export const createGoal = async (goalData) => {
  const response = await api.post('/goals', goalData);
  return response.data;
};

export const updateGoal = async (id, goalData) => {
  const response = await api.put(`/goals/${id}`, goalData);
  return response.data;
};

export default api;