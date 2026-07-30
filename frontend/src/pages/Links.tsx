import { useState } from "react";
import { CreateUrlForm } from "../components/CreateUrlForm";
import { UrlTable } from "../components/UrlTable";
import { useUrls } from "../hooks/useUrls";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function Links() {
  const [search, setSearch] = useState("");
  const { urls, isLoading, error, addUrl, editUrl, removeUrl } = useUrls(search);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold">My links</h1>
        <p className="mt-1 text-sm text-slate-400">Create, search, and manage your short links.</p>
      </div>

      <CreateUrlForm onCreate={addUrl} />

      <div className="flex items-center justify-between">
        <input
          type="text"
          placeholder="Search by URL or short code..."
          className="input-field max-w-xs"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {error && <p className="text-sm text-danger-400">{error}</p>}

      {isLoading ? (
        <p className="text-sm text-slate-500">Loading...</p>
      ) : (
        <UrlTable urls={urls} baseUrl={API_BASE_URL} onEdit={editUrl} onDelete={removeUrl} />
      )}
    </div>
  );
}
