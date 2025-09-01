// [NS-STEP6-PR1] Added: Dynamic ModelSelector with robust fallback when saved value is invalid.
import React, { useEffect, useState } from 'react';
import { fetchModels, type ProviderModel } from '@api';

type ModelSelectorProps = {
  model: string;
  onChange: (value: string) => void;
};

const LS_KEY = 'ns.selectedModel';

const ModelSelector: React.FC<ModelSelectorProps> = ({ model, onChange }) => {
  const [models, setModels] = useState<ProviderModel[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    // [NS-STEP6-PR1] Hydrate from LocalStorage once (if parent didn't pass value yet)
    const saved = localStorage.getItem(LS_KEY);
    if (saved && !model) onChange(saved);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setLoading(true);
    fetchModels()
      .then((data) => {
        setModels(data);
        // [NS-STEP6-PR1] If current value is invalid, pick the first available.
        const options = new Set(data.map((m) => `${m.provider}:${m.id}`));
        if (!model || !options.has(model)) {
          const first = data[0];
          if (first) {
            const val = `${first.provider}:${first.id}`;
            onChange(val);
            localStorage.setItem(LS_KEY, val);
          }
        }
      })
      .catch((e) => setErr(e?.message ?? 'Failed to load models'))
      .finally(() => setLoading(false));
  }, [model, onChange]);

  useEffect(() => {
    // [NS-STEP6-PR1] Persist every change
    if (model) localStorage.setItem(LS_KEY, model);
  }, [model]);

  if (loading) return <span>Loading models…</span>;
  if (err) return <span className="text-red-600">{err}</span>;

  return (
    <label className="flex flex-col gap-1">
      <span className="text-sm font-medium">AI Model</span>
      <select
        value={model}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange(e.target.value)}
        className="form-glass"
      >
        {models.map((m) => {
          const value = `${m.provider}:${m.id}`;
          return (
            <option key={value} value={value}>
              {m.label ?? `${m.provider} • ${m.id}`}
            </option>
          );
        })}
      </select>
    </label>
  );
};

export default ModelSelector;
