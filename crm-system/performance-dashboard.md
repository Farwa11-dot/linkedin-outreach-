# Performance Dashboard — Google Sheets Tracking System

What gets measured gets improved. This dashboard tells you what's working,
what isn't, and where to spend your time next week.

All metrics live in Google Sheets. No paid analytics tools required.

---

## Dashboard Architecture

```
Spreadsheet: "Outreach CRM — Clinics"
│
├── Tab: Leads           ← source of truth for all lead data
├── Tab: Call Log        ← source of truth for all activity data
├── Tab: Follow-Up Queue ← filtered view (operational)
├── Tab: Templates       ← email copy storage
└── Tab: Dashboard       ← everything below lives here
    │
    ├── Section 1: Weekly Snapshot    (top-level health)
    ├── Section 2: Funnel Metrics     (stage-by-stage conversion)
    ├── Section 3: Niche Breakdown    (dental vs aesthetic)
    ├── Section 4: City/Market View   (which markets convert)
    ├── Section 5: Subject Line Tracker (what copy is working)
    └── Section 6: Weekly History Log (trend over time)
```

---

## Tab: `Dashboard` — Full Setup

### Section 1 — Weekly Snapshot (Rows 1–14)

Place this block in the top-left of the Dashboard tab.
It gives you a complete picture in 30 seconds every Monday morning.

| Row | Label | Formula | Notes |
|---|---|---|---|
| 1 | **WEEKLY SNAPSHOT** | (header) | |
| 2 | Week of | (manual entry) | e.g. `Apr 14 – Apr 18` |
| 3 | New Leads Added | `=COUNTIFS(Leads!N:N,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),DAY(TODAY())-7), Leads!N:N,"<="&TODAY())` | Leads where Initial Email Date is in last 7 days |
| 4 | Initial Emails Sent | `=COUNTIFS(CallLog!D:D,"Email Sent", CallLog!E:E,"Initial", CallLog!A:A,">="&TODAY()-7)` | |
| 5 | Follow-Ups Sent | `=COUNTIFS(CallLog!D:D,"Email Sent", CallLog!A:A,">="&TODAY()-7) - B4` | Total email sends minus initial |
| 6 | Total Replies | `=COUNTIFS(Leads!U:U,">="&TODAY()-7)` | Reply Date in last 7 days |
| 7 | Reply Rate % | `=IFERROR(B6/B4*100,0)&"%"` | Replies ÷ initial emails |
| 8 | Calls Booked | `=COUNTIFS(Leads!V:V,">="&TODAY()-7, Leads!Z:Z,"Booked")` | Meeting Date set in last 7 days |
| 9 | Call-to-Book Rate % | `=IFERROR(B8/B6*100,0)&"%"` | Bookings ÷ replies |
| 10 | Active Pipeline | `=COUNTIFS(Leads!N:N,"<>", Leads!T:T,FALSE, Leads!N:N,"<>Not Interested", Leads!N:N,"<>Lost")` | Leads in active sequence |
| 11 | HOT Leads Active | `=COUNTIF(Leads!S:S,"🔴 HOT")` | |
| 12 | WARM Leads Active | `=COUNTIF(Leads!S:S,"🟠 WARM")` | |
| 13 | Deals Closed (MTD) | `=COUNTIFS(Leads!Z:Z,"Booked", Leads!V:V,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))` | Month-to-date closes |
| 14 | Avg Days Lead→Close | (see formula below) | |

**Avg Days Lead→Close formula (B14):**
```
=IFERROR(
  AVERAGEIFS(
    Leads!V:V - Leads!N:N,
    Leads!Z:Z, "Booked"
  ),
"Not enough data")
```
Where V = Meeting Date, N = Initial Email Date. Adjust column refs to match your sheet.

---

### Section 2 — Funnel Metrics (Rows 17–32)

The conversion funnel. Every stage has a count and a conversion rate from the stage above.

