# Effective State And Build Boundaries

Use this capsule when configuration capture, cached planning, generated inputs,
or artifact resolution can explain a difference between source and behavior.
Revalidate the named mechanisms and build edges in the active checkout.

## State Ownership And Capture

Useful starting points:

- Planner `Env` and `MutableEnv.INSTANCE`: distinguish startup values, mutable
  reads, and snapshots captured by a consumer.
- `E6PlannerContext#configureCalciteForkBridges`: installs a process-wide
  `CalciteForkSettings.Provider`. Inspect the bridge and fork's read sites when
  deciding which planner context supplies metadata or settings.
- `E6SqlValidatorImpl` and `E6SqlToRelConverter`: mutable CTE/view, recursion,
  hint, temporary-table, and filter state; inspect reuse and reset boundaries.
- `QueryExecutionNode#prepare` calls `OperatorNodeHelper#setRollupEnabled` and
  `#setDecimal128Enabled`; those helper settings are static. Trace read/capture
  timing and concurrent planning when these settings affect lowering.
- Parameterized/cached planning: optimization may be deferred until binding or
  a stored `RelNode` rebound into another cluster. Follow the active planner,
  metadata provider, and context, not just the stored tree.

For the affected value, identify its owner and lifetime, write/read/capture sites,
cache key and invalidation, rebinding/reset, and concurrent users. A changed
configuration value does not prove existing plans or consumers recaptured it;
a copied or cached node does not prove its derived metadata remains valid.
Query-id cleanup belongs in
[executor-consumers-lifecycle.md](executor-consumers-lifecycle.md).

## Source To Consumer

| Component identity | Current locator | Build boundary |
| --- | --- | --- |
| Planner service and QO | `components/planner` | Root Maven reactor |
| Planner contract/lowering | `shared/planner-interface` | Root Maven reactor |
| Workspace service IDL | `shared/workspace-services-thrift` | Root Maven reactor |
| Shared service IDL | `shared/services-thrift` | Root Maven reactor |
| Java executor | `components/executor` | Root Maven reactor |
| Native executor | `components/native-executor` | Cargo workspace/component |
| Calcite framework fork | `shared/e6-calcite` | Independent Git submodule and Gradle-published Maven artifacts |

The monorepo owns migrated components and integrated verification; Calcite keeps
its independent history at the submodule pin. Prefer integrated Make targets.
The root Maven reactor consumes published `io.e6x.calcite` artifacts rather than
building Calcite as a reactor module. Verify effective resolution and the loaded
artifact where needed; a checkout or dependency declaration alone is insufficient.
For deliberately separate producer/consumer task worktrees, use a task-specific
local artifact version and verify that exact version in the consumer.

Parser generation combines Calcite resources with planner overlays. Trace the
actual generation/build inputs if parser source and behavior disagree. For
Thrift contracts and Java/Rust outputs, use
[plan-contract-lowering.md](plan-contract-lowering.md) rather than duplicating
the contract audit here.
