---
name: calcite-change-impact-map
description: Use when a Calcite patch or proposed fix needs a generic completeness audit across changed mechanisms, sibling call sites, dependent surfaces, gates, and validations before the patch is called complete.
---

# Calcite Change Impact Map

Use a generic impact map instead of issue-shaped checklists.

## Core Rules

- Audit the changed contract or mechanism, not only the first failing example.
- Search for sibling call sites, duplicate logic, and parallel implementations
  before declaring a fix complete.
- Record what was inspected but intentionally left unchanged.

## Mandatory Map

For every non-trivial patch, answer all of these:

1. What contract or mechanism changed?
2. Where else is that mechanism used?
3. What repo-visible surfaces depend on it?
4. What gates or modes can change the result?
5. What invariants must remain unchanged?
6. What test surfaces represent the changed behavior?
7. What nearby surfaces were inspected and intentionally deferred?

## Workflow

1. Name the changed contract precisely: semantic rule, helper behavior,
   validation rule, transformation, naming rule, metadata shape, or plan rule.
2. Find all other uses of the same helper, sibling helpers, copy-pasted logic,
   and parallel code paths built on the same assumption.
3. Enumerate dependent surfaces that could observe the change:
   names, row types, errors, plans, trees, metadata, nullability, or other
   externally visible behavior as applicable.
4. Enumerate gates and modes:
   conformance, Babel, dialect or operator-table choice, planner settings,
   traits, feature flags, or runtime branches.
5. State preserved invariants explicitly.
6. Convert the map into targeted positive and negative validations.
7. Write the resulting map into the active issue brief or PR brief.

## Required Outputs

- One short impact-map section per candidate or patch
- Sibling or parallel code-path inventory
- Preserved-invariant list
- Targeted validation matrix
- Explicit inspected-but-deferred list
