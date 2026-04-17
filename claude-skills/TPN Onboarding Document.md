---
name: tpn-onboarding-document
description: |
  Generate a personalised TPN (The Pharmacist Network) new starter onboarding document PDF from a filled-in Onboarding Brief. Use when Dean says "TPN onboarding document", "create TPN onboarding for [name]", "generate TPN new starter doc", "TPN onboarding", "new TPN starter pack", or hands back a completed Onboarding-Brief.docx with Brand = TPN. Applies the TPN brand theme (deep indigo / violet / purple gradient) and saves the final PDF to the TPN onboarding folder. Optionally generates a separate role-agnostic Pre-Start Checklist PDF for the hiring manager. Not for Morph Consultancy onboarding — use morph-onboarding-document for that.
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

# TPN Onboarding Document Generator

Generate a personalised TPN new starter onboarding pack (A4 PDF, TPN brand theme) from a filled-in Onboarding Brief.

---

## Reference files

| File | Path | Purpose |
|------|------|---------|
| TPN HTML template | `/Users/deanlatham/git-practice/onboarding_templates/tpn_template.html` | Master template with `{{PLACEHOLDER}}` tokens and TPN brand styling |
| Onboarding Brief form | `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Onboarding-Brief.docx` | The Word form the hiring manager fills in |
| Pre-Start Checklist source | `/Users/deanlatham/git-practice/outputs/tpn_pre_start_checklist.html` | Standalone, role-agnostic pre-start checklist (for the hiring manager) |
| Output folder | `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/TPN/` | Where final PDFs are saved |

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
- Section 1 — Brand must say "TPN". If it says "Morph", stop and tell Dean to run morph-onboarding-document instead.
- If any Section 2 field is blank or "TBC", flag it to Dean and ask for a value before generating.

### Step 3 — Handle optional sections

Check Section 7 of the brief:

- **Pre-Start Checklist as separate document? Yes** → after the main PDF is generated, also render `/Users/deanlatham/git-practice/outputs/tpn_pre_start_checklist.html` to `TPN-[FirstName]-Pre-Start-Checklist.pdf` in the TPN folder.
- **Spectrum Life / EAP section? No** → remove it from the template before rendering (see Step 4b).
- **Notes & Personal Log? No** → remove the Notes section and re-paginate.

### Step 4 — Render

**4a. Copy the template to a working file:**
```bash
cp /Users/deanlatham/git-practice/onboarding_templates/tpn_template.html /tmp/tpn_working.html
```

**4b. Apply optional section removals** (if needed — use Python to delete sections and renumber page footers/TOC, following the same pattern as the Pre-Start Checklist removal we've done before).

**4c. Substitute placeholders.** Use a Python script:

```python
import re
path = "/tmp/tpn_working.html"
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
  --print-to-pdf="/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/TPN/TPN-[FirstName]-Onboarding.pdf" \
  "file:///tmp/tpn_working.html"
```

Filename convention: `TPN-[FirstName]-Onboarding.pdf` (e.g. `TPN-Laura-Onboarding.pdf`). If `[FirstName]` has unusual characters, sanitise to alphanumerics only.

### Step 5 — Verify and confirm

Read the first page of the generated PDF to verify the cover populated correctly. Then confirm to Dean:
- File path of main PDF
- File path of Pre-Start Checklist PDF (if generated)
- Any fields left as "TBC" or open questions from the brief

---

## Brand rules

- Do not modify the TPN brand colours, typography, or visual layout. The template already reflects Dean's approved TPN theme.
- Do not add your own copy to the sections. Template copy is set. Only placeholder tokens and optional Week 1 extras should change per brief.
- Key Contacts, Tools & System Access, HR Policies, Compliance tables, and Values content are fixed unless Dean explicitly asks to amend the template.

---

## Optional contacts additions

If Section 6 of the brief lists any new Key Contacts:

- Append them as additional `<tr>` rows in the Key Contacts table in `/tmp/tpn_working.html` before rendering.
- Do not duplicate existing contacts.

---

## After generation

Confirm with Dean:
- "Generated `TPN-[Name]-Onboarding.pdf` in the TPN folder."
- If Pre-Start was also generated: "And `TPN-Pre-Start-Checklist.pdf` alongside it."
- Flag any unresolved questions or TBCs from the brief.
