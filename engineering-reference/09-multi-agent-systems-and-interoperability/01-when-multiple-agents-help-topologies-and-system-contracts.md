# 9.1 When Multiple Agents Help, Topologies, and System Contracts

**Status:** 0.5.0-draft.2 — draft
**Audience:** System designers, accountable owners, evaluators, and operators of multi-agent systems
**Applicability:** Applies when two or more independently contracted, model-driven agents work toward one application outcome. It does not apply when one agent calls deterministic code, a conventional service, or a tool. A single agent with bounded parallel work should use [Part 6](../06-reasoning-and-execution-patterns/README.md).

[Part 9 overview](README.md) · [Applicability and conformance](../../applicability.md) · [9.2 Delegation, Handoffs, and Agent-to-Agent Interfaces](02-delegation-handoffs-and-agent-to-agent-interfaces.md) · [9.3 Coordination, System Evaluation, and Operations](03-coordination-system-evaluation-and-operations.md)

## Purpose and applicability

Adding agents changes what you design and release. The system is a versioned composition of members, roles, interaction edges, shared controls, and a final outcome, not one agent with more prompts. Each member still needs its own [agent contract](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). Composition adds risks that member-level review cannot catch: an unexpected member can join, a valid member can receive work through the wrong edge, nested work can exceed the real budget, or a coordinator can leave work with no terminal owner.

Use composition only when the extra boundaries serve a real goal: isolating a sensitive capability, keeping context that should not be widely shared apart, getting an independently tested check, parallelizing truly independent work, or assigning separately governed responsibilities. A role label or a simulated org chart is not a reason. A deterministic service or ordinary tool is a component of an agent, not a second agent.

Treat the choice as a design and risk decision, not a way to look more capable. This matches the voluntary, lifecycle-wide framing of the NIST AI RMF. [1]

Multi-agent systems also cost much more. One vendor's engineering report measured agents at about 4 times the tokens of a chat, and multi-agent systems at about 15 times. It found the approach worked best on broad, parallelizable, high-value research tasks, and fit poorly where agents must share one tightly coupled context, as in most coding. Its quality gain came from an internal evaluation, so test your own task. [2]

## Working model

A **member** is one independently contracted model-driven component. A **role** is the narrower responsibility a member has in this system. One member may fill several roles only if the System Spec says so and the lost separation is evaluated. A reviewer does not become independent by being renamed; shared instructions, evidence, models, or ownership can make failures correlated.

The **system** is the versioned composition. Its deterministic orchestrator owns coordination state and accepts or rejects proposed state changes. A model-driven coordinator may recommend an allowlisted route or combine bounded results, but it is not the source of policy, approval, final truth, or termination. Inter-agent messages, retrieval output, and shared memory are untrusted data. The interaction envelope, identity, data boundaries, and authority attenuation are in [9.2](02-delegation-handoffs-and-agent-to-agent-interfaces.md); system-wide coordination evidence and operations are in [9.3](03-coordination-system-evaluation-and-operations.md).

A System Spec describes the intended composition. Resolving it produces a **composition manifest**: the immutable record of what the system assembled for a release or run. It lists the pinned member manifests and roles, the allowed graph, topology and policy versions, effective limits, and system version. An evaluator or incident reviewer then has one subject to examine, and member contracts are not copied into a second spec that can drift.

## Decisions and best practices

### Start with the least complex workable shape

Compare three designs against the same outcome and hard constraints:

- **One agent** is the default when one bounded contract, context policy, and capability set can do the job.
- **Ordinary orchestration** fits when steps are known and deterministic code can call an agent, tools, or services in a fixed flow. Parallel calls alone do not make it multi-agent.
- **A multi-agent system** fits only when separately contracted members and their controlled interactions give a benefit the simpler options cannot.

Write down the simpler baseline, the claimed benefit, how the benefit could be disproved, and the owner and review date. Higher average answer quality does not justify a composition that breaks a security, latency, reliability, cost, or other hard gate. Include token cost in the comparison. If the benefit is not shown, simplify or record a governed exception; more components are not progress by themselves.

### Select a topology by control burden

