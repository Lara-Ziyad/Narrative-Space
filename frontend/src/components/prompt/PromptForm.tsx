import { useState, FormEvent } from 'react';
import { generateResponse, fetchHistory } from '@api';
import ModelSelector from './ModelSelector';
import NarrativeTypeSelector from './NarrativeTypeSelector';
import RetrievalSelector from './RetrievalSelector';

type PromptFormProps = {
  onNewEntry?: () => void;
};
const PromptForm: React.FC<PromptFormProps> = ({ onNewEntry }) => {
  const [prompt, setPrompt] = useState<string>('');
  const [narrativeType, setNarrativeType] = useState<string>('poetic');
  const [model, setModel] = useState<string>('4.1-mini');
  const [response, setResponse] = useState<string>('');
  const [retrievalMode, setRetrievalMode] = useState<string>('faiss');
  const [error, setError] = useState<string>("");
   const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true);
    setResponse('');
    setError("");

    try {
      const data = await generateResponse({
        prompt,
        style: narrativeType,
        model,
        retrieval_mode: retrievalMode,
      });

      setResponse(data?.output ?? 'No output received.');
      onNewEntry?.();
    } catch (err) {
      console.error('❌ Error generating response:', err);
      setError(err?.message || '⚠️ Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section-wrapper">
      <h2 className="section-title">Describe Your Space</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          className="form-glass"
          rows={4}
          value={prompt}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setPrompt(e.target.value)}
          placeholder="Enter architectural or imaginative space..."
        />

        <div className="form-spacing">
          <NarrativeTypeSelector narrativeType={narrativeType} onChange={setNarrativeType} />
        </div>

        <div className="form-spacing">
          <ModelSelector model={model} onChange={setModel} />
        </div>

        <div className="form-spacing">
          <RetrievalSelector retrievalMode={retrievalMode} onChange={setRetrievalMode} />
        </div>

        <button type="submit" className="submit-btn">
          Generate
        </button>
      </form>

      {response && (
        <div className="mt-8 whitespace-pre-wrap">
          <h3 className="text-lg font-medium text-amberwood mb-2">📝 Generated Narrative:</h3>
          <p >{response}</p>
        </div>
      )}
    </div>
  );
};

export default PromptForm;
