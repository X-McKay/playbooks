# 8. Production readiness

Use this checklist before an agent's first production launch. It collects the
earlier chapters' requirements in one place. Work through it as the
developer, linking evidence for each item; an accountable owner then
completes and approves it before production launch. An unchecked item is
either a blocker or a recorded
[exception](11-security-and-governance.md#exceptions-and-review).

Every agent needs a governance tier from a
[risk assessment](12-risk-assessment.md), even a read-only one. For a
low-risk agent the assessment can be short: list its scenarios, show that
none is material above low, and record who accepted it. Items that depend on
[Advanced concepts](README.md#part-2-advanced-concepts), such as durable
execution, apply when your agent uses them.

## Contract

- [ ] Agent name and version are stable.
- [ ] Owner, execution class, and governance tier are declared.
- [ ] The Agent Spec references a current, approved risk assessment.
- [ ] Governance tier matches the assessment and all mandatory floors.
- [ ] Inputs, dependencies, outputs, and errors are typed.
- [ ] Model policy and budgets are declared.
- [ ] Governance metadata validates at startup.
- [ ] Capability manifest is reproducible.

## Skills and tools

- [ ] Skills and tools use explicit allowlists.
- [ ] Runtime skill assets exist in the built deployment artifact.
- [ ] Skill activation and non-activation evals pass.
- [ ] Tool effects and retry safety are classified.
- [ ] Authorization and tenant isolation are enforced in code.
- [ ] Side effects are idempotent.
- [ ] Consequential actions require bound approval.
- [ ] Tool outputs are bounded.

## Durable execution

- [ ] Durable runs execute inside workflows.
- [ ] All I/O executes in durable steps.
- [ ] Workflow and durable-step identifiers are stable.
- [ ] Timeouts and retry policies are bounded.
- [ ] Provider transport retries are disabled or justified.
- [ ] Cancellation and compensation are defined.
- [ ] Payloads and histories are bounded.
- [ ] Replay tests pass.
- [ ] A build that can continue in-flight workflows stays available during
  rollout.

## Evaluation

- [ ] Every material risk scenario maps to required eval and control evidence.
- [ ] Eval reports identify covered and uncovered risk scenario IDs.
- [ ] Unit, component, smoke, regression, capability, and safety suites pass.
- [ ] Trajectory and tool-argument checks pass.
- [ ] Durable-execution failure scenarios pass.
- [ ] Required multi-run evaluations pass.
- [ ] Quality, cost, and latency meet thresholds.
- [ ] Critical hard gates have no known failures.
- [ ] Results include complete provenance.

## Observability

- [ ] Request, workflow, agent, model, skill, and tool telemetry correlate.
- [ ] Outcomes and errors use normalized categories.
- [ ] Sensitive-content capture is configured intentionally.
- [ ] Redaction tests pass.
- [ ] Health, quality, safety, and cost dashboards exist.
- [ ] Alerts route to named owners.
- [ ] Consequential actions produce audit records.

## Cost

- [ ] Run-level request, tool, token, and cost limits exist.
- [ ] Shared budget counters use durable storage where required.
- [ ] Unknown-price behavior is explicit.
- [ ] Retry multiplication has a documented upper bound.
- [ ] Context-growth and cache behavior are measured.
- [ ] Budget exhaustion produces a safe typed outcome.
- [ ] Cost per successful compliant outcome is visible.

## Security and governance

- [ ] Prohibited-use and regulatory-applicability screening is complete.
- [ ] Inherent and residual risk are scored with rationale and confidence.
- [ ] Residual risks have treatments, owners, acceptance, and review dates.
- [ ] Threat model is current.
- [ ] Required security, privacy, domain, and risk reviews are complete.
- [ ] Credentials, storage, filesystem, and network access are least
  privilege.
- [ ] MCP servers and dependencies are approved and pinned.
- [ ] Human approval is authenticated and tamper-tested.
- [ ] Kill switches are tested.
- [ ] Incident and rollback runbooks exist.
- [ ] Exceptions are recorded and unexpired.

## Operations

- [ ] Staging, shadow, canary, and promotion criteria match the governance
  tier.
- [ ] On-call and escalation ownership are established.
- [ ] Provider and dependency failures are tested.
- [ ] Worker shutdown, recovery, and replay are tested.
- [ ] Decommissioning responsibility is assigned.

## Ownership

Every agent names product, engineering, quality, operational, domain, and
applicable security owners. One person may fill several roles, but
accountability MUST be explicit.

## Kill switches

Support authenticated, audited
disabling of an agent, version, model, provider, skill, tool, tenant, workflow
type, or new workflow starts. Durable controls distinguish stopping new work,
pausing active work, cancelling it, allowing safe completion, and blocking the
next side effect.

## Incident response

Write the runbook before launch. The sequence is:

1. Contain.
2. Preserve evidence.
3. Identify affected manifests, workflows, tenants, and actions.
4. Revoke or restrict capabilities.
5. Stop or isolate unsafe workflows.
6. Compensate reversible effects.
7. Notify required stakeholders.
8. Add regression cases.
9. Correct and validate the system.
10. Complete a post-incident review.

## Approval record

You fill in the record; the approvers sign it. Keep it with the release.

```text
Agent:
Version:
Manifest ID:
Execution class:
Governance tier:
Risk assessment and version:
Maximum residual risk:
Residual-risk acceptance:
Engineering owner:
Product/domain owner:
Operations owner:
Security/privacy approvers:
Evaluation report:
Threat model:
Deployment plan:
Exceptions:
Approved by:
Approval date:
Next review date:
```

## Common pitfalls

- **Ticking boxes without links.** A checked item with no evidence is a claim,
  not readiness.
- **Doing the checklist at the end.** Items such as replay tests and kill
  switches are cheap to design in and expensive to retrofit.
