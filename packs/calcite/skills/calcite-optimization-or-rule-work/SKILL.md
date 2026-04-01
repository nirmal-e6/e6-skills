---
name: calcite-optimization-or-rule-work
description: Use when the task is a Calcite planner transformation, rule-placement decision, or planner-owned bad-plan investigation and you need the preserved invariant, ownership, interaction risks, and focused tests before implementation.
---

# Calcite Optimization Or Rule Work

Define the planner contract before changing a rule or planner-owned behavior.

## Core Rules

- Use only when planner ownership is already in scope or can be justified
  quickly from evidence.
- State the preserved semantic invariant before proposing a transform.
- Audit overlap, termination, and interaction risks with nearby rules.

## Bring

- Current versus desired plan behavior
- Preserved semantic invariant
- Reproducer query or plan
- Relevant planner settings, traits, or cost assumptions

## Workflow

1. Inspect current planner code, tests, XML goldens, and nearby rules.
2. Identify the owning planner layer or rule family.
3. Define the transformation contract:
   - preconditions
   - preserved semantics
   - expected new plan shape or behavior
4. Enumerate direct interaction risks with nearby rules, traits, or costing
   assumptions.
5. Update the issue brief with the planner contract, risks, and explicit
   non-goals.
6. Pair with `calcite-change-impact-map` before implementation to catch
   sibling rules and dependent plan-output surfaces.

## Required Outputs

- Transformation contract
- Owning planner or rule layer
- Overlap or interaction risk notes
- Implement versus refine versus escalate decision
- Focused positive and negative tests
