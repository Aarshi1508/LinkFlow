import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { StatCard } from "../components/StatCard";
import { fetchDashboardStats } from "../services/urlService";
import { useUrls } from "../hooks/useUrls";
import type { DashboardStats } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const { urls, isLoading } = useUrls("");

  useEffect(() => {
    fetchDashboardStats().then(setStats).catch(() => setStats(null));
  }, []);

  const recentUrls = urls.slice(0, 5);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="mt-1 text-sm text-slate-400">An overview of your shortened links.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <StatCard label="Total links" value={stats?.total_links ?? "—"} />
        <StatCard label="Total clicks" value={stats?.total_clicks ?? "—"} accent />
        <StatCard label="Active links" value={stats?.active_links ?? "—"} />
      </div>

      <div className="card p-5">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-base font-semibold">Recent links</h2>
          <Link to="/links" className="text-sm text-signal-400 hover:underline">
            View all
          </Link>
        </div>

        {isLoading ? (
          <p className="text-sm text-slate-500">Loading...</p>
        ) : recentUrls.length === 0 ? (
          <p className="text-sm text-slate-500">
            No links yet.{" "}
            <Link to="/links" className="text-signal-400 hover:underline">
              Create your first one
            </Link>
            .
          </p>
        ) : (
          <ul className="divide-y divide-ink-700">
            {recentUrls.map((url) => (
              <li key={url.id} className="flex items-center justify-between py-3">
                <div className="min-w-0">
                  <Link
                    to={`/links/${url.id}`}
                    className="font-mono text-sm text-signal-400 hover:underline"
                  >
                    {API_BASE_URL}/link/{url.short_code}
                  </Link>
                  <p className="truncate text-xs text-slate-500">{url.original_url}</p>
                </div>
                <span className="ml-4 shrink-0 text-sm text-slate-400">
                  {url.total_clicks} clicks
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
