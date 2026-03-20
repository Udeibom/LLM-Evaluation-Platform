import { getLeaderboard } from "@/lib/api";
import { ExperimentSummary } from "@/types/experiment";

export default async function ExperimentsPage() {
  const experiments: ExperimentSummary[] = await getLeaderboard();

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">LLM Eval Dashboard</h1>

      <div className="grid gap-6 md:grid-cols-2">
        {experiments.map((exp) => (
          <div
            key={exp.experiment_id}
            className="border rounded-lg p-6 shadow bg-white"
          >
            <h2 className="text-xl font-semibold mb-2">
              {exp.model_name}
            </h2>

            <p>Status: {exp.status ?? "N/A"}</p>
            <p>Samples: {exp.num_samples ?? "N/A"}</p>

            <div className="mt-4 space-y-1">
              <p>
                Mean Score:{" "}
                {typeof exp.mean_score === "number"
                  ? exp.mean_score.toFixed(2)
                  : "N/A"}
              </p>

              <p>
                Std Dev:{" "}
                {typeof exp.std_dev === "number"
                  ? exp.std_dev.toFixed(2)
                  : "N/A"}
              </p>

              <p>
                Hallucination Rate:{" "}
                {typeof exp.hallucination_rate === "number"
                  ? (exp.hallucination_rate * 100).toFixed(1) + "%"
                  : "N/A"}
              </p>

              <p>
                Avg Latency:{" "}
                {typeof exp.avg_latency === "number"
                  ? exp.avg_latency.toFixed(0) + " ms"
                  : "N/A"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}