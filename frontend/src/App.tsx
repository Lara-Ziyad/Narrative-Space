import React from 'react';
import { AuthProvider } from './context/AuthContext';
import { HistoryProvider } from './context/HistoryContext';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'; // <= مهم يكون سطر واحد

import Home from './components/pages/Home';
import Compare from './components/pages/Compare';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <HistoryProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </HistoryProvider>
    </AuthProvider>
  );
};

export default App;
