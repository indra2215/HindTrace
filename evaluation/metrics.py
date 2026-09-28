"""
Evaluation Metrics Computation
==============================
Computes precision, recall, F1, citation accuracy, and memory hit efficiency.
"""

def compute_metrics(results: list[dict]) -> dict:
    """Calculate accuracy and citation overlap statistics."""
    total = len(results)
    if total == 0:
        return {}

    correct = sum(1 for r in results if r["correct"])
    memory_hits = sum(1 for r in results if r.get("memory_used"))

    citation_precisions = []
    citation_recalls = []

    for r in results:
        actual_cites = set(r.get("citations", []))
        gold_cites = set(r.get("gold_docs", []))

        if gold_cites:
            intersection = actual_cites & gold_cites
            p = len(intersection) / len(actual_cites) if actual_cites else 0.0
            rec = len(intersection) / len(gold_cites)
            citation_precisions.append(p)
            citation_recalls.append(rec)

    avg_p = sum(citation_precisions) / len(citation_precisions) if citation_precisions else 0.0
    avg_r = sum(citation_recalls) / len(citation_recalls) if citation_recalls else 0.0
    f1 = 2 * (avg_p * avg_r) / (avg_p + avg_r) if (avg_p + avg_r) > 0 else 0.0

    return {
        "verdict_accuracy": round((correct / total) * 100, 1),
        "memory_hit_percentage": round((memory_hits / total) * 100, 1),
        "citation_precision": round(avg_p * 100, 1),
        "citation_recall": round(avg_r * 100, 1),
        "citation_f1": round(f1 * 100, 1),
    }
