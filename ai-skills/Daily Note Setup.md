# Daily Note Setup

**Skill name:** daily-note-setup
**Description:** Finds today's Obsidian daily note and prepends a structured daily template to the top. Use this skill whenever Dean asks to set up his daily note, get Obsidian ready for today, prepare today's note, start his day in Obsidian, or open his daily note. Triggers include: "set up my daily note", "get my Obsidian ready for today", "prepare today's note", "start my day in Obsidian", "open my daily note", "daily note template", or "morning setup".
**Install file:** daily-note-setup.skill

---

## Purpose

Automatically locates your daily note using your Obsidian config (reads `.obsidian/daily-notes.json` so it works regardless of your folder or filename format), creates the note if it doesn't exist yet, then prepends a full daily template to the top. A hidden marker prevents it from adding the template twice if triggered more than once.

---

## Template Sections

1. To-Do — five empty checkboxes
2. Core Priorities — three numbered slots for the day's main goals
3. Sleep — hours and quality rating
4. Medication — Elvanse morning and afternoon tick boxes
5. Mood & Energy — two /10 ratings
6. Exercise / Movement — session and notes
7. Gut — comfort rating and notes
8. Thoughts of the Day — free text

To modify the template contents, edit the template block in the `.skill` file directly.

---

## Dependencies

- Access to `/Users/deanlatham/Desktop/Obsidian Vault` (file system)
- `.obsidian/daily-notes.json` must exist in the vault for automatic path resolution
