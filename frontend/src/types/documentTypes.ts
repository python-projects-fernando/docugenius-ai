// Representa um único tipo de documento
export interface DocumentType {
  id: number;
  name: string;
  description: string;
}

// Representa os dados da paginação
export interface PaginationData<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Representa a resposta da API para a listagem de tipos de documento
export interface ListDocumentTypesResponse {
  success: boolean;
  message: string;
  data: PaginationData<DocumentType>; // Usando generics para reutilizar PaginationData
  error_code: string | null;
  errors: string[] | null;
}

// --- Tipos para outras operações (futuras) ---
// Exemplo para criar/atualizar:
export interface CreateDocumentTypeRequest {
  name: string;
  description: string;
}

export interface UpdateDocumentTypeRequest extends Partial<CreateDocumentTypeRequest> {
  // Pode incluir campos específicos para atualização, se necessário
  // Por exemplo, se a API exigir o ID no body:
  // id: number;
}

// Exemplo para resposta de criação/atualização:
export interface SingleDocumentTypeResponse {
  success: boolean;
  message: string;
  data: DocumentType;
  error_code: string | null;
  errors: string[] | null;
}