// src/config.js
// Centralized config for API URLs and other environment-dependent values

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
