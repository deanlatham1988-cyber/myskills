---
name: end-of-session
description: Close-out learning loop AND the MORPh capture verb — one skill that saves everything to the correct place before a chat ends. Scans the whole session for corrections Dean made, preferences he said out loud, patterns that kept breaking, infrastructure that changed (new skills, new Zoho WorkDrive folders, changed IDs or paths), and any failed tool/API attempts — then feeds each finding back into its canonical home (skill files, auto-memory, Zoho references, or the correction ledger). It also files the session's substance into the MORPh brain — builds, decisions, tools, rules and notes routed into `1 MORPh/` with seat slices to the bench brains, a session overview to Rupert's brain, and log lines — absorbing what `/save-to-brain` used to do (merged 1 Sep 2026). Applies the twice rule — a correction said once is ledgered, only a repeat earns a skill-file edit — and shows every exact line change for one approval before anything is written. Use when Dean says "/end-of-session", "end of session", "end of chat", "close out this session", "wrap up this session", "what did we learn this session", "update the skills before we finish", "close this chat down", or any phrasing that means "harvest this session before I close it" — and also the capture phrasings "save to brain", "save this to the brain", "add this to the brain", "brain this", "log this", "record this", "capture this for morph", "write this up", "document this" (mid-session captures run the filing step only, not the whole loop). Distinct from /session-handover (continuity brief for the next chat about THIS work) and /end-of-day (laptop shutdown). Can be chained with either.
metadata:
  version: 2.0.0
---

# End of Session

You are running Dean's **session close-out loop** — the one skill that, when a chat is about to close, saves everything to the correct place. It does two jobs in one pass:

1. **Learnings** — corrections, preferences, broken patterns, infrastructure drift and failed attempts, fed back into skill files, auto-memory, Zoho references and the correction ledger. The skill that heals the other skills.
2. **Substance** — the builds, decisions, tools, rules and notes the session produced, filed into the MORPh brain (`1 MORPh/`) with seat slices, Rupert's overview and log lines. (This was `/save-to-brain` until the two merged on 1 September 2026.)

**Proactive use:** also offer the filing (Steps 4–6) unprompted at the end of any meaningful MORPh build, any strategic decision, any new tool or skill entering use, or any new voice/brand rule — offer, never auto-write.

**Mid-session capture:** when Dean says "brain this" / "log this" / "save to brain" mid-session, or another skill (`/granola`, `/finish-project`, `/rupert`, `/build-into-project`, …) hands off here, run **Steps 4–6 only** (file, show Dean the exact markdown, apply and log) — not the scan, not the ledger, not the whole close-out loop. Diffs-first still applies: nothing is written before Dean's yes.

Two failure modes this skill exists to kill:

1. **Lost corrections** — Dean corrects something, explains something twice, or states a preference out loud, and it never makes it into a skill file or memory. The next chat makes the same mistake.
2. **Silent infrastructure drift** — a new skill gets created, a new WorkDrive folder appears, a Zoho API call fails in a new way, an ID or path changes — and nothing central records it. Future chats retry known-dead approaches or can't find things that moved.

## Hard rules

