import { useCallback, useEffect, useState } from "react";
import {
  createShortUrl,
  deleteUrl as deleteUrlRequest,
  fetchUrls,
  updateUrl as updateUrlRequest,
} from "../services/urlService";
import type { CreateUrlPayload, ShortenedUrl, UpdateUrlPayload } from "../types";

export function useUrls(search: string) {
  const [urls, setUrls] = useState<ShortenedUrl[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadUrls = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchUrls(search || undefined);
      setUrls(data);
    } catch {
      setError("Couldn't load your links. Try refreshing.");
    } finally {
      setIsLoading(false);
    }
  }, [search]);

  useEffect(() => {
    loadUrls();
  }, [loadUrls]);

  async function addUrl(payload: CreateUrlPayload): Promise<ShortenedUrl> {
    const created = await createShortUrl(payload);
    setUrls((prev) => [created, ...prev]);
    return created;
  }

  async function editUrl(id: number, payload: UpdateUrlPayload) {
    const updated = await updateUrlRequest(id, payload);
    setUrls((prev) => prev.map((u) => (u.id === id ? updated : u)));
    return updated;
  }

  async function removeUrl(id: number) {
    await deleteUrlRequest(id);
    setUrls((prev) => prev.filter((u) => u.id !== id));
  }

  return { urls, isLoading, error, addUrl, editUrl, removeUrl, reload: loadUrls };
}
