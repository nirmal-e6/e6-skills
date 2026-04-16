---
name: calcite-pr-intake
description: Use when one or more Calcite SQL symptoms, failing queries, missing syntax/support requests, or reviewer-found inconsistencies need to be classified, split into PR-sized candidates, and turned into durable issue briefs before coding.
---

# Calcite PR Intake

Turn raw Calcite symptoms into candidate records, split decisions, and issue
briefs before implementation starts.

## Core Rules

- One candidate equals one invariant or policy question and one primary owning
  layer.
- Do not mix a clear bug fix with a semantics debate or explicit engine-target
  compatibility work in one PR.
- Treat external engines as evidence, not as default oracles. If engines
  disagree, stop and split the candidate into bug, compatibility, or
  discussion work.
- Issue briefs are shared multi-agent artifacts. Preserve existing entries and
  append timestamped coordination notes when another agent may resume the work.
  Record active claims for files or surfaces when work is split across agents.

## Bring

- Exact SQL, failing test, stack trace, reviewer comment, or plan.
- Expected versus actual behavior.
- Any context that can change behavior: dialect, Babel, conformance,
  parser/operator-table choices, planner settings, or runtime path.
- Lists are allowed; decompose them first.

## Workflow

1. Normalize the prompt into numbered candidates.
2. Classify each candidate as exactly one of:
   - support check
   - confirmed bug
   - feature or compatibility work
   - research or discussion item
   - external-engine-bug evidence
3. Name the primary owner: parser, validator, sql2rel or decorrelator,
   planner or rules, runtime, or unknown yet.
4. Record the split decision and explicit non-goals.
5. Gather minimum repo evidence:
   - first failing stage
   - nearest working examples
   - closest existing tests and fixtures
   - likely affected surfaces sharing the same mechanism
6. Create or update an issue brief in
   `$HOME/.e6/skills/artifacts/calcite/issue-briefs/`
   using
   `$HOME/.e6/skills/e6-skills/shared/templates/calcite/ISSUE-BRIEF-TEMPLATE.md`.
   If the brief already exists, re-read the latest file, update it in place,
   and append a coordination-log entry instead of overwriting another agent's
   notes.
   Derive and record:
   - candidate slug
   - default branch kind: `fix`, unless the work is explicitly exploratory
   - suggested final branch name: `<kind>/<candidate-slug>`
7. Recommend the next path:
   - confirmed bug -> `systematic-debugging`, then `test-driven-development`
   - support check only -> stop after verdict
   - feature or compatibility work -> design only after the target policy is explicit
   - research or discussion item -> no code yet

## Calcite Quick Map

- Parser admission: `core/src/main/codegen/templates/Parser.jj`
- Validator and name resolution:
  `core/src/main/java/org/apache/calcite/sql/validate/`
- SQL-to-Rel and decorrelation:
  `core/src/main/java/org/apache/calcite/sql2rel/`
- Planner and rules:
  `core/src/main/java/org/apache/calcite/plan/`,
  `core/src/main/java/org/apache/calcite/rel/rules/`
- Primary tests:
  `SqlValidatorTest`, `SqlToRelConverterTest`, `RelOptRulesTest`,
  parser tests, and nearby `iq` or XML expectation fixtures

## Required Outputs

- Candidate queue with one row per candidate
- Classification and owner hypothesis for each row
- Explicit split decisions and non-goals
- Issue brief paths
- Recommended branch slug and branch name per implementation candidate
- Recommended next skill or process per candidate
