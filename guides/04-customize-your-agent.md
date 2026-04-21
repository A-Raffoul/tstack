# Guide 4 — Customize Your Agent

> Make the assistant truly yours — takes about 5 minutes

---

## Why customize?

Out of the box, your assistant is helpful but generic. When you customize it, you tell it:
- Who you are and what you do
- Which Jira projects to look at by default
- Who your teammates are (so you can say "assign to Marco" instead of using an email)
- How you like to communicate
- Any habits or preferences it should always respect

The more context you give it, the less you have to repeat yourself.

---

## Option A — Let the assistant guide you (recommended)

1. Open the Chat panel in VS Code
2. Select **Agent** mode at the bottom
3. Type this message:
```
#setup-my-agent
```
4. The assistant will ask you questions one at a time and update your instructions automatically

---

## Option B — Edit the file directly

Open `.github/copilot-instructions.md` in VS Code and fill in the section called **"Team & Project Context"**.

Here's what each field means:

---

### Your name
```
- **My name:** Sarah
```
The assistant will use this when referring to you or when drafting messages on your behalf.

---

### Your role
```
- **My role:** Music Supervisor
```
Or: Project Manager, Producer, Creative Lead, Team Coordinator — whatever fits.

This helps the assistant understand the kind of work you do and tailor its suggestions.

---

### Your Jira projects
```
- **My Jira projects:** MUS, SYNC, PROD
```
List the project keys separated by commas. These are the short codes that appear at the start of ticket numbers (e.g., `MUS-142`).

You can find them in Jira by looking at any ticket in your project — the letters before the dash are the project key.

---

### Your team members
```
- **My team members:** Marco (Developer), Lisa (Designer), Tom (QA), Anna (Producer)
```
Add names and roles for the people you work with most often.  
Once added, you can say things like "assign to Anna" and the assistant will know who you mean.

---

### Sprint cadence
```
- **My sprint cadence:** 2 weeks
```
Or: `1 week`, `3 weeks`, or `We don't use sprints — we work in continuous flow`.

---

### Priority language
```
- **Priority language:** P1 (Critical), P2 (High), P3 (Medium), P4 (Low)
```
Or use whatever your team uses: `Blocker / Critical / Major / Minor` or `Urgent / High / Normal / Low`.

---

### Language preference
```
- **Language preference:** English
```
Your assistant will respond in this language. You can write to it in any language, and it will respond in your preferred one.

---

### Custom working preferences

At the bottom of the instructions file, you can add any other notes about how you work. For example:

```
Additional preferences:
- Always ask me before creating more than one ticket at a time
- When writing ticket descriptions, use bullet points not paragraphs
- For music-related tasks, use track-centric language (track, sync, cue, license)
- I prefer short summaries — don't give me more than 5 bullet points at once
```

---

## Tips for great instructions

- **Be specific** — "always use bullet points" is more useful than "be concise"
- **Use examples** — "for status updates, use the format: Done / Doing / Next" tells the assistant exactly what you want
- **Update as you go** — as you use the assistant, you'll discover things to add. Open the file and add them whenever
- **Less is more for names** — for team members, first names are usually enough

---

## Testing your changes

After saving the file, test your new settings:

```
Remind me who is on my team and what projects I work in.
```

The assistant should reflect exactly what you put in the file.

---

## Sharing this kit with a colleague

If you want someone else to set up their own assistant using this kit:

1. **Reset** the personalization section in `.github/copilot-instructions.md` back to the placeholder text
2. **Reset** `.vscode/mcp.json` back to its original placeholders (so your credentials aren't included)
3. Zip or share the folder — they follow the same guides to set it up for themselves

Everyone gets their own version, personalized to them.

---

## You're all set

Your assistant is ready to use. Here are a few things to try:

```
Show me all my open Jira tickets.
```

```
#daily-standup
```

```
#create-ticket
```

```
#status-report
```
