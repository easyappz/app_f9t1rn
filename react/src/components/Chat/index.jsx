import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMessages, sendMessage } from '../../api/messages';
import './styles.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    loadMessages();
  }, [navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadMessages = async () => {
    try {
      setLoading(true);
      const data = await getMessages();
      setMessages(data.results || []);
    } catch (error) {
      console.error('Error loading messages:', error);
      if (error.response && error.response.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!messageText.trim()) {
      return;
    }

    try {
      setSending(true);
      await sendMessage(messageText);
      setMessageText('');
      await loadMessages();
    } catch (error) {
      console.error('Error sending message:', error);
      if (error.response && error.response.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    } finally {
      setSending(false);
    }
  };

  const handleProfileClick = () => {
    navigate('/profile');
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  return (
    <div className="chat-container" data-easytag="id1-react/src/components/Chat/index.jsx">
      <div className="chat-header">
        <div className="chat-header-title">
          <h1>Групповой чат</h1>
        </div>
        <button className="profile-button" onClick={handleProfileClick}>
          Профиль
        </button>
      </div>

      <div className="chat-messages">
        {loading ? (
          <div className="chat-loading">Загрузка сообщений...</div>
        ) : messages.length === 0 ? (
          <div className="chat-empty">Нет сообщений</div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className="message-item">
              <div className="message-header">
                <span className="message-author">{message.author}</span>
                <span className="message-time">{formatTime(message.created_at)}</span>
              </div>
              <div className="message-text">{message.text}</div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSendMessage} className="chat-form">
          <textarea
            className="chat-textarea"
            placeholder="Напишите сообщение..."
            value={messageText}
            onChange={(e) => setMessageText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage(e);
              }
            }}
            disabled={sending}
            rows={1}
          />
          <button
            type="submit"
            className="chat-send-button"
            disabled={sending || !messageText.trim()}
          >
            {sending ? 'Отправка...' : 'Отправить'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chat;