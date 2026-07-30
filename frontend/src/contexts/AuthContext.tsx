import { createContext, useEffect, useState, type ReactNode } from "react";
import { fetchProfile, loginUser, registerUser } from "../services/authService";
import type { LoginPayload, RegisterPayload, User } from "../types";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const TOKEN_KEY = "linkflow_token";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  // Wait until any stored token has been validated.
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
      setIsLoading(false);
      return;
    }

    fetchProfile()
      .then(setUser)
      .catch(() => localStorage.removeItem(TOKEN_KEY))
      .finally(() => setIsLoading(false));
  }, []);

  async function login(payload: LoginPayload) {
    const { access_token } = await loginUser(payload);
    localStorage.setItem(TOKEN_KEY, access_token);
    const profile = await fetchProfile();
    setUser(profile);
  }

  async function register(payload: RegisterPayload) {
    await registerUser(payload);
   // Log in after registration to obtain a JWT.
    await login({ email: payload.email, password: payload.password });
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
