---
name: calcite-query-support-check
description: Use when the question is whether a SQL shape works in current Calcite, which stage fails first, or whether a query likely needs Babel, conformance, or other context before any implementation work begins.
---

# Calcite Query Support Check

Classify current Calcite support before turning a query into feature work or a
bug.

## Core Rules

- Decide support status stage by stage: parser, validator, sql2rel,
  planner, and other directly relevant stages.
- Stop after the verdict unless the user explicitly asks to continue into
  implementation or diagnosis.
- Treat external engines as evidence about compatibility expectations, not as
  automatic proof that Calcite is wrong.

## Bring

- Exact SQL text
- Expected outcome
- Relevant context: dialect, Babel, conformance, fun, operator table,
  parser settings, planner settings, or runtime path

## Workflow

1. Inspect current code, tests, and docs before assuming behavior.
2. Identify the first likely failing stage and the nearest existing test or
   fixture that exercises the same area.
3. Report one of:
   - supported now
   - unsupported by design or current scope
   - unsupported but plausibly implementable
   - ambiguous and needs research or policy discussion
4. If the query is part of a larger batch, update the active issue brief or
   recommend creating one through `calcite-pr-intake`.
5. Recommend the next path only when needed:
   - support verdict only -> stop
   - behavior looks wrong -> `calcite-bug-root-cause`
   - missing callable surface or syntax -> `calcite-function-or-operator-work`
   - planner-owned problem -> `calcite-optimization-or-rule-work`

## Required Outputs

- Stage-by-stage support verdict
- First failing stage
- Support classification
- Nearest existing test or harness suggestion
- Recommended next step, if any
