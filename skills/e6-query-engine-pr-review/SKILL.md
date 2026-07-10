---
name: e6-query-engine-pr-review
description: Use when reviewing one or more existing E6 query-engine PRs or diffs whose correctness depends on semantics, owning-layer choice, cross-component contracts, or merge and dependency order.
---

# E6 Query Engine PR Review

Review one coherent existing change set, even when it spans repositories or
multiple PRs.

## Ownership

This skill owns correctness review: source-state limits, intended invariant,
behavior-level ownership, changed-contract consumers, semantic fallout,
risk-shaped tests, correction rechecks, and residual risk.

It does not own future Calcite candidate intake, the worker's Calcite handoff,
implementation, or delivery coordination. Review is non-mutating with respect
to the reviewed deliverable and external PR state. It may use clearly isolated,
disposable tests, instrumentation, or code changes solely to prove or disprove a
finding. Discard that evidence experiment; persisting a fix, modifying the
reviewed change, posting, approving, or merging requires separate authorization.

## Required Context And Evidence

- Exact PRs/diffs, base/head or equivalent source state, and unavailable evidence
- Intended invariant, scope, non-goals, and claimed validation
- Logical components and current source-of-truth status
- Relevant modes, flags, fallbacks, artifacts, and compatibility constraints
- Prior findings or corrections that require rechecking

## Workflow

1. Verify the change set and source state. State any freshness or access limit
   before drawing conclusions.
2. Express the change as one semantic contract and identify its behavior-level
   owner. Compare it with the strongest fair existing Calcite, QO, interface,
   or executor mechanism before accepting new machinery.
3. Follow the changed contract through producers, sibling paths, artifacts,
   serialization, generated sources, state capture/reset, and runtime consumers.
   Use `e6-query-engine-context` only for edges the diff actually reaches.
4. Test preserved invariants across relevant flags, fallbacks, executor modes,
   cached paths, and cross-PR merge/dependency order.
5. Judge validation by risk and first affected surface; compile success or one
   passing layer does not prove downstream consumption.
6. When read-only evidence is insufficient, record the setup and result of a
   clearly isolated disposable experiment without changing the review target.
7. Lead with severity-ordered findings. Give evidence, semantic consequence,
   and a direct correction or verification ask for each.
8. Recheck corrections against the original finding and dependent surfaces,
   then state contradictions, deferred questions, and residual risk.

## Output And Stop Contract

Return findings first, then source-state limits, open questions, validation gaps,
and residual risk. If there are no findings, say so and name what remains
untested or unavailable. Stop after the review report unless implementation or
external review actions were separately requested.

## Composition Boundaries

- Compose with `e6-query-engine-context` for bounded cross-component discovery.
- Add Calcite root-cause, function/operator, optimization/rule, or impact-map
  lenses only when the reviewed mechanism is proven to be Calcite-owned.
- Do not substitute `calcite-pr-intake` for an existing change review or
  `calcite-pr-handoff` for reviewing someone else's coherent E6 change set.
- A multi-PR review remains review; use E6 coordination only when the requested
  outcome is delivery reconciliation against a terminal state.
