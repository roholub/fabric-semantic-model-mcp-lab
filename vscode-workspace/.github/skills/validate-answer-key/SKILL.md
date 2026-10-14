---
name: validate-answer-key
description: "Prove it: check the fixed Working Copy's numbers against the answer key"
disable-model-invocation: true
---

Goal: show that the semantic model still gives the right business answers after the fixes, and where the data itself needs work.

Connect to **Customer 360 - Working Copy** if you are not already connected. Read `reference/answer_key.csv`.
For each question, write and run one read-only DAX query against the connected semantic model, using the semantic model's measures where they exist.
Use the date columns in the question text (ActivityDateTime, StartDate, EndDate, OrderDate, EventDate).

Rules for this semantic model:
- Customers: count rows in the customer table (there is no Unknown member here).
- Markets: names differ by source system. For Q08, group the variants of the same market (for example "South Florida" and "Miami") and show which names you grouped. Never guess a grouping without listing it.
- Orphans: web rows and ad orders whose e-mail has no customer count in the "all readers" questions and not in the "known customers" questions. Say which questions this affects.
- Flags stored as text ("Y"/"N", "TRUE"/"FALSE"): convert in the query, not in the semantic model.

Questions whose expected value is labeled "GOLD:" or that depend on the gold Market table need a note: say whether the question can be answered on this semantic model and how.

Show one table: question_id | question | expected | actual | match (yes/no) | DAX used.
For any mismatch, explain the most likely cause (a definition, a relationship, a filter, a data problem) and propose a fix, but don't apply it.