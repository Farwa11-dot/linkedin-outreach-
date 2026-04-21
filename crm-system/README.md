# Solo Founder Client Acquisition System
### Cold outreach → qualified pipeline → closed clients

Built for one person doing outbound sales to dental and aesthetic clinics.
Free tools only. Manually operated. Light automation for reminders.

---

## What This System Does

Takes a lead from a Google Maps listing all the way to a signed client —
with a clear action at every stage, a score that tells you where to spend
your time, and a dashboard that tells you what's working.

```
RESEARCH          OUTREACH           CONVERSION         CLOSE
─────────         ──────────         ──────────         ──────
Source lead  →  Score (0–10)  →  Email sequence  →  Discovery call
                                                   →  Demo
                                                   →  Close
                                                   →  Onboard
```

---

## Architecture

```
DAILY DIGEST (n8n, 8am)
│  Reads CRM → ranks by Priority Tier → emails you ranked to-do list
│
▼
MORNING BLOCK (~20 min)
│
├── Reply inbox: classify by type, respond personally, update CRM
│   (follow-up-intelligence.md → reply routing playbook)
│
└── Follow-Up Queue (Sheets): HOT first, work down by score
    Send manually in Gmail → update CRM → log in Call Log

OUTREACH BLOCK (~30 min)
│
├── Score new leads (5 min/lead) → lead-scoring.md
├── Write & send initial emails manually → email-sequences.md
└── Update CRM: status, dates, next follow-up

CONVERSION (as calls are booked)
│
├── Pre-call prep (5 min) → conversion-system.md
├── Discovery call → qualify, diagnose, transition to demo
├── Demo → ROI frame on their numbers → soft close
└── Objection handling → re-close → onboard
```

---

## Pipeline Stages (full map in `sales-pipeline.md`)

```
Sourced → Scored → Ready → Contacted → Follow-Up 1/2/3 → Breakup
                                │
                            Reply received
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                  ▼
          Positive           Not Now           Not Interested
              │                 │                  │
        Call Scheduled       Park               Lost
              │
           Qualified
              │
          Demo Held
              │
           Closing
              │
         Closed Won
              │
          Onboarding
```

---

## File Map

### Foundation
| File | Purpose |
|---|---|
| `README.md` | System overview (this file) |
| `crm-setup.md` | Full Sheets schema: 33 columns, scoring formulas, priority queue filter |
| `outreach-workflow.md` | What to do at every pipeline stage |
| `daily-workflow.md` | Minute-by-minute daily operating routine |

### Intelligence Layer
| File | Purpose |
|---|---|
| `lead-scoring.md` | 5-dimension 0–10 model, scoring examples, Sheets integration |
| `offer-positioning.md` | Value props + ROI framing for dental and aesthetic |
| `priority-system.md` | HOT/WARM/COOL/COLD tiers, urgency flag formulas, visual CRM setup |
| `follow-up-intelligence.md` | Reply-type routing (6 types), breakup email templates |
| `icp-optimization.md` | Monthly ICP review, score model changelog, niche cut/double rules |

### Outreach & Conversation
| File | Purpose |
|---|---|
| `email-sequences.md` | 4-step email sequences — dental + aesthetic (missed calls angle) |
| `multi-channel-follow-up.md` | Day-by-day email + phone + DM sequences per lead tier |
| `conversation-handling.md` | Exact reply flows: vague interest, info requests, pricing questions |
| `call-booking-system.md` | Booking scripts (email, DM, phone), Calendly timing, no-show recovery |

### Conversion & Close
| File | Purpose |
|---|---|
| `conversion-system.md` | Discovery call script, demo structure, closing script, 7 objection responses |
| `offer-pricing.md` | 3-tier offer (Entry/Main/Upgrade), pricing presentation flow, risk reversals |
| `sales-pipeline.md` | 14-stage pipeline, entry/exit criteria, CRM updates per stage |

### Measurement & Optimization
| File | Purpose |
|---|---|
| `performance-dashboard.md` | 6-section Sheets dashboard: funnel, niche, city, subject line tracker |
| `icp-optimization.md` | Monthly review loop, segment scoring, niche decision framework |
| `speed-response-system.md` | Response time rules by event type, Gmail setup, post-call window |

### Automation
| File | Purpose |
|---|---|
| `n8n/reminders-workflow.json` | 8am priority digest: HOT first, surfaces replies + new HOT leads |
| `n8n/reply-alert-workflow.json` | Every-30min alert: fires when a reply sits 2h+ unanswered |
| `n8n/setup-guide.md` | Credential wiring, import steps, troubleshooting |

### Practical Setup
| File | Purpose |
|---|---|
| `calendly-setup.md` | 10-step free Calendly setup: event type, intake question, when to share the link |
| `demo-flow.md` | Minute-by-minute 15-min call script: opening, discovery, demo, ROI, close |
| `lead-sourcing-system.md` | 30-min daily sourcing: city rotation, 8 Maps search terms, email finding, quick scoring |
| `landing-page.md` | 6-section warm-lead page: full copy, Carrd 25-min build guide, when to send the link |
| `onboarding-process.md` | Post-close process: onboarding form, test call, go-live, Week 1 + 30-day check-ins |

---

## Google Sheets Tab Structure

```
Outreach CRM — Clinics
│
├── Leads          ← 33-column master pipeline (source of truth)
├── Follow-Up Queue ← SORT(FILTER(...)) — priority-ranked daily to-do
├── Call Log       ← one row per touchpoint
├── Templates      ← email copy with {{placeholders}}
└── Dashboard      ← funnel metrics, niche breakdown, subject line tracker
```

---

## Column Schema Summary (`Leads` tab)

| Block | Columns | Contains |
|---|---|---|
| Identity | A–K | Name, industry, email, phone, city, source |
| Scoring | L–S | Personalization note, 5 score dimensions, Lead Score, Priority Tier |
| Pipeline | T–Z | Status, email send dates, last contact, next follow-up |
| Replies | AA–AE | Reply checkbox, date, type, summary, meeting date |
| Outcome | AF–AG | Outcome dropdown, freeform notes |

---

## Guiding Principles

**1. Score before you email.**
Five minutes of scoring prevents hours of wasted follow-up on leads
who will never buy.

**2. Priority determines sequence.**
HOT leads get emailed within 24 hours and get a call attempt at Day 5.
COOL leads wait until your HOT and WARM queue is clear.

**3. Reply type determines response.**
A "Not Now" reply and a "Not Interested" reply require completely different
responses. Treating them the same is how you lose warm leads.

**4. Every lost deal is data.**
Log why every lead went cold. Pattern-matching across 50 lost deals
tells you more than any split test.

**5. The dashboard tells you what to fix.**
Reply rate below 3%: fix copy. Call-to-close below 30%: fix demo.
Demo-to-booked below 20%: fix objection handling. Each metric
points at a specific part of the system.
