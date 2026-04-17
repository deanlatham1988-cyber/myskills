---
name: morph-onboarding-document
description: |
  Generate a personalised Morph Consultancy new starter onboarding document PDF from a filled-in Onboarding Brief. Use when Dean says "Morph onboarding document", "create Morph onboarding for [name]", "generate Morph new starter doc", "Morph onboarding", "new Morph starter pack", or hands back a completed Onboarding-Brief.docx with Brand = Morph. The template is a skeleton — all role/person-specific content (schedule, week plan, contacts, tools, training, HR policies) comes from the filled-in brief. Applies the MORPh brand theme (deep navy / purple → magenta gradient, MORPh ring logo, no CONFIDENTIAL pill) and saves the final PDF to the Morph onboarding folder. Optionally generates a separate role-agnostic Pre-Start Checklist PDF for the hiring manager. Not for TPN onboarding — use tpn-onboarding-document for that.
version: 2.0.0
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

Generate a personalised Morph Consultancy new starter onboarding pack (A4 PDF, MORPh brand theme) from a filled-in Onboarding Brief. The HTML template is a pure skeleton — this skill's job is to take the form answers and inject them into the right placeholders.

---

## Reference files

| File | Path | Purpose |
|------|------|---------|
| Morph HTML template (skeleton) | `/Users/deanlatham/git-practice/onboarding_templates/morph_template.html` | Master skeleton with placeholder tokens and MORPh brand styling |
| Onboarding Brief form | `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Onboarding-Brief.docx` | The Word form the hiring manager fills in |
| Output folder | `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Morph/` | Where final PDFs are saved |

---

## Workflow

### Step 1 — Confirm there's a filled-in brief

Ask Dean: "Has the hiring manager filled in the Onboarding Brief? If yes, drop the path here. If not, I'll send them the blank form at `/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Onboarding-Brief.docx`."

**Do not proceed without a completed brief.** No chat-based interview fallback — this is by explicit instruction.

### Step 2 — Parse the brief

Extract the filled brief to markdown:

```bash
pandoc --track-changes=all "[path to filled brief]" -o /tmp/brief.md
```

Parse the 10 sections. Validate Section 1 says "Morph" (or "MORPh") — if it says "TPN", stop and direct Dean to `tpn-onboarding-document`.

### Step 3 — Token set

The Morph template uses these 12 placeholders. Map each from the brief:

| Token | Source section | Format |
|-------|---------------|--------|
| `{{NEW_HIRE_NAME}}` | §2 Full name | Plain text |
| `{{ROLE}}` | §2 Job title / role | Plain text (used in cover title, welcome, running header) |
| `{{TEAM}}` | §2 Team | Plain text |
| `{{START_DATE}}` | §2 Start date | "DD Month YYYY" |
| `{{MANAGER}}` | §2 Hiring manager | Name only unless Dean says otherwise |
| `{{DAY1_ROWS}}` | §3 Day 1 schedule table | `<tr><td>...</td>...</tr>` rows, one per schedule entry |
| `{{WEEK1_CONTENT}}` | §4 Week 1 plan | HTML block: one `<div class="day-heading">Day</div><ul class="checklist"><li>bullet</li>...</ul>` per day (Tue/Wed/Thu/Fri) |
| `{{TRAINING_INTRO}}` | §5 intro paragraph | Plain paragraph text (can include `<strong>` for emphasis) |
| `{{TRAINING_ROWS}}` | §5 training table | `<tr><td>Module</td><td>Provider</td><td>Deadline</td><td></td></tr>` rows (leave last cell empty for sign-off) |
| `{{KEY_CONTACTS_ROWS}}` | §6 contacts table | `<tr><td>Name</td><td>Role</td><td>For What</td><td>Contact</td></tr>` rows |
| `{{TOOLS_ROWS}}` | §7 tools table | `<tr><td>Tool</td><td>Access</td><td>Requested By</td><td></td></tr>` rows (leave last cell empty for granted-tick) |
| `{{HR_POLICIES_CONTENT}}` | §8 HR Policies free text | HTML block — use `<h2>Heading</h2><p>…</p>` structure. Preserve hiring manager's section headings. |

**Validation:**
- If any Section 2 field is blank or "TBC", flag to Dean and ask for a value.
- If §3 is empty, flag — Day 1 schedule is required.
- If §4 is empty for any day, that day becomes an empty day heading in the output. Warn Dean but proceed.
- §5, §6, §7 tables can have any number of rows.
- §8 can be short if the hiring manager has little to add — that's fine.

