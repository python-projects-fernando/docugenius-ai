// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './pages/Login';
import AdminDashboard from './pages/admin/AdminDashboard'; // Importe o componente AdminDashboard

// Componente da Página Inicial (mantendo seu código atual)
const HomePage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">DG</span>
            </div>
            <span className="text-xl font-bold text-gray-900">DocuGeniusAI</span>
          </div>
          <nav className="hidden md:flex space-x-8">
            {/* Adicione links aqui se necessário */}
          </nav>
          <div className="flex items-center space-x-3">
            {/* Substitua o botão "Sign In" por um Link para /login */}
            <Link to="/login">
              <button className="hidden md:inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-800 rounded-lg hover:bg-gray-50 font-medium transition-colors">
                Sign In
              </button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-grow flex items-center py-16">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="text-center">
            <span className="inline-flex items-center px-4 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mb-4">
              Core Identity
            </span>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Precision Intelligence
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-10">
              DocuGeniusAI combines professional reliability with cutting-edge artificial intelligence.
              Our platform ensures accuracy, clarity, and efficiency in every document lifecycle, driven by smart, intuitive design.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
              <div className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Reliability</h3>
                <p className="text-gray-600 text-sm">
                  Robust engineering, consistent performance, and enterprise-grade stability.
                </p>
              </div>

              <div className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Innovation</h3>
                <p className="text-gray-600 text-sm">
                  AI-powered schema generation and intelligent automation at your fingertips.
                </p>
              </div>

              <div className="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Clarity</h3>
                <p className="text-gray-600 text-sm">
                  Clean interfaces, structured outputs, and zero ambiguity in document workflows.
                </p>
              </div>
            </div>

            <div className="mt-16">
              <button className="px-8 py-3 bg-gray-900 hover:bg-black text-white font-medium rounded-lg transition-colors duration-200 shadow-md">
                Explore the Platform
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-gray-100 text-gray-600 py-8 border-t border-gray-200">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; {new Date().getFullYear()} DocuGeniusAI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

// Componente App principal com Router e Rotas
const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Rota para a página inicial */}
        <Route path="/" element={<HomePage />} />
        {/* Rota para a página de login */}
        <Route path="/login" element={<Login />} />
        {/* Rota para o dashboard do admin */}
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        {/* Rota curinga para páginas não encontradas (opcional) */}
        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
    </Router>
  );
};

export default App;