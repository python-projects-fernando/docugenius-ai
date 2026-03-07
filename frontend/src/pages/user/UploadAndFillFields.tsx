// src/pages/user/UploadAndFillFields.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../../config/api';
import type {
  DocumentField,
  DocumentType,
  GenerateDocumentRequest, // Importe do documentTypes.ts
  GenerateDocumentResponse // Importe do documentTypes.ts
} from '../../types/documentTypes';

const UploadAndFillFields: React.FC = () => {
  const { documentTypeId } = useParams<{ documentTypeId: string }>();
  const navigate = useNavigate();

  const [documentType, setDocumentType] = useState<DocumentType | null>(null);
  const [fields, setFields] = useState<DocumentField[]>([]);
  const [filledFields, setFilledFields] = useState<Record<string, any>>({});
  const [loadingFields, setLoadingFields] = useState<boolean>(true);
  const [loadingGeneration, setLoadingGeneration] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null); // URL para download
  const [generationMessage, setGenerationMessage] = useState<string>(''); // Mensagem de sucesso

  // Converter documentTypeId string para número
  const typeIdNumber = parseInt(documentTypeId || '', 10);

  if (isNaN(typeIdNumber)) {
    setError('Invalid document type ID provided in the URL.');
    return <div>Error: {error}</div>;
  }

  // Função para buscar os campos do tipo de documento
  const fetchFields = async () => {
    try {
      setLoadingFields(true);
      setError(null);

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      const response = await fetch(`${API_BASE_URL}/user/document-fields/by-document-type/${typeIdNumber}`, {
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
        setFields(data.data.items);
        // Inicializa filledFields com valores vazios ou padrão se necessário
        const initialFilledFields: Record<string, any> = {};
        data.data.items.forEach((field: DocumentField) => {
          // Pode-se inicializar com valores padrão aqui se necessário
          initialFilledFields[field.name] = '';
        });
        setFilledFields(initialFilledFields);
      } else {
        throw new Error(data.message || 'Failed to fetch document fields');
      }
    } catch (err) {
      console.error('Error fetching document fields:', err); // Corrigido
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
    } finally {
      setLoadingFields(false);
    }
  };

  // Busca os campos quando o componente monta e o ID muda
  useEffect(() => {
    fetchFields();
  }, [typeIdNumber]); // Adicionando typeIdNumber como dependência

  // Handler para alterações nos campos do formulário
  const handleFieldChange = (fieldName: string, value: any) => {
    setFilledFields(prev => ({
      ...prev,
      [fieldName]: value,
    }));
  };

  // Função para renderizar o input correto com base no tipo de campo
  const renderFieldInput = (field: DocumentField) => {
    const currentValue = filledFields[field.name] ?? '';

    // Função auxiliar para lidar com onChange
    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const { value, type } = e.target;
      let processedValue: any = value;

      if (type === 'checkbox') {
        processedValue = (e.target as HTMLInputElement).checked;
      } else if (field.field_type === 'number') {
        processedValue = value === '' ? '' : Number(value); // Mantém string vazia ou converte para número
      } else if (field.field_type === 'date') {
        // Valor já é string no formato YYYY-MM-DD
        processedValue = value;
      }

      handleFieldChange(field.name, processedValue);
    };

    switch (field.field_type) {
      case 'text':
      case 'email':
      case 'number': // Pode usar input text e converter no handler
      case 'date':
        return (
          <input
            type={field.field_type === 'number' ? 'text' : field.field_type} // Usar text para number para permitir string vazia
            id={field.name}
            name={field.name}
            value={currentValue}
            onChange={handleChange}
            required={field.is_required}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );
      case 'textarea':
        return (
          <textarea
            id={field.name}
            name={field.name}
            value={currentValue}
            onChange={handleChange}
            required={field.is_required}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );
      case 'select':
        // Assume que options estão embutidas no field ou são fixas. Pode precisar de adaptação.
        // Por enquanto, input text como placeholder
        console.warn(`Field type 'select' not fully implemented for field '${field.name}'. Using text input.`);
        return (
          <input
            type="text"
            id={field.name}
            name={field.name}
            value={currentValue}
            onChange={handleChange}
            required={field.is_required}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );
      case 'checkbox':
        return (
          <input
            type="checkbox"
            id={field.name}
            name={field.name}
            checked={!!currentValue} // Converte para booleano
            onChange={handleChange}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
        );
      default:
        // Tipo desconhecido
        console.warn(`Unknown field type '${field.field_type}' for field '${field.name}'. Using text input.`);
        return (
          <input
            type="text"
            id={field.name}
            name={field.name}
            value={currentValue}
            onChange={handleChange}
            required={field.is_required}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );
    }
  };

  // Função para validar campos obrigatórios
  const validateForm = (): boolean => {
    for (const field of fields) {
      if (field.is_required) {
        const value = filledFields[field.name];
        // Considera vazio se for string vazia, null, undefined, ou false para checkbox
        if (value === '' || value === null || value === undefined || (field.field_type === 'checkbox' && !value)) {
          alert(`The field "${field.name}" is required.`); // Ou usar um componente de erro mais elegante
          return false;
        }
      }
    }
    return true;
  };

  // Função para submeter o formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    if (loadingGeneration) {
      // Previne múltiplos cliques durante o processamento
      return;
    }

    try {
      setLoadingGeneration(true);
      setError(null);
      setDownloadUrl(null); // Limpa URL anterior
      setGenerationMessage(''); // Limpa mensagem anterior

      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        throw new Error('Access token not found in localStorage.');
      }

      // Prepara o payload para a API de geração
      const payload: GenerateDocumentRequest = {
        document_type_id: typeIdNumber,
        filled_fields: filledFields,
      };

      const response = await fetch(`${API_BASE_URL}/user/document-types/generate-document`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorBody = await response.text(); // ou response.json() se for JSON consistente
        console.error("Error from generation API:", errorBody);
        throw new Error(`HTTP error! Status: ${response.status}, Body: ${errorBody}`);
      }

      const data: GenerateDocumentResponse = await response.json(); // Use o tipo importado

      if (data.success) {
        // Extraímos a URL de download da resposta
        const downloadUrlFromResponse = data.data?.download_url;
        const locationIdentifier = data.data?.location_identifier; // Pode ser útil se não tiver download_url

        if (downloadUrlFromResponse) {
          setDownloadUrl(downloadUrlFromResponse);
        } else if (locationIdentifier) {
          // Se a API não der download_url, podemos construir a URL com o location_identifier
          // Supondo que a rota de download seja /api/v1/user/documents/download/{location_identifier}
          setDownloadUrl(`${API_BASE_URL}/user/documents/download/${encodeURIComponent(locationIdentifier)}`);
        } else {
          // Se não houver nenhuma forma de obter a URL, é um erro da API
          console.error("Generation API did not return download_url or location_identifier.");
          setError("Failed to retrieve download information from the server.");
          return;
        }

        setGenerationMessage(data.message || 'Document generated successfully!');

      } else {
        // A API retornou success: false
        throw new Error(data.message || 'API returned success: false during document generation.');
      }
    } catch (err) {
      console.error('Error generating document:', err);
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred while generating the document.';
      setError(errorMessage);
    } finally {
      setLoadingGeneration(false);
    }
  };

  // Função para disparar o download
  const triggerDownload = () => {
    if (downloadUrl) {
      // Abre a URL de download em uma nova aba/janela (o comportamento pode variar por navegador)
      window.open(downloadUrl, '_blank');
      // Alternativamente, pode-se usar um iframe oculto ou fetch + blob se precisar de mais controle
      // Exemplo com fetch + blob (útil para nomes de arquivo específicos ou autenticação via cookie):
      /*
      fetch(downloadUrl, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`, // Se ainda for necessário
        },
      })
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        // Define o nome do arquivo, se possível, ou deixa o navegador decidir
        // link.setAttribute('download', 'documento_gerado.docx');
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
      })
      .catch(err => {
        console.error('Error downloading the file:', err);
        setError('Failed to download the generated document.');
      });
      */
    }
  };

  if (loadingFields) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="ml-4 text-gray-600">Loading document fields...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
        <div className="p-4 bg-red-100 text-red-700 rounded-lg">
          Error: {error}
        </div>
        <button
          onClick={() => navigate(-1)} // Volta para a tela anterior
          className="mt-4 px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Fill Document Details</h1>
          <p className="text-gray-600 mb-6">
            {/* Usar documentType.name se já estiver disponível, senão mostrar o ID */}
            Filling fields for: {documentType ? documentType.name : `Document Type ID: ${typeIdNumber}`}
          </p>

          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {generationMessage && (
            <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-lg">
              {generationMessage}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Document Information</h2>
              {fields.length === 0 ? (
                <p className="text-gray-500 italic">No fields configured for this document type.</p>
              ) : (
                <div className="space-y-4">
                  {fields.map((field) => (
                    <div key={field.id} className="space-y-1">
                      <label htmlFor={field.name} className="block text-sm font-medium text-gray-700">
                        {field.name} {field.is_required && '*'}
                        {field.description && <span className="block text-xs text-gray-500 mt-1">{field.description}</span>}
                      </label>
                      {renderFieldInput(field)}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="flex justify-between items-center pt-4">
              <button
                type="button"
                onClick={() => navigate(-1)} // Volta para a tela anterior
                className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
                disabled={loadingGeneration}
              >
                Back
              </button>
              <button
                type="submit"
                className={`px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors ${
                  loadingGeneration ? 'opacity-70 cursor-not-allowed' : ''
                }`}
                disabled={loadingGeneration}
              >
                {loadingGeneration ? 'Generating...' : 'Generate Document'}
              </button>
            </div>
          </form>

          {/* Seção de Download - Visível apenas após a geração bem-sucedida */}
          {downloadUrl && (
            <div className="mt-8 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Document Generated!</h2>
              <p className="text-gray-600 mb-4">
                Your document has been created successfully. Click the button below to download it.
              </p>
              <button
                onClick={triggerDownload}
                className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-lg transition-colors"
              >
                Download Document (.docx)
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default UploadAndFillFields;