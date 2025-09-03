import { BASE_URL } from './config';

import type { HistoryItem } from '../context/HistoryContext';

export type GenerateRequest = { prompt: string; style: string; model: string };
export type ProviderModel = { provider: string; id: string; label?: string };

export async function fetchModels(): Promise<ProviderModel[]> {
  // Point to the versioned endpoint to avoid legacy collisions.
  const url = `${BASE_URL}/ai/models?format=compact`;
  const res = await fetch(url, { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to list models');

  const raw = await res.json();
   // raw is expected to be an array in compact mode; still keep a tolerant fallback.
  const arr = Array.isArray(raw) ? raw : (Array.isArray((raw as any)?.models) ? (raw as any).models : []);

  const normalized: ProviderModel[] = (arr as any[]).map((m: any) => {
    if (typeof m === 'string') {
      return { provider: 'openai', id: m, label: m };
    }
    const id = m?.id ?? m?.model ?? m?.name ?? '';
    if (!id) return null as any;
    const provider = m?.provider ?? 'openai';
    const label = m?.label ?? id;
    return { provider, id, label };
  }).filter(Boolean) as ProviderModel[];

  // Debug log (safe in dev)
  // eslint-disable-next-line no-console
  console.log('[ai/models] url:', url, 'raw:', raw, 'normalized:', normalized);

  return normalized;
}

export async function generateResponse(data: GenerateRequest): Promise<{ output: string; sources?: any; retrieval_mode?: string }> {
  const res = await fetch(`${BASE_URL}/ai/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ prompt: data.prompt, style: data.style, model: data.model }),
  });
  if (!res.ok) throw new Error('Failed to generate');
  return res.json();
}

export async function fetchHistory(): Promise<HistoryItem[]> {
  const res = await fetch(`${BASE_URL}/ai/history`, { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}
