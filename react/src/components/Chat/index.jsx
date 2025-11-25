import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMessages, sendMessage } from '../../api/messages';
import './styles.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  const intervalRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    loadMessages();

    intervalRef.current = setInterval(() => {
      loadMessages(true);
    }, 3000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadMessages = async (silent = false) => {
    try {
      if (!silent) {
        setLoading(true);
      }
      setError('');
      const data = await getMessages();
      setMessages(data || []);
    } catch (error) {
      console.error('Error loading messages:', error);
      if (!silent) {
        setError('Не удалось загрузить сообщения');
      }
      if (error.response && error.response.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    } finally {
      if (!silent) {
        setLoading(false);
      }
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!messageText.trim()) {
      return;
    }

    try {
      setSending(true);
      setError('');
      await sendMessage(messageText);
      setMessageText('');
      await loadMessages(true);
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Не удалось отправить сообщение');
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

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${day}.${month}.${year} ${hours}:${minutes}`;
  };

  return (
    <div className="chat-container" data-easytag="id1-react/src/components/Chat/index.jsx">
      <div className="chat-header">
        <div className="chat-header-left">
          <h1 className="chat-title">Корпоративный чат</h1>
        </div>
        <div className="chat-header-right">
          <button className="profile-link" onClick={handleProfileClick}>
            Профиль
          </button>
        </div>
      </div>

      <div className="chat-messages">
        {loading ? (
          <div className="chat-loading">Загрузка сообщений...</div>
        ) : error ? (
          <div className="chat-error">{error}</div>
        ) : messages.length === 0 ? (
          <div className="chat-empty">Нет сообщений. Начните общение!</div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className="message-bubble">
              <div className="message-header">
                <span className="message-username">{message.username}</span>
                <span className="message-timestamp">{formatTimestamp(message.timestamp)}</span>
              </div>
              <div className="message-text">{message.text}</div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <form onSubmit={handleSendMessage} className="chat-form">
          <input
            type="text"
            className="chat-input"
            placeholder="Напишите сообщение..."
            value={messageText}
            onChange={(e) => setMessageText(e.target.value)}
            disabled={sending}
          />
          <button
            type="submit"
            className="chat-send-button"
            disabled={sending || !messageText.trim()}
          >
            {sending ? 'Отправка...' : 'Отправить'}
          </button>
        </form>
        {error && <div className="input-error">{error}</div>}
      </div>
    </div>
  );
};

export default Chat;