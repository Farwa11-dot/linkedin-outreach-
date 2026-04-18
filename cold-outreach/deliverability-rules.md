# Safety, Deliverability & Compliance Rules

The most important file in this system. Violate these and your Gmail accounts get suspended,
your emails land in spam, and you lose all the work you put into building the list.

---

## Gmail Sending Limits (Non-Negotiable)

| Account Age | Max Cold Emails/Day | Max Total Emails/Day |
|---|---|---|
| Week 1–2 (warm-up) | 0 cold | 5–10 real only |
| Week 3 (ramp) | 5 cold | 15 total |
| Week 4 | 10 cold | 20 total |
| Month 2+ | 20 cold | 30 total (hard cap) |

**Hard rules:**
- Never send more than 20 cold emails per Gmail account per day
- Space sends at least 3–8 minutes apart (randomized by n8n)
- Never send before 8am or after 6pm recipient's timezone
- Send Monday–Friday only (weekends look automated)
- Never send the same email to the same address twice

---

## Multi-Inbox Distribution Strategy

With 3 Gmail inboxes, you can safely reach 60 leads/day.

**Round-robin assignment:**
```
Inbox 1 (inbox1@gmail.com): Leads A001–A020  → 20 emails/day
Inbox 2 (inbox2@gmail.com): Leads A021–A040  → 20 emails/day
Inbox 3 (inbox3@gmail.com): Leads A041–A060  → 20 emails/day
```

**In Google Sheets:** Column `Assigned Inbox` determines which account n8n uses to send.

**Rotation rule:** Don't let one inbox carry all the load. Distribute evenly.
If one inbox starts getting replies, keep that one for active conversations.
Rotate cold sends to the others.

---

## Email Content: Spam Trigger Avoidance

### Hard Spam Words (Never Use in Subject or Body)
```
FREE, free, Free
Guarantee / guaranteed
Limited time offer
Act now / Don't miss out
Make money / earn money
100% / 100 percent
No cost
Risk-free
Winner / won
Congratulations
Click here
```

### Formatting Rules
- Plain text only — no HTML, no images, no colored text
- No links in cold emails (first touch especially) — links trigger spam filters
- If you must include a link, use it in follow-up 2 only (after some engagement)
- No attachments ever in cold email
- No unsubscribe footer required for 1:1 outreach (but add one for safety if sending > 50/day)
- Keep email under 200 words
- No excessive punctuation (!!!, ???)

### Technical Deliverability
- Send from Gmail only (not a Gmail alias through another SMTP) — stay native
- Use Google's own sending infrastructure
- Do NOT use bulk SMTP tools (SendGrid, Mailgun, etc.) with your Gmail address

---

## Sender Reputation Maintenance

### Monitor These Weekly

**Bounce rate:** Should stay below 2%
- If above 2%: stop sending, verify your list, only resume when clean

**Reply rate:** Aim for 2–8%
- If below 1%: copy problem, not a deliverability problem — rewrite sequences

**Spam complaints:** Should be 0
- One spam complaint per inbox per week is dangerous
- If it happens: pause that inbox for 3 days, review what you sent

### Inbox Health Checks

Every Friday, send a test email from each sending inbox to:
- Your personal Gmail
- A Hotmail/Outlook address
- A Yahoo address

Check: did they land in inbox or spam? If spam → warm-up protocol again for 1 week.

**Free tool:** [mail-tester.com](https://mail-tester.com) — send a test email to their unique address,
get a spam score out of 10. Target: 8+/10.

---

## Warm-Up Strategy (Detailed)

### Phase 1: Account Creation (Day 0)
- Create accounts
- Do NOT send any emails for 48 hours
- Just log in, browse Gmail, set up signature

### Phase 2: Human Activity Simulation (Days 3–7)
- Subscribe to 5–10 newsletters (industry blogs, local news)
- Reply to welcome emails you receive
- Forward emails to yourself between accounts
- Open emails, scroll slowly, click some links
- Log in from different devices if possible (mobile + desktop)

### Phase 3: Ramp-Up (Days 8–14)
- Send 5 real emails per day (to friends, colleagues, yourself on other accounts)
- Reply to any emails you receive
- Still no cold outreach

### Phase 4: Cold Ramp (Days 15–28)
- Start at 5 cold emails/day
- Increase by 5 every 5 days
- Maintain 2–3x more real/warm emails than cold during ramp

### Phase 5: Steady State (Day 29+)
- Max 20 cold emails/day per inbox
- Always keep some real email activity happening (don't let the account go "cold")

---

## Domain Safety (Gmail-Specific)

Since you're using Gmail (not a custom domain), you don't control SPF/DKIM/DMARC.
Google handles this for you. This is actually good — Gmail has strong sender reputation.

However:

**Do NOT:**
- Forward your Gmail through third-party SMTP
- Use Gmail in bulk tools (those tools strip Google's authentication headers)
- Create multiple Gmail accounts from the same IP in quick succession (triggers Google's bot detection)
  - Solution: create accounts over several days, from different networks or incognito + VPN

**DO:**
- Keep each Gmail account active with real human-like behavior
- If you eventually switch to a custom domain:
  - Set up SPF: `v=spf1 include:_spf.google.com ~all`
  - Set up DKIM (Google Workspace handles this)
  - Set up DMARC: `v=DMARC1; p=none; rua=mailto:youremail@yourdomain.com`

---

## CAN-SPAM Compliance (US Law)

For B2B cold email to businesses in the US, CAN-SPAM applies (not GDPR).

**Required by law:**
1. Your physical address in every email — include in signature
2. Honest subject line — no deceptive subjects
3. Clear identification that it's a commercial message (your name + business)
4. Easy way to opt out — include "reply to unsubscribe" in signature

**Not required for B2B cold email (but good practice):**
- Prior consent (GDPR requires this in EU — not CAN-SPAM)
- Unsubscribe link (a "reply to opt out" line in footer is sufficient)

**Sample footer to add to signature:**
```
You're receiving this because your business appears to serve patients
in the local area. Reply "unsubscribe" to never hear from me again.
[Your Name] | [City, State]
```

**If someone replies "unsubscribe" or "stop":**
- Add them to a `Do Not Contact` tab in your Sheets immediately
- Never email them again from any of your inboxes
- This is both legal and ethical

---

## Emergency Playbook

### If Gmail account gets suspended:
1. Go to accounts.google.com → recover the account
2. Do NOT immediately resume sending
3. Wait 5 days, then re-warm for 7 days before resuming
4. Review what you sent before suspension — if it was volume, reduce limits by 50%

### If bounce rate spikes above 5%:
1. Stop sending immediately
2. Export your leads list
3. Run all emails through a free validator (emailvalidation.io)
4. Remove invalid emails
5. Resume only with verified leads

### If open rates seem very low (< 10%):
1. You may be landing in spam — send mail-tester.com check
2. Try switching to a different inbox for 1 week
3. Simplify your email even further (shorter, plainer)
4. Remove any links from the copy
