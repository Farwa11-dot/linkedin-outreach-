# End-to-End Sales Pipeline

Every stage defined. Entry criteria, exit criteria, actions, and what
gets logged. A lead that enters this pipeline either closes, parks, or
exits clearly — it never just disappears into ambiguity.

---

## Pipeline Map

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       PROSPECTING PHASE                                  │
│                                                                          │
│  [ 1. SOURCED ]──────►[ 2. SCORED ]──────►[ 3. READY TO CONTACT ]       │
│  Google Maps,          Lead scoring          Score ≥ 3, email verified,  │
│  manual research       0–10 model            personalization note written │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         OUTREACH PHASE                                   │
│                                                                          │
│  [ 4. CONTACTED ]────►[ 5. FOLLOW-UP ]────►[ 6. BREAKUP EMAIL ]         │
│  Step 1 sent           Steps 2–3 sent        Final email. No reply →     │
│                        per schedule           Park 90 days               │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ Reply received
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        REPLY HANDLING PHASE                              │
│                                                                          │
│  [ 7. REPLIED ]                                                          │
│       │                                                                  │
│       ├── Positive/Curious ──────────► [ 8. CALL SCHEDULED ]            │
│       ├── Not Now ───────────────────► [ Park at their date ]           │
│       ├── Info Request ─────────────► [ Resource sent → follow up ]     │
│       └── Not Interested / DNC ─────► [ LOST — pipeline exit ]         │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ Call takes place
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      CONVERSION PHASE                                    │
│                                                                          │
│  [ 9. DISCOVERY CALL ]──►[ 10. QUALIFIED ]──►[ 11. DEMO HELD ]          │
│  10–15 min                Good fit confirmed   System shown,             │
│  problem diagnosed        by both parties      ROI framed                │
│                                │                      │                  │
│                                └── Not a fit ─────────►[ LOST ]         │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         CLOSING PHASE                                    │
│                                                                          │
│  [ 12. PROPOSAL/CLOSE ]──►[ 13. CLOSED WON ]──►[ 14. ONBOARDING ]      │
│  Verbal or written          Contract / agreement    Setup, first call,   │
│  agreement in principle     confirmed                go-live             │
│       │                                                                  │
│       └── Objections ───────► Handle → Re-close                         │
│       └── Lost after demo ──► [ LOST — log reason ]                     │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Stage-by-Stage Reference

### Stage 1: Sourced

**Definition:** You found the business and it has basic qualifying info.

**Entry criteria:**
- Business name and location identified
- At least one contact method found (email or contact form)

**Actions:**
- Log in Leads tab with basic fields filled
- Set Status: `New Lead`

**Exit criteria (→ Stage 2):**
- Scoring research complete (all 5 score dimensions filled in)

**What goes in the CRM:**
- Business Name, Industry, Website, Email, City, State, Contact Source
- Status: `New Lead`

---

### Stage 2: Scored

**Definition:** You have researched the lead and assigned a lead score.

**Entry criteria:** Stage 1 complete

**Actions:**
- Check Google Maps: reviews, hours, booking button, photos
- Check Meta Ad Library and Google search for ad activity
- Check website: mobile quality, booking flow, after-hours handling
- Fill in all 5 score dimension columns
- Lead Score auto-calculates, Priority Tier auto-labels

**Exit criteria (→ Stage 3):**
- All score columns filled
- Score ≥ 3 (if below 3: move to `Park - 60 Days`, do not proceed)

**What goes in the CRM:**
- Score columns M–Q filled
- Lead Score (R) and Priority Tier (S) auto-populated
- Status: `New Lead` (unchanged)

---

### Stage 3: Ready to Contact

**Definition:** Scored, email verified, personalization note written. Ready to send.

**Entry criteria:** Score ≥ 3 AND email format validated

**Actions:**
- Write one specific Personalization Note (column L) based on your research
- Optionally verify email with emailvalidation.io or Hunter.io

**Exit criteria (→ Stage 4):**
- Personalization Note is specific and true
- Email confirmed (or best available address in hand)

**What goes in the CRM:**
- Personalization Note filled in (column L)
- Status: `New Lead` (ready for morning outreach block)

---

### Stage 4: Contacted

**Definition:** Step 1 email sent.

