// src/App.tsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom'; // Adicione Navigate se ainda não estiver importado
import Header from './components/Header';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute'; // Importe o componente ProtectedRoute
import Login from './pages/Login';
import AdminDashboard from './pages/admin/AdminDashboard';
import ManageDocumentTypes from './pages/admin/ManageDocumentTypes';
import type { User } from './types/auth';

// Componente da Página Inicial (mantendo seu código atual, MAS SEM O HEADER e SEM O FOOTER)
const HomePage = () => {
  // REMOVA TODO O CONTEÚDO DO HEADER AQUI
  // REMOVA TODO O CONTEÚDO DO FOOTER AQUI
  // O Header e Footer agora são componentes separados e são gerenciados pelo App.tsx
  return (
    // O restante do conteúdo da HomePage permanece o mesmo, SEM O HEADER e SEM O FOOTER
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* REMOVA ESTE BLOCO DE HEADER */}
      {/* <header className="bg-white border-b border-gray-200 shadow-sm">
        ...
      </header> */}
      {/* FIM DO BLOCO HEADER A SER REMOVIDO */}

      {/* Mantenha o MAIN */}
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

      {/* NÃO INCLUA O FOOTER AQUI NO HomePage */}
    </div>
  );
};

// Componente App principal com Router, Header, Routes e Footer
const App: React.FC = () => {
  // Estado para armazenar o usuário logado
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  // useEffect para carregar o estado do usuário do localStorage ao montar o componente
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const parsedUser: User = JSON.parse(storedUser);
        setCurrentUser(parsedUser);
      } catch (error) {
        console.error('Erro ao parsear dados do usuário do localStorage:', error);
        // Opcional: Limpar localStorage se estiver corrompido
        localStorage.removeItem('user');
        localStorage.removeItem('accessToken'); // Limpar token também se o user estiver corrompido
      }
    }
  }, []); // O array de dependências vazio [] garante que este efeito rode apenas uma vez após a montagem inicial

  // Função para lidar com o logout
  const handleLogout = () => {
    console.log('Logout acionado no App.tsx');
    // Limpar o estado do usuário
    setCurrentUser(null);
    // Limpar os dados do localStorage
    localStorage.removeItem('user');
    localStorage.removeItem('accessToken');
  };

  // Função para lidar com o sucesso do login (chamada pelo componente Login.tsx)
  const handleLoginSuccess = (user: User) => {
    console.log('Login bem-sucedido detectado no App.tsx');
    setCurrentUser(user); // Atualiza o estado local do App com o novo usuário
  };

  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        {/* Renderize o Header no topo */}
        <Header currentUser={currentUser} onLogout={handleLogout} />
        {/* O conteúdo principal das rotas */}
        <div className="flex-grow">
          <Routes>
            {/* Rota para a página inicial */}
            <Route path="/" element={<HomePage />} />
            {/* Rota para a página de login - PASSA A FUNÇÃO handleLoginSuccess */}
            <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess} />} />
            {/* Rotas protegidas para admin */}
            <Route path="/admin/dashboard" element={
              <ProtectedRoute allowedRoles={['admin']} currentUser={currentUser}>
                <AdminDashboard />
              </ProtectedRoute>
            } />
            <Route path="/admin/document-types" element={
              <ProtectedRoute allowedRoles={['admin']} currentUser={currentUser}>
                <ManageDocumentTypes />
              </ProtectedRoute>
            } />
            {/* Rota curinga para páginas não encontradas (opcional) */}
            <Route path="*" element={<div>Page Not Found</div>} />
          </Routes>
        </div>
        {/* Renderize o Footer na parte inferior */}
        <Footer />
      </div>
    </Router>
  );
};

export default App;