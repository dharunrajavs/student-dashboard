import React, { createContext, useState, useContext, useEffect, useRef } from 'react';
import { authAPI } from '../services/api';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const skipLoadUser = useRef(false);

  useEffect(() => {
    // Skip loadUser if we just logged in (user already set from login response)
    if (skipLoadUser.current) {
      skipLoadUser.current = false;
      setLoading(false);
      return;
    }
    
    if (token && !user) {
      loadUser();
    } else {
      setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const loadUser = async () => {
    try {
      // Validate token before making request
      const storedToken = localStorage.getItem('token');
      if (!storedToken) {
        setLoading(false);
        return;
      }
      
      // Check if token is valid JWT format
      try {
        const decoded = jwtDecode(storedToken);
        if (decoded.exp < Date.now() / 1000) {
          // Token expired
          localStorage.removeItem('token');
          setToken(null);
          setUser(null);
          setStudent(null);
          setLoading(false);
          return;
        }
      } catch (e) {
        // Invalid token format
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setStudent(null);
        setLoading(false);
        return;
      }
      
      const response = await authAPI.getCurrentUser();
      if (response.data) {
        setUser(response.data.user);
        setStudent(response.data.student);
      }
    } catch (error) {
      console.error('Failed to load user:', error);
      // Clear auth state if token is invalid (401 or 422)
      if (error.response?.status === 401 || error.response?.status === 422) {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setStudent(null);
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials);
      const { access_token, user, student } = response.data;
      
      localStorage.setItem('token', access_token);
      // Skip loadUser since we already have user data from login response
      skipLoadUser.current = true;
      setToken(access_token);
      setUser(user);
      setStudent(student);
      setLoading(false);
      
      return { success: true, user, student };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed'
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Registration failed'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setStudent(null);
  };

  const isAuthenticated = () => {
    if (!token) return false;
    
    try {
      const decoded = jwtDecode(token);
      return decoded.exp > Date.now() / 1000;
    } catch {
      return false;
    }
  };

  const value = {
    user,
    student,
    loading,
    login,
    register,
    logout,
    isAuthenticated,
    loadUser
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
