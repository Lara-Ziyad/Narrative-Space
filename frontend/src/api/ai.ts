const BASE_URL = import.meta.env.VITE_API_BASE_URL;

import type { HistoryItem } from '../context/HistoryContext';

type GenerateRequest = {
  prompt: string;
  type: string;
  model: string;
};

export type ProviderModel = {
  provider: string;
  id: string;
  label?: string;
};

export async function fetchModels(): Promise<ProviderModel[]> {
  const res = await fetch(`${BASE_URL}/ai/models`, {
    credentials: 'include',
  });
  if (!res.ok) throw new Error('Failed to list models');
  return res.json();
  const list = Array.isArray(raw) ? raw : [];
  const normalized: ProviderModel[] = list
    .map((m: any) => {
      if (typeof m === 'string') {
        return { provider: 'openai', id: m, label: `openai • ${m}` };
      }
      const id = m?.id ?? m?.model ?? m?.name ?? '';
      if (!id) return null;
      const provider = m?.provider ?? 'openai';
      const label = m?.label ?? m?.display ?? `${provider} • ${id}`;
      return { provider, id, label };
    })
    .filter(Boolean) as ProviderModel[];

  return normalized;
}

export async function generateResponse(data: GenerateRequest): Promise<{ response: string }> {
  const res = await fetch(`${BASE_URL}/ai/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
        prompt: data.prompt,
      style: data.type,
      model: data.model
      }),
  });

  if (!res.ok) throw new Error('Failed to generate');
  return res.json();
}

export async function fetchHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${BASE_URL}/ai/history`, {
    credentials: 'include',
  });

  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}