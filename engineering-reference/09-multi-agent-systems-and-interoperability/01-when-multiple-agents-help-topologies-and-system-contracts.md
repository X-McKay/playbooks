# 9.1 When Multiple Agents Help, Topologies, and System Contracts

**Status:** 0.5.0 first draft
**Audience:** System designers, accountable owners, evaluators, and operators of multi-agent systems.
**Applicability:** Applies when two or more independently contracted, model-driven agents coordinate toward one application outcome. It does not apply merely because one agent calls deterministic code, a conventional service, or a tool. A single agent with bounded parallel work should use [Part 6](../06-reasoning-and-execution-patterns/README.md) instead.

[Part 9 overview](README.md) · [Applicability and conformance](../../applicability.md) · [9.2 Delegation, Handoffs, and Agent-to-Agent Interfaces](02-delegation-handoffs-and-agent-to-agent-interfaces.md) · [9.3 Coordination, System Evaluation, and Operations](03-coordination-system-evaluation-and-operations.md)

## Purpose and applicability

Adding agents changes the unit being designed and released. A system is no longer only an agent with more prompts. It is a versioned composition of members, roles, interaction edges, shared controls, and a final outcome. Each member still has to satisfy its own [agent contract](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). The composition adds risks that member-level review cannot establish: an unexpected member can join, a valid member can receive work through the wrong edge, nested work can exceed the real budget, or a coordinator can leave work with no terminal owner.

Use composition only when its added boundaries serve a material goal. Useful reasons include isolating a sensitive capability, separating context that should not be broadly shared, obtaining an independently tested check, parallelizing genuinely independent work, or assigning separately governed responsibilities. A role label or a simulated organization chart is not a reason. A deterministic service or ordinary tool remains a component of an agent, not a second agent.

Treat the choice as a design and risk decision, not as a way to make a system appear more capable. This is consistent with the NIST AI RMF’s voluntary framing of trustworthiness considerations across the design, development, use, and evaluation of AI systems.[1]

## Working model

A **member** is one independently contracted model-driven component. A **role** is the narrower responsibility that member has in this particular system. The same member may fill more than one role only when the System Spec says so and the resulting loss of separation is evaluated. A reviewer role, for example, does not become independent simply because it has a different name; shared instructions, evidence, models, or ownership can make its failures correlated.

The **system** is the versioned composition. Its deterministic orchestrator owns coordination state and accepts or rejects proposed state changes. A model-driven coordinator may recommend an allowlisted route or synthesize bounded results, but it is not the source of policy, approval, final truth, or termination. Inter-agent messages, retrieval output, and shared memory remain untrusted data. The detailed interaction envelope, identity, data boundaries, and attenuated authority rules belong to [Chapter 9.2](02-delegation-handoffs-and-agent-to-agent-interfaces.md); system-wide coordination evidence and operations belong to [Chapter 9.3](03-coordination-system-evaluation-and-operations.md).

A System Spec describes the intended composition. Resolving it produces a **composition manifest**: the immutable identity of what the system actually assembled for a release or run. It records the pinned member manifests and roles, allowed graph, topology and policy versions, effective limits, and the relevant system version. This gives an evaluator or incident reviewer a subject to examine without copying member contracts into a second, drifting specification.

## Decisions and best practices

### Start with the least complex workable shape

First compare three designs against the same outcome and hard constraints:

- **One agent** is the default when one bounded contract, context policy, and capability set can meet the need.
- **Ordinary orchestration** is appropriate when steps are known and deterministic code can invoke a single agent, tools, or conventional services in a fixed flow. Parallel calls do not by themselves make it multi-agent composition.
- **A multi-agent system** is appropriate only when separately contracted model-driven members and their controlled interactions add a benefit that the simpler alternatives cannot provide.

Write down the simpler baseline, the claimed benefit, how the benefit can be disproved, and the owner and review date. A higher average answer-quality result does not justify a composition that breaks a security, latency, reliability, cost, or other declared hard gate. If the claimed benefit is not demonstrated, simplify or record a governed exception rather than treating more components as automatic progress.

### Select a topology by control burden

Use a deterministic pipeline when stages and transitions are known. A model-selected supervisor and bounded workers may be warranted when interpretation determines which of a small set of stable specialists should act. Bounded fan-out and gather fit work that is genuinely independent, provided result ordering, duplicate handling, partial failure, and merge rules are explicit. A producer and reviewer arrangement can add useful behavioral evidence, but its reviewer cannot authorize an action or accept residual risk.

