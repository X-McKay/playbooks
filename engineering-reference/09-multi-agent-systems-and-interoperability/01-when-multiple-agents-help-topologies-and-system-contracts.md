# 9.1 When Multiple Agents Help, Topologies, and System Contracts

**Status:** 0.5.0-draft.2 — draft
**Audience:** System designers, accountable owners, evaluators, and operators of multi-agent systems
**Applicability:** Two or more independently contracted, model-driven agents working toward one application outcome; not one agent calling code, a service or a tool. A single agent with bounded parallel work uses [Part 6](../06-reasoning-and-execution-patterns/README.md).

[Part 9 overview](README.md) · [Applicability and conformance](../../applicability.md) · [9.2 Delegation, Handoffs, and Agent-to-Agent Interfaces](02-delegation-handoffs-and-agent-to-agent-interfaces.md) · [9.3 Coordination, System Evaluation, and Operations](03-coordination-system-evaluation-and-operations.md)

## Purpose and applicability

A multi-agent system is a versioned composition of members, roles, edges, shared controls and a final outcome; each member keeps its own [agent contract](../../development-guide/02-agent-basics/02-agent-contracts-and-configuration.md). Composition adds risks member review misses: an unexpected member joins, work uses the wrong edge, nested work exceeds the real budget, or work has no terminal owner.

Compose only when the extra boundaries serve a real goal: isolating a sensitive capability, separating context that should not be widely shared, an independently tested check, truly independent parallel work, or separately governed responsibilities. A role label or simulated org chart is not a reason, and a deterministic service or tool is a component, not an agent. This is a design and risk decision, in line with the NIST AI RMF's voluntary, lifecycle-wide framing.[1]

It is also expensive. One vendor report found agents used about 4 times the tokens of a chat and multi-agent systems about 15 times. It concluded the cost suits valuable, heavily parallel research, not work where agents must share one context or depend on each other closely, as in most coding. Its reported 90.2% gain over a single agent came from its own internal research evaluation, so test your own task.[2]

## Working model

The **System Spec** is the versioned design document that declares the composition. A **member** is one independently contracted model-driven component; a **role** is its narrower responsibility here. A member may fill several roles only if the System Spec says so and the lost separation is evaluated. Renaming does not make a reviewer independent; shared instructions, evidence, models or ownership correlate failures.

The deterministic orchestrator owns coordination state and accepts or rejects proposed changes. A model-driven coordinator may recommend an allowlisted route or combine bounded results, but never sets policy, approval, final truth or termination. Inter-agent messages, retrieval output and shared memory are untrusted data (see [9.2](02-delegation-handoffs-and-agent-to-agent-interfaces.md) and [9.3](03-coordination-system-evaluation-and-operations.md)).

Resolving the System Spec produces a **composition manifest**, the immutable record of what a release or run assembled: pinned members and roles, graph, topology and policy versions, effective limits and system version, giving reviewers one subject.

## Decisions and best practices

### Start with the least complex workable shape

- **One agent** is the default when one bounded contract, context policy and capability set can do the job.
- **Ordinary orchestration** fits known steps that deterministic code runs in a fixed flow; parallel calls alone are not multi-agent.
- **A multi-agent system** fits only when separately contracted members give a benefit the simpler options cannot.

Higher average quality never justifies breaking a hard gate (security, latency, reliability, cost including tokens). If the benefit is not shown, simplify or record a governed exception.

### Select a topology by control burden

Use a deterministic pipeline for known stages; a model-selected supervisor with bounded workers when interpretation picks among a few stable specialists; bounded fan-out and gather for independent work with explicit ordering, duplicate, partial-failure and merge rules; and a producer-reviewer pair for extra evidence, though the reviewer cannot authorize an action or accept residual risk. Handoffs, shared state, recursive trees, meshes and dynamic membership need progressively more control and are not maturity levels; use the least dynamic topology that works, with limits computed across the whole graph.

Membership is static by default; discovery through a registry, endpoint, user input or integration does not admit a member. Dynamic membership (for variable expertise, locality, availability or capacity) stays inside a reviewed static envelope (trusted sources, compatible roles and versions, edges, data boundaries, authority ceilings, limits, terminal conditions, evidence); the admitted graph joins the run record.

### Make the contract establish system truth

The System Spec references member contracts and the risk and evaluation policies (Parts 10 and 4) rather than repeating them.

Each category of shared state has one deterministic owner: at least workflow and branch status, accepted evidence, conflict resolution, final outcome, budget accounting and external effects. A transcript many members read is not truth. Shared memory needs defined writers, readers, record types, provenance, conflict handling, retention and deletion (9.3).

Root limits (runs, depth, parallelism, rounds, requests, volume, time, spend) cover the whole run, not extra allowances per member. Termination makes every outcome, including required-member failure and late or conflicting results, unambiguous; with no allowed next step the system stops in a declared outcome rather than invent a member or route.

