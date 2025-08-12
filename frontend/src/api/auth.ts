const BASE_URL = import.meta.env.VITE_API_BASE_URL;

type RegisterData = {
  username: string;
  email: string;
  password: string;
};

export async function register(data: RegisterData): Promise<{ message: string }> {
  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error('Failed to register');
  return res.json();
}

export async function login(email: string, password: string): Promise<{ message: string }> {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email, password }),
  });

    let data;
    try {
       data = await res.json();
       }
   catch (err) {
       throw new Error('Invalid JSON response from server');
   }

   if (!res.ok) {
      throw new Error(data?.message || 'Login failed');
      }

     return data;
   }

export async function logout(): Promise<{ message: string }> {
  const res = await fetch(`${BASE_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });

  if (!res.ok) throw new Error('Logout failed');
  return res.json();
}

export async function fetchProfile(): Promise<{ username: string; email: string }> {
  const res = await fetch(`${BASE_URL}/auth/profile`, {
    credentials: 'include',
  });

  if (!res.ok) throw new Error('Failed to fetch profile');
  return res.json();
}
