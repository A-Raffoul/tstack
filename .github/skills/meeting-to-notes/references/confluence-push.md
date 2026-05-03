# Confluence Push Reference

## MCP Setup

The Google Drive / Confluence MCP must be connected. Verify before attempting push.

If MCP is unavailable: tell the user and offer to export the accepted table as a formatted text block they can paste manually.

---

## Read Pattern

To fetch a Confluence page:
1. Use the MCP to search or fetch by URL/page ID
2. Extract the page body (storage format or view format depending on MCP)
3. Identify the notes table — look for `<table>` in storage or markdown table in view format

---

## Edit Pattern (in-place, no recreation)

**Critical**: Only modify the notes table. Leave all other content untouched.

Steps:
1. Fetch current page content
2. Locate the target table
3. Insert new rows (accepted suggestions) after any existing rows
4. Apply `[AI Generated]` tag to AI-suggested cells
5. Push updated content back via MCP update call

---

## `[AI Generated]` Tagging

Append ` [AI Generated]` to the **cell content**, not the row.

Example:
```
| Budget review discussed | Approved Q3 budget increase 15% [AI Generated] | Ahmed, 30 Jun [AI Generated] |
```

Cells edited by the moderator before acceptance: no tag.

---

## Conflict Handling

| Situation | Action |
|---|---|
| Page was edited between fetch and push | Warn user, re-fetch, show diff, ask to proceed |
| Table structure changed | Warn and abort push, show result as text instead |
| MCP auth error | Tell user to reconnect Confluence MCP |
| Page not found | Confirm URL with user, retry once |

---

## Fallback: Manual Paste

If push fails for any reason:
1. Format the accepted table as clean markdown
2. Show it in chat
3. Say: "You can paste this directly into your Confluence page."

Never silently fail. Always tell the user what happened.