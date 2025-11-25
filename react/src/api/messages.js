import instance from './axiosInterceptors';

/**
 * Get all chat messages
 * @returns {Promise<Array<{id: number, username: string, text: string, timestamp: string}>>} Response with array of messages
 * @throws {Error} If authentication fails or request is invalid
 */
export const getMessages = async () => {
  const response = await instance.get('/api/messages/');
  return response.data;
};

/**
 * Send a new message to the chat
 * @param {string} text - Message text content (1-1000 characters)
 * @returns {Promise<{id: number, username: string, text: string, timestamp: string}>} Response with created message data
 * @throws {Error} If authentication fails or validation error occurs
 */
export const sendMessage = async (text) => {
  const response = await instance.post('/api/messages/', {
    text,
  });
  return response.data;
};
