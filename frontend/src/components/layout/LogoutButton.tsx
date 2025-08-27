import React from 'react';
import { useAuth } from '../../context/AuthContext';

const LogoutButton: React.FC = () => {
  const { logout, user } = useAuth();

  if (!user) return null; // hide button if not logged in

  return (
    <button
      onClick={logout}
      className="logout-btn"
    >
      Log out
    </button>
  );
};

export default LogoutButton;
