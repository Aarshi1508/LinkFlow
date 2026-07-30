import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchUrlById } from "../services/urlService";
import { StatCard } from "../components/StatCard";
import type { ShortenedUrl } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function formatDateTime(value: string | null) {
  if (!value) return "Never";
  return new Date(value).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export function LinkDetail() {
  const { id } = useParams<{ id: string }>();
  const [url, setUrl] = useState<ShortenedUrl | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    fetchUrlById(Number(id))
      .then(setUrl)
      .catch(() => setError("That link doesn't exist, or you don't have access to it."));
  }, [id]);

  if (error) {
    return (
      <div className="flex flex-col gap-4">
        <p className="text-sm text-danger-400">{error}</p>
        <Link to="/links" className="text-sm text-signal-400 hover:underline">
          Back to My Links
        </Link>
      </div>
    );
  }

  if (!url) {
    return <p className="text-sm text-slate-500">Loading...</p>;
  }

  const shortLink = `${API_BASE_URL}/link/${url.short_code}`;

  return (
    <div className="flex flex-col gap-8">
      <div>
        <Link to="/links" className="text-sm text-slate-400 hover:text-slate-200">
          ← Back to My Links
        </Link>
        <h1 className="mt-2 font-mono text-2xl font-semibold text-slate-50">
          /link/{url.short_code}
        </h1>
        <p className="mt-1 max-w-xl truncate text-sm text-slate-400" title={url.original_url}>
          → {url.original_url}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <StatCard label="Total clicks" value={url.total_clicks} accent />
        <StatCard label="Created" value={formatDateTime(url.created_at)} />
        <StatCard label="Last visited" value={formatDateTime(url.last_visited)} />
      </div>

      <div className="card flex items-center justify-between p-5">
        <span className="font-mono text-sm text-slate-300">{shortLink}</span>
        <button
          onClick={() => navigator.clipboard.writeText(shortLink)}
          className="btn-secondary"
        >
          Copy link
        </button>
      </div>
    </div>
  );
}
