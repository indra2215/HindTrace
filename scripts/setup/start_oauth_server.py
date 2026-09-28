"""
Google OAuth Local Server Helper
Runs a local server on port 8085 to catch the redirect automatically,
and prints the clickable link for the user.
"""
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
]

def main():
    root = Path(__file__).parent.parent.parent
    creds_path = root / "credentials.json"
    if not creds_path.exists():
        print("credentials.json not found!")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        str(creds_path),
        scopes=SCOPES,
        redirect_uri="http://localhost:8085/"
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    print("\n" + "="*70)
    print("CLICK THIS URL TO SIGN IN TO GOOGLE:")
    print(auth_url)
    print("="*70 + "\n")
    
    # Run server listening on port 8085
    creds = flow.run_local_server(port=8085, open_browser=False, prompt='consent')
    
    token_path = root / "token.json"
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    print(f"\n[SUCCESS] token.json successfully saved to {token_path}!")

if __name__ == "__main__":
    main()
