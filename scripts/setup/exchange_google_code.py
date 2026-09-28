import sys
import json
import requests
from pathlib import Path

VERIFIER = "company_HindTrace_secure_code_verifier_123456789012345678901234567890"

def exchange_code(code: str):
    root = Path(__file__).parent.parent.parent
    creds_path = root / "credentials.json"
    if not creds_path.exists():
        print("credentials.json not found!")
        return False

    with open(creds_path, "r", encoding="utf-8") as f:
        creds_data = json.load(f)["installed"]

    data = {
        "code": code.strip(),
        "client_id": creds_data["client_id"],
        "client_secret": creds_data["client_secret"],
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "authorization_code",
        "code_verifier": VERIFIER
    }

    resp = requests.post("https://oauth2.googleapis.com/token", data=data)
    if resp.status_code == 200:
        token_data = resp.json()
        token_path = root / "token.json"
        with open(token_path, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2)
        print(f"SUCCESS: token.json written to {token_path}")
        return True
    else:
        print(f"FAILED (status {resp.status_code}): {resp.text}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        exchange_code(sys.argv[1])
    else:
        print("Usage: python exchange_google_code.py <AUTHORIZATION_CODE>")

