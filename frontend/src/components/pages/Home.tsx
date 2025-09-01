// [NS-STEP6-PR1] Added: Home page extracted from previous MainContent to keep App.tsx router-only.

import React, { useEffect } from 'react';
import AuthForms from '../auth/AuthForms';
import PromptForm from '../prompt/PromptForm';
import HistoryPanel from '../history/HistoryPanel';
import { HistoryProvider, useHistoryContext } from '../../context/HistoryContext';
import { useAuth } from '../../context/AuthContext';
import LoadingSpinner from '../layout/LoadingSpinner';
import LogoutButton from '../layout/LogoutButton';

const HomeInner: React.FC = () => {
  const { user, loading: authLoading, error: authError } = useAuth();
  const { loadHistory } = useHistoryContext();

  const userKey = user?.email ?? null;

  useEffect(() => {
    if (userKey) void loadHistory();
  }, [userKey]);

  return (
    <div className="app-container">
      <img
        src="/images/bg-orange.png"
        className="bg-pic"
        alt="lines background"
      />

      <header className="app-header">
        <h1 className="app-title">Narrative Space</h1>
        <p className="app-subtitle">Generative AI for Architectural Narratives</p>
      </header>

      <div className="logout-btn">
        <LogoutButton />
      </div>

      {authLoading && <LoadingSpinner />}

      {!authLoading && authError && user && (
        <div className=" mb-10 text-red-400 text-center ">
          There is something wrong which is : {authError}
        </div>
      )}

      {!authLoading && !user && (
        <div className="app-main  mt-20">
          <AuthForms />
        </div>
      )}

      {!authLoading && user && (
        <>
          <main className="app-main mb-14 mt-4">
            {/* [NS-STEP6-PR1] Kept: PromptForm props/signatures intact */}
            <PromptForm onNewEntry={loadHistory} />
          </main>
          <main className="app-main mt-10">
            <HistoryPanel />
          </main>
        </>
      )}
    </div>
  );
};

// [NS-STEP6-PR1] Note: HistoryProvider was at App level already; keep using the same context from there.
// If you ever render Home standalone (outside App), you can wrap it with HistoryProvider here.
const Home: React.FC = () => {
  return (
    // [NS-STEP6-PR1] Kept: rely on providers from App.tsx; no extra providers here.
    <HomeInner />
  );
};

export default Home;
