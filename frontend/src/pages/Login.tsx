// src/pages/Login.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config/api';
import type { LoginRequestDTO, LoginResponseDTO, User, UserRole } from '../types/auth';

const Login: React.FC = () => {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!identifier.trim() || !password.trim()) {
      setError('Username and Password are required.');
      return;
    }

    try {

      const requestBody: LoginRequestDTO = {
        identifier, // Nome correto esperado pelo backend
        password,
      };

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      const  LoginResponseDTO = await response.json(); // Tipa a resposta

      if (response.ok && LoginResponseDTO.success) { // Checa se a resposta foi bem-sucedida e se data.success é true
        // Extrai o papel (role) do usuário da resposta usando o DTO
        const userRole: UserRole = LoginResponseDTO.data.user.role;
        const userDataFromResponse = LoginResponseDTO.data.user;

        // Opcional: Converter a resposta do backend para o tipo User do frontend
        // Isso é útil se os campos forem ligeiramente diferentes entre backend e frontend.
        const frontendUser: User = {
          id: userDataFromResponse.id.toString(), // Converte number para string se necessário
          username: userDataFromResponse.username,
          email: userDataFromResponse.email,
          role: userDataFromResponse.role,
        };

        // Armazenar dados do usuário no localStorage (opcional, mas comum)
        localStorage.setItem('user', JSON.stringify(frontendUser));
        localStorage.setItem('accessToken', LoginResponseDTO.data.access_token); // Armazene o token se for usar

        // Verifica o papel do usuário e redireciona
        if (userRole === 'admin') {
          navigate('/admin/dashboard'); // Redireciona para o dashboard do admin
        } else if (userRole === 'common') {
          // Opcional: redirecionar para um dashboard comum ou para a home
          navigate('/'); // Exemplo: redireciona para a home
        } else {
          // Tratar outros papéis se necessário
          // Redirecionar para uma página padrão ou perguntar ao usuário
          navigate('/'); // Exemplo: redireciona para a home
        }

      } else {
        // Tenta obter a mensagem de erro da resposta
        let errorMessage = data.message || `Error ${response.status}: ${response.statusText}`;
        // Ajuste aqui se a estrutura de erro for diferente
        if (response.status === 422) {
          // Exemplo: se a API retornar detalhes de erro em 'errors'
          if (Array.isArray(data.errors) && data.errors.length > 0) {
             errorMessage = `Validation Error: ${data.errors.map(e => e.msg).join(', ')}`;
          } else {
             errorMessage = 'Validation Error: Please check the provided data.'; // Mensagem genérica
          }
        }
        setError(errorMessage);
      }
    } catch (err) {
      console.error('Network or server error:', err);
      setError('Network or server error. Please try again later.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-lg p-8 max-w-md w-full text-center border border-gray-200">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Login</h1>
        {error && <p className="text-red-600 mb-4">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="identifier" className="block text-left text-gray-700 mb-2">Username</label>
            <input
              type="text"
              id="identifier"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div className="mb-6">
            <label htmlFor="password" className="block text-left text-gray-700 mb-2">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-md"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;