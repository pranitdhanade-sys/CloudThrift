type Props = {
  title: string;
  value: string;
  trend?: string;
};

export function KpiCard({ title, value, trend }: Props) {
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="mt-2 text-2xl font-semibold">{value}</p>
      {trend ? <p className="mt-1 text-xs text-emerald-600">{trend}</p> : null}
    </div>
  );
}
