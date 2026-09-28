"""
CLI Script: Verify Groq API Connectivity
========================================
Usage: python scripts/test_groq.py
"""

import os
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY", "")

if __name__ == "__main__":
    print(f">> Testing Groq API connectivity with key: {GROQ_KEY[:10]}...")
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")
    try:
        models = [m.id for m in client.models.list().data]
        print(f">> [OK] Connected! Available models ({len(models)}): {models[:5]}")
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": "Say 'Axiom Groq Ready'"}],
        )
        print(f">> [OK] LLM Test Response: {resp.choices[0].message.content}")
    except Exception as e:
        print(f">> [ERROR] connecting to Groq: {e}")
