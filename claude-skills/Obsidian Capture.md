# Obsidian Capture

**Skill name:** obsidian-capture
**Description:** Saves information to Dean's Obsidian vault — including creating new notes, adding to existing notes, and updating note content. Use this skill whenever Dean wants to capture anything into Obsidian. Triggers include: "add this to Obsidian", "save this to my vault", "put this in my notes", "store this in Obsidian", "add to my second brain", "file this in Obsidian", "capture this", "update my Obsidian note on X", "add more to my note about X", or any time Dean shares content and wants it in his knowledge base.
**Install file:** obsidian-capture.skill

---

## Purpose

This skill saves information to Dean's Obsidian vault with strict fidelity to what Dean has actually provided — never adding extra context, definitions, or examples he hasn't learned yet. It handles folder selection, note formatting by content type, linking to related existing notes (with Dean's approval), and writing the final file.

---

## Note Types

### Academic / Research (Psychology, Philosophy, Research Methods, Economics, Politics, Ideology)
Follows the vault's established template: italic summary, ## Explanation, ## Key Terms, ## Related Concepts, ## Example in Research, ## Source. Sections only included if Dean has provided the relevant content.

### Verbatim / Technical (AI, Coding)
Content preserved exactly as Dean provides it — no paraphrasing or restructuring. Title and code blocks added only.

### Business (Morph Consultancy)
Structured as: ## Overview, ## Key Points, ## Action Items, ## Related. For attached documents, includes an overview and document reference.

---

## Workflow

### Step 1: Confirm vault access
Checks access to `/Users/deanlatham/Desktop/Obsidian Vault`.

### Step 2: Ask where to save
Shows folder structure and asks: new note in existing folder, add to existing note, or new note in a new subfolder.

### Step 3: Draft the note
Uses only the information Dean has provided. For attached documents, writes an overview based on document content.

### Step 4: Suggest related links
Scans the actual vault for related existing notes and presents up to 5 suggestions. Only adds links Dean approves.

### Step 5: Write the file
Saves the `.md` file to the correct vault path and confirms the location.

---

## Key Rule

**Only add what Dean provides.** Never pad notes with additional facts, history, examples, or related concepts he hasn't explicitly shared. The vault captures Dean's actual learning, not an augmented version of it.

---

## Error Handling

**Vault path not found:** If `/Users/deanlatham/Desktop/Obsidian Vault` does not exist or is not accessible, ask Dean for the current vault path before proceeding. Do not create a new vault directory.

**Content type detection:** If the content Dean provides does not clearly fit Academic/Research, Verbatim/Technical, or Business categories, default to a minimal structure: a title and the content as flowing prose under a single `## Notes` heading. Ask Dean if he wants a different structure rather than guessing.

**Related note matching:** When scanning for related existing notes (Step 4), match on: note titles containing shared keywords, tags that overlap, and notes in the same folder. Present matches with the folder path so Dean can judge relevance. If no matches are found, skip the linking step rather than forcing weak suggestions.

**File name conflicts:** If a note with the same filename already exists at the target path, ask Dean whether to append to the existing note or create a new note with a disambiguated name. Never overwrite silently.

---

## Dependencies

- Access to `/Users/deanlatham/Desktop/Obsidian Vault` (file system)
