---
name: meetings-to-notes
description: >
  Use this skill whenever a user wants to convert a meeting transcript into structured notes,
  push meeting notes to Confluence, process a .vtt transcript file, fill in a meeting notes page,
  or extract decisions and action items from a meeting. Trigger on any mention of: meeting notes,
  transcript, Teams transcript, .vtt file, meeting summary, confluence notes, meeting recap,
  action items from meeting. Also trigger if the user says things like "fill in my notes",
  "help me with the meeting", "process the transcript", or pastes a .vtt file.
compatibility:
  tools:
    - bash_tool
    - confluence_mcp
  dependencies:
    - python3
  mcps:
    - name: Confluence
      purpose: Read meeting page (agenda + prefilled notes), push accepted notes back
      required: true
---

# Meetings-to-Notes Skill

Helps meeting moderators turn a Teams transcript + Confluence agenda into structured, executive-ready notes — with suggestions reviewed before pushing to Confluence.

---

## Principles

- **Short and executive-readable**: Every bullet must be punchy. No filler. If it can't be read in 3 seconds, it's too long.
- **Suggestions, not drafts**: Claude proposes; the moderator decides.
- **Transparent AI**: All AI-contributed content is tagged `[AI Generated]` on Confluence.
- **Learn from feedback**: Corrections are stored and applied in future sessions.

---

## Step 0 — Load Memory

Before doing anything else, check for a `feedback.md` file in the skill folder.

```
/mnt/skills/user/meetings-to-notes/feedback.md
```

If it exists, read it silently and apply all corrections noted there (tone, format, verbosity, field preferences). Do not announce this to the user — just apply it.

---

## Step 1 — Gather Inputs

You need two things minimum. Collect what's missing before proceeding.

| Input | Source | Required |
|---|---|---|
| `.vtt` transcript | User uploads file | ✅ |
| Confluence meeting page | URL (via MCP) — serves as both agenda and notes target | ✅ — ask if not provided |
| Prefilled notes | Already on the same Confluence page (optional) | Ask once, then continue either way |
| Feedback history | `feedback.md` in skill folder | Optional |

**The agenda and the notes page are the same Confluence page.** Claude reads the agenda structure from it and writes the notes back into it.

**If the Confluence page URL is not given: stop and ask.**
> "Please share the Confluence URL for this meeting's page."

Do not proceed until you have it.

**Prefilled notes:** Once you have the page, check if it already contains any prefilled notes or partially filled rows. If yes, surface them during review (Step 4) with "Keep, replace, or merge?" If the page has no prefilled content, continue without asking — it's not required.

---

## Step 2 — Clean the VTT (run script, don't parse in context)

**Never parse the raw VTT yourself.** Always run the cleaning script first. Raw VTTs are 50–60% noise and will waste tokens.

### Run the script

```bash
python .github/skills/meeting-to-notes/scripts/clean_vtt.py path/to/transcript.vtt -o transcript_clean.txt --stats
```

- `-o transcript_clean.txt` writes the cleaned output to a file
- `--stats` prints token savings to stderr (raw vs cleaned estimate)

The script handles all Teams-specific quirks:
- Strips WEBVTT headers, cue IDs, timestamps
- Strips `<v Speaker>...</v>` tags, keeps speaker + text
- Normalises speaker names: "First Last (Company)" → "First Last"
- Merges consecutive lines from the same speaker into one turn
- Deduplicates repeated lines (Teams artefact)
- Labels unknown speakers as `[Unknown]`

### Output format

```
John Smith: We need to review the budget before end of month.
Sarah Lee: Agreed. I can have the numbers ready by Friday.
[Unknown]: Can we move that to Thursday?
```

### After running

- Read `transcript_clean.txt` into context — not the original `.vtt`
- If `--stats` reports unknown speakers > 0, flag to the moderator upfront:
  > "⚠️ X line(s) had no speaker attribution — labelled [Unknown]. You may want to verify these."
- If the script errors (encoding issues, malformed VTT), tell the user and show the error message.

See `references/vtt-cleaning.md` for edge cases and manual fallback if the script cannot run.

---

## Step 3 — Read the Confluence Page

Use the Confluence MCP to fetch the meeting page. From a single page, extract two things:

1. **Agenda structure** → section titles and any sub-items (used to organize suggestions)
2. **Notes table structure** → detect existing columns and any prefilled rows

**Detect the notes format:**
Look at the existing table. Identify:
- Column names (e.g., Time Ref | Topic | Discussion | Decisions | Deadlines | Owner)
- Any prefilled rows — surface these during review, don't silently overwrite
- Any recurring patterns (standing items, fixed attendees block)

Adapt your output to match this structure exactly. Do not invent new columns.

---

## Step 4 — Generate the Full Meeting Summary

Present **all agenda sections at once** in a single compact block. The goal is a 30-second skim for a busy team lead — not a report, not a table.

### Output format

```
Here's the meeting summary. Let me know any corrections, then say "push it" when ready.

---
**[Agenda Section Title]**
Decision: [one line — owner + deadline if stated]
Action: [owner — what — by when]

**[Next Section]**
Decision: [...]
Action: [...]
⚠️ Barely discussed in transcript — verify or skip

...
---
```

