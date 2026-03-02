export interface DocumentType {
  id: number;
  name: string;
  description: string;
}

export interface DocumentField {
  id: number;
  name: string;
  description: string;
  field_type: string;
  is_required: boolean;
  document_type_id: number;
}

export interface PaginationData<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ListDocumentTypesResponse {
  success: boolean;
  message: string;
  data: PaginationData<DocumentType>;
  error_code: string | null;
  errors: string[] | null;
}

export interface ListDocumentFieldsResponse {
  success: boolean;
  message: string;
  data: PaginationData<DocumentField>;
  error_code: string | null;
  errors: string[] | null;
}

export interface CreateDocumentTypeRequest {
  name: string;
  description: string;
}

export interface UpdateDocumentTypeRequest extends Partial<CreateDocumentTypeRequest> {}

export interface SingleDocumentTypeResponse {
  success: boolean;
  message: string;
  data: DocumentType;
  error_code: string | null;
  errors: string[] | null;
}

export interface DeleteDocumentTypeResponse {
  success: boolean;
  message: string;
  data: {
    message: string;
    deleted_id: number;
  } | null;
  error_code: string | null;
  errors: string[] | null;
}

export interface CreateDocumentFieldRequest {
  name: string;
  description: string;
  field_type: string;
  is_required: boolean;
  document_type_id: number;
}

export interface UpdateDocumentFieldRequest extends Partial<CreateDocumentFieldRequest> {}

export interface SingleDocumentFieldResponse {
  success: boolean;
  message: string;
  data: DocumentField;
  error_code: string | null;
  errors: string[] | null;
}

// Exemplo para deletar campo de documento
export interface DeleteDocumentFieldResponse {
  success: boolean;
  message: string;
   boolean; // O campo 'data' é um booleano indicando sucesso/falha da operação
  error_code: string | null;
  errors: string[] | null;
}

export interface SuggestDocumentTypesRequest {
  business_description: string;
}

export interface SuggestedDocumentType {
  name: string;
  description: string;
}

export interface SuggestDocumentTypesResponse {
  success: boolean;
  message: string;
  data: {
    suggested_document_types: SuggestedDocumentType[];
  };
  error_code: string | null;
  errors: string[] | null;
}