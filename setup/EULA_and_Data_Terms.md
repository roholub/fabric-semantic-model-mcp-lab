# Step: read and accept the Power BI Authoring MCP license terms

**Do this once, yourself, before the first run.** The agent will also ask you to confirm it at the start of a session
("Have you reviewed and accepted the EULA?"). Answer only after you have read the terms.

- Terms: https://go.microsoft.com/fwlink/?LinkId=2381247 ("Microsoft Software License Terms: Microsoft Power BI Authoring MCP Server")
- This lab does **not** accept the terms for you: do not add `--accept-eula` to `.vscode/mcp.json` unless you have already read and accepted them.
- Summary below is a plain-English aid, **not legal advice**. Read the real terms and ask your own legal team if unsure.

## Why it is needed
The MCP server is Microsoft software installed on your machine, so it is licensed under its own terms. Using it means accepting them.
The server and the agent skill both ask for confirmation so nobody runs it by accident.

## What the terms say (summary of the version checked Oct 13, 2026)
| Topic | In plain English |
|---|---|
| Install and use (1) | Install on any number of your devices. Third-party components have their own notices |
| Not allowed (2) | No reverse engineering; no removing notices; no illegal use or malware; **no sharing, publishing or redistributing the software**, or offering it as a stand-alone service |
| Data (3) | The software may collect usage information and send it to Microsoft. It may process data outside your region (encrypted in transit). You are responsible for your compliance needs and consents |
| Security (5) | MCP is a new standard: review the security of hosts, clients, agents and AI models you connect. Use Entra ID authentication, secure tokens, network isolation. Clients act with **your Fabric permissions**; autonomous or misconfigured clients can do destructive things, so use least-privilege roles and safeguards. Some safeguards are client-specific |
| Support (6) | None promised; "as is" |
| Updates (7) | May check for, download and install updates automatically |
| Liability (11-12) | Provided "as is"; Microsoft's liability is capped at US $5.00 |

## What this means for how we use it
- **Synthetic data only.** The semantic model's metadata and query results go to the AI model provider behind your agent, and the terms say data may be processed outside your region. Training and retention depend on your Copilot plan and the AI model you pick: see the README.
- **Least privilege and safeguards.** The lab starts the server with `--require-confirmation` and uses read-only for the check step; use a workspace role no higher than needed.
- **We do not redistribute the software.** This repo only links to the official install (VS Code extension, npm package or the Microsoft GitHub repo); it never includes the server files.
- **Plain-English summary to share with your team:** "It is Microsoft-licensed software that runs on your machine. It acts with the permissions of whoever signs in, asks before writes when confirmation is on, and your legal and security teams should review the terms and the data flow before using it on real data."