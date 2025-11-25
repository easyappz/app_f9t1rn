import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProfile, logout } from '../../api/auth';
import './styles.css';

const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchProfile = async () => {
      try {
        const data = await getProfile();
        setUser(data);
        setLoading(false);
      } catch (err) {
        setError(err.response?.data?.error || err.message || 'Ошибка загрузки профиля');
        setLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleBackToChat = () => {
    navigate('/chat');
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Не указана';
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getInitials = (username) => {
    if (!username) return '?';
    return username.charAt(0).toUpperCase();
  };

  if (loading) {
    return (
      <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
        <div className="profile-card">
          <div className="loading-message">Загрузка профиля...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
        <div className="profile-card">
          <div className="profile-header">
            <h1>Ошибка</h1>
          </div>
          <p className="error-message">{error}</p>
          <div className="profile-actions">
            <button onClick={handleLogout} className="logout-button">
              Вернуться к входу
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
      <div className="profile-card">
        <div className="profile-header">
          <div className="avatar-placeholder">
            {getInitials(user?.username)}
          </div>
          <h1>Профиль пользователя</h1>
        </div>
        <div className="profile-content">
          <div className="profile-info">
            <div className="info-row">
              <span className="info-label">Имя пользователя:</span>
              <span className="info-value">{user?.username}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Дата регистрации:</span>
              <span className="info-value">{formatDate(user?.created_at)}</span>
            </div>
          </div>
          <div className="profile-actions">
            <button onClick={handleBackToChat} className="back-button">
              ← Вернуться в чат
            </button>
            <button onClick={handleLogout} className="logout-button">
              Выйти из аккаунта
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;