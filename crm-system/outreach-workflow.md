# Outreach Workflow — Step by Step

What to do at every stage of the pipeline. No ambiguity.

---

## Stage 1: New Lead

**Trigger:** You found a clinic worth contacting.

**Actions:**
1. Open the `Leads` tab in your CRM
2. Add a new row at the bottom (or insert above — keep newest at top)
3. Fill in: Lead ID, Business Name, Industry, Contact Name, First Name, Email, Website, City, State, Contact Source
4. Go to their Google Maps listing + website — spend 2 minutes
5. Write your Personalization Note (column L) — one specific, true observation
6. Set Status = `New Lead`
7. Leave all date columns blank for now

**Do NOT email yet.** Just log. You will email in batches, not one-by-one as you find leads.

---

## Stage 2: Initial Email (Step 1)

**Trigger:** You have 3–10 new leads ready to email in today's batch.

**Actions:**
1. Open your Gmail
2. Open your CRM Templates tab — copy the Step 1 body for the matching industry
3. For each lead:
   a. Paste the template into Gmail → New Message
   b. Personalize: replace `{{first_name}}`, `{{business_name}}`, `{{personalization_note}}`
   c. Read it out loud — does it sound like something a real person wrote to a specific business? If not, rewrite.
   d. Send
   e. Immediately go to CRM → set Status = `Contacted`, fill in `Initial Email Date` = today
   f. Set `Next Follow-Up Date` = today + 2 days
   g. Log the send in `Call Log` tab

**Rule: No copy-pasting without personalizing.** If the personalization note is empty, go back and research first.

**Spacing:** Wait at least 5 minutes between sends. Do not send 10 emails in 2 minutes. You are a person, not a server.

---

## Stage 3: Follow-Up 1 (Day 2 — No Reply)

**Trigger:** `Next Follow-Up Date` = today. Lead appears in Follow-Up Queue. No reply received.

**Before emailing:** Re-read your original email in Gmail's Sent folder.
Ask: *Does my follow-up add something new, or just repeat "did you see my email?"*
If it just repeats — don't send it. Write something with a different angle first.

**Actions:**
1. Check Follow-Up Queue tab
2. Click through to their Gmail thread (search by business name or email)
3. Reply to your own sent email (keeps it in one thread)
4. Send a short, different-angle follow-up (see email-sequences.md for copy)
5. In CRM: set Status = `Follow-Up 1 Sent`, fill in `Follow-Up 1 Date` = today
6. Set `Next Follow-Up Date` = today + 3 days (Day 5 from initial)
7. Update `Last Contact Date` = today
8. Log in `Call Log` tab

---

## Stage 4: Follow-Up 2 (Day 5 — No Reply)

**Trigger:** `Next Follow-Up Date` = today. Status is `Follow-Up 1 Sent`. No reply.

**Actions:**
Same as Follow-Up 1, but:
- Use the Step 3 template (value + a light close)
- In CRM: set Status = `Follow-Up 2 Sent`, fill in `Follow-Up 2 Date` = today
- Set `Next Follow-Up Date` = today + 5 days (Day 10 from initial)

---

## Stage 5: Follow-Up 3 (Day 10 — Final Touch)

**Trigger:** `Next Follow-Up Date` = today. Status is `Follow-Up 2 Sent`. No reply.

This is your last email in the sequence. Keep it brief, no pressure, leave the door open.

**Actions:**
- Send the Step 4 final email (see email-sequences.md)
- In CRM: set Status = `Follow-Up 3 Sent`, fill in `Follow-Up 3 Date` = today
- Set `Next Follow-Up Date` = BLANK (no more follow-ups)
- Set `Outcome` = `In Progress` (still possible they respond later)

**Day 11:** If still no reply, update Status = `Park - 90 Days`. Do not email again for 90 days.
Add a note: "Completed 4-touch sequence [date]. Park until [date + 90 days]."

---

## Stage 6: Reply Received

**Trigger:** A lead responds to any of your emails.

**Immediate actions (within 2 hours of reply — ideally faster):**

1. In CRM: check `Reply Received` checkbox, fill in `Reply Date` = today
2. Set Status = `Replied`
3. Write a one-sentence `Reply Summary` in column V:
   - `"Interested, asked for more info on pricing"`
   - `"Said not the right time, check back Q3"`
   - `"Angry, asked to stop emailing"`
   - `"Auto-reply, office closed this week"`
4. Clear `Next Follow-Up Date` (automated follow-ups stop now)
5. Log in `Call Log`: Action Type = `Reply Received`, paste their reply in Notes

**Then respond like a human:**
- Read their email carefully
- Don't immediately pitch — acknowledge what they said first
- If they're interested: offer a specific time ("I have Tuesday 2pm or Thursday 10am EST — which works?")
- If they're not interested: thank them gracefully, ask if you can check back later
- If they asked to stop: apologize briefly, confirm you'll remove them, then mark as Lost immediately

---

## Stage 7: Interested → Booked

**Trigger:** Lead expressed genuine interest. You are scheduling a call/meeting.

**Actions:**
1. Set Status = `Interested`
2. Send them 2–3 specific time options (do not send a Calendly link in cold outreach — it feels transactional)
3. Once they confirm a time:
   - Set Status = `Booked`
   - Fill in `Meeting Date`
   - Set `Next Follow-Up Date` = 1 day before the meeting (reminder to prep)
   - Log in `Call Log`

**Meeting prep (day before):**
- Re-read everything in their CRM row
- Check their website and Google reviews again — anything new?
- Write 3 questions to ask them
- Have your offer summary ready but don't lead with it

---

## Stage 8: After the Meeting

**Win:**
- Status = `Booked` (stays until contract signed)
- Log full meeting notes in `Notes` column
- Set next steps and `Next Follow-Up Date`

**Not yet:**
- Status = `Interested`
- Log what they said and why they're not ready
- Set `Next Follow-Up Date` based on what they told you ("check back in 3 weeks")

**Not interested:**
- Status = `Not Interested` or `Lost`
- Log the real reason in Notes — this data makes you better over time

---

## Follow-Up Rules Summary

| Situation | Action |
|---|---|
| No reply after Step 1 | Follow-up on Day 2 |
| No reply after Step 2 | Follow-up on Day 5 |
| No reply after Step 3 | Follow-up on Day 10 |
| No reply after Step 4 | Park for 90 days |
| Any reply received | Stop automation. Respond manually within 2 hours. |
| "Not interested" reply | Log it, thank them, mark Lost, never email again |
| "Unsubscribe" reply | Mark Lost immediately. Remove from all follow-up queues. |
| Auto-reply (out of office) | Note the return date. Reset `Next Follow-Up Date` to when they're back. |
| Bounced email | Mark email as invalid. Research an alternative contact. |

---

## What "Stopped" Means

Once a lead is in any of these statuses, **never send them another cold outreach email** from this pipeline:

- `Not Interested`
- `Lost`
- `Booked` (they're now a client or active conversation — not cold outreach)

The only exception: a lead who said "not now, check back in 90 days" —
that's a `Park - 90 Days`, and you follow up at their invitation.