| Row | Stage | Count Formula | Conv. Rate |
|---|---|---|---|
| 18 | Leads Sourced (all time) | `=COUNTA(Leads!A:A)-1` | 100% |
| 19 | Contacted (Step 1 sent) | `=COUNTIF(Leads!N:N,"<>")` | `=B19/B18*100&"%"` |
| 20 | Replied | `=COUNTIF(Leads!T:T,TRUE)` | `=B20/B19*100&"%"` |
| 21 | Qualified (call booked) | `=COUNTIFS(Leads!Z:Z,"<>", Leads!Z:Z,"<>Not Interested", Leads!Z:Z,"<>Lost")` | `=B21/B20*100&"%"` |
| 22 | Demo Held | `=COUNTIF(Leads!N:N,"Demo Held")` | `=B22/B21*100&"%"` |
| 23 | Closed Won | `=COUNTIF(Leads!Z:Z,"Booked")` | `=B23/B22*100&"%"` |
| 24 | Not Interested | `=COUNTIF(Leads!N:N,"Not Interested")` | — |
| 25 | Parked | `=COUNTIFS(Leads!N:N,"Park*")` | — |

**Reading this funnel:**
- If Contacted→Replied rate is below 3%: email copy problem
- If Replied→Qualified rate is below 25%: discovery call conversion problem
- If Qualified→Demo rate is below 60%: scheduling or no-show problem
- If Demo→Closed rate is below 30%: pricing, objections, or demo quality problem

Each of these points you at a specific part of the system to fix.

---

### Section 3 — Niche Breakdown (Rows 35–48)

Side-by-side comparison of dental vs aesthetic performance.

**Header row (Row 35):** | Metric | Dental | Aesthetic | Med Spa |

| Row | Metric | Dental Formula | Aesthetic Formula |
|---|---|---|---|
| 36 | Total Leads | `=COUNTIF(Leads!C:C,"Dental")` | `=COUNTIF(Leads!C:C,"Aesthetic")` |
| 37 | Contacted | `=COUNTIFS(Leads!C:C,"Dental",Leads!N:N,"<>")` | `=COUNTIFS(Leads!C:C,"Aesthetic",Leads!N:N,"<>")` |
| 38 | Replied | `=COUNTIFS(Leads!C:C,"Dental",Leads!T:T,TRUE)` | `=COUNTIFS(Leads!C:C,"Aesthetic",Leads!T:T,TRUE)` |
| 39 | Reply Rate % | `=IFERROR(C38/C37*100,0)&"%"` | `=IFERROR(D38/D37*100,0)&"%"` |
| 40 | Calls Booked | `=COUNTIFS(Leads!C:C,"Dental",Leads!Z:Z,"Booked")` | `=COUNTIFS(Leads!C:C,"Aesthetic",Leads!Z:Z,"Booked")` |
| 41 | Close Rate % | `=IFERROR(C40/C38*100,0)&"%"` | `=IFERROR(D40/D38*100,0)&"%"` |
| 42 | Avg Lead Score | `=AVERAGEIF(Leads!C:C,"Dental",Leads!R:R)` | `=AVERAGEIF(Leads!C:C,"Aesthetic",Leads!R:R)` |

**What to look for:** If one niche replies at 2x the rate of the other,
double down on that niche. Do not split your effort evenly if the data
says one outperforms the other.

---

### Section 4 — City / Market View (Rows 52–70)

Which cities are converting? Which are dead weight?

**Setup:** Manual table. Add a row per city you're actively targeting.

| Col A | Col B | Col C | Col D | Col E | Col F |
|---|---|---|---|---|---|
| City | Leads | Contacted | Replied | Reply Rate | Booked |
| Miami, FL | `=COUNTIF(Leads!I:I,"Miami")` | `=COUNTIFS(Leads!I:I,"Miami",Leads!N:N,"<>")` | `=COUNTIFS(Leads!I:I,"Miami",Leads!T:T,TRUE)` | `=E53/D53*100&"%"` | `=COUNTIFS(Leads!I:I,"Miami",Leads!Z:Z,"Booked")` |
| Austin, TX | (same pattern) | | | | |
| Chicago, IL | (same pattern) | | | | |

