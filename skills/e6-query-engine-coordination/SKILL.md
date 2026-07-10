---
name: e6-query-engine-coordination
description: Use when one coherent E6 query-engine outcome spans dependent workstreams, components, repositories, or sessions and needs explicit reconciliation against a terminal state.
---

# E6 Query Engine Coordination

Keep one outcome coherent across dependent technical work without replacing the
workflows that own each decision.

## Ownership

This skill owns E6-specific large-outcome judgment: terminal state and non-goals,
fresh behavior-unit inventory, bounded workstreams, ownership/dependency mapping,
parent reconciliation, dependency gates, contradictions, residual risk, and
evidence-pack closeout.

It does not own technical diagnosis, optimization, review, generic planning,
version-control operations, or native coordination mechanics. Size alone is not
a trigger; dependent work and reconciliation are required.

## Required Context And Evidence

- Observable terminal state, non-goals, and allowed mutation scope
- Fresh inventory of behavior units, not a historical example list
- Logical component authority and split/monorepo source status
- Dependency, artifact, consumer, and validation relationships
- Current dispositions, claims, contradictions, and unavailable evidence

## Workflow

1. Define the terminal state as observable behavior and evidence. Separate
   non-goals and decisions that require user authority.
2. Reinventory the current system into behavior units. Historical lists and
   named files are seeds, never proof of complete scope.
3. Build the ownership/dependency map: source owner, consumer, artifact edge,
   prerequisite, validation gate, and explicit disposition.
4. Partition only bounded workstreams with clear inputs, outputs, mutation
   boundaries, and independent verification. Keep cross-component invariants
   and final reconciliation at the parent.
5. Reconcile returned evidence against current source and the canonical
   inventory. Resolve overlaps, gaps, stale assumptions, and contradictory
   claims before accepting progress.
6. Validate in dependency order: producer contract, generated/published
   artifact, direct consumers, runtime behavior, then broader regression only
   when risk justifies it.
7. Close with an evidence pack covering terminal criteria, dispositions,
   commands/results, contradictions, deferred work, and residual risk.

Use available native coordination only as execution support. Do not explain its
mechanics, prescribe fixed worker counts, or create a goal without the user's
explicit request.

## Output And Stop Contract

Return the terminal contract, fresh inventory, bounded workstreams,
ownership/dependency map, reconciled dispositions, gate evidence,
contradictions, deferred items, and residual risk. Stop only when terminal
criteria are evidenced or a specific decision/authority gap blocks progress.

## Composition Boundaries

- Compose with `e6-query-engine-context` for bounded shared context.
- Let E6 review, diagnosis, optimization, native reasoning, and proven Calcite
  lenses own their technical workstreams; coordination owns reconciliation.
- A multi-PR review remains `e6-query-engine-pr-review` unless delivery across
  dependent workstreams and sessions is itself the requested outcome.
- A narrow or merely large task stays with native reasoning and ordinary
  execution rather than this skill.
