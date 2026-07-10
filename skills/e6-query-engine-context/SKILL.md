---
name: e6-query-engine-context
description: Use when an E6 query-engine task crosses component boundaries, depends on Calcite/QO ownership, or needs broader engine context than the current checkout provides.
---

# E6 Query Engine Context

Build only the context needed to reason about the current outcome.

## Ownership

This skill owns context discovery and boundary justification. It does not own
review, diagnosis, optimization, coordination, implementation, or a complete
engine architecture. Current code and repository instructions outrank these
references.

## Required Context

- Requested outcome and explicit non-goals
- Starting symbol, changed contract, failing representation, or artifact
- Current authoritative checkout and any mirror under consideration
- Observed edge that may require another component
- Known uncertainty, runtime mode, or source-state limit

## Workflow

1. Start at the current code nearest the task, not at a repository inventory.
2. Label each relationship as observed, inferred, or hypothetical. Keep owner
   hypotheses revisable.
3. Expand only along an observed producer/consumer, artifact, serialization,
   generated-source, state/lifecycle, or runtime edge.
4. Read only the relevant capsule:
   - Calcite and planner ownership: [planner-calcite-seam.md](references/planner-calcite-seam.md)
   - Plan contract or serialization: [plan-contract-lowering.md](references/plan-contract-lowering.md)
   - Java/native consumption or cleanup: [executor-consumers-lifecycle.md](references/executor-consumers-lifecycle.md)
   - Mutable state, generation, topology, or evidence handling:
     [state-generation-topology.md](references/state-generation-topology.md)
5. Inspect a counterpart repository or monorepo component only when the traced
   edge crosses into it. Revalidate the exact symbol and build relationship.
6. Stop expanding when the ownership and consumer boundary is supported by
   current evidence.

Full-engine reading is never an unconditional prerequisite.

## Output And Stop Contract

Return the bounded context, observed edge map, owner hypothesis with confidence,
references consulted, unresolved hypotheses, and facts needing revalidation.
Stop when the primary workflow has enough context; do not turn discovery into a
new workflow or architecture document.

## Composition Boundaries

- Compose as a secondary lens under E6 review, diagnosis, optimization, or
  coordination when those skills own the requested outcome.
- Add a Calcite skill only after current mechanism evidence puts Calcite in
  scope; package names and stack frames are not ownership proof.
- For a novel task with no clear specialized owner, use native reasoning and
  the smallest useful current-code context rather than forcing a workflow.
