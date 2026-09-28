import sys
import json
import base64
import hashlib
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

VERIFIER = "company_HindTrace_secure_code_verifier_123456789012345678901234567890"
# SHA256 of verifier
CHALLENGE = "3sl3ropbD-QlDgHP4wpNHOqAq8XrFPvH-HvC6VFS4Dg"

PORT = 8999
REDIRECT_URI = f"http://localhost:{PORT}/"

ROOT = Path(__file__).resolve().parent.parent.parent
CREDS_FILE = ROOT / "credentials.json"
TOKEN_FILE = ROOT / "token.json"

with open(CREDS_FILE, "r", encoding="utf-8") as f:
    creds_info = json.load(f)["installed"]

CLIENT_ID = creds_info["client_id"]
CLIENT_SECRET = creds_info["client_secret"]

AUTH_URL = (
    f"https://accounts.google.com/o/oauth2/auth?"
    f"response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly"
    f"&code_challenge={CHALLENGE}"
    f"&code_challenge_method=S256"
    f"&access_type=offline"
    f"&prompt=consent"
)

# Also an OOB URL if localhost redirect cannot be reached
AUTH_URL_OOB = (
    f"https://accounts.google.com/o/oauth2/auth?"
    f"response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob"
    f"&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly"
    f"&code_challenge={CHALLENGE}"
    f"&code_challenge_method=S256"
    f"&access_type=offline"
    f"&prompt=consent"
)

def exchange_and_save(code: str, redirect_uri: str):
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code_verifier": VERIFIER
    }
    r = requests.post("https://oauth2.googleapis.com/token", data=data)
    if r.status_code == 200:
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(r.text)
        print("\n[SUCCESS] token.json written successfully!")
        return True, "Success! Google Account successfully connected to HindTrace. You may close this tab."
    else:
        err = f"Failed to exchange code: {r.status_code} - {r.text}"
        print(f"\n[ERROR] {err}")
        return False, err

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "code" in query:
            code = query["code"][0]
            ok, msg = exchange_and_save(code, REDIRECT_URI)
            self.send_response(200 if ok else 400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""
            <html>
            <body style="font-family: sans-serif; background: #09090b; color: #f4f4f5; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
                <div style="background: #18181b; padding: 40px; border-radius: 12px; border: 1px solid #27272a; text-align: center; max-width: 500px;">
                    <h2 style="color: {'#22c55e' if ok else '#ef4444'};">{'Authentication Successful!' if ok else 'Authentication Failed'}</h2>
                    <p>{msg}</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
            if ok:
                threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code parameter found.")

def start_server():
    import threading
    server = HTTPServer(("localhost", PORT), OAuthHandler)
    print("\n" + "="*80)
    print("HindTrace - GOOGLE OAUTH URL (Automatic Localhost Redirect):")
    print(AUTH_URL)
    print("="*80)
    print("\nALTERNATIVE (Copy-Paste Code flow if redirect doesn't work):")
    print(AUTH_URL_OOB)
    print("="*80 + "\n")
    sys.stdout.flush()
    server.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        code_arg = sys.argv[1].strip()
        # Try exchanging as OOB code
        ok, msg = exchange_and_save(code_arg, "urn:ietf:wg:oauth:2.0:oob")
        if not ok:
            # Try exchanging as localhost code
            exchange_and_save(code_arg, REDIRECT_URI)
    else:
        start_server()

