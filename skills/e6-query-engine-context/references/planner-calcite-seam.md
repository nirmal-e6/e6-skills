# Planner And Calcite Seam

Use this capsule for planner ingress, Calcite/QO ownership, or fork-boundary
questions. It is a selective discovery map, not an architecture contract.

## Evidence Labels

- **Observed:** directly visible in the named current source or build file.
- **Inference:** supported by observed facts but not declared as a contract.
- **Hypothesis:** a starting claim that current code must confirm or reject.

Recheck every landmark in the active checkout before relying on it.

## Observed Landmarks

- Planner ingress and query lifetime: `e6-query-optimizer/` symbols
  `QueryEngineServiceGrpcImpl#prepareStatementV2`, `#executeStatementV0`,
  `#clearState`, and `QueryPlanningTask#call`.
- Parse through relational optimization: `QueryOptimizer#parseX`, `#parse`,
  `#tryParse`; `CostBasedOptimizer#getValidatedAndConvertedRelNode` and
  `#getOptimizedRelNode`; `E6RelNodeOptimizer#buildOptimizerPrograms`.
- Product dependency: the planner and planner-interface build files select
  `io.e6x.calcite:calcite-core` and guard against accidental upstream Calcite
  artifacts. Verify the current coordinates and enforcement blocks.
- Fork publication: `e6-calcite/build.gradle.kts` can publish the fork under an
  E6 group while retaining `org.apache.calcite.*` packages.
- Product-to-fork bridge: fork `CalciteForkSettings.Provider` and planner
  `E6PlannerContext#configureCalciteForkBridges` connect Calcite mechanisms to
  product flags, metadata, guardrails, and policy.

## Ownership Test

Ask at behavior and API granularity:

1. Must the invariant hold inside generic Calcite parsing, validation,
   relational representation, or planning?
2. Is a narrow Calcite extension point or fork seam required?
3. Is the behavior instead E6 policy, rule ordering, metadata/auth integration,
   fallback choice, or executor-aware planning?
4. Which downstream contract would allow a product bridge to be deleted?

A generic Calcite invariant points toward the fork or upstream comparison. E6
policy and orchestration point toward the product planner. Prefixes, packages,
stack frames, and external-engine behavior are evidence, never verdicts.

## Topology Boundary

Logical planner identity is stable across `e6-query-optimizer` and
`e6-query-engine/components/planner`. The monorepo copy is a locator, not proof
of authority or equivalence. Split repositories remain authoritative until the
user explicitly declares cutover; compare exact files and dependency manifests
before using a monorepo fact.

An upstream or personal Calcite checkout is comparison evidence unless the
product build proves it is the consumed artifact.

## Revalidate Before Concluding

- Effective parser, validator, planner, fallback, cache, and rule modes
- Resolved Calcite artifact and provider initialization
- First incorrect SQL, Rel, or plan representation
- Whether a fork seam is necessary or merely convenient
- Split/monorepo source authority for every touched component
