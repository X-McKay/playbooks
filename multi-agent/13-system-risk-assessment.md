# 13. System risk assessment

This chapter is for developers who write a multi-agent system's risk
assessment: what you assess beyond the members, what evidence you attach, and
who signs it off. The output is one versioned YAML file.

A system risk assessment covers harms created or changed by composing agents.
It references each member's
[single-agent risk assessment](../advanced/04-risk-assessment.md) and
adds scenarios for coordination, interaction, shared state, dynamic admission,
aggregate authority, and emergent behavior. It complements, and does not
replace, member assessments or required legal, regulatory, security, privacy,
safety, and domain review.

## Required distinctions

- **Member risk** is assessed under the single-agent guidance for one agent and use.
- **Composition risk** arises from membership, edges, coordination, aggregate
  capability, shared state, or emergent behavior.
- **System execution class** describes how the composed work executes.
- **System governance tier** describes required assurance and oversight.
- **Inherent risk** is risk before risk-reducing controls.
- **Residual risk** remains after verified controls.
- **Launch decision** is `go`, `conditional_go`, or `no_go` for one composition
  manifest and rollout scope.

The system tier has the participating member tiers as a floor, but it is not
computed only by taking their maximum. Composition scenarios can establish a
higher tier than any member has in isolation.

## Assessment principles

1. Complete and approve required member assessments first.
2. Assess the actual graph and its maximum permitted dynamic envelope.
3. Identify concrete harm scenarios, not generic architectural concerns.
4. Consider normal use, misuse, adversarial behavior, dependency failure,
   concurrency, retries, operator error, and control failure.
5. Record inherent and residual risk without averaging members or scenarios.
6. Credit only implemented controls with design and effectiveness evidence.
7. Treat missing, stale, or incompatible member evidence as uncertainty, not
   low risk.
8. Keep risk acceptance with authorized humans independent of the assessed
   system.

## Scope

Document:

- intended and prohibited uses;
- users, affected parties, environments, jurisdictions, and rollout size;
- system purpose, topology, and claimed composition benefit;
- static members and the maximum dynamic admission envelope;
- roles, interactions, models, tools, skills, data, memory, and artifacts;
- registries, transports, queues, workflows, providers, and downstream
  systems;
- identities, privileges, approvals, shared state, and side effects;
- owners, operators, reviewers, and risk authorities; and
- referenced member risk assessments and unresolved findings.

Assess the maximum credible graph and authority allowed by policy, not only a
typical or demo execution.

## Risk dimensions

Use the eight single-agent risk dimensions without modification: financial,
operational, reputational, legal, security, privacy, regulatory, and human
impact and safety.

System architecture is an amplifier or cause, not a separate harm dimension.
Score impact and likelihood using the organization's calibrated anchors and the
single-agent risk matrix.

## Composition amplifiers

Composition rarely creates a new kind of harm; it makes existing harms more
likely or larger. Evaluate these as drivers of likelihood or impact:

- number, diversity, ownership, and trustworthiness of members;
- aggregate tools, credentials, network access, data, and transaction
  authority;
- topology depth, fan-out, concurrency, cycles, persistence, and reachability;
- model-selected routing and decomposition;
- dynamic admission, substitution, marketplaces, and external publishers;
- shared memory, blackboards, events, and derived data;
- information loss, distortion, and provenance across handoffs and summaries;
- error correlation, collusion, false consensus, and reviewer dependence;
- retry, duplication, race, ordering, and consistency behavior;
- detection latency, stop capability, reversibility, and maximum blast radius;
- dependency concentration in models, registries, workflows, and providers;
  and
- affected population, task frequency, and system lifetime.

## Required scenario families

Consider each family and record why it is applicable or not. A family marked
not applicable without a reason is incomplete.

### Membership and supply chain

- Invalid, compromised, incompatible, or substituted member is admitted.
- Registry or publisher compromise changes available capabilities.
- Revoked or quarantined member continues receiving work.

### Authority and confused deputy

- A caller launders identity, approval, or authority through another member.
- A less privileged agent induces a privileged agent to act outside purpose.
- Aggregate system capability exceeds intended product authority.

### Data and shared state