Handoffs, shared state, recursive task trees, meshes, and dynamic membership impose progressively stronger demands for state ownership, containment, reproducibility, and termination. They are not maturity levels. Prefer the least dynamic topology that meets the documented benefit. If a topology combines profiles, calculate depth, fan-out, retries, concurrency, and budgets across the whole graph rather than granting each branch a separate ceiling.

Static membership is the useful default. Discovery through a registry, network endpoint, user input, or integration does not admit a member. Dynamic membership can be justified by a real need for variable expertise, locality, availability, or capacity, but it must remain inside a reviewed static control envelope. That envelope defines trusted sources, compatible roles and versions, permitted edges, data boundaries, authority ceilings, resource limits, terminal conditions, and the evidence to retain. The actual admitted graph then becomes part of the run record.

### Make the contract establish system truth

A compact System Spec identifies the system purpose and version, accountable and operational owners, its multi-agent justification and baseline, topology, member-role assignments, allowed directed interactions, state ownership, root limits, and terminal outcomes. It references member contracts rather than reproducing their prompts, tools, or capabilities. It also identifies the relevant risk and evaluation policies, while the detailed risk method and release decision remain owned by Parts 10 and 4.

Every category of shared system state needs one deterministic owner. At minimum, name the authority for workflow and branch status, accepted evidence, conflict resolution, final outcome, budget accounting, and any externally visible effect. Shared transcripts are not canonical truth merely because several members can read them. If shared memory is used, specify writers, readers, record types, provenance, conflict handling, retention, and deletion; its detailed coordination controls are covered in Chapter 9.3.

The root limits are for the entire system run, not additional allowances per member. Bound agent runs, depth, parallelism, rounds, model and tool requests, input and output volume, time, and spend as applicable. The termination policy must make success, escalation, rejection, cancellation, failure, exhaustion, required-member failure, and late or conflicting results unambiguous. A system that cannot take an allowed next step must stop in a declared outcome; it must not continue by inventing a new member or route.

## Requirements

- **COMPOSE-01 — Admission decision.** When a proposed design has two or more model-driven agents contributing to one application outcome, the accountable owner **MUST** document the simpler baseline, the material benefit claimed for composition, the falsifiable measures or hard gates, and the decision owner and review date. The system **MUST NOT** be adopted solely to create personas, divide one prompt into roles, or conceal an oversized capability set.

- **COMPOSE-02 — System contract and identity.** A production multi-agent system **MUST** have a versioned System Spec and an immutable composition manifest that identify the system, owners, pinned member identities, role assignments, topology, allowed interactions, effective limits, state ownership, terminal outcomes, effective execution class, governance tier, and applicable policy and evidence identities. Its effective execution class and governance tier **MUST** meet the highest applicable member, interaction, capability, policy, and system-risk floors; composition **MUST NOT** lower either floor. The system contract **MUST NOT** copy or silently override a member’s canonical contract; member requirements remain independently applicable.

- **COMPOSE-03 — Governed topology.** A multi-agent system **MUST** declare an explicit allowlisted interaction graph and a deterministic orchestrator for system state, policy enforcement, and termination. A model-driven coordinator **MAY** propose a route within that graph, but **MUST NOT** create an edge, admit a member, enlarge authority, waive a limit, approve a consequential action, or commit an unvalidated state transition. Apply the detailed delegation and authority rules in Chapter 9.2.

- **COMPOSE-04 — Membership and roles.** Before a member receives production work, the system **MUST** validate its pinned contract or manifest, ownership, applicable assurance evidence, compatibility, and role restrictions. A role **MUST** only narrow a member’s effective capability; it **MUST NOT** grant a tool, data class, authorization scope, caller, or interaction mode that the member and current policy do not already permit. Unknown, unpinned, or user-supplied members **MUST** be denied. A system claiming independent review, voting, or defense in depth **MUST** document what is shared and assess relevant correlation in its risk and evaluation evidence.

- **COMPOSE-05 — Dynamic composition.** A system that admits members or constructs edges during a run **MUST** enforce a reviewed static control envelope and record each admitted member, version or manifest identity, assigned role, effective capability, policy decision, admission reason, and resulting graph. A discovered endpoint or capability **MUST NOT** be treated as permission to invoke it.

- **COMPOSE-06 — Bounds, state, and change.** A multi-agent system **MUST** declare and enforce one finite root budget and a termination policy across the complete delegation graph, including permitted retries. Member and interaction limits **MUST** subdivide that root budget rather than add new allowances. Each category of shared state **MUST** have one declared deterministic owner. A membership, role, interaction, topology, schema, limit, or state-ownership change **MUST** create a new system version and composition manifest and trigger the applicable evaluation, risk, compatibility, and rollout review.

