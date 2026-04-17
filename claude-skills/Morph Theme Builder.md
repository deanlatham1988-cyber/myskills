# Morph Theme Builder

**Skill name:** morph-theme-builder
**Description:** Apply the MORPh brand theme — colors, fonts, and styling — to any artifact Dean has created or is about to create. This includes PowerPoint decks, Word documents, HTML pages, reports, dashboards, landing pages, or any other designed output. Use this skill whenever Dean says "apply a theme", "style this", "make this look professional", "use our brand", "apply the Morph theme", "theme this up", "give this some visual polish", "apply colors and fonts", "make this on-brand", or any phrasing that suggests he wants consistent MORPh branding applied to something. Also trigger when Dean creates a deck or doc and styling hasn't been applied yet — mention that theming is available when there is a natural pause, but do not interrupt the current workflow.
**Install file:** morph-theme-builder.skill

---

## Purpose

This skill applies the MORPh brand theme consistently to any artifact — slide decks, Word documents, HTML pages, reports, dashboards.

This skill applies to locally generated artifacts (PPTX, DOCX, HTML) only. For Gamma slide decks, MORPh brand styling is handled by the toolkit-gamma skill via Gamma's built-in theme system (themeId: hedgb3z7uh7o1ft). Do not attempt to restyle Gamma decks with this skill.

---

## When to use this skill

Any time an artifact needs MORPh branding applied. That includes:
- A deck or doc that's been created but not styled
- A request to "brand" something with MORPh colors
- Client-facing, official, or company-branded outputs
- Cases where the current styling feels generic or mismatched to the audience

---

## The Theme

This skill uses the single **MORPh Brand** theme for all outputs — the official MORPh company theme for any client-facing, official, or company-branded artifact.

---

## How to apply the theme

### Step 1 — Read the theme file

Read `themes/morph-brand.md` to get the exact specification — color palette, fonts, gradients, and per-artifact usage rules.

If the theme file cannot be found or cannot be read, report the error to Dean rather than guessing the theme values. Do not invent colors or fonts.

The theme file must contain at minimum: a named 5-color palette (primary, secondary, accent, background, text), a heading font, a body font, and per-artifact usage rules. If any of these are missing, flag it to Dean before applying.

### Step 2 — Preview the theme

Show Dean a brief summary of what will be applied: primary color, accent color, font pairing, and any gradients. Confirm before proceeding, especially if the artifact already has styling that will be overwritten.

### Step 3 — Back up and apply

Before applying to an existing artifact, work on a copy rather than overwriting the original. For PPTX and DOCX, duplicate the file first (e.g. `report.docx` becomes `report_morph.docx`). For HTML, note the previous styling state so it can be reverted if Dean doesn't like the result.

Apply the colors, fonts, and styling rules from the theme file consistently throughout the artifact. The goal is coherence — every element should feel like it belongs to the same visual system.

**Accessibility:** Ensure all text-on-background combinations meet WCAG AA contrast ratio (4.5:1 for body text, 3:1 for large text). If a color pairing fails this check, adjust the specific element rather than applying it as-is, and note the adjustment for Dean.

---

## Artifact-specific notes

- **PPTX decks**: Use the pptx skill for file manipulation. Apply theme colors to slide backgrounds, title text, body text, accent shapes, and any data visualizations. See `themes/morph-brand.md` for the MORPh PowerPoint template reference.
- **HTML / landing pages**: Apply as CSS variables or inline styles. Use the theme's gradient for hero sections where it exists.
- **Word documents (.docx)**: Apply heading styles, body text color, and accent color to tables, borders, and callout boxes.
- **Reports / dashboards**: Use primary and accent colors for charts, section headers, and KPI cards. Maintain high contrast for data readability.
- **Gamma decks**: Do not use this skill. Gamma decks are themed via the toolkit-gamma skill using Gamma's native theme system.
