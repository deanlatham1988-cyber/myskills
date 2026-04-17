# Toolkit Gamma — Document to Gamma Slide Deck Converter

**Skill name:** toolkit-gamma
**Description:** Convert stakeholder training documents (.docx) into Gamma slide decks with exact wording preservation. Use this skill whenever the user wants to turn a training document, toolkit document, script document, or slide content document into a Gamma presentation. Triggers include: 'create a deck from this document', 'turn this into a Gamma', 'build slides from this toolkit', 'make a presentation from this script', 'convert this to Gamma', 'create training slides', or any mention of converting a .docx into a Gamma slide deck. Also use when the user uploads or references a document that contains slide content and voiceover scripts intended for Gamma. If the user mentions 'toolkit' and 'Gamma' together, or 'training deck', this skill applies. Do NOT use for creating presentations from scratch without a source document, or for editing an existing Gamma deck.
**Install file:** toolkit-gamma.skill

---

## Purpose

This skill converts structured stakeholder training documents (.docx files) into Gamma slide decks. These documents are used in the pharmaceutical and healthcare education space, where clinical accuracy and regulatory precision make exact wording non-negotiable.

The single most important principle of this skill: the wording in the source document is the wording that appears in the final deck. Every word has been chosen deliberately, often reviewed by medical, legal, or regulatory stakeholders. Changing even a single word can alter clinical meaning, breach compliance, or misrepresent guidance. This skill exists precisely because that level of fidelity must be guaranteed every time, regardless of who runs it.

---

## How the Source Documents Are Structured

Each document follows a consistent pattern. Understanding this structure is essential for correct parsing.

**Document-level header:** The document opens with a title (e.g. "DRY EYE DISEASE MANAGEMENT IN PRIMARY CARE") and a brief explanation that the document contains two sections per slide: a voiceover script and slide content.

**Per-slide structure:** Each slide is introduced by a bold heading like `SLIDE 1 --- Introduction` or `SLIDE 5 --- Red Flags for Urgent Referral`. Within each slide block, there are two clearly marked sections:

1. **SLIDE CONTENT** (marked with `📽 SLIDE CONTENT --- Gamma AI`): This contains the actual text that belongs on the slide: headlines, bullet points, grouped sections, tip boxes, and warnings. It also contains layout notes in italics, which are design guidance for the person building the deck.

2. **VOICEOVER SCRIPT** (marked with `🎙 VOICEOVER SCRIPT --- ElevenLabs`): This is the spoken narration script. It is conversational in tone and written for text-to-speech. This content becomes presenter notes in the Gamma deck.

**Layout notes** appear in italics within the slide content section. They describe things like "use a three-column layout" or "add a warning icon". These are guidance for Gamma's AI generator and should be passed through as additional instructions, not as slide content themselves.

---

## Step-by-Step Process

### Step 1: Read the Source Document

Use pandoc to extract the .docx content as markdown. Before running pandoc, verify it is installed by running `which pandoc`. If pandoc is not available, fall back to using the docx skill to read the document content directly. Then read the extracted markdown. If the document contains images, note their presence but do not worry about extracting them.

### Step 2: Parse the Document into Slides

Work through the extracted content and separate it into individual slides. For each slide, extract three components:

1. **Slide content**: Everything under the SLIDE CONTENT section that is NOT in italics (layout notes). This includes headlines, bullet points, section headers, tip boxes, warning text, and any other visible slide text.
2. **Layout notes**: The italic text within the slide content section. These describe the intended visual layout and design choices.
3. **Voiceover script**: Everything under the VOICEOVER SCRIPT section. This is the presenter's spoken narration.

### Step 3: Build the Gamma Input Text

Construct a single inputText string that Gamma's API will use to generate the deck.

Presenter notes formatting is critical. Gamma recognises the marker `[speaker notes]` to place content into the presenter notes area of a card. If you use any other format (like `**Presenter Notes:**`), Gamma will render the voiceover text as visible slide content instead. This is the single most common failure mode of this skill.

For each slide, the format is:

```
---
## [Slide Title]
[Exact slide content, verbatim from source]

[speaker notes]
[Exact voiceover script, verbatim from source]
```

