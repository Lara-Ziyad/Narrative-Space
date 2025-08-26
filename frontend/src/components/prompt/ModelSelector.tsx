import React from 'react';

type ModelSelectorProps = {
  model: string;
  onChange: (value: string) => void;
};

const ModelSelector: React.FC<ModelSelectorProps> = ({ model, onChange }) => {
  return (
    <label>
      <span className="text-amberwood">AI Model:</span>
      <select
        value={model}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange(e.target.value)}
        className="form-glass"
      >
        <option value="4.1-mini">GPT-4.1 Mini</option>
        <option value="claude">Claude</option>
        <option value="gemini">Gemini</option>
        <option value="llama">LLaMA</option>
      </select>
    </label>
  );
};

export default ModelSelector;
