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

| Col | Field | Type | Notes |
|---|---|---|---|
| A | `Lead ID` | Text | Format: `L001`, `L002` — enter manually, never changes |
| B | `Business Name` | Text | Exact name from Google Maps / their website |
| C | `Industry` | Dropdown | `Dental` / `Aesthetic` / `Med Spa` / `Ortho` |
| D | `Contact Name` | Text | Owner, practice manager, or doctor — whoever you're emailing |
| E | `First Name` | Text | Used in email salutation |
| F | `Email` | Text | Primary outreach email |
| G | `Phone` | Text | Optional — useful if they call back |
| H | `Website` | URL | Their website — check it before you email |
| I | `City` | Text | City they operate in |
| J | `State` | Text | 2-letter state code |
| K | `Contact Source` | Dropdown | `Google Maps` / `Website` / `Referral` / `LinkedIn` |
| L | `Personalization Note` | Text | One real observation about their business (see below) |
| M | `Status` | Dropdown | Pipeline stage — see values below |
| N | `Initial Email Date` | Date | When Step 1 was sent |
| O | `Follow-Up 1 Date` | Date | When Step 2 was sent (Day 2) |
| P | `Follow-Up 2 Date` | Date | When Step 3 was sent (Day 5) |
| Q | `Follow-Up 3 Date` | Date | When Step 4 was sent (Day 10) |
| R | `Last Contact Date` | Date | Most recent outreach of any kind |
| S | `Next Follow-Up Date` | Date | When to contact next — this drives your daily queue |
| T | `Reply Received` | Checkbox | Check when any reply comes in |
| U | `Reply Date` | Date | When they replied |
| V | `Reply Summary` | Text | One sentence: what they said |
| W | `Meeting Date` | Date | If booked — when is the call/meeting |
| X | `Outcome` | Dropdown | `In Progress` / `Booked` / `Not Interested` / `Park 90 Days` |
| Y | `Notes` | Text | Anything else — call notes, things they mentioned, context |

### Status Dropdown Values

Set these as data validation on column M:

```
New Lead
Contacted
Follow-Up 1 Sent
Follow-Up 2 Sent
Follow-Up 3 Sent
Replied
Interested
Booked
Not Interested
Lost
Park - 90 Days
```

### Setting Up Data Validation

1. Click column M header to select all of column M
2. **Data** menu → **Data Validation** → **Add Rule**
3. Criteria: **Dropdown** → type each status value, one per line
4. Click **Done**

Repeat for columns C (Industry), K (Contact Source), X (Outcome).

### Conditional Formatting — Color Code Your Pipeline

Select column M → **Format** → **Conditional Formatting**:

| Status | Background Color |
|---|---|
| New Lead | White |
| Contacted | Light blue (#cfe2ff) |
| Follow-Up 1/2/3 Sent | Yellow (#fff2cc) |
| Replied | Light green (#d9ead3) |
| Interested | Green (#b6d7a8) |
| Booked | Dark green (#93c47d) |
| Not Interested | Light red (#f4cccc) |
| Lost | Gray (#efefef) |
| Park - 90 Days | Purple (#d9d2e9) |

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

A filtered view that shows only leads where `Next Follow-Up Date` = today or earlier, and the lead hasn't replied yet.

### Setup

1. Click on the `Follow-Up Queue` tab
2. In cell A1, enter this header: `Today's Follow-Ups`
3. In cell A3, paste this formula:

```
=FILTER(
  Leads!A:Y,
  (Leads!S:S <= TODAY()) *
  (Leads!S:S <> "") *
  (Leads!T:T = FALSE) *
  (Leads!M:M <> "Booked") *
  (Leads!M:M <> "Not Interested") *
  (Leads!M:M <> "Lost") *
  (Leads!M:M <> "Park - 90 Days")
)
```

This pulls every lead where:
- Next Follow-Up Date is today or overdue
- No reply has been received (checkbox unchecked)
- Status is not a closed/done state

Every morning, open this tab first. It is your to-do list.

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
