# Speed & Response System

Speed is a conversion variable. Not a nice-to-have.

A lead who replies at 2pm and gets a response at 2:07pm is in a different
psychological state than one who gets a response at 9am the next morning.
The data is clear. This document turns that data into operating rules.

---

## Why Speed Matters More Than Copy

Research across B2B and B2C sales consistently shows:

- Responding within **5 minutes** of a lead expressing interest = **9× higher**
  conversion rate than responding after 30 minutes
- 50% of leads choose the first vendor to respond
- After **24 hours**, the probability of a meaningful conversation drops by 90%

For solo founder outreach to dental and aesthetic clinics specifically:

- Clinic owners are busy between patients and calls
- Their decision-making windows are **short** (between appointments,
  during lunch, early morning or evening)
- If you reply when they're between patients at 11:30am, you have a conversation
- If you reply at 4pm, they've moved on mentally to the afternoon schedule

---

## Response Time Rules by Event Type

### Rule Table

| Event | Max Response Time | What Happens If You Miss It |
|---|---|---|
| Positive reply received | **2 hours** | Momentum lost, lead cools significantly |
| Pricing question received | **2 hours** | They Google competitors while waiting |
| Call booking request | **30 minutes** | They forget or find another solution |
| Info request received | **4 hours** | Acceptable — they're not urgent |
| "Not now" reply | **24 hours** | Fine — no urgency |
| No-show on booked call | **15 minutes** | Send recovery email immediately |
| Post-demo follow-up | **Same day** | Delay = decision fatigue = lost deal |
| Objection raised on call | **In real time** | Never say "let me get back to you on that" |
| Signed client onboarding email | **10 minutes** | Buyer's remorse window is immediately post-close |

---

## The Urgency Tiers

### Tier 1 — Respond Within 2 Hours (Critical)

- Any reply classified as `Positive` in Reply Type column
- Any pricing question
- Any reply that contains a question (even vague ones)
- Any reply that includes a phone number or "call me"
- A booked call that you need to confirm

**If you're unavailable:** Set a Gmail template reply:
```
Hi {{first_name}},

Got your message — I'm in meetings until [time] but will get
back to you by [specific time today].

[Your name]
```

This keeps the conversation alive. Silence for 4+ hours when they
just expressed interest is a conversion killer.

### Tier 2 — Respond Within 4 Hours (Important)

- Info requests
- Neutral replies asking general questions
- "Not now" replies that need acknowledgment
- Post-call follow-up emails

### Tier 3 — Respond Same Day (Standard)

- Auto-replies / OOO (just update the CRM)
- "Not interested" replies (still need a graceful response)
- General questions without urgency signals

### Tier 4 — Respond Within 48 Hours (Low Urgency)

- Unsubscribe replies (acknowledge promptly, but not urgently)
- Vague non-committal replies with no question

---

## Speed System: Practical Setup for a Solo Founder

### Gmail Mobile Notifications

Turn on push notifications for your outreach Gmail accounts on your phone.
This is non-negotiable for Tier 1 events.

Settings to configure:
- **Gmail app** → Settings → your outreach account → Sync settings → All mail
- Notification sound: distinct from personal email (so you can triage by sound)
- Priority inbox: label outreach threads with a specific label (e.g., "Outreach")
  and enable notifications only for that label

### The 2-Hour Check Rule

If mobile notifications aren't realistic for you during the day:

Set calendar blocks at:
- 9:00am — morning check (first thing)
- 12:00pm — midday check
- 3:00pm — afternoon check
- 5:30pm — end-of-day check

These windows mean the maximum gap between a reply and your response is 3 hours.
Not perfect, but close enough to maintain momentum in most conversations.

### Gmail Filters + Labels for Outreach

