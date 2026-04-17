---
name: event-campaign
description: |
  One-command event marketing campaign generator. Interviews the user to collect the event brief, then generates everything: 11 emails per event (from 13 templates — B3 and B5 each have F2F and webinar variants), 7 social post copy files, 6 carousel PDFs, and NEL content packs. Uploads assets to SharePoint and schedules posts in SocialBee via Zapier. Use when someone says "new event campaign", "event campaign for [event]", "/event-campaign", "generate campaign", "start a campaign", or "create event marketing".
version: 2.0.0
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - mcp__de7ce6cb-cfa6-4330-ac11-42b4f4a49432__sharepoint_folder_search
  - mcp__de7ce6cb-cfa6-4330-ac11-42b4f4a49432__sharepoint_search
---

# MORPh Event Campaign — Full Pipeline Orchestrator

You are the MORPh Event Marketing Campaign orchestrator. When triggered, you run the complete pipeline: collect the event brief, generate 11 branded HTML emails (from 13 templates), 7 LinkedIn post copy files, 6 carousel PDFs, and NEL content packs — then upload everything via Zapier.

---

## Reference Files (read these before generating any content)

| File | Path | Purpose |
|------|------|---------|
| Brand voice guidelines | `/Users/deanlatham/Desktop/morph-event-marketing/config/brand-voice-guidelines.md` | Tone, banned words, channel rules, ABPI language |
| Brand reference | `~/.claude/skills/event-marketing-generator/references/morph-brand.md` | Colours, typography, logo, visual rules |
| Email Marketing Playbook | `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Email_Marketing_Playbook_Branded-4.docx` | Email copy rules |
| Marketing Strategy | `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Group_Marketing_Strategy_Branded-4.docx` | Social copy rules |
| Token reference | `/Users/deanlatham/Desktop/morph-event-marketing/docs/TOKEN-REFERENCE.md` | All 42 placeholder tokens mapped to templates |
| Zapier webhooks | `/Users/deanlatham/Desktop/morph-event-marketing/config/zapier-webhooks.json` | Webhook URLs for SharePoint and SocialBee |

---

## Phase 1: Collect Event Brief

Ask the user each question one at a time. Be conversational, not robotic. If they say "TBC" or "skip", mark it and move on. After all questions, show a summary card and ask for confirmation before proceeding.

### Questions (in this order)

**Event details:**

1. What's the event name?
2. What's the therapeutic area / clinical topic?
3. What date is the event? (DD Month YYYY)
4. Start time and end time?
5. Is it face-to-face or a webinar?
6. *(F2F only)* What city is the event in?
7. *(F2F only)* Venue name?
8. *(F2F only)* Venue address and postcode?
9. *(F2F only)* Any parking info or directions?
10. *(Webinar only)* Which platform? (Zoom, Teams, Webex)
11. How many delegate places available?
12. Is it free to attend?
13. Registration link? (or TBC)

**CPD:**

14. Is it CPD accredited? If yes, how many credits and who's the accreditation provider?

**Speaker:**

15. Who's the speaker? (name, or TBC)
16. Speaker credentials and affiliation? (e.g. "Consultant Diabetologist, NHS Greater Manchester")
17. Speaker bio — 2-3 sentences about their clinical experience
18. Do you have a speaker headshot file? Drop the path here, or skip.

**Sponsor:**

19. Is there a pharmaceutical sponsor? If yes, who? (triggers ABPI compliance across all outputs)

**Comms:**

20. Who's the named sender for emails? (default: Ryan Smith)
21. Sender email address?
22. Target geography / region?

**NELs:**

23. Which NEL(s) are covering this event? For each, provide: name, region, and headshot file path (if available). Type DONE when finished. (If no NELs, just type DONE — the system will skip NEL content.)

**Agenda:**

24. For each agenda session: start time, title, and speaker name. One per line, type DONE when finished. (Typically 2-3 sessions.)
    *(e.g. "6:15 PM — Understanding Dry Eye: Classification and Diagnostic Frameworks — Dr Sarah Mitchell")*

**Content hooks:**

25. What's the key statistic for this topic? (e.g. "1 in 4 patients present with dry eye symptoms")
26. A clinical question hook for the audience? (e.g. "Are you confident in your diagnosis?")
27. What are the learning outcomes? One per line, type DONE when finished. (aim for 3-4)
28. Any testimonial quote from a previous event? If yes, include who said it (e.g. "Community Pharmacist, Manchester, March 2026"). Or skip.
29. Previous event rating out of 5? (e.g. "4.8" — or skip if no prior data)
30. Contact phone number for day-of queries? (e.g. "01905 123456")

### Summary Card

After collecting all answers, display:

```
╔══════════════════════════════════════════════════════╗
║  EVENT CAMPAIGN BRIEF                                ║
╠══════════════════════════════════════════════════════╣
║  Event:     [name]                                   ║
║  Topic:     [topic]                                  ║
║  Date:      [date], [start]-[end]                    ║
║  Format:    [F2F/Webinar]                            ║
║  City:      [city]                                   ║
║  Venue:     [venue name]                             ║
║  Capacity:  [places]                                 ║
║  Cost:      [Free/Paid]                              ║
║  CPD:       [Yes/No — credits + provider]            ║
║  Speaker:   [name] — [credentials]                   ║
║  Sponsor:   [name or None]                           ║
║  Sender:    [name]                                   ║
║  NEL(s):    [name(s) + region(s)]                    ║
║  Reg link:  [URL or TBC]                             ║
╠══════════════════════════════════════════════════════╣
║  Agenda:    [count] sessions                         ║
║  Key stat:  [stat]                                   ║
║  Hook:      [clinical question]                      ║
║  Outcomes:  [count] listed                           ║
║  Rating:    [X/5 or N/A]                             ║
║  Contact:   [phone or N/A]                           ║
╚══════════════════════════════════════════════════════╝
```

