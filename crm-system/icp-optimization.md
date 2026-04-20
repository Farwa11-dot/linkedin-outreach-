# ICP Optimization Loop

Your Ideal Customer Profile is a hypothesis at the start.
After 60 days of data, it should be a fact.

This system turns your CRM results into weekly refinements to your
targeting, scoring weights, and niche focus — so your pipeline gets
more efficient every month without adding more leads.

---

## What ICP Optimization Actually Means

You started with a guess: "dental and aesthetic clinics in the US,
1–10 staff, running ads, with visible booking gaps."

After 60 days, you have real data. Some sub-segments converted.
Some wasted your time. The optimization loop forces you to look at that
data and adjust:
- Which characteristics predict conversion
- Which niches to increase volume in
- Which to reduce or cut
- Whether your scoring model weights need adjusting

---

## The Four Data Questions

Run these every 4 weeks. Pull answers from your Sheets Dashboard.

**Q1: Which leads converted into calls?**
Look at every lead where Status = `Call Scheduled` or beyond.
What do they have in common? Industry? City? Lead Score range?
Service type? Contact Source?

**Q2: Which replies converted into bookings?**
Filter leads where `Reply Type = Positive` AND `Status = Booked`.
What was their lead score? Industry? City? Which email step generated the reply?

**Q3: Which high-score leads didn't convert?**
Leads with Score 7+ that ended up in `Not Interested` or `Lost`.
What happened? Was it the offer? Timing? Wrong contact? Wrong industry?
These are false positives in your scoring model.

**Q4: Which low-score leads surprised you?**
Leads with Score 4 or below that actually replied and converted.
What was different? This tells you which scoring dimension you're underweighting.

---

## Monthly ICP Review (30 Minutes, First Monday of Each Month)

### Step 1 — Pull the Conversion Data (10 min)

Open your Dashboard tab. Copy this data into a temporary analysis block:

```
[Month] ICP Review

Leads contacted this month:          ___
Replies received:                    ___  (___%)
Calls booked:                        ___  (___% of replies)
Clients closed:                      ___  (___% of calls)

By Industry:
  Dental reply rate:                 ___%
  Aesthetic reply rate:              ___%
  Med Spa reply rate:                ___%

By Lead Score range:
  8–10 reply rate:                   ___%
  5.5–7.5 reply rate:                ___%
  3–5 reply rate:                    ___%

By City (top 3 performing):
  [City 1]:                          ___%
  [City 2]:                          ___%
  [City 3]:                          ___%

By Contact Source:
  Google Maps reply rate:            ___%
  Website scrape reply rate:         ___%
  Referral reply rate:               ___%
```

Fill in from your Dashboard formulas (see `performance-dashboard.md`).

### Step 2 — Identify the Top Converter Segment (5 min)

Which combination of filters produced the highest reply-to-booked rate?

Write it down explicitly:
```
Best performing ICP segment this month:
  Industry:         [e.g., Aesthetic / Med Spa]
  Lead Score range: [e.g., 7–10]
  City type:        [e.g., Miami, Dallas, Austin — Sun Belt cities]
  Contact type:     [e.g., direct owner email]
  Service type:     [e.g., injectables + laser]
```

This is your current best ICP. Next month, bias your sourcing toward this profile.

### Step 3 — Identify the Worst Segment (5 min)

Which segment produced the most activity but fewest conversions?

```
Lowest ROI segment this month:
  Industry:         [e.g., General Dentistry only]
  Score range:      [e.g., 3–5]
  City type:        [e.g., small Midwest markets under 100k population]
  Contact type:     [e.g., generic info@ email]
  Conversion rate:  [e.g., 0.3%]
```

Decision: reduce sourcing from this segment by 50% next month.
Redirect that sourcing time to the best ICP segment above.

### Step 4 — Score Model Adjustment (10 min)

Compare your score model predictions against actual conversion.

**If high-score leads (8+) are converting poorly:**
One of your scoring dimensions is overweighted or miscalibrated.
Look for the common thread among false positives.

Example: "Score: Ads was contributing 2 points, but ad spend alone
doesn't predict conversion — we found that ad spend + website gap
together predicted conversion, not ad spend alone."

