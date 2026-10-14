# VS Code setup and connect: step by step (tested Oct 13, 2026)

Do this once before you start your work (about 10 minutes), then use the 2-minute pre-flight each time you come back to it.

## A. One-time setup
1. **Fabric capacity on** (F SKU or trial) and workspace **🕵️ Model Detective Agency** on it. XMLA endpoint set to **Read Write** in the capacity's Fabric admin settings.
2. **Connection for the semantic models** (needed once per semantic model): in the workspace open each semantic model, then Settings, then **Gateway and cloud connections**. Under *Maps to*, pick the shared connection `conn_c360_lab_sql` (create it once: SQL Server, authentication **OAuth 2.0**, sign in with the demo account, Encrypted, privacy level Organizational; leave SSO unchecked). Click **Apply**, then refresh the semantic model once.
3. **VS Code**: install **GitHub Copilot** and the extension **Power BI Authoring MCP Server** (`analysis-services.powerbi-modeling-mcp`, version 1.0.0 or later). Restart VS Code.
4. **Open the folder** `vscode-workspace` (File, then Open Folder). Choose *Trust* when asked.
5. The folder contains `.vscode/mcp.json`, which registers the server `powerbi-authoring-local` and starts it with `npx` (the form Microsoft Learn documents), with `--readwrite --require-confirmation`. If you use the VS Code extension instead, copy `.vscode/mcp.extension-example.json` over it and fix the path: in our tests VS Code did not expand `${userHome}`, so use the full path.
   - Do **not** use the "Add Server" button or the old "Install" entry under *Available*; that creates a second entry marked *Unsupported*.

4b. **Read and accept the license terms** yourself: see `EULA_and_Data_Terms.md`. The agent asks you to confirm at the start of each session.

## B. Pre-flight before you start

**WARM-UP FIRST (do this 30+ minutes before you start your work, not live):** open a chat in Agent mode and send `hello`. The first message can take a long time because it loads the MCP servers, plugins and skills, and the Power BI server cannot start until a chat session exists. Then connect to the semantic model once and run one small read-only question so everything is warm. Reuse that same chat for the real work if you can.

Then the 2-minute checks:
1. Capacity is **Active**. Both models refresh without errors (workspace, then semantic model, then Refresh now).
2. Open the `vscode-workspace` folder. Open **Chat**, switch to **Agent** mode, and send a short message first (for example "hello"). **The MCP server cannot start until a chat session exists.**
3. Open `.vscode/mcp.json` and check the link above the server says **Running**. If it says Error or Start, click **Start**.
4. In the chat tools picker, **untick everything except `powerbi-authoring-local`**. Click **Skip** on any "Waiting for MCP servers" banner and do **not** click "Authenticate" for the other servers.
5. Check which accounts are signed in: click the Accounts icon (bottom-left). Other MCP servers must not be signed in with a real work account. Better: use a separate VS Code **profile** with only this server and no other MCP servers.
6. Send the connect prompt and sign in with the **lab-tenant account** when the browser opens:

   > Connect to semantic model 'Customer 360 - As-Is' in Fabric workspace '🕵️ Model Detective Agency'. Use only the powerbi-authoring-local server. Read-only. Tell me which tables it has, how many columns each, and whether it has any measures.

   Expected: 6 tables (pbi_customer360 has 26 columns including the calculated column Tenure Days), 0 measures.

7. **New chat = new session.** If you open a new chat the connection is gone; the agent asks where to run the check. Choose the custom answer and type: `Connect to Fabric workspace '🕵️ Model Detective Agency', semantic model 'Customer 360 - As-Is' (powerbi-authoring-local only), then continue.`  For a clean health check always use a new chat: results from an earlier check in the same chat make the agent shortcut or call it a "rerun". Warm the connection up in one chat, then start the check in a fresh one.