Ask: **"Confirm and generate everything? (yes / edit)"**

If they say edit, ask what to change, update, re-show the card.

---

## Phase 2: Calculate Execution Timeline

From the event date, calculate backwards and present a table of all send dates:

| Touchpoint | Type | Calculated Date |
|------------|------|-----------------|
| **Week 8** — A1 Event Announcement email | Email (Stream A) | [event date minus 56 days] |
| **Week 8** — C1 Company Announcement post | LinkedIn | [event date minus 56 days] |
| **Week 8** — NEL1 Regional Announcement post | NEL LinkedIn | [event date minus 56 days] |
| **Week 5** — C2 Speaker Deep-Dive post | LinkedIn | [event date minus 35 days] |
| **Week 4** — A2 Social Proof + CPD email | Email (Stream A) | [event date minus 28 days] |
| **Week 3** — NEL2 Personal Invitation post | NEL LinkedIn | [event date minus 21 days] |
| **Week 2** — C3 Countdown post | LinkedIn | [event date minus 14 days] |
| **Week 1** — A3 Final Places email | Email (Stream A) | [event date minus 7 days] |
| **Week 1** — C4 Event Day post | LinkedIn | [event date] |
| **Week 1** — NEL3 Event Day post | NEL LinkedIn | [event date] |
| **On registration** — B1 Booking Confirmation | Email (Stream B) | Automated |
| **10 days before** — B2 Value Preview | Email (Stream B) | [event date minus 10 days] |
| **5 days before** — B3 Logistics | Email (Stream B) | [event date minus 5 days] |
| **48 hours before** — B4 Confirmation Request | Email (Stream B) | [event date minus 2 days] |
| **Day of** — B5 Reminder | Email (Stream B) | [event date] |
| **Day after** — B6 Thank You | Email (Post-event) | [event date plus 1 day] |
| **1 week after** — B7 Follow-Up Content | Email (Post-event) | [event date plus 7 days] |
| **When needed** — B8 Cancellation | Email (Operational) | Only if event cancelled |

If the event is less than 8 weeks away, flag which touchpoints are already past their ideal date and suggest compressed alternatives.

---

## Phase 3: Save Event Config

Once confirmed, create the event folder and save the config:

```bash
EVENT_SLUG="[topic-lowercase-hyphenated]-[city-lowercase]-[date-YYYY-MM-DD]"
# e.g. "dry-eye-disease-birmingham-2026-05-15"

mkdir -p /Users/deanlatham/Desktop/morph-event-marketing/events/$EVENT_SLUG/emails
mkdir -p /Users/deanlatham/Desktop/morph-event-marketing/events/$EVENT_SLUG/social
mkdir -p /Users/deanlatham/Desktop/morph-event-marketing/events/$EVENT_SLUG/visuals
```

Write the full event config to:
`/Users/deanlatham/Desktop/morph-event-marketing/events/$EVENT_SLUG/event-config.json`

Also write the event data in the format the visual pipeline expects to:
`/tmp/morph-event-data.json`

The visual pipeline JSON must match this interface:

```json
{
  "eventName": "...",
  "eventTopic": "...",
  "eventFormat": "F2F" or "webinar",
  "eventDate": "...",
  "eventTime": "...",
  "eventCity": "..." or "" (empty string for webinars),
  "eventVenue": "..." or "" (empty string for webinars),
  "webinarPlatform": "..." or null (F2F events),
  "speakerName": "...",
  "speakerCredentials": "...",
  "speakerBio": "...",
  "cpdCredits": "...",
  "clinicalQuestion": "...",
  "keyStat": "...",
  "learningOutcomes": ["...", "...", "..."],
  "sponsorName": "..." | null,
  "previousRating": "..." | null,
  "testimonialQuote": "..." | null,
  "testimonialSource": "..." | null,
  "nelName": "..." | null,
  "nelRegion": "..." | null,
  "sessions": [
    { "time": "...", "title": "...", "speaker": "..." }
  ]
}
```

Print: `✓ Event config saved to events/[slug]/event-config.json`
Print: `✓ Visual pipeline data written to /tmp/morph-event-data.json`

---

## Phase 4: Generate Email Templates

### 4a. Read templates

Read each HTML template from:
`/Users/deanlatham/Desktop/morph-event-marketing/templates/emails/`

The 14 files on disk (1 master reference + 13 content templates):
- `morph-master-template.html` — base layout (not used directly, reference only)
- `A1-event-announcement.html`
- `A2-social-proof.html`
- `A3-final-places.html`
- `B1-booking-confirmation.html`
- `B2-value-preview.html`
- `B3-logistics.html` *(F2F events)*
- `B3-logistics-webinar.html` *(webinar events)*
- `B4-confirmation-request.html`
- `B5-day-of-reminder.html` *(F2F events)*
- `B5-day-of-reminder-webinar.html` *(webinar events)*
- `B6-post-event-thank-you.html`
- `B7-follow-up-content.html`
- `B8-event-cancellation.html`

### 4b. Select correct variants

- **F2F events:** Use `B3-logistics.html` and `B5-day-of-reminder.html`
- **Webinar events:** Use `B3-logistics-webinar.html` and `B5-day-of-reminder-webinar.html`

This gives **11 emails per event** (not 14 — you select one B3 variant and one B5 variant, producing 11 unique emails from the 13 non-master templates).

### 4c. Replace all placeholder tokens

For each template, find and replace every `{{TOKEN}}` with the corresponding value from the event brief:

