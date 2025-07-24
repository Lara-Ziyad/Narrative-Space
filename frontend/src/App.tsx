import React, { useEffect, useState } from 'react';
import PromptForm from './components/PromptForm';
import HistoryPanel from './components/HistoryPanel';
import { fetchHistory } from './api';
import type { HistoryEntry } from './types';

const App: React.FC = () => {
    const [history, setHistory] = useState<HistoryEntry[]>([]);

    const refreshHistory = async () => {try {
        const data = await fetchHistory();
        setHistory(data);
      } catch (err) {console.error("⚠️ Failed to refresh history");}
  };

    useEffect(() => {refreshHistory();
        }, []);

    useEffect(() => {
  console.log("🔥 Updated history:", history);
}, [history]);

  return (
    <div className="app-container">
      <img
        src="/images/bg-orange.png"
        className="absolute inset-0 w-full h-full object-cover opacity-10 pointer-events-none z-0"
        alt="lines background"
      />

      <header className="app-header">
        <h1 className="app-title">Narrative Space</h1>
        <p className="app-subtitle">Generative AI for Architectural Narratives</p>
      </header>

      <main className="app-main mb-14 mt-14">
        <PromptForm onNewEntry={refreshHistory} />
      </main>


      <main className="app-main mt-10">
        <HistoryPanel history={history} />
      </main>
    </div>
  );
};

export default App;
