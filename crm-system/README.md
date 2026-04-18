# Solo Founder Outbound CRM
### For cold outreach to dental and aesthetic clinics

A simple, free, relationship-first outreach system.
No inbox rotation. No bulk sending. No growth hacks.

---

## What This System Is

A daily operating system for one person doing 10–30 personal outreach
touchpoints per day. Every email is written or reviewed by you. Every
follow-up is intentional. Every reply is handled as a real conversation.

The metric this system optimizes for is not emails sent. It is
**meaningful conversations started**.

---

## System Architecture

```
MORNING (~20 min)
│
├── Open Google Sheets CRM
│   └── Check "Follow-Ups Due Today" view
│       └── Review each lead — read original email, check notes
│
├── Send follow-ups manually (one at a time, in Gmail)
│   └── Personalize each one — reference their specific situation
│
└── Log every action in Sheets — date, what you sent, any reply

AFTERNOON (~30 min)
│
├── Research 5–10 new leads on Google Maps
│   └── Spend 2–3 min per lead — one real observation per business
│
├── Write and send 3–10 initial outreach emails
│   └── Each one references something specific to that business
│
└── Add leads to CRM, set Next Follow-Up Date

EVENING (optional, 5 min)
└── Log any replies received, update statuses
```

---

## Pipeline Stages

```
New Lead
   │
   ▼
Contacted ──────────────────────────────► No Reply → Follow-Up 1 (Day 2)
   │                                                    │
   │                                                    ▼
   │                                       No Reply → Follow-Up 2 (Day 5)
   │                                                    │
   │                                                    ▼
   │                                       No Reply → Follow-Up 3 (Day 10)
   │                                                    │
   │                                                    ▼
   │                                       No Reply → Lost / Park (Day 11)
   │
   └── Reply received at any stage ──────► Replied
                                              │
                                     ┌────────┴────────┐
                                     ▼                  ▼
                                Interested           Not Interested
                                     │                  │
                                     ▼                  ▼
                                  Booked             Lost/Park
```

---

## File Map

| File | What It Does |
|---|---|
| `README.md` | System overview (this file) |
| `crm-setup.md` | Google Sheets structure — every column explained |
| `outreach-workflow.md` | Step-by-step process for each pipeline stage |
| `email-sequences.md` | 3-step email sequence (missed calls angle) |
| `daily-workflow.md` | Daily operating routine — what to do and when |
| `n8n/reminders-workflow.json` | n8n workflow that reminds YOU to follow up |
| `n8n/setup-guide.md` | How to wire up the reminder workflow |

---

## Guiding Principles

**1. Fewer, better emails win.**
Ten personally researched emails outperform a hundred generic ones.
If you can't write one specific thing about their business, don't send yet.

**2. Reply = win. Everything else is pipeline.**
The goal of every email is one thing: start a conversation.
Not a booking, not a sale, not a demo. A conversation.

**3. Stop when they respond — then be human.**
The moment someone replies, automation stops. You respond personally,
quickly, and without a script.

**4. Consistency beats intensity.**
10 leads/day for 60 days beats 100 leads in one week then nothing.
Build the daily habit, not the one-time sprint.

**5. The CRM is your memory.**
You will forget what you said to who and when. The CRM doesn't.
Log everything — even "called, no answer" and "replied, not interested."
That data becomes your map.
