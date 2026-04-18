# Cold Email Scaling Roadmap: 20 → 100+ Emails/Day

Deliverability-first scaling. Every volume increase must be earned
by hitting health metric thresholds — not just waiting out a calendar.

---

## The Core Principle

> Volume is a reward for inbox health, not a default setting.

You do not increase sending because time has passed.
You increase sending because your metrics prove you've earned it.

---

## Gmail Sending Limits — The Full Picture

### Technical vs Practical Limits

| Account Type | Gmail's Hard Limit | Safe Cold Email Limit | Why the Gap |
|---|---|---|---|
| Free Gmail | 500/day total | **20/day cold** | Spam filters trigger at low volumes for new/cold sends |
| Google Workspace (paid) | 2,000/day total | **50/day cold** | Better reputation, but still requires ramp-up |

### Why 20/Day Is the Real Ceiling for Free Gmail (Cold Sends)

Gmail's spam detection does not just count volume — it analyzes:
- **Send pattern**: Do emails go out in bursts or spaced naturally?
- **Engagement ratio**: How many recipients open/reply vs ignore?
- **Bounce rate**: How many addresses are invalid?
- **Complaint rate**: How many hit "Report Spam"?
- **Recipient diversity**: Are you emailing the same domains repeatedly?

A new Gmail account sending 50 cold emails in one morning will trigger
all four signals simultaneously. Gmail's ML classifies the account as
a bulk sender within days, throttling delivery to spam globally.

**20/day with proper spacing is the empirically safe ceiling** for a
free Gmail account doing cold outreach to strangers.

---

## Scaling Phases Overview

```
Phase 0   Phase 1    Phase 2    Phase 3    Phase 4
 (Setup)  (Warm-Up) (Safe Base) (Growth)  (Scale)

  Day 1  → Day 14  → Day 30  → Day 60  → Day 90+

  0 cold   5→15/day  20/day    40/day    100+/day
  1 inbox  1 inbox   2 inboxes 4 inboxes 5+ inboxes
```

---

## Phase 0 — Account Creation (Days 1–3)

**Actions:**
- Create 2 Gmail accounts (start with 2, add more at Phase 3)
- Complete profiles: name, photo, signature
- Enable Gmail API for each in Google Cloud Console
- Add credentials to n8n

**Do not send anything yet.**

**Gate to Phase 1:** Both accounts created, API credentials confirmed working in n8n.

---

## Phase 1 — Warm-Up (Days 4–21)

### The Warm-Up Goal

Build sender reputation by proving these accounts send and receive
real email with real engagement. Gmail watches the ratio of
engaged-to-ignored emails on a rolling 30-day window.

### Week-by-Week Warm-Up Schedule

#### Week 1 (Days 4–10): Human Activity Only

| Action | Daily Target | Notes |
|---|---|---|
| Real emails sent | 5–8 | To friends, colleagues, newsletters |
| Emails received & opened | 5–10 | Subscribe to 5–8 newsletters |
| Email replies sent | 2–3 | Reply to things you receive |
| Cold emails | **0** | Absolutely none |

**What to email:**
- Reply to any newsletter or email you receive
- Subscribe to: Morning Brew, Dentistry Today, MedSpa Magazine (relevant to your niche)
- Email yourself between the two accounts (inbox1 → inbox2 and reverse)
- Forward industry articles to yourself with a comment

#### Week 2 (Days 11–17): Light Engagement Ramp

| Action | Daily Target |
|---|---|
| Real emails sent | 10–15 |
| Cold emails | **0 still** |
| Inbox-to-inbox exchanges | 3–5/day per account |

Start using Gmail actively: search, star, archive, label emails.
Gmail tracks these micro-signals as engagement.

#### Week 3 (Days 18–21): Soft Cold Start

| Inbox | Cold Sends/Day | Real Sends/Day | Total |
|---|---|---|---|
| Inbox 1 | 5 | 10 | 15 |
| Inbox 2 | 5 | 10 | 15 |

Send these first cold emails manually — do not use n8n yet.
This lets you watch reactions in real time.

**Gate to Phase 2:** No spam complaints, bounce rate < 2%, at least 1 reply received in Week 3.

---

## Phase 2 — Safe Baseline (Days 22–45)

### Volume

| Inbox | Cold/Day | Total/Day (all outreach) |
|---|---|---|
| Inbox 1 | 20 | 20 |
| Inbox 2 | 20 | 20 |
| **System total** | **40/day** | **~800/month** |

### Automation Starts Here

Enable n8n workflows (workflow.json + workflow-followup.json).
Configure round-robin routing: odd Lead IDs → Inbox 1, even → Inbox 2.

### Health Check Cadence

Run this checklist every Friday:

