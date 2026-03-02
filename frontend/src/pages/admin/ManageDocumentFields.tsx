// src/pages/admin/ManageDocumentFields.tsx
import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../../config/api';
import DocumentTypeSelector from '../../components/DocumentTypeSelector';
import type {
  DocumentType,
  ListDocumentTypesResponse,
  ListDocumentFieldsResponse,
  DocumentField,
  CreateDocumentFieldRequest,
  SingleDocumentFieldResponse,
} from '../../types/documentTypes';
import { FIELD_TYPES } from '../../constants/fieldTypes';

const ManageDocumentFields: React.FC = () => {
  const [allDocumentTypes, setAllDocumentTypes] = useState<DocumentType[]>([]);
  const [selectedDocumentType, setSelectedDocumentType] = useState<DocumentType | null>(null);
  const [documentFields, setDocumentFields] = useState<DocumentField[]>([]);
  const [loadingTypes, setLoadingTypes] = useState<boolean>(true);
  const [loadingFields, setLoadingFields] = useState<boolean>(false);
  const [errorTypes, setErrorTypes] = useState<string | null>(null);
  const [errorFields, setErrorFields] = useState<string | null>(null);

  // Estado para os dados do novo campo
    const [newFieldData, setNewFieldData] = useState<Omit<CreateDocumentFieldRequest, 'document_type_id'>>({
      name: '',
      description: '',
      field_type: 'text', // <-- Use o valor padrão do enum
      is_required: false,
    });

  // Estados para controle da edição de campos
  const [editingFieldId, setEditingFieldId] = useState<number | null>(null);
  const [editingFieldData, setEditingFieldData] = useState<Partial<DocumentField>>({});

  // Parâmetros de paginação (exemplo) para a listagem de tipos
  const pageTypes = 1;
  const sizeTypes = 100;

  // Função para buscar todos os tipos de documento
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

      const data:  ListDocumentTypesResponse = await response.json();

      if (data.success) {
        setAllDocumentTypes(data.data.items);
      } else {
        throw new Error(data.message || 'Failed to fetch document types');
      }
    } catch (err) {
      console.error('Erro ao buscar tipos de documento:', err);
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setErrorTypes(errorMessage);
    } finally {
      setLoadingTypes(false);
    }
  };

  // Função para buscar os campos de um tipo de documento específico
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
      console.error('Erro ao buscar campos do documento:', err);
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setErrorFields(errorMessage);
    } finally {
      setLoadingFields(false);
    }
  };

  // Função para adicionar um novo campo
  const addNewField = async () => {
  if (!selectedDocumentType) return; // Certifique-se de que selectedDocumentType existe

  try {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      throw new Error('Access token not found in localStorage.');
    }

    // Prepara os dados para envio, incluindo o ID do tipo de documento selecionado
    // Os campos aqui devem corresponder EXATAMENTE aos nomes esperados pelo backend
    const payload: CreateDocumentFieldRequest = {
      ...newFieldData, // name, description, field_type, is_required
      document_type_id: selectedDocumentType.id, // <-- Certifique-se que este ID está correto
    };

    console.log("Enviando payload:", payload); // Adicione este log para debug

    const response = await fetch(`${API_BASE_URL}/admin/document-fields/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      // Leia o corpo da resposta para obter detalhes do erro
      const errorBody = await response.text(); // ou response.json() se for JSON
      console.error("Erro da API:", errorBody);
      throw new Error(`HTTP error! Status: ${response.status}, Body: ${errorBody}`);
    }

    const data: SingleDocumentFieldResponse = await response.json();

    if (response.ok && data.success) {
      // Atualiza a lista local de campos adicionando o novo campo
      setDocumentFields(prev => [...prev, data.data]);
      // Limpa o formulário
      setNewFieldData({
        name: '',
        description: '',
        field_type: 'text', // <-- Corrigido
        is_required: false,  // <-- Corrigido
      });
      alert(data.message || 'Field added successfully!');
    } else {
      // A API retornou success: false
      throw new Error(data.message || 'API returned success: false');
    }
  } catch (err) {
    console.error('Erro ao adicionar campo:', err);
    alert(err instanceof Error ? err.message : 'An unknown error occurred while adding the field.');
  }
};

  // Handler para alterações no formulário de novo campo
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
      setNewFieldData(prev => ({ ...prev, [name]: val })); // val é booleano para checkbox
      break;
    default:
      console.warn(`Campo desconhecido: ${name}`);
  }
};

  // Handler para submeter o formulário de novo campo
  const handleSubmitNewField = (e: React.FormEvent) => {
    e.preventDefault();
    addNewField(); // Chama a função que faz a lógica de API
  };

  // Função para iniciar a edição de um campo
  const startEditing = (field: DocumentField) => {
  setEditingFieldId(field.id);
  setEditingFieldData({
    name: field.name,
    description: field.description,
    field_type: field.field_type, // <-- Corrigido
    is_required: field.is_required, // <-- Corrigido
   });
  };

  // Handler para alterações no formulário de edição
  const handleChangeEditingField = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
  const { name, value, type } = e.target;
  const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;

  switch (name) {
    case 'name':
    case 'description':
    case 'field_type': // <-- Adicionado
      setEditingFieldData(prev => ({ ...prev, [name]: value }));
      break;
    case 'is_required': // <-- Adicionado
      setEditingFieldData(prev => ({ ...prev, [name]: val })); // val é booleano para checkbox
      break;
    default:
      console.warn(`Campo desconhecido: ${name}`);
   }
  };

  // Handler para submeter a edição
  const submitEditingField = async (e: React.FormEvent, fieldId: number) => {
    e.preventDefault();
    if (!selectedDocumentType) return;

    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      // Chamada PATCH para atualizar o campo
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

      const data:  SingleDocumentFieldResponse = await response.json();

      if (response.ok && data.success) {
        // Atualiza a lista local de campos com os dados editados
        setDocumentFields(prev =>
          prev.map(f => f.id === fieldId ? { ...f, ...editingFieldData } : f)
        );
        setEditingFieldId(null);
        setEditingFieldData({});
        alert(data.message || 'Field updated successfully!');
      } else {
        throw new Error(data.message || `HTTP error! Status: ${response.status}`);
      }
    } catch (err) {
      console.error('Erro ao atualizar campo:', err);
      alert(err instanceof Error ? err.message : 'An unknown error occurred while updating the field.');
    }
  };

  // Função para cancelar a edição
  const cancelEditing = () => {
    setEditingFieldId(null);
    setEditingFieldData({});
  };

  // Busca os tipos ao montar o componente
  useEffect(() => {
    fetchAllDocumentTypes();
  }, []);

  // Busca os campos sempre que selectedDocumentType mudar
  useEffect(() => {
    if (selectedDocumentType) {
      fetchDocumentFields(selectedDocumentType.id);
    } else {
      // Limpa campos ao sair do modo de edição
      setDocumentFields([]);
    }
  }, [selectedDocumentType]);

  // Função chamada quando um tipo é selecionado no selector
  const handleSelectDocumentType = (type: DocumentType) => {
    setSelectedDocumentType(type);
  };

  // Função para voltar à lista de seleção
  const handleBackToList = () => {
    setSelectedDocumentType(null);
  };

  // Renderiza o modo Lista ou o modo Campos
  if (selectedDocumentType) {
    // Modo Campos
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col">
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
                    ? "Below are the existing fields. You can edit them or add new ones."
                    : "No fields found for this document type. Add new fields below."}
                </p>

                {/* Lista de Campos Existentes com Edição Inline */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">Existing Fields</h2>
                  {documentFields.length === 0 ? (
                    <p className="text-gray-500 italic">No fields configured yet.</p>
                  ) : (
                    <ul className="divide-y divide-gray-200">
                      {documentFields.map(field => (
                        <li key={field.id} className="py-3">
                          {/* Renderiza o formulário de edição se este campo estiver em edição */}
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
                                    value={editingFieldData.field_type ?? 'TEXT'} // Valor padrão
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
                                name="is_required" // <-- Corrigido
                                type="checkbox"
                                checked={!!editingFieldData.is_required} // <-- Corrigido
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
                                </div>
                              </form>
                            </div>
                          ) : (
                            // Renderiza os dados normais do campo e o botão de editar
                            <div>
                              <div className="flex justify-between items-start">
                                <div>
                                  <div className="font-medium text-gray-900">{field.name}</div>
                                  <div className="text-sm text-gray-500">{field.description}</div>
                                  <div className="text-xs text-gray-400">
                                    Type: {field.field_type} | Required: {field.is_required ? 'Yes' : 'No'} | ID: {field.id}
                                  </div>
                                </div>
                                <button
                                  onClick={() => startEditing(field)}
                                  className="text-xs px-2 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded"
                                >
                                  Edit
                                </button>
                              </div>
                            </div>
                          )}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>

                {/* Formulário para adicionar novos campos */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
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
                        name="is_required" // <-- Corrigido
                        type="checkbox"
                        checked={newFieldData.is_required} // <-- Corrigido
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
              </div>
            )}
          </div>
        </main>
      </div>
    );
  }

  // Modo Lista
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