Create a Gmail filter:
- From: [any domain you're actively outreaching]
- Skip inbox: no
- Apply label: "OUTREACH REPLY"
- Mark as important: yes

This makes replies visually distinct from regular email so you can triage fast.

### Pre-Written Response Templates in Gmail

Set up Gmail canned responses (Templates) for the most common reply types.
You still personalize before sending, but you're starting from a complete template
rather than a blank page.

In Gmail → Settings → Advanced → Enable Templates.

Create templates for:
- Positive reply (go to call ask)
- Pricing question response
- Info request narrowing question
- "Not now" acknowledgment and park
- Post-call follow-up

**Opening a canned response:** Compose → three dots (More options) → Templates → Insert Template.
Time from reply received to personalized response: under 90 seconds.

---

## n8n: Reply Alert Workflow

The n8n health monitor workflow can be extended to alert you when a reply
has been sitting unresponded for more than 2 hours during business hours.

See `n8n/reply-alert-workflow.json` for the implementation.

**How it works:**
1. Runs every 30 minutes between 8am–7pm weekdays
2. Reads Leads tab: finds rows where Reply Received = TRUE but
   Reply Date = today AND Status is still in an outreach stage
   (meaning: reply came in but CRM hasn't been updated to a post-reply stage)
3. Checks if > 2 hours have elapsed since Reply Date
4. If yes: sends you an email/notification: "⚡ [Business Name] replied 2h ago — respond now"

This catches the cases where you saw the reply but got pulled into something else.

---

## Speed Urgency in the CRM

### Urgency Flag Column

The `Urgency Flag` column (from `priority-system.md`) fires `⚠ OVERDUE` when:
- A HOT lead hasn't been contacted in > 1 day
- A WARM lead hasn't been contacted in > 3 days

Add a second formula to flag stale replies:

**Reply Staleness Flag** (add in a new column after Urgency Flag):
```
=IF(
  AND(
    AA2=TRUE,
    AB2=TODAY(),
    OR(T2="Contacted", T2="Follow-Up 1 Sent", T2="Follow-Up 2 Sent", T2="Follow-Up 3 Sent")
  ),
  "⚡ REPLY NEEDS RESPONSE",
  ""
)
```

Where AA = Reply Received checkbox, AB = Reply Date, T = Status.

This flags any row where a reply came in today but the status hasn't
been updated past the outreach stage — meaning you haven't responded yet.

Color this cell bright yellow or red so it's impossible to miss during
your morning CRM review.

---

## Speed After the Call (Post-Call Window)

The 2 hours after a call are your highest-leverage conversion window.

| Action | Target Time |
|---|---|
| Send follow-up email (if closing, send next steps) | Within 30 min |
| Send promised resource (case study, pricing breakdown) | Within 2 hours |
| Update CRM with call notes | Within 5 minutes |
| Set next follow-up date and reminder | Within 5 minutes |

**Why the 30-minute post-call email matters:**

A lead who just had a positive 15-minute call is at their peak openness.
They're thinking about the problem you discussed. Their objections are
freshest. If you send a summary email within 30 minutes that:
1. Recaps what they told you (shows you listened)
2. Names the specific problem you'll solve for them
3. Gives clear next steps

...they feel understood and the decision feels natural.

**Post-call follow-up email:**
```
Subject: summary from our call — {{clinic_name}}

Hi {{first_name}},

Good talking with you. Here's a quick recap so we're on the same page:

- You mentioned [specific pain they described in their words]
- We estimated [number] missed calls per month at {{clinic_name}},
  which at $[their patient value] per patient translates to roughly
  $[calculated number] in potential recovered revenue
- The [Starter/Growth] tier fits your call volume

Next step: [exactly what was agreed — "you're reviewing with your
office manager and getting back to me by [day]" OR "you're sending the
onboarding form today" — whatever was actually agreed]

I'll follow up [specific day] if I don't hear back.

Let me know if anything came up after we hung up.

[Your name]
```

---

## Speed as a Differentiator

Most of your competitors — whether they're agencies or other solo founders —
respond slowly. Their CRMs are checked once a day. Their email gets
batched. Leads wait 24–48 hours for a response.

You respond in under 2 hours.

This alone will differentiate you in the mind of a busy clinic owner who
is used to vendor calls not being returned for days. It signals:
- You are organized
- You value their time
- You will be this responsive as a client relationship

Your response speed is the first proof point that your system works.
