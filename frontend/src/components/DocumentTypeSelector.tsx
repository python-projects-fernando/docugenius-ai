import React from 'react';
import type { DocumentType } from '../types/documentTypes';

interface DocumentTypeSelectorProps {
  documentTypes: DocumentType[];
  onSelect: (type: DocumentType) => void;
  loading?: boolean;
  error?: string | null;
}

const DocumentTypeSelector: React.FC<DocumentTypeSelectorProps> = ({
  documentTypes,
  onSelect,
  loading = false,
  error = null,
}) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="ml-4 text-gray-600">Loading document types...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 text-red-700 rounded-lg">
        Error: {error}
      </div>
    );
  }

  if (documentTypes.length === 0) {
    return (
      <div className="p-4 text-gray-500 italic">
        No document types available.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {documentTypes.map((type) => (
        <div
          key={type.id}
          onClick={() => onSelect(type)}
          className="cursor-pointer bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200 ease-in-out"
        >
          <h3 className="font-medium text-gray-900 truncate">{type.name}</h3>
          <p className="text-sm text-gray-500 mt-1 truncate" title={type.description}>
            {type.description}
          </p>
          <div className="mt-2 text-xs text-gray-400">
            ID: {type.id}
          </div>
        </div>
      ))}
    </div>
  );
};

export default DocumentTypeSelector;