# VS Code workspace

Open **this folder** in VS Code (File > Open Folder) before you start, so GitHub Copilot picks up:

- `.github/copilot-instructions.md`: the guardrails and the review checklist, applied to every chat in this folder.
- `.github/skills/`: the slash commands. In Copilot Chat (Agent mode) type `/` and pick one from the list: `/model-health-check`, `/trace-to-source`, `/apply-approved-fixes` or `/validate-answer-key`. If a command is missing, run **Developer: Reload Window**, then type `/skills`.
- `.vscode/mcp.json`: registers the Power BI Authoring MCP server.
- `source-context/`: the SQL views, pipeline definition, Fabric notebook and scanner sample that the trace step reads.
- `reference/answer_key.csv`: expected numbers for the prove step. Compare it with the `answer_key` table that notebook 01 writes to your lakehouse (the values here come from a run with seed 2026).
- `legacy-prompts/`: the same commands as `.prompt.md` files, for older VS Code versions that still use the Local agent. Copy them to `.github/prompts`.
- `optional/`: extras that are not part of the main steps.
- `docs/`: where the agent writes documentation when you ask it to.