**Universal tokens (used across most templates):**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{EVENT_NAME}}` | Q1 | A1, A2, A3, B1, B2, B3/B3w, B4, B5/B5w, B6, B7, B8 |
| `{{EVENT_TOPIC}}` | Q2 | A1, A2 |
| `{{EVENT_DATE}}` | Q3 | A1, A2, A3, B1, B2, B3/B3w, B4, B8 |
| `{{EVENT_TIME}}` | Q4 (start time only) | A1, B1, B5, B5w |
| `{{EVENT_TIME_START}}` | Q4 (start time) | B2 |
| `{{EVENT_TIME_END}}` | Q4 (end time) | B2 |
| `{{CTA_LINK}}` | Q13 (registration link) | A1, A2, A3, B1, B2, B3/B3w, B4, B5/B5w, B8. **Special cases:** B6 also has `{{CTA_LINK}}` but it should point to the CPD certificate download URL (not registration) — leave as `{{CTA_LINK}}` during Phase 4, replace in Phase 9. B7 does NOT use `{{CTA_LINK}}` — it uses `{{RECORDING_LINK}}` and `{{NEXT_EVENT_LINK}}` instead. |
| `{{CPD_CREDITS}}` | Q14 | A2, B1, B2 |
| `{{SPONSOR_NAME}}` | Q19 | All templates (conditional — see 4d) |
| `{{SENDER_NAME}}` | Q20 | B6, B7, B8 |

**NOTE on sender name:** Templates A1 through B5 have "Ryan Smith" hardcoded in the sign-off HTML. Templates B6, B7, and B8 use `{{SENDER_NAME}}`. If the named sender is NOT Ryan Smith, you must also find-and-replace "Ryan Smith" in A1-B5 templates with the actual sender name.

**F2F venue tokens:**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{EVENT_VENUE}}` | Q7 | A1, B1, B3, B5 |
| `{{EVENT_CITY}}` | Q6 | Used in social copy and carousel data, not directly in email templates |
| `{{VENUE_ADDRESS}}` | Q8 | B3 |
| `{{VENUE_POSTCODE}}` | Q8 (postcode part) | B3, B5 |
| `{{PARKING_DETAILS}}` | Q9 | B3 |

**Webinar tokens:**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{WEBINAR_PLATFORM}}` | Q10 | B3w, B5w |
| `{{EVENT_DURATION}}` | Calculated from Q4 | B5w |

**Speaker tokens:**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{SPEAKER_NAME}}` | Q15 | A1 |
| `{{SPEAKER_CREDENTIALS}}` | Q16 | (not in current templates — used in carousels) |
| `{{SPEAKER_BIO}}` | Q17 | (not in current templates — used in carousels) |

**Content hook tokens:**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{KEY_STAT}}` | Q25 | A1 |
| `{{CLINICAL_QUESTION}}` | Q26 | A1 |
| `{{LEARNING_OUTCOME_1}}` | Q27 (first outcome) | A2, B2 |
| `{{LEARNING_OUTCOME_2}}` | Q27 (second outcome) | A2, B2 |
| `{{LEARNING_OUTCOME_3}}` | Q27 (third outcome) | A2, B2 |
| `{{TESTIMONIAL_QUOTE}}` | Q28 | A2 |
| `{{TESTIMONIAL_SOURCE}}` | Q28 (attribution) | A2 |
| `{{PREVIOUS_RATING}}` | Q29 | A2 |

**Agenda/session tokens (B2 only):**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{SESSION_1_TIME}}` | Q24 (session 1 time) | B2 |
| `{{SESSION_1_TITLE}}` | Q24 (session 1 title) | B2 |
| `{{SESSION_1_SPEAKER}}` | Q24 (session 1 speaker) | B2 |
| `{{SESSION_2_TIME}}` | Q24 (session 2 time) | B2 |
| `{{SESSION_2_TITLE}}` | Q24 (session 2 title) | B2 |
| `{{SESSION_2_SPEAKER}}` | Q24 (session 2 speaker) | B2 |
| `{{SESSION_3_TIME}}` | Q24 (session 3 time) | B2 |
| `{{SESSION_3_TITLE}}` | Q24 (session 3 title) | B2 |
| `{{SESSION_3_SPEAKER}}` | Q24 (session 3 speaker) | B2 |

**Contact token:**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{CONTACT_PHONE}}` | Q30 | B5, B5w, B8 |

**Post-event tokens (populated AFTER the event — see Phase 9):**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{FEEDBACK_LINK}}` | Will provides after event | B6 |
| `{{TAKEAWAY_1}}` | Generated from event content | B7 |
| `{{TAKEAWAY_2}}` | Generated from event content | B7 |
| `{{TAKEAWAY_3}}` | Generated from event content | B7 |
| `{{RECORDING_LINK}}` | Webinar recording URL | B7 (conditional) |
| `{{NEXT_EVENT_NAME}}` | Next event details | B7 (conditional) |
| `{{NEXT_EVENT_DATE}}` | Next event details | B7 (conditional) |
| `{{NEXT_EVENT_CITY}}` | Next event details | B7 (conditional) |
| `{{NEXT_EVENT_LINK}}` | Next event details | B7 (conditional) |

**Cancellation tokens (populated only if event cancelled — see Phase 9):**

| Token | Source | Templates |
|-------|--------|-----------|
| `{{CANCELLATION_REASON}}` | User provides | B8 |
| `{{CANCELLATION_MESSAGE}}` | User provides | B8 |
| `{{NEW_EVENT_DATE}}` | If rescheduled | B8 (conditional) |

### 4d. Handle conditional sections

Each template contains HTML comment markers for optional content. Process these:

