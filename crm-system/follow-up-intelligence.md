# Follow-Up Intelligence — Reply-Based Routing and Breakup Logic

Standard follow-up sequences treat every non-response the same.
This system treats every reply differently — and uses the type of reply
to choose the next move automatically.

---

## The Core Distinction: No Reply vs Reply Type

Most follow-up systems only handle "no reply." But in practice, you get
many types of replies, and each requires a completely different response.

```
INCOMING REPLY
      │
      ▼
What type is it?
      │
      ├── Positive / Curious ──────────── → Fast-Track to Call
      ├── "Not now" / timing objection ── → Park + Trigger sequence
      ├── "Not interested" / negative ─── → Graceful exit
      ├── "Send more info" ──────────────  → Specific resource send
      ├── Auto-reply / OOO ──────────────  → Reset follow-up timer
      ├── Unsubscribe / angry ───────────  → Immediate stop + DNC
      └── No reply (sequence continues) → Day 2 → Day 5 → Day 10 → Breakup
```

---

## Reply Types and Response Playbook

### Reply Type 1: Positive / Curious

**Signals:**
- "This is interesting — tell me more"
- "How does this work exactly?"
- "What's the pricing?"
- "I've been thinking about this"
- "Can we jump on a call?"

**Response goal:** Book the call. Nothing else.

**Template:**

```
Subject: (reply to thread)

Hi {{first_name}},

Great to hear from you — happy to walk you through it.

I have availability [specific day] at [time] and [day] at [time].
Which works better for you?

(Or just grab a time here: [Calendly link if you have one])

[Your name]
```

**What NOT to do:** Do not send a wall of information before the call.
Do not answer pricing in email. Do not send a PDF. Get the call booked.

**CRM updates:**
- Status → `Replied`
- Reply Summary → "Curious / positive — booking call"
- Next Follow-Up Date → day of the call
- Clear all pending sequence follow-ups

---

### Reply Type 2: "Not Now" / Timing Objection

**Signals:**
- "We're slammed right now — check back in a month"
- "We just switched software, bad timing"
- "I'm going on vacation — can you reach out in July?"
- "This is Q4, we're too busy"

**Response goal:** Lock in a specific future date. Then park them with a warm exit.

**Template:**

```
Subject: (reply to thread)

Hi {{first_name}},

Completely understand — timing matters with this kind of thing.

I'll put a reminder to follow up with you around [the month/date they mentioned].
In the meantime, if anything changes and you want to chat sooner, just reply here.

Good luck getting through [busy period].

[Your name]
```

**CRM updates:**
- Status → `Park - [Month]` (e.g., "Park - July")
- Reply Received → checked
- Next Follow-Up Date → the date they mentioned (or +45 days if vague)
- Notes → "Said: [their exact words about timing]"
- Clear sequence dates — do NOT send follow-ups while parked

**When the date arrives:** Don't reference their exact quote robotically.
Just say: "I mentioned I'd follow up around now — still a good time to connect?"

---

### Reply Type 3: "Not Interested" / Negative

**Signals:**
- "Thanks but we're not looking for this"
- "We have this handled"
- "We don't use third-party services"
- (No explanation, just a clear no)

**Response goal:** Leave a positive impression. You never know when things change.

**Template:**

```
Subject: (reply to thread)

Hi {{first_name}},

No problem at all — I appreciate you taking the time to reply.

If things change down the road, I'm easy to find.
Best of luck with {{clinic_name}}.

[Your name]
```

That's it. One short paragraph. Nothing else.

**CRM updates:**
- Status → `Not Interested`
- Reply Received → checked
- Outcome → `Not Interested`
- Notes → what they said (verbatim quote helps)
- Next Follow-Up Date → blank (never reach out again from cold pipeline)

---

### Reply Type 4: "Send More Information"

**Signals:**
- "Can you send me some information?"
- "Do you have a brochure/deck?"
- "Send me pricing"
- "What exactly does this include?"

**Response goal:** Send *only* what they asked for, paired with a question that moves toward a call.

**Do not:** Send a generic PDF. Send a 10-page deck. Spend 2 hours making materials.

**Template:**

```
Subject: (reply to thread)

Hi {{first_name}},

Happy to share — let me ask one quick question first so I can send
the most relevant information rather than a generic overview:

[Choose one based on their request:]

If they asked about pricing:
"What's your approximate volume of calls per week — especially
after-hours or on weekends? Pricing is based on call volume,
so that'll help me give you an accurate number."

If they asked how it works:
"What's the main gap you're trying to address — is it after-hours
calls, weekend inquiries, or something during business hours when
the front desk is tied up?"

[Your name]
```

