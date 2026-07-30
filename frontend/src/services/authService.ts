import api from "./api";
import type { AuthResponse, LoginPayload, RegisterPayload, User } from "../types";

export async function registerUser(payload: RegisterPayload): Promise<User> {
  const { data } = await api.post<User>("/register", payload);
  return data;
}

export async function loginUser(payload: LoginPayload): Promise<AuthResponse> {
  const { data } = await api.post<AuthResponse>("/login", payload);
  return data;
}

export async function fetchProfile(): Promise<User> {
  const { data } = await api.get<User>("/profile");
  return data;
}
