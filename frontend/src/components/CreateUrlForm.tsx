import { useState, type FormEvent } from "react";
import type { AxiosError } from "axios";
import type { ApiError, CreateUrlPayload } from "../types";

interface CreateUrlFormProps {
  onCreate: (payload: CreateUrlPayload) => Promise<unknown>;
}

export function CreateUrlForm({ onCreate }: CreateUrlFormProps) {
  const [originalUrl, setOriginalUrl] = useState("");
  const [customAlias, setCustomAlias] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await onCreate({
        original_url: originalUrl,
        custom_alias: customAlias.trim() || undefined,
      });
      setOriginalUrl("");
      setCustomAlias("");
    } catch (err) {
      const axiosErr = err as AxiosError<ApiError>;
      setError(axiosErr.response?.data?.detail || "Couldn't create that link. Check the URL and try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="card p-5">
      <h2 className="mb-4 text-base font-semibold">Shorten a new link</h2>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label htmlFor="original_url" className="label">
            Destination URL
          </label>
          <input
            id="original_url"
            type="url"
            required
            placeholder="https://example.com/very/long/path"
            className="input-field"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
          />
        </div>
        <div className="sm:w-48">
          <label htmlFor="custom_alias" className="label">
            Custom alias (optional)
          </label>
          <input
            id="custom_alias"
            type="text"
            placeholder="my-link"
            className="input-field"
            value={customAlias}
            onChange={(e) => setCustomAlias(e.target.value)}
          />
        </div>
        <button type="submit" disabled={isSubmitting} className="btn-primary h-[38px]">
          {isSubmitting ? "Creating..." : "Shorten"}
        </button>
      </div>
      {error && <p className="mt-3 text-sm text-danger-400">{error}</p>}
    </form>
  );
}
