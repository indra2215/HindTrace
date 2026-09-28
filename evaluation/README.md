# HindTrace — Evaluation Subsystem

This directory contains the automated evaluation harness for the synthetic engineering corpus.

## Files

1. **`eval_harness.py`**:
   - Executes benchmarks against the 25 gold questions in `ground_truth/gold_questions.csv`.
   - Compares expected vs agent verdict (`confirmed`, `partial`, `unanswerable`).
   - Tracks trap survivability across all 9 trap categories (T1–T9).
   - Measures Hindsight memory hit frequency.

2. **`metrics.py`**:
   - Computes Verdict Accuracy, Citation Precision/Recall/F1, and Memory Efficiency.

## Running Evaluation via CLI

```powershell
python scripts/run_eval.py
```
Or via the UI at `http://localhost:8000/` under the **Eval Harness** tab.

