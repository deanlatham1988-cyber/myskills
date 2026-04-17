---
name: event-marketing-generator
description: |
  Coordinator skill for the MORPh Event Marketing Automation System. Guides Dean/Will through the full event marketing workflow — collecting the event brief, then pointing to the three specialist skills in sequence. Use when someone says "event marketing for [event]", "start the event marketing process", "new event campaign", or wants an overview of the event marketing system.
version: 3.0.0
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Skill
  - AskUserQuestion
---

# Event Marketing Coordinator

This is the starting point for generating all marketing content for a MORPh Training event. It collects the event brief and then guides you through three specialist skills in sequence.

## The System

```
You are here
    │
    ├─ Step 1: /event-email-copy
    │  → 3 registration emails + 5 delegate emails/SMS
    │  → Output: email copy pack
    │
    ├─ Step 2: /event-social-copy
    │  → 4 company LinkedIn posts + 3 NEL ready-to-post packs
    │  → Output: social copy pack
    │
    └─ Step 3: /event-visual-briefs
       → 7 design specs for Ariyan (Adobe Illustrator/Photoshop)
       → Optional: AI draft visuals via banana-claude
       → Output: visual brief document
```

**Quality pipeline on all copy:** draft → brand-voice:enforce-voice → humanizer

## Step 1: Collect the Event Brief

Gather these fields from the user. Store them so they can be passed to each skill.

### Required

| Field | Description |
|-------|-------------|
| Event name | Full event title |
| Speaker | Name, credentials, affiliation |
| Therapeutic area | Clinical topic |
| Learning outcomes | 2-3 specific bullet points |
| CPD credits | Type and number |
| Date and time | Day, date, start-finish |
| Format | Face-to-face or Webinar |
| Venue (if F2F) | Name, address, parking |
| Target geography | Region the event covers |
| Delegate capacity | Total places available |
| Sponsor | Company name or "No sponsor" |
| Named sender | Ryan Smith or Dean |
| Registration link | URL |
| NEL name(s) + region(s) | For NEL content personalisation |

### Optional

| Field | Description |
|-------|-------------|
| Pre-reading | Resources delegates should review |
| Dietary confirmation | Yes/No |
| Webinar link | Platform access URL |
| Previous event stats | For social proof in copy |

## Step 2: Calculate the Execution Timeline

From the event date, calculate backwards:

| Touchpoint | Date |
|------------|------|
| Week 8 — Announcement | [event date minus 56 days] |
| Week 5 — Agenda deep-dive | [event date minus 35 days] |
| Week 4 — Social proof email | [event date minus 28 days] |
| Week 3 — NEL invitation | [event date minus 21 days] |
| Week 2 — Countdown | [event date minus 14 days] |
| Week 1 — Final places + event day | [event date minus 7 days to event day] |
| 10 days before — Value preview | [event date minus 10 days] |
| 5 days before — Logistics | [event date minus 5 days] |
| 48 hours before — Confirmation | [event date minus 2 days] |
| Day-of — Reminder | [event date] |

Present this timeline to the user.

## Step 3: Guide Through the Skills

Tell the user:

> "Your event brief is ready. Run these three skills in order:
>
> 1. **`/event-email-copy`** — generates all 8 emails (Stream A + B)
> 2. **`/event-social-copy`** — generates all 7 social posts (Company + NEL)
> 3. **`/event-visual-briefs`** — generates design specs for Ariyan
>
> Each skill will ask you to paste the event brief. I'll format it for you now so you can copy-paste it into each one."

Then output the event brief as a formatted block the user can paste.

## Reference Documents

- Cadence: `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Events Marketing/8-Week Event Marketing Cadence v2.docx`
- Email Playbook: `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Email_Marketing_Playbook_Branded-4.docx`
- Marketing Strategy: `/Users/deanlatham/Desktop/Morph/Things built /Marketing/Group_Marketing_Strategy_Branded-4.docx`
- Brand Voice: `.claude/brand-voice-guidelines.md`
- Brand Reference: `~/.claude/skills/event-marketing-generator/references/morph-brand.md`
