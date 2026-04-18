# Lead Scoring System — 0 to 10

Score every lead before you email them. High scores get emailed first,
get more follow-up attempts, and get more research time invested.
Low scores sit in the queue until you have capacity.

---

## Why Score Before You Email

Not all clinics are equally worth your time. A practice that:
- Is actively running ads (spending money to acquire patients)
- Has visible operational gaps you can fix
- Has a contact-able owner or manager

...is worth 30 minutes of research and a hand-crafted email.

A practice with no website, generic `info@` email, and no apparent
growth activity is worth 5 minutes maximum.

Scoring forces this decision before you burn time on low-ROI leads.

---

## Scoring Model

Total possible: **10 points** across 5 dimensions.

---

### Dimension 1 — Ad Spend Signals (0–2 pts)

Are they spending money to attract patients? If yes, they are already
convinced that patient acquisition has ROI. They are a warmer buyer.

| Evidence | Points |
|---|---|
| Running Google Ads (visible in Google search for their city + service) | +1 |
| Running Facebook/Instagram Ads (check Meta Ad Library: facebook.com/ads/library) | +1 |
| No paid ads visible anywhere | 0 |

**How to check:**
- Google: search `dentist [their city]` — do they appear in the top sponsored results?
- Meta Ad Library: go to `facebook.com/ads/library` → search their business name → active ads?

**Interpretation:** 2 pts = they are already buying growth. They understand the concept.
They just may not know a better way to capture the leads they're paying for.

---

### Dimension 2 — Service Type & Revenue Potential (0–2 pts)

Higher-ticket services = higher revenue per recovered booking = easier ROI conversation.

| Service Type | Points |
|---|---|
| Cosmetic dentistry / implants / full-mouth restoration | 2 |
| General dentistry + cosmetic mix / orthodontics / Invisalign | 1.5 |
| General dentistry only (cleanings, check-ups) | 1 |
| Med spa / aesthetics: injectables, laser, body contouring | 2 |
| Med spa: facials, basic skincare only | 1 |
| Pure discount / coupon-based practice | 0 |

Round to nearest 0.5. Enter the decimal in the Score Breakdown column.

**Why this matters:** A cosmetic dental practice losing a missed call is losing
a $3,000–$8,000 implant patient. That's a very different conversation from a
practice losing a $150 cleaning appointment.

---

### Dimension 3 — Urgency Signals (0–3 pts)

How acute is their problem right now? More signals = more pain = more motivation to act.

| Signal | Points |
|---|---|
| Google rating below 4.3 stars | +0.5 |
| Fewer than 30 Google reviews (underperforming for their age) | +0.5 |
| No responses to any Google reviews | +0.5 |
| No online booking button on Google Business profile | +0.5 |
| Google Business hours show gaps (closed Saturdays, short hours) | +0.5 |
| Website shows no after-hours contact option | +0.5 |

Max: 3 pts. Add up every signal you observe.

**These signals mean their front desk is a bottleneck.** Every one of these
is a patient who researched them, found friction, and went to a competitor.

---

### Dimension 4 — Website & Digital Presence Quality (0–2 pts)

A poor-quality website signals: (a) the owner doesn't prioritize digital,
which means there's room to help, AND (b) they may have a tech-averse
mindset, which makes selling harder. Read both signals.

| Website Quality | Points |
|---|---|
| Modern, functional, mobile-optimized, has online booking | 0 (no problem to solve here) |
| Functional but missing booking flow or after-hours info | 1 |
| Outdated design, broken on mobile, or very hard to navigate | 1.5 |
| No website, or website is just a Facebook page | 2 (maximum urgency — but harder to sell tech to) |

Note: A 2 here paired with low ad spend (0) and old-school feel = lower
priority than a 2 here with active ads. Context matters.

---

### Dimension 5 — Contact Quality (0–1 pt)

Who are you emailing? The closer to the decision-maker, the better.

| Contact Type | Points |
|---|---|
| Direct owner email (e.g., `dr.smith@clinic.com`) | 1 |
| Office manager or practice manager (named individual) | 0.75 |
| Named staff member | 0.5 |
| Generic `info@`, `hello@`, `contact@` | 0.25 |
| Contact form only (no email found) | 0 |

---

## Score Interpretation

