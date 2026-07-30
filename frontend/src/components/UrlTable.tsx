import type { ShortenedUrl, UpdateUrlPayload } from "../types";
import { UrlRow } from "./UrlRow";

interface UrlTableProps {
  urls: ShortenedUrl[];
  baseUrl: string;
  onEdit: (id: number, payload: UpdateUrlPayload) => Promise<unknown>;
  onDelete: (id: number) => Promise<unknown>;
}

export function UrlTable({ urls, baseUrl, onEdit, onDelete }: UrlTableProps) {
  if (urls.length === 0) {
    return (
      <div className="card flex flex-col items-center gap-1 px-6 py-16 text-center">
        <p className="text-sm font-medium text-slate-300">No links yet</p>
        <p className="text-sm text-slate-500">Shorten your first URL above to see it here.</p>
      </div>
    );
  }

  return (
    <div className="card overflow-x-auto">
      <table className="w-full min-w-[640px] text-left">
        <thead>
          <tr className="border-b border-ink-700 text-xs uppercase tracking-wide text-slate-500">
            <th className="px-4 py-3 font-medium">Short link</th>
            <th className="px-4 py-3 font-medium">Destination</th>
            <th className="px-4 py-3 font-medium">Clicks</th>
            <th className="px-4 py-3 font-medium">Last visited</th>
            <th className="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody>
          {urls.map((url) => (
            <UrlRow key={url.id} url={url} baseUrl={baseUrl} onEdit={onEdit} onDelete={onDelete} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
