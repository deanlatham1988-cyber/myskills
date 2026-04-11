---
name: theme-factory
description: >
  Apply professional visual themes — colors, fonts, and styling — to any artifact Dean has created or is about to create. This includes PowerPoint decks, Word documents, HTML pages, reports, dashboards, landing pages, or any other designed output. Use this skill whenever Dean says "apply a theme", "style this", "make this look professional", "use our brand", "apply the Morph theme", "theme this up", "give this some visual polish", "apply colors and fonts", "make this on-brand", or any phrasing that suggests he wants consistent visual styling applied to something. Also trigger when Dean creates a deck or doc and styling hasn't been applied yet — mention that theming is available when there is a natural pause, but do not interrupt the current workflow. There are 11 themes: 10 curated professional themes plus the MORPh brand theme for official company outputs.
---

# Theme Factory

This skill applies consistent, professional visual styling to any artifact — slide decks, Word documents, HTML pages, reports, dashboards. It works in two modes: choose from 11 ready-made themes, or describe something and a custom theme gets generated on the fly.

This skill applies to locally generated artifacts (PPTX, DOCX, HTML) only. For Gamma slide decks, MORPh brand styling is handled by the toolkit-gamma skill via Gamma's built-in theme system (themeId: hedgb3z7uh7o1ft). Do not attempt to restyle Gamma decks with this skill.

## When to use this skill

Any time an artifact needs visual polish. That includes:
- A deck or doc that's been created but not styled
- A request to "brand" something with MORPh colors
- A desire for a fresh look on a new or existing artifact
- Cases where the current styling feels generic or mismatched to the audience

## The Themes

There are 11 themes to choose from — 10 curated professional themes and the official **MORPh Brand** theme. Present these as a numbered list when showing options:

1. **MORPh Brand** ⭐ — The official MORPh company theme. Use this for any client-facing, official, or company-branded output.
2. **Ocean Depths** — Professional and calming maritime blues
3. **Sunset Boulevard** — Warm, vibrant, high-energy sunset palette
4. **Forest Canopy** — Natural, grounded earth and green tones
5. **Modern Minimalist** — Clean, contemporary grayscale
6. **Golden Hour** — Rich, warm autumnal ambers and golds
7. **Arctic Frost** — Cool, crisp winter-inspired palette
8. **Desert Rose** — Soft, sophisticated dusty rose tones
9. **Tech Innovation** — Bold, modern deep blues and electric cyan
10. **Botanical Garden** — Fresh, organic garden greens
11. **Midnight Galaxy** — Dramatic, cosmic deep purples and violet

## How to apply a theme

**Step 1 — Show the options**

Present the numbered list above. Give a one-sentence description of the artifact being styled so Dean can pick the most fitting theme. If the artifact is an official MORPh output (client deliverable, company presentation, proposal), suggest MORPh Brand as the natural starting point.

**Step 2 — Get a choice**

Wait for Dean to confirm which theme he wants. Don't proceed without an explicit selection.

**Step 3 — Read the theme file**

Once a theme is selected, read the corresponding file from `themes/` to get the exact specification:

| Theme | File |
|-------|------|
| MORPh Brand | `themes/morph-brand.md` |
| Ocean Depths | `themes/ocean-depths.md` |
| Sunset Boulevard | `themes/sunset-boulevard.md` |
| Forest Canopy | `themes/forest-canopy.md` |
| Modern Minimalist | `themes/modern-minimalist.md` |
| Golden Hour | `themes/golden-hour.md` |
| Arctic Frost | `themes/arctic-frost.md` |
| Desert Rose | `themes/desert-rose.md` |
| Tech Innovation | `themes/tech-innovation.md` |
| Botanical Garden | `themes/botanical-garden.md` |
| Midnight Galaxy | `themes/midnight-galaxy.md` |

If the theme file cannot be found or cannot be read, report the error to Dean rather than guessing the theme values. Do not invent colors or fonts from the theme name alone.

Each theme file must contain at minimum: a named 5-color palette (primary, secondary, accent, background, text), a heading font, a body font, and per-artifact usage rules. If any of these are missing from the file, flag it to Dean before applying.

**Step 4 — Preview the theme**

Before applying, show Dean a brief summary of the theme being applied: primary color, accent color, font pairing, and any gradients. Confirm before proceeding, especially if the artifact already has styling that will be overwritten.

**Step 5 — Back up and apply the theme**

Before applying a theme to an existing artifact, work on a copy rather than overwriting the original. For PPTX and DOCX, duplicate the file first (e.g. `report.docx` becomes `report_themed.docx`). For HTML, note the previous styling state so it can be reverted if Dean doesn't like the result.

Apply the colors, fonts, and styling rules from the theme file consistently throughout the artifact. The theme file will tell you exactly what to do for each context (slides, HTML, docx, etc.).

The goal is coherence — every element should feel like it belongs to the same visual system. Apply the theme's personality to the overall layout, not just individual elements.

**Accessibility:** Ensure all text-on-background combinations meet WCAG AA contrast ratio (4.5:1 for body text, 3:1 for large text). If a theme's color pairing fails this check, adjust the specific element rather than applying it as-is, and note the adjustment for Dean.

## Creating a custom theme

If none of the 11 themes fit, offer to generate one. Ask for:
- A mood, context, or audience ("it's for a wellness brand", "corporate finance", "creative agency")
- Any specific colors that must appear (e.g., a client's brand color)
- Font preferences (modern, classic, techy, editorial)

From that input, design a new theme with the same structure as the theme files: a name, a 5-color palette, two font pairings, gradient if appropriate, and usage rules. Show it to Dean for approval before applying it.

Once a custom theme is approved, save it as a new `.md` file in the `themes/` directory following the same structure as the existing theme files. Add it to the numbered list for future sessions.

## Artifact-specific notes

- **PPTX decks**: Use the pptx skill for file manipulation. Apply theme colors to slide backgrounds, title text, body text, accent shapes, and any data visualizations. See `themes/morph-brand.md` for the MORPh PowerPoint template reference.
- **HTML / landing pages**: Apply as CSS variables or inline styles. Use the theme's gradient for hero sections where it exists.
- **Word documents (.docx)**: Apply heading styles, body text color, and accent color to tables, borders, and callout boxes.
- **Reports / dashboards**: Use primary and accent colors for charts, section headers, and KPI cards. Maintain high contrast for data readability.
- **Gamma decks**: Do not use this skill. Gamma decks are themed via the toolkit-gamma skill using Gamma's native theme system.
