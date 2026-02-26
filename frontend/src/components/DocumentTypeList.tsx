// src/components/DocumentTypeList.tsx
import React from 'react';
import type { DocumentType } from '../types/documentTypes';

interface DocumentTypeListProps {
  documentTypes: DocumentType[];
  onEdit?: (type: DocumentType) => void;
  onDelete?: (id: number) => void;
  actionsEnabled: boolean;
}

const DocumentTypeList: React.FC<DocumentTypeListProps> = ({
  documentTypes,
  onEdit,
  onDelete,
  actionsEnabled,
}) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200 table-auto">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
            {actionsEnabled && (
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-48">Actions</th>
            )}
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
              {actionsEnabled && (
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium w-48">
                  {onEdit && (
                    <button
                      onClick={() => onEdit(type)}
                      className="text-indigo-600 hover:text-indigo-900 mr-4"
                    >
                      Edit
                    </button>
                  )}
                  {onDelete && (
                    <button
                      onClick={() => onDelete(type.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DocumentTypeList;