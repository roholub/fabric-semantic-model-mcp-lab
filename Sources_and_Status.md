# Product status and sources (checked October 12, 2026)

Preview features can change. Re-check these pages before you rely on them.

| Capability | Status | Source |
|---|---|---|
| **Power BI Authoring MCP server, local** (formerly Power BI Modeling MCP server; VS Code extension ID `analysis-services.powerbi-modeling-mcp`) | Generally available. Learn page updated Sep 17, 2026; extension v1.0.0 published Sep 25, 2026. Windows and Linux; not macOS. | https://learn.microsoft.com/en-us/power-bi/developer/mcp/power-bi-authoring-mcp ; https://github.com/microsoft/powerbi-modeling-mcp |
| **Power BI Authoring MCP server, hosted** (`https://api.fabric.microsoft.com/v1/mcp/powerbi/authoring`) | Preview (announced in the Power BI September 2026 feature summary). Needs the tenant setting "Users can use the Power BI Model Context Protocol server endpoint". | Same Learn page |
| Power BI MCP servers overview | Overview of all Power BI MCP servers | https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview |
| Power BI consumption MCP server (the earlier "remote Power BI MCP server") | Preview. For consumption, Microsoft now recommends Fabric IQ MCP. | https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started |
| Fabric IQ MCP | Generally available; read-only | https://learn.microsoft.com/en-us/fabric/iq/connectors/fabric-iq-mcp |
| Fabric MCP Server, local (microsoft/mcp) | Generally available: 1.0.0 on Apr 14, 2026; 1.4.0 on Aug 27, 2026. Can't create semantic models (no item definition). | https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/pro-dev-local/overview-local-mcp-server |
| Fabric Core MCP server, remote | Generally available (Fabric September 2026 feature summary); preview since March 2026 | https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/core-remote/overview-core-mcp-server |
| Skills for Fabric (microsoft/skills-for-fabric) | Preview (v0.3.x). Wraps the Power BI Authoring MCP server. | https://learn.microsoft.com/en-us/fabric/fundamentals/skills-for-fabric-overview |
| Semantic model authoring skill | Preview | https://learn.microsoft.com/en-us/power-bi/developer/agentic/semantic-model-authoring-skill-overview |
| Copilot in Power BI web modeling | Preview. Browser-based; needs Write permission and a capacity that supports Copilot (F2+ or P1+). | https://learn.microsoft.com/en-us/power-bi/transform-model/copilot-web-modeling |
| Prep data for AI | Preview | https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai |
| Best Practice Analyzer and Memory Analyzer (Semantic Link Labs 0.17.1, Sep 10, 2026) | Notebook tools; 60+ rules in five categories | https://learn.microsoft.com/en-us/power-bi/transform-model/service-notebooks ; https://github.com/microsoft/semantic-link-labs |
| Star schema guidance | Guidance | https://learn.microsoft.com/en-us/power-bi/guidance/star-schema |
| XMLA endpoint read-write | Read-only by default; capacity admins set Read Write | https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools |
| GitHub Copilot: MCP policy and allowlists | "MCP servers in Copilot" policy is disabled by default for enterprises; allowlists GA Aug 6, 2026; new default-policy behavior from Oct 22, 2026 | https://docs.github.com/en/copilot/concepts/enterprise/mcp-management ; https://github.blog/changelog/2026-08-06-mcp-allowlists-in-enterprise-managed-settings/ ; https://github.blog/changelog/2026-09-24-default-enablement-of-copilot-features-for-copilot-business-and-enterprise/ |
| Power BI metadata scanning (scanner) APIs | Return tables, columns, measures (DAX), M expressions, data sources and lineage; need a Fabric admin or service principal plus tenant settings | https://learn.microsoft.com/en-us/fabric/governance/metadata-scanning-overview |

## Key facts from Microsoft's documentation, worth quoting accurately
- Read-write is the default mode and `--readonly` blocks writes. The Learn page says the server asks for confirmation once per model before the first write.
  In our tests (server 1.0.0, Oct 13, 2026) confirmation prompts were skipped unless the server was started with `--require-confirmation`, which is why this lab uses that flag. Re-check the current documentation.
- Transactions and traces are available on the local server only.
- Write permission is needed to change a model; with only Build permission, the server can only
  run DAX queries.
- The local server reaches Fabric models through the XMLA endpoint, which must be Read Write on the
  capacity. There's no separate tenant setting for the local server; disabling XMLA blocks it.
- Metadata, schemas and query results retrieved by the server go to the MCP client and can be
  forwarded to the configured language model provider as part of the conversation.
- DAX query results are capped at 100,000 rows. The server does modeling only (no report pages).
- Microsoft recommends backing up the model and working with Power BI Projects (PBIP) in Git.
- After an XMLA write to a model published from Power BI Desktop, it can't be downloaded as a .pbix.

## Known naming conflicts and open questions
- Some Learn pages still use the old name "Power BI Modeling MCP server".
- The exact GA date of the local Authoring server isn't stated in one place (Learn says GA; the
  extension reached v1.0.0 on Sep 25, 2026).
- GitHub Copilot Free: agent mode is listed as limited; MCP support on the Free plan wasn't
  confirmed in GitHub's docs. Free and individual plans may use interactions for model training
  unless the user opts out, so use an organization plan for company data.

## Added Oct 13, 2026: pages used for the MCP-landscape and governance sections
| Claim | Source (Microsoft Learn, last updated) |
|---|---|
| The Fabric MCP servers are a directory of separate servers (remote and local); an agent can use more than one | https://learn.microsoft.com/en-us/rest/api/fabric/articles/mcp-servers/fabric-mcp-servers-list (Sep 23, 2026) |
| Authoring is one server with hosted (preview) and local (GA) deployment; not for consumption (use Fabric IQ) | https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview (Sep 29, 2026) |
| Avoid registering both local and hosted authoring servers; Write vs Build permission; deep-reasoning model; back up and use PBIP under Git; data goes to the LLM provider; 100,000-row DAX limit | https://learn.microsoft.com/en-us/power-bi/developer/mcp/power-bi-authoring-mcp (Sep 29, 2026) |
| "Skills tell the agent what to do. Tools let the agent do it"; the powerbi-authoring plugin bundles skills and the local server | https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-agentic-overview (Oct 5, 2026) |
| A skill is a static SKILL.md file; skills do not execute code | https://learn.microsoft.com/en-us/fabric/fundamentals/skills-for-fabric-overview (Sep 29, 2026) |
| Permissions, least privilege, security review, data handling, compliance responsibility | Power BI MCP overview (link above) |

Naming note: the Fabric directory page still lists the local server as "Power BI Modeling MCP server" while the Power BI pages call it "Power BI Authoring MCP server".
Not re-verified on Oct 13: the GA/Preview status of the other servers in the directory (check each server's page).

| Claim | Source (checked Oct 13, 2026) |
|---|---|
| Where Copilot models are hosted, provider data commitments, and training: not used for Copilot Business or Enterprise data; individual plans may be used unless opted out; retention differs by provider and model | https://docs.github.com/en/copilot/reference/ai-models/model-hosting |
