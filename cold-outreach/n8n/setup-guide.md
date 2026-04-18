# n8n Workflow Setup Guide

Step-by-step instructions to get both workflows running.

---

## Files

- `workflow.json` — Step 1 (initial outreach), runs at 9am Mon–Fri
- `workflow-followup.json` — Steps 2 & 3 (follow-ups), runs at 10am Mon–Fri

---

## Before You Import

You need these credentials ready in n8n:
1. **Google Sheets OAuth2** — connected to your CRM spreadsheet
2. **Gmail OAuth2** — one credential per sending inbox (inbox1, inbox2, inbox3)

---

## Step 1: Add Google Credentials to n8n

1. Open n8n → **Credentials** (left sidebar) → **Add Credential**
2. Search: `Google Sheets OAuth2 API`
3. Click **Connect with Google** → sign in with the Google account that owns the Sheets
4. Name it: `Google Sheets — CRM`
5. Save

Repeat for each Gmail sending account:
1. Add Credential → `Gmail OAuth2 API`
2. Connect with Google → sign in with your **sending** Gmail (inbox1)
3. Name it: `Gmail — Inbox 1`
4. Save
5. Repeat for `Gmail — Inbox 2`, `Gmail — Inbox 3`

---

## Step 2: Get Your Spreadsheet ID

From your Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_IS_HERE/edit
```
Copy the ID between `/d/` and `/edit`.

---

## Step 3: Import workflow.json

1. n8n → **Workflows** → **Import from File**
2. Upload `workflow.json`
3. Open each node and update:

| Node | What to update |
|---|---|
| `Read Leads from Google Sheets` | Set `documentId` to your spreadsheet ID; select credential `Google Sheets — CRM` |
| `Log Send to Google Sheets` | Same spreadsheet ID |
| `Update Lead Status in Google Sheets` | Same spreadsheet ID |
| `Send via Gmail` | Select credential `Gmail — Inbox 1`; set replyTo to your reply-to address |
| `Build Personalized Email` | Replace `[YOUR NAME]`, `[YOUR TITLE]`, `[YOUR PHONE]` in the code |

4. Click **Save**
5. Toggle **Active** (top right) to ON

---

## Step 4: Import workflow-followup.json

Same process as Step 3. This workflow handles Steps 2 and 3.

For multi-inbox sending in follow-ups, you can duplicate the `Send via Gmail` node
and use n8n's **Switch** node to route based on `Assigned Inbox` column value.

---

## Step 5: Test Before Going Live

1. Add one test lead to Sheets with:
   - A real email address you control
   - Status = `ready`
   - Assigned Inbox = `inbox1`
   - Clinic Type = `dental`
   - First Name = `Test`
   - Personalization Tag = `you have fewer than 10 Google reviews`

2. In n8n → open `workflow.json` → click **Execute Workflow** (manual trigger)

3. Check:
   - Did the email arrive in your inbox?
   - Did the Sent Log update?
   - Did the Lead status change to `emailed-step1`?

If yes → you're ready to go live.

---

## Step 6: Multi-Inbox Routing (Optional Enhancement)

To route sends to different Gmail accounts based on `Assigned Inbox`:

1. After the `Build Personalized Email` node, add a **Switch** node
2. Set Switch rules:
   - Value = `{{ $json['Assigned Inbox'] }}`
   - Case 1: `inbox1` → route to Gmail node with Inbox 1 credential
   - Case 2: `inbox2` → route to Gmail node with Inbox 2 credential
   - Case 3: `inbox3` → route to Gmail node with Inbox 3 credential
3. Each Gmail node has a different OAuth credential but the same template

---

## Monitoring & Alerts (Optional)

Add a **Telegram** or **Email** notification at the end of each workflow run:

1. Add a **Telegram** node (free bot) at the end of the chain
2. Message: `Outreach run complete: {{ $node['Filter: Status = ready'].outputItems.length }} emails sent today`

Or use **Gmail** to email yourself a daily summary — just another Gmail node pointed at your personal inbox.

---

## Troubleshooting

| Error | Fix |
|---|---|
| `401 Unauthorized` on Google Sheets | Re-authorize credential in n8n Credentials panel |
| `403 Forbidden` on Gmail | Gmail API not enabled in Google Cloud Console — check Step 3 in implementation-guide.md |
| Workflow runs but no emails sent | Check Filter node — leads may not match `Status = ready` |
| `Quota exceeded` error | You hit Google API rate limits — add longer delays between API calls |
| n8n crashes | Memory issue on small VPS — upgrade to 1GB RAM minimum |
