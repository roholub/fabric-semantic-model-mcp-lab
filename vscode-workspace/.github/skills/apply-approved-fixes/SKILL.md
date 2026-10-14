---
name: apply-approved-fixes
description: "Apply only the fixes I approve, in one transaction, and prove the totals did not change"
disable-model-invocation: true
---

Apply only the fixes I list in my message. Before changing anything:

1. Confirm the connected semantic model's name contains "Working Copy" or "Gold".
   If it doesn't, stop and tell me.
2. Show the exact change list (object, property, old -> new) and wait for "approved".
3. Capture baseline numbers with DAX: row count per table and the sum of every numeric
   fact column.
4. Apply the changes in one transaction. Re-run the baseline queries.
5. If any baseline number changed, roll back and explain why. Otherwise commit.
6. Summarize what changed and show the before/after table.
