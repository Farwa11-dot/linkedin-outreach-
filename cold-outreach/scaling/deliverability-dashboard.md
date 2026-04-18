# Deliverability Dashboard — Tracking & Monitoring Setup

How to measure inbox health without paid tools. All formulas run inside Google Sheets.

---

## The 5 Metrics That Matter

| Metric | Green | Yellow | Red | How to Measure |
|---|---|---|---|---|
| **Bounce Rate** | < 2% | 2–4% | > 4% | Sent Log ÷ total sends |
| **Reply Rate** | > 2% | 1–2% | < 1% | Sheets reply count ÷ sends |
| **Spam Complaints** | 0 | 1 in 14 days | 1 in 7 days | Manual Gmail check |
| **mail-tester Score** | ≥ 8/10 | 6–7/10 | < 6/10 | Weekly test |
| **Inbox Placement** | Inbox | — | Spam | Weekly delivery test |

---

## Google Sheets Dashboard Setup

### Sheet: `Dashboard` (add this tab to your CRM)

**Section 1 — System-Wide Stats (Row 1–15)**

| Cell | Label | Formula |
|---|---|---|
| B2 | Total Sends (All Time) | `=COUNTA(SentLog!A:A)-1` |
| B3 | Total Sends (Last 7 Days) | `=COUNTIFS(SentLog!A:A,">="&TODAY()-7,SentLog!H:H,"sent")` |
| B4 | Total Bounces (Last 7 Days) | `=COUNTIFS(SentLog!A:A,">="&TODAY()-7,SentLog!H:H,"bounced")` |
| B5 | Bounce Rate % (7-day) | `=IFERROR(B4/B3*100,0)` |
| B6 | Total Replies (All Time) | `=COUNTIF(Leads!T:T,"yes")` |
| B7 | Reply Rate % (of all sends) | `=IFERROR(B6/B2*100,0)` |
| B8 | Leads in Sequence | `=COUNTIFS(Leads!O:O,"emailed-step1")+COUNTIFS(Leads!O:O,"emailed-step2")` |
| B9 | Meetings Booked | `=COUNTIF(Leads!O:O,"booked")` |
| B10 | Sequence Complete | `=COUNTIF(Leads!O:O,"emailed-step3")` |
| B11 | Do Not Contact | `=COUNTIF(Leads!X:X,TRUE)` |

**Section 2 — Per-Inbox Stats (Row 18–35)**

Create this block for each inbox (Inbox 1–5):

| Cell | Label | Formula (for Inbox 1) |
|---|---|---|
| C19 | Inbox 1 Sends (7-day) | `=COUNTIFS(SentLog!F:F,"inbox1",SentLog!A:A,">="&TODAY()-7)` |
| C20 | Inbox 1 Bounces (7-day) | `=COUNTIFS(SentLog!F:F,"inbox1",SentLog!H:H,"bounced",SentLog!A:A,">="&TODAY()-7)` |
| C21 | Inbox 1 Bounce Rate | `=IFERROR(C20/C19*100,0)` |
| C22 | Inbox 1 Status | `=IF(C21>4,"🔴 RED",IF(C21>2,"🟡 YELLOW","🟢 GREEN"))` |

Repeat for inbox2, inbox3, inbox4, inbox5 in rows below.

**Section 3 — Weekly Trend (Row 40–60)**

Track week-over-week in a table:

| Column A | Column B | Column C | Column D | Column E |
|---|---|---|---|---|
| Week | Sends | Bounces | Bounce % | Reply % |
| Apr 7 | 140 | 2 | 1.4% | 2.1% |
| Apr 14 | 180 | 3 | 1.7% | 1.8% |

Fill this manually every Monday morning (5 min). Visual trend matters.

**Conditional Formatting for Dashboard:**

Apply to all `Status` cells and rate cells:
- Value > 4 (bounce) → Red fill, white text
- Value 2–4 (bounce) → Orange fill, black text
- Value < 2 (bounce) → Green fill, black text

---

## Weekly Health Check Workflow (10 Minutes Every Friday)

### Step 1: Run mail-tester.com (2 min)

