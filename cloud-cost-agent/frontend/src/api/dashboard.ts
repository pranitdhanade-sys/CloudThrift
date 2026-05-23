export type DashboardSummary = {
  mtd_spend: number;
  mom_change_pct: number;
  forecast_30d: number;
  identified_savings: number;
};

export async function fetchSummary(baseUrl = "http://localhost:8000"): Promise<DashboardSummary> {
  const response = await fetch(`${baseUrl}/api/dashboard/summary`);
  if (!response.ok) {
    throw new Error("Failed to fetch summary");
  }
  return response.json();
}
