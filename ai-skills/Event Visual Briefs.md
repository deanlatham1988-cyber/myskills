---
name: event-visual-briefs
description: |
  Generate design briefs for all event marketing visual assets — carousel slides, infographics, countdown graphics, and event day visuals. Briefs are detailed enough for Ariyan (Design Apprentice) to execute in Adobe Illustrator/Photoshop. Optionally generates AI draft visuals via banana-claude as reference. Use when Dean or Will says: "create visual briefs for [event]", "design specs for event graphics", "event visuals brief", "what graphics do we need for [event]", or after running event-social-copy and needing the accompanying visuals.
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

# Event Visual Briefs Generator

Generate detailed design specifications for all visual assets needed for a MORPh Training event marketing campaign. These briefs are for Ariyan (Design Apprentice) to execute in Adobe Illustrator/Photoshop.

## Before You Start

1. Read the brand reference at `~/.claude/skills/event-marketing-generator/references/morph-brand.md` — this has all hex values, fonts, dimensions, and style rules
2. If `event-social-copy` has already been run, read its output — the visual briefs should match the social copy exactly
3. Check if banana-claude is set up (look for `~/.banana/presets/`) — if available, offer to generate AI draft visuals as reference for Ariyan

## Step 1: Collect Input

This skill needs either:
- **The event brief** (same fields as event-email-copy and event-social-copy), OR
- **The social copy output** from event-social-copy (preferred — the visual briefs should match the copy exactly)

If neither is provided, ask for the event brief.

---

## Step 2: Generate Visual Briefs

Generate a detailed design brief for each visual asset needed across the campaign.

### MORPh Brand Specifications (for every visual)

| Element | Specification |
|---------|--------------|
| **Primary Dark** | #170132 — backgrounds, deep contrast |
| **Primary Navy** | #02084B — headings, text on light |
| **Primary Magenta** | #FD02F7 — accents, CTAs, highlights |
| **Primary Purple** | #9A2CFB — secondary accent, gradients |
| **White** | #FFFFFF — text on dark, clean space |
| **Gradient** | #9A2CFB → #FD02F7 (purple to magenta) — accent bars, CTA buttons |
| **Heading font** | Code Next Bold (fallback: Montserrat Bold) |
| **Body font** | Inter Light (fallback: Open Sans Light) |
| **Logo** | Use transparent PNG. Dark bg = light logo. Light bg = dark logo. |
| **Style** | Clean, professional, clinical education. No stock photo faces. Abstract geometric or clean data motifs. |
| **ABPI** | No pharmaceutical product imagery. No specific medicine names. Clinical education framing only. |

---

## THE 7 VISUAL ASSETS

### V1: Event Announcement — Company LinkedIn (Week 8)

**Type:** Carousel (cover + 2-3 slides) OR single image
**Dimensions:** 1080 x 1080px per slide (carousel) or 1200 x 627px (landscape single)

