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

  const defaultModel = localStorage.getItem('ns.selectedModel') || 'openai:gpt-4o-mini';
  const [model, setModel] = useState<string>(defaultModel);

  const [response, setResponse] = useState<string>('');
  const [retrievalMode, setRetrievalMode] = useState<string>('faiss');
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!prompt.trim()){
      setError('⚠️ Please add a description!  ');
      return;
    }

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

      setPrompt('');
      onNewEntry?.();
    } catch (err: any) {
      console.error('❌ Error generating response:', err);
      setError(err?.message || '⚠️ Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section-wrapper">
      <h2 className="section-title">Describe Your Space</h2>

      {/* [NS-STEP6-PR1] Kept: same form tags and onSubmit handler name */}
      <form onSubmit={handleSubmit}>
        <textarea
          className="form-glass"
          rows={4}
          value={prompt}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setPrompt(e.target.value)}
          placeholder="Enter architectural or imaginative space..."
          disabled={loading}
        />
        {error && <div className="auth-error">{error}</div>}

        <div className="form-spacing">
          {/* [NS-STEP6-PR1] Kept: same component and prop names */}
          <NarrativeTypeSelector narrativeType={narrativeType} onChange={setNarrativeType} />
        </div>

        <div className="form-spacing">
          {/* [NS-STEP6-PR1] Confirmed: ModelSelector passes/receives provider-qualified model (e.g., openai:gpt-4o-mini) */}
          <ModelSelector model={model} onChange={setModel} />
        </div>

        <div className="form-spacing">
          {/* [NS-STEP6-PR1] Kept: retrieval selector unchanged; value sent as retrieval_mode */}
          <RetrievalSelector retrievalMode={retrievalMode} onChange={setRetrievalMode} />
        </div>

        {/* [NS-STEP6-PR1] Kept: same submit button tags/structure */}
        <button type="submit" className="submit-btn">
          {loading ? (
            // Inline spinner inside the button
            <span className="submit-btn-span">
              <span className="submit-btn-generating" />
              Generating…
            </span>
          ) : (
            'Generate'
          )}
        </button>
      </form>

      {response && (
        <div className="mt-8 whitespace-pre-wrap">
          <h3 className="text-lg font-medium text-amberwood mb-2">📝 Generated Narrative:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default PromptForm;
