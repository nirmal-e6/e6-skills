# State, Generation, Topology, And Evidence

Use this capsule when behavior depends on mutable/global state, cached or
generated representations, split/monorepo location, volatile facts, sensitive
evidence, or promotion of a newly learned rule.

## State And Generation Edges

The following relationships were observed in current code. Recheck the named
symbols and effective modes before applying them.

- Planner `Env` supplies startup configuration while `MutableEnv.INSTANCE`
  carries runtime-updatable state. A changed value does not prove that an
  existing consumer recaptured it.
- Fork `CalciteForkSettings.Provider` is process-global and is installed by
  planner `E6PlannerContext#configureCalciteForkBridges`.
- `E6SqlValidatorImpl` and `E6SqlToRelConverter` keep mutable CTE/view,
  recursion, hint, temporary-table, and filter state. Reset boundaries are
  semantic boundaries.
- Parameterized and cached planning can defer optimization/lowering or rebind a
  stored relational value into a current cluster. A cached `RelNode` is not
  automatically context free.
- `QueryExecutionNode#prepare` has set process-static lowering flags on
  `OperatorNodeHelper`; concurrent planning and capture time therefore require
  explicit scrutiny.
- Planner and executors maintain query-id keyed contexts with distinct
  cancellation, clear, close, and memory lifecycles.
- Parser generation combines resources from the Calcite artifact with planner
  overlays. Thrift generation connects IDL, scripts, checked-in Java/Rust
  output, and both executor consumers.

For any mutable or generated feature, trace declaration, mutation, capture,
propagation, cache/rebind, reset, concurrency, generated output, serialization,
consumer, and cleanup only where the current mechanism uses those edges.

## Logical Topology

| Component identity | Authoritative split locator | Monorepo correspondence |
| --- | --- | --- |
| Planner service and QO | `e6-query-optimizer` | `components/planner` |
| Planner contract/lowering | `e6-planner-interface` | `shared/planner-interface` |
| Java executor | `e6-executor` | `components/executor` |
| Native executor | `e6-native-executor` | `components/native-executor` |
| Calcite framework fork | `e6-calcite` | External artifact dependency |

These are discovery identities, not file-equivalence claims. Split repositories
remain authoritative until the user explicitly declares cutover. After cutover,
revalidate the table rather than preserving the old authority as doctrine.

Use artifact/crate identity, entry symbols, and contract names to follow a
component across layouts. Treat source present in both layouts as potentially
divergent until exact files and manifests prove otherwise.

## Evidence Boundaries

- **Durable:** reviewed semantic invariants, ownership tests, stable logical
  identities, and revalidation rules.
- **Volatile:** branch/PR state, CI, artifact versions, effective flags, current
  defaults, timings, test counts, services, and source-authority status.
- **Sensitive/raw:** customer SQL, logs, CSVs, full plans, credentials, private
  threads, and incident attachments.
- **Derived:** a sanitized mechanism reproducer or generalized lesson that does
  not disclose raw data or volatile identifiers.

Keep sensitive/raw evidence at user-designated local intake locators. Store only
locators and handling classifications in working output; never copy raw material
into this repository, implementation repositories, or shared durable artifacts.
Volatile evidence must include when and where it was observed and what would
invalidate it.

## Learning Promotion

Solve novel work with current code and native reasoning first. Promote a lesson
only after recurrence across independent tasks or a clearly reusable invariant,
review for sensitivity and staleness, and an explicit revalidation trigger.
Prefer improving an existing capsule over adding a skill or catalog. Keep
rejected hypotheses visible in local working evidence, not as durable facts.
