import { createContext, useContext, useState, useEffect } from 'react';
import { fetchHistory } from '@api';

export type HistoryItem = {
  id: number;
  prompt: string;
  response: string;
  model?: string | null;
  style?: string | null;
  timestamp?: string | null; // ISO string from server
};

export type HistoryContextValue = {
  history: HistoryItem[];
  setHistory: React.Dispatch<React.SetStateAction<HistoryItem[]>>;
  loadHistory: () => Promise<void>;
};

const HistoryContext = createContext<HistoryContextValue | undefined>(undefined);

export const HistoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [history, setHistory] = useState<HistoryItem[]>([]);

  const loadHistory = async () => {
    try {
      const data = await fetchHistory();
      setHistory(Array.isArray(data) ? (data as HistoryItem[]) : []);
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  return (
    <HistoryContext.Provider value={{ history, setHistory, loadHistory }}>
      {children}
    </HistoryContext.Provider>
  );
};

export const useHistoryContext = () => useContext(HistoryContext);

