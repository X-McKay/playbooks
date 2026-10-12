# 10. Security and governance

This chapter is for developers who own a multi-agent system. Everything in the
[single-agent security chapter](../advanced/03-security-and-governance.md)
still applies to every member; this chapter adds what you design, evidence,
and get signed off once agents work together. The core idea: no agent is
trusted merely because it belongs to the same system or was selected by
another agent.

## Governance inheritance

Every member keeps its single-agent
governance tier, execution class, risk assessment, owners, controls, and
approval requirements. The system adds its own composition assessment and
governance decision on top.

The system governance tier is the highest of:

1. the maximum inherent system-level scenario tier;
2. the tier of every reachable member in its assigned use;
3. applicable legal, regulatory, contractual, or internal-policy floors; and
4. capability floors created by the combined system.

Composition controls may make launch acceptable, but they do not silently lower
the assurance required by the underlying use or member capability. The
[system risk assessment](13-system-risk-assessment.md) is where you work this
out.

## Ownership

In addition to the
[member ownership the single-agent guidance requires](../core/12-production-readiness.md#ownership),
your System Spec names:

- accountable product and business owners;
- system engineering and operational owners;
- security, privacy, legal, compliance, and domain reviewers as applicable;
- owners for every member, role, edge, registry, policy, and state store; and
- an incident commander and a risk-acceptance authority.

Member owners remain accountable for their agent contracts. System owners are
accountable for admission, integration behavior, end-to-end outcomes, and
composition risk. Responsibility MUST NOT disappear between those layers.

## Trust model

Treat each of these as a separate trust boundary:

- user and external input;
- the deterministic orchestrator and policy control plane;
- each member agent and model provider;
- every interaction and transport;
- tool, MCP, retrieval, and external-service boundaries;
- the registry, marketplace, package, and deployment supply chain;
- workflow, queue, event bus, blackboard, memory, and artifact stores;
- human approval and operational interfaces; and
- telemetry, evaluation, and audit systems.

Crossing a boundary requires authenticated identity, explicit authorization,
typed validation, data policy, integrity protection where needed, and
correlated evidence.

## Threat model

Your system threat model includes each member's
[single-agent threat model](../advanced/03-security-and-governance.md#threat-model)
and adds the threats that only exist between agents. At minimum, assess:

- direct and indirect prompt injection across agent boundaries;
- identity, instruction, evidence, approval, and authority laundering;
- confused-deputy use of a more privileged member;
- unauthorized member, role, edge, tenant, or data access;
- excessive agency through recursive or dynamically created work;
- shared-memory, blackboard, registry, bid, or artifact poisoning;
- false consensus, collusion, reviewer capture, and correlated failure;
- malicious or compromised member substitution;
- schema confusion, result forgery, replay, and duplicate delivery;
- race conditions, stale policy, inconsistent graph, and time-of-check/use
  gaps;
- data aggregation that creates a more sensitive derived dataset;
- denial-of-wallet, queue starvation, event storms, and resource exhaustion;
- hidden or duplicated side effects across concurrent branches;
- kill-switch, audit, telemetry, or evidence-store failure; and
- supply-chain compromise of agents, models, skills, tools, policies, or
  schemas.

Link each threat to concrete scenarios; preventive, detective, and recovery
controls; tests and adversarial evals; and indicators, alerts, and runbooks.

## Identity and authorization

The members' rules for
[identity and authorization](../core/09-tools.md#identity-and-authorization)
apply at every hop. Composition adds one more rule: authority can only shrink
as it moves.

Authenticated actor, tenant, environment, and purpose originate outside model
control. They propagate through typed trusted context, not prompts or
agent-generated messages. Every interaction re-evaluates authorization using
the [authority-attenuation](05-delegation-and-interactions.md#authority-attenuation)
rule: a caller can delegate only a subset of its current delegable scope, and
a callee can exercise only the intersection with its own role and Agent Spec.

Members MUST NOT:

- assert or change actor or tenant identity;
- grant roles, scopes, membership, or approval;
- forward bearer credentials by default;
- treat another agent's assertion as authorization evidence;
- use a broader service identity when an attenuated identity is available; or
- persist delegated authority beyond its task and expiry.

Enforce authorization at the member boundary and again at every tool or
external resource.

## Inter-agent content

The single-agent guidance already treats
[tool results and retrieved content as untrusted](../core/09-tools.md#untrusted-content).
Extend that to other agents: all agent-generated content is untrusted.
Summarization, voting, review, or agreement does not make content trusted.

Design your message types so receivers can tell apart:

- data from instructions;
- claims from verified evidence;
- proposed actions from completed effects;
- agent identity labels from authenticated principals;
- recommendations from policy decisions; and
- review results from human approval.

Use typed fields and evidence references. Sanitize or isolate untrusted
active content, but do not rely on prompt wording alone to prevent injection.

## Dynamic admission

If members are picked at run time, use an authenticated registry and a
deterministic admission policy. Before work begins, validate:

- member identity, owner, package or endpoint, and integrity;
- agent and manifest version;
- contract, schema, protocol, and runtime compatibility;
- execution class, governance tier, risk status, and evidence freshness;
- skills, tools, credentials, network, and data-access ceilings;
- jurisdiction, residency, provider, and tenant constraints;
- current health, quarantine, revocation, and incident status; and
- cost, latency, and capacity claims against trusted measurements.

Model-generated descriptions, bids, self-attestations, and discovery metadata
are inputs to selection, not admission evidence.

The run manifest records the decision and evidence digest. Admission expires:
long-lived systems revalidate members at policy-defined boundaries without
changing in-flight behavior nondeterministically.

## Registries, marketplaces, and supply chain

Registries and marketplaces are privileged infrastructure. They require:

- authenticated publishers and controlled write access;
- immutable versions and integrity metadata;
- provenance, ownership, review, and revocation status;
- compatibility and policy metadata;
- audit records for publication and change; and
- availability, rollback, and compromise runbooks.

Production systems SHOULD use allowlisted publishers, repositories, packages,
providers, and manifests. Pin dependencies and scan packages, images, skills,
tools, policies, schemas, and generated artifacts.

A compromised registry MUST NOT automatically alter active workflow behavior.
Your quarantine and revocation policy defines whether to stop, isolate,
substitute, or finish already admitted work.

## Shared state and memory

Each shared memory, blackboard, event store, and artifact store
declares:

- record schemas and provenance;
- authorized readers and writers;
- tenant and purpose binding;
- consistency and conflict semantics;
- integrity, version, and freshness checks;
- moderation or validation before promotion to accepted state;
- retention, deletion, residency, and backup; and
- poisoning detection, quarantine, and recovery.

Separate proposed, observed, verified, accepted, rejected, and superseded
facts. Agents MUST NOT overwrite provenance or promote their own claims to
verified state without the declared validation path.

Derived collections can be more sensitive than their inputs. Classification
and access policy consider aggregation, inference, linkage, and
re-identification.

## Protocol and transport security

Interaction transports provide appropriate confidentiality, integrity, peer
authentication, replay protection, message size limits, timeouts, and
denial-of-service controls.

Messages include stable system, graph, delegation, schema, actor, tenant,
deadline, and policy context. Receivers reject stale, duplicate, malformed,
wrong-tenant, wrong-graph, or unauthorized messages before model execution.

Async and event-driven systems define delivery and settlement semantics. A
transport acknowledgement is not evidence that business work or an external
effect completed.

## Isolation

Apply the [member isolation controls](../advanced/03-security-and-governance.md#isolation),
then isolate members from each other. Use process, container, sandbox,
account, network, task-queue, namespace, and data-store isolation proportionate
to risk. Separate agents with different owners, tenants, credentials,
untrusted code, or consequential capabilities.

A coordinator SHOULD NOT share its broad environment, filesystem, credentials,
or network access with specialists. Code-executing and externally supplied
members require strong sandboxing, resource limits, restricted egress, and
artifact inspection.

Keep the control plane isolated from member work. Agents cannot edit their
System Spec, policies, limits, registry status, telemetry requirements, or kill
switches.

## Approval and separation of duties

Consequential action uses the single-agent
[human approval](../advanced/01-durable-execution.md#human-approval)
contract and also records the system and causal context. Approval interfaces
show the final action, arguments, actor, tenant, relevant evidence, material
disagreement, system and member identities, policy version, expiry, and
expected side effects.

Agent consensus, a reviewer role, quorum, reputation, or marketplace selection
is not approval. An agent MUST NOT approve its own output, accept its own risk,
or suppress information required by the approver.

High-risk systems SHOULD separate system development, registry publication,
policy approval, production promotion, and residual-risk acceptance roles.

## Change classes

Classify each change with the single-agent
[change classes](../advanced/03-security-and-governance.md#change-classes).
In a multi-agent system, treat these as behavioral or security changes that
need focused review:

- member addition, removal, upgrade, restriction, or substitution;
- topology, routing, aggregation, recursion, or dynamic-admission changes;
- interaction schema, authority, data-flow, retry, or timeout changes;
- new shared state, registry, transport, model, tool, skill, or data source;
- increased fan-out, depth, autonomy, duration, population, or transaction
  value;
- approval, termination, quarantine, kill-switch, or fallback changes; and
- telemetry, audit, retention, or redaction changes.

Material changes require a system version change, a regenerated manifest,
appropriate member and system evals, replay review, risk reassessment, and
rollout and rollback plans.

## Deployment

Follow the member deployment progression in the
[single-agent guidance](../advanced/03-security-and-governance.md). For the
system, production deployments SHOULD use immutable images and read-only
application filesystems; pinned manifests, policies, schemas, models, and
dependencies; separate identities and least-privilege credentials by role;
restricted network egress and approved service endpoints; encrypted transport
and managed secrets; signed or otherwise integrity-protected release artifacts
where appropriate; staged rollout by tenant, task class, graph profile, or
traffic percentage; and fast rollback to a known composition manifest.

Dynamic admission expands runtime choice but does not replace controlled
system deployment. The admission envelope itself is versioned and released.

## Kill switches and quarantine

Each member already has
[kill switches](../core/12-production-readiness.md#kill-switches).
The system adds controls to:

- stop new system runs;
- stop new delegation or dynamic admission;
- disable one member, role, edge, model, tool, registry, or topology profile;
- cancel or pause active workflows;
- block consequential actions while preserving read-only investigation;
- revoke credentials and artifact access; and
- enter a tested deterministic or human-operated fallback.

Kill switches operate outside model control, propagate within a stated SLO,
are tested regularly, and produce audit evidence.

Quarantine prevents new work and defines treatment of active work, cached
results, shared-state contributions, approvals, and artifacts from the affected
member. Removing a member from discovery is not sufficient containment.

## Incident response

Use the single-agent
[incident runbook sequence](../advanced/03-security-and-governance.md)
and add system runbooks for:

- unauthorized member, edge, scope, tenant, or data flow;
- prompt-injection propagation or shared-state poisoning;
- registry, member, provider, or supply-chain compromise;
- false consensus or reviewer failure;
- runaway recursion, events, retries, queues, or spend;
- duplicate or unapproved side effects;
- stuck workflows, inconsistent graph, or failed cancellation; and
- audit, telemetry, approval, or artifact-store failure.

Preserve workflow history, run manifests, graph versions, the interaction
ledger, audit records, policy decisions, evidence hashes, model and member
versions, and affected artifacts, subject to privacy and legal requirements.

Incidents and near misses create regression cases and may trigger member
quarantine, system rollback, risk reassessment, control testing, and
affected-party notification.

## Exceptions and review

Record exceptions as the
[single-agent guidance](../advanced/03-security-and-governance.md) describes,
naming scope, rationale, compensating controls, evidence, accountable owner,
approver, start, expiry, monitoring, and rollback trigger. Exceptions MUST NOT
be granted by an agent or hidden in prompts, registry metadata, or routing
code.

Review the system at least as frequently as required by its governance tier
and after material architecture, membership, capability, data, jurisdiction,
incident, or control-effectiveness changes.

## Decommissioning

Retire each member as the single-agent guidance describes. Decommissioning the system
also includes:

- preventing new runs, admission, and delegation;
- completing, cancelling, migrating, or compensating active workflows;
- revoking member, registry, model, tool, and artifact credentials;
- removing queue subscriptions, events, schedules, callbacks, and endpoints;
- retiring manifests, policies, approvals, caches, shared state, and
  artifacts;
- applying retention and deletion obligations;
- preserving required audit and incident evidence; and
- updating discovery, ownership, runbooks, and dependent systems.

## Common pitfalls

- **Trusting teammates.** A message from another member was treated as
  instructions or as proof of authority because it came from inside the
  system.
- **Counting agreement as approval.** A quorum or reviewer agent signed off a
  consequential action that needed a human.
- **Delisting instead of quarantining.** The member was removed from discovery
  but kept finishing work and writing to shared state.
- **Trusting the acknowledgement.** A queue confirmed delivery, and the system
  recorded the business effect as done.

## Before you move on

- [ ] The system governance tier is derived from members, scenarios, floors,
  and combined capability, and nothing lowered it.
- [ ] Every trust boundary is drawn, and every threat links to a test.
- [ ] Authority attenuates at every edge, and identity never travels in
  prompts.
- [ ] System kill switches and quarantine are tested and produce evidence.
- [ ] Owners and the risk-acceptance authority are named and have signed off.
