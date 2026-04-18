# Google Sheets CRM — Setup Guide

One spreadsheet. Four tabs. Everything in one place.

---

## Create the Spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com) → New
2. Name it: `Outreach CRM — Clinics`
3. Create four tabs (click `+` at the bottom):
   - `Leads` — main pipeline
   - `Follow-Up Queue` — auto-filtered view of who needs contact today
   - `Call Log` — every touchpoint recorded
   - `Templates` — your email drafts, stored here for quick copy-paste

---

## Tab 1: `Leads`

This is your master pipeline. Every lead lives here permanently — even dead ones.

### Full Column List

**Block 1 — Identity (A–K)**

| Col | Field | Type | Notes |
|---|---|---|---|
| A | `Lead ID` | Text | Format: `L001`, `L002` — enter manually, never changes |
| B | `Business Name` | Text | Exact name from Google Maps / their website |
| C | `Industry` | Dropdown | `Dental` / `Aesthetic` / `Med Spa` / `Ortho` |
| D | `Contact Name` | Text | Owner, practice manager, or doctor |
| E | `First Name` | Text | Used in email salutation |
| F | `Email` | Text | Primary outreach email |
| G | `Phone` | Text | Useful if they call back or for HOT lead call attempt |
| H | `Website` | URL | Their website — check before every email |
| I | `City` | Text | City they operate in |
| J | `State` | Text | 2-letter state code |
| K | `Contact Source` | Dropdown | `Google Maps` / `Website` / `Referral` / `LinkedIn` |

**Block 2 — Research & Scoring (L–S)**

| Col | Field | Type | Notes |
|---|---|---|---|
| L | `Personalization Note` | Text | One specific, true observation — required before emailing |
| M | `Score: Ads` | Number | 0–2 — are they running Google or Facebook ads? |
| N | `Score: Service` | Number | 0–2 — how high-ticket is their service mix? |
| O | `Score: Urgency` | Number | 0–3 — count of urgency signals observed |
| P | `Score: Website` | Number | 0–2 — website quality and booking gap |
| Q | `Score: Contact` | Number | 0–1 — owner email vs generic inbox |
| R | `Lead Score` | Formula | `=IFERROR(SUM(M2:Q2),"")` — auto-calculates |
| S | `Priority Tier` | Formula | See formula below — auto-labels HOT/WARM/COOL/COLD |

**Block 3 — Pipeline Status (T–Z)**

| Col | Field | Type | Notes |
|---|---|---|---|
| T | `Status` | Dropdown | Full pipeline stage — see values below |
| U | `Initial Email Date` | Date | When Step 1 was sent |
| V | `Follow-Up 1 Date` | Date | When Step 2 was sent |
| W | `Follow-Up 2 Date` | Date | When Step 3 was sent |
| X | `Follow-Up 3 Date` | Date | When breakup email was sent |
| Y | `Last Contact Date` | Date | Most recent outreach of any kind |
| Z | `Next Follow-Up Date` | Date | Drives the Follow-Up Queue tab — this is your to-do list |

**Block 4 — Reply Tracking (AA–AE)**

| Col | Field | Type | Notes |
|---|---|---|---|
| AA | `Reply Received` | Checkbox | Check the moment any reply arrives |
| AB | `Reply Date` | Date | When they replied |
| AC | `Reply Type` | Dropdown | `Positive` / `Not Now` / `Not Interested` / `Info Request` / `Auto-Reply` / `Unsubscribe` |
| AD | `Reply Summary` | Text | One sentence — what did they say? |
| AE | `Meeting Date` | Date | Confirmed call or demo date |

**Block 5 — Outcome & Notes (AF–AG)**

| Col | Field | Type | Notes |
|---|---|---|---|
| AF | `Outcome` | Dropdown | `In Progress` / `Booked` / `Not Interested` / `Park 90 Days` / `Do Not Contact` |
| AG | `Notes` | Text | Call notes, objections raised, context — free form |

---

### Formulas for Auto-Calculated Columns

**Lead Score (column R):**
```
=IFERROR(SUM(M2:Q2),"")
```

**Priority Tier (column S):**
```
=IF(R2="","",
  IF(R2>=8,   "🔴 HOT",
  IF(R2>=5.5, "🟠 WARM",
  IF(R2>=3,   "🟡 COOL",
              "⚪ COLD"))))
```

Copy these formulas down for every row that has a Lead ID.

---

### Status Dropdown Values

Set data validation on column T. Full pipeline:

```
New Lead
Contacted
Follow-Up 1 Sent
Follow-Up 2 Sent
Follow-Up 3 Sent
Replied
Call Scheduled
Qualified
Demo Held
Closing
Booked
Not Interested
Lost
Park - 90 Days
Park - 60 Days
Do Not Contact
```

### Setting Up Data Validation

1. Click the column header to select the whole column
2. **Data** menu → **Data Validation** → **Add Rule**
3. Criteria: **Dropdown** → type each value, one per line
4. Click **Done**

Apply dropdowns to: `C` (Industry), `K` (Contact Source), `T` (Status),
`AC` (Reply Type), `AF` (Outcome).

### Conditional Formatting — Status Column (Column T)

Select column T → **Format** → **Conditional Formatting**:

