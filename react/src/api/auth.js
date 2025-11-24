import instance from './axios';

/**
 * Register a new user
 * @param {string} username - Username for the new account
 * @param {string} password - Password for the new account
 * @returns {Promise} Response with token and user data
 */
export const register = async (username, password) => {
  const response = await instance.post('/api/register/', {
    username,
    password,
  });
  return response.data;
};

/**
 * Login user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise} Response with token and user data
 */
export const login = async (username, password) => {
  const response = await instance.post('/api/login/', {
    username,
    password,
  });
  return response.data;
};

/**
 * Get authenticated user profile
 * @returns {Promise} Response with user profile data
 */
export const getProfile = async () => {
  const token = localStorage.getItem('token');
  const response = await instance.get('/api/profile/', {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};
