---
description: Trace each model problem back to where it starts in the SQL views, pipeline and notebooks
---
Read-only. For the connected semantic model, use the files under `source-context/` (SQL views and stored
procedure, the pipeline definition, the Fabric gold notebook, the scanner table sample).

1. For each table in the model, name the source view or object it comes from (use the scanner sample).
2. For each issue you found in the model health check, say where it begins: the view or procedure and the
   statement (for example the CAST or join that causes it), or "model only".
3. Say which issues the Fabric gold notebook already fixes, so the right fix is "point the model at gold",
   not "patch the view".
4. Say what the nightly pipeline does not check (row counts, orphan rows, market mapping) and suggest three
   cheap checks.

Output a table: Issue | Where it starts (file and statement) | Fix at the source | Fix in the model | Already fixed in gold?
Do not change anything.