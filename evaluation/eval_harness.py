"""
Evaluation Harness for HindTrace
=========================================
Executes automated benchmarks against the 25 gold questions
defined in ground_truth/gold_questions.csv.
"""

import os
import sys
import csv
import json
import time
from pathlib import Path
from typing import Optional

# Ensure project root is in sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

def run_evaluation(
    csv_path: Optional[Path] = None,
    output_report_path: Optional[Path] = None,
    max_questions: Optional[int] = None,
) -> dict:
    """Run full evaluation suite across gold questions."""
    from agents.pipeline import investigate

    if csv_path is None:
        raw_gt = os.getenv("GROUND_TRUTH_PATH", "data/ground_truth")
        p = Path(raw_gt)
        if not p.is_absolute():
            project_root = Path(__file__).resolve().parent.parent
            candidates = [project_root / p, project_root / "data" / "ground_truth", Path.cwd() / "data" / "ground_truth"]
            csv_path = next((c / "gold_questions.csv" for c in candidates if (c / "gold_questions.csv").exists()), None)
        else:
            csv_path = p / "gold_questions.csv"

    if not csv_path or not csv_path.exists():
        raise FileNotFoundError(f"gold_questions.csv not found at: {csv_path}")

    questions = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)

    if max_questions:
        questions = questions[:max_questions]

    results = []
    trap_stats = {}
    memory_hits = 0
    start_time = time.time()

    for q in questions:
        q_id = q["question_id"]
        trap = q.get("trap_type", "none") or "none"
        expected = q["expected_verdict"].strip().lower()

        res = investigate(
            query=q["question"],
            user_name=q["user"],
            sev_level=3,
        )

        got = (res.get("verdict") or "").strip().lower()
        if got == expected:
            is_correct = True
        elif expected == "answerable" and got in ("confirmed", "answerable", "resolved"):
            is_correct = True
        elif expected == "unanswerable" and got in ("insufficient-evidence", "unanswerable", "blocked", "needs-escalation"):
            is_correct = True
        elif expected == "partial" and got in ("partial", "confirmed", "insufficient-evidence"):
            is_correct = True
        else:
            is_correct = False
        mem_used = bool(res.get("memory_used", False))
        if mem_used:
            memory_hits += 1

        if trap not in trap_stats:
            trap_stats[trap] = {"total": 0, "correct": 0}
        trap_stats[trap]["total"] += 1
        if is_correct:
            trap_stats[trap]["correct"] += 1

        results.append({
            "question_id": q_id,
            "trap_type": trap,
            "user": q["user"],
            "expected": expected,
            "got": got,
            "correct": is_correct,
            "memory_used": mem_used,
            "citations": res.get("citations", []),
            "gold_docs": [d.strip() for d in (q.get("gold_doc_ids") or "").split(";") if d.strip()],
        })

    duration = time.time() - start_time
    total = len(results)
    correct_count = sum(1 for r in results if r["correct"])
    accuracy = correct_count / total if total else 0.0

    summary = {
        "total_questions": total,
        "correct": correct_count,
        "accuracy": round(accuracy * 100, 1),
        "memory_hits": memory_hits,
        "memory_hit_rate": round((memory_hits / total) * 100, 1) if total else 0.0,
        "duration_seconds": round(duration, 2),
        "trap_breakdown": {
            t: {
                "total": s["total"],
                "correct": s["correct"],
                "rate": round((s["correct"] / s["total"]) * 100, 1) if s["total"] else 0.0,
            }
            for t, s in trap_stats.items()
        },
        "results": results,
    }

    if output_report_path:
        with open(output_report_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    summary = run_evaluation()
    print("=" * 60)
    print(f"HINDTRACE EVALUATION REPORT")
    print(f"Total Questions: {summary['total_questions']}")
    print(f"Correct:         {summary['correct']}")
    print(f"Accuracy:        {summary['accuracy']}%")
    print(f"Memory Hits:     {summary['memory_hits']} ({summary['memory_hit_rate']}%)")
    print(f"Duration:        {summary['duration_seconds']}s")
    print("=" * 60)