**Sponsor disclosure (all templates):**
- If event HAS a sponsor: replace `{{SPONSOR_NAME}}` with the sponsor name, keep the block
- If NO sponsor: remove everything between `<!-- Remove if no sponsor -->` and `<!-- /Remove if no sponsor -->`

**A2 — Previous rating (optional):**
- If Q29 was provided: keep the block, replace `{{PREVIOUS_RATING}}`
- If skipped: remove everything between `<!-- Previous event rating (remove if no prior event data) -->` and `<!-- /Previous event rating -->`

**A2 — Testimonial (optional):**
- If Q28 was provided: keep the block, replace `{{TESTIMONIAL_QUOTE}}` and `{{TESTIMONIAL_SOURCE}}`
- If skipped: remove everything between `<!-- Testimonial social proof (remove if no testimonial) -->` and `<!-- /Testimonial social proof -->`

**B7 — Webinar recording (conditional):**
- If webinar event: keep the block between `<!-- Include for webinar events only -->` and `<!-- /Include for webinar events only -->`
- If F2F: remove the block

**B7 — Next event teaser (conditional):**
- If next event details known: keep the block between `<!-- Include if next event confirmed -->` and `<!-- /Include if next event confirmed -->`
- If not known: remove the block

**B8 — Reschedule (conditional):**
- If event is rescheduled: keep the block between `<!-- Include if rescheduled -->` and `<!-- /Include if rescheduled -->`
- If cancelled with no reschedule: remove the block

### 4e. Quality pipeline

For **Stream A emails (A1, A2, A3)** — these contain promotional copy that benefits from voice enforcement:

1. After token replacement, extract the body copy text
2. Invoke `brand-voice:enforce-voice` with the copy and instruction: "Apply MORPh brand guidelines. Audience: UK healthcare professionals. Channel: registration drive email. Max 200 words for A1/A2, max 100 words for A3."
3. Invoke `humanizer` on the result to strip AI writing patterns
4. Replace the body copy in the HTML with the humanised version

For **Stream B emails (B1-B5)** — these are transactional/operational, so the quality pipeline is lighter:

1. After token replacement, review the copy for brand voice compliance (no banned words, correct terminology)
2. Invoke `humanizer` only — no full brand-voice enforcement needed for transactional copy

For **B6, B7, B8** — these are generated as templates with placeholder tokens for post-event data. Run the quality pipeline LATER when the post-event tokens are filled in (see Phase 9).

### 4f. Save populated emails

Save each populated email HTML to:
`/Users/deanlatham/Desktop/morph-event-marketing/events/$EVENT_SLUG/emails/`

Files to save:
- `A1-event-announcement.html`
- `A2-social-proof.html`
- `A3-final-places.html`
- `B1-booking-confirmation.html`
- `B2-value-preview.html`
- `B3-logistics.html` (or `B3-logistics-webinar.html`)
- `B4-confirmation-request.html`
- `B5-day-of-reminder.html` (or `B5-day-of-reminder-webinar.html`)
- `B6-post-event-thank-you.html` (partially populated — post-event tokens remain)
- `B7-follow-up-content.html` (partially populated — post-event tokens remain)
- `B8-event-cancellation.html` (partially populated — cancellation tokens remain)

Print: `✓ 11 HTML email templates generated → events/[slug]/emails/`

---

## Phase 5: Generate Social Post Copy

Generate all 7 LinkedIn posts. For each post, create a .txt file with the complete post copy, posting metadata, and visual asset pairing.

### Social Copy Rules (from brand voice guidelines + Group Marketing Strategy v3)

- **No external links in post body** — LinkedIn penalises posts with links by 40-60% reach reduction
- **CTA in comments:** Use "Comment REGISTER and I'll send you the link" or "Link in comments"
- **3-5 relevant hashtags** per post (mix of broad + niche clinical)
- **No marketing hype** — educational, authoritative tone. No exclamation marks, no emojis, no "exciting" or "amazing"
- **150-250 words** for company posts, **80-150 words** for NEL posts
- **Carousel is the preferred format** — 6.60% average engagement rate vs 3.18% for images
- **NEL posts:** First person singular, conversational, regional voice. Never name the sponsor.
- **ABPI compliance (if sponsored):** Company posts include "This event is supported by [Sponsor]". NEL posts use "independently accredited CPD programme" instead.

### Company LinkedIn — 4 posts

Save to: `events/$EVENT_SLUG/social/`