This approach surfaces what they actually need to know, positions you as
consultative rather than salesy, and moves the conversation forward.

After they respond to your question → answer specifically → offer a 15-minute call.

**CRM updates:**
- Status → `Replied`
- Reply Summary → "Asked for info: [what specifically]"
- Next Follow-Up Date → 2 days (if no reply to your response)

---

### Reply Type 5: Auto-Reply / Out of Office

**Signals:**
- Standard OOO email
- "I'm out of the office until [date]"
- Automated response with no personal content

**Response goal:** None right now. Reset the timer to when they're back.

**Action:** Do not reply to the auto-reply.

**CRM updates:**
- Notes → "OOO until [date] — auto-reply received [date]"
- Next Follow-Up Date → their return date + 1 day
- Status → unchanged (sequence paused, not advanced)

---

### Reply Type 6: Unsubscribe / Angry

**Signals:**
- "Remove me from your list"
- "Stop emailing me"
- "How did you get my email?"
- Hostile tone of any kind

**Response goal:** Acknowledge, apologize briefly, confirm removal. Immediately.

**Template:**

```
Subject: (reply to thread)

Hi {{first_name}},

My apologies for the unwanted contact — I'll remove you from
my outreach right now. You won't hear from me again.

[Your name]
```

Send within 1 hour. Do not explain yourself. Do not defend the email.

**CRM updates:**
- Status → `Do Not Contact`
- Reply Received → checked
- Outcome → `Lost`
- Notes → "Unsubscribed [date] — do not contact from any account"

**Non-negotiable:** Never email this person or business again from any inbox.

---

## No-Reply Sequence: Days and Breakup Logic

For leads who never respond:

```
Day 0   → Initial email (Step 1)
Day 2   → Follow-Up 1 (different angle — social proof)
Day 5   → Follow-Up 2 (value framing — what they gain)
Day 10  → Breakup Email
Day 11  → Status → Park - 90 Days. Done.
```

### The Breakup Email

The breakup email is the most important email in the sequence.
It gets the highest reply rate of all four — because people respond
to endings, loss aversion, and genuine closure.

**Rules:**
- Keep it under 70 words
- No pitch
- No ask for a call
- End with a door genuinely left open
- Tone: warm, not passive-aggressive

**Template (Dental):**

```
Subject: closing the loop — {{clinic_name}}

Hi {{first_name}},

Last email from me — I don't want to clog your inbox.

If the timing ever changes and you want to look at the missed
call problem at {{clinic_name}}, I'm easy to find.

Either way, good luck. The practice looks like it's doing
genuinely good work.

[Your name]
```

**Template (Aesthetic):**

```
Subject: closing the loop — {{clinic_name}}

Hi {{first_name}},

Last note from me — I know your inbox is busy.

If {{clinic_name}} ever wants to look at the after-hours
inquiry problem, I'm one email away.

Wishing you a great rest of the month.

[Your name]
```

**After sending:** Status → `Park - 90 Days`. Walk away. Check back in 90 days with a
fresh angle — not a continuation of this sequence.

---

## Personalized Follow-Up Based on Reply Type (Templates)

### If they mentioned a specific pain in their reply

**Example reply:** "We do miss a lot of Saturday calls. It's frustrating."

**Your response:**

```
"That makes total sense — Saturdays are actually the highest-volume
missed-call day for most practices we work with.

The good news: that's exactly what the system is built for. Saturdays
through to Monday morning, it answers, qualifies, and books — and
your front desk sees all of it logged when they open up Monday.

Worth 15 minutes to see it in action?"
```

Mirror their words. Address their specific day/scenario. Keep it tight.

### If they mentioned a specific objection in their reply

**Example reply:** "We tried a similar thing before and it wasn't worth it."

**Your response:**

```
"I appreciate the honesty — what happened with it, if you don't mind me asking?

I want to understand what didn't work, because the failure mode
usually tells me whether what we do would be different or the same.

Sometimes it's a fit issue. Sometimes it's a setup issue. Either way,
I'd rather know before I waste your time."
```

Acknowledge, get curious, don't defend your product pre-emptively.

---

## CRM: Reply Type Column

Add this column to your Leads tab (after Reply Summary):

| Col | Field | Dropdown Values |
|---|---|---|
| [new col] | `Reply Type` | `Positive` / `Not Now` / `Not Interested` / `Info Request` / `Auto-Reply` / `Unsubscribe` / `No Reply` |

This column lets you filter:
- All `Positive` replies → your hottest pipeline
- All `Not Now` leads by Next Follow-Up Date → your warm pipeline
- All `Info Request` replies → need resource send + follow-up

It also tells you, over time, which emails generate which reply types —
which is more useful data than open rates.