Use a deterministic pipeline when stages and transitions are known. A model-selected supervisor with bounded workers fits when interpretation decides which of a few stable specialists should act. Bounded fan-out and gather fits truly independent work, if result ordering, duplicate handling, partial failure, and merge rules are explicit. A producer and reviewer pair can add useful evidence, but the reviewer cannot authorize an action or accept residual risk.

Handoffs, shared state, recursive task trees, meshes, and dynamic membership demand progressively more from state ownership, containment, reproducibility, and termination. They are not maturity levels. Use the least dynamic topology that delivers the documented benefit. If a topology mixes profiles, compute depth, fan-out, retries, concurrency, and budgets across the whole graph, not a separate ceiling per branch.

Static membership is the default. Finding a member through a registry, network endpoint, user input, or integration does not admit it. Dynamic membership can be justified by a need for variable expertise, locality, availability, or capacity, but only inside a reviewed static control envelope. The envelope defines trusted sources, compatible roles and versions, permitted edges, data boundaries, authority ceilings, resource limits, terminal conditions, and the evidence to keep. The admitted graph then becomes part of the run record.

### Make the contract establish system truth

A compact System Spec names the system purpose and version, accountable and operational owners, the multi-agent justification and baseline, topology, member-role assignments, allowed directed interactions, state ownership, root limits, and terminal outcomes. It references member contracts and does not repeat their prompts, tools, or capabilities. It also points to the risk and evaluation policies; the risk method and release decision belong to Parts 10 and 4.

Each category of shared state needs one deterministic owner. At minimum, name the authority for workflow and branch status, accepted evidence, conflict resolution, final outcome, budget accounting, and any externally visible effect. A shared transcript is not truth just because several members can read it. If you use shared memory, specify writers, readers, record types, provenance, conflict handling, retention, and deletion; coordination controls are in 9.3.

Root limits cover the whole system run, not extra allowances per member. Bound agent runs, depth, parallelism, rounds, model and tool requests, input and output volume, time, and spend as they apply. The termination policy must make success, escalation, rejection, cancellation, failure, exhaustion, required-member failure, and late or conflicting results unambiguous. A system with no allowed next step must stop in a declared outcome and must not invent a member or route.

Scale effort to the task. Without explicit rules, agents tend to over-invest in simple queries. Put effort-scaling guidance in the coordinator's instructions and back it with enforced limits, for example one agent and a few calls for a simple lookup, and several workers with a larger cap only for broad, complex tasks. [2]

## Requirements

- **COMPOSE-01 — Admission decision.** When a proposed design has two or more model-driven agents contributing to one application outcome, the accountable owner **MUST** document the simpler baseline, the material benefit claimed for composition, the falsifiable measures or hard gates, and the decision owner and review date. The system **MUST NOT** be adopted solely to create personas, divide one prompt into roles, or conceal an oversized capability set.

- **COMPOSE-02 — System contract and identity.** A production multi-agent system **MUST** have a versioned System Spec and an immutable composition manifest that identify the system, owners, pinned member identities, role assignments, topology, allowed interactions, effective limits, state ownership, terminal outcomes, effective execution class, governance tier, and applicable policy and evidence identities. Its effective execution class and governance tier **MUST** meet the highest applicable member, interaction, capability, policy, and system-risk floors; composition **MUST NOT** lower either floor. The system contract **MUST NOT** copy or silently override a member’s canonical contract; member requirements remain independently applicable.

- **COMPOSE-03 — Governed topology.** A multi-agent system **MUST** declare an explicit allowlisted interaction graph and a deterministic orchestrator for system state, policy enforcement, and termination. A model-driven coordinator **MAY** propose a route within that graph, but **MUST NOT** create an edge, admit a member, enlarge authority, waive a limit, approve a consequential action, or commit an unvalidated state transition. Apply the detailed delegation and authority rules in Chapter 9.2.

