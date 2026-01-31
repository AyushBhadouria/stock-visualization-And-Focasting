import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
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

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (email, password) => api.post('/auth/register', { email, password }),
  getMe: () => api.get('/auth/me'),
};

export const stockAPI = {
  search: (query) => api.get(`/stocks/search?query=${query}`),
  getStock: (symbol, period = '1y') => api.get(`/stocks/${symbol}?period=${period}`),
  getQuote: (symbol) => api.get(`/stocks/${symbol}/quote`),
  getHistory: (symbol, period = '1y') => api.get(`/stocks/${symbol}/history?period=${period}`),
  getCompany: (symbol) => api.get(`/stocks/${symbol}/company`),
};

export const indicatorAPI = {
  getIndicators: (symbol, indicators = 'sma,rsi,macd', period = '1y') => 
    api.get(`/indicators/${symbol}?indicators=${indicators}&period=${period}`),
  getAllIndicators: (symbol, period = '1y') => 
    api.get(`/indicators/${symbol}/all?period=${period}`),
};

export const forecastAPI = {
  generateForecast: (symbol, model = 'ensemble', days = 30) => 
    api.post(`/forecasts/${symbol}`, { model, days }),
  getModels: () => api.get('/forecasts/models'),
};

export const watchlistAPI = {
  getWatchlist: () => api.get('/watchlist'),
  addToWatchlist: (symbol) => api.post('/watchlist', { symbol }),
  removeFromWatchlist: (symbol) => api.delete(`/watchlist/${symbol}`),
};

export const alertAPI = {
  getAlerts: () => api.get('/alerts'),
  createAlert: (symbol, condition, target_price) => 
    api.post('/alerts', { symbol, condition, target_price }),
  deleteAlert: (alertId) => api.delete(`/alerts/${alertId}`),
};

export const patternAPI = {
  getCandlestickPatterns: (symbol, period = '3mo') => 
    api.get(`/patterns/${symbol}/candlestick?period=${period}`),
  getSupportResistance: (symbol, period = '6mo') => 
    api.get(`/patterns/${symbol}/support-resistance?period=${period}`),
  getTrendLines: (symbol, period = '6mo') => 
    api.get(`/patterns/${symbol}/trends?period=${period}`),
};

export const portfolioAPI = {
  getPortfolio: () => api.get('/portfolio'),
  addTransaction: (transaction) => api.post('/portfolio/transaction', transaction),
  getTransactions: () => api.get('/portfolio/transactions'),
};

export const newsAPI = {
  getMarketNews: (limit = 20) => api.get(`/news/market?limit=${limit}`),
  getStockNews: (symbol, limit = 10) => api.get(`/news/${symbol}?limit=${limit}`),
};

export default api;