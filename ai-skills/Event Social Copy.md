---
name: event-social-copy
description: |
  Generate all event social media copy from an event brief — 4 company LinkedIn posts and 3 NEL ready-to-post content packs. All copy runs through brand-voice enforcement and humaniser. Use when Dean or Will says: "generate event social posts", "create LinkedIn content for [event]", "event social pack", "write the social posts for [event]", "NEL content for [event]", or provides an event brief and asks for social content.
version: 1.0.0
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Skill
  - AskUserQuestion
---

# Event Social Copy Generator

Generate all 7 social media touchpoints for a MORPh Training event — 4 company LinkedIn posts and 3 NEL ready-to-post content packs.

## Before You Start

1. Read the brand voice guidelines at `.claude/brand-voice-guidelines.md`
2. Read the brand reference at `~/.claude/skills/event-marketing-generator/references/morph-brand.md`
3. If the `event-email-copy` skill has already been run for this event, read its output to maintain consistency

## Step 1: Collect the Event Brief

Same event brief as event-email-copy. Ask for missing fields.

### Required Fields

| Field | Example |
|-------|---------|
| Event name | Diabetes Masterclass: Type 2 Management in Primary Care |
| Speaker name and credentials | Dr Sarah Khan, Consultant Diabetologist, NHS Greater Manchester |
| Therapeutic area | Diabetes / Endocrinology |
| Key learning outcomes (2-3) | 1. Latest NICE guidelines for T2D 2. When to escalate from metformin 3. Practical prescribing frameworks |
| CPD credits | 2 CPD credits (CPPE-accredited) |
| Event date and time | Thursday 15 May 2026, 7:00pm - 9:00pm |
| Format | Face-to-face OR Webinar |
| Venue (if F2F) | Hilton Manchester Deansgate, 303 Deansgate, M3 4LQ |
| Target geography | Greater Manchester and surrounding areas |
| Delegate capacity | 40 places |
| Sponsor (if applicable) | Novo Nordisk OR "No sponsor" |
| Registration link | [URL] — but DO NOT put this in the post body |
| NEL name(s) and region(s) | James Okoro, Manchester North |

---

## Step 2: Generate All 7 Posts

Generate each post in full, then run the quality pipeline.

### Quality Pipeline

For each post:
1. **Draft** the copy following the rules below
2. **Apply brand voice** — invoke `brand-voice:enforce-voice`
3. **Humanise** — invoke `humanizer` to strip AI patterns

Present the final humanised version.

---

## LinkedIn Rules (from Group Marketing Strategy v3)

- **No external links in the post body.** External links trigger a 40-60% reach penalty. Use comment-based CTAs: "Comment REGISTER below and we'll send you the link" or "Drop me a message for the registration link."
- **Format priority:** Carousel (6.60% engagement) > Native document (5.85-6.10%) > Native video under 90s (5.60%) > Single image (4.85%)
- **Never use marketing hype.** Educational, authoritative tone. No "amazing opportunity", "don't miss out", "we're excited to announce."
- **3-5 relevant hashtags** per post.
- **Tag speaker** if appropriate and agreed.
- **Content must work as standalone clinical value** — not just event promotion.
- **Golden Hour:** Seed authentic engagement in first 60 minutes of posting.
- **No specific medicine names** on public social channels (ABPI).

---

## COMPANY LINKEDIN (4 posts)

### C1: Event Announcement (Week 8)

**Purpose:** First awareness. Clinical question framing. Stop the scroll with clinical substance.

Generate:
- **Post copy** (150-250 words):
  - Open with a clinical question or provocative stat from the therapeutic area. This is the hook — it must make a pharmacist stop scrolling.
  - Bridge to the event as the answer (2-3 sentences)
  - Speaker credentials (1 sentence)
  - CPD credits, date, location, format
  - CTA: "Comment REGISTER below and we'll send you the link" or "Comment INTERESTED for details"
- **Suggested format:** Carousel (cover slide + 2-3 content slides) or single image
- **3-5 hashtags** relevant to the therapeutic area + #CPD #Pharmacist #ClinicalEducation
- **Visual brief note:** Describe what the accompanying carousel/image should contain (event name, speaker, date, CPD, key question)

### C2: Agenda / Speaker Deep-Dive (Week 5)

**Purpose:** Depth and credibility. Position the clinical content. Give people a reason to save the post.

Generate:
- **Post copy** (150-250 words):
  - Deep-dive into the therapeutic area or what the speaker will cover
  - Specific learning outcomes (as a numbered or bulleted list within the post)
  - Why this matters now — clinical context, guideline changes, policy shifts
  - Tag speaker if appropriate
  - CTA: "Comment REGISTER for details"
- **Suggested format:** Carousel (3-5 slides) — one learning outcome per slide
- **3-5 hashtags**
- **Visual brief note:** Carousel slide content — cover slide with event title, then one slide per learning outcome, final slide with CTA + date + CPD

### C3: Countdown + Final Push (Week 2)

**Purpose:** Urgency through scarcity and value, not hype.

