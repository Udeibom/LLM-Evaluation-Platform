import { Experiment } from "@/types/experiment";

export const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getExperiments(): Promise<Experiment[]> {
  const res = await fetch(`${API_URL}/experiments`);
  if (!res.ok) {
    throw new Error("Failed to fetch experiments");
  }
  return res.json();
}

export async function getExperimentSummary(id: string) {
  const res = await fetch(`${API_URL}/experiments/${id}/summary`);
  if (!res.ok) {
    throw new Error("Failed to fetch experiment summary");
  }
  return res.json();
}

export async function getAllExperimentSummaries() {
  const experiments = await getExperiments();

  const summaries = await Promise.all(
    experiments.map(async (exp) => {
      const res = await fetch(`${API_URL}/experiments/${exp.id}/summary`);
      if (!res.ok) return null;
      return res.json();
    })
  );

  return summaries.filter(Boolean);
}

export async function compareExperiments(a: string, b: string) {
  const res = await fetch(
    `${API_URL}/experiments/compare?experiment_a=${a}&experiment_b=${b}`
  );
  if (!res.ok) throw new Error("Comparison failed");
  return res.json();
}

export async function compareStatistics(a: string, b: string) {
  const res = await fetch(
    `${API_URL}/experiments/compare/statistics?experiment_a=${a}&experiment_b=${b}`
  );
  if (!res.ok) throw new Error("Statistical test failed");
  return res.json();
}