- Sensitive data crosses an unauthorized edge or tenant.
- Shared memory, blackboard, event, artifact, or summary is poisoned.
- Aggregation or linkage creates a more sensitive derived dataset.
- Provenance or material dissent is lost.

### Coordination and emergent behavior

- Agents reinforce an incorrect claim into false consensus.
- Reviewers rubber-stamp, collude, or share correlated failure.
- Routing, handoff, or aggregation omits required work or evidence.
- Conflicting agents deadlock, oscillate, or terminate incorrectly.

### Durability and effects

- Retry, concurrency, or duplicate delivery repeats an effect.
- Cancellation fails to stop descendants or leaves partial effects.
- Stale graph, policy, approval, or state causes an unsafe action.
- Recovery or compensation operates on the wrong branch or tenant.

### Resource and availability

- Recursion, fan-out, voting, bidding, or event feedback exhausts spend or
  capacity.
- One coordinator, registry, provider, or queue becomes a systemic bottleneck.
- Resource contention harms other tenants or critical workloads.

### Human and governance

- Human approvers receive incomplete, misleading, or overwhelming evidence.
- Responsibility gaps between member and system owners delay intervention.
- Operators cannot reconstruct, stop, quarantine, or safely resume the system.

## Scenario method

Write each scenario in the single-agent guidance
[scenario form](../advanced/04-risk-assessment.md#scenario-method):

> Because **[composition cause or initiating condition]**, the system could
> **[unsafe action, output, state, or omission]**, causing **[harm]** to
> **[affected party or asset]**.

Each scenario records:

- stable ID, title, owner, status, and scenario family;
- primary and secondary risk dimensions;
- affected parties and assets;
- causes, preconditions, participating roles, edges, and state;
- referenced member scenarios;
- inherent impact, likelihood, tier, confidence, and rationale;
- preventive, detective, and recovery controls;
- evidence for each credited control;
- residual impact, likelihood, tier, confidence, and rationale; and
- eval cases, indicators, alerts, runbooks, treatment, and acceptance.

Use the scenario ID as an eval tag, trace attribute, ledger reference, alert
and runbook key, incident reference, and reassessment trigger.

## Regulatory and prohibited-use screen

Run one system-level screen in addition to the member
[screens](../advanced/04-risk-assessment.md#regulatory-and-prohibited-use-screen).
Composition can change regulatory applicability by changing purpose, affected
population, decision authority, data linkage, autonomy, or scale.

- A prohibited use is `no_go` regardless of member assessments or matrix
  score.
- Binding classifications set minimum system tier and controls.
- Unknown applicability is unresolved risk.
- Dynamic membership MUST NOT route around jurisdiction, residency, sector, or
  provider restrictions.
- The assessment MUST NOT claim that its score establishes legal compliance.

## Inherent-risk boundary

Assess inherent composition risk with the risk-reducing system controls
absent, while treating the basic existence and capabilities of members and
topology as part of the system under assessment.

For example, typed authorization, bounded fan-out, deterministic admission, and
human approval are controls. The fact that the system can select specialists,
aggregate their data, or reach a consequential executor is inherent
capability.

## Controls and evidence

Composition controls include:

- **Preventive:** static allowlists, deterministic admission, authority
  attenuation, typed edges, isolation, data-flow policy, bounded graphs, bound
  approval, and immutable manifests.
- **Detective:** graph and interaction telemetry, admission audit, anomaly
  detection, reconciliation, drift monitoring, and independent review.
- **Recovery:** cancellation propagation, member quarantine, edge disablement,
  rollback, compensation, credential revocation, and deterministic fallback.

Evidence may include code and policy review, schema checks, deterministic
tests, system evals, adversarial exercises, failure injection, durable replay,
concurrency and duplicate tests, audit samples, production metrics,
kill-switch exercises, and independent domain review.

A member control receives composition-risk credit only when evidence shows it
remains effective through the system path. A planned, inherited-but-untested,
or self-attested control receives no residual-risk reduction.

## Governance tier and mandatory floors

The system governance tier is the highest of:

1. the maximum inherent composition-scenario tier;
2. the maximum governance tier of reachable members in their assigned use;
3. legal, regulatory, contractual, or internal-policy floors; and
4. aggregate-capability and topology floors.

At minimum:

- Any reachable consequential action requires `human_governed` execution and
  at least the applicable single-agent floor.
- Broad cross-tenant, privileged code, critical-system, or aggregate
  transaction authority is at least `high`.
- Dynamic admission of externally controlled members with material authority
  or sensitive data is at least `high` unless a documented organizational
  standard establishes a stricter floor.
- Material, potentially irreversible human or safety impact is at least `high`
  and may be `critical`.
- Unbounded recursion, fan-out, membership, events, spend, or side effects is
  `no_go`, not a risk to accept.
- Missing required member assessments, ownership, or composition evidence
  prevents a `low` classification.

## Residual-risk decision

Apply the single-agent
[treatment and acceptance rules](../advanced/04-risk-assessment.md).
Additionally:

- A critical residual composition scenario is `no_go`.
- A high residual scenario requires independent review, designated
  risk-authority acceptance, continuous monitoring, and a tested system-level
  containment mechanism.
- Conditions attach to the exact composition manifest and rollout envelope.
- Changing members, topology, authority, scale, or dynamic-admission policy
  may invalidate acceptance.

No member, coordinator, reviewer, quorum, system-generated report, or model may
accept system risk. You prepare the case; a named human with the authority
accepts it.

## Risk-to-evidence traceability

| Risk property | Required system evidence |
| --- | --- |
| Membership and supply chain | Admission denial, integrity, revocation, substitution, and quarantine tests |
| Authority and data flow | Scope attenuation, confused-deputy, tenant, purpose, and edge-denial tests |
| Coordination | Routing, handoff, aggregation, conflict, dissent, and termination evals |
| Dynamic behavior | Graph bounds, malicious candidates, registry failure, recursion, and drift evidence |
| Durability and effects | Retry, replay, duplication, ordering, cancellation, approval, and compensation tests |
| Resource control | Expansion analysis, budget escrow, backpressure, overload, and kill-switch tests |
| Operations | Indicators, alerts, ledger, runbooks, exercises, owners, and recovery evidence |

A release fails when a material scenario lacks evidence required by its tier
or when a claimed control is contradicted by integrated-system results.

## Lifecycle and reassessment

Reassess after:

- a member, role, edge, topology, registry, model, provider, tool, skill, data
  source, memory, event, or downstream consumer changes;
- autonomy, depth, fan-out, concurrency, authority, population, frequency,
  transaction value, jurisdiction, or deployment scope increases;
- admission, routing, aggregation, retry, approval, termination, or quarantine
  policy changes;
- a failed hard gate, incident, near miss, complaint, drift alert, or
  regulatory change; or
- evidence shows a member or composition control is ineffective.

Review intervals MUST be no longer than the strictest interval required by the
system tier, any reachable member tier, and applicable obligation.

## Canonical artifact

Store one versioned system assessment under:

```text
docs/risk-assessments/systems/<system-name>.yaml
```

Use the [system risk-assessment template](templates/system-risk-assessment.yaml).
The System Spec references it, and composition manifests, eval reports,
approvals, deployments, traces, and incidents record its version or digest.

The assessment is complete only when scope, member references, scenarios,
controls, evidence, classification, acceptance, and review dates are populated
and approved by the required humans.

## Common pitfalls

- **Taking the maximum member tier and stopping.** Composition scenarios can
  push the system above every member.
- **Assessing the demo graph.** The policy allowed far more depth, fan-out, or
  admission than the run that was assessed.
- **Crediting inherited controls.** A member control was counted without
  evidence that it still works through the system path.
- **Treating missing evidence as low risk.** A stale or absent member
  assessment lowered the score instead of raising uncertainty.

## Before you ask for sign-off

- [ ] Every member assessment is complete and approved.
- [ ] Scope covers the maximum permitted graph and admission envelope.
- [ ] Every scenario family is assessed or marked not applicable with a
  reason.
- [ ] Only evidenced controls reduce residual risk.
- [ ] The tier reflects every floor, and no `no_go` condition remains.
- [ ] The YAML file validates and is approved by the required humans.
