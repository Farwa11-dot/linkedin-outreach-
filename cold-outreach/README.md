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

| File | Purpose |
|---|---|
| `README.md` | System overview (this file) |
| `implementation-guide.md` | Step-by-step setup from zero |
| `email-sequences.md` | 3-step email templates (dental + aesthetic) |
| `personalization-guide.md` | How to research and tag leads for free |
| `deliverability-rules.md` | Sending limits, warm-up, safety rules |
| `sheets/crm-template.md` | Google Sheets CRM column definitions |
| `n8n/workflow.json` | Importable n8n automation workflow |

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

## Daily Capacity (Safe Mode)

| Inboxes | Daily Sends | Monthly Reach |
|---|---|---|
| 1 Gmail | 20 emails/day | ~400 leads/month |
| 2 Gmails | 40 emails/day | ~800 leads/month |
| 3 Gmails | 60 emails/day | ~1,200 leads/month |

> Never exceed 20 cold emails/day per Gmail account. Gmail's soft limit is 500/day
> total but cold email volume above 20–30/day triggers spam filters rapidly.
