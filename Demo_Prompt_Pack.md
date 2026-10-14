# Prompt pack: check, trace, fix and prove a semantic model with an AI agent

Copy-paste prompts in order. Run them in **VS Code > Copilot Chat > Agent mode**, with the `vscode-workspace` folder open and the
**Power BI Authoring MCP server** running (see `setup/VSCode_Setup_and_Connect.md`).
Expected results come from a test run at the default scale; your numbers should match the `answer_key` table from notebook 01.

The pauses are part of the point: the agent is gathering evidence, not guessing.

---
## Section 1: Check (read-only, about 15 minutes)

**Prompt 1.1: connect**
```
Connect to semantic model 'Customer 360 - As-Is' in Fabric workspace '🕵️ Model Detective Agency'.
```
Expected: a sign-in prompt the first time, then confirmation that it's connected.

**Prompt 1.2: tour**
```
Give me a one-screen tour of this model: tables with row counts, relationships (from, to, cardinality, direction, active), measures, calculated columns, and whether auto date/time tables exist. Don't change anything.
```
Expected: 6 tables (150,000 customers; about 1.28 million web rows), 5 relationships on e-mail columns with one set to Both, 0 measures, 1 calculated column (Tenure Days), hidden LocalDateTable tables from auto date/time.

Why it matters: this is what most first versions look like. Nothing here is wrong on day one. It just gets slow and inconsistent as it grows.

**Prompt 1.3: run the health check**: type `/model-health-check` and pick it from the list.
Expected: a ranked findings table. Score it against `setup/Planted_Issues_Answer_Key.md` (16 planted issues). The first line of the reply should be "Health check prompt v4 loaded."

**Prompt 1.4: show the evidence for the e-mail key**
```
Show me the evidence for the e-mail key finding: distinct count and average length of pbi_customer360[Email], and how many pbi_web_activity rows have no matching customer. Include the DAX you ran.
```
Expected: 150,000 distinct, about 39 characters on average; 18,853 orphan web rows.

**Prompt 1.5: the South Florida question**
```
Leadership asks: how many active subscriptions do we have in South Florida? Answer from this model, then tell me whether I should trust the number. Show active subscriptions for every MarketName that could mean South Florida.
```
Expected: "South Florida" 2,538 and "Miami" 491; the true number is 3,029 (answer key Q08).
Why it matters: same data, two names, two answers. One shared Market table fixes it for every report and every agent at once.

---
## Section 2: Trace to source (read-only, about 5 minutes)

Stay in the same chat as the health check: the skill uses its findings.

**Prompt 2.1**: type `/trace-to-source`.
The agent reads `source-context/` (SQL views, nightly procedure, pipeline JSON, Fabric gold notebook, scanner sample) and maps every finding from the semantic model back to the statement that causes it, flags what the gold layer already fixes, and lists cheap pipeline checks.
Expected: the e-mail key, date-time columns, float and text-typed numbers, market names and unknown readers are all traced to a specific view; most are already solved in the gold notebook, so the main recommendation is "point the semantic model at gold" rather than patching the views.

---
## Section 3: Fix (on the working copy, about 10 minutes)

**Prompt 3.1 (optional guardrail check): ask for a change on the protected semantic model**
```
Hide the Email column in pbi_web_activity.
```
Expected: the agent does not change the protected semantic model. It plans the change, says the semantic model is protected, and offers to apply it on the Working Copy: choose "Do not make any change". (The rule comes from the workspace instructions.)
Why it matters: your rules are enforced in plain English, before the server's own confirmation even comes up.

**Prompt 3.2: switch to the working copy**
```
Connect to semantic model 'Customer 360 - Working Copy' in Fabric workspace '🕵️ Model Detective Agency'.
```

**Prompt 3.3: apply the quick wins**: type `/apply-approved-fixes` and add:
```
Fixes: (1) hide the e-mail key columns in every table except pbi_customer360, and hide _etl_load_ts, _source_file and row_hash everywhere; (2) set Summarize By to None on PostalCode; (3) add four measures in a display folder "Measures", each with a description and format string: Total Page Views = sum of pbi_web_activity[PageViews]; Active Subscriptions = rows in pbi_subscriptions with sub_sts = "A"; Active Subscribers = distinct e-mails with sub_sts = "A"; Ad Revenue = sum of pbi_ad_orders[Amount]; (4) add a one-sentence description to each of the six tables.
```
Expected: the agent lists the changes and waits; you reply `approved`; the MCP server asks once to confirm writing to this semantic model; the agent applies everything in one transaction and shows an identical before/after table (for example PageViews 7,613,993; Amount 28,433,534.77). New measures: Active Subscriptions 91,077; Active Subscribers 74,682.
Why it matters: hiding columns and adding measures doesn't change a single number. That's the proof you want before anything goes near production.

