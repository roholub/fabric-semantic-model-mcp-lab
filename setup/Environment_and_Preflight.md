# Setup checklist, pre-flight and fallbacks

## One-time setup
| # | Step | Done |
|---|---|---|
| 1 | Fabric workspace `🕵️ Model Detective Agency` on an F SKU or trial capacity | [ ] |
| 2 | Capacity setting: XMLA endpoint = **Read Write** (Admin portal > Capacity settings > Power BI workloads). The tenant setting "Allow XMLA endpoints and Analyze in Excel with on-premises semantic models" must be on (it is by default) | [ ] |
| 3 | Lakehouse `LH_C360_Lab`; import and run `notebooks/01_Generate_Synthetic_C360.ipynb` (scale `demo`) | [ ] |
| 4 | Compare the `answer_key` table printed by notebook 01 with `vscode-workspace/reference/answer_key.csv` (it keeps questions Q01-Q08 and Q13) | [ ] |
| 5 | Create the two semantic models: the TMDL script in README Step 3, or the by-hand route in `setup/AsIs_Model_Setup.md` | [ ] |
| 6 | Optional: run `notebooks/02_BPA_and_Memory_Check.ipynb` on the As-Is model for an independent second opinion | [ ] |
| 7 | VS Code (latest), GitHub Copilot and Copilot Chat signed in, Agent mode available | [ ] |
| 8 | Register the **Power BI Authoring MCP server** (`.vscode/mcp.json`); Command Palette > *MCP: List Servers* shows it running | [ ] |
| 9 | Open the `vscode-workspace` folder in VS Code; type `/` in chat and confirm the skills appear (`/model-health-check`, `/trace-to-source`, `/apply-approved-fixes`, `/validate-answer-key`) | [ ] |
| 10 | Pick the strongest reasoning AI model in the Copilot model picker, and use that same AI model each time so results are comparable | [ ] |
| 11 | Run all four sections once and score the health check against the planted issues | [ ] |
| 12 | Reset the working copy (`setup/VSCode_Setup_and_Connect.md`, section F) | [ ] |

## Pre-flight (before each session)
- The capacity is active, and both models refresh without errors.
- Update VS Code and the extension, then restart VS Code.
- Open a chat in Agent mode and send a short message first. The first message can be slow, and the MCP server cannot start until a chat session exists. Then connect to the semantic model once.
- Confirm the Working Copy is pristine (no measures, nothing hidden, no descriptions).
- Close what you don't need (mail, chat notifications) so nothing interrupts a long run.

## Fallbacks
| If this happens | Do this |
|---|---|
| Sign-in or connection fails | Retry once. Then switch to Power BI Desktop: open the As-Is file and use "Connect to 'Customer 360 - As-Is' in Power BI Desktop". |
| XMLA write is blocked | Run the Section 3 fixes against the semantic model open in Power BI Desktop instead of the workspace. |
| The agent goes off script or runs long | Say "Stop. Summarize what you found so far in the findings format." Then continue. |
| A number doesn't match the answer key | Ask the agent to explain the mismatch. That is useful information, not a failure. |
| Short on time | Run the check and the fix only; skip trace and prove. |
| Something else | See the troubleshooting table in `setup/VSCode_Setup_and_Connect.md`. |