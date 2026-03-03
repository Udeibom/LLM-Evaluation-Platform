export default function ComparisonTable({ data }: any) {
  return (
    <table className="w-full border rounded-lg overflow-hidden">
      <thead className="bg-gray-100 text-left">
        <tr>
          <th className="p-3">Metric</th>
          <th className="p-3">{data.model_a}</th>
          <th className="p-3">{data.model_b}</th>
        </tr>
      </thead>
      <tbody>
        <tr className="border-t">
          <td className="p-3">Mean Score</td>
          <td className="p-3">{data.mean_a}</td>
          <td className="p-3">{data.mean_b}</td>
        </tr>
        <tr className="border-t">
          <td className="p-3">Win Rate</td>
          <td className="p-3">{data.win_rate_a}</td>
          <td className="p-3">{data.win_rate_b}</td>
        </tr>
        <tr className="border-t">
          <td className="p-3">p-value</td>
          <td className="p-3" colSpan={2}>
            {data.p_value}
          </td>
        </tr>
      </tbody>
    </table>
  );
}