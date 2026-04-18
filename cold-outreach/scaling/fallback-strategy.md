# Fallback Strategy — When Emails Start Going to Spam

A systematic recovery protocol for every failure mode.
Run this document when any Red metric is triggered.

---

## Detection: How You Know You Have a Problem

### Signal 1: mail-tester.com Score Drops

Send a test email to your unique mail-tester address. Score below 7/10 = problem.
Run this test weekly (Friday), not just when you suspect an issue.

### Signal 2: Inbox Delivery Test Fails

Send test emails from each inbox to accounts you control:
- A Gmail address
- An Outlook/Hotmail address
- A Yahoo address

Check the **spam folder** of each. If any land in spam → that inbox has a problem.

### Signal 3: Bounce Rate Spike

Calculate from Sent Log:
```
=COUNTIF(SentLog!H:H,"bounced") / COUNTIF(SentLog!H:H,"sent") * 100
```

Above 4% → immediate pause.

### Signal 4: Open Rate Proxy Drops

You can't track opens in plain text emails, but you CAN proxy it:
- Reply rate below 0.5% after 50+ sends = likely spam placement
- Normal cold email reply rate with inbox delivery: 1–4%

### Signal 5: Google Warns You

Gmail will sometimes notify you: "This account has been temporarily suspended."
Or a recipient will forward you a "[SPAM]" tagged version of your email.

---

## Failure Mode 1: Single Inbox Goes to Spam

**Symptoms:**
- One inbox fails delivery test
- Other inboxes still passing
- No Google account suspension

**Response (execute in order):**

```
Hour 0:   Pause n8n routing to affected inbox immediately
          → In Sheets: change all Assigned Inbox = "inbox-X" to a healthy inbox (small batch)

Day 1:    Do NOT send any cold emails from the affected inbox
          Send 10 warm/real emails from it (replies to newsletters, etc.)
          Run mail-tester — note the score

Day 2-4:  Continue warm emails only (10/day)
          No cold sends
          Run mail-tester daily

Day 5:    If mail-tester ≥ 8/10: resume at 5 cold/day
          If mail-tester < 8/10: extend warm-only period by 5 more days

Day 10:   If stable: increase to 10 cold/day
Day 14:   If stable: back to 20 cold/day (full allocation)
```

**Root cause investigation (do this on Day 1):**
- Check the last 20 emails sent from that inbox — any spam words?
- Check bounce rate for that inbox specifically
- Check if you sent to the same domain more than once
- Review send timing — did anything go out in a burst?

---

## Failure Mode 2: High Bounce Rate (> 4%)

**Symptoms:**
- Sent Log shows many `bounced` status entries
- May get a "Mail Delivery Failed" flood in Gmail inbox

**Response:**

```
Immediate:  Stop ALL sends across ALL inboxes
            (high bounces poison sender reputation globally, not per-inbox)

Day 1:      Export all remaining "ready" leads from Sheets
            Run every email through emailvalidation.io (free tier: 100/month)
            Or use Hunter.io email verifier (free tier)
            Delete / mark invalid any that score < 80% confidence

Day 2:      Manually check a sample of 10 bounced emails
            Were they: typos? Format errors (no @)? Domain doesn't exist?
            Fix your sourcing/verification step in the pipeline

Day 3-7:    Resume sending ONLY verified leads
            Start at 10/day per inbox (half capacity)
            Monitor bounce rate daily

Day 8:      If bounce rate back to < 2%: restore full 20/day per inbox
```

**Prevention fix:**
After this event, add an email verification step to your lead intake.
Every email entering the CRM must be verified before status is set to `ready`.

---

## Failure Mode 3: Spam Complaint Received

**Symptoms:**
- A recipient replied angrily asking to be removed
- A recipient reports your email as spam
- You receive a delivery failure with "your message was blocked by the recipient"

**Response:**

