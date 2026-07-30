// Shared frontend types matching the backend schemas.
export interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ShortenedUrl {
  id: number;
  original_url: string;
  short_code: string;
  total_clicks: number;
  last_visited: string | null;
  created_at: string;
}

export interface DashboardStats {
  total_links: number;
  total_clicks: number;
  active_links: number;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface CreateUrlPayload {
  original_url: string;
  custom_alias?: string;
}

export interface UpdateUrlPayload {
  original_url?: string;
  custom_alias?: string;
}

// Shape of FastAPI's default error response: { "detail": "..." }
export interface ApiError {
  detail: string;
}
