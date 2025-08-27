import React, { useEffect }  from 'react';
import AuthForms from './components/auth/AuthForms';
import PromptForm from './components/prompt/PromptForm';
import HistoryPanel from './components/history/HistoryPanel';
import { HistoryProvider, useHistoryContext } from './context/HistoryContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoadingSpinner from './components/layout/LoadingSpinner';


const MainContent: React.FC = () => {
    const { user, loading: authLoading, error: authError } = useAuth();
    const { history, loadHistory } = useHistoryContext();
    const userKey = user?.email ?? null;
    useEffect(() => {
    if (userKey) void loadHistory();
    }, [userKey]);

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

            {authLoading && <LoadingSpinner />}

            {!authLoading && authError && (
               <div className="p-3 text-red-400 text-sm">Failed to verify session: {authError}</div>
            )}

            {!authLoading && !user && (
               <div>
                 <AuthForms />
               </div>
            )}



      {!authLoading && user && (
        <>
         <div>
             <AuthForms />
         </div>
          <main className="app-main mb-14 mt-14">
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

const App: React.FC = () => {
  return (
      <AuthProvider>
        <HistoryProvider>
          <MainContent />
        </HistoryProvider>
      </AuthProvider>

  );
};

export default App;
