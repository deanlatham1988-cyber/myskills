---
name: event-email-copy
description: |
  Generate all event email copy from an event brief — 3 registration drive emails (Stream A) and 5 delegate engagement emails/SMS (Stream B). Outputs a .docx content pack with subject lines, preview text, body copy, and CTAs for every touchpoint. All copy runs through brand-voice enforcement and humaniser. Use when Dean or Will says: "generate event emails", "create email copy for [event]", "event email pack", "write the emails for [event]", or provides an event brief and asks for email content.
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

# Event Email Copy Generator

Generate all 8 email touchpoints for a MORPh Training event from a single event brief.

## Before You Start

1. Read the brand voice guidelines at `.claude/brand-voice-guidelines.md` (or the working folder equivalent)
2. Read the brand reference at `~/.claude/skills/event-marketing-generator/references/morph-brand.md`
3. Read the Email Marketing Playbook rules embedded below — these are the source of truth for email copy

## Step 1: Collect the Event Brief

Ask the user for any missing fields. Do not guess clinical details.

### Required Fields

| Field | Example |
|-------|---------|
| Event name | Diabetes Masterclass: Type 2 Management in Primary Care |
| Speaker name and credentials | Dr Sarah Khan, Consultant Diabetologist, NHS Greater Manchester |
| Therapeutic area | Diabetes / Endocrinology |
| Key learning outcomes (2-3) | 1. Latest NICE guidelines for T2D management 2. When to escalate from metformin 3. Practical prescribing frameworks |
| CPD credits (type and number) | 2 CPD credits (CPPE-accredited) |
| Event date and time | Thursday 15 May 2026, 7:00pm - 9:00pm |
| Format | Face-to-face OR Webinar |
| Venue (if F2F) | Hilton Manchester Deansgate, 303 Deansgate, M3 4LQ. Free parking. |
| Target geography | Greater Manchester and surrounding areas |
| Delegate capacity | 40 places |
| Sponsor (if applicable) | Novo Nordisk OR "No sponsor" |
| Named email sender | Ryan Smith or Dean |
| Registration link | [URL] |

### Optional Fields

| Field | Example |
|-------|---------|
| Pre-reading or resources | NICE NG28 summary document |
| Dietary confirmation needed | Yes/No |
| Webinar platform link | Zoom/Teams link |
| Previous event stats | "87% rated last masterclass excellent" |

---

## Step 2: Generate All 8 Emails

Generate each email in full, then run the quality pipeline.

### Quality Pipeline

For each email:
1. **Draft** the copy following the rules below
2. **Apply brand voice** — invoke `brand-voice:enforce-voice` with the draft and instruct it to apply MORPh brand guidelines
3. **Humanise** — invoke `humanizer` to strip AI writing patterns

Present the final humanised version to the user.

---

## STREAM A: Registration Drive Emails (3 emails)

### Rules (from Email Marketing Playbook v1)

- **Subject lines:** 40-60 characters. Frame a clinical question or include a specific number.
- **NEVER use:** "Urgent", "Free", "Guarantee", "Act Now", "Last Chance" — these destroy credibility with clinical audiences and trigger spam filters.
- **Preview text:** Intentionally written. Never "View in browser." Secondary hook with CPD credits or speaker name.
- **Body copy:** 100-200 words. Pain-Solution structure — identify a specific clinical challenge, position the event as the resolution.
- **Single CTA only:** Descriptive action language. "Register for Masterclass" not "Click here".
- **Named sign-off:** Ryan Smith or Dean. Never a generic inbox.
- **Segmentation note:** Include a note that the email must be segmented by therapeutic area and geography before sending.
- **Frequency cap:** Maximum 1-2 promotional emails per month to the general list.
- **Send timing:** 11am-2pm (midday lull) or 5-8pm (post-work). Monday 10am for pharma-facing contacts.

### A1: Event Announcement (Week 8)

