import { useEffect, useState } from 'react';
import { fetchHistory } from '../api';


type HistoryEntry = {
  id: number;
  prompt: string;
  response: string;
  timestamp?: string;
  style?: string;
  model?: string;
};

type HistoryPanelProps = {
  history: HistoryEntry[];
};

const HistoryPanel: React.FC<HistoryPanelProps> = ({ history }) => {
  return (
    <div className="history-panel">
      <h2 className="history-heading">📜 History</h2>
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
