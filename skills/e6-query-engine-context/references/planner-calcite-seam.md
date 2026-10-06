# Planner And Calcite Seam

Use this capsule for planner ingress, Calcite/QO ownership, or fork-boundary
questions. Revalidate these starting landmarks in the active checkout.

## Starting Landmarks

- Planner ingress and query lifetime in `components/planner`:
  `QueryEngineServiceGrpcImpl#prepareStatementV2`, `#executeStatementV0`,
  `#clearState`, and `QueryPlanningTask#call`.
- Parse through relational optimization: `QueryOptimizer#parseX`, `#parse`,
  `#tryParse`; `CostBasedOptimizer#getValidatedAndConvertedRelNode` and
  `#getOptimizedRelNode`; `E6RelNodeOptimizer#buildOptimizerPrograms`.
- Planner and planner-interface POMs: Calcite coordinates and enforcement against
  accidental upstream artifacts. Package names do not identify the loaded JAR.
- Product-to-fork bridge: planner
  `E6PlannerContext#configureCalciteForkBridges` and fork
  `CalciteForkSettings.Provider` connect framework behavior to product settings,
  metadata, and policy. Inspect both sides when that seam is reached.

## Ownership Test

Ask at behavior and API granularity:

1. Must the invariant hold inside generic Calcite parsing, validation,
   relational representation, or planning?
2. Does an existing extension point satisfy it, or is a fork change necessary?
3. Is the behavior E6 policy, program order, metadata/auth integration,
   fallback choice, or executor-aware planning?
4. Which consumer or framework contract would let a product bridge be removed?

A generic framework invariant points toward Calcite; product policy and
orchestration point toward the E6 planner. Prefixes, packages, stack frames, and
external-engine behavior are evidence, never ownership verdicts.

Trace the executing program, registration and gating before attributing behavior
to a rule. For metadata-dependent behavior, follow the provider and planner
context used by that invocation. A registered rule or configured provider does
not prove it was used by the failing path. Leave optimization design to the
primary optimization skill.

## Source And Artifact Boundary

Calcite source and commits belong to the independent `shared/e6-calcite`
submodule. Product planning and integrated consumer verification belong to the
query-engine worktree. Trace the pinned source through the root Make build and
resolved Maven artifact; neither a source edit nor a pin update proves the
planner loaded it. See [state-generation-topology.md](state-generation-topology.md)
when resolution or configuration capture is the uncertainty.
