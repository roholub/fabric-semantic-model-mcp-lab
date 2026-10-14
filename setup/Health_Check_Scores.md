This file is a log of how the health-check skill scored on the 16 planted problems across versions. It is here so you can see how the instructions changed the results, and as a template for scoring your own runs.

> **Read this first.** Runs 1-4 below are the **baseline**: in VS Code 1.141 the Copilot session does not load `.prompt.md` files, so our `/model-health-check` prompt was never delivered. The agent worked only from the instructions file and the Fabric plugin's own skill. Run 5 is the first run where the prompt was delivered (converted to a skill). Baseline: 11-13 of 16 issues found. With the skill: 16 of 16.
# Run 1 score: health check on "Customer 360 - As-Is" (Oct 13, 2026, VS Code + GitHub Copilot + Power BI Authoring MCP local 1.0.0)

Answer-key file. Keep outside the agent's workspace (it lists the planted issues).

**Result: 11 found, 2 partly found, 3 missed (13 of 16 with partial credit). 7 findings, 0 false positives. No changes made.**

| ID | Planted issue | Result | What the agent said |
|---|---|---|---|
| P01 | Email (long text) as the key everywhere | Found | F2: all five relationships use email text |
| P02 | Wide customer table mixing attributes and snapshot metrics | **Missed** | Not mentioned |
| P03 | Stale snapshot (LifetimePageViews) disagrees with detail | **Missed** | It summed the column but never compared it with the web detail (5,636,582 vs 7,540,425) |
| P04 | No shared Market table, name variants | Partial | Only a "design decision" at the end; no evidence of the 65 spellings for 43 markets |
| P05 | Orphan rows | Found | F1: 18,853 web rows and 1,810 ad orders (matches answer key) |
| P06 | High-cardinality date-times | Found | F5: 1,250,205 distinct values for 1,275,702 rows (matches) |
| P07 | Auto date/time on, no marked Date table | Found | F5 and Q7 |
| P08 | Unneeded columns | Partial | Said to hide 9 technical columns; did not mention row_hash uniqueness, LastArticleTitle or FullName |
| P09 | PostalCode as a whole number | Found | F4 (sum of postal codes 7,690,863,144) |
| P10 | Floating-point currency | Found | F4 |
| P11 | Numbers and flags stored as text | Found | F4 (TicketPrice, IsEnterprise, Attended) |
| P12 | No explicit measures | Found | F3 |
| P13 | Bi-directional relationship | Found | F2 (rel1) |
| P14 | Calculated column with TODAY() (Tenure Days) | **Missed** | It summed the column but did not read its expression |
| P15 | No descriptions, cryptic names | Found | F6, F7 |
| P16 | Keys and technical columns visible, IDs summarized | Found | F6, F4 |

## What the misses have in common
All three misses (and the partial one on markets) need a **cross-table or expression check**: compare a snapshot with detail,
list distinct values across tables, read a calculated column's expression. The agent was very good at counting and metadata
and skipped the checks that need a comparison. The prompt already asked for them; the agent did not do them.

## What I changed in prompt v2
Turned the evidence step into a numbered list that must each be reported, with a coverage table at the end
("check, done or not, result"), so a skipped check is visible. Re-run and compare with this score.

## Other things learned
- The agent first called the old user-level server ``com.microsoft/powerbi-modeling-mcp`` (EULA error), then used ``powerbi-authoring-local``. Disable the old entry before the session.
- The agent can accept the EULA itself through an ``accept_eula`` tool after you answer yes.
- The protected-model rule worked: it said the As-Is model is not writable because its name has no "Working Copy" or "Gold".
- It cleaned up only its own temp files and disconnected at the end.

---

# Run 2 score (Oct 13, 2026, prompt v2, same setup)

**Result: 11 found, 4 partly found, 1 missed. 12 findings, 0 false positives. No changes made.** (Run 1: 11 / 2 / 3.)

| ID | Run 2 | Note |
|---|---|---|
| P01 | Found | H04 |
| P02 | Found | H12 (low severity): mixes attributes and derived metrics |
| P03 | Partial | "stale or conflicting definitions", but no comparison of the snapshot with the detail (5,636,582 vs 7,540,425) |
| P04 | Partial | Asked for a Market dimension, but reported "65 markets in every table"; did not group variants (65 spellings = 43 markets) |
| P05 | Found | 18,853 web rows and 1,810 ad orders |
| P06 | Found | Reported the share of values with a time part |
| P07 | Found | |
| P08 | Partial | Found unique-per-row hashes; not the other unneeded columns |
| P09 | Found | 6,443 postal codes below 10000 |
| P10 | Found | Float artifacts in totals |
| P11 | Partial | TicketPrice only; dropped Attended and IsEnterprise |
| P12 | Found | |
| P13 | Found | Best evidence yet: 44,904 of 150,000 customers removed by the reverse filter |
| P14 | **Missed** | Never read the Tenure Days expression |
| P15 | Found | |
| P16 | Found | |

