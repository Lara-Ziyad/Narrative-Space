import React from 'react';

type RetrievalSelectorProps = {
  retrievalMode: string; // "faiss" | "chroma"
  onChange: (value: string) => void;
};

const RetrievalSelector: React.FC<RetrievalSelectorProps> = ({ retrievalMode, onChange }) => {
  return (
    <div className="space-y-1">
      <label className="block space-y-2">
        <span className="text-amberwood">Context Source (How should we search your knowledge?)</span>
        <select
          value={retrievalMode}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) => onChange(e.target.value)}
          className="form-glass"
        >
          <option value="faiss">Fast semantic search (Vector Index)</option>
          <option value="chroma">Precise search with filters (Metadata)</option>
        </select>
      </label>
      <p className="text-xs text-amberwood/70">
        • <strong>Fast semantic search</strong>: best for large general text, quickest results.<br />
        • <strong>Precise search with filters</strong>: best when documents have tags/metadata for accurate filtering.
      </p>
    </div>
  );
};

export default RetrievalSelector;
