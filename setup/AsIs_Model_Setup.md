# Set up the "as-is" model by hand in Power BI Desktop (optional, about 15 minutes)

The README's Step 3 creates the same models from a TMDL script. Use this by-hand route if you prefer Power BI Desktop, or if you want to see how a first version gets built.

The as-is model is built the way most first versions are built: load the tables, accept the
defaults, add a quick visual. The data already contains most of the planted issues. Two more
are added by hand below (steps 5 and 6). Don't fix anything else; the agent should find it.

**Names used in this repo**
- Fabric workspace: `🕵️ Model Detective Agency` (on a Fabric or trial capacity)
- Lakehouse: `LH_C360_Lab` (filled by notebook 01)
- Models: `Customer 360 - As-Is` (never changed), `Customer 360 - Working Copy`
  (the agent's fixes go here)

## Steps
1. **Power BI Desktop** (latest). Check *File > Options and settings > Options > Current file >
   Data load*: **Auto date/time** is on (the default). Leave *Autodetect new relationships* on.
2. **Connect to the lakehouse SQL analytics endpoint.** Either *OneLake catalog > Lakehouses >
   LH_C360_Lab > Connect to SQL endpoint*, or *Get data > SQL Server* with the endpoint's
   connection string (lakehouse > SQL analytics endpoint > Settings > copy SQL connection string)
   and database `LH_C360_Lab`. Choose **Import** and sign in with your work account.
3. **Select the six `pbi_` tables** (`pbi_customer360`, `pbi_subscriptions`, `pbi_web_activity`,
   `pbi_newsletter_signups`, `pbi_event_registrations`, `pbi_ad_orders`) and select **Load**
   (no Power Query changes). About 1.3 million web rows load in a minute or two.
4. **Model view: make the relationships exactly these** (autodetect usually creates the first four;
   create any that are missing and delete any others):
   - `pbi_customer360[Email]` (1) -> `pbi_subscriptions[Email]` (*)
   - `pbi_customer360[Email]` (1) -> `pbi_web_activity[Email]` (*)
   - `pbi_customer360[Email]` (1) -> `pbi_newsletter_signups[Email]` (*)
   - `pbi_customer360[Email]` (1) -> `pbi_event_registrations[Email]` (*)
   - `pbi_customer360[Email]` (1) -> `pbi_ad_orders[ContactEmail]` (*)
5. **Planted issue: bi-directional filter.** Edit the `pbi_customer360` -> `pbi_subscriptions`
   relationship and set *Cross filter direction* to **Both**.
6. **Planted issue: TODAY() calculated column.** On `pbi_customer360`, add a new column:
   `Tenure Days = DATEDIFF ( pbi_customer360[SignupDateTime], TODAY (), DAY )`
7. **Don't** add measures, descriptions, display folders, or hide anything.
8. **One report page ("Overview")**, implicit measures only:
   - Clustered bar: `pbi_web_activity[MarketName]` by *Sum of PageViews* (you'll see "Miami" and
     "South Florida" as separate bars, plus DFW, Twin Cities, Puget Sound...).
   - Card: *Count of SubscriptionID*.
   - Matrix: `pbi_subscriptions[MarketName]` rows, `sub_sts` columns, *Count of Email*.
9. **Save** as `Customer 360 - As-Is.pbix` (optionally also *Save as* a Power BI
   Project, .pbip, in a Git folder) and **Publish** to `🕵️ Model Detective Agency`.
10. **Save as** `Customer 360 - Working Copy.pbix` and **Publish** again.
11. In the workspace, confirm both semantic models exist. Run notebook 02 once to record the
    Best Practice Analyzer baseline for the As-Is model.

## Reset
- Delete the **Working Copy** semantic model and report in the workspace, then publish
  `Customer 360 - Working Copy.pbix` again. (After the agent changes a semantic model through
  the XMLA endpoint, that semantic model can no longer be downloaded as a .pbix, so always keep the local
  file as the source.)