1. Go to [mail-tester.com](https://mail-tester.com)
2. Copy the unique test email address shown on screen
3. From Inbox 1, send a cold email draft to that address (use your current Step 1 template)
4. Return to mail-tester → Check Your Score
5. Screenshot or log the score in your Dashboard sheet
6. Repeat for each inbox (each inbox gets its own unique test address)

**What mail-tester checks:**
- SPF validity
- DKIM signing
- DMARC policy
- Spam word analysis
- HTML quality (even for plain text)
- Blacklist status
- Server configuration

**Acting on mail-tester feedback:**
- "Spam words detected" → edit your email copy, remove flagged words
- "Not signed with DKIM" → Gmail handles this automatically; if flagged, your email may be going through a relay — stop that
- "Listed on blacklist" → your IP or Gmail's sending server is blacklisted — use a different inbox for now, Gmail usually resolves within days

### Step 2: Inbox Delivery Test (3 min)

Send a real email from each inbox to:
1. A personal Gmail account you control (different from sending inboxes)
2. An Outlook or Hotmail address you control
3. Optionally: a Yahoo address

**Check:**
- Did it land in Inbox or Spam?
- Was there any delay (> 5 min delivery time is a soft warning)?
- Does the email look right (no formatting breaks)?

Log results in Dashboard: Inbox / Spam / Delayed for each provider.

### Step 3: Pull Metrics from Sheets (3 min)

Open Dashboard tab → check:
- `B5` (Bounce Rate 7-day) — is it green?
- `B7` (Reply Rate) — trending up or down?
- Per-inbox status cells — any red or yellow?

### Step 4: Decision (2 min)

Using the scaling decision tree from `scaling-roadmap.md`:
- All green + 14 days since last increase → scale up
- Any yellow → hold
- Any red → trigger fallback protocol

---

## Blacklist Monitoring (Free)

Check if your sending IP is blacklisted (Gmail's servers can get listed):

**Free tools:**
- [mxtoolbox.com/blacklists](https://mxtoolbox.com/blacklists) — enter `gmail.com` or `smtp.gmail.com`
- [multirbl.valli.org](https://multirbl.valli.org) — comprehensive check

If Gmail's SMTP servers are listed on a specific RBL, there's nothing you can do directly —
Gmail typically gets delisted within 24–48 hours. The workaround is to send from a
different Gmail account (different sending IP pool) while waiting.

**Important:** You are not responsible for Gmail's server reputation. This rarely happens.
Blacklisting of your *content* is what you control. Focus on that.

---

## Tracking Open Rate Without Tracking Pixels

Cold email best practice is plain text — no tracking pixels.
But you can estimate open rates indirectly:

**Method 1: Reply Rate as Proxy**
- Industry benchmark: 10–30% open → 1–5% reply
- If you're seeing 2%+ reply rate, your open rate is likely healthy (15%+)
- If reply rate < 0.5%, either nobody's opening OR your copy converts poorly

**Method 2: Offer Response Test**
In Step 3 emails, add: "Reply 'yes' if you want the one-pager."
Count yes replies ÷ total Step 3 sends = engagement rate for opened-but-not-replied leads.

**Method 3: Occasional Link Test**
In Step 2 (not Step 1), include ONE link to a Google Doc or simple landing page.
Google Analytics (free) on that page tells you click-through count.
Click rate ÷ Step 2 sends = rough proxy for engagement.
(Remove the link after the test — don't leave links in cold emails permanently.)

---

## Red Flag Checklist — Check These If Metrics Decline

```
COPY ISSUES
[ ] Does the subject line contain any spam words? (see deliverability-rules.md list)
[ ] Is the email over 200 words?
[ ] Are there any links in Step 1?
[ ] Is there an image or attachment?
[ ] Does the footer include an unsubscribe instruction?

LIST QUALITY ISSUES
[ ] What % of recent bounces were from the same source? (Google Maps? Hunter?)
[ ] Are emails being sent to generic addresses like info@, admin@, contact@?
    (These go to shared inboxes — low engagement, higher spam rate)
[ ] When were these emails last verified?

SENDING BEHAVIOR ISSUES
[ ] Are sends going out with less than 3-minute gaps?
[ ] Are sends happening on weekends?
[ ] Are sends happening before 8am or after 6pm recipient time?
[ ] Is one inbox sending more than 20 cold emails in a single day?
[ ] Is the same domain receiving more than 1 email per week?

INFRASTRUCTURE ISSUES
[ ] Is n8n running on a residential IP or a known-clean IP?
[ ] Are Gmail credentials properly OAuth2 (not SMTP password)?
[ ] Has any inbox gone inactive (no real email activity in 7+ days)?
```
