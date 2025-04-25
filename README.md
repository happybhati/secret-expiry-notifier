# 🔐 Secret Expiry Notifier

This automation checks a Google Sheet daily for secrets that are nearing expiration and sends alerts to the responsible Slack teams.

### Features
- Fetches secrets data from Google Sheets
- Sends Slack notifications 30 days before expiry
- Works as a GitHub Action (no extra infrastructure needed)

### Setup
1. Share your Google Sheet with a service account
2. Add your service account key & Slack Webhook to GitHub Secrets
3. Done! GitHub Actions will notify teams daily 🎯