| Status | Background Color |
|---|---|
| New Lead | White |
| Contacted | Light blue (#cfe2ff) |
| Follow-Up 1/2/3 Sent | Yellow (#fff2cc) |
| Replied | Light green (#d9ead3) |
| Call Scheduled | Teal (#a2c4c9) |
| Qualified | Green (#b6d7a8) |
| Demo Held | Dark green (#6aa84f), white text |
| Closing | Orange (#f9cb9c) |
| Booked | Dark green (#274e13), white text |
| Not Interested | Light red (#f4cccc) |
| Lost | Gray (#efefef) |
| Park - 90 Days | Purple (#d9d2e9) |
| Do Not Contact | Dark red (#cc0000), white text |

### Conditional Formatting — Priority Tier Column (Column S)

Select column S → **Format** → **Conditional Formatting**:

| Text Contains | Background | Text |
|---|---|---|
| `🔴 HOT` | Red (#ea4335) | White, Bold |
| `🟠 WARM` | Orange (#ff9900) | Black |
| `🟡 COOL` | Yellow (#fbbc04) | Black |
| `⚪ COLD` | Light gray (#f3f3f3) | Gray |

### The Personalization Note Column (Column L)

This is the most important column in the CRM. Fill it in before you email — not after.

Good examples:
```
"No online booking button on Google profile"
"4.2 stars — no response to any reviews"
"Website looks broken on mobile"
"Closed on weekends — missing patient bookings"
"No referral program mentioned anywhere on site"
"Only 11 Google reviews despite being open 8 years"
"Instagram active but Google Business has 0 posts in 6 months"
```

Bad examples (these tell you nothing specific):
```
"Nice clinic"
"Dental practice in Miami"
"Could use more patients"
```

Rule: if you cannot fill in column L with something specific and true, do more research before emailing.

---

## Tab 2: `Follow-Up Queue`

A filtered view showing leads due for contact today, sorted by priority tier.
HOT leads always appear at the top. This is your morning to-do list.

### Setup

1. Click on the `Follow-Up Queue` tab
2. In cell A1, enter this header: `Today's Priority Queue`
3. In cell B1: `=COUNTA(A4:A10000) & " actions due today"`
4. In cell A3, paste this formula:

```
=SORT(
  FILTER(
    Leads!A:AG,
    (Leads!Z:Z <= TODAY()) *
    (Leads!Z:Z <> "") *
    (Leads!AA:AA = FALSE) *
    (Leads!T:T <> "Booked") *
    (Leads!T:T <> "Not Interested") *
    (Leads!T:T <> "Lost") *
    (Leads!T:T <> "Park - 90 Days") *
    (Leads!T:T <> "Park - 60 Days") *
    (Leads!T:T <> "Do Not Contact")
  ),
  18, TRUE
)
```

Column 18 is the Lead Score column (R) — this sorts highest score to the top
so HOT leads always surface first.

This pulls every lead where:
- `Next Follow-Up Date` (col Z) is today or overdue
- No reply received (col AA checkbox unchecked)
- Status is not a terminal/closed state

Every morning, open this tab first. Work top to bottom.

### Add a Count Summary in B1

```
=COUNTA(A4:A1000) & " follow-ups due today"
```

---

## Tab 3: `Call Log`

Every touchpoint gets logged here. One row per action.

### Columns

| Col | Field | Notes |
|---|---|---|
| A | `Date` | When this happened |
| B | `Lead ID` | Links back to Leads tab |
| C | `Business Name` | Copy from Leads |
| D | `Action Type` | `Email Sent` / `Reply Received` / `Call Made` / `Meeting Held` / `Note Added` |
| E | `Step` | `Initial` / `Follow-Up 1` / `Follow-Up 2` / `Follow-Up 3` / `Reply` |
| F | `Subject Line Used` | Copy the subject from your email |
| G | `Notes` | What happened / what you said / what they said |

**Why log everything?**
In 6 weeks you will not remember that you emailed Dr. Martinez on March 14th
and he asked you to follow up after tax season. The Call Log tells you.
It also gives you a real count of your activity — not vanity metrics, but
actual touchpoints.

### Auto-Populate Date

In column A, press `Ctrl+;` to insert today's date quickly.

---

## Tab 4: `Templates`

Store your live email templates here for fast copy-paste.

### Columns

| Col | Field |
|---|---|
| A | `Template Name` |
| B | `Step` |
| C | `Industry Target` |
| D | `Subject Line` |
| E | `Body` |
| F | `Last Revised` |

Store your Step 1, Step 2, and Step 3 templates here.
When you sit down to email, copy the body, paste into Gmail,
then personalize the `{{placeholders}}` before sending.

---

## Quick-Entry Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+;` | Insert today's date |
| `Ctrl+D` | Copy cell above down |
| `Ctrl+Shift+V` | Paste values only (no formatting) |
| `Ctrl+F` | Find a lead by name |
| `Alt+I, R` | Insert a new row above |

---

## Weekly Maintenance (5 Minutes Every Monday)

```
[ ] Count leads by status — are enough moving through the pipeline?
[ ] Any "Park - 90 Days" leads whose park date has passed? Reactivate them.
[ ] Any leads with Next Follow-Up Date more than 14 days overdue? 
    Decision: email them or mark Lost.
[ ] Check Booked leads — did the meeting happen? Update outcome.
[ ] Add to Notes column: any context you remember that isn't logged yet.
```

---

## Spreadsheet Sharing

Share the spreadsheet with:
- Your own Gmail sending accounts (if you have more than one) — Viewer access
- Nobody else

Do not share with clients. Do not link it publicly. It contains contact data.
