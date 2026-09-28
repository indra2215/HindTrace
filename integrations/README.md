# HindTrace — Live Enterprise Integrations

Connectors for hooking HindTrace into live enterprise communication channels.

## 1. Slack Integration (`integrations/slack_client.py`)
- **Incoming Webhooks**: Post rich Block Kit escalation cards to `#cloud-eng` or team channels on SEV1/SEV2 incidents.
- **Setup**:
  1. Go to `https://api.slack.com/apps` and create a Slack App.
  2. Enable **Incoming Webhooks** and add a webhook to your target channel.
  3. Add to `.env`:
     ```bash
     SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T.../B.../..."
     ```

## 2. Gmail / Google Workspace (`integrations/gmail_client.py`)
- **Use Case**: Searches and ingests automated incident email alerts and postmortems (`label:incident OR subject:INC-`).
- **Setup**:
  1. In Google Cloud Console, enable the **Gmail API**.
  2. Create OAuth 2.0 Client Credentials and download as `credentials.json`.
  3. Set `GMAIL_CREDENTIALS_PATH="credentials.json"` in `.env`.

## 3. Google Drive (`integrations/gdrive_client.py`)
- **Use Case**: Automatically syncs shared postmortem folders and runbooks into `corpus/`.
- **Setup**:
  1. In Google Cloud Console, enable the **Google Drive API**.
  2. Share your Incident Postmortems folder with the client email.
  3. Set `GDRIVE_INCIDENTS_FOLDER_ID="your_folder_id"` in `.env`.

