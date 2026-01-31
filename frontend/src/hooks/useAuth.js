import { create } from 'zustand';
import { authAPI } from '../services/api';

const useAuthStore = create((set, get) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authAPI.login(email, password);
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      set({ token: access_token, isAuthenticated: true, isLoading: false });
      
      // Get user info
      const userResponse = await authAPI.getMe();
      set({ user: userResponse.data });
      
      return true;
    } catch (error) {
      set({ 
        error: error.response?.data?.detail || 'Login failed', 
        isLoading: false 
      });
      return false;
    }
  },

  register: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authAPI.register(email, password);
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      set({ token: access_token, isAuthenticated: true, isLoading: false });
      
      // Get user info
      const userResponse = await authAPI.getMe();
      set({ user: userResponse.data });
      
      return true;
    } catch (error) {
      set({ 
        error: error.response?.data?.detail || 'Registration failed', 
        isLoading: false 
      });
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, token: null, isAuthenticated: false });
  },

  clearError: () => set({ error: null }),

  initializeAuth: async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await authAPI.getMe();
        set({ user: response.data, isAuthenticated: true });
      } catch (error) {
        localStorage.removeItem('token');
        set({ token: null, isAuthenticated: false });
      }
    }
  },
}));

export default useAuthStore;