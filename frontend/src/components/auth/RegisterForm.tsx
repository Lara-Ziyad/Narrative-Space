import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { register } from '../../api/auth'; // adjust path if your alias is @api/auth

export default function RegisterForm() {
  const [username, setUsername] = useState('');
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState<string>('');
  const [loading, setLoading]   = useState(false);
  const [success, setSuccess]   = useState<string>('');

  const { refresh } = useAuth();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register({ username, email, password });
      setSuccess('✅ Registration successful. Please log in to continue.');

//       await refresh();

      // (Optional) clear inputs
      setUsername('');
      setEmail('');
      setPassword('');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Registration failed';
      setError(msg);
      setUsername('');
      setEmail('');
      setPassword('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="auth-title">Register</h2>

      <form onSubmit={handleRegister}>
        <input
          type="text"
          className="auth-input"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="email"
          className="auth-input"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          className="auth-input"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
         {success && <p className= 'mt-4'>{success}</p>}
        {error && <div className="auth-error">{error}</div>}

        <button type="submit" className="auth-button" disabled={loading}>
          {loading ? 'Registering…' : 'Register'}
        </button>
      </form>
    </div>
  );
}
