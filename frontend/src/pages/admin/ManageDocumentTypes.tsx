// src/pages/admin/ManageDocumentTypes.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { API_BASE_URL } from '../../config/api';
import type { DocumentType, ListDocumentTypesResponse, DeleteDocumentTypeResponse } from '../../types/documentTypes';

const ManageDocumentTypes: React.FC = () => {
  const [documentTypes, setDocumentTypes] = useState<DocumentType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Parâmetros de paginação (exemplo)
  const page = 1;
  const size = 100;

  // Função para buscar os tipos de documento
  const fetchDocumentTypes = async () => {
    try {
      setLoading(true);
      setError(null);

      // Lê o token de acesso do localStorage
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/user/document-types/?page=${page}&size=${size}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data:  ListDocumentTypesResponse = await response.json();

      if (data.success) {
        setDocumentTypes(data.data.items);
      } else {
        // Se a API retornar success: false, tenta pegar a mensagem de erro
        throw new Error(data.message || 'Failed to fetch document types');
      }
    } catch (err) {
      console.error('Erro ao buscar tipos de documento:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  // Função para deletar um tipo de documento
  const deleteDocumentType = async (id: number) => {
    if (!window.confirm(`Are you sure you want to delete the document type with ID ${id}?`)) {
      return; // Sai da função se o usuário cancelar
    }

    try {
      // Lê o token de acesso do localStorage
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/admin/document-types/${id}`, { // Note o ID na URL
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data:  DeleteDocumentTypeResponse = await response.json();

      if (data.success) {
        console.log('Deletion response:', data); // Log para ver a resposta real
        alert(data.message); // Mostra a mensagem de sucesso da API
        // Atualiza a lista removendo o item deletado
        setDocumentTypes(prevTypes => prevTypes.filter(type => type.id !== id));
      } else {
        // Se a API retornar success: false, tenta pegar a mensagem de erro
        throw new Error(data.message || 'Failed to delete document type');
      }
    } catch (err) {
      console.error('Erro ao deletar tipo de documento:', err);
      alert(err instanceof Error ? err.message : 'An unknown error occurred during deletion.');
    }
  };

  // Busca os dados ao montar o componente
  useEffect(() => {
    fetchDocumentTypes();
  }, [page, size]); // Dependências: refaz a busca se page ou size mudar

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <main className="flex-grow container mx-auto px-4 py-8 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading document types...</p>
          </div>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <main className="flex-grow container mx-auto px-4 py-8 flex items-center justify-center">
          <div className="text-center">
            <p className="text-red-600">Error: {error}</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Manage Document Types</h1>
            {/* Link para adicionar um novo tipo de documento */}
            <Link to="/admin/document-types/new">
              <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors shadow-sm">
                Add New Type
              </button>
            </Link>
          </div>

          {/* Tabela ou Grid para listar os tipos de documentos */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200 table-auto">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-48">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {documentTypes.map((type) => (
                  <tr key={type.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{type.id}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{type.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div
                        className="text-sm text-gray-500 truncate"
                        style={{ maxWidth: '200px' }}
                        title={type.description}
                      >
                        {type.description}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium w-48">
                      {/* Links para editar e excluir */}
                      <Link to={`/admin/document-types/${type.id}/edit`} className="text-indigo-600 hover:text-indigo-900 mr-4">
                        Edit
                      </Link>
                      <button
                        onClick={() => deleteDocumentType(type.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ManageDocumentTypes;