Fix: reduce Score: Ads to 1 point maximum. Add a new dimension or
increase weight on a dimension that does predict conversion.

**If low-score leads are converting better than expected:**
You are underweighting something. Look at what the surprising converters
had in common that your model didn't score.

Example: "Service type score wasn't differentiating cosmetic dentistry
from general dentistry well enough — both got 1.5 but cosmetic converted
3× more often."

Fix: increase Score: Service weight for cosmetic/implant practices to 2,
reduce general dentistry to 0.75.

---

## Niche Decision Framework

After each monthly review, make a binary decision for each niche:

| Niche | Conversion Data | Decision |
|---|---|---|
| General Dentistry | < 2% reply rate, low avg case value | Reduce 50% |
| Cosmetic Dentistry / Implants | > 5% reply rate, high case value | Double sourcing |
| Orthodontics / Invisalign | 3% reply rate, medium case value | Maintain |
| Med Spa / Aesthetics | > 6% reply rate, fast close | Prioritize |
| Dermatology (clinical) | < 1% reply rate, long sales cycle | Cut |

**Cut rule:** If a niche produces < 1% reply rate after 50+ sends, it's cut.
Not "reduce" — cut. Stop sourcing leads there entirely.

**Double rule:** If a niche produces > 5% reply rate with > 30% call-to-close,
double sourcing from that niche next month.

You are not trying to serve every clinic. You are trying to find the
30% of the market that converts at 3× the rate and serve them exclusively.

---

## Scoring Model Update Procedure

When you've identified a weight that needs changing:

1. Open `lead-scoring.md`
2. Find the dimension to adjust
3. Update the point values and the interpretation notes
4. In your CRM, update the scoring columns for leads in `New Lead` status
   (re-score them with new weights before sending)
5. Do NOT retroactively re-score leads already in the sequence — it will
   distort your historical analysis

Keep a version log at the bottom of `lead-scoring.md`:
```
## Score Model Changelog
v1.0 (Apr 2026): Initial model
v1.1 (May 2026): Reduced Score:Ads from 2→1 max. Increased Score:Service
                 for cosmetic practices from 1.5→2. Added 0.5 bonus for
                 practices with < 4.3 stars AND no review responses.
```

---

## ICP Feedback Loop in Google Sheets

Add a `ICP Review` tab to your CRM. Structure:

| Col A | Col B | Col C | Col D | Col E |
|---|---|---|---|---|
| Month | Best Segment | Worst Segment | Score Change Made | Lead Target Change |
| Apr 2026 | Aesthetic, 7–10, Miami | General Dental, 3–5, small markets | Ads: 2→1, Service: cosmetic 1.5→2 | +20% aesthetic sourcing, -50% general dental |

This becomes your targeting roadmap. In 6 months you will look back and
see exactly how your ICP evolved — and why your conversion rates improved.

---

## Leading Signals to Track (Predictive ICP Signals)

After 90 days, try to identify the 2–3 signals that most consistently predict conversion.

Common predictors for this offer (missed call / AI receptionist):

| Signal | Why It Predicts Conversion |
|---|---|
| Active Instagram + no booking button on Google | They are investing in awareness but leaking conversions |
| 4.1–4.4 Google star rating | Enough negative signal to make them receptive, not so bad they are in denial |
| Running Google Ads + closed on Saturdays | Paying for traffic that can't book on their busiest inquiry day |
| Cosmetic/implant service mix + < 30 reviews | High patient value, low social proof — growth-minded owner |
| Direct owner email found | Owner is involved in operations — will make decisions quickly |

Once you identify your own top 2–3 predictors from real data, add them as
a pre-scoring filter. Only score leads that match at least 2 of the predictors.
This saves 2–3 minutes of research per lead that was never going to convert.

---

## When to Expand to a New Niche

Do not expand until:
1. Your current best niche is generating 3+ booked calls per month consistently
2. You have a repeatable close process (> 30% demo-to-close)
3. Your current ICP is genuinely saturated in your target cities

When you expand:
- Treat the new niche as a Phase 1 warm-up (first 30 leads are research, not pipeline)
- Build separate email templates for the new niche before sending
- Track it as a separate segment in the Dashboard to avoid polluting your existing data
