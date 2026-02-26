// src/types/documentTypes.ts

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
   PaginationData<DocumentType>; // Usando generics para reutilizar PaginationData
  error_code: string | null;
  errors: string[] | null;
}

// --- Tipos para outras operações ---

// Exemplo para criar:
export interface CreateDocumentTypeRequest {
  name: string;
  description: string;
}

// Exemplo para atualizar (campos opcionais):
export interface UpdateDocumentTypeRequest extends Partial<CreateDocumentTypeRequest> {
  // Pode incluir campos específicos para atualização, se necessário
  // id: number; // Exemplo: se a API exigir o ID no body da requisição PUT/PATCH
}

// Exemplo para resposta de criação/atualização:
export interface SingleDocumentTypeResponse {
  success: boolean;
  message: string;
   DocumentType;
  error_code: string | null;
  errors: string[] | null;
}

export interface DeleteDocumentTypeResponse {
  success: boolean;
  message: string;
  data: {
    message: string;
    deleted_id: number;
  } | null; // Pode ser null em caso de erro
  error_code: string | null;
  errors: string[] | null;
}