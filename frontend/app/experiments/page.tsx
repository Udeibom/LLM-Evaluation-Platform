import { getExperiments } from "@/lib/api";
import { Experiment } from "@/types/experiment";

export default async function ExperimentsPage() {
  const experiments: Experiment[] = await getExperiments();

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Experiments</h1>

      <div className="space-y-4">
        {experiments.map((exp) => (
          <div
            key={exp.id}
            className="border rounded-lg p-4 shadow-sm bg-white"
          >
            <p><strong>Model:</strong> {exp.model_name}</p>
            <p><strong>Status:</strong> {exp.status}</p>
            <p><strong>Run ID:</strong> {exp.run_id}</p>
            <p><strong>Duration:</strong> {exp.duration_ms ?? "N/A"} ms</p>
            <p><strong>Started At:</strong> {exp.started_at ?? "N/A"}</p>
            <p><strong>Completed At:</strong> {exp.completed_at ?? "N/A"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}