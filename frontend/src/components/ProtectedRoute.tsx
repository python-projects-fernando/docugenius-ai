// src/components/ProtectedRoute.tsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import type { User } from '../types/auth'; // Importe o tipo User

interface ProtectedRouteProps {
  children: React.ReactNode; // O componente filho (página) a ser renderizado
  allowedRoles?: ('admin' | 'common')[]; // Papéis permitidos, se não especificado, qualquer usuário logado pode acessar
  currentUser: User | null; // Usuário logado atual (ou null)
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles, currentUser }) => {
  const location = useLocation(); // Obtém a rota atual para redirecionar após login, se necessário

  // Verifica se o usuário está logado
  if (!currentUser) {
    // Se não estiver logado, redireciona para a página de login
    // e armazena a rota que o usuário tentou acessar
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Se papéis permitidos forem especificados, verifica se o papel do usuário está na lista
  if (allowedRoles && !allowedRoles.includes(currentUser.role)) {
    // Se o papel do usuário não estiver na lista de permitidos, redireciona para página de erro ou dashboard
    // Exemplo: redireciona para a página inicial
    return <Navigate to="/" replace />;
  }

  // Se estiver logado e tiver permissão, renderiza o componente filho
  return <>{children}</>;
};

export default ProtectedRoute;