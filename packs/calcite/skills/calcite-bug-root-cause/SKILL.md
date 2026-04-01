---
name: calcite-bug-root-cause
description: Use when current Calcite behavior looks wrong or regressed and the first job is to prove the owning layer, find the real fix point, reject symptom patches, and map affected surfaces before coding.
---

# Calcite Bug Root Cause

Prove the owner and the source-level fix before writing the patch.

## Core Rules

- No fix without root cause.
- Name the invariant that current behavior violates.
- Reject symptom-patch alternatives explicitly.
- Inventory affected surfaces sharing the same mechanism before implementing.

## Bring

- Exact or near-exact repro
- Expected versus actual behavior
- Relevant context: dialect, conformance, Babel, parser settings,
  planner/runtime path, stack trace, or failing test

## Workflow

1. Inspect current code, tests, and docs nearest to the repro.
2. Reduce to the smallest trustworthy repro.
3. Identify the primary owner: parser, validator, sql2rel or decorrelator,
   planner or rule, runtime, or still unknown.
4. State the violated invariant and the likely source-level fix point.
5. Enumerate rejected alternatives that would only patch the symptom.
6. Build or update the issue brief, including:
   - owner hypothesis
   - chosen fix point
   - explicit non-goals
   - adjacent surfaces sharing the same mechanism
7. Before calling diagnosis complete, pair with `calcite-change-impact-map`
   for the changed mechanism and validation surface.

## Required Outputs

- Minimized repro
- Owning-layer classification
- Root cause
- Rejected symptom-patch alternatives
- Chosen fix point
- Affected-surface inventory
- Targeted validation scope
