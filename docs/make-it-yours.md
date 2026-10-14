# Make it yours: build your own skills, instructions and checks

This is the long version of the "Make It Yours" section of the README. It is not official Microsoft guidance. Where a statement comes from Microsoft or GitHub documentation, the source is linked.

## 1. What a skill is, and where it lives

A skill is a folder with a `SKILL.md` file: a name and a description at the top, then plain-language instructions. Microsoft describes skills as static knowledge. They do not run code on their own, and the AI tool decides what to do with the guidance ([Skills for Fabric overview](https://learn.microsoft.com/en-us/fabric/fundamentals/skills-for-fabric-overview)).

In VS Code, according to the [Agent Skills page](https://code.visualstudio.com/docs/agent-customization/agent-skills):

| Kind | Where it lives |
|---|---|
| Project skill (shared through your repository) | `.github/skills/`, `.claude/skills/` or `.agents/skills/` |
| Personal skill (yours only) | `~/.copilot/skills/`, `~/.claude/skills/` or `~/.agents/skills/` |

- Type `/skills` in Chat to see and configure them. Type `/create-skill` to have the agent draft one for you.
- Discovery makes a skill available to the AI model. It does not guarantee the AI model uses it for every prompt.
- Skills in this repo set `disable-model-invocation: true`, so they only run when you type the slash command. That is what you want for anything that touches a semantic model.
- **Prompt files do not work here.** In VS Code 1.141 the Copilot chat runs on Agent Host, which does not load `.prompt.md` files. See the README for how I found out.

Microsoft also packages skills with the server in a plugin. The `powerbi-authoring` plugin from Skills for Fabric bundles skills and the local Power BI Authoring MCP server ([Power BI Agentic overview](https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-agentic-overview)). That is a good source of general Power BI guidance. Your own skills should say what *your* standards are.

## 2. Instructions versus skills

| | Instructions file (`.github/copilot-instructions.md`) | Skill (`.github/skills/<name>/SKILL.md`) |
|---|---|---|
| When it applies | Automatically, to every chat in the folder | Only when you call it (with `disable-model-invocation: true`) |
| Put here | Standards and rules that always apply: naming, star schema rules, what must never happen, masking, the protected-model rule | A workflow with steps: check, trace, fix, prove |

## 3. A skeleton for your own skill

Use this structure, the same one as the four skills in this repo.

```markdown
---
name: your-skill-name
description: "One sentence: what it does, and that it is read-only (or what it changes)"
disable-model-invocation: true
---

Begin your reply with exactly this line: Your skill name v1 loaded.

Goal: <what a good result looks like>. Do not change anything.   <- or the exact rules for changes

Rules for this task: complete every numbered item in order, keep the numbers in your report,
do not merge or skip items, and end with a coverage table.

1. <what to read>
2. Evidence: run a query for EACH item and report the result even when nothing is wrong:
   E1. ...
   E2. ...
3. Report in this format: <your table columns>. Sort by impact.
4. Coverage table (last section): one row per evidence item, done / not done, one line of result.
```

Three habits made the biggest difference in this repo:
1. **A first-line "vN loaded" check.** If you do not see it, the skill was not delivered.
2. **Numbered evidence items and a coverage table.** A skipped check becomes visible instead of silent.
3. **Write what the agent must not do** (read-only, ask before changes, never write to a semantic model unless its name says it is a working copy).

## 4. Scoring your own runs

The lab has planted issues, so I could score each run (11 to 13 of 16 before the skill was delivered, 16 of 16 after). On your own semantic model you do not have a planted list. Build one:

| Source of "known issues" | How to use it |
|---|---|
| The Best Practice Analyzer output (60+ rules in five categories, per [Microsoft Learn](https://learn.microsoft.com/en-us/power-bi/transform-model/service-notebooks)) | Treat each violation as a known issue. Does the agent find it? |
| Issues your team already knows about | Write them down before the run, and check them off |
| A semantic model you break on purpose | Copy a dev semantic model, add a few known problems (a bi-directional relationship, a text key), and see what the agent catches |

Keep a short score file like `setup/Health_Check_Scores.md`: date, skill version, semantic model, what was found, what was missed. When you change a skill, run it again in a **new chat** and compare.

## 5. Source context for the trace step

The trace skill reads whatever is in `source-context/`. For your semantic models that means:
- the SQL views and stored procedures behind the tables the semantic model imports
- pipeline definitions (export them as files)
- notebook code
- a table of which semantic model tables come from which source object. The [metadata scanner APIs](https://learn.microsoft.com/en-us/fabric/governance/metadata-scanning-overview) return names of tables and columns, measures, DAX expressions and mashup queries for semantic models. Setup is done by a Fabric admin, and scanning needs no special license. The `scanner/` sample in this repo is a simplified table built from scan results, not the raw API output.

Copy files as read-only exports. Remove secrets, connection strings and personal data first.

## 6. A short ownership checklist

- [ ] The toolkit lives in Git, and changes go through review
- [ ] Each skill has a version and a first-line check
- [ ] Each skill has a score history
- [ ] The instructions file says what the agent must never do
- [ ] Runs happen on a dev or test copy, with a backup, least privilege and masked data
- [ ] Someone owns the answer key and updates it when the business definition changes
- [ ] You have read the MCP server's license terms and your Copilot plan's data-handling terms