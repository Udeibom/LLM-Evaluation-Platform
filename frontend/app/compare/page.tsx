"use client";

import { useEffect, useState } from "react";

type TestSuite = {
  id: string;
  name: string;
};

const AVAILABLE_MODELS = [
  "llama-3.3-70b-versatile",
  "mixtral-8x7b-32768",
  "llama3-8b-8192"
];

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function ComparePage() {
  const [testSuites, setTestSuites] = useState<TestSuite[]>([]);
  const [selectedSuite, setSelectedSuite] = useState("");
  const [modelA, setModelA] = useState("");
  const [modelB, setModelB] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);

  useEffect(() => {
    async function loadSuites() {
      try {
        const res = await fetch(`${API_URL}/test-suites/`);

        if (!res.ok) {
          throw new Error("Failed to fetch test suites");
        }

        const data = await res.json();
        setTestSuites(data);
      } catch (error) {
        console.error("Error loading test suites:", error);
      }
    }

    loadSuites();
  }, []);

  async function runComparison() {
    if (!selectedSuite || !modelA || !modelB) {
      alert("Select test suite and two models.");
      return;
    }

    try {
      setLoading(true);
      setResult(null);
      setJobStatus("starting");

      const res = await fetch(`${API_URL}/comparisons/run`, {
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

      if (!res.ok) {
        throw new Error("Comparison failed");
      }

      const job = await res.json();

      // Poll the job status
      let finished = false;

      while (!finished) {
        const statusRes = await fetch(`${API_URL}/comparisons/${job.id}`);
        const data = await statusRes.json();

        setJobStatus(data.status);

        if (data.status === "completed") {
          setResult(data);
          finished = true;
        } else {
          await new Promise((r) => setTimeout(r, 2000));
        }
      }
    } catch (error) {
      console.error("Comparison error:", error);
      alert("Failed to run comparison.");
    } finally {
      setLoading(false);
    }
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
        {testSuites.map((suite) => (
          <option key={suite.id} value={suite.id}>
            {suite.name}
          </option>
        ))}
      </select>

      <h3 style={{ marginTop: 20 }}>Model A</h3>
      <select value={modelA} onChange={(e) => setModelA(e.target.value)}>
        <option value="">-- Select --</option>
        {AVAILABLE_MODELS.map((model) => (
          <option key={model} value={model}>
            {model}
          </option>
        ))}
      </select>

      <h3 style={{ marginTop: 20 }}>Model B</h3>
      <select value={modelB} onChange={(e) => setModelB(e.target.value)}>
        <option value="">-- Select --</option>
        {AVAILABLE_MODELS.map((model) => (
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

      {loading && (
        <div style={{ marginTop: 20 }}>
          <p>Job Status: {jobStatus || "starting..."}</p>
        </div>
      )}

      {result && (
        <div style={{ marginTop: 40 }}>
          <h2>Results</h2>

          <p><b>Total Prompts:</b> {result.total_prompts}</p>
          <p><b>Model A Wins:</b> {result.wins_a}</p>
          <p><b>Model B Wins:</b> {result.wins_b}</p>
          <p><b>Ties:</b> {result.ties}</p>

          <p>
            <b>Win Rate A:</b>{" "}
            {(result.win_rate_a * 100).toFixed(1)}%
          </p>

          <p>
            <b>Win Rate B:</b>{" "}
            {(result.win_rate_b * 100).toFixed(1)}%
          </p>
        </div>
      )}
    </div>
  );
}