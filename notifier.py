import os
import json
import yaml
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from slack_sdk.webhook import WebhookClient

# Load config
CONFIG_PATH = "config.yaml"
config = {}
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

SHEET_ID = config.get("sheet_id")
ALERT_DAYS = config.get("alert_days", 30)

# Slack webhook (fallback to GitHub secret environment variable)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL") or config.get("default_slack_webhook")
DEFAULT_SLACK_CHANNEL = config.get("default_slack_channel", "#general")

# Setup Google Sheets API client
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

if not credentials_json:
    raise Exception("Missing GOOGLE_CREDENTIALS_JSON")

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(credentials_json),
    scopes=SCOPES
)
client = gspread.authorize(credentials)

# Open the sheet
sheet = client.open_by_key(SHEET_ID).sheet1
records = sheet.get_all_records()

# Date calculations
today = datetime.date.today()
alert_window = today + datetime.timedelta(days=ALERT_DAYS)

# Slack client
slack = WebhookClient(SLACK_WEBHOOK_URL)

# Track sent alerts
alerts_sent = 0

# Process each row
for row in records:
    try:
        secret_name = row.get("Secret Name")
        expiry_str = row.get("Expiry Date")
        rotation_instructions = row.get("Rotation Instructions")
        slack_tag = row.get("Slack Tag") or "team"
        environment = row.get("Environment") or "unknown"

        expiry_date = datetime.datetime.strptime(expiry_str, "%Y-%m-%d").date()
        days_remaining = (expiry_date - today).days

        if today <= expiry_date <= alert_window:
            # Send formatted Slack alert using Block Kit
            slack.send(
                blocks=[
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "🚨 Secret Expiry Alert"}
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Secret:*\n`{secret_name}`"},
                            {"type": "mrkdwn", "text": f"*Environment:*\n`{environment}`"},
                            {"type": "mrkdwn", "text": f"*Expires on:*\n*{expiry_date}* (_in {days_remaining} days_)"},
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*🔁 Rotation:*\n{rotation_instructions}"},
                            {"type": "mrkdwn", "text": f"*👤 Responsible:*\n{slack_tag}"}
                        ]
                    },
                    {"type": "divider"}
                ]
            )
            alerts_sent += 1

    except Exception as e:
        print(f"⚠️ Error processing row: {row} → {e}")

print(f"✅ Alerting complete. {alerts_sent} secrets flagged for expiry.")
