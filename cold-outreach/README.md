# Free Cold Outreach System — Dental & Aesthetic Clinics (US)

A fully free, safe, and deliverable cold email outreach system for solo founders.
No paid tools. No spam. No burned domains.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEAD SOURCING (Free)                         │
│   Google Maps → Manual Research → Personalization Notes         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                 GOOGLE SHEETS CRM                               │
│   Lead data → Status tracking → Follow-up scheduling           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               n8n AUTOMATION ENGINE (self-hosted)               │
│                                                                 │
│  [Schedule Trigger 9am]                                         │
│         │                                                       │
│         ▼                                                       │
│  [Read Google Sheets] → [Filter: status = "ready"]             │
│         │                                                       │
│         ▼                                                       │
│  [Build Personalized Email from Template]                       │
│         │                                                       │
│         ▼                                                       │
│  [Check Daily Limit ≤ 20 emails/inbox]                          │
│         │                                                       │
│         ▼                                                       │
│  [Route: Gmail Inbox 1 / 2 / 3 (round-robin)]                  │
│         │                                                       │
│         ▼                                                       │
│  [Send via Gmail API] → [Random Delay 3–8 min between sends]   │
│         │                                                       │
│         ▼                                                       │
│  [Update Google Sheets: status, sent date, inbox used]         │
│         │                                                       │
│         ▼                                                       │
│  [Schedule Follow-up Row: +3 days / +7 days]                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REPLY HANDLING                               │
│   Gmail filters → Sheets log → Manual follow-through           │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Map

### Core System
| File | Purpose |
|---|---|
| `README.md` | System overview (this file) |
| `implementation-guide.md` | Step-by-step setup from zero |
| `email-sequences.md` | 3-step email templates (dental + aesthetic) |
| `personalization-guide.md` | How to research and tag leads for free |
| `deliverability-rules.md` | Sending limits, warm-up, safety rules |
| `sheets/crm-template.md` | Google Sheets CRM column definitions |

### Scaling System
| File | Purpose |
|---|---|
| `scaling/scaling-roadmap.md` | Phase-by-phase volume growth: 20 → 100+/day |
| `scaling/multi-inbox-strategy.md` | Identity design, routing, and isolation for 2–5 inboxes |
| `scaling/deliverability-dashboard.md` | Metric tracking, formulas, and weekly health checks |
| `scaling/fallback-strategy.md` | Recovery playbook for every failure mode |

### n8n Workflows
| File | Purpose |
|---|---|
| `n8n/workflow.json` | Single-inbox Step 1 sends (beginner) |
| `n8n/workflow-followup.json` | Step 2 & 3 follow-ups |
| `n8n/workflow-multisend.json` | Multi-inbox scaled sending with Switch router (2–5 inboxes) |
| `n8n/workflow-health-monitor.json` | Monday health report + auto-pause on red metrics |
| `n8n/setup-guide.md` | Credential wiring + import instructions |

---

## Quick-Start (5 Steps)

1. **Source leads** — Google Maps search: `"dental clinic" [city, state]`
2. **Log in Sheets** — paste business name, email, personalization tag
3. **Warm up Gmail** — send 5–10 real emails/day for 2 weeks before cold outreach
4. **Import n8n workflow** — connect Google Sheets + Gmail credentials
5. **Set status = "ready"** on leads you want to send — n8n does the rest

---

## Targets

- Dental clinics (general dentistry, orthodontics, cosmetic dentistry)
- Aesthetic clinics (med spas, dermatology, anti-aging, laser clinics)
- US-based, 1–10 staff (solo founder / small practice = best fit)

---

## Scaling Capacity (by Phase)

| Phase | Timeline | Inboxes | Daily Sends | Monthly Reach |
|---|---|---|---|---|
| Phase 1 (Warm-Up) | Day 1–21 | 1 | 0 → 15 | — |
| Phase 2 (Baseline) | Day 22–45 | 2 | 40 | ~800 |
| Phase 3 (Growth) | Day 46–75 | 4 | 60 → 80 | ~1,400 |
| Phase 4 (Scale) | Day 76+ | 5 | 100 | ~2,000 |

> Volume increases are gated on health metrics (bounce rate, reply rate, inbox placement).
> See `scaling/scaling-roadmap.md` for exact thresholds and the week-by-week plan.

## Which Workflow to Use

| You are at... | Use this workflow |
|---|---|
| Getting started (1 inbox) | `n8n/workflow.json` |
| Running 2–5 inboxes | `n8n/workflow-multisend.json` |
| Sending follow-ups | `n8n/workflow-followup.json` |
| Monitoring health weekly | `n8n/workflow-health-monitor.json` |
