import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { Navbar } from "./Navbar";

/**
 * Gates any nested route behind authentication. While we're still checking
 * for a stored token (isLoading), we render nothing rather than briefly
 * flashing the login page for an already-logged-in user.
 */
export function ProtectedRoute() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-ink-950">
        <span className="text-sm text-slate-500">Loading...</span>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-ink-950">
      <Navbar />
      <main className="mx-auto max-w-6xl px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}
