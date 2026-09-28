"""
Database Schema Initializer for Hindsight Local SQLite
"""
import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bank TEXT NOT NULL,
    incident_id TEXT NOT NULL,
    root_cause TEXT NOT NULL,
    resolution TEXT NOT NULL,
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_memories_bank ON memories(bank);
CREATE INDEX IF NOT EXISTS idx_memories_incident ON memories(incident_id);
"""

def initialize_database(db_path: Path):
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    print(f"Database schema initialized at {db_path}")

if __name__ == "__main__":
    db_file = Path(__file__).resolve().parent.parent / "hindsight_local.db"
    initialize_database(db_file)