---
## Section 4: Prove it (about 5 minutes)

Same chat as the fixes, or a new chat connected to the Working Copy.

**Prompt 4.1: validate against the answer key**: type `/validate-answer-key`.
Expected: Q01 150,000; Q02 91,077; Q03 13,095; Q04 6,082; Q05 624,744; Q06 2,732; Q07 7,603,075.08; Q08 3,029 (needs the agent to group "Miami" with "South Florida"); Q13 7,540,425 (known customers only). The agent should explain any difference.

**Prompt 4.2: a business question, with the DAX shown**
```
How many customers read at least one article and attended at least one event between April 1 and September 30, 2026? Use the model's measures where they exist and show the DAX.
```
Expected: 2,732 (Q06). The agent has to convert the "Y" flag and exclude web rows with no customer.

**Prompt 4.3: what the fixes did and did not change**
```
Compare Customer 360 - As-Is and Customer 360 - Working Copy: list what is different in the semantic model and confirm that no total changed.
```

---

## Optional extra: build a new semantic model from the gold tables (not part of the main lab)

Out of scope for checking an existing semantic model. The skill is in `vscode-workspace/optional/build-from-gold`; copy it into `.github/skills` to use it.


**Optional 1: plan**: type `/build-from-gold`.
Expected: the agent lists 12 `dim_` and `fact_` tables and proposes the star schema,
relationships, Date table, hidden columns and measure DAX, then waits.

**Optional 2: build**
```
Approved. Build it, then show me a summary of what you created.
```
Expected: `Customer 360 Gold` appears in the workspace with 12 tables, 21
relationships (two inactive), a marked Date table, 10 measures and descriptions. It can take a few minutes.

Fallback if creation fails: in the lakehouse select *New semantic model*, name it
`Customer 360 Gold`, tick the `dim_` and `fact_` tables, then connect to it and ask the
agent to continue from "Relationships" in the build prompt.

---

## Reference DAX for the gold semantic model (fallback)
Paste these if the agent's version doesn't validate. Table names are the renamed ones.
```DAX
Customers = CALCULATE ( COUNTROWS ( Customer ), Customer[customer_key] > 0 )

Active Subscriptions =
VAR _asOf = MAX ( 'Date'[date] )
RETURN
    CALCULATE (
        COUNTROWS ( Subscriptions ),
        REMOVEFILTERS ( 'Date' ),
        Subscriptions[start_date] <= _asOf,
        ISBLANK ( Subscriptions[end_date] ) || Subscriptions[end_date] > _asOf
    )

New Subscriptions = COUNTROWS ( Subscriptions )

Cancellations =
CALCULATE (
    COUNTROWS ( Subscriptions ),
    USERELATIONSHIP ( Subscriptions[end_date], 'Date'[date] ),
    Subscriptions[status] = "Cancelled"
)

Churn Rate = DIVIDE ( [Cancellations], [Active Subscriptions] )

Page Views = SUM ( 'Web Engagement'[page_views] )

Readers =
CALCULATE (
    DISTINCTCOUNT ( 'Web Engagement'[customer_key] ),
    'Web Engagement'[articles_read] > 0,
    'Web Engagement'[customer_key] > 0
)

Event Attendees =
CALCULATE (
    DISTINCTCOUNT ( 'Event Registrations'[customer_key] ),
    'Event Registrations'[attended] = TRUE ()
)

Readers Who Attended Events =
VAR _readers =
    CALCULATETABLE (
        VALUES ( 'Web Engagement'[customer_key] ),
        'Web Engagement'[articles_read] > 0,
        'Web Engagement'[customer_key] > 0
    )
VAR _attendees =
    CALCULATETABLE (
        VALUES ( 'Event Registrations'[customer_key] ),
        'Event Registrations'[attended] = TRUE ()
    )
RETURN
    COUNTROWS ( INTERSECT ( _readers, _attendees ) )

Ad Revenue = SUM ( 'Ad Orders'[amount] )
```

Validation query pattern (Q06):
```DAX
EVALUATE
CALCULATETABLE (
    ROW ( "Readers who attended events", [Readers Who Attended Events] ),
    DATESBETWEEN ( 'Date'[date], DATE ( 2026, 4, 1 ), DATE ( 2026, 9, 30 ) )
)
```