```
Immediate:  Add the sender's domain to your Do Not Contact list in Sheets
            (block the entire domain, not just that email)
            Format: add a "Blocked Domains" tab, list @theirdomain.com

Day 1:      Pause the sending inbox for 48 hours (no cold sends)
            Send warm emails only

Day 2:      Review the email you sent — what triggered the complaint?
            Was the subject line aggressive? Was it the third follow-up?
            Adjust copy accordingly

Day 3:      Resume at reduced volume: 10/day for one week, then back to 20/day
```

**Complaint rate targets:**
- < 0.1%: excellent
- 0.1–0.3%: acceptable, monitor
- > 0.3%: serious problem — pause and fix copy

---

## Failure Mode 4: Gmail Account Suspended

**Symptoms:**
- Cannot log in to Gmail
- n8n returns auth error for that credential
- Gmail shows "Account suspended for Terms of Service violation"

**Response:**

```
Immediate:  Go to accounts.google.com/signin/recovery
            Follow Google's appeal process
            Most suspensions are temporary (3–7 days) for first offense

During suspension:
            Reassign all leads from that inbox to other inboxes (at reduced rate)
            Do NOT create a new Gmail account immediately from the same IP
            (Google links accounts by IP — new account = immediate suspicion)

After reinstatement:
Day 1-7:    Use account for real email only. No cold sends.
Day 8-14:   5 cold/day max
Day 15-28:  10 cold/day
Day 29+:    Return to 20/day only if all health checks green
```

**If account is permanently suspended:**
- Accept it — do not try to reuse the address
- Create a replacement account from a different network (mobile data)
- Begin full warm-up from Phase 1
- Keep the suspended account in your records so you never accidentally re-add
  the same leads to a new pipeline

---

## Failure Mode 5: Entire System Goes Cold (All Inboxes Failing)

**Symptoms:**
- All inboxes fail delivery tests simultaneously
- Bounce rate high across all sends
- Reply rate has dropped to near 0%

**This means your email copy or list quality is the problem — not the infrastructure.**

**Response:**

```
Day 1:      Full stop — no sends from any inbox
            Do not touch the inboxes

Day 2-3:    Diagnose the list:
            - What % of the list is unverified?
            - Are you targeting the right emails (contact vs generic info@)?
            - Are you sourcing from a low-quality source?

Day 2-3:    Diagnose the copy:
            - Run your current email through mail-tester.com
            - Score below 8? Fix the copy issues flagged
            - Check for spam words (see deliverability-rules.md)
            - Are you including links in the email? Remove them.

Day 4:      Rebuild: new email template, clean (verified) list of 50 leads
            Test send 5/inbox/day for 1 week

Day 10:     If metrics recover: resume normal schedule
            If still failing: consider whether your offer/targeting is the problem,
            not just the technical setup
```

---

## Preventive Maintenance Calendar

| Frequency | Action |
|---|---|
| Daily | Scan Gmail sent folder — anything look off? |
| Weekly (Friday) | Run mail-tester.com for each inbox |
| Weekly (Friday) | Run delivery test (send to Gmail + Outlook + Yahoo you control) |
| Weekly (Friday) | Calculate bounce rate and reply rate from Sent Log |
| Weekly (Friday) | Check Sheets for any `do-not-contact` updates needed |
| Monthly | Audit lead list — re-verify emails older than 60 days |
| Monthly | Review and refresh email copy (new subject line tests) |
| Monthly | Evaluate whether to add a new inbox (use scaling gates from scaling-roadmap.md) |

---

## Quick Reference: Red Metric → Response

| Red Metric | Immediate Action | Recovery Time |
|---|---|---|
| Bounce rate > 4% | Stop all sends, clean list | 3–7 days |
| Spam complaint | Pause inbox, fix copy | 48 hours + 1-week ramp |
| mail-tester < 6/10 | Pause inbox, fix copy issues | 1–2 weeks |
| Inbox delivery fails | Pause inbox, warm-only mode | 7–14 days |
| Account suspended | Appeal + hold | 7–30 days |
| Reply rate < 0.5% | Fix copy, not infrastructure | 1–2 weeks |
| All inboxes failing | Full stop, diagnose list + copy | 1–3 weeks |