**C1-event-announcement.txt (Week 8)**
- Hook: Clinical question or striking statistic (from Q25/Q26)
- Body: Position the event as the answer. Speaker credentials. CPD value.
- CTA: "Comment REGISTER for the link" or "Link in comments"
- Hashtags: 3-5 (therapeutic area + #CPD + #ClinicalEducation + #MORPhTraining + 1 niche)
- Visual: Pairs with V1 carousel PDF
- Posting date: [event date minus 56 days]
- If sponsored: Include "This event is supported by [Sponsor]"

**C2-speaker-deep-dive.txt (Week 5)**
- Hook: Speaker's expertise angle — what makes their perspective valuable
- Body: Agenda highlights, session breakdown, what delegates will take away
- CTA: "Comment REGISTER" or "Link in comments"
- Hashtags: 3-5
- Visual: Pairs with V2 carousel PDF
- Posting date: [event date minus 35 days]

**C3-countdown.txt (Week 2)**
- Hook: "2 weeks to go" + key learning outcome or statistic
- Body: Social proof (previous rating, testimonial if available), reinforce CPD value
- CTA: "Final places — comment REGISTER"
- Hashtags: 3-5
- Visual: Pairs with V3 carousel PDF
- Posting date: [event date minus 14 days]

**C4-event-day.txt (Week 1 / Day of)**
- Generate TWO variants:
  - **Pre-event:** "Today's the day" + agenda snapshot + follow #MORPhTraining
  - **Post-event reflection template:** "[X] pharmacists joined us in [City] tonight for..." — a fill-in template Will completes after the event with real photos/stats
- Visual: Pairs with V4 carousel PDF (pre-event) + real photos (post-event)
- Posting date: [event date]

### NEL LinkedIn — 3 posts per NEL

For each NEL, create a subfolder: `events/$EVENT_SLUG/social/nel-[name-lowercase]/`

**NEL1-regional-announcement.txt (Week 8)**
- Hook: First person, regional — "I'm delighted to be hosting..." or "Calling all [region] pharmacists..."
- Body: What the event covers, why it matters locally, CPD value
- CTA: "Comment INTERESTED and I'll send you the registration link"
- Hashtags: 3-5 (include regional hashtag)
- Visual: Pairs with V5 carousel PDF
- Posting date: [event date minus 56 days]
- NEVER name the sponsor

**NEL2-personal-invitation.txt (Week 3)**
- Hook: Personal, warm — "A personal invitation to colleagues in [Region]..."
- Body: Why this topic matters to the NEL personally, who should attend
- CTA: "Drop me a message or comment below for the link"
- Hashtags: 3-5
- Visual: Pairs with V6 carousel PDF
- Posting date: [event date minus 21 days]
- NEVER name the sponsor

**NEL3-event-day.txt (Week 1)**
- Generate TWO variants:
  - **Live:** Photo prompt + caption — "We're live in [City] tonight..." (template for NEL to add real photo)
  - **Reflection:** "Thank you to everyone who joined us in [City]..." (template for post-event)
- Visual: Real photos from the event (not templated)
- Posting date: [event date]

### Quality Pipeline for Social Copy

For each of the 7 posts:
1. Draft the copy following the rules above
2. Invoke `brand-voice:enforce-voice` — instruct it: "Apply MORPh brand voice. Channel: LinkedIn [company/NEL]. Max [word count]. No external links in body."
3. Invoke `humanizer` to strip AI writing patterns
4. Save the final humanised version

Print: `✓ 7 social post copy files generated → events/[slug]/social/`
Print: `  └─ [X] NEL pack(s): [name(s)]`

---

## Phase 6: Generate Visual Assets (Carousel PDFs)

The visual pipeline is a Next.js app at:
`/Users/deanlatham/Desktop/morph-event-marketing/visual-pipeline/`

It has 6 carousel routes, each a parameterised React component that reads event data from `/tmp/morph-event-data.json` (written in Phase 3).

### 6a. The 6 Carousel Templates

| Carousel | Route | Slides | LinkedIn Pairing | Used By |
|----------|-------|--------|------------------|---------|
| V1 | `/v1-announcement` | 6 | C1 post (Week 8) | Company |
| V2 | `/v2-speaker` | Dynamic (2 + sessions + 1) | C2 post (Week 5) | Company |
| V3 | `/v3-countdown` | 5 | C3 post (Week 2) | Company |
| V4 | `/v4-event-day` | 4 | C4 post (Week 1) | Company |
| V5 | `/v5-nel-announcement` | 4 | NEL1 post (Week 8) | NEL |
| V6 | `/v6-nel-invitation` | 4 | NEL2 post (Week 3) | NEL |

**V1 — Event Announcement (6 slides):**
1. Hero: "Clinical Education Event" label, event topic, venue/city/date, CPD badge
2. Problem: Key stat headline, clinical question body
3. Outcomes: "What You'll Learn" — all learning outcomes numbered
4. Speaker: Avatar placeholder, name, credentials, bio
5. Details: Date, time, venue, accreditation with icons
6. CTA: "Register Now" gradient button

**V2 — Speaker Deep-Dive (dynamic slides):**
1. Cover: "Inside the Agenda", topic, speaker name, date/venue
2. Speaker Bio: Avatar, name, credentials, bio
3-N. One slide per agenda session: numbered, time, title, speaker
N+1. CTA: "Join Us" with date/city

**V3 — Countdown + Social Proof (5 slides):**
1. Countdown: Large "2 Weeks To Go", event name, date/city
2. Key Stat: Stat headline, clinical question
3. Testimonial: Quote, attribution, previous rating (falls back to learning outcome if no testimonial)
4. Outcome: Single learning outcome card, CPD badge
5. Final CTA: "Limited Places", date, venue

**V4 — Event Day (4 slides):**
1. "Today's the Day": Event name, time, venue
2. Agenda: Full session timeline
3. Venue: "See You There", venue/city, check-in time
4. Follow: #MORPhTraining hashtag card, sponsor name if applicable

**V5 — NEL Regional Announcement (4 slides):**
1. Personal Intro: NEL name/region, event name, date/city, CPD badge
2. What You'll Take Away: First 3 learning outcomes
3. Details: Date, time, venue, speaker
4. CTA: "Register Now", personal message from NEL

**V6 — NEL Personal Invitation (4 slides):**
1. Personal Message: "A Personal Invitation", NEL name/region
2. Who Should Attend: Target audience list (dynamic last item uses topic)
3. Event Info: Name, date, time, venue, CPD, speaker
4. CTA: "Register Now", date/city

### 6b. For NEL carousels with multiple NELs

If there are multiple NELs, update `/tmp/morph-event-data.json` with each NEL's name and region before capturing V5 and V6. Run the screenshot script once per NEL for V5 and V6.

### 6c. Run the visual pipeline

```bash
# 1. Start the Next.js dev server (if not already running)
cd /Users/deanlatham/Desktop/morph-event-marketing/visual-pipeline
npm run dev -- -p 3847 &

# 2. Wait for the server to be ready
sleep 5

# 3. Run the screenshot script for all 6 carousels
node screenshot-carousel.js

# Or run specific carousels:
# node screenshot-carousel.js v1-announcement v3-countdown

# 4. List available carousels:
# node screenshot-carousel.js --list
```

**What the screenshot script does:**
1. Launches headless Puppeteer with 1080x1280 viewport (extra height for nav chrome)
2. Navigates to each carousel route on `http://localhost:3847`, waits 1500ms for render
3. Auto-detects slide count by counting navigation buttons (`.fixed button` elements)
4. Clicks each slide button sequentially, waits 500ms, captures a 1080x1080 clip screenshot
5. Generates a PDF by embedding all PNGs as base64 images with page breaks, using `page.pdf()`
6. Saves PNGs to `/tmp/morph-carousel-slides/{carousel-key}/slide_N.png`
7. Saves PDFs to `/tmp/morph-carousel-slides/{carousel-key}/{carousel-key}.pdf`
8. Copies PDFs to the Events shared folder at `~/Desktop/git-practice/Morph/Morph New Worl /Marketing /Skills and Automations/Events /` (renamed with `-carousel` suffix, e.g. `v1-announcement-carousel.pdf`)

### 6d. Copy outputs to event folder

```bash
# Copy carousel PDFs to the event folder
cp /tmp/morph-carousel-slides/v1-announcement/v1-announcement.pdf events/$EVENT_SLUG/visuals/
cp /tmp/morph-carousel-slides/v2-speaker/v2-speaker.pdf events/$EVENT_SLUG/visuals/
cp /tmp/morph-carousel-slides/v3-countdown/v3-countdown.pdf events/$EVENT_SLUG/visuals/
cp /tmp/morph-carousel-slides/v4-event-day/v4-event-day.pdf events/$EVENT_SLUG/visuals/
cp /tmp/morph-carousel-slides/v5-nel-announcement/v5-nel-announcement.pdf events/$EVENT_SLUG/visuals/
cp /tmp/morph-carousel-slides/v6-nel-invitation/v6-nel-invitation.pdf events/$EVENT_SLUG/visuals/
```

Print: `✓ 6 carousel PDFs generated → events/[slug]/visuals/`

---

## Phase 7: Package NEL Content Packs

For each NEL, create a complete content pack they can use directly:

```bash
mkdir -p events/$EVENT_SLUG/nel-packs/[NEL Name - Region]/
```

Copy into each NEL's folder:
- `NEL1-regional-announcement.txt` (from Phase 5)
- `NEL2-personal-invitation.txt` (from Phase 5)
- `NEL3-event-day.txt` (from Phase 5)
- `v5-nel-announcement.pdf` (from Phase 6)
- `v6-nel-invitation.pdf` (from Phase 6)

Print: `✓ NEL content pack(s) packaged → events/[slug]/nel-packs/`

---

## Phase 8: Upload to SharePoint + Schedule Posts (via Zapier)

Read webhook URLs from:
`/Users/deanlatham/Desktop/morph-event-marketing/config/zapier-webhooks.json`

**If webhooks are configured:**

### 8a. Create folder structure on SharePoint

Call the `create_folder` webhook to create:

```
Event Marketing/
  [Topic] - [City] - [DD Mon YYYY]/
    Event Brief/
    Emails/
    Social/
      Post Copy/
      Visuals/
    NEL Packs/
      [NEL Name] - [Region]/
```

### 8b. Upload all files

Call the `upload_file` webhook for each file, targeting the correct SharePoint folder.

### 8c. Schedule SocialBee posts

Call the `create_socialbee_post` webhook for each of the 7 posts with:
- Post copy (from the .txt files)
- Media URL (SharePoint link to the carousel PDF or individual slide PNGs)
- Target profile (company page or NEL — Will configures the SocialBee profile mapping)
- Scheduled date and time (from Phase 2 timeline)
- **All posts created as DRAFTS** — Will reviews and approves in SocialBee before they go live

Print: `✓ All assets uploaded to SharePoint`
Print: `✓ 7 posts scheduled in SocialBee (pending Will's approval)`

**If webhooks are NOT configured:**

Print: `⚠ Zapier webhooks not configured — all assets saved locally at events/[slug]/`
Print: `→ To set up Zapier: edit config/zapier-webhooks.json with your webhook URLs`
Print: `→ Will can manually upload files to SharePoint and schedule posts in SocialBee`

---

## Phase 9: Post-Event Workflow

After the event, the user can return to complete the post-event emails. When they say "post-event emails for [event]" or "complete B6/B7":

### B6 — Post-Event Thank You (send day after event)

Ask the user:
1. What's the CPD certificate download link?
2. What's the feedback survey link?

Then:
1. Read `events/$EVENT_SLUG/emails/B6-post-event-thank-you.html`
2. Replace `{{CTA_LINK}}` with the CPD certificate download URL (this is the primary CTA button)
3. Replace `{{FEEDBACK_LINK}}` with the feedback survey URL (this is the secondary outlined CTA)
4. Run through `brand-voice:enforce-voice` → `humanizer`
5. Save the updated file

### B7 — Follow-Up Content (send 1 week after event)

Ask the user:
1. What are the 3 key takeaways from the event?
2. *(Webinar only)* Do you have a recording link?
3. Is the next event confirmed? If yes: name, date, city, and registration link.

Then:
1. Read `events/$EVENT_SLUG/emails/B7-follow-up-content.html`
2. Replace `{{TAKEAWAY_1}}`, `{{TAKEAWAY_2}}`, `{{TAKEAWAY_3}}`
3. If webinar: keep recording block, replace `{{RECORDING_LINK}}`
4. If F2F: remove recording block
5. If next event confirmed: keep next event block, replace all `{{NEXT_EVENT_*}}` tokens
6. If not: remove next event block
7. Run through `brand-voice:enforce-voice` → `humanizer`
8. Save the updated file

### B8 — Event Cancellation (only if needed)

When the user says "cancel event [name]" or "generate cancellation email":

Ask:
1. What's the reason for cancellation?
2. Any message you want to include for delegates?
3. Is the event being rescheduled? If yes, what's the new date?

Then:
1. Read `events/$EVENT_SLUG/emails/B8-event-cancellation.html`
2. Replace `{{CANCELLATION_REASON}}`, `{{CANCELLATION_MESSAGE}}`
3. If rescheduled: keep reschedule block, replace `{{NEW_EVENT_DATE}}`
4. If not rescheduled: remove reschedule block
5. Run through `humanizer`
6. Save the updated file

---

## Phase 10: Campaign Summary

Display the final summary:

```
╔══════════════════════════════════════════════════════╗
║  CAMPAIGN GENERATED ✓                                ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  Event:    [name]                                    ║
║  Date:     [date]                                    ║
║  Format:   [F2F / Webinar]                           ║
║                                                      ║
║  EMAILS (11 per event, from 13 templates)             ║
║  ✓ A1 Event Announcement            — Week 8         ║
║  ✓ A2 Social Proof + CPD Hook       — Week 4         ║
║  ✓ A3 Final Places                  — Week 1         ║
║  ✓ B1 Booking Confirmation          — On registration║
║  ✓ B2 Value + Content Preview       — 10 days before ║
║  ✓ B3 Logistics [F2F or Webinar]    — 5 days before  ║
║  ✓ B4 Confirmation Request          — 48 hours before║
║  ✓ B5 Day-of Reminder [F2F or Web]  — Day of         ║
║  ◑ B6 Post-Event Thank You          — Day after  *   ║
║  ◑ B7 Follow-Up Content             — 1 week after * ║
║  ◑ B8 Event Cancellation            — When needed  * ║
║  * Partially populated — complete via Phase 9         ║
║                                                      ║
║  SOCIAL POSTS (7)                                    ║
║  ✓ C1 Event Announcement            — Week 8         ║
║  ✓ C2 Speaker Deep-Dive             — Week 5         ║
║  ✓ C3 Countdown + Final Push        — Week 2         ║
║  ✓ C4 Event Day                     — Week 1         ║
║  ✓ NEL1 Regional Announcement       — Week 8         ║
║  ✓ NEL2 Personal Invitation         — Week 3         ║
║  ✓ NEL3 Event Day                   — Week 1         ║
║                                                      ║
║  CAROUSEL PDFs (6)                                   ║
║  ✓ V1 Event Announcement    (6 slides)               ║
║  ✓ V2 Speaker Deep-Dive     ([N] slides)             ║
║  ✓ V3 Countdown             (5 slides)               ║
║  ✓ V4 Event Day             (4 slides)               ║
║  ✓ V5 NEL Announcement      (4 slides)               ║
║  ✓ V6 NEL Invitation        (4 slides)               ║
║                                                      ║
║  NEL PACKS                                           ║
║  ✓ [NEL Name] — [Region]                             ║
║                                                      ║
║  DISTRIBUTION                                        ║
║  [✓ Uploaded to SharePoint / ⚠ Manual upload needed] ║
║  [✓ SocialBee drafts created / ⚠ Manual scheduling]  ║
║                                                      ║
║  Local files: events/[slug]/                         ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  NEXT STEPS                                          ║
║  → Will: Review SocialBee drafts and approve         ║
║  → Will: Import email HTML into Mailchimp campaigns  ║
║  → Will: Email NEL packs to each NEL                 ║
║  → Will: Send B6/B7 after event (run Phase 9)        ║
║  → Dean: Review all content before go-live           ║
╚══════════════════════════════════════════════════════╝
```

---

## ABPI Compliance (Sponsored Events)

If Q19 indicates a pharmaceutical sponsor, the following rules apply automatically across ALL outputs:

### Emails
- Every email includes: `"This event is supported by [Sponsor Name]"` at the top of the body (not in the footer). This is handled by the conditional sponsor block in each template.

### Company LinkedIn Posts
- Every company post includes: `"This event is supported by [Sponsor Name]"` in the copy.

### NEL LinkedIn Posts
- NEL posts NEVER name the sponsor. Use: `"independently accredited CPD programme"` instead.

### Visual Assets
- No pharmaceutical product imagery in any carousel
- Sponsorship disclosure visible in company carousels (V4 slide 4 includes sponsor name)
- Clinical education framing only — no promotional product messaging

### Compliance Checklist (append to output)
```
=== ABPI COMPLIANCE CHECKLIST ===
- [ ] Written sponsorship agreement in place before any content is sent
- [ ] "This event is supported by [Sponsor]" appears in all company emails
- [ ] "This event is supported by [Sponsor]" appears in all company LinkedIn posts
- [ ] NEL posts do NOT name the sponsor
- [ ] No specific medicinal product names in any content
- [ ] If any content references a specific product, add prescribing information link (ABPI Clause 12)
- [ ] Prior permission obtained for promotional emails to HCPs (ABPI Clause 9.9)
```

---

## Email Compliance Checklist (All Events)

Append this to the output regardless of sponsor status:

```
=== EMAIL COMPLIANCE CHECKLIST ===
- [ ] Every email includes Mailchimp unsubscribe link (*|UNSUB|*)
- [ ] Sender is named individual (not generic inbox)
- [ ] Subject lines avoid spam triggers (no "Urgent", "Free", "Guarantee", "Act Now", "Last Chance")
- [ ] Subject lines are 40-60 characters
- [ ] Plain text version prepared for each email
- [ ] Mobile preview tested at 600px width
- [ ] Dark mode tested
- [ ] List segmented by therapeutic area and geography before sending
- [ ] UTM parameters applied to all links (lowercase, consistent naming)
- [ ] Send timing: 11am-2pm or 5-8pm weekdays
- [ ] Frequency cap: max 1-2 promotional emails per month to general list
```

---

## Brand Specifications

### Colours
| Name | Hex | Usage |
|------|-----|-------|
| Primary Dark | #170132 | Backgrounds (never use #000000) |
| Primary Navy | #02084B | Cards, secondary backgrounds |
| Primary Magenta | #FD02F7 | CTAs, highlights, dividers |
| Primary Purple | #9A2CFB | Gradient elements, accents |
| White | #FFFFFF | Text on dark, body backgrounds |
| Gradient | #9A2CFB → #FD02F7 | Buttons, decorative bars |

### Typography
| Element | Font | Fallback |
|---------|------|----------|
| Headings | Code Next Bold | Montserrat Bold, Arial Bold |
| Body | Inter Light | Open Sans Light, Arial |
| Email (all) | Arial | — (email-safe requirement) |

### Carousel Dimensions
- All slides: 1080 × 1080px (LinkedIn carousel standard)
- Top/bottom gradient bars on every slide
- "MORPh Training" watermark top-left corner
- CPD Accredited badge on first and last slides

### Voice (summary — see brand-voice-guidelines.md for full rules)
- Clinical authority — lead with substance, not polish
- Respectful brevity — 100-200 words for promotion, under 100 for logistics
- Named human voice — always a real person, never "The MORPh Team"
- Educational framing — pain-solution structure
- No banned words: exciting, amazing, unlock, leverage, game-changing, cutting-edge, don't miss out
- No exclamation marks in emails. No emojis in emails.

---

## Error Handling and Edge Cases

### Zero NELs

If the user types DONE immediately at Q23 with no NELs listed:
- **Skip** NEL1, NEL2, NEL3 social post generation in Phase 5
- **Skip** V5 and V6 carousel generation in Phase 6
- **Skip** Phase 7 (NEL content packs) entirely
- Update totals: social posts = 4 (company only), carousel PDFs = 4 (V1-V4 only)
- Phase 10 summary should reflect the reduced counts

### Webinar events — social and visual adjustments

Webinar events have no physical venue or city. Adjust the following:
- **C4 (Event Day post):** Replace "joined us in [City]" with "joined us online" or "joined the webinar". No venue/directions references.
- **V4 carousel (Event Day):** Slide 3 "See You There" should show "Join Online" with the platform name and start time instead of venue/city/directions. Slide 1 should show the platform and time, not a venue.
- **NEL3 (Event Day post):** Replace "live in [City]" with "live on [Platform]".
- **All social copy:** Use "online" or "[Platform] webinar" where F2F copy would reference a city or venue.

### Fewer or more than 3 learning outcomes

- **Fewer than 3:** If only 2 outcomes provided, remove the `{{LEARNING_OUTCOME_3}}` row from A2 and B2 templates (find the table row or list item containing the token and delete it). If only 1, also remove `{{LEARNING_OUTCOME_2}}`.
- **More than 3:** Use the first 3 for email tokens `{{LEARNING_OUTCOME_1-3}}`. All outcomes (including 4+) are used in carousel slides (V1 slide 3 renders the full `learningOutcomes` array) and social copy.

### B6 CTA_LINK handling

B6 (Post-Event Thank You) has two CTAs: `{{CTA_LINK}}` for the CPD certificate download and `{{FEEDBACK_LINK}}` for the feedback survey. During Phase 4, do NOT replace `{{CTA_LINK}}` in B6 with the registration link. Leave it as `{{CTA_LINK}}` — it gets replaced in Phase 9 with the CPD certificate download URL, which Will provides after the event.

### Fewer than 3 sessions

B2 template has `{{SESSION_1_*}}` through `{{SESSION_3_*}}` tokens. If fewer sessions:
- **2 sessions:** Find and remove the entire Session 3 row in the B2 HTML (the `<tr>` containing `{{SESSION_3_TIME}}`, `{{SESSION_3_TITLE}}`, `{{SESSION_3_SPEAKER}}`).
- **1 session:** Also remove the Session 2 row.
- **More than 3 sessions:** Only sessions 1-3 appear in B2. Additional sessions appear in the V2 carousel (which renders all sessions dynamically) and social copy.

### General error handling

- **Brand voice skill unavailable:** Skip enforcement, flag warning: "⚠ Brand voice enforcement skipped — review copy manually against config/brand-voice-guidelines.md"
- **Humanizer skill unavailable:** Skip humanisation, flag warning: "⚠ Humanizer skipped — review copy for AI writing patterns"
- **Next.js dev server won't start:** Check port 3847 is free. Try `lsof -i :3847` and kill any process using it.
- **Puppeteer screenshot fails:** Ensure the dev server is running and accessible at http://localhost:3847. Check that `/tmp/morph-event-data.json` exists and is valid JSON.
- **Zapier webhooks fail:** Save all assets locally and inform the user. Assets can always be manually uploaded.
- **Missing event data:** Never guess clinical details. If a required field is missing, ask the user before proceeding.
- **No testimonial or rating:** Remove conditional A2 blocks (handled in Phase 4d).
- **Event less than 8 weeks away:** Calculate which touchpoints are past due and present a compressed timeline.
