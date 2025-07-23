const BASE_URL = import.meta.env.VITE_API_BASE_URL;

type GenerateRequest = {
  prompt: string;
  type: string;
  model: string;
};

export async function generateResponse(data: GenerateRequest): Promise<{ response: string }> {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error('Failed to generate');
  return res.json();
}
