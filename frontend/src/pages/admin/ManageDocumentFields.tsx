import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../../config/api';
import DocumentTypeSelector from '../../components/DocumentTypeSelector';
import Modal from '../../components/Modal';
import { FIELD_TYPES } from '../../constants/fieldTypes';
import type {
  DocumentType,
  ListDocumentTypesResponse,
  ListDocumentFieldsResponse,
  DocumentField,
  CreateDocumentFieldRequest,
  SingleDocumentFieldResponse,
  DeleteDocumentFieldResponse,
  SuggestDocumentFieldsRequest,
  SuggestedField,
  SuggestDocumentFieldsResponse,
} from '../../types/documentTypes';

const ManageDocumentFields: React.FC = () => {
  const [allDocumentTypes, setAllDocumentTypes] = useState<DocumentType[]>([]);
  const [selectedDocumentType, setSelectedDocumentType] = useState<DocumentType | null>(null);
  const [documentFields, setDocumentFields] = useState<DocumentField[]>([]);
  const [loadingTypes, setLoadingTypes] = useState<boolean>(true);
  const [loadingFields, setLoadingFields] = useState<boolean>(false);
  const [errorTypes, setErrorTypes] = useState<string | null>(null);
  const [errorFields, setErrorFields] = useState<string | null>(null);

  const [newFieldData, setNewFieldData] = useState<Omit<CreateDocumentFieldRequest, 'document_type_id'>>({
    name: '',
    description: '',
    field_type: 'text',
    is_required: false,
  });

  const [editingFieldId, setEditingFieldId] = useState<number | null>(null);
  const [editingFieldData, setEditingFieldData] = useState<Partial<DocumentField>>({});

  const [suggestedFields, setSuggestedFields] = useState<SuggestedField[]>([]);
  const [loadingSuggestion, setLoadingSuggestion] = useState<boolean>(false);
  const [errorSuggestion, setErrorSuggestion] = useState<string | null>(null);

  const [modalState, setModalState] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    type: 'success' | 'error' | 'confirm';
    onConfirm?: (() => void) | null;
  }>({
    isOpen: false,
    title: '',
    message: '',
    type: 'success',
    onConfirm: null,
  });

  const pageTypes = 1;
  const sizeTypes = 100;

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

  const openConfirmModal = (message: string, onConfirm: () => void) => {
    setModalState({
      isOpen: true,
      title: 'Confirm Action',
      message: message,
      type: 'confirm',
      onConfirm: onConfirm,
    });
  };

  const closeModal = () => {
    if (modalState.onConfirm) {
      modalState.onConfirm();
    }
    setModalState(prev => ({ ...prev, isOpen: false }));
  };

  const handleConfirm = () => {
    if (modalState.onConfirm) {
      modalState.onConfirm();
    }
    closeModal();
  };

  const fetchAllDocumentTypes = async () => {
    try {
      setLoadingTypes(true);
      setErrorTypes(null);

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/user/document-types/?page=${pageTypes}&size=${sizeTypes}`, {
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
        setAllDocumentTypes(data.data.items);
      } else {
        throw new Error(data.message || 'Failed to fetch document types');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setErrorTypes(errorMessage);
    } finally {
      setLoadingTypes(false);
    }
  };

  const fetchDocumentFields = async (docTypeId: number) => {
    try {
      setLoadingFields(true);
      setErrorFields(null);

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/admin/document-fields/by-document-type/${docTypeId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: ListDocumentFieldsResponse = await response.json();

      if (data.success) {
        setDocumentFields(data.data.items);
      } else {
        throw new Error(data.message || 'Failed to fetch document fields');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setErrorFields(errorMessage);
    } finally {
      setLoadingFields(false);
    }
  };

  const addNewField = async () => {
    if (!selectedDocumentType) return;

    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const payload: CreateDocumentFieldRequest = {
        ...newFieldData,
        document_type_id: selectedDocumentType.id,
      };

      const response = await fetch(`${API_BASE_URL}/admin/document-fields/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(`HTTP error! Status: ${response.status}, Body: ${errorBody}`);
      }

      const data: SingleDocumentFieldResponse = await response.json();

      if (response.ok && data.success) {
        setDocumentFields(prev => [...prev, data.data]);
        setNewFieldData({
          name: '',
          description: '',
          field_type: 'text',
          is_required: false,
        });
        openSuccessModal(data.message || 'Field added successfully!');
      } else {
        throw new Error(data.message || 'API returned success: false');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred while adding the field.';
      openErrorModal(errorMessage);
    }
  };

  const handleChangeNewField = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;

    switch (name) {
      case 'name':
      case 'description':
      case 'field_type':
        setNewFieldData(prev => ({ ...prev, [name]: value }));
        break;
      case 'is_required':
        setNewFieldData(prev => ({ ...prev, [name]: val }));
        break;
    }
  };

  const handleSubmitNewField = (e: React.FormEvent) => {
    e.preventDefault();
    addNewField();
  };

  const startEditing = (field: DocumentField) => {
    setEditingFieldId(field.id);
    setEditingFieldData({
      name: field.name,
      description: field.description,
      field_type: field.field_type,
      is_required: field.is_required,
    });
  };

  const handleChangeEditingField = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;
    setEditingFieldData(prev => ({ ...prev, [name]: val }));
  };

  const submitEditingField = async (e: React.FormEvent, fieldId: number) => {
    e.preventDefault();
    if (!selectedDocumentType) return;

    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/admin/document-fields/${fieldId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editingFieldData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: SingleDocumentFieldResponse = await response.json();

      if (response.ok && data.success) {
        setDocumentFields(prev =>
          prev.map(f => f.id === fieldId ? { ...f, ...editingFieldData } : f)
        );
        setEditingFieldId(null);
        setEditingFieldData({});
        openSuccessModal(data.message || 'Field updated successfully!');
      } else {
        throw new Error(data.message || `HTTP error! Status: ${response.status}`);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred while updating the field.';
      openErrorModal(errorMessage);
    }
  };

  const cancelEditing = () => {
    setEditingFieldId(null);
    setEditingFieldData({});
  };

  const deleteField = async (fieldId: number) => {
    openConfirmModal(`Are you sure you want to delete the field with ID ${fieldId}?`, async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          throw new Error('Access token not found in localStorage.');
        }

        const response = await fetch(`${API_BASE_URL}/admin/document-fields/${fieldId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data: DeleteDocumentFieldResponse = await response.json();

        if (!data || typeof data.success !== 'boolean') {
          throw new Error('Invalid response from server.');
        }

        if (data.success) {
          setDocumentFields(prev => prev.filter(f => f.id !== fieldId));
          closeModal();
        } else {
          throw new Error(data.message || 'Failed to delete document field.');
        }
      } catch (err) {
        setModalState(prev => ({
          ...prev,
          title: 'Error',
          message: err instanceof Error ? err.message : 'An unknown error occurred.',
          type: 'error',
          onConfirm: undefined,
        }));
      }
    });
  };

  const handleSuggestFields = async () => {
    if (!selectedDocumentType) return;

    try {
      setLoadingSuggestion(true);
      setErrorSuggestion(null);
      setSuggestedFields([]);

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const requestPayload: SuggestDocumentFieldsRequest = {
        document_type_name: selectedDocumentType.name,
        document_type_description: selectedDocumentType.description,
      };

      const response = await fetch(`${API_BASE_URL}/admin/document-fields/suggest`, {
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

      const data: SuggestDocumentFieldsResponse = await response.json();

      if (response.ok && data.success) {
        setSuggestedFields(data.data.fields);
      } else {
        throw new Error(data.message || 'Failed to get field suggestions.');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setErrorSuggestion(errorMessage);
      openErrorModal(errorMessage);
    } finally {
      setLoadingSuggestion(false);
    }
  };

  const saveSuggestedField = async (suggestedField: SuggestedField) => {
    if (!selectedDocumentType) return;

    try {
      setLoadingFields(true);
      setErrorFields(null);

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const payload: CreateDocumentFieldRequest = {
        name: suggestedField.name,
        description: suggestedField.description,
        field_type: suggestedField.type,
        is_required: suggestedField.required,
        document_type_id: selectedDocumentType.id,
      };

      const response = await fetch(`${API_BASE_URL}/admin/document-fields/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(`HTTP error! Status: ${response.status}, Body: ${errorBody}`);
      }

      const data: SingleDocumentFieldResponse = await response.json();

      if (response.ok && data.success) {
        setDocumentFields(prev => [...prev, data.data]);
        setSuggestedFields(prev => prev.filter(f => f.name !== suggestedField.name || f.description !== suggestedField.description));
        openSuccessModal(data.message || 'Suggested field saved successfully!');
      } else {
        throw new Error(data.message || 'API returned success: false while saving suggested field.');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred while saving the suggested field.';
      setErrorFields(errorMessage);
      openErrorModal(errorMessage);
    } finally {
      setLoadingFields(false);
    }
  };

  useEffect(() => {
    fetchAllDocumentTypes();
  }, []);

  useEffect(() => {
    setSuggestedFields([]);
    setErrorSuggestion(null);

    if (selectedDocumentType) {
      fetchDocumentFields(selectedDocumentType.id);
    } else {
      setDocumentFields([]);
    }
  }, [selectedDocumentType]);

  const handleSelectDocumentType = (type: DocumentType) => {
    setSelectedDocumentType(type);
  };

  const handleBackToList = () => {
    setSelectedDocumentType(null);
  };

  if (selectedDocumentType) {
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
              <h1 className="text-3xl font-bold text-gray-900">Manage Fields for: {selectedDocumentType.name}</h1>
              <button
                onClick={handleBackToList}
                className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
              >
                Back to List
              </button>
            </div>

            {loadingFields && (
              <div className="flex items-center justify-center p-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                <p className="ml-4 text-gray-600">Loading fields for {selectedDocumentType.name}...</p>
              </div>
            )}

            {errorFields && (
              <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
                Error loading fields: {errorFields}
              </div>
            )}

            {!loadingFields && !errorFields && (
              <div>
                <p className="text-gray-600 mb-4">Document Type ID: {selectedDocumentType.id}</p>
                <p className="text-gray-500 mb-6">
                  {documentFields.length > 0
                    ? "Below are the existing fields. You can new ones."
                    : "No fields found for this document type. Add new fields below."}
                </p>

                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">Existing Fields</h2>
                  {documentFields.length === 0 ? (
                    <p className="text-gray-500 italic">No fields configured yet.</p>
                  ) : (
                    <ul className="divide-y divide-gray-200">
                      {documentFields.map(field => (
                        <li key={field.id} className="py-3">
                          {editingFieldId === field.id ? (
                            <div className="border-l-4 border-blue-500 pl-4 py-2">
                              <form onSubmit={(e) => submitEditingField(e, field.id)} className="space-y-2">
                                <div>
                                  <label htmlFor={`editName_${field.id}`} className="block text-xs font-medium text-gray-700 mb-1">
                                    Name *
                                  </label>
                                  <input
                                    type="text"
                                    id={`editName_${field.id}`}
                                    name="name"
                                    value={editingFieldData.name ?? ''}
                                    onChange={handleChangeEditingField}
                                    required
                                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                                  />
                                </div>
                                <div>
                                  <label htmlFor={`editDescription_${field.id}`} className="block text-xs font-medium text-gray-700 mb-1">
                                    Description
                                  </label>
                                  <textarea
                                    id={`editDescription_${field.id}`}
                                    name="description"
                                    value={editingFieldData.description ?? ''}
                                    onChange={handleChangeEditingField}
                                    rows={2}
                                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                                  />
                                </div>
                                <div>
                                  <label htmlFor={`editType_${field.id}`} className="block text-xs font-medium text-gray-700 mb-1">
                                    Type *
                                  </label>
                                  <select
                                    id={`editType_${field.id}`}
                                    name="field_type"
                                    value={editingFieldData.field_type ?? 'text'}
                                    onChange={handleChangeEditingField}
                                    required
                                    className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                                  >
                                    {FIELD_TYPES.map(type => (
                                      <option key={type.value} value={type.value}>
                                        {type.label}
                                      </option>
                                    ))}
                                  </select>
                                </div>
                                <div className="flex items-center text-sm">
                                  <input
                                    id={`editRequired_${field.id}`}
                                    name="is_required"
                                    type="checkbox"
                                    checked={!!editingFieldData.is_required}
                                    onChange={handleChangeEditingField}
                                    className="h-3 w-3 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                  />
                                  <label htmlFor={`editRequired_${field.id}`} className="ml-1 text-gray-700">
                                    Required
                                  </label>
                                </div>
                                <div className="flex space-x-2 pt-1">
                                  <button
                                    type="submit"
                                    className="text-xs px-2 py-1 bg-green-600 hover:bg-green-700 text-white rounded"
                                  >
                                    Save
                                  </button>
                                  <button
                                    type="button"
                                    onClick={cancelEditing}
                                    className="text-xs px-2 py-1 bg-gray-500 hover:bg-gray-600 text-white rounded"
                                  >
                                    Cancel
                                  </button>
                                  <button
                                    type="button"
                                    onClick={() => deleteField(field.id)}
                                    className="text-xs px-2 py-1 bg-red-100 hover:bg-red-200 text-red-800 rounded"
                                  >
                                    Delete
                                  </button>
                                </div>
                              </form>
                            </div>
                          ) : (
                            <div>
                              <div className="flex justify-between items-start">
                                <div>
                                  <div className="font-medium text-gray-900">{field.name}</div>
                                  <div className="text-sm text-gray-500">{field.description}</div>
                                  <div className="text-xs text-gray-400">
                                    Type: {field.field_type} | Required: {field.is_required ? 'Yes' : 'No'} | ID: {field.id}
                                  </div>
                                </div>
                                <div className="flex space-x-2">
                                  <button
                                    onClick={() => startEditing(field)}
                                    className="text-xs px-2 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded"
                                  >
                                    Edit
                                  </button>
                                  <button
                                    onClick={() => deleteField(field.id)}
                                    className="text-xs px-2 py-1 bg-red-100 hover:bg-red-200 text-red-800 rounded"
                                  >
                                    Delete
                                  </button>
                                </div>
                              </div>
                            </div>
                          )}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">Add New Field</h2>
                  <p className="text-gray-500 mb-4">Enter details for the new field.</p>

                  <form onSubmit={handleSubmitNewField} className="space-y-4">
                    <div>
                      <label htmlFor="newFieldName" className="block text-sm font-medium text-gray-700 mb-1">
                        Name *
                      </label>
                      <input
                        type="text"
                        id="newFieldName"
                        name="name"
                        value={newFieldData.name}
                        onChange={handleChangeNewField}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label htmlFor="newFieldDescription" className="block text-sm font-medium text-gray-700 mb-1">
                        Description
                      </label>
                      <textarea
                        id="newFieldDescription"
                        name="description"
                        value={newFieldData.description}
                        onChange={handleChangeNewField}
                        rows={2}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    <div>
                      <label htmlFor="newFieldType" className="block text-sm font-medium text-gray-700 mb-1">
                        Type *
                      </label>
                      <select
                        id="newFieldType"
                        name="field_type"
                        value={newFieldData.field_type}
                        onChange={handleChangeNewField}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        {FIELD_TYPES.map(type => (
                          <option key={type.value} value={type.value}>
                            {type.label}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="flex items-center">
                      <input
                        id="newFieldIsRequired"
                        name="is_required"
                        type="checkbox"
                        checked={newFieldData.is_required}
                        onChange={handleChangeNewField}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label htmlFor="newFieldIsRequired" className="ml-2 block text-sm text-gray-700">
                        Required
                      </label>
                    </div>
                    <div className="flex justify-end pt-4">
                      <button
                        type="submit"
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
                      >
                        Add Field
                      </button>
                    </div>
                  </form>
                </div>

                <div className="mb-8">
                  <h2 className="text-xl font-semibold text-gray-800 mb-4">AI-Powered Field Suggestions</h2>
                  <button
                    onClick={handleSuggestFields}
                    disabled={loadingSuggestion}
                    className={`px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors ${loadingSuggestion ? 'opacity-70 cursor-not-allowed' : ''}`}
                  >
                    {loadingSuggestion ? 'Generating...' : 'Generate Field Suggestions'}
                  </button>

                  {errorSuggestion && (
                    <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
                      {errorSuggestion}
                    </div>
                  )}

                  {suggestedFields.length > 0 && (
                    <div className="mt-6 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                      <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-medium text-gray-900">Suggested Fields</h3>
                        <button
                          onClick={handleSuggestFields}
                          disabled={loadingSuggestion}
                          className={`px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-lg transition-colors ${loadingSuggestion ? 'opacity-70 cursor-not-allowed' : ''}`}
                        >
                          Regenerate
                        </button>
                      </div>
                      <ul className="divide-y divide-gray-200">
                        {suggestedFields.map((suggested, index) => (
                          <li key={index} className="py-4 flex justify-between items-start">
                            <div>
                              <h4 className="font-medium text-gray-900">{suggested.name}</h4>
                              <p className="text-sm text-gray-500 mt-1">{suggested.description}</p>
                              <p className="text-xs text-gray-400 mt-1">
                                Type: {suggested.type} | Required: {suggested.required ? 'Yes' : 'No'}
                              </p>
                            </div>
                            <button
                              onClick={() => saveSuggestedField(suggested)}
                              disabled={loadingFields}
                              className={`ml-4 px-3 py-1 text-sm bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors ${loadingFields ? 'opacity-70 cursor-not-allowed' : ''}`}
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
            )}
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Select Document Type to Manage Fields</h1>
          <DocumentTypeSelector
            documentTypes={allDocumentTypes}
            onSelect={handleSelectDocumentType}
            loading={loadingTypes}
            error={errorTypes}
          />
        </div>
      </main>
    </div>
  );
};

export default ManageDocumentFields;