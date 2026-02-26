import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { API_BASE_URL } from '../../config/api';
import Modal from '../../components/Modal';
import type {
  CreateDocumentTypeRequest,
  SingleDocumentTypeResponse,
  SuggestDocumentTypesRequest,
  SuggestDocumentTypesResponse,
  SuggestedDocumentType,
} from '../../types/documentTypes';

const CreateDocumentType: React.FC = () => {
  const [formData, setFormData] = useState<CreateDocumentTypeRequest>({ name: '', description: '' });
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [businessDescription, setBusinessDescription] = useState<string>('');
  const [suggestedTypes, setSuggestedTypes] = useState<SuggestedDocumentType[]>([]);
  const [loadingSuggestion, setLoadingSuggestion] = useState<boolean>(false);
  const [errorSuggestion, setErrorSuggestion] = useState<string | null>(null);

  const navigate = useNavigate();

  const [modalState, setModalState] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    type: 'success' | 'error';
    onConfirm?: (() => void) | null;
  }>({
    isOpen: false,
    title: '',
    message: '',
    type: 'success',
    onConfirm: null,
  });

  const openSuccessModal = (message: string, onConfirm?: () => void) => {
    setModalState({
      isOpen: true,
      title: 'Success',
      message: message,
      type: 'success',
      onConfirm: onConfirm,
    });
  };

  const openErrorModal = (message: string) => {
    setModalState({
      isOpen: true,
      title: 'Error',
      message: message,
      type: 'error',
    });
  };

  const closeModal = () => {
    if (modalState.onConfirm) {
      modalState.onConfirm();
    }
    setModalState(prev => ({ ...prev, isOpen: false }));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/admin/document-types/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data: SingleDocumentTypeResponse = await response.json();

      if (response.ok && data.success) {
        openSuccessModal(
          data.message || 'Document type created successfully!',
          () => navigate('/admin/document-types')
        );
      } else {
        throw new Error(data.message || `HTTP error! Status: ${response.status}`);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      openErrorModal(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingSuggestion(true);
    setErrorSuggestion(null);
    setSuggestedTypes([]);

    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const requestPayload: SuggestDocumentTypesRequest = {
        business_description: businessDescription,
      };

      const response = await fetch(`${API_BASE_URL}/admin/document-types/suggest`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestPayload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: SuggestDocumentTypesResponse = await response.json();

      if (response.ok && data.success) {
        setSuggestedTypes(data.data.suggested_document_types);
      } else {
        throw new Error(data.message || 'Failed to get suggestions.');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setErrorSuggestion(errorMessage);
      openErrorModal(errorMessage);
    } finally {
      setLoadingSuggestion(false);
    }
  };

  const saveSuggestedType = async (suggestedType: SuggestedDocumentType) => {
    setLoading(true);
    setError(null);

    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/admin/document-types/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(suggestedType),
      });

      const data: SingleDocumentTypeResponse = await response.json();

      if (response.ok && data.success) {
        openSuccessModal(
          data.message || 'Suggested document type saved successfully!',
          () => {
            setSuggestedTypes(prev =>
              prev.filter(
                t =>
                  t.name !== suggestedType.name ||
                  t.description !== suggestedType.description
              )
            );
          }
        );
      } else {
        throw new Error(data.message || `HTTP error! Status: ${response.status}`);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      openErrorModal(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
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
          </>
        }
      >
        <p>{modalState.message}</p>
      </Modal>

      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Create New Document Type</h1>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Manual Creation</h2>
            {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">{error}</div>}
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
              <div className="mb-4">
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                  Name *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="mb-6">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                  Description *
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  required
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <Link
                  to="/admin/document-types"
                  className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
                >
                  Cancel
                </Link>
                <button
                  type="submit"
                  disabled={loading}
                  className={`px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                >
                  {loading ? 'Creating...' : 'Create Type'}
                </button>
              </div>
            </form>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">AI-Powered Document Type Suggestions</h2>
            <form onSubmit={handleSuggest} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
              <div className="mb-4">
                <label htmlFor="businessDescription" className="block text-sm font-medium text-gray-700 mb-1">
                  Business Description *
                </label>
                <textarea
                  id="businessDescription"
                  name="businessDescription"
                  value={businessDescription}
                  onChange={(e) => setBusinessDescription(e.target.value)}
                  required
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Describe the business context for document types suggestion..."
                />
              </div>
              <button
                type="submit"
                disabled={loadingSuggestion}
                className={`px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors ${loadingSuggestion ? 'opacity-70 cursor-not-allowed' : ''}`}
              >
                {loadingSuggestion ? 'Generating...' : 'Generate Suggestions'}
              </button>
            </form>

            {errorSuggestion && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">{errorSuggestion}</div>}

            {suggestedTypes.length > 0 && (
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-gray-900">Suggested Document Types</h3>
                  <button
                    onClick={handleSuggest}
                    disabled={loadingSuggestion}
                    className={`px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-lg transition-colors ${loadingSuggestion ? 'opacity-70 cursor-not-allowed' : ''}`}
                  >
                    Regenerate
                  </button>
                </div>
                <ul className="divide-y divide-gray-200">
                  {suggestedTypes.map((suggested, index) => (
                    <li key={index} className="py-4 flex justify-between items-start">
                      <div>
                        <h4 className="font-medium text-gray-900">{suggested.name}</h4>
                        <p className="text-sm text-gray-500 mt-1">{suggested.description}</p>
                      </div>
                      <button
                        onClick={() => saveSuggestedType(suggested)}
                        disabled={loading}
                        className={`ml-4 px-3 py-1 text-sm bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                      >
                        Save
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default CreateDocumentType;