**Entry criteria:** Stage 3 complete, email drafted and sent

**Actions:**
- Write and send Step 1 email manually in Gmail
- Log send in Call Log

**Exit criteria:**
- Reply received → Stage 7
- No reply → Stage 5 (follow-up sequence begins)

**What goes in the CRM:**
- Status: `Contacted`
- Initial Email Date: today
- Next Follow-Up Date: today + 2 (HOT) or today + 3 (WARM/COOL)
- Call Log entry: Action = `Email Sent`, Step = `Initial`

---

### Stage 5: Follow-Up

**Definition:** One or more follow-up emails sent, still no reply.

**Entry criteria:** Stage 4 complete, no reply received

**Actions (per follow-up step):**
- Check Follow-Up Queue tab for leads due today
- Re-read original email thread before writing follow-up
- Send follow-up — reply to original thread in Gmail
- Update CRM dates and status

**Exit criteria:**
- Reply received → Stage 7
- All 3 follow-ups sent without reply → Stage 6

**What goes in the CRM (update after each follow-up):**
- Status: `Follow-Up 1 Sent` / `Follow-Up 2 Sent` / `Follow-Up 3 Sent`
- Corresponding date column filled
- Next Follow-Up Date updated
- Call Log entry for each send

---

### Stage 6: Breakup Email

**Definition:** Final email in sequence. No reply received after 3 follow-ups.

**Entry criteria:** Follow-Up 3 sent, no reply

**Actions:**
- Send breakup email (short, warm, no pitch)
- Wait 24 hours for any last-minute reply

**Exit criteria:**
- Reply received → Stage 7
- No reply → Status = `Park - 90 Days`

**What goes in the CRM:**
- Status: `Park - 90 Days`
- Next Follow-Up Date: today + 90
- Notes: "Completed 4-touch sequence [date]. Park until [date+90]."
- Call Log entry: Step = `Breakup Email`

---

### Stage 7: Replied

**Definition:** Lead has responded to any email in the sequence.

**Entry criteria:** Incoming reply to any of your outreach emails

**Actions (within 2 hours of reply):**
- Read reply fully
- Classify reply type (see follow-up-intelligence.md)
- Update CRM immediately
- Draft response (review before sending)
- Clear Next Follow-Up Date

**Exit criteria (based on reply type):**
- Positive/Curious → Stage 8
- Not Now → Park (with future Follow-Up Date set to their timeline)
- Info Request → Send resource → follow up in 2 days → Stage 8 or re-park
- Not Interested → Stage `Lost`
- Unsubscribe → Stage `Do Not Contact`

**What goes in the CRM:**
- Reply Received: checked
- Reply Date: today
- Reply Summary: one sentence
- Reply Type: dropdown (Positive / Not Now / Info Request / etc.)
- Status: `Replied`
- Next Follow-Up Date: cleared or set per reply type

---

### Stage 8: Call Scheduled

**Definition:** A discovery call or intro call has been agreed to and is in the calendar.

**Entry criteria:** Lead expressed interest and confirmed a specific call time

**Actions:**
- Send 2 specific time options (avoid Calendly links for cold-to-warm transitions)
- Once confirmed: send a brief confirmation email
  ```
  "Confirmed — [Day, Time, Timezone]. I'll call you at [their phone number].
  Looking forward to it."
  ```
- Add to your personal calendar with prep note
- Set reminder: Next Follow-Up Date = 1 day before the call (prep reminder)

**Exit criteria:**
- Call held → Stage 9
- No-show → follow up same day, offer reschedule once

**What goes in the CRM:**
- Status: `Call Scheduled`
- Meeting Date: confirmed call date
- Notes: their phone number, any context they gave when booking

---

### Stage 9: Discovery Call

**Definition:** Initial discovery conversation held (10–15 min).

**Entry criteria:** Call scheduled and held

**Actions:**
- Follow discovery call script (conversion-system.md)
- Take notes during call — key pain points, patient values, objections
- If good fit: transition to demo on same call or schedule a separate demo session

**Exit criteria:**
- Good fit confirmed, demo shown or scheduled → Stage 10 / Stage 11
- Not a fit → Status = `Not Interested`, log reason

