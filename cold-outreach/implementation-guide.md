# Step-by-Step Implementation Guide

Complete setup from zero to sending in ~3–4 hours.

---

## Phase 1 — Gmail Account Setup (Day 1)

### Step 1: Create Sending Inboxes

Create **2–3 Gmail accounts** dedicated to outreach. Do NOT use your main personal Gmail.

Naming convention that looks human:
```
sarah.moran.outreach@gmail.com   ← too obvious, avoid
sarah.m.connects@gmail.com       ← better
```

For each account:
1. Go to [gmail.com](https://gmail.com) → create new account
2. Use a real-sounding first + last name
3. Add a profile photo (any professional headshot from Unsplash/This Person Doesn't Exist)
4. Fill in the "About" section if prompted

### Step 2: Configure Gmail Settings

In each account → Settings → General:
- **Send As**: Set display name to your real name + title  
  e.g. `Sarah Chen | Growth Advisor`
- **Vacation Responder**: OFF
- **Signature**: Add a simple 3-line signature (name, title, phone/LinkedIn)

In Settings → Filters and Blocked Addresses:
- Create a filter: `to:(your-sending-email)` → Never send to spam (for testing your own emails)

### Step 3: Enable Gmail API for n8n

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project: `ColdOutreach`
3. Enable these APIs:
   - Gmail API
   - Google Sheets API
4. Go to **Credentials** → Create OAuth 2.0 Client ID → Desktop App
5. Download the JSON credentials file
6. Repeat for each Gmail account (or use same OAuth app, add accounts as test users)

---

## Phase 2 — Google Sheets CRM Setup (Day 1)

### Step 4: Create the Master Spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com) → New spreadsheet
2. Name it: `Cold Outreach CRM — Clinics`
3. Create these sheets (tabs):
   - `Leads` — main tracking sheet
   - `Sent Log` — auto-logged by n8n
   - `Templates` — store your email templates
   - `Stats` — daily send counts

See `sheets/crm-template.md` for full column setup.

### Step 5: Protect the Spreadsheet

- Share with your Gmail sending accounts (Editor access)
- Lock the header row: Right-click row 1 → Protect range → Allow only you to edit

---

## Phase 3 — Lead Sourcing (Day 1–2, ongoing)

### Step 6: Find Leads via Google Maps

Search Google Maps for:
```
"dental clinic" New York NY
"dentist office" Austin TX
"med spa" Miami FL
"aesthetic clinic" Los Angeles CA
"cosmetic dentist" Chicago IL
```

For each result, collect:
- Business name
- Website URL
- Phone number
- Address
- Owner/contact name (check their website About page, Google Business profile)

### Step 7: Find Emails (Free Methods)

**Method A — Website scrape (manual)**
1. Go to their website
2. Check: Contact page, About page, footer
3. Look for: `hello@`, `info@`, `dr.name@`, `appointments@`

**Method B — Hunter.io free tier**
- [hunter.io](https://hunter.io) → 25 free searches/month
- Enter domain → get likely email format

**Method C — Google search operators**
```
site:theirdomain.com email
"@theirdomain.com" contact
"dental" "info@" "New York" filetype:pdf
```

**Method D — LinkedIn (free)**
- Search practice name → find owner/office manager
- Check their LinkedIn bio for contact info

### Step 8: Verify Emails Before Sending

Use [verify-email.org](https://verify-email.org) or [emailvalidation.io](https://emailvalidation.io) (free tiers) to validate addresses before loading into Sheets. This prevents bounces that hurt your sender score.

**Rule: Only send to emails with ≥ 80% confidence score.**

---

## Phase 4 — Email Warm-Up (Days 1–14, before cold outreach)

### Step 9: Manual Warm-Up Protocol

You MUST warm up new Gmail accounts before cold outreach. Skip this and you'll land in spam within days.

**Week 1 (Days 1–7):**
- Send 5 real, conversational emails per day from each account
- Email colleagues, friends, newsletters you subscribe to
- Reply to emails you receive
- Open emails, scroll, click links (simulate human behavior)
- Do NOT send any cold emails yet

**Week 2 (Days 8–14):**
- Increase to 10 real emails/day
- Start sending 3–5 cold emails/day manually (no automation yet)
- Check if any land in spam (send test to a Gmail account you control, check spam folder)

**Day 15+:**
- Begin automated sending at 10 emails/day per inbox
- Increase by 5/day each week until reaching 20/day max

**Free warm-up tool alternative:**
- [Mailwarm](https://mailwarm.com) — has a free tier (limited)
- Join warm-up networks manually: find other founders doing outreach and exchange warm-up emails

---

## Phase 5 — n8n Setup (Day 2–3)

### Step 10: Install n8n (Self-Hosted, Free)

**Option A — Local machine (simplest):**
```bash
# Requires Node.js 18+
npm install n8n -g
n8n start
# Opens at http://localhost:5678
```

**Option B — Docker (recommended for stability):**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Option C — Free cloud hosting:**
- [Railway.app](https://railway.app) — deploy n8n container, 500 free hours/month
- [Render.com](https://render.com) — free tier supports n8n

### Step 11: Import the Workflow

1. Open n8n at `http://localhost:5678`
2. Go to **Workflows** → **Import from File**
3. Upload `n8n/workflow.json` from this repo
4. Set credentials:
   - Google Sheets: OAuth2 (use the JSON from Step 3)
   - Gmail: OAuth2 (same credentials)
5. Update the **Google Sheets node** with your spreadsheet ID (from the URL)
6. Activate the workflow

### Step 12: Configure Sending Schedule

In n8n workflow → Schedule Trigger node:
- Set to: `0 9 * * 1-5` (9am Monday–Friday)
- Timezone: Your local timezone (or EST to match US business hours)

---

## Phase 6 — Go Live (Day 14+)

### Step 13: Load First Batch of Leads

1. Open your Google Sheets CRM
2. Paste 20–30 leads into the `Leads` tab
3. Set `Status` = `ready` for leads you want to send to
4. Set `Assigned Inbox` = `inbox1`, `inbox2`, or `inbox3`

### Step 14: Monitor First Sends

After n8n runs for the first time:
- Check `Sent Log` tab — entries should appear
- Go to your Gmail Sent folder — emails should be there
- Check that Sheets updated statuses to `emailed-step1`
- Wait 24 hours, then check: did any bounce? Any replies?

### Step 15: Daily Routine (10 min/day)

```
Morning:
  [ ] Check replies in Gmail — respond within 2 hours
  [ ] Review Sent Log for bounces — mark those leads "invalid"
  [ ] Add 10–20 new leads to Sheets with status "ready"

Weekly:
  [ ] Review stats tab — open rate proxy (replies / sends)
  [ ] Rotate email copy if reply rate < 2%
  [ ] Check spam rates (ask a friend to confirm your emails landed in inbox)
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Emails landing in spam | Slow down sends, check SPF/DMARC isn't missing, add plain-text version |
| Gmail account suspended | You exceeded limits or sent too fast — recover account, slow down significantly |
| n8n workflow not triggering | Check that workflow is "Active" (toggle in top right) |
| Google Sheets API error | Re-authorize OAuth credentials in n8n credentials panel |
| High bounce rate (> 5%) | Improve email verification step — use Hunter.io to validate |
| Low reply rate (< 1%) | Rewrite subject line and opening sentence; test different offer angles |
