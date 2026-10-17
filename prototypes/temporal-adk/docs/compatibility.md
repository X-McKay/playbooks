# Compatibility findings

## Pinned ADK contract

The first native run uses ADK 2.12.0 and its public time, ID and random provider
seams. The complete dependency graph is in `../uv.lock`.

A regression test exposed that `exclude_unset=True` silently loses session
`events` appended in place to a default list. The codec therefore retains all
field values plus recursive field-set metadata. The metadata preserves explicit
null versus absent fields. Binary continuation fields are encoded losslessly.
The codec excludes ADK-declared nonserialized execution objects such as
`tools_dict`; registry identity must independently bind their semantics.

ADK emits an experimental function-schema warning. The tests exercise that
version-specific declaration path; the warning is not suppressed.

## Official integration reuse assessment

Inspected temporalio/ai-integrations commit
`78e845a9e379ac18b4b69593d62b5dc3873700ab`.
The model wrapper requires Workflow context for Activity dispatch and falls back
to ordinary execution outside it. ToolContextSnapshot is a one-way read-only
contract. This prototype follows those contracts; it does not import the
Workflow-bound wrappers or claim upstream owns remote reconstruction.

The official schema preparation handles response-schema types. This initial
profile rejects those types and dynamic schemas rather than copying that broader
adapter. No upstream source is vendored. A future dispatch-seam contribution
can reuse the conformance corpus without making delivery depend on acceptance.

## Deployment target

The requested integration environment is a dedicated kind cluster running
Temporal and OpenShell. Its CNI must actually enforce ingress and egress
NetworkPolicy. Local ADK tests do not establish Kubernetes or sandbox behavior.
