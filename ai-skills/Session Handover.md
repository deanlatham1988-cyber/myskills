---
name: session-handover
description: Generate a handover document so the next Claude chat can pick up exactly where this one left off. Use when the user says "session handover", "hand off this session", "handover document", "prep for next chat", "bookmark this session", "write a handover", "pick this up later", "continuation brief", "the chat is getting slow", "this session is degrading", "pack this up for next time", or "/session-handover". Writes a structured markdown file to .claude/HANDOFF.md that the next session reads as its first action.
metadata:
  version: 1.0.0
---

# Session Handover

You are writing a **session continuity brief**. The receiver is the next Claude chat, not a human. Dean's current session is ending (too long, degrading, or paused) and he needs everything the next chat requires to resume without losing ground.

Your job: capture the session's goal, decisions, state, and outstanding threads into a single dense markdown file the next Claude reads as its first action.

---

## Pipeline

Run these steps in order. Use parallel tool calls where independent.

### 1. Gather state from disk
- `git status --short` and `git log --oneline -5` — current branch, uncommitted work, recent commits
- `git diff --stat` — what's been modified in this session (if uncommitted)
- Read `.ultraplan/plan.md` if it exists — the active plan is often the best summary of intent
- Read any skill/spec/plan files that were created or edited during the session (infer from conversation)
- Check for a current `TodoWrite` list — capture all non-completed items verbatim

### 2. Synthesise session events from the conversation
Scan back through the conversation and extract:
- **Goal** — what is Dean trying to accomplish? One paragraph.
- **Decisions made** — choices that were resolved, with the rationale. Mark who decided what (Dean vs. Claude recommendation Dean approved).
- **Files created / modified / deleted** — exact absolute paths.
- **Things tried and ruled out** — approaches that were rejected, with the reason. These are critical: the next session will re-propose them unless warned.
- **User preferences expressed this session** — any Dean-specific guidance that came up (style, tools, approach) that isn't already in his standing memory.
- **Open questions** — things awaiting Dean's input or a future decision.

### 3. Ask one catch-all question
Before writing the file, ask Dean exactly one question:
> "Before I write the handover — is there anything critical from this session I might have missed that the next chat needs to know?"

Accept whatever he says (including "no, go ahead") and fold it into the right section.

### 4. Write the handover file
Write to `{cwd}/.claude/HANDOFF.md` (overwrite if exists). Also write an archive copy to `{cwd}/.claude/handovers/YYYY-MM-DD-HHMM-[slug].md` where `[slug]` is a 2-3 word kebab-case description of the session goal (e.g. `session-handover-skill`, `morph-onboarding-pdf`).

Create the `.claude/handovers/` directory if it doesn't exist. If `{cwd}/.claude/` doesn't exist, create it.

### 5. Print the resume instruction to Dean
After the file is written, end your response with this exact block (substitute the real absolute path):

```
Handover saved to {absolute-path-to-HANDOFF.md}

Paste this into your next session:
─────────────────────────────────
Review {absolute-path-to-HANDOFF.md} before we continue.
─────────────────────────────────
```

Do not add extra commentary after this block. The block IS the ending.

---

## Output Template

Use this exact structure for `HANDOFF.md`. Fill every section — if a section is genuinely empty, write "_None._" rather than omitting it.

```markdown
# Session Handover — {Short Title}
_Generated: {YYYY-MM-DD HH:MM} · Project: {project-dir-name} · Branch: {git-branch}_

## Resume Prompt
Paste into a new Claude chat to resume:
> Review `{absolute-path-to-this-file}` before we continue.

## Session Goal
{One paragraph — what Dean is trying to accomplish, framed so a cold reader understands the why.}

## Current State
- **Branch:** {git branch}
- **Uncommitted changes:** {list of modified/untracked files, or "None"}
- **Active plan file:** {path to .ultraplan/plan.md or similar, or "None"}
- **Open todos (from this session):**
  - [ ] {todo 1}
  - [ ] {todo 2}

## What's Been Done
Decisions made and work completed, most recent first:
- **{Decision/action}** — {one-line rationale or outcome}. Files: `{paths}` (if applicable).
- ...

## What's Left
- {Pending task 1 — with enough detail to act on, including file paths if known}
- {Pending task 2}
- **Open questions for Dean:** {anything awaiting his input}

## Critical Context for the Next Session

### Files to read first
Ranked by importance for fastest orientation:
1. `{path}` — {why}
2. `{path}` — {why}
3. `{path}` — {why}

### Anti-patterns — already tried or ruled out
- {Thing X tried/proposed, rejected because Y}
- ...

### Session-specific preferences
Guidance Dean gave during this session that isn't in his standing memory:
- {preference 1}
- {preference 2}

### Domain context relevant to the task
{Anything MORPh/TPN brand-specific, technical-stack-specific, or project-specific the next session needs. Keep to what's actually relevant to the pending work, not a general brief.}

## Next Immediate Step
The very first thing the next session should do, written as an instruction:
> {e.g. "Run the Verification command from .ultraplan/plan.md and report output."}
```

