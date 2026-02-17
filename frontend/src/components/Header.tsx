// src/components/Header.tsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import type { User } from '../types/auth'; // Importe o tipo User

// Interface define a forma das props
interface HeaderProps {
  currentUser: User | null; // Usuário logado ou null
  onLogout: () => void;    // Função para lidar com o logout
}

// Componente Header recebe as props e as utiliza
const Header: React.FC<HeaderProps> = ({ currentUser, onLogout }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout(); // Chama a função de logout passada via props
    navigate('/'); // Redireciona para a página inicial após logout
  };

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">DG</span>
            </div>
            <span className="text-xl font-bold text-gray-900">DocuGeniusAI</span>
          </div>
        </Link>

        <nav className="hidden md:flex space-x-8">
          {/* Exibe links baseados no papel do usuário ou estado de login, se necessário */}
          {currentUser && (
            <>
              {currentUser.role === 'admin' && (
                <Link to="/admin/dashboard" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                  Admin Panel
                </Link>
              )}
              {/* Exemplo de link comum para ambos os tipos de usuário logados */}
              {/* <Link to="/dashboard" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Dashboard
              </Link> */}
            </>
          )}
        </nav>

        <div className="flex items-center space-x-3">
          {currentUser ? (
            // Se estiver logado, mostra o nome do usuário e o botão de logout
            <>
              <span className="text-sm text-gray-600">Hello, {currentUser.username}</span>
              <button
                onClick={handleLogout}
                className="hidden md:inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            // Se não estiver logado, mostra o botão de login
            <Link to="/login">
              <button className="hidden md:inline-flex items-center px-4 py-2 bg-white border border-gray-300 text-gray-800 rounded-lg hover:bg-gray-50 font-medium transition-colors">
                Sign In
              </button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;