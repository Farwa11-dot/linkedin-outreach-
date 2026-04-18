# Priority System — Hot, Warm, Cold Lead Management

How to decide who gets your attention today, tomorrow, and next week.
A solo founder's time is the scarcest resource in this system.
Spend it where conversion probability is highest.

---

## The Three Tiers

```
🔴 HOT  (Score 8–10)  ──── Contact within 24h. Maximum effort. Call if needed.
🟠 WARM (Score 5.5–7.5) ── Contact within 72h. Full sequence. Standard effort.
🟡 COOL (Score 3–5)   ──── Contact this week if queue allows. Shorter research.
⚪ COLD (Score 0–2.5) ──── Park. Do not email now. Revisit in 60 days.
```

This is not about ignoring low-score leads forever. It is about sequencing.
When your queue is clear and HOT leads are handled, COOL leads get their turn.

---

## Hot Leads (Score 8–10): The 24-Hour Rule

A HOT lead is one where:
- Multiple urgency signals are visible (poor reviews, no booking button, after-hours gap)
- They are actively spending on ads (they already believe in patient acquisition ROI)
- You have a direct owner or decision-maker email
- Their service type makes each missed booking genuinely expensive

**Treatment:**

| Action | Timing |
|---|---|
| Email (Step 1) | Within 24 hours of scoring |
| Follow-Up 1 | Day 2 — do not wait until Day 3 |
| Follow-Up 2 | Day 4 |
| Call attempt (if no reply) | Day 5 — call the number on Google Maps |
| Final breakup email | Day 8 |
| Park | Day 9 |

**The Day 5 Call:** For HOT leads only, make a phone call before sending the breakup email.
```
"Hi, is this [clinic name]? Could I speak with [contact name] for a moment?
I sent a couple of emails over the past week about patient inquiry handling —
I wanted to make sure it didn't get buried. Do you have 2 minutes?"
```
If they answer: great. If not: leave a brief voicemail — 20 seconds maximum. Then
send the breakup email the same day. Log both attempts in the Call Log.

**In CRM:** HOT leads should always be at the top of your sorted Leads view.
Never let a HOT lead sit in "New Lead" status for more than 24 hours.

---

## Warm Leads (Score 5.5–7.5): Standard Sequence

A WARM lead has real potential but fewer urgent signals or a lower-value service mix.

**Treatment:**

| Action | Timing |
|---|---|
| Email (Step 1) | Within 48–72 hours of scoring |
| Follow-Up 1 | Day 3 |
| Follow-Up 2 | Day 6 |
| Breakup email | Day 11 |
| Park | Day 12 |

No phone call for WARM leads unless they reply and ask for one.
If a WARM lead replies positively, they immediately become effectively HOT — treat them as such.

**In CRM:** WARM leads are the bulk of your active pipeline.
Sort them by `Next Follow-Up Date` ascending — oldest due date gets actioned first.

---

## Cool Leads (Score 3–5): Batch When Ready

A COOL lead has some fit signals but not enough urgency or revenue context
to justify jumping the queue.

**Treatment:**

| Action | Timing |
|---|---|
| Email (Step 1) | This week, when HOT and WARM queue is clear |
| Follow-Up 1 | Day 4 (slightly longer spacing) |
| Follow-Up 2 | Day 8 |
| Breakup email | Day 14 |
| Park | Day 15 |

**Batching approach:** Reserve your last 3–5 initial emails each day for COOL leads,
after HOT and WARM follow-ups are handled.

**Re-scoring:** Before emailing a COOL lead that has been sitting for 2+ weeks,
re-check their Google Maps profile and website. Scores change.
A clinic that had good reviews two weeks ago may have slipped to 4.1 stars.
A clinic that had no ads may now be running them. Rescore before you send.

---

## Cold Leads (Score 0–2.5): Park, Don't Email

A COLD lead either:
- Has no visible gaps to solve (their system is working)
- Has no viable email contact
- Is in a market or service type that doesn't match your offer well

**Treatment:** Set `Status` = `Park - 60 Days`. Add a note: "Low score [X] — park until [date]."
Do not email. Do not follow up. Let the date arrive and rescore then.

**Why not just delete them?** Their situation changes. A clinic with great reviews
today may have a new negative review wave in 60 days. A practice with no ads may
start running them. Keep the record, change the date, revisit.

---

## The In-Sequence Priority Rule

Once a lead is in the sequence (past Step 1), priority is determined by
**stage and lead score combined**:

