# 7. Evaluation

This guide is for developers who need to show that a multi-agent system
works, not just that its members do. Every member still needs the evaluation
the Agent Playbook's [evaluation](../agent-playbook/07-evaluation.md) chapter
requires, but passing member evals does not demonstrate that the composition
works. A system is incomplete until its claimed composition benefit, member
behavior, interaction contracts, emergent failure modes, operational limits,
and recovery behavior are represented in reproducible tests and evals.

## Test each layer with the right tool

| Layer | Purpose | Typical execution |
| --- | --- | --- |
| Policy and schema tests | Deterministic contracts, graph, scopes, and budgets | No model |
| Member tests | Individual Agent Playbook conformance | Mocked and real model |
| Interaction tests | Handoffs, delegation, data flow, and failures | Mocked members |
| Coordination tests | Routing, aggregation, termination, and state | Mocked and real members |
| End-to-end system evals | Outcome quality and composition benefit | Real system |
| Durable execution scenarios | Retry, replay, concurrency, cancellation, recovery | Mocked and real members |
| Adversarial system evals | Cross-agent attacks and emergent failure | Realistic sandbox |
| Online evals | Drift, graph behavior, and unknown failures | Sampled production |

Deterministic properties MUST use deterministic tests. A model judge is not
an acceptable evaluator for authorization, admission, tenant isolation,
approval, schema validity, budget enforcement, idempotency, or termination.
Where you do use a judge, the Agent Playbook's rules for LLM judges apply.

## Beat a simpler baseline

The multi-agent admission test is executable. The evaluation plan identifies
a reasonable simpler baseline, normally one of:

- a deterministic implementation;
- one agent with the same underlying tools and evidence;
- one agent with deferred skills rather than specialist agents; or
- the previous static composition, when proposing a dynamic one.

Compare the system and baseline on task success, hard-gate safety, latency,
cost, operational complexity, and the specific claimed benefits. Control
datasets, tools, permissions, model families where practical, and run counts.

A system SHOULD NOT proceed merely because it wins one quality metric. Record
whether the improvement justifies the added failure modes, operational
burden, and cost.

## Organize datasets by what can go wrong

```text
evals/systems/<system_name>/
├── datasets/
│   ├── smoke/
│   ├── outcomes/
│   ├── routing/
│   ├── handoffs/
│   ├── aggregation/
│   ├── adversarial/
│   ├── durability/
│   ├── dynamic-admission/
│   └── regressions/
├── evaluators/
│   ├── deterministic/
│   ├── outcome/
│   ├── graph/
│   ├── interaction/
│   ├── safety/
│   ├── operational/
│   └── durability/
├── experiments/
│   ├── baseline/
│   ├── ablations/
│   └── topology/
├── fixtures/
└── baselines/
```

Every confirmed system defect becomes a sanitized regression case. Cases
carry stable IDs, risk-scenario tags, topology and capability tags, expected
invariants, required branches, and dataset provenance.

## Hard gates

These are binary release gates when applicable:

- Every member and interaction is admitted by current policy.
- No undeclared edge or incompatible schema is used.
- Delegation never amplifies authority or crosses tenant boundaries.
- No prohibited data crosses an interaction boundary.
- No consequential action executes without valid bound approval.
- Duplicate, retried, or concurrent work creates no duplicate side effect.
- Root and child budgets, concurrency, depth, fan-out, rounds, and deadlines
  hold.
- Cancellation and kill switches stop new dispatch and propagate correctly.
- Required members, evidence, and reviews cannot be silently skipped.
- System state reaches an accurate terminal or escalation status.
- Durable replay passes for supported histories.
- Critical system-risk cases have zero known failures.

One hard-gate failure blocks release. Average member quality, majority votes,
or high aggregate task success cannot compensate for it.

## Judge the outcome, not the members

Measure the end-to-end product outcome rather than treating member completion
as success. Alongside the Agent Playbook's quality metrics, consider evidence
completeness, process adherence, conflict recognition and resolution quality,
user effort and time to a useful outcome, recovery from incomplete or failed
work, and cost and latency per successful, compliant outcome.

The final evaluator receives the authoritative system result, relevant
evidence, and a normalized execution summary. It MUST NOT infer success from
an agent's self-reported status.

## Evaluate the path through the graph

Evaluate the system's path as well as its answer:

- appropriate topology, member, and role selection;
- correct and minimal delegation;
- correct edge, schema, arguments, authority, and data context;
- handoff completeness and unambiguous ownership;
- required ordering, and approval before effects;
- useful parallelism without avoidable duplication;
- preservation of evidence, uncertainty, and dissent;
- correct aggregation and conflict handling;
- no ping-pong, deadlock, livelock, or premature termination; and
- graceful budget exhaustion, failure, and escalation.

Prefer invariants and allowed partial orders over one exact trace, because
several safe execution paths may be valid.

## Measure what each topology risks

Each [topology](02-reference-architecture.md) invites its own failures:

