import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../config/api';
import type { LoginRequestDTO, LoginResponseDTO, User, UserRole } from '../types/auth';

interface LoginProps {
  onLoginSuccess: (user: User) => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
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
        identifier,
        password,
      };

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });


      const data: LoginResponseDTO = await response.json();

      if (response.ok && data.success) {
        const userRole: UserRole = data.data.user.role;
        const userDataFromResponse = data.data.user;

        const frontendUser: User = {
          id: userDataFromResponse.id.toString(),
          username: userDataFromResponse.username,
          email: userDataFromResponse.email,
          role: userDataFromResponse.role,
        };

        localStorage.setItem('user', JSON.stringify(frontendUser));
        localStorage.setItem('accessToken', data.data.access_token);

        onLoginSuccess(frontendUser);

        if (userRole === 'admin') {
          navigate('/admin/dashboard');
        } else if (userRole === 'common') {
          navigate('/generate'); // <--- ALTERADO AQUI
        } else {
          // Idealmente, isso não deveria acontecer se os roles forem bem definidos.
          // Poderia redirecionar para login ou uma página de erro.
          navigate('/login'); // Ou '/unauthorized' se tiver uma
        }

      } else {
        let errorMessage = data.message || `Error ${response.status}: ${response.statusText}`;

        if (response.status === 422) {
          if (Array.isArray(data.errors) && data.errors.length > 0) {
             errorMessage = `Validation Error: ${data.errors.map(e => e.msg).join(', ')}`;
          } else {
             errorMessage = 'Validation Error: Please check the provided data.';
          }
        }

        setError(errorMessage);
      }
    } catch (err) {
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