- **Diffs first, always.** No file is written or edited until Dean has seen the exact lines that will change (old → new) and said yes. One approval covers the whole batch. This applies to every target including the ledger.
- **The twice rule.** One correction in a session is a *note*, not an edit. It goes to the correction ledger. It only earns a skill-file or memory edit once it has been said **twice** — either twice in this session, or once now plus a matching ledger entry from a previous session. Otherwise you're rebuilding the system around a bad day.
  - Exceptions that skip straight to an edit (facts, not preferences): infrastructure changes (new folder, changed ID, new skill), failed-attempt findings with a confirmed cause, bench findings (a seat's trap or standing fact is evidence, not a mood), and anything Dean explicitly says to record now.
  - The twice rule applies to learnings only. Session **substance** (Step 4) files on the first sighting — a build happened once and still goes in the brain.
- **Surgical edits only.** Change the minimum lines that encode the learning. Never restructure a skill file, never rewrite sections wholesale, never "improve while you're in there".
- **Literal capture.** Record what Dean actually said and what actually happened. Don't infer dates, named parties, reasoning, alternatives, implications, scope, or cross-references beyond the evidence in the session. Show the literal draft first and ask explicitly before adding any inferred field. In brain captures, leave template fields (Why / Alternatives / Implications / Status) blank with `*(not given — ask Dean)*` rather than inventing them. Style-match is for *formatting*; content stays literal until Dean expands it. (Reference: memory file `feedback_literal_capture_only.md`.)
- **One home per fact.** Before writing anywhere, check whether an existing file already covers it — update that file rather than creating a duplicate. Zoho facts go to their canonical homes (below), not to new files.

## Pipeline

### 1. Scan the entire session

Walk back through the whole conversation and collect candidates in six buckets:

**A. Corrections and preferences (about Dean)**
- Did Dean correct something Claude did or wrote?
- Did anything have to be explained twice?
- Did Dean state a preference, rule, or way-of-working out loud that isn't already in a skill file or memory?
- These update how the system *understands Dean* — how he thinks and how he decides.

**B. Broken patterns and formats (about execution)**
- What patterns, formats, or steps kept getting broken or needed re-stating?
- Which skill, when invoked, produced something Dean had to fix — and what was the fix?
- These update how skills *execute*.

**C. Infrastructure drift (facts, not preferences)**
- New skills created or renamed this session.
- New folders, files, or IDs — especially Zoho WorkDrive folders, Zoho Projects IDs, vault paths, tool script locations.
- Changed conventions (a file moved, a canonical home changed).

**D. Failed attempts (especially Zoho)**
- Every tool call or API call that failed this session: what was tried, the exact error, and the outcome — *fixed* (record the fix), *dead end* (record why so no future chat retries it), or *unresolved* (record the state it was left in).
- Zoho failures are the priority case: connection errors, scope errors, wrong base URLs, parameter-shape mistakes. These are exactly the things that keep getting re-learned chat after chat.

**E. Bench findings (per-seat and Rupert-level)**
- Did a bench specialist report a correction, trap, quirk, or standing fact this session?
- Whose patch does it belong to? A finding only one seat needs goes to that seat's brain, not to a skill file the other nine will never read.
- Did anything change about **running the bench** — delegation, permission tiers, which seat owns what, a subagent limitation? That's Rupert's own brain.
- Detection only here — the filing itself happens in Step 4.

**F. Session substance (what the session actually produced)**
- Builds finished, decisions made, tools/skills entering use, voice/brand rules, process changes, notes worth keeping.
- Anything a future chat would want to *know*, as opposed to anything that changes how the system *behaves* (buckets A–E).
- Filed in Step 4.

If a bucket is empty, say so in one line and move on. An honest "nothing to harvest" run is a valid run — do not manufacture findings.

### 2. Check the ledger

Read `~/.claude/skills/end-of-session/ledger.md` (create it from the template below if missing).

- For each bucket-A/B candidate, check whether a matching entry already exists. A match = the same correction/preference in substance, not necessarily the same words.
- **Match found** → the twice rule is satisfied: promote it to a real edit this run, and mark the ledger entry as promoted (date + where it landed).
- **No match** → it's a first sighting: draft a new ledger entry, no skill edit yet.

### 3. Route each learning to its home

| Finding | Home |
|---|---|
| Correction/preference tied to ONE skill's behaviour (twice-confirmed) | That skill's `SKILL.md` — surgical edit |
| Correction/preference that applies across sessions generally (twice-confirmed) | Auto-memory: `feedback_*.md` + `MEMORY.md` index line |
| Fact about Dean, his team, or his tools | Auto-memory: `user_*.md` / `reference_*.md` |
| New skill created this session | Ledger note only — the skill file is its own record; add a memory entry only if there's a non-obvious gotcha |
| Zoho API failure, fix, or quirk | `~/.claude/skills/use-zoho-mcp/SKILL.md` (error decoder / relevant section) and/or the matching `reference_zoho_*.md` memory — whichever is the canonical home for that fact |
| New WorkDrive folder / Zoho ID | `use-zoho-mcp` SKILL.md identifiers section, or the relevant `reference_zoho_*.md` |
| Non-Zoho tool failure or environment quirk | Auto-memory: `reference_*.md` or `project_*.md` |
| Bench findings and session substance | Step 4 below |
| First-sighting correction (said once) | Ledger only |

Auto-memory lives at `~/.claude/projects/-Users-deanlatham-git-practice/memory/`. Follow its frontmatter format and add the one-line `MEMORY.md` index entry for any new file.

### 4. File the session's substance into the brain

This is the filing step — the whole of what `/save-to-brain` used to do. Mid-session captures and hand-offs from other skills run Steps 4–6 only (this step, then show, then apply and log).

**Not filed here:** raw ideas → `/save-to-ideas` · tasks/to-dos → **Zoho** (never task tickboxes in `1 MORPh/`) · a finished tracked project → `/finish-project` · non-MORPh (Academia / Personal) → `/update-to-obsidian`.

**4a. Read the MORPh file map.** `ls "/Users/deanlatham/Obsidian Vault/1 MORPh/"` and refresh from `1 MORPh/README.md`. Don't write to a file you haven't read.

**4b. Classify against the MORPh routing table.**

| Update type | Target file | Notes |
|---|---|---|
| **New built artefact** (deliverable, output) | `Context/Things-Weve-Built.md` | Append to relevant section. *(Transitional: absorbed into the Memory Centre when P3 of the brain redesign lands.)* |
| **New recurring artefact type** | `Context/Things-We-Create.md` | why we create it / what it looks like / process / skill / worked example |
| **New tool / generator / skill / MCP in use** | `Context/Tools-We-Use.md` (broad) AND `Toolkit/My-Tools.md` — the single list of every MORPh tool | Append a three-column row (command / what it does / when to invoke it) to the right themed section. Never write to `Marketing-Tools.md` or `Operations-Tools.md`; they've been pointer stubs since 29 July 2026. Not yet in regular use → `Toolkit/Researching-Tools.md` |
| **Strategic decision made** (in effect) | `Context/Decisions.md` → Active | what was decided / why / alternatives / status — only as Dean stated them |
| **Pending decision** (open question) | `Context/Decisions.md` → Pending | the question / options / what it's blocked on |
| **Decision reversed / replaced** | `Context/Decisions.md` → Superseded | what replaced it and why |
| **Change in role / hierarchy** | `Context/About-Me.md` | edit relevant section |
| **Change in business structure** (MORPh / TPN / group) | `Context/The-Business.md` | edit relevant section |
| **New voice / writing rule** | `Context/Voice-and-Style.md` | append rule with rationale |
| **New formatting / brand standard** | `Context/Document-Standards.md` | append to relevant section |
| **Process / convention change** | `Context/How-We-Work.md` | edit or append |
| **New event-recap voice rule** | `Context/Social-Philosophy.md` | append |
| **New slash command / skill installed** | `Toolkit/My-Tools.md` (picker) AND `Toolkit/Skill Details.md` (for cross-cutting skills) | follow the picker convention (below) |
| **Learning only ONE bench seat needs** | `Executive Bench/<Name>/Brain.md` | Dated, newest first, literal capture. Never candidate or employee personal data. |
| **Learning about running the bench itself** | `Executive Bench/Rupert/Brain.md` | Rupert's own seat brain, distinct from the shared brain which is all of `1 MORPh/`. |

If you genuinely can't classify it, ask Dean rather than guessing.

**4c. Fan out: seats, then Rupert, then the shared brain.** Run all three in order. These are stages, not alternatives — nothing is skipped because it landed somewhere else.

*Stage 1 — the seats.* Walk the whole capture and ask whose patch each part belongs to:

| Patch | Seat |
|---|---|
| Money, invoicing, cash, financial docs | David |
| Brand, campaigns, content, CRM marketing | Andrew |
| People, HR policy, contracts, org design | Hazel |
| Data, counts, quality, datasets | Steven |
| Events, registrations, sponsors | Deborah |
| Projects, boards, phases, plans | Connor |
| Sales, pipeline, deals, leads | Peter |
| Hiring delivery, vacancies, candidates, Recruit | Nadia |
| Diary, bookings, availability | Elaine |

For each seat touched, write the slice **that seat alone needs** — a trap, a quirk, a correction, a standing fact they would otherwise re-learn every activation — to `Executive Bench/<Name>/Brain.md`. Dated, newest first, literal capture. Never any candidate or employee personal data. If a seat was involved but learned nothing durable, say so in one line and skip it.

*Stage 2 — Rupert.* Write a **full overview** to `Executive Bench/Rupert/Brain.md` under `## Session overviews`: what was done, what was decided, which seats were involved and what each took away. This is the only place holding the whole picture. A short paragraph or a few bullets — an index, not a transcript.

*Stage 3 — the shared brain.* File the build, decision, tool or rule into its normal `1 MORPh/` home using the routing table above.

One finding can legitimately appear three times: as a seat slice, as a line in Rupert's overview, and as a `Context/` entry. That is the design, not duplication.

**4d. Read the target file, then draft.** Read the target file (or the relevant section) to match tone, find the insertion point, and avoid duplicating an entry already there. Draft in the file's existing style: UK English, no em dashes, factual and concise, no padding, file paths in backticks, leading with what/where and following with why/how only as Dean gave it. Tools files: the plain-English column is mandatory. Decisions: Why + Alternatives only as Dean gave them.

**Picker file convention:** when adding a skill/tool entry to a picker in `Toolkit/`, follow the picker template (Vault CLAUDE.md Global Rule 11): no duplicate H1, Quick-reference row added, emoji-prefixed `##` tables, one home per skill (cross-reference elsewhere, don't duplicate), keep stub sections, update the Cross-references block and the "Last revised" footer.

### 5. Show your work

Present the whole batch in one message, grouped by target file — learnings and brain captures together. For each change show:

- **File** — absolute path
- **Why** — one line: the session evidence that earned it (quote Dean's words where short)
- **The exact edit** — old line(s) → new line(s), or the full text of a new ledger/memory/brain entry

Then ask for one go-ahead (use a pop-up: Apply all / Apply some / Skip). "Apply some" walks the items one by one, and per item Dean can also say `edit` or `different file` (reroute). Nothing is written before the yes.

### 6. Apply, log, and report

Apply the approved edits with `Edit` (append/edit) or `Write` (new file), matching surrounding formatting. Do not scan `1 MORPh/In-Flight/` for tickboxes — that pre-step is retired; tasks live in Zoho. Then append **one line per `1 MORPh/` file touched** to `~/Obsidian Vault/log.md`:

```
- YYYY-MM-DD — 1 MORPh/<path> — <one-line summary>
```

Never edit or delete existing log lines. Report one line per file written. If a promoted ledger entry landed, mark it `promoted → <file>` with today's date rather than deleting it (history matters for clean-house).

After filing, check in one line whether the capture implies another MORPh file needs touching (e.g. a build that's also a strategic decision). Offer, don't auto-write.

### 7. Offer the chain

End by offering, as a pop-up, whichever apply:
- `/session-handover` — if the session's *work* is unfinished and a next chat will pick it up.
- `/end-of-day` — if Dean is finishing for the day.
- Done — close out.

## Clean house (on request only)

Not part of the normal run. When Dean says "clean house" (here or standalone), sweep for staleness:

- Ledger entries older than ~60 days never repeated → propose deletion.
- Promoted ledger entries older than ~30 days → propose deletion (their learning lives in the target file now).
- Rupert's `## Session overviews` older than ~90 days → propose collapsing to a one-line summary or deletion. Seat brains and `Context/` hold the durable facts.
- Skill lines and memory files that contradict something learned since, or reference things that no longer exist → propose the fix.

Same rules as always: show exact lines, one approval, surgical only. The vault has its own tool (`/lint-vault`) — don't sweep the vault from here.

## Ledger template

If `~/.claude/skills/end-of-session/ledger.md` doesn't exist, create it as:

```markdown
# Correction ledger

First-sighting corrections and preferences. One entry per item. An entry is promoted to a real skill/memory edit when the same correction is seen a second time (the twice rule).

Format:
- `YYYY-MM-DD` — **<short label>** — what Dean said/corrected (literal), which skill/context it arose in. `[promoted → <file> YYYY-MM-DD]` when it graduates.

## Entries
```

## What this skill is NOT

- Not `/session-handover` — that captures the in-flight *work* so the next chat can resume it. This captures learnings and knowledge into the standing system. A session can need both.
- Not `/save-to-ideas` — raw ideas grow on the Ideas board, not here.
- Not `/finish-project` — a finished tracked project gets its rich Memory Centre record there.
- Not `/lint-vault` — vault-wide health checks are out of scope here.
- Not autonomous — even though this loop could run agent-driven, Dean has chosen diffs-first on every run. Never auto-apply.

**Sister skills:** `/save-to-ideas` (raw ideas) · `/finish-project` (project close-out) · `/search-brain` (read-side retrieval) · `/update-to-obsidian` (whole-vault capture with persona fork) · `/session-handover` (continuity) · `/end-of-day` (shutdown). `/save-to-brain` was merged into this skill on 1 September 2026 and is now a pointer stub.
