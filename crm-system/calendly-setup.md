# Calendly Setup — Sales Call Booking System

Free plan only. One event type. Everything you need to book discovery calls
without back-and-forth emails or manual scheduling.

---

## What You Actually Need

- One event type: 15-minute intro call
- Google Calendar integration (so calls block your real calendar)
- One intake question (what specifically do they want to discuss)
- A confirmation email that sets expectations
- The right link at the right moment in the conversation

That's it. Do not over-engineer this.

---

## Step 1 — Create Your Calendly Account

1. Go to [calendly.com](https://calendly.com) → Sign up free
2. Sign up with Google (this auto-connects your Google Calendar)
3. Complete your profile:
   - **Name:** Your real first + last name
   - **Welcome message:** Leave blank for now (you'll set it per event)
   - **Time zone:** Your local timezone

---

## Step 2 — Connect Google Calendar

If you didn't connect during signup:
1. Calendly dashboard → **Account** (top right) → **Calendar Connections**
2. Click **Connect** next to Google Calendar
3. Select the Google account that has your actual schedule
4. Under **Check for conflicts:** select your main calendar
5. Under **Add to calendar:** select the same calendar

From now on, any Calendly booking automatically blocks your Google Calendar and
sends both parties a Google Calendar invite.

---

## Step 3 — Create Your One Event Type

1. Calendly dashboard → **Event Types** → **New Event Type** → **One-on-One**
2. Configure:

**Event name:**
```
10-Min Intro Call — [Your Name]
```
Not "Discovery Call." Not "Demo." "10-Min Intro Call" has the lowest friction.
It sounds fast and specific, not like a pitch.

**Duration:** 15 minutes
(Label it 10-min to reduce hesitation, but book 15 so you're not rushed)

**Location:** Zoom, Google Meet, or phone call
- If phone: set to "I'll call the invitee" and collect their phone number
- If video: Google Meet is free and auto-generates links

**Description (shown on booking page):**
```
A quick 10-minute call to see if [your system name] is a good fit
for your practice.

I'll ask about your current patient inquiry process, share how we
handle the gaps, and we'll both know by the end if it makes sense.
No slides. No pitch. Just a real conversation.
```

---

## Step 4 — Set Your Availability

1. On the event type → **When can people book this event?**
2. Set **date range:** 60 rolling days (leads booking ahead)
3. Set **available hours:**
   - Monday–Friday: 9am–5pm (your timezone)
   - Remove lunch: block 12pm–1pm
4. Set **minimum scheduling notice:** 2 hours
   (Prevents someone booking at 9:50am for a 10am call)
5. Set **buffer time after events:** 15 minutes
   (Gives you time to update CRM after each call)

---

## Step 5 — Add the Intake Question

This is the most important configuration step. One question only.

1. Event type → **Questions** tab → **Add Question**
2. Type: **Multiple lines**
3. Question:
```
What's the one thing you'd most want to solve on this call?
```
4. Mark as **Required**

**Why this question:**
- Forces them to show up with a specific problem (not vague curiosity)
- Gives you prep material before the call
- Pre-qualifies intent — someone who writes a real answer is engaged
- Weeds out calendar time-wasters who can't articulate why they're booking

---

## Step 6 — Configure Confirmation & Reminder Emails

1. Event type → **Notifications & Cancellation Policy**

**Confirmation email to invitee:**
Subject: `Confirmed: 10-min intro call with [Your Name]`

Edit the body:
```
Looking forward to speaking with you.

Before the call, it helps to have one number in mind:
roughly how many calls does [their clinic] get per week?
Even a guess is fine.

See you [day/time].

[Your Name]
[Your Phone — in case there's a connection issue]
```

**Reminder email:** 1 day before + 1 hour before (both on by default, keep them)

**Cancellation policy:** Add a note:
```
If you need to reschedule, use the link in your confirmation email.
I'll do the same if something comes up on my end.
```

---

## Step 7 — Customize Your Booking Page URL

1. Account Settings → **Profile** → Your unique Calendly link
2. Change from the random default to something clean:
   - `calendly.com/yourname` or `calendly.com/yourname-intro`
3. This is the URL you'll share in emails and DMs

---

## Step 8 — Get Your Shareable Links

Two links to save:

**Full booking page:**
`https://calendly.com/yourname/10-min-intro`
Use in: follow-up emails after they confirm interest, DM conversations

**Direct embed code (for landing page — optional):**
Event type → **Share** → **Add to Website** → copy the embed snippet

---

## When to Share the Calendly Link

| Situation | Share Link? |
|---|---|
| First cold email (Step 1) | ❌ Never — too transactional, too early |
| Follow-up emails (Step 2–3) | ❌ Offer specific times instead |
| After they reply positively | ❌ First offer two specific times in the email |
| After they can't make your offered times | ✅ "Here's my calendar: [link]" |
| After they explicitly ask for a link | ✅ Immediately |
| In your email signature | ✅ Optional — subtle, not pushy |
| On your landing page | ✅ Primary CTA |

**The rule:** Specific times first. Calendly link as the fallback.
Two specific options create a scheduling decision. A Calendly link creates
a browsing decision. Scheduling decisions convert higher.

---

## Step 9 — Add Calendly Link to Your Email Signature

In Gmail → Settings → Signature:

```
[Your Name]
[Your Title]
[Your Phone]

Book a 10-min call: calendly.com/yourname/10-min-intro
```

This surfaces passively. Don't draw attention to it in the email body
until they're ready. Let it sit in the signature as a low-friction option.

---

## Step 10 — Test It Before Going Live

1. Open your Calendly booking page in an incognito window
2. Book a test call with yourself
3. Check: did Google Calendar block the time?
4. Did you receive the confirmation email?
5. Does the intake question appear and is it required?
6. Is the confirmation email copy right?

Fix anything that looks off. Then you're live.

---

## CRM Integration

When a lead books via Calendly:

1. You'll receive an email: "New event: [Business Name]"
2. Open Google Sheets → find the lead's row
3. Update:
   - Status → `Call Scheduled`
   - Meeting Date → the booked date/time
   - Notes → copy their intake question answer into Notes column
   - Next Follow-Up Date → the day before the call (prep reminder)

You don't need Calendly-to-Sheets automation. Manual logging takes 60 seconds
and ensures you actually review their intake answer before the call.

---

## Free Plan Limitations

Calendly free plan allows:
- 1 event type only ← you only need 1
- Unlimited bookings
- Google Calendar integration
- Basic email notifications
- Custom intake questions

You do NOT need paid Calendly features for this system. Do not upgrade.
