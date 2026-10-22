# Problem packet and output contract

Use this reference to validate a planning request and to make the two outputs concrete. It is an implementation aid, not a runtime schema, authorization record, or observed evidence.

## Minimum problem packet

A usable packet identifies the following. Use explicit `draft assumption` or `blocker` values for unknown facts; do not infer a missing value.

| Packet area | Required planning content | Why it is needed |
| --- | --- | --- |
| Identity | Problem ID, source revision or date, requester, accountable owner or owner blocker | Trace the proposal and prevent anonymous configuration. |
| Bounded job | Purpose, included task, exclusions, intended downstream consumer, harm-sensitive context | Define what belongs in the contract. |
| Execution shape | Response-only, fixed workflow, or reason a bounded adaptive choice is needed | Select the smallest inspectable runtime shape. |
| Caller input | Each task-data field: name, type, requiredness, validation, and invalid-input outcome | Define what a caller may submit. |
| Trusted dependencies | Each identity, scope, deadline, authority, or policy fact: name, type, trusted source, lifecycle, and boundary | Keep authority outside caller and model data. |
| Context and evidence | Approved inputs, source status or limitations, and untrusted-content treatment | Separate material to assess from operating rules. |
| Capabilities | Desired identities, narrow purposes, effect class, owners, review owners when shared, and explicit exclusions | Start from no optional capability. |
| Bounds | Request, model, capability-call, time, and cost limits where applicable; unit, enforcement point, and stop behavior | Make a finite run enforceable. |
| Outcomes | Required fields and caller handling for `complete`, `needs_information`, `declined`, and `failed`; any extension | Prevent a success-only interface. |
| Instructions | Task and scope, evidence/decision rule, uncertainty behavior, output guidance, instruction-revision intent | Make behavior reviewable without confusing it with control. |
| Change and evidence | Changed claim, candidate version intent, planned cases, and known open questions | Connect a proposal to later evaluation without inventing observations. |

Return `needs_information` for a packet that lacks a bounded purpose, caller/output relationship, owner status, or enough information to distinguish task data from trusted authority. Record an unresolved budget, model policy, capability identity, output schema, risk reference, governance tier, or execution class as a construction blocker, not as a runtime default.

## Agent contract output

Produce a single reviewable draft with the following sections. A project may choose the artifact format and location, but each field must remain identifiable.

| Contract section | Required content |
| --- | --- |
| Identity and status | Contract ID, draft status, agent version state, source packet reference, accountable owner, review owner, purpose, and non-goals. |
| Anatomy and boundaries | Model, instructions, context, runtime control, run state, output boundary, optional-component status, and shared executable-capability owners. |
| Typed input interface | Caller task-data fields and validation rules; separately, trusted dependencies with types, provenance, lifecycle, and prohibited untrusted sources. |
| Runtime shape | Fixed path or finite adaptive actions; observations, transitions, validation/admission point, stop conditions, resource limits, and terminal paths. |
| Configuration | Execution class, governance/risk references, model policy, instruction identity, output-schema identity, source policy, desired capability list, effective-admission rule, and explicit exclusions. |
| Output interface | Output fields/schema, all terminal outcomes, bounded content, caller handling, and receiving-boundary validation rule. |
| Instruction design | Stable operating instructions plus distinct request, evidence/task-data, trusted-runtime-fact, and proposed-response roles; revision ID and exemplar checks. |
| External startup manifest | Preconditions, emitting boundary, immutable identity, required resolved identities/digests, record locations, secrecy exclusion, and change rules. |
| Failure and change handling | Fail-closed construction conditions, admitted-operation unavailable behavior, no-substitution rule, material-change identity rule, and evaluation handoff. |
| Assumptions, blockers, handoffs | Explicit draft assumptions, questions, blocked dependencies, and canonical-owner handoffs. |

## Implementation acceptance criteria output

Create a separately titled criteria list. Every criterion must contain:

- **ID:** a stable local label such as `AC-CONSTRUCT-01`;
- **contract trace:** section and requirement group it demonstrates;
- **condition:** a setup or input that can be recreated;
- **expected behavior:** accepted result, rejected construction, or declared terminal outcome;
- **verification:** artifact inspection, deterministic check, or test observation to collect later; and
- **evidence status:** `planned` until a real observation is recorded.

Use one criterion per observable claim. Do not collapse schema validation, source support, authorization, and external-effect claims into a single passing result. Include an explicit negative criterion for each declared boundary or default-free construction field.

## Role and authority matrix

| Material | May influence | Must not become |
| --- | --- | --- |
| Caller request | Task selection and answer content within scope | Identity, permission, capability membership, policy, or budget. |
| Evidence or retrieved content | Support or qualify an answer | Operating instructions, authority, or an admitted capability. |
| Trusted runtime fact | Protected-boundary context within its declared type | A reason to rewrite reviewed configuration. |
| Model proposal | Candidate answer, clarification, terminal status, or finite action request | Authorization, dispatch receipt, external effect, or configuration update. |
| External startup manifest | Identifier for an assembled configuration | Approval, trust verdict, source truth, or operational-success proof. |

## Stop and escalation rule

When the packet implies a new trust boundary, external interface, evaluation claim, durability need, or lifecycle operation, keep the contract draft scoped to its planning facts. Name the missing owner and block that later decision. Do not compensate by expanding prompts, capabilities, or retries.
