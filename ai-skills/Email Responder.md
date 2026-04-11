# Email Responder

**Skill name:** email-responder
**Description:** Process unread Outlook inbox emails, summarise each one, and draft responses in Dean's voice. Use this skill whenever Dean asks to go through his emails, catch up on his inbox, process his mail, draft email replies, respond to emails, or do an email run. Also trigger when Dean says things like "what's in my inbox", "help me reply to my emails", "email catchup", "go through my unread", "batch my email responses", or "draft replies for me". If Dean mentions emails and responses together, use this skill.
**Install file:** email-responder.skill

---

## Purpose

This skill processes Dean's unread Outlook inbox emails in a structured batch workflow. It summarises each email, asks Dean what he wants to say, then drafts a polished response using his personal language style. The goal is to compress email processing time: Dean provides the intent, the skill handles the writing.

---

## Workflow

### Step 1: Fetch unread emails

Pulls unread emails from the Inbox folder via the Outlook email search tool. Default limit is 20 emails per batch.

### Step 2: Read each email's full content

Uses the read_resource tool to get the full body, sender details, and subject line for every unread email.

### Step 3: Filter out noise

Automatically skips emails that don't need a response:

- No-reply senders (noreply, do-not-reply, mailer-daemon, etc.)
- Newsletters and marketing (unsubscribe links, mailchimp, hubspot, sendgrid, etc.)
- Automated notifications (GitHub, Jira, Asana, Azure DevOps, CI/CD) unless they contain a direct question
- Calendar invites and updates without substantive content

When in doubt, the skill includes the email rather than filtering it.

### Step 4: Present the batch overview

Shows a numbered list of actionable emails with sender name, subject line, and a one-sentence summary of the ask. Then asks which ones to respond to.

### Step 5: Process each email for response

For each selected email:

1. Shows a concise summary (who, what, any deadlines, who's CC'd)
2. Asks Dean what he wants to say back
3. Drafts the response using the dean-language-style skill (Minto Pyramid, SCQ, no em dashes, no AI filler, academic-professional register)
4. Presents the draft formatted and ready to paste into Outlook
5. Asks for approval or edits before moving to the next email

### Step 6: Wrap up

Gives a brief summary of how many emails were in the inbox, how many were filtered, how many responded to, and how many skipped.

---

## Error Handling

**Outlook connector unavailable:** If the Outlook email search tool returns an authentication error or is not connected, stop and tell Dean to reconnect the Microsoft 365 connector in his Claude settings before retrying.

**Individual email read failure:** If `read_resource` fails on a specific email (e.g. the email was deleted between fetch and read, or a permissions issue), skip that email, note it in the batch overview as "could not be read", and continue processing the rest.

**Reply vs Reply-All:** Default to Reply unless the original email was sent to a group or distribution list. If multiple people are on the To/CC line who appear to be active participants (not just CC'd for visibility), ask Dean whether he wants Reply or Reply-All before drafting.

**Batch size:** The default is 20 emails. If Dean says "go through all my emails" or similar, ask how many to process. For very large inboxes, suggest working in batches of 20 to keep the conversation manageable.

---

## Dependencies

- Outlook email connector (for outlook_email_search and read_resource)
- The dean-language-style skill (read once per session to load writing rules)
