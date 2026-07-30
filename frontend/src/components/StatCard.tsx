interface StatCardProps {
  label: string;
  value: number | string;
  accent?: boolean;
}

export function StatCard({ label, value, accent = false }: StatCardProps) {
  return (
    <div className="card p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p
        className={`mt-2 font-display text-3xl font-semibold ${
          accent ? "text-signal-400" : "text-slate-50"
        }`}
      >
        {value}
      </p>
    </div>
  );
}
