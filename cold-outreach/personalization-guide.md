# Personalization System — Free Tools Only

Goal: make every email feel individually written without spending hours per lead.
Target: 2–3 minutes of research per lead, one meaningful personalization tag.

---

## The 80/20 Personalization Rule

80% of the email is templated. 20% (one sentence) is personalized.
That one sentence is called the **personalization tag** — it goes in `{{personalization_tag}}`.

You do NOT need to write a custom email per lead. You need to observe one real thing
about their business that shows you actually looked.

---

## Research Process (2–3 min per lead)

### Step 1 — Google Maps Profile (60 seconds)

Search `[clinic name] [city]` on Google Maps. Check:

| Signal | What to look for | Tag to use |
|---|---|---|
| Review count | < 20 reviews | "you don't have many reviews yet — that's a quick win" |
| Review score | 3.5–4.2 stars | "your rating has room to improve with a few more recent reviews" |
| Photos | < 10 photos or old | "your Google profile photos look a bit dated" |
| Responses to reviews | None | "I noticed you don't respond to reviews publicly — that's a trust signal patients check" |
| Business hours | Unusual/limited | "you're closed on Saturdays, which is when a lot of patients prefer to book" |
| Booking button | Missing | "there's no direct booking link on your Google profile" |

### Step 2 — Their Website (60 seconds)

Click through to their website. Scan:

| Signal | What to look for | Tag to use |
|---|---|---|
| Booking flow | Buried or hard to find | "your booking page takes a few clicks to find — most patients drop off" |
| Loyalty/referral program | Not mentioned | "I couldn't find a referral program or loyalty offer anywhere on the site" |
| Before/after gallery | Missing | "there's no before/after gallery — that's often the first thing aesthetic patients look for" |
| Testimonials | None on homepage | "no patient testimonials on your homepage yet" |
| Mobile friendliness | Broken on mobile | "the site looks a bit off on mobile — most patients are searching from their phone" |
| Special offer for new patients | Missing | "no new patient offer visible — that's usually a quick conversion win" |

### Step 3 — Google Business Profile (30 seconds)

Look at their Google Business listing (in Maps sidebar):

| Signal | What to look for | Tag to use |
|---|---|---|
| Posts | No posts in 30+ days | "your Google Business page hasn't had a post in a while" |
| Q&A section | Empty | "the Q&A section on your Google profile is empty — patients do ask questions there" |
| Services list | Empty or sparse | "your services aren't listed on Google, so you're not showing up in those searches" |

---

## Tagging System in Google Sheets

Add a `Personalization Tag` column (Column L in the CRM).

Paste the raw observation — not the polished version. n8n or you will slot it into the template.

**Examples of what to type in Sheets:**
```
only 8 Google reviews
no booking button on Google
photos look old / clinic interior
no referral program on site
not ranking in top 3 local
closed weekends
mobile site broken
no new patient offer
```

Then in your email template, write the personalization tag as a natural sentence:
```
I noticed {{personalization_tag}} — I work with practices on exactly that.
```

---

## Personalization Tiers

Not all leads deserve the same research depth. Tier them:

### Tier 1 — High-value prospects (10 min research)
- Multi-location clinic
- Obvious growth trajectory (new equipment, recent expansion mentioned on site)
- Owner's name visible and verified

Extra steps:
- Check their Instagram: what are they posting? Any engagement problems?
- Check LinkedIn: did the owner post recently?
- Google their name + "interview" or "podcast" — mention it in email

### Tier 2 — Standard prospects (2–3 min research)
- Single-location, typical clinic
- Use the Google Maps + website check above
- One personalization tag is enough

### Tier 3 — Bulk prospects (1 min)
- You only have their business name + email
- Use location-based personalization instead:
  ```
  "I've been working with a few practices in {{city}} recently and thought {{clinic_name}} might be relevant."
  ```
- This is weaker but still better than no personalization

---

## Batch Research Workflow

Research 10 leads at a time. Open 10 browser tabs (Google Maps + website per lead).
Move through them quickly — you're pattern matching, not writing essays.

**Keyboard shortcuts to speed up:**
- `Ctrl+Tab` — cycle browser tabs
- `Ctrl+L` — jump to address bar
- In Sheets: `Ctrl+D` — copy cell down (duplicate tag if same issue across similar clinics)

Time target: 10 leads researched and logged in Sheets in 20–25 minutes.

---

## What NOT to Do

- Do not reference anything personal (family, personal social media, etc.)
- Do not use AI-generated "I loved your post about..." lines — they read as fake
- Do not mention competitors by name
- Do not reference anything that could be wrong (e.g. "I saw you just expanded" if unverified)
- Do not use flattery ("Your clinic is amazing!") — it signals mass outreach immediately
