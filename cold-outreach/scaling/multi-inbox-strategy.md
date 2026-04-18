# Multi-Inbox Strategy — 2 to 5 Gmail Accounts

How to structure, operate, and route sends across multiple inboxes
without burning any of them.

---

## Inbox Identity Design

Each inbox must feel like a real person — not a rotation slot.

### Naming Convention

Create a consistent persona per inbox:

| Inbox | Gmail Address | Display Name | Role Persona |
|---|---|---|---|
| Inbox 1 | `alex.chen.outreach@gmail.com` | Alex Chen | Growth Consultant |
| Inbox 2 | `jamie.r.connects@gmail.com` | Jamie Ross | Clinic Advisor |
| Inbox 3 | `morgan.hill.biz@gmail.com` | Morgan Hill | Practice Strategist |
| Inbox 4 | `taylor.m.growth@gmail.com` | Taylor Mills | Healthcare Consultant |
| Inbox 5 | `jordan.a.clinic@gmail.com` | Jordan Arce | Patient Growth Lead |

**Rules:**
- Use common, non-unusual names (no hyphens, no numbers)
- Don't use the word "outreach", "marketing", "sales" in the address
- Add a profile photo to each (royalty-free professional headshot from [thispersondoesnotexist.com](https://thispersondoesnotexist.com))
- Write a Gmail bio for each (Settings → About)

### Signature Per Inbox

Keep signatures minimal but consistent across all inboxes:

```
[FIRST NAME LAST NAME]
[Title — e.g., "Practice Growth Advisor"]
[Phone — optional]

Helping dental & aesthetic clinics grow without paid ads.
```

Do NOT include: company name, website URL, or social links in cold emails.
These are link signals that spam filters flag.

---

## Inbox Isolation Rules

**Each inbox is a standalone identity. Inboxes must NOT:**
- Email each other (cross-inbox traffic looks automated to Gmail)
- Send to the same domain twice in the same day
- Send to the same recipient from two different inboxes (ever)
- Share IP addresses when accessed via automation (n8n should use the same IP for all — this is fine; the risk is humans switching between accounts)

**Each inbox MUST:**
- Have its own Google Cloud OAuth credential
- Send from its own Gmail session in n8n
- Maintain its own real email activity (not just cold sends)
- Be checked/logged into manually at least 3x/week

---

## Lead-to-Inbox Assignment Strategy

### Strategy 1: Geographic Split (Recommended)

Assign leads by US region so each inbox "owns" a territory:

| Inbox | Region | States |
|---|---|---|
| Inbox 1 | Northeast | NY, NJ, CT, MA, PA |
| Inbox 2 | Southeast | FL, GA, NC, SC, VA |
| Inbox 3 | Midwest | IL, OH, MI, MN, WI |
| Inbox 4 | South/Central | TX, AZ, CO, NV |
| Inbox 5 | West Coast | CA, OR, WA |

**Why geographic:** If a recipient googles the sender, consistency matters.
A "clinic advisor in Miami" emailing a Florida dentist feels more local.

### Strategy 2: Clinic Type Split

| Inbox | Clinic Type |
|---|---|
| Inbox 1 & 2 | Dental (general + ortho) |
| Inbox 3 & 4 | Aesthetic / Med Spa |
| Inbox 5 | Cosmetic dentistry (overlap niche) |

### Strategy 3: Pipeline Stage Split (Advanced)

| Inbox | Usage |
|---|---|
| Inbox 1 & 2 | Cold Step 1 sends only |
| Inbox 3 & 4 | Follow-up Step 2 & 3 only |
| Inbox 5 | Warm leads + replies (conversation inbox) |

This prevents the "follow-up from a different name" problem — all follow-ups come from the same inbox as Step 1.

---

## Domain-Level Throttling

Even with multiple inboxes, never hammer the same domain:

**Rule:** Max 1 email per domain per 7 days, across ALL inboxes combined.

Example:
- `info@smilesdental.com` receives Step 1 from Inbox 1 on Monday
- No other inbox sends to `@smilesdental.com` until the following Monday
- If they have multiple contacts (e.g. `dr.smith@smilesdental.com`), still wait 7 days

**How to enforce in Sheets:**
Add a column `Last Contacted Domain Date` and a formula:
```
=IF(COUNTIF(SentLog!D:D,"*@"&MID(E2,FIND("@",E2)+1,100))>0,"contacted","clear")
```

---

## Reply Handling Across Multiple Inboxes

Replies come back to whichever inbox sent the email. This is correct.

**Setup:**
- In Gmail Settings → See all settings → Accounts → "Send mail as"
- Each inbox sends FROM itself and receives replies to itself
- Do NOT use a catch-all forwarding address — it confuses threading

**n8n reply detection (optional):**
Add a Gmail Trigger node in n8n for each inbox set to trigger on new emails
with label "Inbox". When a reply arrives → n8n updates Sheets `Reply Received` = yes,
`Reply Date` = today.

---

## Inbox Rotation Logic in n8n

### Simple: Column-Based Assignment

The `Assigned Inbox` column in Google Sheets controls which n8n Gmail credential sends.
n8n reads the column → switches to the correct Gmail node → sends.

```
Assigned Inbox = "inbox1" → Gmail node with credential "Gmail — Inbox 1"
Assigned Inbox = "inbox2" → Gmail node with credential "Gmail — Inbox 2"
...
```

See `n8n/workflow-multisend.json` for the Switch node implementation.

### Advanced: Auto-Assign Based on Capacity

If you want n8n to auto-assign inboxes (rather than manually setting in Sheets):

```javascript
// In a Code node before sending
const items = $input.all();
const inboxCounts = { inbox1: 0, inbox2: 0, inbox3: 0 };
const MAX = 20;

for (const item of items) {
  // Find inbox with lowest count
  const available = Object.entries(inboxCounts)
    .filter(([_, count]) => count < MAX)
    .sort(([_, a], [__, b]) => a - b);
    
  if (available.length === 0) break; // All inboxes full for today
  
  const [assignedInbox] = available[0];
  inboxCounts[assignedInbox]++;
  item.json['Assigned Inbox'] = assignedInbox;
}

return items.filter(i => i.json['Assigned Inbox']);
```

---

## Inbox Health Scorecard

Track per-inbox (add to Stats sheet):

| Metric | Inbox 1 | Inbox 2 | Inbox 3 | Inbox 4 | Inbox 5 |
|---|---|---|---|---|---|
| Sends (7-day) | | | | | |
| Bounces (7-day) | | | | | |
| Bounce rate % | | | | | |
| Replies received | | | | | |
| Spam complaints | | | | | |
| Last mail-tester score | | | | | |
| Status | 🟢 | 🟢 | 🟡 | 🟢 | 🔴 |

If any inbox goes Red → pause it immediately, do not route new sends to it.

---

## When to Retire an Inbox

If an inbox gets suspended by Google OR consistently scores below 6/10 on
mail-tester after re-warming, retire it:

1. Export all leads assigned to it from Sheets
2. Reassign them to a healthy inbox (in batches, not all at once)
3. Create a replacement inbox and begin warm-up
4. Do not delete the old account — keep it active with real email
   (some recipients may reply to old emails weeks later)

---

## Cost: $0 Breakdown

| Item | Cost |
|---|---|
| Gmail accounts (free tier) | $0 |
| Google Cloud API project | $0 (within free quotas) |
| n8n (self-hosted on local machine) | $0 |
| Profile photos (This Person Doesn't Exist) | $0 |
| **Total** | **$0/month** |

If you eventually want Google Workspace ($6/month/inbox) instead of free Gmail,
the sending limits increase to 2,000/day per account — but you still should
not cold send more than 50/day per inbox from a reputation standpoint.
The ROI of Workspace at 100/day volume is not worth it. Only consider at 300+/day.
