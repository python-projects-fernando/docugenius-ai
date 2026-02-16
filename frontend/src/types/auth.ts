export interface LoginRequestDTO {
  identifier: string;
  password: string;
}

export type UserRole = 'admin' | 'common';

export interface UserDataDTO {
  id: number;
  username: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginSuccessResponseDTO {
  success: true;
  message: string;
  data: {
    access_token: string;
    token_type: string;
    user: UserDataDTO;
  };
  error_code: null;
  errors: null;
}

export interface LoginErrorResponseDTO {
  success: false;
  message: string;
  data: null;
  error_code?: string;
  errors?: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}

export type LoginResponseDTO = LoginSuccessResponseDTO | LoginErrorResponseDTO;

export interface User {
  id: string;
  username: string;
  email: string;
  role: UserRole;
}
