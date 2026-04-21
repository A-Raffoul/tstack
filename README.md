# Your Personal AI Assistant — Setup Kit

> **Who is this for?**  
> Project managers, music composers, creative leads, and anyone who works with Jira — no coding experience needed.

---

## What is this?

This kit helps you set up your own personal AI assistant inside **VS Code** using **GitHub Copilot**.  
Once set up, you can chat with your assistant in plain English to:

- Create, update, and search Jira tickets
- Generate status reports and sprint summaries
- Draft meeting notes and project plans
- Get reminders and next-step suggestions
- Ask questions about your projects without switching tabs

Think of it like having a smart colleague who always knows your Jira board and can write things for you.

---

## Before You Start — What You Need

| What | Why | Where to get it |
|------|-----|----------------|
| **GitHub account** | To use GitHub Copilot | [github.com](https://github.com) → Sign up (free) |
| **GitHub Copilot subscription** | The AI assistant | [github.com/features/copilot](https://github.com/features/copilot) |
| **VS Code** | The app you'll chat in | [code.visualstudio.com](https://code.visualstudio.com) |
| **Atlassian/Jira account** | Your project boards | You likely already have this |

---

## Setup — Step by Step

### Step 1: Install VS Code and GitHub Copilot

1. Download and install [VS Code](https://code.visualstudio.com)
2. Open VS Code
3. Click the **Extensions** icon on the left sidebar (looks like building blocks)
4. Search for **"GitHub Copilot"** and click **Install**
5. Sign in with your GitHub account when prompted

> Need help? See the detailed guide → [guides/02-setup-vscode.md](guides/02-setup-vscode.md)

---

### Step 2: Open This Folder in VS Code

1. In VS Code, go to **File → Open Folder**
2. Select the folder that contains this README file
3. Click **Open**

VS Code will automatically detect all the settings in this kit.

---

### Step 3: Connect Your Jira Account

This kit includes a pre-configured connection to Jira through a tool called **MCP** (think of it as a bridge between your AI and Jira).

You need to provide your Atlassian credentials once:

1. Open the file `.vscode/mcp.json` in this folder
2. Replace the placeholder values with your details:
   - `YOUR_ATLASSIAN_EMAIL` → your Jira login email
   - `YOUR_ATLASSIAN_API_TOKEN` → your API token (see below)
   - `YOUR_ATLASSIAN_SITE_URL` → your Jira URL (e.g., `https://yourcompany.atlassian.net`)

**How to get an API token:**
1. Go to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Give it a name (e.g., "My Copilot Assistant")
4. Copy the token and paste it in the config file

> Detailed guide → [guides/03-connect-jira.md](guides/03-connect-jira.md)

---

### Step 4: Personalize Your Assistant

Run the setup questionnaire to make the assistant truly yours:

1. Open the **Chat** panel in VS Code (click the chat bubble icon or press `Ctrl+Shift+I`)
2. Make sure **Agent** mode is selected at the bottom of the chat
3. Type this message and press Enter:

```
Use the prompt file #setup-my-agent to guide me through personalizing my assistant.
```

Your assistant will ask you questions about how you work and automatically update its instructions.

> Want to do it manually? See → [guides/04-customize-your-agent.md](guides/04-customize-your-agent.md)

---

## Ready to Use — Your First Chats

Once set up, open the Chat panel and try these:

```
Show me all Jira tickets assigned to me that are due this week.
```

```
Create a Jira ticket for a bug in the login page — high priority, assign to me.
```

```
Write a sprint summary for my team based on what we completed this week.
```

```
What are the blockers in the current sprint?
```

---

## What's in This Kit

```
setup-my-agent/
├── README.md                          ← You are here
├── .github/
│   └── copilot-instructions.md        ← Your assistant's personality & behavior
├── .vscode/
│   └── mcp.json                       ← Jira connection settings
├── guides/
│   ├── 01-what-is-this.md            ← Plain-English overview
│   ├── 02-setup-vscode.md            ← Setting up VS Code step by step
│   ├── 03-connect-jira.md            ← Connecting to Jira
│   └── 04-customize-your-agent.md    ← How to make the agent yours
└── prompts/
    ├── setup-my-agent.prompt.md       ← Interactive setup guide
    ├── daily-standup.prompt.md        ← Daily standup helper
    ├── sprint-planning.prompt.md      ← Sprint planning session
    ├── create-ticket.prompt.md        ← Create well-structured tickets
    └── status-report.prompt.md        ← Generate status reports
```

---

## Getting Help

- **Something isn't working?** Open a chat and ask: `Help me troubleshoot my Jira connection`
- **Want to do something new?** Ask the assistant — it'll figure it out or guide you
- **Questions about GitHub Copilot?** [docs.github.com/copilot](https://docs.github.com/en/copilot)

---

> Made with GitHub Copilot — for humans, not developers.