**Purpose:** First awareness. Clinical question framing. Establish the event exists and why it matters.

Generate:
- **Subject line** — clinical question format preferred (e.g., "Are you managing [condition] to the latest [guideline]?")
- **Preview text** — CPD hook or speaker credentials (e.g., "Earn 2 CPD credits — [Therapeutic Area] Masterclass, [Town]")
- **Body copy** (100-200 words):
  - Open with a clinical question or challenge relevant to the therapeutic area
  - Position the event as the answer (1-2 sentences)
  - Speaker credentials (1-2 sentences)
  - CPD credits prominently stated
  - Date, time, location
  - Single CTA button text: "Register for [Event Type]"
- **Sign-off:** Named individual
- **Segmentation note:** "Send to: [therapeutic area] contacts in [geography]"

### A2: Social Proof + CPD Hook (Week 4)

**Purpose:** Different angle from announcement. Evidence-based persuasion. Reinforce professional value.

Generate:
- **Subject line** — CPD credit or specific number format (e.g., "Earn 2 CPD credits — [X] pharmacists already registered")
- **Preview text** — learning outcomes or delegate numbers
- **Body copy** (100-200 words):
  - Lead with social proof (delegate numbers, testimonial from previous event, or past event stats if provided)
  - Specific learning outcomes as bullet points
  - CPD credits and how they apply to revalidation/appraisal
  - Reinforce professional commitment angle
  - Single CTA: "Register for [Event Type]"
- **Sign-off:** Named individual

### A3: Final Places (Week 1)

**Purpose:** Final push. Short, direct, no fluff. Urgency through scarcity, not hype.

Generate:
- **Subject line** — clinical question OR "Final places — [Event Name], [Date]" (NOT "Last Chance" or "Act Now")
- **Preview text** — remaining capacity + CPD
- **Body copy** (UNDER 100 words):
  - Remaining capacity (e.g., "12 places remaining")
  - One key learning outcome
  - CPD credits
  - Single CTA: "Register Now"
- **Sign-off:** Named individual

---

## STREAM B: Registered Delegate Engagement (5 touchpoints)

### Rules

- These go to **confirmed delegates only**. Never send registration drive content to confirmed delegates.
- CPD accreditation is the single most effective attendance driver — lead with it.
- Tone shifts from value-building (early) to practical preparation (late).
- 48-hour confirmation request is the single most impactful touchpoint for no-show reduction.

### B1: Booking Confirmation (On registration)

**Purpose:** Transactional. Confirm their place. Get it in their calendar immediately.

Generate:
- **Subject line:** "[Event Name] — Your place is confirmed"
- **Body copy:**
  - "Thank you for registering" confirmation
  - Instruction to add to calendar (one-click .ics invite mention)
  - Event details: date, time, location/link
  - Speaker name and credentials (brief — 1 sentence)
  - CPD credits they will earn
  - What to expect (1-2 sentences)
  - "If you have any questions, reply to this email" contact line
- **Sign-off:** Named individual

### B2: Value + Content Preview (10 days before)

**Purpose:** Build anticipation. Keep the event front of mind during the drop-off risk window.

Generate:
- **Subject line** — clinical question or CPD format
- **Body copy** (100-150 words):
  - Agenda deep-dive or key session highlights
  - What delegates will learn (specific outcomes as bullets)
  - Pre-reading or preparation if applicable (from event brief)
  - Speaker highlight (1 sentence)
  - "We look forward to seeing you on [date]"
- **Sign-off:** Named individual

### B3: Logistics (5 days before)

**Purpose:** Practical preparation. Remove friction. Tone shifts to direct and operational.

Generate:
- **Subject line:** "[Event Name] — Everything you need for [date]"
- **Body copy** (short, practical, scannable — use bullet points):
  - Venue address with brief directions (F2F) OR platform access details and link (webinar)
  - Parking information (F2F)
  - Dietary confirmation reminder if applicable
  - Start time and expected finish time
  - "Any questions? Reply to this email or call [number]"
