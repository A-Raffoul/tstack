# Guide 3 — Connecting Your Assistant to Jira

> Estimated time: 5–10 minutes  
> You'll need: your Jira login email, your company's Jira URL, and an API token (explained below)

---

## Why does this need setup?

Your assistant needs permission to read and write in your Jira account.  
Instead of using your password, Jira uses something called an **API token** — it's like a special key you create just for this assistant.

You create it once, paste it in a config file, and your assistant can access Jira automatically after that.

---

## Step 1 — Find your Jira URL

Your Jira URL looks something like:
```
https://yourcompany.atlassian.net
```

You can find it by logging in to Jira in your browser and copying the address from the address bar — just keep everything up to and including `.atlassian.net`.

Write it down — you'll need it in a moment.

---

## Step 2 — Create an Atlassian API Token

1. Go to this page (while logged in to your Atlassian account):  
   [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

2. Click **Create API token**

3. Give it a name — something like: `My Copilot Assistant`

4. Click **Create**

5. **Copy the token immediately** — you won't be able to see it again after you close the window

> **Keep it safe.** This token gives access to your Jira account. Don't share it or put it in emails.

---

## Step 3 — Add Your Credentials to the Config File

1. In VS Code, find and open the file: `.vscode/mcp.json`  
   (It's in the `.vscode` folder in this kit)

2. You'll see three lines with placeholder text — replace each one:

```json
"ATLASSIAN_EMAIL": "YOUR_ATLASSIAN_EMAIL",
```
→ Replace `YOUR_ATLASSIAN_EMAIL` with your Jira login email, keeping the quotes

```json
"ATLASSIAN_API_TOKEN": "YOUR_ATLASSIAN_API_TOKEN",
```
→ Replace `YOUR_ATLASSIAN_API_TOKEN` with the token you just copied

```json
"ATLASSIAN_SITE_URL": "YOUR_ATLASSIAN_SITE_URL"
```
→ Replace `YOUR_ATLASSIAN_SITE_URL` with your Jira URL (e.g., `https://yourcompany.atlassian.net`)

3. Save the file (`Ctrl+S`)

---

## Step 4 — Install the Jira Connector

The Jira connector runs in the background. VS Code will try to install it automatically when you first use it, but you can trigger it manually:

1. Open a terminal in VS Code: go to **Terminal → New Terminal** at the top
2. Paste this command and press Enter:
```
npx -y @atlassian/mcp-atlassian --version
```
3. If it prints a version number, you're ready. If it asks to install, type `y` and press Enter.

---

## Step 5 — Test the Connection

1. Open the Chat panel (the chat bubble icon on the left)
2. Make sure **Agent** mode is selected at the bottom
3. Type this and press Enter:
```
Can you see my Jira projects? List them.
```

If the assistant lists your Jira projects, the connection is working!

---

## Troubleshooting

**"I can't connect to Jira" or no projects listed**
- Double-check the email, token, and URL in `.vscode/mcp.json` — no extra spaces or missing quotes
- Make sure you're using an API token, not your password
- Check that your API token hasn't expired at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

**"Permission denied" errors**
- Your Atlassian account may not have permission to access certain projects — contact your Jira admin

**The MCP connector didn't install**
- Make sure you have internet access
- Try running `node --version` in the terminal. If it says "command not found," you may need to install Node.js from [nodejs.org](https://nodejs.org) first.

---

## Keeping your credentials safe

The `.gitignore` file in this kit already tells VS Code not to share your `mcp.json` file if you use version control.  
But if you share this folder with someone else, make sure to:
1. Reset the `.vscode/mcp.json` file to its original placeholders first, OR
2. Delete the file before sharing

---

## Next step

→ [Guide 4: Customize Your Agent](04-customize-your-agent.md)
