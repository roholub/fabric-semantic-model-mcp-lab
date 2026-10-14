---
description: Read-only health check of the connected semantic model against Microsoft best practices (v3: numbered evidence, mandatory coverage table)
---
Begin your reply with exactly this line: Health check prompt v3 loaded.

Run a read-only health check of the semantic model I'm connected to. Do not change anything.

**Rules for this task.** Treat this as a fresh review even if you have already checked this model earlier in the chat: do not reuse earlier results and do not describe it as a "rerun" or a "drift check". Run every query again. Complete every numbered item below, in order, and keep the numbers (E1, E2, ...) in your report.
Do not merge, skip or summarize items. If an item does not apply, say "not applicable" and why. Your answer is NOT complete
until it ends with the coverage table in step 5.

1. **Inventory**: tables with row counts; columns (data type, Summarize By, hidden);
   relationships (from -> to, cardinality, cross-filter direction, active); measures;
   calculated columns **with their full DAX expressions**; auto date/time tables; whether a Date table is marked.
2. **Evidence**: run a DAX query for EACH item and report the result, even when nothing is wrong:
   E1. distinct count and average length of every column used in a relationship;
   E2. fact rows with no matching row on the one side of each relationship;
   E3. for every descriptive column that appears in more than one table (for example market, region or product names):
       list the distinct values side by side and flag values that look like aliases, nicknames or spelling variants of the
       same real-world entity. Report total distinct names versus the number of real entities after grouping variants;
   E4. for every column whose name or values suggest a count, total, "lifetime" value or snapshot: recompute the same figure
       from the detail table through the relationships and show BOTH numbers and the difference;
   E5. every calculated column: its full expression, and whether it uses TODAY(), NOW() or another volatile function;
   E6. columns with one distinct value per row that are not a key (hashes, load timestamps), free-text columns with high
       cardinality, columns that duplicate other columns (for example a full name next to first and last name), and
       columns not used by any relationship or measure;
   E7. for the largest tables: data type and distinct count of each date or date-time column, and whether the time part is ever non-zero;
   E8. any table with more than 15 columns that mixes descriptions and metrics (list them);
   E9. every text column that looks like a number, currency amount, date or yes/no flag: show a sample of distinct values;
   E10. relationships with a cross-filter direction other than single: show how a count of the one-side table changes when the many-side table is filtered.
3. **Check** against the checklist in the workspace instructions (model design, performance,
   DAX, error prevention, maintenance and usability, AI readiness).
4. **Report** in the findings format, sorted by impact. Use numbers from your queries as evidence.
   End with "Top 3 quick wins" and "Needs a design decision".
5. **Coverage table** (the last section): one row per E1..E10 and per checklist area, each marked done / not done,
   with the result in one line. Do not skip a row.