| Topology | Measure |
| --- | --- |
| Supervisor and worker | Routing precision and recall, unnecessary delegation, unavailable-member behavior, coordinator bottlenecks, specialist misuse |
| Fan-out and gather | Coverage gain, branch diversity, redundant work, stragglers, merge correctness, partial results, whether parallelism improves wall-clock time |
| Producer and reviewer | Reviewer detection and false-rejection rates, correlated failures, rubber-stamping, correction effectiveness, retry loops |
| Quorum or voting | Error correlation, calibration, tie policy, minority correctness, aggregation sensitivity, performance against the strongest single member |
| Hierarchy and handoff | Information loss at every level, summary fidelity, ownership transfer, compounded latency, whether escalation reaches the correct authority |
| Blackboard and event-driven | Stale reads, conflicting writes, provenance loss, poisoning, duplicate or reordered events, feedback loops, convergence, recovery after consumer outage |
| Recursive task trees | Decomposition quality, useful versus redundant nodes, depth and fan-out distributions, subtree cancellation, synthesis completeness, worst-case resource expansion |
| Dynamic membership and allocation | Admission correctness, compatibility, registry failure, substitution, selection regret, malicious or misleading capability claims, reproducibility, quarantine, behavior when no valid member is available |

## Inject faults

System suites SHOULD inject:

- member timeout, crash, malformed output, and budget exhaustion;
- a slow or unavailable registry, model, tool, queue, or artifact store;
- duplicate, missing, delayed, and reordered messages;
- a stale graph version or member manifest mismatch;
- conflicting evidence and simultaneous writes;
- worker loss before and after dispatch or side effect;
- approval expiry or argument tampering;
- telemetry and audit export failure; and
- quarantine or a kill switch during active work.

Assert on final status, state integrity, budget reconciliation, side effects,
recovery, alerts, and the evidence retained for investigation.

## Attack across agents

Include cross-agent scenarios for:

- direct and indirect prompt injection propagation;
- instruction, identity, approval, and authority laundering;
- confused-deputy use of a more privileged member;
- shared-memory or blackboard poisoning;
- data exfiltration through summaries, evidence, bids, or error messages;
- collusion, false consensus, and reviewer capture;
- Sybil-style dynamic members or registry substitution;
- denial-of-wallet through recursion, fan-out, retries, or event loops; and
- malicious result timing intended to bypass cancellation or policy.

Adversarial inputs remain untrusted throughout the graph. Sanitizing or
summarizing them through another agent does not make them trusted.

## Prove each part earns its place

For material changes, run ablation and topology experiments that compare:

- the system against its admission baseline;
- the system with each optional member removed;
- static and dynamic routing;
- sequential and parallel execution;
- alternative aggregation or conflict policies;
- homogeneous and intentionally diverse member configurations; and
- current and candidate limits for depth, fan-out, rounds, and concurrency.

Ablation shows whether each member and mechanism contributes enough value to
justify its cost and risk.

## Repeat runs and report distributions

Follow the Agent Playbook's
[multi-run evaluation](../agent-playbook/07-evaluation.md#multi-run-evaluation),
and also repeat cases affected by routing, concurrency, arrival order,
dynamic selection, reviewer behavior, or stochastic decomposition. Report:

```text
end-to-end and hard-gate pass rates
worst-case and failure-category distributions
member, edge, depth, fan-out, and round distributions
p50/p95/p99 active latency and completion duration
model, tool, token, and cost distributions
routing, handoff, conflict, and termination metrics
```

Rare high-impact failures remain visible; aggregate means MUST NOT hide them.

## Release policy

Like an agent's [release gates](../agent-playbook/07-evaluation.md#release-gates),
a system policy declares absolute and relative requirements, for example:

```yaml
hard_gates:
  unauthorized_edges: 0
  authority_amplification_events: 0
  unapproved_consequential_actions: 0
  duplicate_side_effects: 0
  termination_limit_violations: 0
  durable_replay_pass_rate: 1.0
quality:
  task_success_rate_min: 0.92
  regression_allowed: 0.02
coordination:
  valid_routing_rate_min: 0.98
  handoff_completeness_rate_min: 0.99
  unnecessary_delegations_per_run_max: 0.5
operational:
  p95_active_latency_seconds_max: 30
  average_cost_usd_max: 1.50
admission:
  baseline_quality_improvement_min: 0.03
  maximum_cost_multiplier: 2.0
```

Thresholds are system-specific. Release fails on a hard gate, a missed
absolute threshold, excessive regression, absent required scenario coverage,
or missing provenance.

## Watch for graph drift online

Online evaluation follows the Agent Playbook's rules: asynchronous,
side-effect-free, privacy controlled, and version attributed. Stratify
sampling by topology, graph version, role, interaction, depth, member
selection, outcome, risk scenario, and degraded mode.

Monitor graph drift as well as model drift. Unexpected members, edges, depth,
fan-out, role assignment, selection distribution, or termination status
require investigation even when final-answer quality appears stable.

## Provenance

Every report records:

```text
system and composition manifest versions
member capability manifests and models
topology, graph, schemas, and policies
workflow and worker build
datasets, cases, evaluators, and risk tags
judge models and rubrics
baseline and ablation configuration
run count, concurrency, timing, and random seeds where relevant
case-level outcomes, traces, latency, usage, and cost
```

## Common pitfalls

- **Adding up member scores.** Every member passed, and nobody tested the
  handoffs where the system failed.
- **Trusting the coordinator's report.** The evaluator read "completed" from
  an agent instead of the authoritative result.
- **Watching answers, not the graph.** Quality held steady while new members
  and edges appeared in production.

## Before you move on

- [ ] The system beats a simpler baseline by enough to justify its cost.
- [ ] Deterministic properties have deterministic tests, not judges.
- [ ] Hard-gate, coordination, topology, fault, and adversarial cases exist.
- [ ] Ablations and repeated runs back each release decision.
