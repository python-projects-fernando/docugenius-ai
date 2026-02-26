import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation, Link } from 'react-router-dom';
import { API_BASE_URL } from '../../config/api';
import Modal from '../../components/Modal';
import type { DocumentType, SingleDocumentTypeResponse } from '../../types/documentTypes';

const EditDocumentType: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  const [formData, setFormData] = useState<DocumentType | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

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

  useEffect(() => {
    const locationState = location.state as { documentType?: DocumentType } | null;

    if (locationState?.documentType) {
      setFormData(locationState.documentType);
      setLoading(false);
      return;
    }

    const fetchFromBackend = async () => {
      try {
        setLoading(true);
        setError(null);

        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found in localStorage.');
        }

        const response = await fetch(`${API_BASE_URL}/user/document-types/${id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data: SingleDocumentTypeResponse = await response.json();

        if (data.success) {
          setFormData(data.data);
        } else {
          throw new Error(data.message || 'Failed to fetch document type');
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
        setError(errorMessage);
        openErrorModal(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchFromBackend();
    } else {
      setError('Document type ID not provided.');
      setLoading(false);
    }
  }, [id, location.state]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    if (formData) {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData) return;

    try {
      setLoading(true);
      setError(null);

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/admin/document-types/${formData.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: formData.name, description: formData.description }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: SingleDocumentTypeResponse = await response.json();

      if (data.success) {
        openSuccessModal(
          data.message || 'Document type updated successfully!',
          () => navigate('/admin/document-types')
        );
      } else {
        throw new Error(data.message || 'Failed to update document type.');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      openErrorModal(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !formData) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <main className="flex-grow container mx-auto px-4 py-8 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading document type...</p>
          </div>
        </main>
      </div>
    );
  }

  if (error && !formData) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <main className="flex-grow container mx-auto px-4 py-8 flex items-center justify-center">
          <div className="text-center">
            <p className="text-red-600">Error: {error}</p>
            <Link to="/admin/document-types" className="mt-4 inline-block text-blue-600 hover:text-blue-800">
              Back to List
            </Link>
          </div>
        </main>
      </div>
    );
  }

  if (!formData) return null;

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
          <h1 className="text-3xl font-bold text-gray-900 mb-6">
            Edit Document Type - ID: {formData.id}
          </h1>

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
            <div className="flex justify-between">
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
                {loading ? 'Updating...' : 'Update Type'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default EditDocumentType;