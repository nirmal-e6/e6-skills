---
name: e6-query-engine-optimization
description: Use when an E6 bad plan, performance opportunity, planner enhancement, or optimization design may span Calcite, query-optimizer policy, plan contracts, or executor capabilities.
---

# E6 Query Engine Optimization

Choose the strongest safe optimization mechanism, including no new code.

## Ownership

This skill owns investigation and design after the observable problem and
candidate planning boundary are evidenced. It covers the semantic invariant,
strongest fair baseline, phase and owner, executor-aware benefit, alternatives,
interactions, and risk-shaped proof.

It does not own unknown-stage diagnosis, review of an existing change set,
generic Calcite rule work, or implementation before the contract is accepted.

## Required Context And Evidence

- Observable current behavior and desired improvement, with a trustworthy baseline
- Semantic invariant and query/data shapes that must preserve results
- Current planner modes, flags, traits, costing assumptions, and fallback paths
- Candidate phase and owner with supporting and disconfirming evidence
- Planner-interface and executor capabilities that determine real benefit

## Workflow

1. State the measurable or observable problem separately from the proposed
   mechanism. A smaller plan alone is not a semantic invariant or product win.
2. Define preserved semantics: multiplicity, null extension, ordering, identity,
   field mapping, evaluation domain, liveness, and other relevant obligations.
3. Establish the strongest fair current baseline across existing Calcite rules,
   QO programs/policy, flags, metadata, cost models, and supported modes. Distinguish
   illegal plans, reduction/phase-ordering gaps, missing exploration candidates,
   bad estimates, and selection errors. Check supported enumerators before
   adding a selection heuristic.
4. Identify the owning phase and behavior-level owner. For a new rule or
   heuristic, compare broader mechanisms in current upstream code, established
   databases, and primary research; explain why the strongest alternatives
   apply or fail. A sound narrow matcher alone does not justify new machinery.
   Prefer a small extension at the owner, existing utilities, and clear inline
   logic. Justify new abstractions and flags; remove unnecessary scaffolding.
5. Prove executor-aware benefit through the plan contract and actual consumer
   capabilities; do not optimize a representation the selected executor cannot
   exploit. Keep comparisons within the existing cost contract, currently
   row-count-based in E6. Additional cost dimensions require deliberate design.
6. Audit overlap, termination, rule order, traits, costing, repeated tree or
   metadata work, caches, fallbacks, serialization, generated contracts,
   concurrency, and alternate executors only where the mechanism can interact
   with them.
7. Select risk-shaped evidence: focused semantic negatives, plan differences,
   mode comparisons, consumer checks, and performance evidence appropriate to
   the claim.

## Output And Stop Contract

Return the problem, invariant, strongest baseline, phase/owner decision,
alternatives, executor-visible benefit, interaction risks, evidence plan,
residual risk, and one decision: use existing mechanism, no code change,
implement, refine, or escalate. Stop before implementation unless requested.

## Composition Boundaries

- Use `e6-query-engine-diagnosis` first when the initial wrong representation or
  owner is unknown.
- Compose with `e6-query-engine-context` for bounded planner-contract and
  executor-consumer discovery.
- Compose with `calcite-optimization-or-rule-work` only when current evidence
  establishes Calcite planner ownership. Product QO policy does not become a
  Calcite task merely because it operates on Calcite relational nodes.
