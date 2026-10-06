# Plan Contract And Lowering

Use this capsule for relational-to-executor lowering, shared plan definitions,
serialization, or generated plan contracts. Revalidate the landmarks and selected
execution path in the active checkout.

## Starting Path

1. Planner `QueryExecutionNode#prepare` calls planner-interface
   `OperatorNodeHelper#createOperatorTree`.
2. `OperatorNodeHelper#getOperatorNode` dispatches over relational node types
   into `AbstractOperatorNode` objects, wrapped in `QueryPlan`.
3. Planner `ExecutionNode#serializeQueryPlan` selects Java serialization or
   binary Thrift; `QueryExecutionNode#execute` also has query-shape-specific
   routing. Follow the actual branch, including deferred parameter binding.

Repo-relative entry files:

- `components/planner/src/main/java/io/e6x/sql/QueryExecutionNode.java`
- `components/planner/src/main/java/io/e6x/sql/ExecutionNode.java`
- `shared/planner-interface/src/main/java/io/e6x/sql/plan/QueryPlan.java`
- `shared/planner-interface/src/main/java/io/e6x/sql/plan/operators/OperatorNodeHelper.java`

## Schema And Identity Boundaries

Follow the same values across `RelDataType`, operator `RowInfo`, wire fields, and
consumer schemas. Check field order, input ordinals, type/nullability, and numeric
precision/scale where they are transformed. Preserve fields used by expressions
and residual predicates even when they are absent from the final projection.

Not every dependency is a tree child. `E6TempTableScan` reaches its definition
through `E6TempTable#getOptimizedWithNode`; lowering wraps it in
`TempSinkOperatorNode`, whose definition has a separate child accessor. Inspect
these edges when visiting, rewriting, estimating, hashing, or serializing a
shared plan; following only ordinary inputs can miss the definition.

Distinguish a definition's identity from each reference's output schema and
parent. Java `ExecutionOperatorBuilderV2` and native `convert_to_physical_plan`
reuse temp definitions by name. If an encoding emits a definition once, verify
name/ID scope, consumer lookup and construction order, repeated references, and
reset between plans. Do not infer a safe sharing protocol from equal plan text.

## Representation And Generation Boundaries

`QueryPlan` has Java object serialization for the Java executor and `toThrift`
conversion into `TQueryPlan` for the native executor. The language-neutral
operator union and query metadata begin in
`shared/planner-interface/src/main/resources/e6_operators.thrift`; sibling IDLs
supply expressions, fields, functions, types, and service contracts.

Identify the affected representations and operator variants. Check value/type
preservation, optional-field defaults, union dispatch, and compatibility of
existing field numbers. Check cached or mixed-version consumption when the plan
can outlive the producing process; one representation does not prove the other.

Trace the changed IDL through its actual generator, Java/Rust outputs, build
manifests, and consumers. Verify that generation covers the changed module and
that consumers compile or load that output. A nearby generation script or one
regenerated language does not prove complete coverage; generated class bodies
are not the owning contract.

## Consumer Proof

Follow the affected variants to:

- Java: `QueryExecutorServiceImpl#executeQuery` and
  `ExecutionOperatorBuilderV2#createOperatorTree`
- Native: Thrift decoding and `convert_to_physical_plan`
- Planner: serialization selection, execution routing, and result schema

Compilation proves less than consumer acceptance, and acceptance proves less
than correct results. Validate the changed contract at its producer and consumer
boundaries, with execution evidence when the claim depends on it. Expand into
sibling `shared/workspace-services-thrift` or `shared/services-thrift` only when
the changed IDL/build edge reaches them.
