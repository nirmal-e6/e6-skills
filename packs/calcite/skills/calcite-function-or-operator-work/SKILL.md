---
name: calcite-function-or-operator-work
description: Use when the task is adding, changing, or auditing a Calcite function, operator, callable SQL surface, or closely related syntax and you need the semantic contract, ownership, gating, and focused tests before implementation.
---

# Calcite Function Or Operator Work

Define the contract and extension point before editing code.

## Core Rules

- Decide whether the work is a bug fix, new surface, compatibility target, or
  discussion item before implementation.
- Be explicit about legal and illegal forms, type behavior, null behavior, and
  conformance or dialect gating.
- Keep the implementation shape as narrow as the contract allows.

## Bring

- Target SQL examples
- Expected semantics
- Illegal forms and expected errors
- Type or null behavior expectations
- Dialect or conformance scope

## Workflow

1. Inspect current code, tests, and docs for similar operators or syntax.
2. Classify the work:
   - existing behavior is wrong
   - new callable surface
   - compatibility work for a named engine or dialect
   - ambiguous semantics needing discussion first
3. Identify the owning layers and extension points.
4. Record gating notes: dialect, Babel, conformance, operator table, or other
   relevant switches.
5. Update the issue brief with the semantic contract, ownership decision, and
   non-goals.
6. Before implementation, pair with `calcite-change-impact-map` to identify
   sibling operators, parallel syntax, and preserved invariants.

## Required Outputs

- Feature classification
- Semantic contract
- Owning layers and extension point
- Gating or compatibility notes
- Implement-now versus research-first decision
- Focused tests and validation
