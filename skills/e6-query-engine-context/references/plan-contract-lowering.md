# Plan Contract And Lowering

Use this capsule when a Calcite `RelNode`, executor-facing plan, serialization
format, generated source, or downstream plan consumer is in scope.

All relationships below were observed in current code when this map was built;
revalidate symbols and representations in the active checkout.

## Observed Lowering Path

1. Planner `QueryExecutionNode#prepare` invokes planner-interface
   `OperatorNodeHelper#createOperatorTree`.
2. `OperatorNodeHelper#getOperatorNode` dispatches over relational node types
   and creates executor-facing `AbstractOperatorNode` objects.
3. The root is wrapped in planner-interface `QueryPlan`; it is no longer a
   Calcite `RelNode`.
4. Planner `ExecutionNode#serializeQueryPlan` chooses Java serialization or
   binary Thrift. `QueryExecutionNode#execute` has query-shape-specific routing,
   including a Thrift path for DML.

Start with these repo-relative landmarks:

- `e6-query-optimizer/src/main/java/io/e6x/sql/QueryExecutionNode.java`
- `e6-query-optimizer/src/main/java/io/e6x/sql/ExecutionNode.java`
- `e6-planner-interface/src/main/java/io/e6x/sql/plan/QueryPlan.java`
- `e6-planner-interface/src/main/java/io/e6x/sql/plan/operators/OperatorNodeHelper.java`

## Dual Contract

`QueryPlan` participates in two representations:

- Java object serialization consumed by the Java executor
- `toThrift` conversion into `TQueryPlan` consumed by the native executor

The language-neutral contract begins in
`e6-planner-interface/src/main/resources/e6_operators.thrift`, where
`TOperatorNode` selects operator variants and `TQueryPlan` carries the root and
query metadata. Sibling IDLs define expressions, fields, functions, types, and
the executor service.

A field or operator change is incomplete until both representations, union
membership, numbering/compatibility, and consumers have been checked.

## Generated-Source Boundary

Treat IDL, generation scripts, checked-in Java/Rust outputs, build manifests,
and consuming code as one dependency edge. Do not review generated class bodies
as the source of truth. At map time, `e6-planner-interface/generate.sh` did not
prove regeneration coverage for every checked-in module; inspect the current
script and generated markers rather than inheriting that observation.

## Consumer Audit

Follow only variants touched by the change:

- Java: `QueryExecutorServiceImpl#executeQuery` to
  `ExecutionOperatorBuilderV2#createOperatorTree`
- Native: Thrift deserialization to `convert_to_physical_plan`
- Planner: creation, serialization choice, query-shape routing, and result path
- Mixed-version or cached-plan behavior when the contract can outlive a process

Compile or source generation alone does not prove downstream consumption.
Choose validation along the artifact graph: source contract, generated outputs,
publication/resolution if applicable, each changed consumer, then risk-shaped
integration behavior.

## Topology Boundary

Logical planner-interface identity is stable across `e6-planner-interface` and
`e6-query-engine/shared/planner-interface`. Split repositories remain
authoritative until the user declares cutover. Compare exact IDL, scripts,
manifests, and generated outputs before treating the monorepo copy as equivalent.
