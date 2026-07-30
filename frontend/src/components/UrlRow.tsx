import { useState } from "react";
import { Link } from "react-router-dom";
import type { ShortenedUrl, UpdateUrlPayload } from "../types";

interface UrlRowProps {
  url: ShortenedUrl;
  baseUrl: string;
  onEdit: (id: number, payload: UpdateUrlPayload) => Promise<unknown>;
  onDelete: (id: number) => Promise<unknown>;
}

function formatDate(value: string | null) {
  if (!value) return "Never";
  return new Date(value).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function UrlRow({ url, baseUrl, onEdit, onDelete }: UrlRowProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [alias, setAlias] = useState(url.short_code);
  const [destination, setDestination] = useState(url.original_url);
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const shortLink = `${baseUrl}/link/${url.short_code}`;

  async function handleSave() {
    setError(null);
    try {
      await onEdit(url.id, { original_url: destination, custom_alias: alias });
      setIsEditing(false);
    } catch {
      setError("Couldn't save - alias may already be taken.");
    }
  }

  if (isEditing) {
    return (
      <tr className="border-b border-ink-700 bg-ink-800/40">
        <td className="px-4 py-3" colSpan={5}>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
            <input
              className="input-field sm:w-40"
              value={alias}
              onChange={(e) => setAlias(e.target.value)}
            />
            <input
              className="input-field flex-1"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
            />
            <div className="flex gap-2">
              <button onClick={handleSave} className="btn-primary">
                Save
              </button>
              <button onClick={() => setIsEditing(false)} className="btn-secondary">
                Cancel
              </button>
            </div>
          </div>
          {error && <p className="mt-2 text-sm text-danger-400">{error}</p>}
        </td>
      </tr>
    );
  }

  return (
    <tr className="border-b border-ink-700 last:border-0 hover:bg-ink-800/30">
      <td className="px-4 py-3">
        <Link
          to={`/links/${url.id}`}
          className="font-mono text-sm text-signal-400 hover:underline"
        >
          /link/{url.short_code}
        </Link>
      </td>
      <td className="max-w-xs truncate px-4 py-3 text-sm text-slate-400" title={url.original_url}>
        {url.original_url}
      </td>
      <td className="px-4 py-3 text-sm text-slate-200">{url.total_clicks}</td>
      <td className="px-4 py-3 text-sm text-slate-400">{formatDate(url.last_visited)}</td>
      <td className="px-4 py-3">
        <div className="flex items-center justify-end gap-2">
          <button
            onClick={() => navigator.clipboard.writeText(shortLink)}
            className="btn-secondary !px-3 !py-1.5 text-xs"
          >
            Copy
          </button>
          <button
            onClick={() => setIsEditing(true)}
            className="btn-secondary !px-3 !py-1.5 text-xs"
          >
            Edit
          </button>
          {confirmingDelete ? (
            <>
              <button onClick={() => onDelete(url.id)} className="btn-danger !py-1.5 text-xs">
                Confirm
              </button>
              <button
                onClick={() => setConfirmingDelete(false)}
                className="btn-secondary !px-3 !py-1.5 text-xs"
              >
                Cancel
              </button>
            </>
          ) : (
            <button
              onClick={() => setConfirmingDelete(true)}
              className="btn-danger !py-1.5 text-xs"
            >
              Delete
            </button>
          )}
        </div>
      </td>
    </tr>
  );
}