## Worked example

The internal policy assistant answers questions from approved, current, permission-filtered documents and returns citations plus uncertainty. It has no external write capability. For the `travel-policy-current` fixture, the current approved policy permits a London hotel amount of GBP 220; a superseded document differs.

The initial design is one bounded agent with approved retrieval. Its baseline evaluation asks whether it selects the current, permitted source, gives GBP 220 with a supporting citation, and returns `needs_information` when a current permitted source is absent. The team considers a composition because it hypothesizes that separating evidence preparation from answer checking will catch stale-source and unsupported-claim failures without violating the same latency and cost gates. That is a hypothesis, not a measured benefit or a reason to release the composition before comparison evidence exists.

The candidate uses a fixed, sequential topology. A policy responder receives a question. An evidence-retriever returns only typed evidence references, document versions, effective dates, and retrieval uncertainty from the approved corpus. The responder produces a cited draft. An answer-checker receives the draft and evidence references and returns a bounded check result. The deterministic orchestrator verifies that the cited document is current and permitted, applies the checker outcome policy, and owns the terminal result. The checker may flag missing support or a stale source; it cannot decide that an unsupported answer is acceptable.

```yaml
# Illustrative System Spec excerpt; values are example controls, not live settings.
system: policy-answer-composition
version: 0.5.0-draft-example
owners:
  accountable: policy-assistant-owner
  operational: policy-assistant-operator
justification:
  baseline: policy-assistant-single-agent
  hypothesis: bounded evidence checking reduces stale-source failures
  decision_review: before-release

topology:
  profile: sequential-producer-and-checker
  membership: static
  orchestrator: deterministic-policy-orchestrator

members:
  - role: evidence-retriever
    member_manifest: policy-evidence-retriever-example
    restrictions: [approved-policy-retrieval]
  - role: policy-responder
    member_manifest: policy-responder-example
    restrictions: [cited-policy-answer]
  - role: answer-checker
    member_manifest: policy-answer-checker-example
    restrictions: [evidence-reference-review]

interactions:
  - id: collect-evidence
    from: deterministic-policy-orchestrator
    to: evidence-retriever
    input: PolicyQuestion
    output: EvidenceSet
  - id: check-draft
    from: deterministic-policy-orchestrator
    to: answer-checker
    input: CitedPolicyDraft
    output: CheckResult

limits:
  max_agent_runs: 3
  max_parallel_agents: 1
  max_rounds: 1
  max_model_requests: 6
  max_tool_calls: 4

termination:
  outcomes: [complete, needs_information, declined, failed, bounded_partial]
  on_unsupported_or_stale_citation: needs_information
```

A meaningful negative case lets the retriever surface the superseded document. The orchestrator must reject it as the final support because it is not current, regardless of how fluent the responder’s draft is. If the checker finds that no current citation supports the answer, the composition terminates with `needs_information` after its declared bounded correction path; it does not start an unbounded reviewer debate. The evaluation compares this candidate with the single-agent baseline on the same current, superseded, permission-denied, missing-evidence, and injected-content cases. It also records what the responder and checker share, so a passing check is not misrepresented as independent review.

This example stays ephemeral because it has no externally visible side effect. If a later variant can prepare or apply a policy update, the system’s effective execution class cannot silently remain ephemeral. It must add the durable execution, exact approval binding, and unknown-outcome handling required by Part 7.

## Evidence and checklist

Keep evidence proportionate to the topology, but make the system subject identifiable and testable:

- Keep the admission decision and its single-agent or deterministic baseline with the System Spec.
- Validate construction against pinned members, role restrictions, schema compatibility, declared edges, effective execution class and governance floor, root limits, and terminal outcomes. Fail closed on an invalid composition.
- Retain the composition manifest ID with evaluation records, traces, approvals when applicable, release records, and incident references.
- Test that undeclared edges, unknown or unpinned members, role-based capability expansion, empty effective capability, and over-limit dispatch are denied.
- Test topology-specific paths: partial and late results, duplicate branches, required-member failure, cancellation, exhaustion, and the declared final outcome. Chapter 9.3 specifies the integrated system evidence and operational interpretation.
- Reassess the composition when its membership, graph, policies, shared state, or effective capabilities change. A member update is a system behavior change even when the orchestration source is untouched.

Next, define the interaction envelopes and authority attenuation in [Chapter 9.2](02-delegation-handoffs-and-agent-to-agent-interfaces.md), then establish integrated coordination evidence and operations in [Chapter 9.3](03-coordination-system-evaluation-and-operations.md).

## References

[1]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"
