# Google Sheets CRM — Column Definitions & Setup

---

## Sheet 1: `Leads` (Main Tracking)

| Column | Header | Type | Values / Notes |
|---|---|---|---|
| A | `Lead ID` | Auto | e.g. `L001`, `L002` — set manually or via formula |
| B | `Business Name` | Text | Full clinic name as it appears on Google Maps |
| C | `Contact Name` | Text | Owner, office manager, or doctor name (first + last) |
| D | `First Name` | Text | For `{{first_name}}` in templates |
| E | `Email` | Text | Verified email address |
| F | `Phone` | Text | Optional — for reference |
| G | `Website` | URL | Their website URL |
| H | `City` | Text | e.g. `Austin`, `Miami` |
| I | `State` | Text | 2-letter code: `TX`, `FL` |
| J | `Clinic Type` | Dropdown | `dental` / `aesthetic` / `medSpa` / `orthodontics` |
| K | `Personalization Tag` | Text | One raw observation (see personalization-guide.md) |
| L | `Source` | Dropdown | `googleMaps` / `hunter` / `linkedin` / `referral` |
| M | `Email Verified` | Dropdown | `yes` / `no` / `unknown` |
| N | `Assigned Inbox` | Dropdown | `inbox1` / `inbox2` / `inbox3` |
| O | `Status` | Dropdown | See status values below |
| P | `Step 1 Sent Date` | Date | Auto-filled by n8n |
| Q | `Step 2 Sent Date` | Date | Auto-filled by n8n |
| R | `Step 3 Sent Date` | Date | Auto-filled by n8n |
| S | `Next Action Date` | Date | Auto-calculated by n8n |
| T | `Reply Received` | Dropdown | `yes` / `no` |
| U | `Reply Date` | Date | When they replied |
| V | `Reply Sentiment` | Dropdown | `positive` / `negative` / `neutral` / `unsubscribe` |
| W | `Notes` | Text | Free-form notes — manual entry only |
| X | `Do Not Contact` | Checkbox | Check if they unsubscribed or asked to stop |

---

## Status Values (Column O)

```
new            → lead added, not yet ready to send
ready          → approved for sending, n8n will pick this up
emailed-step1  → Step 1 sent, waiting for Step 2
emailed-step2  → Step 2 sent, waiting for Step 3
emailed-step3  → Step 3 sent, sequence complete
replied        → they responded — handle manually
booked         → call/meeting scheduled
not-interested → said no / not a fit
do-not-contact → unsubscribed or asked to stop
invalid-email  → bounced / email not valid
paused         → temporarily hold sending
```

---

## Status Flow Diagram

```
new
 │
 ▼ (you set it)
ready
 │
 ▼ (n8n triggers Step 1)
emailed-step1
 │
 ├─── reply received? ──► replied ──► booked / not-interested
 │
 ▼ (n8n triggers Step 2 at Day+3)
emailed-step2
 │
 ├─── reply received? ──► replied ──► booked / not-interested
 │
 ▼ (n8n triggers Step 3 at Day+7)
emailed-step3
 │
 ├─── reply received? ──► replied ──► booked / not-interested
 │
 ▼ (no reply)
[sequence complete — leave alone for 90 days]
```

---

## Sheet 2: `Sent Log`

Auto-populated by n8n. Do not edit manually.

| Column | Header | Notes |
|---|---|---|
| A | `Timestamp` | When n8n sent |
| B | `Lead ID` | Links back to Leads tab |
| C | `Business Name` | Copy from Leads |
| D | `Email` | Address sent to |
| E | `Step` | `1`, `2`, or `3` |
| F | `Inbox Used` | Which Gmail account sent it |
| G | `Subject` | Subject line used |
| H | `Status` | `sent` / `failed` / `bounced` |

---

## Sheet 3: `Templates`

Store your email templates here for easy editing without touching n8n.

| Column | Header | Notes |
|---|---|---|
| A | `Template ID` | e.g. `dental-step1`, `aesthetic-step2` |
| B | `Clinic Type` | `dental` or `aesthetic` |
| C | `Step` | `1`, `2`, or `3` |
| D | `Subject A` | First subject line variant |
| E | `Subject B` | Second subject line variant (A/B test) |
| F | `Body` | Full email body with `{{placeholders}}` |
| G | `Active` | Checkbox — only active templates are used |
| H | `Last Updated` | Date |

---

## Sheet 4: `Stats`

Manual or formula-driven weekly review.

| Column | Header | Formula Example |
|---|---|---|
| A | `Week` | `Week of Apr 14` |
| B | `Emails Sent` | `=COUNTIF(SentLog!H:H,"sent")` |
| C | `Bounces` | `=COUNTIF(SentLog!H:H,"bounced")` |
| D | `Replies Received` | `=COUNTIF(Leads!T:T,"yes")` |
| E | `Bounce Rate %` | `=C2/B2*100` |
| F | `Reply Rate %` | `=D2/B2*100` |
| G | `Meetings Booked` | `=COUNTIF(Leads!O:O,"booked")` |
| H | `Inbox 1 Sends` | `=COUNTIF(SentLog!F:F,"inbox1")` |
| I | `Inbox 2 Sends` | `=COUNTIF(SentLog!F:F,"inbox2")` |
| J | `Inbox 3 Sends` | `=COUNTIF(SentLog!F:F,"inbox3")` |

---

## Useful Google Sheets Formulas

### Flag leads ready for follow-up (Step 2):
```
=IF(AND(O2="emailed-step1", TODAY()-P2 >= 3, T2="no"), "SEND STEP 2", "")
```

### Flag leads ready for follow-up (Step 3):
```
=IF(AND(O2="emailed-step2", TODAY()-Q2 >= 4, T2="no"), "SEND STEP 3", "")
```

### Count leads by status:
```
=COUNTIF(O:O,"ready")
=COUNTIF(O:O,"emailed-step1")
=COUNTIF(O:O,"replied")
=COUNTIF(O:O,"booked")
```

### Conditional formatting setup:
- Status = `ready` → light blue
- Status = `emailed-step1` → yellow
- Status = `emailed-step2` → orange
- Status = `emailed-step3` → light gray
- Status = `replied` → green
- Status = `booked` → dark green
- Status = `do-not-contact` → red

---

## Data Validation Setup

For dropdown columns, set data validation:
1. Select column O (Status)
2. Data menu → Data Validation → List from range or List of items
3. Paste the comma-separated values

Do this for: Clinic Type, Source, Status, Assigned Inbox, Reply Received, Reply Sentiment.

---

## Quick-Entry Tips

- Use `Ctrl+;` to insert today's date in any cell
- Use `Ctrl+D` to copy the cell above down
- Freeze row 1: View → Freeze → 1 row
- Freeze column A: View → Freeze → 1 column
- Sort by `Next Action Date` to see what's due today
