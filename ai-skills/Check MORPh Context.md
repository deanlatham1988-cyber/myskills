---
name: check-morph-context
description: Load the MORPh Context briefing doc from Dean's Obsidian vault and use it to ground any MORPh-related task. Use when Dean says "check morph context", "load morph context", "read morph context", "I'm working on MORPh", "starting a MORPh task", or any phrasing that suggests he wants the MORPh Context doc read before the task starts. Also use proactively at the start of any MORPh task — Dean's role, Project 2026, any of the five workstreams (People, Systems, Sales/Marketing, Event Experience, NELs), Morph Training, The Pharmacist Network, NELs, Amz, Ryan Smith, Ariyan, Will, brand assets, branded PDFs/DOCX/PPTX, onboarding documents, event marketing, or anything involving the MORPh Brand Pack.
---

# Check MORPh Context

This skill reads Dean's live MORPh Context briefing doc from Obsidian. That doc is the single source of truth for anything MORPh-related. Read it at the start of any MORPh task so you have full context on role, business, workstreams, standards, and where to find things — before making assumptions.

## When to use

Always use this skill at the start of a MORPh task if you haven't already loaded the context this session. Triggers:

- Dean says "check morph context", "load morph context", "read morph context"
- Dean references any of the five workstreams (WS1 People, WS2 Systems, WS3 Sales/Marketing, WS4 Event Experience, WS5 NELs)
- Dean references Project 2026, the transformation programme, Morph Training, The Pharmacist Network (TPN), NELs, Amz, Ryan Smith, Ariyan, Will
- Dean is creating a branded artifact (PDF, DOCX, PPTX, HTML, Gamma deck) for MORPh or TPN
- Dean is working on onboarding documents, event marketing, HR, systems specs, recruitment automation, clinical training content, or the brand pack

Do **not** re-read it if it's already been read in the current session — reference it instead.

## How to apply

**Step 1 — Read the context doc**

Read the file at:
```
/Users/deanlatham/Desktop/Obsidian Vault/AI/Context for AI/MORPh Context.md
```

If the file can't be found or read, tell Dean rather than guessing the context. The doc is Dean's actively maintained single source of truth — do not substitute remembered facts for a failed read.

**Step 2 — Orient**

Scan the doc for the sections relevant to the task at hand:

- **Dean's Role** — confirm who Dean is, who he manages (Will, Ariyan), who he works with (Amz, Ryan, Alex)
- **The Business** — Morph Training vs The Pharmacist Network; group structure; NEL delivery model
- **Workstream Progress** — current status of WS1–WS5 with what's done and what's remaining
- **What Has Been Built** — ~35 deliverables including process maps, feedback system, HR/onboarding, marketing assets, systems specs, skills
- **Document Creation Preferences** — decision tree for which tool/skill to use for any artifact (onboarding generators, theme builders, toolkit-gamma, PDF generators)
- **Document Formatting Standards** — canonical typography hierarchy (36pt cover / 26pt H1 / 20pt H2 / 16pt H3 / 11pt body), 1.5 line spacing, structural rules, reusable components
- **Where to Find Things** — Asana, desktop folders, brand assets, skills, transcripts

**Step 3 — Apply the context**

Use what you've read to inform the task. Specifically:

- If creating a branded document, consult the **Document Creation Preferences** decision tree to pick the correct tool (theme builder skill, onboarding generator, ReportLab script, toolkit-gamma, etc.) and apply the **Document Formatting Standards** hierarchy verbatim.
- If the task involves a workstream, reference the current status (done / remaining) before planning work.
- If the task involves an external stakeholder or colleague, reference their role from **Dean's Role** so you address the right person.

**Step 4 — Flag stale or conflicting information**

If the doc contradicts something you're working on (e.g. a task has moved from "remaining" to "done" since the doc was last updated, or a skill listed in the doc no longer exists), flag it to Dean and offer to update the Obsidian doc. Do not silently reconcile — the doc is the source of truth, but Dean maintains it.

## Companion skills

- `obsidian-capture` — use to update the MORPh Context doc itself when Dean wants to add new context
- `morph-theme-builder` / `tpn-theme-builder` — apply the actual brand styling once you know from Context which is needed
- `toolkit-gamma` — for Gamma decks (Context points at this)
- `consolidate-memory` — reflective pass over local memory files; not for Obsidian
