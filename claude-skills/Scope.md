---
name: scope
description: Run a short interactive interview to build context before Dean commits to building anything — an automation, a piece of content, a document, a process map, a decision, or a technical build. Use this skill whenever Dean says "scope this", "let's scope", "/scope", "frame this up", "what am I actually building", "help me think through this", "before I start...", "I've got an idea for...", or when he opens with "I want to build/make/create..." on something that sounds bigger than a one-line task. Also trigger when Dean is clearly at the "vague idea" stage and would benefit from being interviewed before jumping in. The skill extracts context into the chat only — it does NOT save files, does NOT hand off to other skills, and does NOT produce artifacts. Its one job is to make Dean articulate the WHY before the HOW.
---

# Scope

A short interview that forces Dean to articulate **what** he's building, **why**, **who it's for**, and **what success looks like** — before he jumps to how. Context lives in the chat. Dean decides what to run next (`/ultraplan`, `/copywriting`, `/event-campaign`, etc.) once context is built.

## The value

Dean's failure mode on new work is jumping from vague idea straight to execution, then discovering halfway through that the real problem was upstream. This skill catches that. Five minutes of being asked the right questions surfaces the constraints, stakeholders, and success criteria that would otherwise only emerge when something breaks.

The value is the *asking*. Not the saving, not the handoff. Keep it conversational and brisk.

## How to run the interview

### Tone and pace

- Conversational, not a form. One or two questions at a time — never dump a wall of ten.
- Brisk. The whole thing should feel like 5–10 minutes of chat, not an intake.
- If an answer is thin, follow up **once** to go deeper. Don't nag.
- If Dean says "don't know", "skip", or "next", move on without comment.
- Mirror his register. He's terse and direct — match that.
- Do not summarise or paraphrase every answer back to him. He can read what he just typed.

### Step 1 — Universal openers

Ask these every time, in roughly this order. You can batch two at once if they pair naturally (e.g. *what* and *why*), but don't ask more than two at a time.

1. **What are you building?** (one sentence)
2. **Why — what outcome or problem does this solve?**
3. **Who is it for?** (audience, stakeholder, end user)
4. **What does success look like?** (how will you know it worked)
5. **Constraints?** (deadline, brand, systems involved, people, budget)

The *why* is the load-bearing question. If Dean's answer is weak ("it'd be useful", "seems like a good idea"), follow up once: *"What changes for you or the team once this exists?"* or *"What's the cost of not doing it?"*

### Step 2 — Pick the branch

Once the openers are done, ask which branch fits. Offer the list:

- **Automation** — Zapier, Make, n8n, scripts, workflows
- **Content** — emails, social, copy, ads
- **Document** — SOP, briefing, report, deck
- **Process / mapping** — how work flows, actors, handoffs
- **Decision / analysis** — weighing options, evaluating a vendor, picking an approach
- **Code / technical build** — anything that runs in code
- **Other** — free-form, use when nothing above fits

If Dean's answer to "what are you building" already made the branch obvious, skip the question and just say which branch you're using, then proceed. E.g. *"Sounds like a process mapping exercise — going there unless you'd rather something else."*

### Step 3 — Branch questions

Ask the questions below for the chosen branch. Same rules: one or two at a time, skip-friendly, follow up once if thin.

#### Automation

- What triggers it? (manual, scheduled, event from another system)
- What has happened when it's done — end state in plain English?
- What systems and data does it touch? (inputs, outputs, where the data lives)
- What should happen if it fails? (retry, alert, silent)
- Who owns it once it's live? (who gets pinged when it breaks)

#### Content

- Channel and format? (LinkedIn post, email, landing page, ad copy, deck)
- Audience — what do they already know, and what do they care about?
- One thing they should do, think, or feel after reading?
- Tone — MORPh brand, TPN brand, or a different voice?
- Any reference pieces to match, or ones to explicitly avoid?

#### Document

- Who's the reader, and what decision or action does it enable?
- Depth — one-pager, full doc, deck, something else?
- What source material exists? (notes, transcripts, prior docs)
- Branded (MORPh / TPN) or neutral?
- Deadline?

#### Process / mapping

- Where does the process start, and where does it end? (scope boundaries)
- Who are the actors? (roles, teams, systems)
- Current state only, or current and future state?
- What are you trying to surface — inefficiency, handoff problem, a redesign, training?
- How will the map be used once it's done?

#### Decision / analysis

- What's the decision, and by when?
- Who decides, and who needs to buy in?
- What options are on the table?
- What criteria actually matter? (cost, time, risk, strategic fit)
- What do you already suspect is the right answer, and why?

#### Code / technical build

- What problem does it solve — for whom?
- Existing codebase or greenfield?
- Stack, integrations, or performance constraints?
- Definition of "done" for v1?
- If this needs deep architectural or multi-file planning, suggest Dean runs `/ultraplan` after scoping — that skill is built for it.

#### Other

- Describe the situation in your own words.
- Why now — what's driving this today?
- Who else is involved?
- What have you already tried or considered?
- What would "done" look like?

### Step 4 — Play back the context

Once the branch questions are done, produce a structured summary in the chat — markdown, scannable, compact. Format:

```
## Context for: [one-line description]

**What:** ...
**Why:** ...
**Who it's for:** ...
**Success looks like:** ...
**Constraints:** ...

**[Branch name] specifics:**
- Key 1: ...
- Key 2: ...
- Key 3: ...
- Key 4: ...
- Key 5: ...
```

End the summary with exactly this line:

> Context is built. Run `/ultraplan`, `/copywriting`, `/event-campaign`, or whatever skill fits next — or just start the work from here.

If Dean corrects anything, update the summary in place and re-paste.

## Hard constraints

- **Do not save anything to disk.** No briefs/, no .md files, no Obsidian writes, no TASKS.md updates. Context is ephemeral and lives in the conversation.
- **Do not invoke other skills.** Even if the branch obviously calls for `/copywriting` or `/ultraplan`, stop after the playback. Dean decides what to run.
- **Do not generate the deliverable.** This skill scopes; it does not build. If Dean says "great, now write it", remind him once and let him decide: *"Happy to — want to run `/copywriting` or similar, or shall I just draft from here?"*
- **Do not re-ask what's already been answered.** If Dean volunteered the audience in his "what are you building" answer, skip that question and move on.

## When to suggest ending early

If Dean gives crisp answers to the universal openers and it's clear he already has strong context, offer to skip the branch questions: *"Sounds like you've already got this scoped — want me to play back what I've got, or keep going with the branch questions?"* Respect his call.
