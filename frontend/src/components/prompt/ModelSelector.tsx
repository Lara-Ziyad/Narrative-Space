import React, { useEffect, useState } from 'react';
import { fetchModels, type ProviderModel } from '@api';

type ModelSelectorProps = {
  model: string;
  onChange: (value: string) => void;
};

const LS_KEY = 'ns.selectedModel';

const FALLBACK: ProviderModel[] = [
  { provider: 'openai', id: 'gpt-4.1-mini', label: 'gpt-4.1-mini' },
  { provider: 'openai', id: 'gpt-4o-mini',  label: 'gpt-4o-mini' },
  { provider: 'openai', id: 'gpt-4o',       label: 'gpt-4o' },
];

function sanitize(val: string | null): string | null {
  if (!val) return null;
  if (val.includes('undefined')) return null;
  if (val.includes('.')) val = val.replace(/^([a-z0-9_-]+)\./i, '$1:');
  if (!val.includes(':')) return null;
  return val;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ model, onChange }) => {
  const [models, setModels] = useState<ProviderModel[]>([]);
  const [loading, setLoading] = useState(false);
  const [warn, setWarn] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    (async () => {
      setLoading(true);
      try {
        const data = await fetchModels();
        const list = (data?.length ? data : FALLBACK).filter(m => m?.provider && m?.id);
        if (!mounted) return;
        setModels(list);
        setWarn(data?.length ? null : 'Failed to list models — using defaults.');
        const valid = new Set(list.map(m => `${m.provider}:${m.id}`));
        const fromProp = sanitize(model);
        const fromLS   = sanitize(localStorage.getItem(LS_KEY));
        const first    = `${list[0].provider}:${list[0].id}`;
        const chosen   = valid.has(fromProp || '') ? (fromProp as string)
                        : valid.has(fromLS || '') ? (fromLS as string)
                        : first;
        if (chosen !== model) onChange(chosen);
        localStorage.setItem(LS_KEY, chosen);
      } catch {
        if (!mounted) return;
        setModels(FALLBACK);
        setWarn('Failed to list models — using defaults.');
        const first = `${FALLBACK[0].provider}:${FALLBACK[0].id}`;
        if (first !== model) onChange(first);
        localStorage.setItem(LS_KEY, first);
      } finally {
        setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []); // run once

  useEffect(() => {
    const s = sanitize(model);
    if (s) localStorage.setItem(LS_KEY, s);
  }, [model]);

  if (loading) return <span>Loading models…</span>;

  const options = models.length ? models : FALLBACK;
  const current = sanitize(model) || `${options[0].provider}:${options[0].id}`;

  return (
    <label>
      <span className="text-amberwood">AI Model:</span>
      {warn && <div className="text-red-600 text-sm mb-1">{warn}</div>}
      <select
        className="form-glass"
        value={current}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
          const next = sanitize(e.target.value) || e.target.value;
          onChange(next);
          localStorage.setItem(LS_KEY, next);
        }}
      >
        {options.map((m) => {
          const value = `${m.provider}:${m.id}`;
          return (
            <option key={value} value={value}>
              {m.label ?? m.id}
            </option>
          );
        })}
      </select>
    </label>
  );
};

export default ModelSelector;
