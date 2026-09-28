"""
Google OAuth2 Setup Script
===========================
Run this ONCE to generate token.json for Gmail + Google Drive API access.

Usage:
    python scripts/setup_google_auth.py

Prerequisites:
    pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

What it does:
    1. Opens your browser for Google sign-in
    2. Requests Gmail (read) + Drive (read) scopes
    3. Saves token.json in the project root
    4. From then on, all API calls use token.json automatically
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

CREDENTIALS_FILE = project_root / "credentials.json"
TOKEN_FILE       = project_root / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

def main():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("\n[ERROR] Google client libraries not installed.")
        print("Run: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2\n")
        sys.exit(1)

    if not CREDENTIALS_FILE.exists():
        print(f"\n[ERROR] credentials.json not found at: {CREDENTIALS_FILE}")
        sys.exit(1)

    creds = None

    # Load existing token if present
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If no valid token, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("[OK] Token refreshed successfully.")
        else:
            print("\n>> Opening browser for Google sign-in...")
            print("   Scopes: Gmail (read-only) + Drive (read-only)")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
            print("[OK] Authentication successful!")

        # Save token for future use
        TOKEN_FILE.write_text(creds.to_json())
        print(f"[OK] token.json saved to: {TOKEN_FILE}")
    else:
        print("[OK] Existing token.json is valid, no re-auth needed.")

    # Quick connectivity test
    print("\n>> Testing Gmail API...")
    try:
        from googleapiclient.discovery import build
        service = build("gmail", "v1", credentials=creds)
        profile = service.users().getProfile(userId="me").execute()
        print(f"[OK] Gmail connected as: {profile.get('emailAddress')}")
        print(f"     Total messages: {profile.get('messagesTotal', '?')}")
    except Exception as e:
        print(f"[WARN] Gmail test failed: {e}")

    print("\n>> Testing Drive API...")
    try:
        from googleapiclient.discovery import build
        drive = build("drive", "v3", credentials=creds)
        about = drive.about().get(fields="user").execute()
        print(f"[OK] Drive connected as: {about['user']['emailAddress']}")
    except Exception as e:
        print(f"[WARN] Drive test failed: {e}")

    print("\n=== Setup Complete ===")
    print("token.json is saved. Gmail and Drive integrations are now active.")
    print("Restart the server: python run.py")


if __name__ == "__main__":
    main()