Critical rules when building the input text:

- Copy all slide content and voiceover scripts character for character from the source document. Do not paraphrase, summarise, reorder, add, or remove any words.
- Preserve the original formatting markers: bullet points, numbered lists, bold headings, warning symbols, checkmarks, and emoji markers.
- Keep grouped sections intact with their sub-bullets beneath them.
- Do not merge slides or split slides differently from how the source document defines them. Each SLIDE N in the source becomes exactly one card in Gamma.
- Layout notes should NOT appear in the slide content itself. They go via the additionalInstructions parameter.

### Step 4: Compile Layout Instructions

Gather all layout notes from across the document and compile them into a single additionalInstructions string, formatted per-slide.

Global instructions always include:

- Healthcare/pharmaceutical training presentation context. Clinical accuracy is paramount.
- Do NOT alter, rephrase, or summarise any slide text or presenter notes.
- MORPh brand styling throughout. Headings in dark navy (#02084B) or white (#FFFFFF).
- MORPh logo MUST appear on every slide.
- Section divider slides: bold and minimal.
- Warning/red flag slides: red or amber accent colours.
- Speaker notes content placed in presenter notes area, NOT on the visible slide surface.
- No AI-generated images or photographs. Graphics, icons, shapes, and diagrams are fine.

### Step 5: Verify Theme and Call the Gamma API

Before calling Gamma, use the `get_themes` tool to confirm that the MorphTemplate theme (`hedgb3z7uh7o1ft`) still exists. If the theme ID is not found, stop and ask Dean which theme to use instead. Do not fall back to a default theme silently.

Parameters:

| Parameter | Value | Why |
|---|---|---|
| textMode | "preserve" | Guarantees exact wording fidelity |
| themeId | "hedgb3z7uh7o1ft" | MorphTemplate custom theme |
| cardOptions.dimensions | "16x9" | Standard presentation ratio |
| cardOptions.headerFooter | topLeft: themeLogo, size: md | MORPh logo on every slide |
| textOptions.language | "en-gb" | British English |
| textOptions.amount | "detailed" | Full content per slide |
| textOptions.tone | "professional" | Healthcare register |
| imageOptions.source | "noImages" | No AI images, graphics only |
| additionalInstructions | [from Step 4] | Per-slide layout guidance |

Three non-negotiable parameters:

1. `textMode: "preserve"` ensures the input text is used as-is.
2. `themeId: "hedgb3z7uh7o1ft"` (MorphTemplate) must be used on every deck.
3. `cardOptions.headerFooter` with themeLogo places the MORPh logo on every card, including first and last.

### Step 6: Share the Result

Once Gamma returns the gammaUrl, share it with the user. Remind them to review the presenter notes on each slide to confirm the voiceover scripts have been placed correctly.

---

## Handling Variations

**Documents without voiceover scripts:** Proceed normally but omit the speaker notes section from each card.

**Documents with images:** Do not attempt to replace them with AI-generated images. Note their placement in the layout instructions so the user can add the original image manually in the Gamma editor. The imageOptions.source must always be set to "noImages".

**Documents with different section markers:** Look for the pattern rather than exact marker text. The two sections per slide will always be: one for on-slide content and one for spoken narration.

**Very long documents (20+ slides):** Gamma handles large presentations well with textMode: "preserve". No special handling is needed, but suggest the user review the deck card by card to confirm nothing was truncated. For documents exceeding 50 slides, warn Dean that generation may take longer and confirm he wants to proceed as a single deck rather than splitting into parts.

---

## Verification Checklist

After generating the deck, verify:

1. Does the number of cards match the number of slides in the source document?
2. Was textMode: "preserve" used in the API call?
3. Was the MorphTemplate theme (hedgb3z7uh7o1ft) applied?
4. Were all voiceover scripts directed into presenter notes (not onto the visible slide)?
5. Were layout notes excluded from the visible slide content?
6. Was the input text built by copying verbatim from the source?
7. Is imageOptions.source set to "noImages"?
8. Does the MORPh logo appear on every slide?
9. Did Gamma insert any AI-generated images despite `noImages` being set? If so, flag them for Dean to remove manually in the Gamma editor.
