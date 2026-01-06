/**
 * API service for communicating with the backend
 */
import axios from 'axios';

const API_BASE_URL =
  import.meta.env.MODE === 'development'
    ? 'http://localhost:8000/api/v1'
    : import.meta.env.VITE_API_BASE_URL;

console.log('API BASE URL:', API_BASE_URL);


// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    console.log('Token exists:', !!token);

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Authorization header added');
    } else {
      console.log('No token found - request will be unauthenticated');
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.method?.toUpperCase(), response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.statusText);
    console.error('Error details:', error.response?.data);

    // Don't auto-redirect on 401 errors - let components handle auth failures
    // This prevents conflicts with React Router navigation
    console.log('API Error handled by component - not auto-redirecting');
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (email, password, fullName) => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Resume API
export const resumeAPI = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  extractSkills: async (text) => {
    const response = await api.post('/resume/extract-skills', null, {
      params: { text },
    });
    return response.data;
  },
};

// Job Recommendation API
export const jobAPI = {
  recommend: async (userSkills, topN = 10) => {
    const response = await api.post('/jobs/recommend', {
      user_skills: userSkills,
      top_n: topN,
    });
    return response.data;
  },

  getSkillGap: async (jobId, userSkills) => {
    const response = await api.post(`/jobs/skill-gap/${jobId}`, {
      user_skills: userSkills,
    });
    return response.data;
  },
};

export default api;

