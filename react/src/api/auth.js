import instance from './axiosInterceptors';

/**
 * Register a new user
 * @param {string} username - Username for the new account (3-150 characters)
 * @param {string} password - Password for the new account (minimum 6 characters)
 * @returns {Promise<{token: string, user: {id: number, username: string}}>} Response with token and user data
 * @throws {Error} If registration fails (user exists or validation error)
 */
export const register = async (username, password) => {
  const response = await instance.post('/api/register/', {
    username,
    password,
  });
  
  // Save token to localStorage
  if (response.data.token) {
    localStorage.setItem('token', response.data.token);
  }
  
  return response.data;
};

/**
 * Login user and save authentication token
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<{token: string, user: {id: number, username: string}}>} Response with token and user data
 * @throws {Error} If login fails (invalid credentials)
 */
export const login = async (username, password) => {
  const response = await instance.post('/api/login/', {
    username,
    password,
  });
  
  // Save token to localStorage
  if (response.data.token) {
    localStorage.setItem('token', response.data.token);
  }
  
  return response.data;
};

/**
 * Get authenticated user profile
 * @returns {Promise<{id: number, username: string, created_at: string}>} Response with user profile data
 * @throws {Error} If authentication fails (invalid or missing token)
 */
export const getProfile = async () => {
  const response = await instance.get('/api/profile/');
  return response.data;
};

/**
 * Logout user by clearing authentication token from localStorage
 * @returns {void}
 */
export const logout = () => {
  localStorage.removeItem('token');
};