- **COMPOSE-04 — Membership and roles.** Before a member receives production work, the system **MUST** validate its pinned contract or manifest, ownership, applicable assurance evidence, compatibility, and role restrictions. A role **MUST** only narrow a member’s effective capability; it **MUST NOT** grant a tool, data class, authorization scope, caller, or interaction mode that the member and current policy do not already permit. Unknown, unpinned, or user-supplied members **MUST** be denied. A system claiming independent review, voting, or defense in depth **MUST** document what is shared and assess relevant correlation in its risk and evaluation evidence.

- **COMPOSE-05 — Dynamic composition.** A system that admits members or constructs edges during a run **MUST** enforce a reviewed static control envelope and record each admitted member, version or manifest identity, assigned role, effective capability, policy decision, admission reason, and resulting graph. A discovered endpoint or capability **MUST NOT** be treated as permission to invoke it.

- **COMPOSE-06 — Bounds, state, and change.** A multi-agent system **MUST** declare and enforce one finite root budget and a termination policy across the complete delegation graph, including permitted retries. Member and interaction limits **MUST** subdivide that root budget rather than add new allowances. Each category of shared state **MUST** have one declared deterministic owner. A membership, role, interaction, topology, schema, limit, or state-ownership change **MUST** create a new system version and composition manifest and trigger the applicable evaluation, risk, compatibility, and rollout review.

## Worked example

The internal policy assistant answers questions from approved, current, permission-filtered documents and returns citations plus uncertainty. It cannot write externally. In the `travel-policy-current` fixture the current approved policy allows GBP 220 for a London hotel, and a superseded document differs. The fixture is fictional.

The starting design is one bounded agent with approved retrieval. The baseline evaluation asks whether it picks the current, permitted source, gives GBP 220 with a supporting citation, and returns `needs_information` when no current permitted source exists. The team considers composition because it hypothesizes that separating evidence preparation from answer checking will catch stale-source and unsupported-claim failures within the same latency and cost gates. That is a hypothesis, not a measured benefit, so the composition is not released before comparison evidence exists.

The candidate uses a fixed, sequential topology. A policy responder receives a question. An evidence-retriever returns only typed evidence references, document versions, effective dates, and retrieval uncertainty from the approved corpus. The responder writes a cited draft. An answer-checker receives the draft and evidence references and returns a bounded check result. The deterministic orchestrator verifies that the cited document is current and permitted, applies the checker outcome policy, and owns the terminal result. The checker may flag missing support or a stale source; it cannot decide that an unsupported answer is acceptable.

```yaml
# System Spec excerpt; values are examples.
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

A key negative case lets the retriever surface the superseded document. The orchestrator must reject it as final support because it is not current, however fluent the draft is. If the checker finds no current citation supports the answer, the composition ends with `needs_information` after its declared bounded correction path; it does not start an open-ended reviewer debate. The evaluation compares the candidate with the single-agent baseline on the same current, superseded, permission-denied, missing-evidence, and injected-content cases, and records what the responder and checker share, so a passing check is not passed off as independent review.

This example stays ephemeral because it has no externally visible side effect. If a later variant can prepare or apply a policy update, its execution class cannot stay ephemeral. It must add the durable execution, exact approval binding, and unknown-outcome handling required by Part 7.

## Evidence and checklist

Keep evidence proportionate to the topology, but make the system identifiable and testable:

- Keep the admission decision and its single-agent or deterministic baseline with the System Spec.
- Validate construction against pinned members, role restrictions, schema compatibility, declared edges, execution class and governance floor, root limits, and terminal outcomes. Fail closed on an invalid composition.
- Keep the composition manifest ID with evaluation records, traces, approvals, release records, and incident references.
- Test that undeclared edges, unknown or unpinned members, role-based capability expansion, empty effective capability, and over-limit dispatch are denied.
- Test topology-specific paths: partial and late results, duplicate branches, required-member failure, cancellation, exhaustion, and the declared final outcome. 9.3 covers integrated system evidence.
- Reassess the composition when membership, graph, policies, shared state, or effective capabilities change. A member update changes system behavior even if the orchestration source is untouched.

Next, define interaction envelopes and authority attenuation in [9.2](02-delegation-handoffs-and-agent-to-agent-interfaces.md), then integrated evidence and operations in [9.3](03-coordination-system-evaluation-and-operations.md).

## References

[1]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"
[2]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"
