import instance from './axiosInterceptors';

/**
 * Get chat messages with pagination
 * @param {number} [page=1] - Page number (minimum: 1)
 * @param {number} [pageSize=50] - Number of messages per page (1-100)
 * @returns {Promise<{count: number, next: string|null, previous: string|null, results: Array<{id: number, username: string, text: string, timestamp: string}>}>} Response with paginated messages
 * @throws {Error} If authentication fails or request is invalid
 */
export const getMessages = async (page = 1, pageSize = 50) => {
  const response = await instance.get('/api/messages/', {
    params: {
      page,
      page_size: pageSize,
    },
  });
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
