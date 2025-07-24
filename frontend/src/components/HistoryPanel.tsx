import { useEffect, useState } from 'react';
import { fetchHistory } from '../api';
type HistoryEntry = {
  id: string;
  prompt: string;
  response: string;
  timestamp?: string;
};

const HistoryPanel: React.FC = () => {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
  const loadHistory = async () => {
    try {
      const data = await fetchHistory();
      setHistory(data);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    }
  };

  loadHistory();
}, []);



  return (
   <div className="history-panel">
  <h2 className="history-heading">📜 History</h2>
  {error && <p className="history-error">{error}</p>}
  {history.length === 0 ? (
    <p className="history-empty">No history yet.</p>
  ) : (
    <ul className="space-y-6">
      {history.map((entry) => (
        <li key={entry.id} className="history-entry">
          <p className="history-prompt">
            <strong>Prompt:</strong> {entry.prompt}
          </p>
          <p className="history-response">
            <strong>Response:</strong> {entry.response}
          </p>
        </li>
      ))}
    </ul>
  )}
</div>
  );
};
export default HistoryPanel;
