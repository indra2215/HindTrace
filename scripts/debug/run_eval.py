"""
CLI Script: Run 25 Gold Questions Evaluation
============================================
Usage: python scripts/run_eval.py
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluation.eval_harness import run_evaluation

if __name__ == "__main__":
    print("=" * 65)
    print(">> Running HindTrace 25 Gold Questions Benchmark")
    print("=" * 65)

    summary = run_evaluation()

    print(f"\nCompleted in {summary['duration_seconds']}s")
    print(f"Overall Accuracy:  {summary['accuracy']}% ({summary['correct']}/{summary['total_questions']})")
    print(f"Hindsight Hits:    {summary['memory_hits']} ({summary['memory_hit_rate']}%)")
    print("\nTrap Breakdown:")
    for trap, stats in summary["trap_breakdown"].items():
        print(f"  - [{trap:^8}]: {stats['correct']}/{stats['total']} ({stats['rate']}%)")
    print("=" * 65)