**Brief for Ariyan:**
- **Cover slide:**
  - Background: #170132 (dark) or #02084B (navy)
  - Event name in Code Next Bold, white, prominent
  - Speaker name and credentials below in Inter Light, white
  - Date and location in Inter Light
  - "Earn [X] CPD Credits" badge — magenta (#FD02F7) accent
  - MORPh logo (light variant) in corner
  - Gradient accent bar (#9A2CFB → #FD02F7) at bottom or side

- **Content slides (if carousel):**
  - One key clinical question or learning outcome per slide
  - Numbered (1, 2, 3) for progression
  - Same dark background
  - Large text, minimal — each slide must be readable in 3 seconds
  - Magenta accent for numbers or highlight text

- **Final slide:**
  - "Comment REGISTER for details" CTA
  - Date, location, CPD credits repeated
  - MORPh logo

### V2: Agenda / Speaker Deep-Dive — Company LinkedIn (Week 5)

**Type:** Carousel (3-5 slides)
**Dimensions:** 1080 x 1080px per slide

**Brief for Ariyan:**
- **Cover slide:**
  - "What You'll Learn" or the therapeutic area as headline
  - Speaker name and photo placeholder (if photo available)
  - Event name below
  - Dark background, white text, magenta accents

- **Content slides (one per learning outcome):**
  - Learning outcome number (large, magenta)
  - Outcome text (white, Inter Light, 2-3 lines max)
  - Optional: abstract clinical/science icon or motif per slide
  - Consistent layout across all content slides

- **Final slide:**
  - "Comment REGISTER" CTA
  - Date + location + CPD credits
  - MORPh logo

### V3: Countdown Graphic — Company LinkedIn (Week 2)

**Type:** Single image
**Dimensions:** 1200 x 1200px (square)

**Brief for Ariyan:**
- **"1 Week to Go"** or **"7 Days"** — large, bold, Code Next Bold
- Background: dark (#170132) with gradient accent
- Event name below the countdown
- Date and time
- Remaining places: "[X] places left" in magenta
- CPD credits
- MORPh logo
- Energy and urgency through design (bold type, gradient), NOT through hype language

### V4: Event Day Graphic — Company LinkedIn (Week 1)

**Type:** Single image or story format
**Dimensions:** 1200 x 627px (landscape) for main post

**Brief for Ariyan:**
- **F2F version:**
  - "Happening Today" or "We're Live" — large, bold
  - Event name, venue, time
  - Dark background with magenta accent
  - Space left for a real photo to be overlaid or posted alongside
  - MORPh logo

- **Webinar version:**
  - "We're Live" — large, bold
  - Event name, time
  - "Join now" prompt (but no link in the graphic — that goes in comments)
  - Dark background, clean layout

### V5: NEL Regional Announcement — NEL LinkedIn (Week 8)

**Type:** Single image (personalised per NEL)
**Dimensions:** 1080 x 1080px (square)

**Brief for Ariyan:**
- **Personalised for each NEL:**
  - "[NEL Name] invites you" or "For pharmacists in [Region]" — headline
  - Event name, date, location
  - Speaker name
  - CPD credits badge (magenta)
  - MORPh logo (smaller — this is the NEL's post, not the company's)
- **Style:** Warmer, more approachable than company graphics. Same brand colours but less corporate feel. Should look like something a person would share, not an ad.

### V6: NEL Personal Invitation — NEL LinkedIn (Week 3)

**Type:** Single image
**Dimensions:** 1080 x 1080px (square)

**Brief for Ariyan:**
- **"[X] Places Left"** — large, prominent
- Event name and date below
- CPD credits
- Quote-style layout option: "I'd love to see you at..." with NEL name
- Warm, personal feel — same brand colours but lighter touch
- MORPh logo (small)

### V7: NEL Event Day Shareable — NEL LinkedIn (Week 1)

**Type:** Single image (to accompany NEL's own photo)
**Dimensions:** 1200 x 627px (landscape — works as a share card)

**Brief for Ariyan:**
- "Live Now" or "Happening Tonight"
- Event name
- MORPh branding subtle (this accompanies a real photo, not replaces it)
- Clean, minimal — the real photo is the star
- **Note:** The NEL should also take and post their own real photo. This graphic is a branded complement.

---

## Optional: AI Draft Visuals

If banana-claude is set up, offer to generate AI draft visuals for each brief. These serve as **reference/inspiration for Ariyan**, not final assets.

When invoking banana-claude:
- Use the MORPh brand colour palette
- Request clean, professional, clinical education aesthetic
- Specify exact dimensions
- Include all text that should appear on the graphic
- Save outputs to the event's content pack folder

Ask the user: "Would you like me to generate AI draft visuals as reference for Ariyan, or are the written briefs sufficient?"

---

## Output Format

Present all 7 briefs clearly:

```
=== VISUAL BRIEFS — [Event Name] ===

--- V1: Event Announcement Carousel (Week 8) ---
Type: Carousel (3 slides)
Dimensions: 1080 x 1080px per slide
[Detailed brief]

--- V2: Agenda Deep-Dive Carousel (Week 5) ---
...

--- V3: Countdown Graphic (Week 2) ---
...

--- V4: Event Day Graphic (Week 1) ---
[F2F version]
[Webinar version]

--- V5: NEL Regional Announcement (Week 8) ---
NEL: [Name], [Region]
[Personalised brief]

--- V6: NEL Personal Invitation (Week 3) ---
...

--- V7: NEL Event Day Shareable (Week 1) ---
...

=== BRAND REFERENCE ===
Colours: #170132, #02084B, #FD02F7, #9A2CFB, #FFFFFF
Gradient: #9A2CFB → #FD02F7
Fonts: Code Next Bold (headings), Inter Light (body)
Logo: /Users/deanlatham/Desktop/Morph/MORPh Brand Pack/Logo/
```

After presenting, ask if the user wants:
1. The briefs saved as .docx for Ariyan
2. AI draft visuals generated via banana-claude

---

## Reference Documents

- Brand Reference: `~/.claude/skills/event-marketing-generator/references/morph-brand.md`
- Brand Pack: `/Users/deanlatham/Desktop/Morph/MORPh Brand Pack/`
- Brand Voice Guidelines: `.claude/brand-voice-guidelines.md`
