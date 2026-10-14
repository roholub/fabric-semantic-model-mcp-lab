# Planted issues: answer key for the health check (answer key: keep it out of the agent's reach)

Keep this file **outside** the VS Code workspace so the agent can't read it. Use it to score the
agent's review (for example, "found 13 of 16") and to steer the conversation.

Numbers come from a test run at `demo` scale, seed 2026. Your run should match closely; the
`answer_key` table from notebook 01 is the source of truth for anything numeric.

| ID | Category | Planted issue | Evidence the agent should surface | Recommended fix |
|---|---|---|---|---|
| P01 | Model design / Performance | All five relationships use **Email** (long text) as the key | 150,000 distinct e-mails, about 39 characters on average | Integer customer key from the gold layer |
| P02 | Model design | **Wide customer table** (25 columns) mixes attributes with snapshot metrics (NewsletterCount, EventCount, LifetimePageViews) | Column list; metrics stored as columns | Split into a Customer dimension plus fact tables; metrics as measures |
| P03 | Error prevention | **Snapshot disagrees with detail**: LifetimePageViews is as of June 30 | SUM(LifetimePageViews) = 5,636,582 vs. SUM(PageViews) for known customers = 7,540,425 | One definition per metric, as a measure over the detail table |
| P04 | Model design | **No shared Market table**; every table has its own MarketName with source-specific variants | 65 distinct names for 43 markets; active subscriptions: "South Florida" 2,538 + "Miami" 491 = 3,029 | One Market dimension with standard names and a variant mapping |
| P05 | Error prevention | **Orphan rows**: web activity e-mails with no customer | 18,853 web rows (73,568 page views); 1,810 ad orders with an unknown contact | Unknown member (-1) in the gold layer; investigate at source |
| P06 | Performance | **High-cardinality date-time columns** (ActivityDateTime, StartDate, SignupDateTime, LastSeenDateTime, OrderDate) | ActivityDateTime: about 1.25 million distinct values vs. 365 distinct dates | Store dates (and time separately only if needed) |
| P07 | Performance | **Auto date/time on**, no marked Date table | Hidden LocalDateTable tables, one per date column | Turn off auto date/time; add and mark a Date table |
| P08 | Performance / Maintenance | **Unneeded columns**: `_etl_load_ts`, `_source_file`, `row_hash` (unique per row), `LastArticleTitle`, `FullName` | row_hash: 1,275,702 distinct values | Remove at source or from the semantic model |
| P09 | Error prevention | **PostalCode stored as a whole number**: leading zeros lost and summed by default | 6,443 postal codes below 10000 (Boston 021xx shows as 21xx) | Text data type; Summarize By = None |
| P10 | Performance / Formatting | **Floating-point currency** (`plan_prc`, `Amount`; also `OpenRate`) | plan_prc values like 14.920000012987451 | Fixed decimal; round at source |
| P11 | Error prevention | **Numbers and flags stored as text**: TicketPrice like "$153.00", Attended "Y"/"N" | Data types of the columns | Decimal price; true/false flag |
| P12 | DAX | **No explicit measures**, no format strings; visuals use implicit sums | 0 measures in the semantic model | A measures layer with descriptions and formats |
| P13 | Model design | **Bi-directional relationship** customer360 <-> subscriptions (planted by hand) | Relationship list | Single direction; handle special cases in measures |
| P14 | DAX / Performance | **Calculated column using TODAY()** (`Tenure Days`, planted by hand): frozen at refresh time | Calculated column list | A measure, or compute upstream |
| P15 | Maintenance / AI readiness | **No descriptions; cryptic names** (`sub_sts`, `plan_prc`, `bill_cyc`, `chnl`), `pbi_` table names | 0 descriptions | Friendly names, descriptions with synonyms; Prep data for AI |
| P16 | Usability | **Keys and technical columns visible**, IDs summarized by default | Email visible in every fact table | Hide keys; Summarize By = None on IDs |

## Reference totals for the before/after check (as-is model)
| Table | Rows | Numeric totals |
|---|---|---|
| pbi_customer360 | 150,000 | LifetimePageViews 5,636,582 |
| pbi_subscriptions | 142,586 | Active (sub_sts = "A") 91,077; distinct active subscriber e-mails 74,682 |
| pbi_web_activity | 1,275,702 | PageViews 7,613,993; Sessions 1,909,766; ArticlesRead 4,568,156 |
| pbi_newsletter_signups | 169,310 | |
| pbi_event_registrations | 22,003 | |
| pbi_ad_orders | 5,135 | Amount 28,433,534.77; Impressions 662,031,930 |
