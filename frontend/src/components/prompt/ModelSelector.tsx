// [NS-STEP6-PR1] ModelSelector: id-only labels, sanitize, fallback.
import React, { useEffect, useState } from 'react';
import { fetchModels, type ProviderModel } from '@api';

type ModelSelectorProps = { model: string; onChange: (value: string) => void; };
const LS_KEY = 'ns.selectedModel';

const FALLBACK: ProviderModel[] = [
  { provider: 'openai', id: 'gpt-4.1-mini', label: 'gpt-4.1-mini' },
  { provider: 'openai', id: 'gpt-4o-mini',  label: 'gpt-4o-mini' },
  { provider: 'openai', id: 'gpt-4o',       label: 'gpt-4o' },
];

const LEGACY_MAP: Record<string, string> = {
  '4.1-mini': 'openai:gpt-4.1-mini',
  'claude':   'anthropic:claude-3-haiku',
  'gemini':   'google:gemini-1.5-pro',
  'llama':    'ollama:llama3',
};

const sanitize = (v: string | null) => {
  if (!v) return null;
  if (LEGACY_MAP[v]) return LEGACY_MAP[v];
  if (v.includes('undefined')) return null;
  if (v.includes('.')) return v.replace(/^([a-z0-9_-]+)\./i, '$1:'); // provider.model -> provider:model
  if (!v.includes(':')) return null;
  return v;
};

const ModelSelector: React.FC<ModelSelectorProps> = ({ model, onChange }) => {
  const [models, setModels] = useState<ProviderModel[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    const saved = sanitize(localStorage.getItem(LS_KEY));
    const prop = sanitize(model);
    if (saved && !prop) onChange(saved);
    if (localStorage.getItem(LS_KEY) && !saved) localStorage.removeItem(LS_KEY);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setLoading(true);
    fetchModels()
      .then((data) => {
        setErr(null);
        const list = (data?.length ? data : FALLBACK).filter(m => m?.provider && m?.id);
        setModels(list);
        const valid = new Set(list.map(m => `${m.provider}:${m.id}`));
        if (!model || !valid.has(model)) {
          const first = list[0];
          const val = `${first.provider}:${first.id}`;
          onChange(val);
          localStorage.setItem(LS_KEY, val);
        }
      })
      .catch((e) => {
        setErr(e?.message ?? 'Failed to list models');
        setModels(FALLBACK);
        const val = `${FALLBACK[0].provider}:${FALLBACK[0].id}`;
        onChange(val);
        localStorage.setItem(LS_KEY, val);
      })
      .finally(() => setLoading(false));
  }, [model, onChange]);

  useEffect(() => {
    const s = sanitize(model);
    if (s) localStorage.setItem(LS_KEY, s);
  }, [model]);

  if (loading) return <span>Loading models…</span>;

  return (
    <label>
      <span className="text-amberwood">AI Model:</span>
      {err && <div className="text-red-600 text-sm mb-1">Failed to list models — using defaults.</div>}
      <select
        value={sanitize(model) || `${FALLBACK[0].provider}:${FALLBACK[0].id}`}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange(e.target.value)}
        className="form-glass"
      >
        {models.map((m) => {
          const value = `${m.provider}:${m.id}`;
          return (
            <option key={value} value={value}>
              {m.label ?? m.id} {/* id-only label */}
            </option>
          );
        })}
      </select>
    </label>
  );
};

export default ModelSelector;