---

## Rules

- **Write absolute paths, never relative.** The next session may not be opened in the same working directory.
- **Be dense but complete.** Aim for scannable bullets, not prose paragraphs. The next Claude should be oriented in under 60 seconds of reading.
- **Capture rationale, not just decisions.** "We picked X" is useless without "because Y". The next session will re-open resolved questions otherwise.
- **Anti-patterns are first-class.** Anything Dean or Claude tried and ruled out must be captured, or the next session will propose the same rejected idea and waste a cycle.
- **Do not duplicate standing memory.** Dean's auto-memory (`MEMORY.md`) already loads in every session. Don't restate his role, brand standards, or baseline preferences — only session-specific things go here.
- **Graceful degradation** — if the project has no git, no plan file, and no todos, still produce a useful handover from conversation content alone. Just mark those sections "_None._"
- **Don't include sensitive content.** If the session touched secrets, credentials, private contracts, or anything Dean flagged as confidential, write "_Redacted — refer to Dean for context_" rather than the content itself.

---

## Edge Cases

- **No `.claude/` dir in project**: create it. Create `.claude/handovers/` too.
- **Project is not a git repo**: skip git commands, mark branch/diff sections as "Not a git project".
- **TodoWrite list is empty**: write "_None._" under Open todos. Extract pending work from the conversation and `.ultraplan/plan.md` instead.
- **Very long session**: rely on `.ultraplan/plan.md`, memory files, and recently-modified file timestamps as ground truth over conversational recall — the earliest parts of the conversation may have summarised out of context.
- **Multiple artefacts in flight**: if Dean was juggling two unrelated things, write two Session Goal paragraphs and split What's Left by artefact. Don't merge them.

---

## One Worked Example

Input: Dean has been in a 90-minute session building the session-handover skill itself. He says `/session-handover`.

Expected output file (`/Users/deanlatham/git-practice/.claude/HANDOFF.md`):

```markdown
# Session Handover — Session-Handover Skill Build
_Generated: 2026-04-17 14:45 · Project: git-practice · Branch: main_

## Resume Prompt
Paste into a new Claude chat to resume:
> Review `/Users/deanlatham/git-practice/.claude/HANDOFF.md` before we continue.

## Session Goal
Build a `session-handover` skill at `~/.claude/skills/session-handover/` that writes a markdown brief the next Claude chat can read to resume work without context loss. Dean approved the ultraplan in `.ultraplan/plan.md`; implementation is underway.

## Current State
- **Branch:** main
- **Uncommitted changes:** `.ultraplan/plan.md`, `~/.claude/skills/session-handover/SKILL.md` (outside repo)
- **Active plan file:** `/Users/deanlatham/git-practice/.ultraplan/plan.md`
- **Open todos:** _None._

## What's Been Done
- **Plan written and approved** — `.ultraplan/plan.md` — skill scope, structure, verification
- **SKILL.md drafted** at `/Users/deanlatham/.claude/skills/session-handover/SKILL.md` — frontmatter, pipeline, output template, edge cases, worked example

## What's Left
- Test the skill end-to-end by running `/session-handover` in a fresh session
- Verify the generated `HANDOFF.md` is sufficient for a cold chat to resume (Phase 5 verification in the plan)
- **Open questions for Dean:** whether to build companion `/session-resume` skill (deferred per plan)

## Critical Context for the Next Session

### Files to read first
1. `/Users/deanlatham/.claude/skills/session-handover/SKILL.md` — the skill itself
2. `/Users/deanlatham/git-practice/.ultraplan/plan.md` — approved plan
3. `/Users/deanlatham/git-practice/.claude/HANDOFF.md` — this file

### Anti-patterns — already tried or ruled out
- Naming it `handoff-document` — renamed to `session-handover` because the receiver is another LLM, not a human
- HTML or PDF output — rejected in favour of markdown for fastest LLM parsing and Git/Obsidian compatibility
- Context-rich paste line — rejected in favour of a tight fixed line; the HANDOFF file handles orientation

### Session-specific preferences
- _None beyond standing memory._

### Domain context relevant to the task
- Skill convention: `~/.claude/skills/[name]/SKILL.md` with YAML frontmatter + markdown body; optional `references/` subdir
- Output lands in `{project}/.claude/HANDOFF.md`, archive at `{project}/.claude/handovers/`

## Next Immediate Step
> Run the verification described in `.ultraplan/plan.md` — confirm `.claude/HANDOFF.md` was produced correctly and that a fresh chat reading only the resume prompt can orient itself.
```
