// types/experiment.ts

export interface Experiment {
  id: string;
  run_id: string;
  test_suite_id: string;
  model_name: string;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  duration_ms: number | null;
}

export interface ExperimentSummary {
  experiment_id: string;
  run_id: string;
  model_name: string;
  status: string;

  num_samples: number;
  mean_score: number;
  std_dev: number;
  hallucination_rate: number;

  avg_latency: number;
  max_latency: number;
  min_latency: number;

  started_at: string | null;
  completed_at: string | null;
  duration_ms: number | null;
}