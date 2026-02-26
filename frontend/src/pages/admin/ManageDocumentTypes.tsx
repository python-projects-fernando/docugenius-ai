// src/pages/admin/ManageDocumentTypes.tsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../../config/api';
import Modal from '../../components/Modal'; // Importe o componente Modal
import type { DocumentType, ListDocumentTypesResponse, DeleteDocumentTypeResponse } from '../../types/documentTypes';

const ManageDocumentTypes: React.FC = () => {
  const navigate = useNavigate();
  const [documentTypes, setDocumentTypes] = useState<DocumentType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Estados para controlar as modais
  const [modalState, setModalState] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    type: 'success' | 'error' | 'confirm'; // Tipos de modal
    onConfirm?: (() => void) | null; // Callback para ação de confirmação
  }>({
    isOpen: false,
    title: '',
    message: '',
    type: 'success',
    onConfirm: null,
  });

  // Parâmetros de paginação (exemplo)
  const page = 1;
  const size = 100;

  // Função para abrir a modal de sucesso (com callback opcional)
  const openSuccessModal = (message: string, onConfirm?: () => void) => {
    setModalState({
      isOpen: true,
      title: 'Success',
      message: message,
      type: 'success',
      onConfirm: onConfirm,
    });
  };

  // Função para abrir a modal de erro
  const openErrorModal = (message: string) => {
    setModalState({
      isOpen: true,
      title: 'Error',
      message: message,
      type: 'error',
    });
  };

  // Função para abrir a modal de confirmação
  const openConfirmModal = (message: string, onConfirm: () => void) => {
    setModalState({
      isOpen: true,
      title: 'Confirm Action',
      message: message,
      type: 'confirm',
      onConfirm: onConfirm, // Armazena a função de confirmação
    });
  };

    // Função para fechar a modal
  const closeModal = () => {
    setModalState(prev => ({ ...prev, isOpen: false }));
  };

  // Função para lidar com a confirmação na modal
  const handleConfirm = () => {
    if (modalState.onConfirm) {
      modalState.onConfirm(); // Chama a função de confirmação passada
    }
    closeModal(); // Fecha a modal após confirmar
  };

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

      const data: ListDocumentTypesResponse = await response.json();

      if (data.success) {
        setDocumentTypes(data.data.items);
      } else {
        // Se a API retornar success: false, tenta pegar a mensagem de erro
        throw new Error(data.message || 'Failed to fetch document types');
      }
    } catch (err) {
      console.error('Erro ao buscar tipos de documento:', err);
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage); // Mostra erro na página
      // openErrorModal(errorMessage); // Opcional: mostrar erro em modal também
    } finally {
      setLoading(false);
    }
  };

    // Função para deletar um tipo de documento
  const deleteDocumentType = async (id: number) => {
    // Abre a modal de confirmação
    openConfirmModal(`Are you sure you want to delete the document type with ID ${id}?`, async () => {
      try {
        // Lê o token de acesso do localStorage
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found in localStorage.');
        }

        const response = await fetch(`${API_BASE_URL}/admin/document-types/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data: DeleteDocumentTypeResponse = await response.json();

        // Validação básica da resposta
        if (!data || typeof data.success !== 'boolean') {
          throw new Error('Invalid response from server.');
        }

        if (data.success) {
          console.log('Deletion successful:', data);
          // ✅ Sucesso: remove o item da lista e fecha a modal
          setDocumentTypes(prevTypes => prevTypes.filter(type => type.id !== id));
          closeModal(); // Fecha a modal de confirmação imediatamente
        } else {
          // ❌ Falha: mostra erro na modal de confirmação (ou em uma nova modal de erro, se preferir)
          throw new Error(data.message || 'Failed to delete document type.');
        }
      } catch (err) {
        console.error('Erro ao deletar tipo de documento:', err);
        // Mostra o erro na própria modal de confirmação (substituindo a mensagem)
        setModalState(prev => ({
          ...prev,
          title: 'Error',
          message: err instanceof Error ? err.message : 'An unknown error occurred.',
          type: 'error',
          onConfirm: undefined, // Remove o callback de confirmação
        }));
        // Ou, se preferir uma modal separada de erro, use: openErrorModal(...)
      }
    });
  };

  // Busca os dados ao montar o componente
  useEffect(() => {
    fetchDocumentTypes();
  }, [page, size]);

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
            {/* Renderiza a Modal */}
      <Modal
        isOpen={modalState.isOpen}
        onClose={closeModal}
        title={modalState.title}
        footer={
          <>
            {modalState.type === 'success' && (
              <button
                onClick={closeModal}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
              >
                OK
              </button>
            )}
            {modalState.type === 'error' && (
              <button
                onClick={closeModal}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors"
              >
                Close
              </button>
            )}
            {modalState.type === 'confirm' && (
              <div className="flex justify-end space-x-3">
                <button
                  onClick={closeModal}
                  className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleConfirm}
                  className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors"
                >
                  Confirm
                </button>
              </div>
            )}
          </>
        }
      >
        <p>{modalState.message}</p>
      </Modal>

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
                      <button
                          onClick={() => navigate(`/admin/document-types/${type.id}/edit`, { state: { documentType: type } })}
                          className="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          Edit
                      </button>
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