```
[ ] Bounce rate this week: ____%   (threshold: < 2%)
[ ] Reply rate this week:  ____%   (threshold: > 1%)
[ ] Spam reports:          ____    (threshold: 0)
[ ] mail-tester.com score: ____/10 (threshold: ≥ 8)
[ ] Inbox delivery confirmed: Y/N  (send to Gmail + Outlook test addresses)
```

**Gate to Phase 3:** All 5 checkboxes passing for 2 consecutive weeks.

---

## Phase 3 — Growth (Days 46–75)

### Volume

| Inbox | Cold/Day |
|---|---|
| Inbox 1 | 20 |
| Inbox 2 | 20 |
| Inbox 3 (new) | 5 → 15 → 20 (ramp over 3 weeks) |
| Inbox 4 (new) | 5 → 15 → 20 (ramp over 3 weeks) |
| **System total** | **80/day at full ramp** |

### Adding New Inboxes at Phase 3

Each new inbox goes through its own mini warm-up (2–3 weeks) before
carrying full cold load. Do not skip this even though your other
inboxes are healthy.

New inbox ramp schedule:
- Week 1 of new inbox: 5 cold/day
- Week 2: 10 cold/day
- Week 3: 20 cold/day (full allocation)

While a new inbox is ramping, existing inboxes carry the load.

### Routing Logic Update

Update n8n to route by `Assigned Inbox` column (4-way split):
- Inbox 1: Leads A001–A020
- Inbox 2: Leads A021–A040
- Inbox 3: Leads A041–A055 (ramping)
- Inbox 4: Leads A056–A070 (ramping)

**Gate to Phase 4:** 4 inboxes all at full 20/day, all health checks green for 2 weeks.

---

## Phase 4 — Scale (Day 76+)

### Volume

| Inbox | Cold/Day |
|---|---|
| Inbox 1 | 20 |
| Inbox 2 | 20 |
| Inbox 3 | 20 |
| Inbox 4 | 20 |
| Inbox 5 (new) | 5 → 20 (ramp) |
| **System total** | **100/day** = **~2,000/month** |

### What Changes at 100/day

At this volume, manual monitoring is no longer sufficient.
The following must be automated:

1. **Daily bounce rate calculation** — n8n reads Sent Log, calculates rate, alerts if > 2%
2. **Auto-pause on threshold breach** — if bounce rate > 3%, n8n stops adding `ready` leads for that inbox
3. **Weekly health report** — n8n emails you a summary every Monday morning
4. **Do-not-contact sync** — replies with "unsubscribe" are auto-flagged in Sheets

See `n8n/workflow-health-monitor.json` for automation of these checks.

---

## Exact Thresholds — When to Scale Up vs Pull Back

### Green Light: Increase Volume ✓

All of the following must be true:

| Metric | Threshold |
|---|---|
| Bounce rate (7-day) | **< 2%** |
| Reply rate (7-day) | **> 1%** |
| Spam complaints | **0** in past 7 days |
| mail-tester score | **≥ 8/10** |
| Inbox delivery test | **Inbox** (not spam) on Gmail + Outlook |
| Days since last volume increase | **≥ 14 days** |

### Yellow: Hold Current Volume ⚠

Any single condition:
- Bounce rate 2–4%
- Reply rate 0.5–1%
- 1 spam complaint in past 14 days
- mail-tester score 6–7/10

Action: hold volume, investigate root cause, do not add new inboxes.

### Red: Scale Down ✗

Any single condition:
- Bounce rate > 4%
- Spam complaint in past 7 days
- mail-tester score < 6/10
- Inbox delivery test shows spam placement

Action: trigger the Fallback Protocol (see `fallback-strategy.md`).

---

## Scaling Decision Tree

```
Every Friday → Run Health Check
        │
        ▼
   All metrics GREEN?
        │
   YES ──────────────────────► Running < 2 weeks since last increase?
        │                              │
        │                          YES → HOLD (wait until 14 days)
        │                          NO  → SCALE UP (add 5 sends/inbox or add inbox)
        │
   NO ──────────────────────► Any metric YELLOW?
                                       │
                                   YES → HOLD + investigate
                                   NO  → Any metric RED?
                                              │
                                          YES → FALLBACK PROTOCOL
                                          NO  → review data, check again in 3 days
```

---

## Volume Milestones Summary

| Milestone | Timeline | Inboxes | Daily Volume | Monthly Reach |
|---|---|---|---|---|
| Phase 0 | Day 1–3 | 2 created | 0 | 0 |
| Phase 1 | Day 4–21 | 1 active | 5 → 15 | — |
| Phase 2 | Day 22–45 | 2 active | 40 | ~800 |
| Phase 3 | Day 46–75 | 4 active | 60 → 80 | ~1,400 |
| Phase 4 | Day 76+ | 5 active | 100 | ~2,000 |

> These are conservative timelines assuming you hit every gate. If
> you miss a gate, add 2 weeks before re-evaluating. Do not rush phases.
