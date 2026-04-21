# Guide 1 — What Is This, Really?

> A plain-English explanation — no tech knowledge needed.

---

## The short version

This kit gives you a **personal AI assistant** that lives inside a free coding app called VS Code.  
You talk to it in normal sentences — just like texting a very smart colleague.

It's connected to your Jira account, so it can look things up, create tickets, write summaries, and help you stay on top of your projects — all without you switching tabs.

---

## What it's NOT

- It's not a robot that does things automatically without asking you
- It won't delete or change anything in Jira without your confirmation
- It doesn't need to be running all the time — you open it when you need it
- It doesn't replace Jira — it works *alongside* it

---

## What does "agent" mean?

When we say your assistant is an "agent," it means it can:

1. **Understand** what you're asking in plain English
2. **Look things up** (like checking your Jira board)
3. **Take a small action** (like drafting a ticket)
4. **Show you what it's about to do and ask if it's OK**
5. **Do the thing** once you confirm

You're always in control. The assistant asks before it acts.

---

## Real examples

> **You:** "What tickets are overdue in my project?"  
> **Assistant:** Checks Jira, shows you a list with ticket keys and due dates.

> **You:** "Create a ticket for the audio sync bug — high priority, assign to Marco."  
> **Assistant:** Shows you the draft ticket, asks "Does this look right before I create it?"  
> **You:** "Yes, go ahead."  
> **Assistant:** Creates the ticket and gives you the link.

> **You:** "Write a status update for the client — keep it short and positive."  
> **Assistant:** Pulls recent Jira activity and writes a polished update you can copy-paste.

---

## What's Copilot?

**GitHub Copilot** is Microsoft's AI assistant — the engine behind your personal assistant.  
Think of GitHub Copilot as the "brain" and this kit as the "personality" you've given it.

Your instructions file (`.github/copilot-instructions.md`) tells Copilot:
- How to talk to you
- What you care about
- What your Jira projects are called
- Who your teammates are

That's why it feels personal — because it is.

---

## What's an MCP server?

An MCP (Model Context Protocol) server is just a "bridge" that lets your AI talk to another app — in this case, Jira.

You don't need to understand how it works. You just need to fill in your Jira credentials once in the config file, and after that it works automatically.

---

## Next step

→ [Guide 2: Setting up VS Code and GitHub Copilot](02-setup-vscode.md)
