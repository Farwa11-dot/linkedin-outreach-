# n8n Setup Guide — Reminder Workflow Only

This workflow does one thing: every weekday morning at 8am, it reads your
Google Sheets CRM and emails you a plain-text digest of who needs a follow-up today.

It does NOT send any outreach emails. You do that yourself, manually, in Gmail.

---

## What You Get

An email to yourself every weekday morning that looks like this:

```
OUTREACH FOLLOW-UP DIGEST — Monday, April 14, 2026
============================================================

⚡ REPLIES RECEIVED (respond today):
----------------------------------------
• Smile Bright Dental (Dr. Martinez)
  Email: office@smilebrightdental.com
  Reply summary: Interested, asked about pricing
  Status: Replied

📬 FOLLOW-UPS DUE TODAY (3):
----------------------------------------
• Glow Aesthetic Clinic (Sarah)
  Email: hello@glowclinic.com
  Stage: Contacted
  Last contact: 2026-04-12
  Personalization: No booking button on Google profile

• Downtown Dentistry (Dr. Kim)
  Email: info@downtowndentistry.com
  Stage: Follow-Up 1 Sent
  Last contact: 2026-04-11
  Personalization: Closed Saturdays

• Pure Med Spa (Jamie)
  Email: jamie@puremedspa.com
  Stage: Follow-Up 2 Sent
  Last contact: 2026-04-09
  Personalization: Instagram active but 0 Google posts

============================================================
TOTAL ACTIONS TODAY: 4
  Replies to handle: 1
  Follow-ups to send: 3
  Overdue (catch up): 0
```

---

## Setup Steps

### Step 1: Install n8n

**Local machine (simplest):**
```bash
npm install n8n -g
n8n start
# Open: http://localhost:5678
```

**Docker:**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

For this reminder workflow, n8n only needs to run on your machine.
It does not need to be hosted online — just open at 8am (or run it in the background).

If you want it to run automatically without keeping your machine on: deploy free on
[Railway.app](https://railway.app) or [Render.com](https://render.com).

---

### Step 2: Add Google Credentials

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project called `OutreachCRM`
3. Enable these APIs:
   - **Gmail API**
   - **Google Sheets API**
4. Credentials → Create → OAuth 2.0 Client ID → Desktop App
5. Download the JSON file

In n8n:
1. Left sidebar → **Credentials** → **Add Credential**
2. Search: `Google Sheets OAuth2 API` → connect with your Google account
3. Name it: `Google Sheets — CRM`
4. Add another: `Gmail OAuth2 API` → connect with your Gmail
5. Name it: `Gmail — Your Account`

---

### Step 3: Import the Workflow

1. n8n → **Workflows** → **Import from File**
2. Upload `reminders-workflow.json`
3. Open the workflow, then update:

| Node | What to change |
|---|---|
| `Read All Leads` | Set `documentId` to your spreadsheet ID |
| `Email Digest to Yourself` | Set `toList` to your personal email |
| All nodes with credentials | Select the correct credential from the dropdown |

**Your spreadsheet ID** is in the URL:
```
https://docs.google.com/spreadsheets/d/THIS_PART_HERE/edit
```

---

### Step 4: Test It

1. In the workflow editor → click **Execute Workflow** (manual trigger button)
2. Check if an email arrives in your inbox
3. Does the digest list your test leads correctly?
4. If yes → toggle the workflow to **Active** (top-right switch)

---

### Step 5: Adjust the Schedule (Optional)

The default is 8am Monday–Friday. To change:
1. Click the **Schedule Trigger** node
2. Change the cron expression:
   - `0 7 * * 1-5` → 7am weekdays
   - `0 8 * * 1-5` → 8am weekdays (default)
   - `0 9 * * 1-5` → 9am weekdays

You can also run it manually any time by clicking "Execute Workflow" in n8n.

---

## Optional: Telegram Instead of Email

If you prefer a Telegram notification (faster to notice on mobile):

1. Create a Telegram bot: message @BotFather on Telegram → `/newbot`
2. Copy the bot token
3. Get your chat ID: message @userinfobot
4. In n8n: replace the Gmail node with a **Telegram** node
5. Set: `Chat ID` = your chat ID, `Text` = `{{ $json['digest'] }}`

The Telegram message character limit (4096 chars) may truncate long digests —
if so, shorten the digest format in the Code node.

---

## What n8n Does vs What You Do

| Task | Who Does It |
|---|---|
| Read your Sheets CRM | n8n (automated) |
| Identify who needs follow-up today | n8n (automated) |
| Email you the digest | n8n (automated) |
| Write the follow-up emails | **You** (manual) |
| Send the follow-up emails | **You** (manual, in Gmail) |
| Update CRM after sending | **You** (manual, in Sheets) |
| Reply to leads | **You** (manual, in Gmail) |
| Log replies in CRM | **You** (manual, in Sheets) |

The automation is a memory aid. The relationships are yours to build.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| No email arriving | Check the workflow is Active; check spam folder |
| "Not authenticated" error | Re-authorize Google credentials in n8n |
| Digest shows 0 leads even though Sheets has leads | Check that `Next Follow-Up Date` column has real dates (not text) |
| Digest shows the same leads every day | You need to update `Next Follow-Up Date` after you follow up |
| n8n not running at 8am | Set n8n to start on boot, or deploy to Railway/Render |
