"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function MeanScoreBarChart({ data }: { data: any[] }) {
  return (
    <BarChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="model" />
      <YAxis domain={[0, 5]} />
      <Tooltip />
      <Bar dataKey="mean_score" />
    </BarChart>
  );
}