**Rules:**
- Show only what matters: decisions and actions. Skip discussion summaries unless a section had nothing but discussion.
- Each line must survive a 3-second skim. Start with a verb or a name. No "It was discussed that..." or "The team agreed to consider..."
- Deadlines: only include if explicitly stated in the transcript. If an action has no date spoken, write `— date not stated, to be confirmed` rather than omitting it or guessing.
- One owner per action item. If multiple people are involved, pick the accountable one. Never write "X + Y" as a joint owner.
- Do not list proposed team members by name unless the team was explicitly approved in the meeting.
- **Directional alignment is not a decision.** Only write `Decision:` if something was formally approved or explicitly stated as final in the transcript. If the group aligned in direction but deferred the final call, write `Direction: [what was aligned on] — pending formal approval` instead. Unapproved names are premature and may cause confusion.
- If a section had no decision or action, write `Nothing actionable — skip?`
- If a section was barely covered (<2 transcript lines), add `⚠️ Barely discussed — verify or skip`
- Omit a "Notes for moderator" block unless there is a genuine ambiguity the moderator must resolve (e.g., conflicting owners, unclear deadline).

---

## Step 5 — Moderator Review

After showing the full summary:

1. Wait for the moderator to reply with corrections in plain language, e.g.:
   - "Section 2, action should be Sarah not Ahmed"
   - "Remove the deadline on section 3"
   - "Skip the last section"
   - "push it"

2. Apply all corrections in one pass and show only the changed lines.

3. On "push it" (or explicit approval): confirm once — "Ready to push X sections to Confluence, tagging AI rows. Go?" — then push.

Do not ask for per-section approval. The moderator reviews everything at once and edits what needs editing.

---

## Step 6 — Push to Confluence

**Only push when the user explicitly says so** (e.g. "push it", "go ahead", "push to Confluence"). Never push automatically after generating or correcting the summary — always wait for that explicit instruction.

**WARNING — `updateConfluencePage` replaces the entire page body.** If you push without first preserving the full existing page content, you will permanently overwrite sections (participants, informed, goals, existing agenda rows, etc.). Before every push:
1. Re-fetch the current page with `getConfluencePage`
2. Copy the full existing body
3. Only modify the target sections (Notes table, ## Notes, ## Action items, ## Decisions)
4. Write back the full page with your changes merged in

Never write a partial page body — always include everything.

Use the Confluence MCP to edit the notes page:

- **Do not recreate the page.** Edit in place.
- **Table cells must be one short line max.** Never put multi-sentence content, bullets, or line breaks inside a table cell — the Confluence markdown parser will break the row. If a topic needs detail, add a **Notes** section below the table with proper bullet points.
- **Never use `[brackets]` in Confluence markdown.** They get escaped to `\[\]` and render as literal text. Use `*(italic)*` for labels like *(AI Generated)*.
- Insert accepted rows into the existing table with the short-form note only (e.g. "No final decision — see notes below").
- Add a dedicated **## Notes** section below the table for all detailed directions, decisions, and discussion points — formatted as bullet points under a bold topic heading.
- Append `*(AI Generated)*` to each bullet or section that was AI-suggested and accepted without editing.
- Cells the moderator edited manually: do **not** tag.
- Do not modify anything outside the notes table and the Notes section.

After pushing, confirm: "✅ Notes pushed to [page title]. X rows tagged [AI Generated], Y rows untagged (edited by you)."

---

## Step 7 — Collect Feedback

After pushing, ask:

> "Quick feedback for next time: anything off? (tone, length, missing fields, wrong format)"

If the moderator gives feedback:

1. Append it to `feedback.md` with today's date and meeting title.
2. Confirm: "Noted — I'll apply this from next session."

### `feedback.md` format

```markdown
# Feedback Log

## [YYYY-MM-DD] — [Meeting Title or "Unknown"]
- [correction 1]
- [correction 2]
```

If `feedback.md` doesn't exist yet, create it.

---

## Edge Cases

| Situation | Handling |
|---|---|
| Agenda section not covered in transcript | Flag: `⚠️ Not discussed in transcript` |
| Multiple speakers, unclear owner | List all names, moderator picks |
| Decision mentioned but no deadline | Write `date not stated — to be confirmed`, don't infer or omit |
| Action has multiple potential owners | Pick the accountable one; never use joint "X + Y" ownership |
| Team composition proposed but not approved | Omit individual names; note the team structure was proposed, not approved |
| Group aligns on direction but defers final decision | Use `Direction:` not `Decision:` — write "pending formal approval" |
| Confluence table cell has long content | Keep cell to one line — move detail to a ## Notes section below the table |
| Need to tag AI content in Confluence | Use `*(AI Generated)*` — never `[AI Generated]` (brackets get escaped) |
| Prefilled row already exists | Show it, ask: "Keep, replace, or merge?" |
| VTT has no speaker names | Note this upfront, use "Unattributed" |
| Meeting notes page not provided | Stop and ask before any processing |

---

## Tone Guide

Apply these always. Load `feedback.md` for user-specific overrides.

- ✅ "Approved vendor shortlist: 3 firms" 
- ✅ "Ahmed: deliver prototype by 30 Jun"
- ❌ "It was decided that the team would look into..."
- ❌ "Discussion took place regarding the topic of..."
- ❌ "The attendees agreed to consider..."

Every line should survive a 3-second skim by a C-level reader.

---

## References

- See `references/vtt-cleaning.md` for VTT parsing edge cases
- See `references/confluence-push.md` for MCP push patterns and error handling