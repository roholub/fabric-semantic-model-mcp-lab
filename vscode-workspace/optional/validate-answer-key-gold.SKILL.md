---
name: validate-answer-key
description: "Check the Customer 360 Gold model's numbers against the answer key"
disable-model-invocation: true
---

Read `reference/answer_key.csv`. For each question, write and run one DAX query against the
connected **Customer 360 Gold** model, using the semantic model's measures where they
exist. Use 'Date'[date] filters for the date ranges in the question text.

Show one table: question_id | question | expected | actual | match (yes/no) | DAX used.
For any mismatch, explain the most likely cause (a definition, a relationship, a filter)
and propose a fix, but don't apply it.