**What goes in the CRM:**
- Status: `Qualified` (if proceeding) or `Not Interested`
- Notes: detailed call notes — their exact words about the problem, their numbers
- Next Follow-Up Date: date of demo if not done on same call

---

### Stage 10: Qualified

**Definition:** Discovery confirmed genuine pain. Both parties agree it's worth exploring.

**Entry criteria:** Discovery call held, mutual agreement to proceed

**Actions:**
- Confirm demo appointment if not done during discovery
- Brief prep: tailor the demo to the specific problem they described

**Exit criteria:**
- Demo held → Stage 11

**What goes in the CRM:**
- Status: `Qualified`
- Notes: what specific problem to address in demo

---

### Stage 11: Demo Held

**Definition:** Full demo of your solution shown and tailored to their situation.

**Entry criteria:** Discovery complete, demo appointment set

**Actions:**
- Run the demo (conversion-system.md — Demo Structure section)
- Walk through the ROI framing with their specific numbers
- Attempt a close at the end of the demo
- If not ready to close: agree on a specific next step and date

**Exit criteria:**
- Verbal yes / agreement to proceed → Stage 12
- "Need to think about it" → Stage 12 with follow-up date set
- "Not for us" → `Not Interested`

**What goes in the CRM:**
- Status: `Demo Held`
- Notes: their reaction, any specific objections raised, next step agreed
- Next Follow-Up Date: if follow-up needed (max 2 business days)

---

### Stage 12: Closing

**Definition:** Active closing conversation. Navigating final objections and agreement.

**Entry criteria:** Demo held, lead is evaluating

**Actions:**
- Handle objections using scripts from conversion-system.md
- Never "wait and see" — always set a specific follow-up time
- Send anything promised (one-pager, case study, pricing detail) within 24 hours
- Limit closing attempts to 2 follow-ups after the demo (do not badger)

**Exit criteria:**
- Agreement reached → Stage 13
- Final no after 2 follow-up attempts → `Not Interested`, log reason

**What goes in the CRM:**
- Status: `Closing`
- Notes: where they are in the decision, what specifically is holding them back
- Next Follow-Up Date: specific date agreed with them

---

### Stage 13: Closed Won

**Definition:** Agreement confirmed. Onboarding begins.

**Entry criteria:** Verbal or written agreement to proceed

**Actions:**
- Send onboarding intake form or welcome email within 10 minutes of close
- Schedule the first onboarding call
- Update CRM immediately

**What goes in the CRM:**
- Status: `Booked`
- Outcome: `Booked`
- Notes: what was agreed (product, price, start date)

---

### Stage 14: Onboarding

**Definition:** Client is being set up. System is being configured.

This stage moves outside the CRM and into your client management process.
The Leads CRM row is now an historical record, not an active pipeline entry.

**Keep in CRM:**
- Status: `Booked` (do not delete)
- Notes: date of first onboarding call, any setup notes
- Move to a separate `Clients` tab if your pipeline grows

---

## Lost Leads: What to Log and Why

Every lost lead is data. Log before you close.

| Lost Reason | What to Record |
|---|---|
| Not interested (no reason given) | "No reason given — not interested after [stage]" |
| "We already have something" | What do they have? Name it if possible |
| Price objection | What price point did they react to? |
| Wrong decision-maker | Who is the real decision-maker? (note for future) |
| Bad timing | When did they suggest to check back? |
| Never responded | How many touches? Which stage? |
| Wrong fit (service type) | Why wasn't it a fit? (informs targeting refinement) |

In 6 months, your lost lead notes become your most valuable research.
Pattern-matching across 50 lost deals tells you exactly where your system breaks.

---

## Pipeline Velocity Targets (Solo Founder)

| Stage Transition | Target Time |
|---|---|
| Sourced → Contacted | ≤ 48 hours (HOT: ≤ 24h) |
| Contacted → Reply | 2–10 days (depends on sequence) |
| Reply → Call Scheduled | ≤ 48 hours after reply |
| Call Scheduled → Held | ≤ 5 business days |
| Demo → Close Attempt | Same call or ≤ 48 hours after |
| Close Attempt → Decision | ≤ 5 business days |

**Leakage warning:** If leads are sitting more than 2× these times at any stage,
that stage is leaking. Check your Follow-Up Queue for overdue entries —
n8n should be alerting you to these every morning.
