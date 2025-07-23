import React from 'react';

type ModelSelectorProps = {
  model: string;
  onChange: (value: string) => void;
};

const ModelSelector: React.FC<ModelSelectorProps> = ({ model, onChange }) => {
  return (
    <label>
      AI Model:
      <select value={model} onChange={(e) => onChange(e.target.value)}
        className="form-glass">
        <option value="gpt-4">GPT-4</option>
        <option value="claude">Claude</option>
        <option value="gemini">Gemini</option>
        <option value="llama">LLaMA</option>
      </select>
    </label>
  );
};

export default ModelSelector;
