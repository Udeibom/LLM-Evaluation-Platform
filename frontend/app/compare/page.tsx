"use client";

import { useEffect, useState } from "react";

type TestSuite = {
  id: string;
  name: string;
};

const AVAILABLE_MODELS = [
  "llama-3.3-70b-versatile",
  "google/flan-t5-base",
  "mistralai/Mistral-7B-Instruct-v0.2"
];

export default function ComparePage() {
  const [testSuites, setTestSuites] = useState<TestSuite[]>([]);
  const [selectedSuite, setSelectedSuite] = useState("");
  const [modelA, setModelA] = useState("");
  const [modelB, setModelB] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/test-suites/")
      .then(res => res.json())
      .then(data => setTestSuites(data));
  }, []);

  async function runComparison() {
    if (!selectedSuite || !modelA || !modelB) {
      alert("Select test suite and two models.");
      return;
    }

    setLoading(true);
    setResult(null);

    const res = await fetch("http://localhost:8000/comparisons/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        test_suite_id: selectedSuite,
        model_a: modelA,
        model_b: modelB
      })
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Run Model Comparison</h1>

      <h3>Select Test Suite</h3>
      <select
        value={selectedSuite}
        onChange={(e) => setSelectedSuite(e.target.value)}
      >
        <option value="">-- Select --</option>
        {testSuites.map(suite => (
          <option key={suite.id} value={suite.id}>
            {suite.name}
          </option>
        ))}
      </select>

      <h3 style={{ marginTop: 20 }}>Model A</h3>
      <select value={modelA} onChange={(e) => setModelA(e.target.value)}>
        <option value="">-- Select --</option>
        {AVAILABLE_MODELS.map(model => (
          <option key={model} value={model}>
            {model}
          </option>
        ))}
      </select>

      <h3 style={{ marginTop: 20 }}>Model B</h3>
      <select value={modelB} onChange={(e) => setModelB(e.target.value)}>
        <option value="">-- Select --</option>
        {AVAILABLE_MODELS.map(model => (
          <option key={model} value={model}>
            {model}
          </option>
        ))}
      </select>

      <div style={{ marginTop: 30 }}>
        <button onClick={runComparison} disabled={loading}>
          {loading ? "Running..." : "Run Comparison"}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 40 }}>
          <h2>Results</h2>
          <p>Total Prompts: {result.total_prompts}</p>
          <p>Wins A: {result.wins_a}</p>
          <p>Wins B: {result.wins_b}</p>
          <p>Ties: {result.ties}</p>
          <p>Win Rate A: {(result.win_rate_a * 100).toFixed(1)}%</p>
          <p>Win Rate B: {(result.win_rate_b * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  );
}