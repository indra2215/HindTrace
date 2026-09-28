"""
CLI Script: Pre-seed Hindsight Memory Banks
===========================================
Usage: python scripts/seed_memory.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from memory.hindsight_client import seed_historical_memories, list_memories

if __name__ == "__main__":
    print(">> Pre-seeding Hindsight Memory with Historical Incidents...")
    count = seed_historical_memories()
    print(f">> [OK] Successfully seeded {count} incident memories.")

    print("\nCurrent Memory Bank Status:")
    for bank in ["org-shared", "team-ml", "team-cloud"]:
        mems = list_memories(bank)
        print(f"  - [{bank}]: {len(mems)} memories")
        for m in mems[:3]:
            print(f"      * {m['key']} ({m['content'].get('verdict')})")
