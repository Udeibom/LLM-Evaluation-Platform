import { getExperimentSummary } from "@/lib/api";

export default async function ExperimentDetail({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const summary = await getExperimentSummary(id);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">
        Model: {summary.model}
      </h1>

      <div className="grid grid-cols-2 gap-4">
        <Stat label="Mean Score" value={summary.mean_score} />
        <Stat label="Std Dev" value={summary.std_dev} />
        <Stat
          label="Hallucination Rate"
          value={`${summary.hallucination_rate * 100}%`}
        />
        <Stat
          label="Win Rate"
          value={`${summary.win_rate * 100}%`}
        />
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: any }) {
  return (
    <div className="p-4 border rounded-lg">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-xl font-semibold">{value}</p>
    </div>
  );
}