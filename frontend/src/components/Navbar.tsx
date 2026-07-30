import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const navLinkClasses = ({ isActive }: { isActive: boolean }) =>
  `text-sm font-medium transition ${
    isActive ? "text-signal-400" : "text-slate-400 hover:text-slate-200"
  }`;

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="border-b border-ink-700 bg-ink-950/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-8">
          <NavLink to="/dashboard" className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-signal-500" />
            <span className="font-display text-lg font-semibold text-slate-50">LinkFlow</span>
          </NavLink>
          <nav className="flex items-center gap-6">
            <NavLink to="/dashboard" className={navLinkClasses}>
              Dashboard
            </NavLink>
            <NavLink to="/links" className={navLinkClasses}>
              My Links
            </NavLink>
          </nav>
        </div>

        <div className="flex items-center gap-4">
          <span className="hidden text-sm text-slate-400 sm:inline">{user?.name}</span>
          <button onClick={logout} className="btn-secondary">
            Log out
          </button>
        </div>
      </div>
    </header>
  );
}
