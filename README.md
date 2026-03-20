# LLM Evaluation Platform

A backend-first platform for benchmarking Large Language Models (LLMs) on factual QA, reasoning, and instruction-following tasks using LLM-as-a-judge scoring, hallucination detection, latency tracking, and leaderboard analytics.

---

## 🚀 Why This Exists

Evaluating LLMs is still messy and inconsistent. Most developers rely on subjective testing or scattered benchmarks that don’t reflect real-world use.

This platform standardizes LLM evaluation by:
- Running structured experiments across datasets
- Scoring outputs using a judge model
- Tracking reliability metrics like hallucination rate
- Comparing models with reproducible results

---

## ✨ Features

- Run experiments across multiple LLMs
- Evaluate outputs using LLM-as-a-judge scoring
- Track:
  - Mean score
  - Hallucination rate
  - Latency
  - Win rates (head-to-head comparisons)
- Benchmark performance across dataset categories
- Parallel inference pipeline for faster evaluations
- Leaderboard system for model ranking
- API-first design for easy integration

---

## 🧠 Architecture

**Core Components:**

- FastAPI Backend – Handles experiment execution and API exposure  
- Groq Inference Layer – Runs model predictions  
- Judge Service – Scores outputs using an LLM  
- Metrics Service – Computes evaluation metrics  
- Leaderboard API – Aggregates and ranks model performance  
- Database (PostgreSQL / Supabase) – Stores experiments and results  

**Flow:**

Datasets → Experiment Runner → Model Outputs → Judge Service → Evaluations → Metrics → Leaderboard API

---

## 📊 Dataset Categories

- Factual QA
- Reasoning
- Instruction Following

---

## 🔌 API Endpoints

POST   /experiments  
GET    /experiments/{id}  
GET    /leaderboard  

---

## 🏆 Results Snapshot

| Model                     | Mean Score | Hallucination Rate | Avg Latency | Pass Rate |
|--------------------------|-----------|--------------------|-------------|----------|
| llama-3.3-70b-versatile  | 3.65      | 0.5%               | 1232 ms     | -        |
| llama-3.1-8b-instant     | 3.32      | 3.9%               | 1638 ms     | -        |
| llama-3.1-70b-versatile  | 0.94      | 0.0%               | 289 ms      | -        |
| mixtral-8x7b-32768       | 0.31      | 0.0%               | 58 ms       | -        |
| llama3-8b-8192           | 0.31      | 0.0%               | 69 ms       | -        |


---

## ⚙️ Getting Started

### 1. Clone the repo
git clone https://github.com/Udeibom/LLM-Eval-Platform.git  

### 2. Create virtual environment
python -m venv venv  
source venv/bin/activate  

### 3. Install dependencies
pip install -r requirements.txt  

### 4. Run the server
uvicorn main:app --reload  

### 5. Open API docs
http://127.0.0.1:8000/docs  

---

## 🧪 Example Use Case

Run a comparison between two models on a factual dataset and get:
- Win rates
- Tie rates
- Latency comparison
- Judge-based scoring

---

## 🔮 Future Work

- Semantic similarity scoring using embeddings
- Category-level leaderboards
- Judge response caching
- Confidence intervals for evaluation metrics
- Full frontend dashboard
- Experiment history visualization

---

## 🛠 Tech Stack

- Python / FastAPI
- Groq API (LLM inference)
- PostgreSQL / Supabase
- Async pipelines for parallel execution

---

## 📌 Notes

This project is designed as a reusable evaluation framework for:
- AI product teams
- LLM benchmarking
- Developer tooling
- AI-assisted coding workflows

---

## 📬 Contact

If you’d like to collaborate or discuss this project, feel free to reach out.