| Score | Tier | Label | Treatment |
|---|---|---|---|
| 8.0 – 10 | 🔴 HOT | Priority | Email within 24h. Max research. Call attempt if no reply by Day 5. |
| 5.5 – 7.5 | 🟠 WARM | Standard | Email within 48–72h. Full sequence. |
| 3.0 – 5.0 | 🟡 COOL | Low Priority | Email when queue is clear. Shorter research. |
| 0 – 2.5 | ⚪ COLD | Skip / Park | Do not email now. Revisit in 60 days or skip entirely. |

---

## Google Sheets Integration

### Add These Columns to Your `Leads` Tab

Insert after column L (Personalization Note):

| Col | Field | Type | Notes |
|---|---|---|---|
| M | `Score: Ads` | Number | 0, 1, or 2 — enter after research |
| N | `Score: Service` | Number | 0–2 in 0.5 increments |
| O | `Score: Urgency` | Number | Sum of urgency signals, max 3 |
| P | `Score: Website` | Number | 0–2 |
| Q | `Score: Contact` | Number | 0–1 in 0.25 increments |
| R | `Lead Score` | Formula | `=SUM(M2:Q2)` — auto-calculates total |
| S | `Priority Tier` | Formula | See formula below |

Shift all existing date/status columns right by 7 columns after adding these.

### Lead Score Formula (Column R)

```
=IFERROR(SUM(M2:Q2), "")
```

### Priority Tier Formula (Column S)

```
=IF(R2="","",
  IF(R2>=8,"🔴 HOT",
    IF(R2>=5.5,"🟠 WARM",
      IF(R2>=3,"🟡 COOL",
        "⚪ COLD"))))
```

### Conditional Formatting — Color the Lead Score Cell

Select column R → Format → Conditional Formatting:

| Condition | Color |
|---|---|
| Greater than or equal to 8 | Red (#ea4335), white text |
| Between 5.5 and 7.9 | Orange (#ff9900), black text |
| Between 3 and 5.4 | Yellow (#fbbc04), black text |
| Less than 3 | Light gray (#efefef), gray text |

### Sort Your Leads View

To always work highest-score first:
1. Select all data (Ctrl+A)
2. Data → Create a filter
3. Click the filter arrow on column R (Lead Score)
4. Sort Z → A (highest first)

Or: Data → Named ranges → save as `ScoredLeads` and apply sort on open.

---

## Scoring Workflow (5 Min Per Lead)

```
1. Open Google Maps → find the clinic
   → check: hours, reviews, review count, booking button, photos
   → score: Urgency (col O)

2. Open their website
   → check: mobile view, booking flow, after-hours info, design quality
   → score: Website (col P), Service type (col N)

3. Google their name in search
   → do they appear in sponsored results?
   → score: Ads (col M)

4. Check Meta Ad Library (facebook.com/ads/library)
   → search business name → any active ads?
   → update: Ads score if found

5. Note the email you found
   → is it owner/direct or generic?
   → score: Contact (col Q)

6. Total auto-calculates in col R → Priority auto-labels in col S
```

Total time: 4–6 minutes per lead. Score before you write. Write before you send.

---

## Scoring Examples

**Example 1: High-Score Lead**

> Coastal Smiles Implant Center — Miami, FL
> - Running Google Ads: yes (+1), no Meta ads (0) → Ads: 1
> - Implants + cosmetic dentistry → Service: 2
> - 3.9 stars, 18 reviews, no review responses, no booking button, closes at 3pm → Urgency: 2.5
> - Website: functional but no booking, poor mobile → Website: 1
> - Found `dr.patel@coastalsmiles.com` → Contact: 1
> **Total: 7.5 — 🟠 WARM. Full sequence. Email within 48h.**

**Example 2: Low-Score Lead**

> Main Street Dentistry — Des Moines, IA
> - No ads → Ads: 0
> - Basic cleanings and check-ups only → Service: 1
> - 4.7 stars, 85 reviews, has booking button, good hours → Urgency: 0
> - Modern website with online booking → Website: 0
> - `info@mainstreetdentistry.com` → Contact: 0.25
> **Total: 1.25 — ⚪ COLD. Skip. They don't have the problem you solve.**

**Example 3: Hot Lead**

> Luxe Aesthetic Studio — Austin, TX
> - Active Facebook and Google Ads → Ads: 2
> - Injectables, laser, body contouring → Service: 2
> - 4.1 stars, 22 reviews, 0 responses, no booking button, closes at 5pm → Urgency: 2.5
> - Outdated website, not mobile-friendly → Website: 1.5
> - Found `jessica@luxeaesthetic.com` (owner's first name on About page) → Contact: 1
> **Total: 9.0 — 🔴 HOT. Email today. Hand-craft the personalization. Call if no reply by Day 5.**
