import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../../config/api';
import DocumentTypeSelector from '../../components/DocumentTypeSelector';
import type { DocumentType } from '../../types/documentTypes';

const SelectDocumentType: React.FC = () => {
  const [documentTypes, setDocumentTypes] = useState<DocumentType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();

  const fetchDocumentTypes = async () => {
    try {
      setLoading(true);
      setError(null);

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const page = 1;
      const size = 100;

      const response = await fetch(`${API_BASE_URL}/user/document-types/with-fields?page=${page}&size=${size}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setDocumentTypes(data.data.items);
      } else {
        throw new Error(data.message || 'Failed to fetch document types');
      }
    } catch (err) {
      console.error('Erro ao buscar tipos de documento:', err);
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocumentTypes();
  }, []);

  const handleSelect = (type: DocumentType) => {
    navigate(`/generate/upload/${type.id}`);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Select Your Document Type</h1>
          <p className="text-gray-600 mb-8">
            Choose the type of document you want to generate.
          </p>

          <DocumentTypeSelector
            documentTypes={documentTypes}
            onSelect={handleSelect}
            loading={loading}
            error={error}
          />
        </div>
      </main>
    </div>
  );
};

export default SelectDocumentType;