```
HIGHEST PRIORITY TODAY:
1. Positive replies (any tier) — respond within 2 hours
2. HOT leads due for any follow-up step
3. HOT leads due for a call attempt (Day 5)
4. WARM leads due for Step 2 or Step 3
5. COOL leads due for Step 2 or Step 3
6. HOT leads — new, not yet emailed
7. WARM leads — new, not yet emailed
8. COOL leads — new, not yet emailed
9. Breakup emails (any tier)
```

Work down this list each morning. Stop when your follow-up capacity
for the day is used (aim for max 10–15 touchpoints per morning block).

---

## CRM Visual Setup

### New Columns to Add to `Leads` Tab

These columns already appear in `crm-setup.md` (updated version).
Key columns for the priority view:

| Column | Content | Source |
|---|---|---|
| `Lead Score` | 0–10 numeric total | Formula: `=SUM(score cols)` |
| `Priority Tier` | 🔴 HOT / 🟠 WARM / 🟡 COOL / ⚪ COLD | Formula (see below) |
| `Days Since Last Contact` | How stale is this lead? | Formula (see below) |
| `Urgency Flag` | Should this lead be actioned today? | Formula (see below) |

### Priority Tier Formula

```
=IF(R2="","",
  IF(R2>=8,   "🔴 HOT",
  IF(R2>=5.5, "🟠 WARM",
  IF(R2>=3,   "🟡 COOL",
              "⚪ COLD"))))
```

Where R2 is the `Lead Score` cell.

### Days Since Last Contact Formula

```
=IF(R2="","",
  IF(LastContactDate="", "Never contacted",
    TODAY() - LastContactDate))
```

Replace `LastContactDate` with the actual column reference (e.g., `V2`).

### Urgency Flag Formula

Fires a visual flag when a HOT or WARM lead has been sitting too long:

```
=IF(AND(PriorityTier="🔴 HOT",  DaysSinceContact>1),  "⚠ OVERDUE",
  IF(AND(PriorityTier="🟠 WARM", DaysSinceContact>3),  "⚠ OVERDUE",
  IF(AND(PriorityTier="🟡 COOL", DaysSinceContact>7),  "⚠ OVERDUE",
    "")))
```

This column shows `⚠ OVERDUE` when a lead of their tier hasn't been contacted
within their expected window. Empty means on track.

### Conditional Formatting for Priority Tier Column

Select the Priority Tier column → Format → Conditional Formatting:

| Rule | Format |
|---|---|
| Text contains `🔴 HOT` | Red background (#ea4335), white text, **bold** |
| Text contains `🟠 WARM` | Orange background (#ff9900), black text |
| Text contains `🟡 COOL` | Yellow background (#fbbc04), black text |
| Text contains `⚪ COLD` | Light gray background (#f3f3f3), gray text |

Apply the same formatting to the `Urgency Flag` column:

| Rule | Format |
|---|---|
| Text contains `⚠ OVERDUE` | Red text, bold |

---

## The Priority View (Named Range / Filter View)

Create a filter view that shows your active priority stack:

1. In the `Leads` tab: **Data → Filter views → Create new filter view**
2. Name it: `Daily Priority Queue`
3. Apply these filters:
   - `Status` is not one of: `Not Interested`, `Lost`, `Do Not Contact`, `Park - 90 Days`, `Park - 60 Days`
   - `Reply Received` is `FALSE` (checkbox unchecked)
4. Sort by: `Lead Score` descending (column R → Z→A)
5. Secondary sort: `Next Follow-Up Date` ascending

Save the filter view. Each morning, open this view and work top to bottom.

---

## Weekly Priority Audit (10 Minutes, Every Monday)

```
[ ] How many HOT leads are in "New Lead" status? (should be 0 — email them same day)
[ ] How many HOT leads have gone more than 3 days without a touchpoint? (overdue flag check)
[ ] How many WARM leads have been in sequence for more than 2 weeks with no reply? (consider moving to Park)
[ ] How many "Park - 90 Days" leads have a park date that has now passed? (rescore and reactivate)
[ ] What is your current reply rate for HOT vs WARM vs COOL? (update Stats sheet)
```

---

## Priority Changes Mid-Sequence

Scores and priorities can change after initial contact:

| Event | Priority Change |
|---|---|
| They reply with curiosity | → Treat as HOT regardless of original score |
| They run new ads (spotted during review) | → Re-score, may upgrade tier |
| Their reviews drop below 4.0 stars | → Re-score urgency, may upgrade tier |
| They say "not now but check back" | → Park at their requested date, no tier change |
| They miss two calls with you after showing interest | → Note in CRM, drop follow-up frequency |

Mid-sequence rescoring is manual. Make it a habit when you review
a lead's row before sending a follow-up: glance at their Google Maps profile.
It takes 30 seconds and occasionally surfaces a significant change.