### Step 4 — Handle optional sections (§9)

- **Pre-Start Checklist as separate document? Yes** → after the main PDF is generated, also create a Morph-themed standalone Pre-Start Checklist PDF (clone the Morph template, strip to cover + Pre-Start section, render). Output: `Morph-Pre-Start-Checklist.pdf` in the Morph folder.
- **Notes & Personal Log? No** → remove the Notes section from the working HTML and re-paginate footers/TOC.

### Step 5 — Render

**5a. Copy template to working file:**
```bash
cp /Users/deanlatham/git-practice/onboarding_templates/morph_template.html /tmp/morph_working.html
```

**5b. Apply optional section removals** if needed (Notes & Personal Log).

**5c. Substitute placeholders** with a Python script. Example:

```python
import re, html
path = "/tmp/morph_working.html"
with open(path) as f: content = f.read()

# Build HTML fragments from brief
day1_rows = "\n        ".join(
    f"<tr><td>{r['time']}</td><td>{r['activity']}</td><td>{r['with']}</td><td>{r['location']}</td></tr>"
    for r in day1_schedule
)

week1_blocks = []
for day, bullets in week1_plan.items():
    lis = "\n      ".join(f"<li>{b}</li>" for b in bullets)
    week1_blocks.append(f'<div class="day-heading">{day}</div>\n    <ul class="checklist">\n      {lis}\n    </ul>')
week1_content = "\n\n    ".join(week1_blocks)

training_rows = "\n        ".join(
    f"<tr><td>{m['module']}</td><td>{m['provider']}</td><td>{m['deadline']}</td><td></td></tr>"
    for m in training_modules
)

contacts_rows = "\n        ".join(
    f"<tr><td>{c['name']}</td><td>{c['role']}</td><td>{c['for_what']}</td><td>{c['contact']}</td></tr>"
    for c in key_contacts
)

tools_rows = "\n        ".join(
    f"<tr><td>{t['tool']}</td><td>{t['access']}</td><td>{t['requested_by']}</td><td></td></tr>"
    for t in tools
)

substitutions = {
    "{{NEW_HIRE_NAME}}": new_hire_name,
    "{{ROLE}}": role,
    "{{TEAM}}": team,
    "{{START_DATE}}": start_date,
    "{{MANAGER}}": manager,
    "{{DAY1_ROWS}}": day1_rows,
    "{{WEEK1_CONTENT}}": week1_content,
    "{{TRAINING_INTRO}}": training_intro,
    "{{TRAINING_ROWS}}": training_rows,
    "{{KEY_CONTACTS_ROWS}}": contacts_rows,
    "{{TOOLS_ROWS}}": tools_rows,
    "{{HR_POLICIES_CONTENT}}": hr_policies_html,
}
for token, value in substitutions.items():
    content = content.replace(token, value)

with open(path, "w") as f: f.write(content)
```

**HTML-escape values** that might contain `&`, `<`, `>`, `"`. Use `html.escape()` in Python for plain-text cells (name/role/contact/etc). Do NOT escape pre-built HTML fragments.

**5d. Render to PDF via Chrome headless:**

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="/Users/deanlatham/Desktop/git-practice/Morph/Morph New World /People /Oboarding/Morph/Morph-[FirstName]-Onboarding.pdf" \
  "file:///tmp/morph_working.html"
```

Filename: `Morph-[FirstName]-Onboarding.pdf`. Sanitise FirstName to alphanumerics only.

### Step 6 — Verify and confirm

Read the first page of the generated PDF. Verify:
- Cover populated correctly (name, role, start date, manager)
- MORPh ring logo rendered
- **No CONFIDENTIAL pill on the cover** — this was explicitly removed and must not return

Confirm to Dean:
- File path of main PDF
- File path of Pre-Start Checklist PDF (if generated)
- Any fields left as "TBC" or open questions from the brief

---

## Brand rules

- Do not modify the MORPh brand colours, typography, or visual layout. The skeleton reflects Dean's approved MORPh theme: deep navy/purple cover, indigo headings, magenta accent bar, stacked-bar checklist icons, gradient ring logo.
- **No CONFIDENTIAL pill on the cover.** Dean explicitly removed this. Do not re-add under any circumstance.
- Do not invent content. If the brief is missing something, ask Dean — don't fill gaps with assumptions.
- Section headings and running layout are fixed. Only the tokenised placeholders should change per brief.
