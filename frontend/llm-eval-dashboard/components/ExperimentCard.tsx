import Link from "next/link";

export default function ExperimentCard({ experiment }: any) {
  return (
    <Link
      href={`/experiments/${experiment.run_id}`}
      className="border rounded-xl p-5 shadow-sm hover:shadow-md transition bg-white"
    >
      <p className="text-sm text-gray-500">{experiment.started_at}</p>
      <h2 className="text-lg font-semibold mt-2">{experiment.model}</h2>
      <p className="text-sm mt-1">
        Status: {experiment.status}
      </p>
    </Link>
  );
}