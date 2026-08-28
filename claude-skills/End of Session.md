---
name: end-of-session
description: Close-out learning loop for Dean's sessions — the skill that heals the other skills. Before a chat ends, scan the whole session for corrections Dean made, preferences he said out loud, patterns that kept breaking, infrastructure that changed (new skills, new Zoho WorkDrive folders, changed IDs or paths), and any failed tool/API attempts — then feed each finding back into its canonical home (skill files, auto-memory, Zoho references, or the correction ledger) so future chats start already knowing. Applies the twice rule — a correction said once is ledgered, only a repeat earns a skill-file edit — and shows every exact line change for one approval before anything is written. Use when Dean says "/end-of-session", "end of session", "end of chat", "close out this session", "close this chat down", "wrap up this session", "what did we learn this session", "update the skills before we finish", or any phrasing that means "harvest this session's learnings before I close it". Distinct from /session-handover (continuity brief for the next chat about THIS work) and /end-of-day (laptop shutdown) — this skill updates the standing system, not the in-flight work. Can be chained with either.
metadata:
  version: 1.0.0
---

# End of Session

You are running Dean's **session close-out learning loop**. The premise: Dean is not one-shot prompting. He defines, corrects, and decides his way through every session, and all of that gets left behind the second the chat closes — unless this skill harvests it. Skills and memory are living documents; this is the mechanism that keeps them alive without Dean opening the files himself.

Two failure modes this skill exists to kill:

1. **Lost corrections** — Dean corrects something, explains something twice, or states a preference out loud, and it never makes it into a skill file or memory. The next chat makes the same mistake.
2. **Silent infrastructure drift** — a new skill gets created, a new WorkDrive folder appears, a Zoho API call fails in a new way, an ID or path changes — and nothing central records it. Future chats retry known-dead approaches or can't find things that moved.

## Hard rules

- **Diffs first, always.** No file is written or edited until Dean has seen the exact lines that will change (old → new) and said yes. One approval covers the whole batch. This applies to every target including the ledger.
- **The twice rule.** One correction in a session is a *note*, not an edit. It goes to the correction ledger. It only earns a skill-file or memory edit once it has been said **twice** — either twice in this session, or once now plus a matching ledger entry from a previous session. Otherwise you're rebuilding the system around a bad day.
  - Exceptions that skip straight to an edit (facts, not preferences): infrastructure changes (new folder, changed ID, new skill), failed-attempt findings with a confirmed cause, and anything Dean explicitly says to record now.
- **Surgical edits only.** Change the minimum lines that encode the learning. Never restructure a skill file, never rewrite sections wholesale, never "improve while you're in there".
- **Literal capture.** Record what Dean actually said and what actually happened. Don't infer scope, reasoning, or implications beyond the evidence in the session.
- **One home per fact.** Before writing anywhere, check whether an existing file already covers it — update that file rather than creating a duplicate. Zoho facts go to their canonical homes (below), not to new files.

## Pipeline

### 1. Scan the entire session

Walk back through the whole conversation and collect candidates in four buckets:

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

If a bucket is empty, say so in one line and move on. An honest "nothing to harvest" run is a valid run — do not manufacture findings.

### 2. Check the ledger

Read `~/.claude/skills/end-of-session/ledger.md` (create it from the template below if missing).

- For each bucket-A/B candidate, check whether a matching entry already exists. A match = the same correction/preference in substance, not necessarily the same words.
- **Match found** → the twice rule is satisfied: promote it to a real edit this run, and mark the ledger entry as promoted (date + where it landed).
- **No match** → it's a first sighting: draft a new ledger entry, no skill edit yet.

### 3. Route each finding to its home

| Finding | Home |
|---|---|
| Correction/preference tied to ONE skill's behaviour (twice-confirmed) | That skill's `SKILL.md` — surgical edit |
| Correction/preference that applies across sessions generally (twice-confirmed) | Auto-memory: `feedback_*.md` + `MEMORY.md` index line |
| Fact about Dean, his team, or his tools | Auto-memory: `user_*.md` / `reference_*.md` |
| New skill created this session | Ledger note only — the skill file is its own record; add a memory entry only if there's a non-obvious gotcha |
| Zoho API failure, fix, or quirk | `~/.claude/skills/use-zoho-mcp/SKILL.md` (error decoder / relevant section) and/or the matching `reference_zoho_*.md` memory — whichever is the canonical home for that fact |
| New WorkDrive folder / Zoho ID | `use-zoho-mcp` SKILL.md identifiers section, or the relevant `reference_zoho_*.md` |
| Non-Zoho tool failure or environment quirk | Auto-memory: `reference_*.md` or `project_*.md` |
| First-sighting correction (said once) | Ledger only |

Auto-memory lives at `~/.claude/projects/-Users-deanlatham-git-practice/memory/`. Follow its frontmatter format and add the one-line `MEMORY.md` index entry for any new file.

### 4. Show your work

Present the whole batch in one message, grouped by target file. For each change show:

- **File** — absolute path
- **Why** — one line: the session evidence that earned it (quote Dean's words where short)
- **The exact edit** — old line(s) → new line(s), or the full text of a new ledger/memory entry

Then ask for one go-ahead (use a pop-up: Apply all / Apply some / Skip). "Apply some" walks the items one by one. Nothing is written before the yes.

### 5. Apply and report

Apply the approved edits. Report one line per file written. If a promoted ledger entry landed, mark it `promoted → <file>` with today's date rather than deleting it (history matters for clean-house).

### 6. Offer the chain

End by offering, as a pop-up, whichever apply:
- `/session-handover` — if the session's *work* is unfinished and a next chat will pick it up.
- `/end-of-day` — if Dean is finishing for the day.
- Done — close out.

## Clean house (on request only)

Not part of the normal run. When Dean says "clean house" (here or standalone), sweep for staleness:

- Ledger entries older than ~60 days never repeated → propose deletion.
- Promoted ledger entries older than ~30 days → propose deletion (their learning lives in the target file now).
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

- Not `/session-handover` — that captures the in-flight *work* so the next chat can resume it. This captures *learnings* into the standing system. A session can need both.
- Not `/lint-vault` — the vault is out of scope here.
- Not autonomous — even though this loop could run agent-driven, Dean has chosen diffs-first on every run. Never auto-apply.
