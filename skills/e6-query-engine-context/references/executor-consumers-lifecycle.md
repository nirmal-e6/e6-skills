# Executor Consumers And Lifecycle

Use this capsule for plan ingestion, physical construction, query state, results,
cancellation, or Java/native capability differences. Revalidate the selected
query shape and runtime mode before making support or parity claims.

## Starting Landmarks

### Java executor

- `components/executor/src/main/java/io/e6x/server/QueryExecutorServiceImpl.java`
  (`executeQuery`) reads Java-serialized `QueryPlan` bytes.
- `components/executor/src/main/java/io/e6x/sql/plan/pipelined/ExecutionOperatorBuilderV2.java`
  (`createOperatorTree`) builds Java operators from planner-interface nodes.
- `components/executor/src/main/java/io/e6x/engine/pipelined/PipelinedExecutor.java`
  owns pipeline execution and chunk production.
- `QueryContextCache`, `QueryContext`, and service maps hold query-id keyed
  state, permits, memory, and captured configuration.

### Native executor

- `components/native-executor/src/thrift_server.rs` decodes `TQueryPlan`.
- `components/native-executor/e6-physical-plan/src/plan_conversion.rs`
  (`convert_to_physical_plan`) constructs DataFusion physical plans.
- `components/native-executor/src/query_executor/` owns query execution and
  `QueryContext`, including result channels, cancellation, timeout, memory,
  and plan/analyze state.

## Capability And Routing

Trace the selected executor and query-shape branch through decoding, operator
construction, expression/type support, execution, and result delivery. Preparing
a query does not prove it can be lowered or executed. Accepting an operator does
not prove every type or mode it can carry is supported. Inspect current handlers
and fallback/selection inputs instead of maintaining a static capability list.

Compare the last correct producer representation with the consumer's inputs and
interpretation. A runtime symptom does not establish executor ownership; a plan
that looks unchanged can still have different fields or captured configuration.
Distinguish an explicit unsupported branch from an untested path.

## Lifecycle Boundaries

For changed state, trace:

1. Creation, configuration capture, registration, and lookup ownership
2. Completion, timeout, cancellation, retry, and partial failure
3. Result-store/stream ownership transfer, state removal, and resource release
4. Cache/global-state reuse, reset, and concurrent access

Planner and executors have distinct query contexts. Follow the affected remote
call and error path when a handoff changes; success-path cleanup alone does not
establish the lifecycle contract.

## Validation Shape

Check bytes/fields and the affected consumer first. Compare Java/native results
where they promise the same semantics; exercise cancellation or failure when
state ownership changes. Keep untested modes and runtime-state assumptions
explicit rather than claiming parity from compilation or one successful route.