## C. If something goes wrong
| Symptom | Fix |
|---|---|
| Server entry says **Unsupported** | Remove the duplicate entry; use only the workspace `mcp.json` |
| Link says **Error**; log says "Cannot start an MCP server before the session runtime has been created" | Send a message in Chat first, then click Start |
| Chat stuck on "Waiting for MCP servers" | Click **Skip**; untick the other servers |
| "Authentication failed" on connect | Sign in with the lab-tenant account in the browser window; try again |
| "XMLA endpoint" or read-write error | Capacity admin settings: set XMLA to Read Write |
| Refresh error "default data connection without explicit credentials" | Map the semantic model to `conn_c360_lab_sql` (step A2) |
| Chat asks **Run in terminal?** for a "weekly plugin update check" (`last-update-check.json`) | That is the Fabric plugin's check-updates skill, not our server. Click **Skip**. Before the session disable the Fabric collection plugin(s) under Agent Customizations, then Plugins, or use a clean VS Code profile |
| `/model-health-check` is missing from the slash list | VS Code 1.141+ (Agent Host) does not load .prompt.md files. This repo uses skills in `.github/skills`. Run **Developer: Reload Window**, type `/skills` to check, and pick the command from the list instead of pasting text. The first reply line should be "Health check prompt v4 loaded." |
| Notebook 02 fails at `%pip install` when run from a pipeline or an API job | Inline `%pip` is turned off for non-interactive runs by default. Run the notebook interactively, or pass the boolean parameter `_inlineInstallationEnabled = True` ([Manage Apache Spark libraries](https://learn.microsoft.com/en-us/fabric/data-engineering/library-management)) |
| ConnectFabric "Request timed out" | The Microsoft sign-in is pending. Finish the sign-in prompt (browser or VS Code), then tell the agent to retry |
| DAX calls fail with "Request timed out" | The semantic model was cold and several queries ran at once. Run one small query first (for example row counts), then continue one query at a time with a 200-second timeout |
| Server log empty / never starts | Check the path in `mcp.json` points to an existing .exe |

## D. Facts worth knowing
- The server confirms before writing **only** if started with `--require-confirmation` (without it, confirmations are skipped by default).
- `--readonly` blocks all writes; use it for the check step, then restart with `--readwrite` for the fix step.
- Log files: `%APPDATA%\Code\logs\<session>\window1\` (look for `agentHostMcpServer*` and `mcpServer*powerbi*`).
## E. How `/model-health-check` works (so you can explain it)
`/model-health-check` is a **skill** (a saved slash command) in `.github/skills/model-health-check/SKILL.md`. Typing `/` and picking it sends those instructions to the agent. It is not a built-in analyzer and not a feature of the MCP server; it is a well-written request.

1. **Inventory (facts):** the agent calls the server's tools to *read* the semantic model: tables, columns, relationships, measures and calculated-column expressions.
2. **Evidence (facts):** the agent writes and runs read-only DAX queries against the live semantic model (the E1-E10 list): orphan rows, snapshot versus detail, distinct values, date-time cardinality. If the agent ran the query, the number is right.
3. **Judgment (AI):** the semantic model compares what it found with the checklist in `.github/copilot-instructions.md` (star schema, performance, DAX, error prevention, maintenance, AI readiness). What counts as an issue and how serious it is can be wrong, which is why every finding must show its DAX.
4. **Report:** findings with severity, evidence, fix and effort, then a coverage table that shows which checks ran.

It changes nothing: the prompt says read-only, the server writes only to a semantic model whose name contains "Working Copy" or "Gold", and `--require-confirmation` asks before each query or change.

In one line: *the agent measures first, then judges. The numbers come from queries you can rerun, and each recommendation comes with its evidence.*

## F. Reset the working copy (about 5 minutes)
The agent's changes to the Working Copy go through the XMLA endpoint and cannot be undone or downloaded as a .pbix, so you rebuild it instead.
1. Run `fabric/as-is-model/reset_working_copy.ps1` (needs `az login` and the generated TMDL schema). It deletes the Working Copy and redeploys the flawed definition under the same name. If a network call fails, run it again.
2. Open the new Working Copy, then Settings, then **Gateway and cloud connections**, map it to your connection and click **Apply** (the API cannot set credentials).
3. Refresh it. Check that `[Total Page Views]` no longer exists and the six tables have no descriptions. The As-Is model is never changed, so it needs no reset.

## G. What the fix step looks like (tested Oct 13, 2026)
- The skill `/apply-approved-fixes` plans first, then waits for you to type or select "approved".
- It captures row counts and sums, begins a transaction, applies all writes (25 in our test), and commits. New measures are not queryable until the transaction commits, so the agent commits and then re-runs the same DAX. If a number had changed, it would have had to revert with compensating changes. Don't promise an automatic rollback.
- Asking for a change on the As-Is model: the agent refuses (protected-model rule) and offers to apply it to the Working Copy instead. Say no unless you want that change.