# Executor Consumers And Lifecycle

Use this capsule for Java/native plan ingestion, physical construction,
per-query state, results, cancellation, clear/close behavior, or capability
differences. Revalidate current code and runtime modes before making parity or
ownership claims.

## Observed Consumer Boundaries

### Java executor

- `e6-executor/src/main/java/io/e6x/server/QueryExecutorServiceImpl.java`
  (`executeQuery`) deserializes Java bytes into `QueryPlan`.
- `e6-executor/src/main/java/io/e6x/sql/plan/pipelined/ExecutionOperatorBuilderV2.java`
  (`createOperatorTree`) recursively maps planner-interface nodes into Java operators.
- `e6-executor/src/main/java/io/e6x/engine/pipelined/PipelinedExecutor.java`
  owns pipeline execution and chunk production.
- Service maps, `QueryContextCache`, and `QueryContext` hold query-id keyed
  state, memory, task permits, and effective environment snapshots.

### Native executor

- `e6-native-executor/src/thrift_server.rs` deserializes `TQueryPlan`.
- `e6-physical-plan/src/plan_conversion.rs#convert_to_physical_plan` maps the
  operator union into a DataFusion physical plan.
- `query_executor` creates per-query state, optionally optimizes/pipelines the
  physical plan, executes a stream, and hands batches to the service layer.
- Native `QueryContext` owns result channels, cancellation, timeout, memory,
  and plan/analyze lifecycle state.

These are logical entry points. Confirm package paths and signatures in the
active split repository or corresponding monorepo component.

## Lifecycle Questions

For a changed state or execution path, trace:

1. Creation and the flags/configuration captured at creation time
2. Registration by query id and every lookup owner
3. Normal completion, timeout, cancellation, retry, and partial failure
4. Result-store or stream handoff before state removal
5. `clear`, `close`, cache eviction, and memory/reference release ordering
6. Reuse, reset, and concurrency behavior for process-global or cached state

Planner, Java executor, and native executor maintain different query state.
A cleanup fix is not complete until the producer, remote call, consumer, and
retry/error paths agree on lifecycle semantics.

## Capability And Routing Boundaries

Capability is query-shape and mode dependent, not a deployment-wide Boolean.
Observed examples include a DML Thrift route and an optional two-pass INSERT
path that can use different executors. Public native service methods have also
had explicit gaps. Treat all such details as volatile: inspect the current
service handler, cluster/executor selection inputs, and fallback path.

Do not infer executor ownership merely because the final symptom appears at
runtime. Compare the last correct serialized plan with the first incorrect
consumer interpretation.

## Validation Shape

- Prove plan bytes/fields at the consumer boundary when serialization is in scope.
- Exercise only affected operator variants and modes first.
- Compare Java and native behavior when their contract should match.
- Test cancellation/clear/close and failure paths when state ownership changes.
- Record unsupported or untested capabilities as residual risk, not parity.

## Topology Boundary

Logical identities map from `e6-executor` to
`e6-query-engine/components/executor` and from `e6-native-executor` to
`e6-query-engine/components/native-executor`. Split repositories remain
authoritative until the user declares cutover; paired files may differ, so
revalidate exact symbols and manifests before using a monorepo copy.
