---
name: morph-onboarding-document
description: |
  Generate a personalised Morph Consultancy new starter onboarding document PDF from a filled-in Onboarding Brief. Use when Dean says "Morph onboarding document", "create Morph onboarding for [name]", "generate Morph new starter doc", "Morph onboarding", "new Morph starter pack", or hands back a completed Onboarding-Brief.docx with Brand = Morph. Applies the MORPh brand theme (deep navy / purple → magenta gradient, MORPh ring logo, no CONFIDENTIAL pill) and saves the final PDF to the Morph onboarding folder. Optionally generates a separate role-agnostic Pre-Start Checklist PDF for the hiring manager. Not for TPN onboarding — use tpn-onboarding-document for that.
version: 1.0.0
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Morph Onboarding Document Generator

Generate a personalised Morph Consultancy new starter onboarding pack (A4 PDF, MORPh brand theme) from a filled-in Onboarding Brief.

---

## Reference files

| File | Path | Purpose |
|------|------|---------|
| Morph HTML template | `/Users/deanlatham/git-practice/onboarding_templates/morph_template.html` | Master template with `{{PLACEHOLDER}}` tokens and MORPh brand styling |
| Onboarding Brief form | `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Onboarding-Brief.docx` | The Word form the hiring manager fills in |
| Output folder | `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Morph/` | Where final PDFs are saved |

---

## Workflow

### Step 1 — Confirm there's a filled-in brief

Ask Dean: "Has the hiring manager filled in the Onboarding Brief? If yes, drop the path here. If not, I'll send them the blank form at `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Onboarding-Brief.docx`."

**Do not proceed without a completed brief.** No chat-based interview fallback — this is by explicit instruction. If Dean doesn't have a filled brief, direct him to the form.

### Step 2 — Read and parse the brief

Use pandoc to extract the filled-in brief to markdown:

```bash
pandoc --track-changes=all "[path to filled brief]" -o /tmp/brief.md
```

Parse these fields from the brief:

| Token | Section in brief | Notes |
|-------|-----------------|-------|
| `{{NEW_HIRE_NAME}}` | Section 2 — Full name | |
| `{{ROLE}}` | Section 2 — Job title / role | Used in cover title, welcome copy, running header |
| `{{TEAM}}` | Section 2 — Team | |
| `{{START_DATE}}` | Section 2 — Start date | Format as "DD Month YYYY" (e.g. "20 April 2026") — no time by default |
| `{{MANAGER}}` | Section 2 — Hiring manager name and role | Just the name unless Dean says otherwise |
| `{{TUE_EXTRA}}` | Section 4 — Tuesday | Convert free text into `<li>…</li>` items. Empty string if nothing provided |
| `{{WED_EXTRA}}` | Section 4 — Wednesday | Same |
| `{{THU_EXTRA}}` | Section 4 — Thursday | Same |

**Validate:**
- Section 1 — Brand must say "Morph" (or "MORPh"). If it says "TPN", stop and tell Dean to run tpn-onboarding-document instead.
- If any Section 2 field is blank or "TBC", flag it to Dean and ask for a value before generating.

### Step 3 — Handle optional sections

Check Section 7 of the brief:

- **Pre-Start Checklist as separate document? Yes** → after the main PDF is generated, also create a Morph-themed standalone Pre-Start Checklist PDF (mirror the pattern of the TPN pre-start — clone the Morph template, strip to just cover + Pre-Start section, rename heading, render). Output: `Morph-Pre-Start-Checklist.pdf` in the Morph folder.
- **Spectrum Life / EAP section?** — this section does not exist in the Morph template by default. Ignore.
- **Notes & Personal Log? No** → remove the Notes section and re-paginate.

### Step 4 — Render

**4a. Copy the template to a working file:**
```bash
cp /Users/deanlatham/git-practice/onboarding_templates/morph_template.html /tmp/morph_working.html
```

**4b. Apply optional section removals** (if needed — use Python to delete sections and renumber page footers/TOC, following the same pattern as the Pre-Start Checklist removal we've done before).

**4c. Substitute placeholders.** Use a Python script:

```python
import re
path = "/tmp/morph_working.html"
with open(path) as f: content = f.read()

# Extras — each is either a list of <li> strings joined, or empty
tue_extra = "\n      ".join(f"<li>{item}</li>" for item in tue_items) if tue_items else ""
wed_extra = "\n      ".join(f"<li>{item}</li>" for item in wed_items) if wed_items else ""
thu_extra = "\n      ".join(f"<li>{item}</li>" for item in thu_items) if thu_items else ""

substitutions = {
    "{{NEW_HIRE_NAME}}": new_hire_name,
    "{{ROLE}}": role,
    "{{TEAM}}": team,
    "{{START_DATE}}": start_date,
    "{{MANAGER}}": manager,
    "{{TUE_EXTRA}}": tue_extra,
    "{{WED_EXTRA}}": wed_extra,
    "{{THU_EXTRA}}": thu_extra,
}
for token, value in substitutions.items():
    content = content.replace(token, value)

with open(path, "w") as f: f.write(content)
```

**4d. Render to PDF via Chrome headless:**

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Morph/Morph-[FirstName]-Onboarding.pdf" \
  "file:///tmp/morph_working.html"
```

Filename convention: `Morph-[FirstName]-Onboarding.pdf` (e.g. `Morph-Laura-Onboarding.pdf`). If `[FirstName]` has unusual characters, sanitise to alphanumerics only.

### Step 5 — Verify and confirm

Read the first page of the generated PDF to verify the cover populated correctly — especially check the MORPh ring logo rendered and there is **no CONFIDENTIAL pill** on the cover (this was explicitly removed).

Then confirm to Dean:
- File path of main PDF
- File path of Pre-Start Checklist PDF (if generated)
- Any fields left as "TBC" or open questions from the brief

---

## Brand rules

- Do not modify the MORPh brand colours, typography, or visual layout. The template already reflects Dean's approved MORPh theme: deep navy/purple background, indigo headings, magenta accent bar, stacked-bar checklist icons, gradient ring logo.
- **No CONFIDENTIAL pill on the cover.** Dean explicitly removed this. Do not re-add under any circumstance.
- Do not add your own copy to the sections. Template copy is set. Only placeholder tokens and optional Week 1 extras should change per brief.
- Key Contacts, Tools & System Access, HR Policies, Compliance tables, and Values content are fixed unless Dean explicitly asks to amend the template.

---

## Optional contacts additions

If Section 6 of the brief lists any new Key Contacts:

- Append them as additional `<tr>` rows in the Key Contacts table in `/tmp/morph_working.html` before rendering.
- Do not duplicate existing contacts.

---

## After generation

Confirm with Dean:
- "Generated `Morph-[Name]-Onboarding.pdf` in the Morph folder."
- If Pre-Start was also generated: "And `Morph-Pre-Start-Checklist.pdf` alongside it."
- Flag any unresolved questions or TBCs from the brief.
