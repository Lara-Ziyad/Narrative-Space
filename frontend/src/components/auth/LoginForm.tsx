import { useState } from 'react';
const BASE_URL = import.meta.env.VITE_API_BASE_URL;
import { fetchHistory } from '@api';
import { useHistoryContext } from '../../context/HistoryContext';
import { useAuth } from '../../context/AuthContext';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const { loadHistory } = useHistoryContext();
  const { refresh } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || 'Login failed');
      }

      await refresh();
      alert('✅ Logged in successfully');
      await loadHistory();
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div >
      <h2 className="auth-title">Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          className="auth-input"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="auth-input"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <div className="auth-error">{error}</div>}

        <button type="submit" className="auth-button">
          Login
        </button>
      </form>
    </div>
  );
}
