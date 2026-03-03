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