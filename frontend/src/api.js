const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function generateResponse(prompt) {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ prompt }),
  });

  if (!res.ok) throw new Error('Failed to generate');
  return res.json();
}
