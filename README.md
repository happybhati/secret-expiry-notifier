# 🔐 Secret Expiry Notifier Template

[![Use this template](https://img.shields.io/badge/Use%20this%20template-blue?style=for-the-badge&logo=github)](https://github.com/happybhati/secret-expiry-notifier/generate)

This GitHub Actions-based automation checks a Google Sheet daily for secrets nearing expiration and sends Slack alerts to the responsible teams.

---

## 📦 Features
- ✅ Reads secret metadata from Google Sheets
- 🚨 Sends Slack alerts 30 days before expiry
- 🔁 Configurable dry-run/testing mode
- 📊 Logs alerts into a `Logs` tab in your Sheet
- 💬 Uses Slack Block Kit for clean, structured messages

---

## 📁 Folder Structure
```
.
├── .github/
│   └── workflows/
│       └── notifier.yml         # GitHub Actions workflow
├── notifier.py                  # Main Python script
├── config.yaml                  # Config (sheet ID, thresholds)
├── requirements.txt             # Python dependencies
└── README.md                    # You are here
```

---

## 🚀 Setup Instructions

### 1. 🧾 Google Sheet
Create a new Google Sheet with the following headers in row 1:

```
Secret Name | Expiry Date | Rotation Instructions | Owner | Slack Tag | Environment
```

Example row:
```
db-prod-password | 2025-05-20 | Follow rotation guide: runbook-123 | Platform Team | @platform-team | prod
```

Share the sheet with your service account email (see step 2).

---

### 2. 🔐 Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable APIs:
   - Google Sheets API
   - Google Drive API
4. Create a **Service Account**
5. Generate a **JSON key**, download it
6. Copy the `client_email` and share your Google Sheet with it

---

### 3. 🔔 Slack Setup

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app → Enable **Incoming Webhooks**
3. Add a webhook to your desired channel
4. Copy the Webhook URL

---

### 4. 🔐 GitHub Secrets
Go to your GitHub repo → Settings → Secrets → Actions → Add:

- `GOOGLE_CREDENTIALS_JSON` → Paste the entire content of your JSON key
- `SLACK_WEBHOOK_URL` → Your Slack webhook URL

---

### 5. ⚙️ config.yaml (Optional)
```yaml
sheet_id: "YOUR_SHEET_ID"
alert_days: 30
default_slack_webhook: "USE_GITHUB_SECRET"
default_slack_channel: "#secrets-alerts"
```

---

### 6. 🧪 Test It Locally
```bash
export GOOGLE_CREDENTIALS_JSON='your json here'
export SLACK_WEBHOOK_URL='your webhook here'
python notifier.py
```

Use this to verify before pushing live.

---

### 7. 🤖 GitHub Actions Workflow

`.github/workflows/notifier.yml`
```yaml
name: Secret Expiry Notifier

on:
  schedule:
    - cron: '0 11 * * *'  # 6 AM EST / 7 AM EDT
  workflow_dispatch:

jobs:
  run-notifier:
    runs-on: ubuntu-latest
    env:
      GOOGLE_CREDENTIALS_JSON: ${{ secrets.GOOGLE_CREDENTIALS_JSON }}
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
      DRY_RUN: false
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          pip install -r requirements.txt
          python notifier.py
```

---

## ✅ Status
Built by the community to help any team maintain secret hygiene without paid services.

PRs welcome 💙

---

## 👤 Author

Developed with 💻 by [Happy Bhati](https://github.com/happybhati)

- Senior Software Engineer | Red Hat
- Passionate about automation, observability, and solving real-world ops problems

Feel free to fork, reuse, and improve!