Generate:
- **Post copy** (100-150 words):
  - "One week to go" or "7 days" opening
  - Speaker quote if available, or one key agenda item that hasn't been featured yet
  - Remaining capacity if it's strong (e.g., "12 places left")
  - CPD credits
  - CTA: Comment-based
- **Suggested format:** Single image (countdown graphic) or short text post
- **3-5 hashtags**
- **Visual brief note:** Bold countdown graphic — "1 Week to Go", event name, date, places remaining, CPD credits

### C4: Event Day (Week 1)

**Purpose:** Live content. Social proof in real time. Energy.

Generate TWO versions:

**F2F version:**
- "We're here at [Venue]" opening
- Key talking points for a photo caption (what to highlight when posting a real photo)
- Tag speaker
- 3-5 hashtags
- **Note to team:** Take and post a real photo. The generated graphic is a complement, not a replacement.

**Webinar version:**
- "Happening now" or "We're live" opening
- Key topic teaser (1-2 sentences)
- Do NOT include the access link in the post body (reach penalty) — direct people to the bio link or comments
- 3-5 hashtags

**Post-event version (same day or next morning):**
- Key stat if available (attendance, feedback)
- "Thank you to [Speaker]"
- Delegate quote prompt: "[Insert delegate feedback quote here]"
- "Next event" teaser if known
- 3-5 hashtags

---

## NEL LINKEDIN — Ready-to-Post Content (3 posts per NEL)

### NEL Voice Rules

- **First person, conversational, regional.** These must sound like a real pharmacist talking to their network, not a company announcement.
- **Not copy-paste corporate content.** The NEL's regional angle and personal voice must come through.
- **Never name specific medicines** (ABPI).
- **Comment-based CTAs** — "Drop me a message" or "Comment below if you want the link."
- Personalise with the NEL's name and region from the event brief.

For each NEL listed in the event brief, generate a personalised set of 3 posts.

### NEL1: Regional Announcement (Week 8)

Generate:
- **Post copy** (100-200 words, first person):
  - "Why I'm bringing this to pharmacists in [region]" angle
  - Personal connection to the topic — why it matters locally
  - Speaker credentials, CPD credits, date, location
  - CTA: "Comment below if you'd like the registration link" or "Drop me a message"
- **3-5 hashtags** (include regional ones like #ManchesterPharmacy if appropriate)
- **Visual brief note:** Personalised event infographic — "[NEL Name] invites you" or "For pharmacists in [region]", event details, CPD credits, MORPh branding (warm, approachable — less corporate than company page graphics)

### NEL2: Personal Invitation (Week 3)

Generate:
- **Post copy** (80-120 words, first person):
  - "I'd love to see you there" tone
  - One or two specific things they'll learn
  - Remaining capacity and CPD credits
  - Feels like messaging a colleague, not publishing a press release
  - CTA: "Message me if you want a place" or "Comment REGISTER"
- **3-5 hashtags**
- **Visual brief note:** Personal invitation graphic — "[X] places left", event name, date, CPD. Warm, personal feel.

### NEL3: Event Day Post (Week 1)

Generate TWO versions:

**Live post (day-of):**
- 50-80 words, first person
- "We're here", "Great turnout", capture the energy
- Prompt: "Take a photo at the event and post it alongside this copy"
- 3-5 hashtags

**Reflection post (next day):**
- 100-150 words, first person
- "What I took away from last night" angle
- Personal, genuine, brief
- 1-2 specific things that resonated
- 3-5 hashtags

---

## ABPI Compliance

If the event has a pharmaceutical sponsor:
- Add "This event is supported by [Sponsor Name]" to every company LinkedIn post
- NEL posts: do NOT mention the sponsor by name (their personal profiles should not appear as sponsor channels). Instead, use: "This is an independently accredited CPD programme."
- No specific medicine names in any social post

---

## Output Format

Present all 7 posts clearly labelled:

```
=== COMPANY LINKEDIN ===

--- C1: Event Announcement (Week 8) ---
Format: [Carousel / Single Image]
[Post copy]
Hashtags: [hashtags]
Visual brief: [description for design team]

--- C2: Agenda / Speaker Deep-Dive (Week 5) ---
...

--- C3: Countdown + Final Push (Week 2) ---
...

--- C4: Event Day (Week 1) ---
[F2F version]
[Webinar version]
[Post-event version]

=== NEL LINKEDIN — [NEL Name], [Region] ===

--- NEL1: Regional Announcement (Week 8) ---
[Post copy]
Visual brief: [description]

--- NEL2: Personal Invitation (Week 3) ---
...

--- NEL3: Event Day Post (Week 1) ---
[Live version]
[Reflection version]
```

After presenting, ask if the user wants the output saved as .docx.

---

## Reference Documents

- Brand Voice Guidelines: `.claude/brand-voice-guidelines.md`
- Brand Reference: `~/.claude/skills/event-marketing-generator/references/morph-brand.md`
- Group Marketing Strategy v3: `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Group_Marketing_Strategy_Branded-4.docx`
- 8-Week Event Marketing Cadence v2: `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Events Marketing/8-Week Event Marketing Cadence v2.docx`
