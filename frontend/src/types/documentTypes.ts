export interface DocumentType {
  id: number;
  name: string;
  description: string;
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
  PaginationData<DocumentType>;
  error_code: string | null;
  errors: string[] | null;
}

export interface CreateDocumentTypeRequest {
  name: string;
  description: string;
}

export interface UpdateDocumentTypeRequest extends Partial<CreateDocumentTypeRequest> {
}

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
  } | null;
  error_code: string | null;
  errors: string[] | null;
}