Add a row for each city you've worked. Sort by Reply Rate descending.

**Decision rule:** After 30+ leads per city, a city with < 2% reply rate
gets deprioritized. A city with > 5% reply rate gets more leads sourced immediately.

Markets are not equal. Find where your offer resonates most, then concentrate there.

---

### Section 5 — Subject Line Tracker (Rows 74–95)

The most actionable data in the whole dashboard. Which subject lines drive replies.

**Setup:** Every time you send a batch of emails with a specific subject line,
log it here manually.

| Col A | Col B | Col C | Col D | Col E | Col F |
|---|---|---|---|---|---|
| Subject Line | Industry | Sends | Replies | Reply Rate % | Notes |
| `quick question for {{first_name}}` | Dental | 45 | 4 | 8.9% | Strong opener |
| `missed calls at {{clinic_name}}` | Dental | 30 | 1 | 3.3% | Too direct |
| `{{first_name}} — something I noticed` | Aesthetic | 28 | 5 | 17.9% | Best performer |
| `quick idea for {{clinic_name}}` | Aesthetic | 22 | 2 | 9.1% | Decent |

**Reply Rate % formula:** `=D75/C75*100`

**Conditional formatting:** Apply to Reply Rate column:
- ≥ 10%: green background
- 5–9.9%: yellow
- < 5%: red

**Rule:** Run each subject line for a minimum of 20 sends before drawing conclusions.
One batch of 5 emails is not data. Twenty sends is a sample.

**Acting on data:** If a subject line is below 5% after 25+ sends, retire it.
Write two new variants. Run them for 3 weeks. Repeat.

---

### Section 6 — Weekly History Log (Rows 99–onward)

A rolling manual log. Fill in one row every Monday. Reveals trends over time.

| Col | Header |
|---|---|
| A | Week |
| B | Leads Added |
| C | Emails Sent |
| D | Replies |
| E | Reply Rate % |
| F | Calls Booked |
| G | Closed |
| H | HOT Leads in Pipeline |
| I | Best Subject Line This Week |
| J | Best City This Week |
| K | Notes / What Changed |

This becomes your business journal. In month 3, you will look back at Week 1
and see exactly how far things have moved — and why.

---

## Metric Benchmarks: What Good Looks Like

Use these as calibration, not targets to chase blindly.

| Metric | Struggling | Acceptable | Strong |
|---|---|---|---|
| Reply Rate (cold email) | < 2% | 3–6% | > 8% |
| Reply→Qualified Rate | < 20% | 25–40% | > 50% |
| Qualified→Demo Rate | < 50% | 60–75% | > 80% |
| Demo→Close Rate | < 20% | 30–50% | > 60% |
| Overall Lead→Close | < 0.5% | 1–3% | > 4% |
| Avg Days to Close | > 45 days | 20–35 days | < 20 days |

**The most important single metric:** Reply Rate. Everything else is downstream of it.
If your reply rate is high but close rate is low, the offer or call needs work.
If your reply rate is low, nothing else matters until you fix copy and targeting.

---

## Weekly Dashboard Routine (10 Minutes Every Monday)

```
1. Fill in Section 6 (Weekly History) — one new row, all columns (5 min)

2. Read Section 1 (Weekly Snapshot) — any metric moving in the wrong direction?

3. Check Section 3 (Niche Breakdown) — is one niche pulling ahead? Lean into it.

4. Check Section 4 (City View) — any city hitting > 5% reply rate? Source more there.

5. Check Section 5 (Subject Lines) — is any subject line ready to retire (25+ sends, < 5%)?
   Write a replacement variant if so.

6. One action decision: what is the ONE thing to change or double down on this week?
   Write it in the Notes column of Section 6. Hold yourself to it.
```

Total time: 10 minutes. The discipline of a weekly review compounds over months.
