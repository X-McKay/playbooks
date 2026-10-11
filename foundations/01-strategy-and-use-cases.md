# 1. Strategy and use-case selection

## Purpose, outcomes, and boundaries

An agent is a software system that uses model outputs to select or sequence
actions. Its risk comes from the authority those actions carry, the data they
touch, whether they can be undone, and the uncertainty of the decisions behind
them. A strategy for agents therefore starts with business outcomes and bounded
authority, not with a preferred model or a collection of disconnected
guardrails.

A successful agent solves a defined problem within an agreed operating
envelope, produces evidence of its behavior, and can be stopped without waiting
for it to cooperate.

Most organizations progress from assistance to bounded execution:

- A **research assistant** retrieves approved documents and prepares a cited
  answer.
- A **change-preparation agent** drafts an update, and a person approves its
  exact content before anything changes.
- A **service agent** executes a narrow, reversible action under a transaction
  limit.

The same contract and release vocabulary should describe all three; their
[execution classes](../agent-playbook/01-principles-and-scope.md#execution-classes),
governance tiers, and controls differ. "Agent" is never an exemption from
software engineering, identity management, change control, or incident
response.

Aim for a paved road: a starter package, typed capability interfaces, local
validation, repeatable evaluations, reviewable policy, immutable release
evidence, and consistent runtime controls. Developers then spend their effort
on domain behavior and evaluation cases, platform teams own the shared
controls, and business owners own outcomes, authorized use, acceptable
consequences, and recovery decisions.

## Should this be an agent?

Before building, document the work being improved, the current baseline, the
people affected, and the decisions the agent may make. Then compare an agent
with simpler alternatives:

| Alternative | Prefer it when |
| --- | --- |
| Deterministic workflow or rules | The inputs and the sequence of steps are known and stable. |
| Search or retrieval interface | People need to find information and can judge it themselves. |
| Single-call assistant | One model response, reviewed by a person, is enough. |
| Agent | Uncertainty in inputs or in the sequence of actions provides material value that outweighs the cost of evaluating and controlling it. |

Multi-step autonomy adds obligations: explaining termination, escalation,
resource consumption, and recovery from failure. Multiple coordinating agents
add more; the [Multi-Agent Systems Playbook](../multi-agent-playbook/01-principles-and-scope.md)
requires that choice to be justified separately.

## Use-case charter

A charter records the value hypothesis and the boundaries of the first
release. It SHOULD name:

- business owner, technical owner, and operating (on-call) owner;
- target users and the task they need done;
- authorized inputs, outputs, and actions;
- maximum consequence and prohibited actions;
- the baseline being improved and how it is measured;
- where evidence will be collected; and
- the exit criteria that end or promote the trial.

```yaml
# Example charter. Values are illustrative, not policy defaults.
use_case: internal-knowledge-assistance
business_owner: knowledge-operations
technical_owner: agent-platform-pilot
operating_owner: knowledge-support-on-call
authority: retrieve-approved-documents-and-draft-answer
prohibited: [cross-tenant-search, external-send, credential-access]
baseline: manual-supported-question-resolution
pilot_exit:
  value: measured-resolution-time-improvement
  safety: no-known-critical-gate-failures
  operations: exercised-disable-and-recovery-procedure
  economics: approved-cost-per-successful-task
```

For example, an internal knowledge assistant might aim to reduce resolution
time for supported questions while keeping citations correct and tenants
isolated. A purchasing assistant might initially prepare orders only, with no
spend authority. Expanding it to place orders is a new capability and a new
risk decision, not a configuration change.

Use cases progress through discovery, bounded pilot, controlled production,
and expansion. Each promotion changes the operating envelope and requires
updated evidence. A useful prototype that runs on broad developer credentials
is not a production candidate until those credentials and capabilities are
replaced. A failed pilot can still produce reusable datasets, tool interfaces,
or control tests: keep those assets and stop the use case when its value
hypothesis fails.

## Measure value, reliability, safety, and adoption separately

A single "agent score" hides the difference between useful output and safe
authority. For each metric, define its numerator, denominator, population,
measurement window, owner, and exclusions. Segment by release, task type,
business function or tenant, and governance tier. Set targets after a baseline
and a risk review; the definitions below are measurement contracts, not
universal thresholds.

| Metric | Definition | Interpretation and owner |
| --- | --- | --- |
| Verified task success | Tasks meeting the task's correctness rubric and every required deterministic constraint, divided by eligible completed tasks. | Report abandoned, escalated, and timed-out tasks separately. The product owner owns the rubric. |
| Net time recovered | Baseline effort minus assisted effort, including review, correction, and incident follow-up, per matched task cohort. | Do not count output-generation time as business savings. The business owner validates the comparison. |
| Cost per verified success | Total model, tool, runtime, evaluation, and allocated operations cost divided by verified successful tasks. | Unsuccessful work is included in cost. Finance and product owners review distribution and trend. |
| Critical control failures | Demonstrated authorization, isolation, approval, or other hard-gate violations, with attempted and completed actions counted separately. | Any known release-blocking failure blocks promotion. Security owns severity. |
| Risk scenario coverage | Material risk scenarios with passing required evidence, divided by the material scenarios required for declared and observed capabilities. | Unknown capabilities are reported separately; they cannot improve coverage by shrinking the denominator. |
| Revocation effectiveness | Time from an authorized disable to each enforcement layer's acknowledgement and to the last newly authorized consequential action. | Report p50, p95, maximum, and failures. Operations owns the drill. |
| Delivery lead time | Elapsed time from a complete submission to reviewable evidence, and then to production approval. | Separate developer effort, automated execution, and approval wait. The platform owner owns improvement. |
| Governed adoption | Active production agents with complete, current inventory records and verified controls, divided by all known active production agents. | Discover the denominator from deployment and identity inventories; self-registration alone is not enough. |

Track operational service levels independently: request latency, workflow age,
tool error rate, queue delay, telemetry delivery lag, policy freshness, and
budget exhaustion. Define objectives per use case and governance tier; an
interactive assistant and a multi-day workflow need different latency
measures. A quality regression can justify rollback while infrastructure is
healthy, and a stale authorization decision can justify blocking new actions
while the model is answering correctly.

Publish scorecards that show denominator size and uncertainty. A safety suite
with zero observed failures is evidence about that suite, not proof of general
safety. Compare paired cases across releases, show important subgroup
regressions, and keep critical controls as deterministic pass/fail gates (see
[hard gates](../agent-playbook/07-evaluation.md#hard-gates)). Treat user
acceptance, reviewer agreement, and sampled output quality as complementary
evidence with stated bias and confidence limits.

## Tradeoffs to decide deliberately

- **Generated policy versus authored policy.** Observing an agent can propose
  the access it needs, but observation is incomplete and can capture accidental
  or malicious behavior. Treat generated rules as proposals bounded by declared
  purpose and central invariants, never as authority.
- **Static analysis versus runtime evidence.** Analysis reveals likely side
  effects, but dynamic behavior, remote tools, and runtime configuration leave
  uncertainty. Expose that uncertainty and ask for evidence rather than
  assigning an unjustified low risk.
- **Convenience versus transparency.** Automatically injected controls reduce
  setup but can make failures opaque. Prefer explicit, versioned plans and a
  way to show the resolved identity, routes, isolation profile, model
  configuration, and telemetry path for any release.
- **Durability versus correctness.** Durable execution recovers coordination
  state but does not replace idempotency, business reconciliation, or
  compensation.
- **Centralization versus concentration risk.** Shared gateways and policy
  services need tested fail-closed behavior at consequential boundaries,
  bounded caching and freshness, and a clear message to users when they are
  unavailable.
- **Observability versus privacy.** Telemetry can become a sensitive data
  store. Default to metadata, controlled redaction, and selective content
  retention.
- **Safety overhead versus sustainability.** Measure and attribute the cost
  and latency of controls so that safe defaults remain affordable.

Nothing in this guide establishes regulatory compliance. Qualified owners
determine legal and regulatory obligations, map them to controls and evidence,
and keep those mappings separate from claims about technical capability (see
the [regulatory screen](../agent-playbook/13-risk-assessment.md#regulatory-and-prohibited-use-screen)).
Risk tolerance, approval thresholds, data classes, and retention rules remain
organizational decisions.
