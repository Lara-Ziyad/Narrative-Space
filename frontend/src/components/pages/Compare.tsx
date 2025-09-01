import React, { useEffect, useState } from 'react';
import { fetchModels, type ProviderModel, generateResponse } from '../../api/ai';

const Compare: React.FC = () => {
  const [models, setModels] = useState<ProviderModel[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [prompt, setPrompt] = useState('');
  const [style, setStyle] = useState('poetic');
  const [results, setResults] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    fetchModels().then(setModels).catch(console.error);
  }, []);

  const toggle = (val: string) => {
    setSelected((prev) => (prev.includes(val) ? prev.filter((v) => v !== val) : [...prev, val]));
  };

  const run = async () => {
    setBusy(true);
    const out: Record<string, string> = {};
    for (const key of selected) {
      const res = await generateResponse({ prompt, type: style, model: key });
      out[key] = res.output || '';
    }
    setResults(out);
    setBusy(false);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">Model Comparison</h2>

      <div className="mb-3">
        <textarea
          className="form-glass w-full"
          rows={4}
          placeholder="Enter your spatial description…"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
      </div>

      <div className="mb-3">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {models.map((m) => {
            const val = `${m.provider}:${m.id}`;
            const checked = selected.includes(val);
            return (
              <label key={val} className="flex items-center gap-2">
                <input type="checkbox" checked={checked} onChange={() => toggle(val)} />
                <span>{m.label ?? `${m.provider} • ${m.id}`}</span>
              </label>
            );
          })}
        </div>
      </div>

      <div className="flex items-center gap-2 mb-4">
        <select className="form-glass" value={style} onChange={(e) => setStyle(e.target.value)}>
          <option value="poetic">Poetic</option>
          <option value="philosophical">Philosophical</option>
          <option value="critical">Critical</option>
          <option value="fictional">Fictional</option>
        </select>
        <button className="btn-primary" disabled={!prompt || selected.length === 0 || busy} onClick={run}>
          {busy ? 'Comparing…' : 'Compare'}
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-4 mt-6">
        {Object.entries(results).map(([k, v]) => (
          <div key={k} className="p-3 rounded-xl shadow bg-white/70">
            <div className="text-sm text-gray-600 mb-2">{k}</div>
            <div className="whitespace-pre-wrap">{v}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Compare;
