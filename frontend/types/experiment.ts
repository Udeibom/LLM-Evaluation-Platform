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