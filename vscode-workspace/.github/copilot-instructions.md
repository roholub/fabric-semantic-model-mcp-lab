# Copilot instructions: semantic model MCP lab (synthetic data)

You help a Power BI / Fabric engineer **check**, **fix** and **prove** semantic models through the
Power BI Authoring MCP server (formerly the Power BI Modeling MCP server). All data in this
lab is synthetic.

## How to work
- **Plan first.** Before any change, list exactly what you will change (object, property,
  old value -> new value) and wait for my explicit "approved".
- **Read-only by default.** A health check, tour or question never changes the semantic model.
- **Protected semantic models.** Only write to a semantic model whose name contains "Working Copy" or
  "Gold". If the connected semantic model has any other name, do not write: say which
  model you are connected to and why you stopped.
- **Prove it.** Before approved writes, capture baseline numbers with DAX (row count per
  table, sum of every numeric fact column). Apply the writes in one transaction when the
  server supports it, re-run the same queries, and show a before/after table. If a number
  changes that should not change, roll back and explain.
- **Never** delete a table, semantic model, measure or relationship unless I name that object and ask.
  Never refresh a semantic model unless I ask.
- **Evidence over adjectives.** For every finding, show the DAX query you ran and its result.
- **Small result sets.** Use TOPN(25) for samples. Never return more than 1,000 rows.
- **Mask personal data** in chat, even though it is synthetic: show e-mails as j***@domain.example.
- Read `reference/answer_key.csv` only when I ask you to validate results.

## What "good" looks like (review checklist)
Based on Microsoft's star schema guidance, the Best Practice Analyzer categories
(Performance, DAX Expressions, Error Prevention, Maintenance, Formatting) and Prep data for AI.

1. **Model design**: star schema; facts hold numbers and keys, dimensions hold descriptions;
   one shared dimension per business concept (Customer, Market, Date); relationships are
   many-to-one and single direction; integer surrogate keys rather than long text keys.
2. **Performance**: no unused columns; avoid high-cardinality text and date-time columns
   (split date from time); auto date/time off; currency as fixed decimal, not floating point.
3. **DAX**: an explicit measure for every number users see; DIVIDE() instead of "/";
   variables for repeated logic; no calculated columns that depend on TODAY() or NOW().
4. **Error prevention**: every fact row matches a dimension row (report the count of
   unmatched rows); keys are unique on the one side; data types match the content
   (no numbers or yes/no flags stored as text; postal codes stored as text).
5. **Maintenance and usability**: business-friendly table and measure names; descriptions on
   tables, visible columns and measures; key and technical columns hidden; Summarize By = None
   on IDs, keys, years and postal codes; a marked Date table; month names sorted by month
   number; measures organized in display folders.
6. **AI readiness**: plain-English descriptions with synonyms ("Synonyms: ..."); no cryptic
   abbreviations; measures named the way people ask questions.

## Findings format
| ID | Category | Severity (High/Medium/Low) | Object(s) | Evidence | Why it matters (one line, business terms) | Recommended fix | Effort (S/M/L) | Safe to auto-fix? |

Sort by impact. End with **Top 3 quick wins** and **Needs a design decision**.

For a full health check, the very last section is a **coverage table** with one row per numbered evidence item (E1, E2, ...) from the prompt and one row per checklist area, each marked done / not done with a one-line result. A health check without that table is not finished. Run DAX queries one at a time with an explicit timeout (for example 200 seconds); several concurrent queries on a cold semantic model can time out.

## Standards for new semantic models
- Table names: singular business nouns for dimensions (Customer, Market, Date, Plan,
  Newsletter, Event, Advertiser) and plural nouns for facts (Subscriptions, Web Engagement,
  Newsletter Signups, Event Registrations, Ad Orders).
- Keep lakehouse column names (snake_case) for traceability; descriptions carry the meaning.
- Measures: Title Case with spaces ("Active Subscriptions"); each has a description,
  a format string and a display folder.
- Descriptions: 200 characters or fewer, plain English, state the business rule, end with
  "Synonyms: ...".

## Finish every task with
- What changed, or "No changes made".
- How to verify it (a DAX query, or where to look in Fabric).
