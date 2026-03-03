"use client";

import { useEffect, useState } from "react";
import {
  compareExperiments,
  compareStatistics,
  getExperiments,
} from "@/lib/api";

interface Experiment {
  id: string;
  model_name: string;
}

export default function ComparePage() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [expA, setExpA] = useState<string>("");
  const [expB, setExpB] = useState<string>("");

  const [comparison, setComparison] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    async function loadExperiments() {
      const data = await getExperiments();
      setExperiments(data);
    }
    loadExperiments();
  }, []);

  async function handleCompare() {
    if (!expA || !expB) return;

    const result = await compareExperiments(expA, expB);
    const statResult = await compareStatistics(expA, expB);

    setComparison(result);
    setStats(statResult);
  }

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">
        Compare Experiments
      </h1>

      {/* Selectors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <select
          value={expA}
          onChange={(e) => setExpA(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="">Select Experiment A</option>
          {experiments.map((exp) => (
            <option key={exp.id} value={exp.id}>
              {exp.model_name} ({exp.id.slice(0, 6)})
            </option>
          ))}
        </select>

        <select
          value={expB}
          onChange={(e) => setExpB(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="">Select Experiment B</option>
          {experiments.map((exp) => (
            <option key={exp.id} value={exp.id}>
              {exp.model_name} ({exp.id.slice(0, 6)})
            </option>
          ))}
        </select>
      </div>

      <button
        onClick={handleCompare}
        className="bg-black text-white px-4 py-2 rounded"
      >
        Compare
      </button>

      {/* Results */}
      {comparison && (
        <div className="mt-8 border rounded p-6 bg-white shadow">
          <h2 className="text-xl font-semibold mb-4">
            Comparison Results
          </h2>

          <p>Total Prompts: {comparison.total_prompts}</p>
          <p>Wins A: {comparison.wins_a}</p>
          <p>Wins B: {comparison.wins_b}</p>
          <p>Ties: {comparison.ties}</p>

          <div className="mt-4">
            <p>
              Win Rate A:{" "}
              {(comparison.win_rate_a * 100).toFixed(1)}%
            </p>
            <p>
              Win Rate B:{" "}
              {(comparison.win_rate_b * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      )}

      {stats && (
        <div className="mt-6 border rounded p-6 bg-white shadow">
          <h2 className="text-xl font-semibold mb-4">
            Statistical Test
          </h2>

          <p>T-Statistic: {stats.t_statistic.toFixed(3)}</p>
          <p>P-Value: {stats.p_value.toFixed(5)}</p>

          <p
            className={`mt-2 font-semibold ${
              stats.significant
                ? "text-green-600"
                : "text-red-600"
            }`}
          >
            {stats.significant
              ? "Statistically Significant Difference"
              : "No Significant Difference"}
          </p>
        </div>
      )}
    </div>
  );
}