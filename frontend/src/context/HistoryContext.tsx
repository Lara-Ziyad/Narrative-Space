import { createContext, useContext, useState, useEffect } from 'react';
import { fetchHistory } from '@api';

const HistoryContext = createContext<any>(null);

export const HistoryProvider = ({ children }: { children: React.ReactNode }) => {
  const [history, setHistory] = useState([]);

  const loadHistory = async () => {
    try {
      const data = await fetchHistory();
      setHistory(data);
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
