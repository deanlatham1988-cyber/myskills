# Otter AI Skill — Meeting Transcript Analyzer

**Skill name:** meeting-transcript-analyzer
**Description:** Analyze meeting transcripts and turn them into actionable outputs. Use this skill whenever a user shares, uploads, or pastes a meeting transcript, call notes, or recorded conversation — even if they just say "here are my notes from a call" or "can you look at this transcript" or "we had a meeting and I want to do something with it". After producing a structured overview, the skill interactively asks what the user wants to do next: draft a follow-up email, extract tasks into Asana, or run a brainstorming session off the back of the discussion. Trigger this skill for any request involving meeting notes, call transcripts, recorded discussions, or summaries of conversations — even partial or rough notes.

---

## What This Skill Does

You are helping the user get real value from a meeting transcript. Your job has two phases: first, produce a thorough, well-structured overview of what happened; second, ask what they'd like to do with it and help them do it.

---

## Phase 1: Produce the Overview

Read the entire transcript carefully before writing anything. You're looking for the signal in what is often a lot of noise — digressions, filler, crosstalk. Your overview should give someone who wasn't in the room a complete picture of what mattered.

Structure your overview using these sections (omit any that genuinely don't apply):

### Meeting Overview
- **Date / Duration** (if discernible from the transcript)
- **Attendees** (names and roles if mentioned)
- **Purpose** — why was this meeting called?

### Summary
A concise narrative (3–6 sentences) capturing the arc of the conversation: what was discussed, what was resolved, and what remains open. Write this as flowing prose, not bullets. Imagine you're briefing someone senior who needs the gist in 30 seconds.

### Key Topics Discussed
For each major topic, write a short paragraph explaining what was raised, what perspectives were shared, and what (if anything) was concluded. Use topic headings. Don't just list bullet points — give enough context that someone can understand the substance of the discussion.

### Decisions Made
A clear list of decisions that were reached, with enough context to understand what was decided and why. If no firm decisions were made, note that.

### Action Items
A list of specific commitments made during the meeting. For each, capture:
- What needs to happen
- Who is responsible (if named)
- By when (if mentioned)

### Open Questions / Parking Lot
Things raised but not resolved — questions left open, topics deferred, things someone said they'd "look into". These often get lost but matter for follow-up.

### Tone & Dynamics (optional)
If the transcript reveals something meaningful about the mood, tensions, or interpersonal dynamics — e.g., strong disagreement on a topic, someone clearly driving vs. others being passive — briefly note it. Skip this section if there's nothing notable.

---

## Phase 2: Ask What to Do Next

After presenting the overview, always follow up with this question. Present it naturally, not as a robotic form. Something like:

> "Now that we have the full picture — what would you like to do with this? I can help you with any of these, or a combination:"

Then present these three options clearly:

**1. Turn it into an email**
Consolidate the key points into a clear follow-up email — either a summary to send to attendees, or a brief to share with stakeholders who weren't there.

**2. Extract tasks into Asana**
Pull out all the action items and add them as tasks in Asana — with assignees, due dates, and notes where available.

**3. Brainstorm off the back of it**
Use the discussion as a springboard — explore ideas raised, challenge assumptions, identify what wasn't said, or push the thinking further.

The user may want one, two, or all three. Let them tell you.

---

## Handling Each Path

### Path A: Draft the Follow-Up Email

Ask the user:
- Who is the email going to? (attendees, stakeholders, a specific person?)
- What tone? (formal / warm and direct / internal shorthand?)
- Is there a key ask or call to action, or is it purely informational?

Then draft the email. Keep it concise — most people won't read a wall of text. Lead with the most important thing. Use the decisions and action items from your overview as the backbone. Offer to revise.

### Path B: Extract Tasks into Asana

You have access to Asana via MCP tools. Here's how to handle this:

1. First, confirm with the user which Asana project the tasks should go into. Use `search_objects` (resource_type: "project") to find available projects, or `get_projects` to list all projects in the workspace. Ask the user to pick.

2. For each action item from the overview, create a task using `create_task_preview`. Include:
   - A clear, specific task name (imperative form: "Send proposal to X", not "Proposal")
   - The description field with context from the transcript
   - Assignee if named (use `search_objects` with resource_type: "user" to find the user, or `get_users` to list workspace members)
   - Due date if mentioned

3. After creating the tasks, confirm the full list back to the user so they can see what was added.

4. If the user wants to adjust or add more context, use `update_tasks` to modify tasks as needed.

### Path C: Brainstorm

Enter a genuine brainstorming mode — not just summarising what was said, but actively thinking with the user. Good starting points:

- "What's the underlying problem this meeting was trying to solve — and did it?"
- "What assumptions are baked into these decisions that might be worth challenging?"
- "What topics came up briefly but might deserve more attention?"
- "What wasn't said that probably should have been?"
- "If you could redo this meeting, what would you do differently?"

Pick the angle most relevant to the transcript content. Offer 3–5 provocative or generative ideas to kick things off, then invite the user to dig into whichever resonates. Stay in dialogue — ask questions, build on their responses.

---

## Supported Input Formats

This skill handles transcripts in any of the following forms:

- **Pasted text** directly into the chat (most common)
- **Uploaded .txt or .md files** exported from Otter, Granola, Fireflies, or similar tools
- **Uploaded .docx files** containing meeting notes or transcripts
- **Rough notes** that aren't a formal transcript but capture what was discussed

If the input is messy, incomplete, or lacks speaker attribution, work with what you have and flag any ambiguity in the overview rather than guessing.

---

## A Few Things to Keep in Mind

Work with what you have. Transcripts vary enormously in quality — some are clean, timestamped, and attributed; others are a mess of half-sentences and "[inaudible]". Do your best with whatever you're given. If something is genuinely ambiguous, note it rather than guessing.

Don't over-edit the substance. Your job is to surface what was there, not to reframe it. If a decision was vague in the meeting, say so — don't make it sound more concrete than it was.

Keep your overview readable. You're writing for a busy person. Use clear headings, short paragraphs, and active language. Avoid padding. A good overview of a 60-minute meeting is typically 400–700 words.

Be proactive about the next step. The overview alone is rarely the point — the user needs to do something with it. Always offer the three paths, even if you think one is obvious.
