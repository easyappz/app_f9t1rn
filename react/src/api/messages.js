import instance from './axios';

/**
 * Get chat messages with pagination
 * @param {number} page - Page number (default: 1)
 * @param {number} pageSize - Number of messages per page (default: 50)
 * @returns {Promise} Response with paginated messages
 */
export const getMessages = async (page = 1, pageSize = 50) => {
  const token = localStorage.getItem('token');
  const response = await instance.get('/api/messages/', {
    params: {
      page,
      page_size: pageSize,
    },
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

/**
 * Send a new message to the chat
 * @param {string} text - Message text content
 * @returns {Promise} Response with created message data
 */
export const sendMessage = async (text) => {
  const token = localStorage.getItem('token');
  const response = await instance.post(
    '/api/messages/',
    {
      text,
    },
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );
  return response.data;
};
