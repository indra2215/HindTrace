"""
Gold Standard Incident Question Dataset Loader
"""
import json
from pathlib import Path
from typing import List, Dict, Any

def load_gold_questions() -> List[Dict[str, Any]]:
    """Loads gold evaluation questions for benchmark testing."""
    root = Path(__file__).resolve().parent.parent.parent
    gt_path = root / "evaluation" / "gold_questions" / "ground_truth.json"
    if gt_path.exists():
        with open(gt_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
