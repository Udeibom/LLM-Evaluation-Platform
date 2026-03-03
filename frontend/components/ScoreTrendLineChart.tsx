"use client";

import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function ScoreTrendLineChart({ data }: { data: any[] }) {
  return (
    <LineChart width={700} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="run_id" />
      <YAxis domain={[0, 5]} />
      <Tooltip />
      <Line type="monotone" dataKey="mean_score" />
    </LineChart>
  );
}