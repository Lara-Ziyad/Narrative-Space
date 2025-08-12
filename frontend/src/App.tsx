import React from 'react';
import AuthForms from './components/auth/AuthForms';
import PromptForm from './components/prompt/PromptForm';
import HistoryPanel from './components/history/HistoryPanel';
import { HistoryProvider, useHistoryContext } from './context/HistoryContext';

const MainContent: React.FC = () => {
  const { history, loadHistory } = useHistoryContext();

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

      <div>
        <AuthForms />
      </div>

      <main className="app-main mb-14 mt-14">
        {/* When generation is done, reload history */}
        <PromptForm onNewEntry={loadHistory} />
      </main>

      <main className="app-main mt-10">
        <HistoryPanel history={history} />
      </main>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <HistoryProvider>
      <MainContent />
    </HistoryProvider>
  );
};

export default App;