**Did not follow v2:** no E1-E8 numbering, no coverage table, and E4 (snapshot versus detail) and E5 (calculated-column expressions) were not run. Unverified whether the prompt file or pasted text was used.

**Prompt v3 changes:** "complete every item, don't merge" rule; explicit alias check (E3) and snapshot recompute (E4); expression for every calculated column (E5); duplicate and free-text columns (E6); text-typed values (E9); cross-filter effect (E10); coverage table mandatory as the last section.

---

# Run 3 (Oct 13, 2026, prompt v3): INVALID test

Run in the same chat as run 2. The agent treated the request as a **rerun to detect drift**, reused its earlier approach, and ignored v3 (no E-numbering, no coverage table, fewer queries than run 2). For reference only: 9 found, 4 partial, 3 missed (P02, P03, P14 missing).

**Lesson:** run each check in a **new chat**. Earlier results in the chat make the agent shortcut. Added a "treat this as a fresh review" rule to the prompt.

---

# Run 4 score (Oct 13, 2026, new chat, prompt v3): best run

**Result: 13 found, 3 partly found, 0 missed. 11 findings, 0 false positives. No changes made.** (Run 1: 11 / 2 / 3; run 2: 11 / 4 / 1.)

| ID | Run 4 | Note |
|---|---|---|
| P01 | Found | F04, F01 |
| P02 | Found | F03: customer table also stores aggregated price, newsletter, event, page-view values |
| P03 | Partial | Printed LifetimePageViews 5,636,582 but never compared it with the detail (7,540,425); raised as a design question only |
| P04 | Partial | Said "the same 65 markets in every table": misleading, the 65 are spellings of 43 markets; no side-by-side values |
| P05 | Found | 18,853 web rows, 1,810 ad orders |
| P06 | Found | 1,250,205 distinct timestamps |
| P07 | Found | F05 |
| P08 | Partial | Hashes and ETL columns; not the other unneeded columns |
| P09 | Found | |
| P10 | Found | |
| P11 | Found | TicketPrice, Y/N, TRUE/FALSE |
| P12 | Found | |
| P13 | Found | From metadata; no filter-effect numbers this time (run 2 had 44,904) |
| P14 | **Found (first time)** | F08: expression with TODAY(), values 14-4,303 |
| P15 | Found | |
| P16 | Found | F11 |

**Still not followed:** E1-E10 numbering and the coverage table (second time). E3 (aliases side by side) and E4 (snapshot vs detail) were skipped, which explains the two partials.
**Minor inaccuracy:** IsEnterprise values listed as "FALSE, TRUE, blank" while the blank-flag count was 0.
**Timeouts:** the first four DAX queries ran concurrently and timed out; sequential retries with timeoutSeconds=200 worked. Warm up the model with one small query first.

---

# Run 5 score (Oct 13, 2026, new chat, skill v3): first run with the prompt actually delivered

First line was "Health check prompt v3 loaded."; E1-E10 numbered and completed; coverage table present and complete.

**Result: 16 found, 0 partial, 0 missed. 13 findings, 0 false positives. No changes made.**

| ID | Run 5 | Note |
|---|---|---|
| P01 | Found | Evidence E1 (long text keys) and checklist; not a row in the findings table |
| P02 | Found | F5 |
| P03 | Found | F2: LifetimePageViews 5,636,582 vs 7,613,993; NewsletterCount and EventCount also out of step |
| P04 | Found | F3: 65 spellings, about 50 entities (real: 43); lists aliases; Miami/South Florida left as a decision |
| P05 | Found | F1: 18,853 and 1,810 |
| P06 | Found | F8, E7 |
| P07 | Found | F11 |
| P08 | Found | F8, E6, F13 |
| P09 | Found | F6 |
| P10 | Found | F6 |
| P11 | Found | F6, E9 |
| P12 | Found | F4 |
| P13 | Found | F7, E10 |
| P14 | Found | F9 |
| P15 | Found | F10, F12 |
| P16 | Found | F10 |

**Small gaps:** text keys missing from the findings table; page-view gap overstated because orphan web rows are included in the detail total; report is very long (add a short summary at the top).
**Connect:** the first ConnectFabric calls timed out twice while the sign-in was pending; they worked after the sign-in completed.