import api from "./api";
import type {
  CreateUrlPayload,
  DashboardStats,
  ShortenedUrl,
  UpdateUrlPayload,
} from "../types";

export async function createShortUrl(payload: CreateUrlPayload): Promise<ShortenedUrl> {
  const { data } = await api.post<ShortenedUrl>("/shorten", payload);
  return data;
}

export async function fetchUrls(search?: string): Promise<ShortenedUrl[]> {
  const { data } = await api.get<ShortenedUrl[]>("/urls", {
    params: search ? { search } : undefined,
  });
  return data;
}

export async function fetchUrlById(id: number): Promise<ShortenedUrl> {
  const { data } = await api.get<ShortenedUrl>(`/urls/${id}`);
  return data;
}

export async function updateUrl(id: number, payload: UpdateUrlPayload): Promise<ShortenedUrl> {
  const { data } = await api.put<ShortenedUrl>(`/urls/${id}`, payload);
  return data;
}

export async function deleteUrl(id: number): Promise<void> {
  await api.delete(`/urls/${id}`);
}

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const { data } = await api.get<DashboardStats>("/dashboard/stats");
  return data;
}