Without rules, agents over-invest in simple queries (early versions in the same report spawned 50 workers for simple questions). Put effort scaling in the coordinator's instructions and enforce it with limits. The report's starting points: one agent with 3 to 10 tool calls for a simple lookup, 2 to 4 workers for a comparison, and more than 10 workers only for complex research.[2]

## Requirements

- **COMPOSE-01 — Admission decision.** When a proposed design has two or more model-driven agents contributing to one application outcome, the accountable owner **MUST** document the simpler baseline, the material benefit claimed for composition, the falsifiable measures or hard gates, and the decision owner and review date. The system **MUST NOT** be adopted solely to create personas, divide one prompt into roles, or conceal an oversized capability set.

- **COMPOSE-02 — System contract and identity.** A production multi-agent system **MUST** have a versioned System Spec and an immutable composition manifest that identify the system, owners, pinned member identities, role assignments, topology, allowed interactions, effective limits, state ownership, terminal outcomes, effective execution class, governance tier, and applicable policy and evidence identities. Its effective execution class and governance tier **MUST** meet the highest applicable member, interaction, capability, policy, and system-risk floors; composition **MUST NOT** lower either floor. The system contract **MUST NOT** copy or silently override a member’s canonical contract; member requirements remain independently applicable.

- **COMPOSE-03 — Governed topology.** A multi-agent system **MUST** declare an explicit allowlisted interaction graph and a deterministic orchestrator for system state, policy enforcement, and termination. A model-driven coordinator **MAY** propose a route within that graph, but **MUST NOT** create an edge, admit a member, enlarge authority, waive a limit, approve a consequential action, or commit an unvalidated state transition. Apply the detailed delegation and authority rules in Chapter 9.2.

- **COMPOSE-04 — Membership and roles.** Before a member receives production work, the system **MUST** validate its pinned contract or manifest, ownership, applicable assurance evidence, compatibility, and role restrictions. A role **MUST** only narrow a member’s effective capability; it **MUST NOT** grant a tool, data class, authorization scope, caller, or interaction mode that the member and current policy do not already permit. Unknown, unpinned, or user-supplied members **MUST** be denied. A system claiming independent review, voting, or defense in depth **MUST** document what is shared and assess relevant correlation in its risk and evaluation evidence.

- **COMPOSE-05 — Dynamic composition.** A system that admits members or constructs edges during a run **MUST** enforce a reviewed static control envelope and record each admitted member, version or manifest identity, assigned role, effective capability, policy decision, admission reason, and resulting graph. A discovered endpoint or capability **MUST NOT** be treated as permission to invoke it.

- **COMPOSE-06 — Bounds, state, and change.** A multi-agent system **MUST** declare and enforce one finite root budget and a termination policy across the complete delegation graph, including permitted retries. Member and interaction limits **MUST** subdivide that root budget rather than add new allowances. Each category of shared state **MUST** have one declared deterministic owner. A membership, role, interaction, topology, schema, limit, or state-ownership change **MUST** create a new system version and composition manifest and trigger the applicable evaluation, risk, compatibility, and rollout review.

## Worked example

In the fictional `travel-policy-current` fixture the policy allows GBP 220 for a London hotel and a superseded document differs. The baseline is the read-only policy assistant as one agent: it should cite the current permitted source for GBP 220 and return `needs_information` when none exists. The team hypothesizes that separating evidence preparation from answer checking catches stale-source and unsupported-claim failures within the same latency and cost gates, and waits for comparison evidence before release.

In the fixed candidate sequence, an evidence-retriever returns typed references, versions, effective dates and uncertainty; a policy responder writes a cited draft; an answer-checker returns a bounded result that may flag missing support or a stale source but cannot accept an unsupported answer. The deterministic orchestrator verifies the cited document is current and permitted and owns the terminal result.

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

When the retriever surfaces the superseded document, the orchestrator rejects it as final support however fluent the draft; with no supporting current citation, the run ends `needs_information` after its declared correction path, not a reviewer debate. Evaluation compares candidate and baseline on current, superseded, permission-denied, missing-evidence and injected-content cases, recording what responder and checker share. With no external effect the example stays ephemeral; an update-capable variant needs Part 7's controls.

## Evidence and checklist

Scale evidence to the topology:

- Keep the admission decision and baseline with the System Spec, and validate construction against it, failing closed.
- Carry the composition manifest ID into evaluations, traces, approvals, releases and incidents.
- Test denial of undeclared edges, unknown or unpinned members, role-based capability expansion, empty effective capability and over-limit dispatch.
- Test partial and late results, duplicate branches, required-member failure, cancellation, exhaustion and the final outcome (integrated evidence in 9.3).
- Reassess after any member update, even if orchestration is untouched.

## References

[1]: https://www.nist.gov/itl/ai-risk-management-framework "NIST AI Risk Management Framework"
[2]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system"
