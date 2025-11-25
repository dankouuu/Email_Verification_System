import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App.jsx';
import SendEmailPage from './pages/SendEmailPage.jsx';
import VerificationPage from './pages/VerificationPage.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}/>
        <Route path="/send" element={<SendEmailPage />}/>
        <Route path="/verify" element={<VerificationPage />}/>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
