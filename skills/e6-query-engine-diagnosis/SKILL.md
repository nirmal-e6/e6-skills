---
name: e6-query-engine-diagnosis
description: Use when an E6 query, plan, prepare path, build, or runtime behavior is wrong, surprising, regressed, or insufficiently explained and the owning stage or mechanism is not yet proven.
---

# E6 Query Engine Diagnosis

Find the first incorrect representation and prove the behavior-level owner
before choosing a fix.

## Ownership

This skill owns unknown or cross-engine symptoms through stage localization,
mechanism-faithful reproduction, owner and fix-point proof, rejected hypotheses,
consumer impact, and dependency-shaped validation.

It does not own implementation, review, performance design after ownership is
settled, or a Calcite-only support/root-cause task whose boundary is already
proved.

## Required Context And Evidence

- Expected versus actual behavior and the narrowest trustworthy symptom
- Current source authority and path: ingress, prepare, execute, or result
- Effective dialect, modes, flags, cache/fallback state, and executor route
- Source database type and available transformation evidence when intake SQL
  is not directly E6-compatible
- Sensitive/raw evidence locators and handling limits, without copied contents
- Existing repros, plans, errors, tests, and disproved hypotheses

Raw customer SQL, logs, CSVs, full plans, credentials, and incident attachments
must remain at user-designated local intake locators. Never copy them into this
repository, implementation repositories, or shared durable artifacts.

## Workflow

1. Classify evidence as sensitive, volatile, or safe-derived. Preserve local
   locators and produce only the smallest sanitized mechanism reproducer.
2. Trace the first incorrect boundary: ingress, parse, validate, SQL-to-Rel,
   optimization, lowering, serialization, executor interpretation, runtime
   state, result production, or an external dependency.
3. Reproduce the mechanism, not merely similar SQL. Preserve the decisive
   identity, type/coercion, gate, cache, fallback, query shape, or runtime mode.
4. If source-dialect SQL cannot execute directly, use the supplied database type
   and transformation evidence to derive the smallest semantically equivalent
   E6-compatible reproducer. Record the source database type and transformation
   assumptions. Treat the transformation as an owning boundary only when
   evidence shows it is wrong.
5. Compare the last correct producer representation with the first incorrect
   consumer. State owner confidence and evidence that would move ownership.
6. Name the violated invariant, root cause, and source-level fix point when
   proved. Record rejected hypotheses and why symptom patches or broad toggles
   fail the contract.
7. Follow only affected consumers and select validation along their dependency
   graph, including alternate modes and lifecycle paths when relevant.
8. If the request is a support check only, stop at the stage-by-stage verdict
   and nearest evidence; do not manufacture implementation work.

## Output And Stop Contract

Return evidence handling, sanitized repro, first failing stage, owner and
confidence, invariant/root cause or current limit, rejected hypotheses,
affected consumers, validation evidence, residual risk, and the next route.
Stop when the requested verdict or fix-point proof is reached.

## Composition Boundaries

- Compose with `e6-query-engine-context` for bounded producer/consumer discovery.
- Use `calcite-query-support-check` as primary for a current-Calcite verdict
  only. Add `calcite-bug-root-cause` after mechanism evidence places the defect
  in Calcite; then use other Calcite lenses only for their proven mechanisms.
- Unknown-owner bad plans stay in diagnosis. Move to
  `e6-query-engine-optimization` only after the observable problem, semantic
  invariant, phase, and candidate owner are established.
