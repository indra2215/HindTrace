"""
Entry point for HindTrace
Run: python run.py
"""
import sys
import os
from pathlib import Path

# Put project root on sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load .env
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

import uvicorn

if __name__ == "__main__":
    print(">> Starting HindTrace")
    print("   Corpus:  ", os.getenv("CORPUS_PATH", "../output_extracted/corpus"))
    print("   Hindsight: local SQLite mode")
    print("   URL:     http://localhost:8000\n")

    uvicorn.run(
        "api.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=False,
        log_level="info",
    )

