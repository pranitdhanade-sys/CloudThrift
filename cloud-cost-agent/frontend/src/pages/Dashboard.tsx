import { useEffect, useState } from "react";

import { KpiCard } from "../components/KpiCard";
import { fetchSummary, type DashboardSummary } from "../api/dashboard";

export function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    fetchSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  return (
    <section className="grid grid-cols-1 gap-4 md:grid-cols-4">
      <KpiCard title="MTD Spend" value={`$${summary?.mtd_spend ?? "--"}`} trend={`${summary?.mom_change_pct ?? "--"}% MoM`} />
      <KpiCard title="30D Forecast" value={`$${summary?.forecast_30d ?? "--"}`} />
      <KpiCard title="Savings Found" value={`$${summary?.identified_savings ?? "--"}`} />
      <KpiCard title="Status" value={summary ? "Healthy" : "Loading"} />
    </section>
  );
}