- **Sign-off:** Named individual

### B4: Confirmation Request (48 hours before)

**Purpose:** Confirm attendance. Easy opt-out reduces day-of no-shows. Highest-impact touchpoint.

Generate TWO versions:

**Email version:**
- **Subject line:** "Can we confirm your place for [day, date]?"
- **Body copy** (under 80 words):
  - "Reply C to confirm your attendance"
  - Final logistical checklist: time, location (1-2 lines)
  - Easy opt-out: "If you can no longer attend, just let us know — we can offer your place to a colleague on the waiting list"
- **Sign-off:** Named individual

**SMS version:**
- Under 160 characters
- Format: "[First Name], your [Event Name] is in 48 hours. Reply C to confirm or let us know if plans have changed. [Sender Name]"

### B5: Day-of Reminder (Morning / 2 hours before)

Generate TWO versions based on event format:

**F2F — SMS:**
- Under 160 characters
- Include: directions/parking reminder, check-in time, venue name
- Format: "See you at [time]. [Venue name], [postcode]. Free parking available. Check-in from [time]. [Sender Name]"

**Webinar — Email:**
- **Subject line:** "We're live in 2 hours — your access link"
- **Body copy** (under 50 words):
  - Direct access link (prominent)
  - Start time
  - "Click to join when ready"
- **Sign-off:** Named individual

---

## ABPI Compliance Module

**If the event brief includes a pharmaceutical sponsor, add the following to EVERY email:**

1. **Sponsorship disclosure** at the top of the email body (not in the footer):
   - "This event is supported by [Sponsor Name]"
2. **Compliance note** appended to the content pack:
   - "Confirm written sponsorship agreement is in place before sending"
   - "If any email references a specific medicinal product, add prescribing information link (ABPI Clause 12)"
   - "Prior permission required for promotional emails to HCPs (ABPI Clause 9.9)"

---

## Output Format

Present all 8 emails in sequence, clearly labelled:

```
=== STREAM A: REGISTRATION DRIVE ===

--- A1: Event Announcement (Week 8) ---
Subject: [subject line]
Preview: [preview text]
Segmentation: [therapeutic area] contacts in [geography]
Send window: [recommended time]

[body copy]

[Named sign-off]

--- A2: Social Proof + CPD Hook (Week 4) ---
...

--- A3: Final Places (Week 1) ---
...

=== STREAM B: DELEGATE ENGAGEMENT ===

--- B1: Booking Confirmation (On registration) ---
...

--- B2: Value + Content Preview (10 days before) ---
...

--- B3: Logistics (5 days before) ---
...

--- B4: Confirmation Request (48 hours before) ---
[Email version]
[SMS version]

--- B5: Day-of Reminder (Morning / 2hrs) ---
[F2F SMS version]
[Webinar email version]

=== COMPLIANCE CHECKLIST ===
- [ ] Every email includes unsubscribe link
- [ ] Sender is named individual
- [ ] Subject lines avoid spam triggers
- [ ] Plain text version prepared
- [ ] Mobile preview tested at 600px
- [ ] Dark mode tested
- [ ] List segmented by therapeutic area and geography
- [ ] UTM parameters applied (lowercase)
- [ ] ABPI checklist completed (if sponsor)
```

After presenting all emails, ask the user if they want the output saved as a .docx file using the `anthropic-skills:docx` skill.

---

## Reference Documents

- Brand Voice Guidelines: `.claude/brand-voice-guidelines.md`
- Brand Reference: `~/.claude/skills/event-marketing-generator/references/morph-brand.md`
- Email Marketing Playbook v1: `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Email_Marketing_Playbook_Branded-4.docx`
- 8-Week Event Marketing Cadence v2: `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Events Marketing/8-Week Event Marketing Cadence v2.docx`
