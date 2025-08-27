// src/context/AuthContext.tsx
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from 'react';
import { fetchProfile, logout as apiLogout } from '@api';

/**
 * Minimal user shape coming from /auth/profile
 * Add more fields if your backend returns them.
 */
export type User = {
  username: string;
  email: string;
} | null;

type AuthContextValue = {
  /** Current authenticated user, or null when not logged in */
  user: User;
  /** True while verifying/restoring the session */
  loading: boolean;
  /** Last non-fatal auth error */
  error: string | null;
  /** Re-check session from the server (GET /auth/profile) */
  refresh: () => Promise<void>;
  /** Log out and clear local state */
  logout: () => Promise<void>;
};

/** Safe default so consumers never crash even outside the provider */
const defaultValue: AuthContextValue = {
  user: null,
  loading: true,
  error: null,
  refresh: async () => {},
  logout: async () => {},
};

const AuthContext = createContext<AuthContextValue>(defaultValue);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const u = await fetchProfile();
      setUser(u ?? null);
    } catch (e) {
      console.error('fetchProfile failed:', e);
      setUser(null);
      setError(e instanceof Error ? e.message : 'Failed to fetch profile');
    } finally {
      setLoading(false);
    }
  }, []);


  /** Logs out on the server and clears local state */
  const logout = useCallback(async () => {
    try {
      await apiLogout();
    } catch (e) {
      console.error('logout failed:', e);
    } finally {
      setUser(null);
    }
  }, []);

  /** Verify session on first mount */
  useEffect(() => {
    void refresh();
  }, [refresh]);

  return (
    <AuthContext.Provider value={{ user, loading, error, refresh, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextValue => useContext(AuthContext);
