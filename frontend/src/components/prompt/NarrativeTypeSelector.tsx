import React from 'react';

type NarrativeTypeSelectorProps = {
  narrativeType: string;
  onChange: (value: string) => void;
};

const NarrativeTypeSelector: React.FC<NarrativeTypeSelectorProps> = ({ narrativeType, onChange }) => {
  return (
    <label>
      <span className="text-amberwood">Narrative Style:</span>
      <select
        value={narrativeType}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange(e.target.value)}
        className="form-glass"
      >
        <option value="poetic">Poetic</option>
        <option value="philosophical">Philosophical</option>
        <option value="critical">Critical</option>
        <option value="fictional">Fictional</option>
      </select>
    </label>
  );
};

export default NarrativeTypeSelector;
