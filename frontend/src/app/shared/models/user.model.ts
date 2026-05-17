export interface User {
  id: string;
  email: string;
  full_name: string;
  phone: string;
  role: 'admin' | 'guest';
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  phone: string;
  role: 'admin' | 'guest';
}

export interface UserUpdate {
  full_name?: string;
  email?: string;
  phone?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}
