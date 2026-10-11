# 4. Operating model

Agents cross organizational lines: a business function decides what to
automate, a platform team runs shared controls, security sets minimum
requirements, and developers build the behavior. This guide describes who
decides what, what each group needs to see, and how adoption grows on
evidence rather than on a calendar.

## Treat the platform as a product

Shared agent infrastructure and controls are a product with a roadmap, support
boundaries, service levels, and incident ownership. They must not become an
invisible dependency maintained informally by each agent team.

- **Central security** defines mandatory controls and validates that they are
  enforced.
- **Business functions** decide what work to automate and which consequences
  are acceptable within organizational policy.
- **Developers** implement bounded behavior and submit evidence.
- **Operations** owns the reliability of the controls and the runtime that
  executes agents.

## Decision rights

| Decision or activity | Accountable | Responsible | Consulted or informed |
| --- | --- | --- | --- |
| Use-case value and authorized purpose | Business owner | Product lead | Users, data owner, security |
| Agent contract standard and approved integrations | Platform owner | Platform engineering | Developer representatives, operations |
| Risk method and minimum controls | Risk or security authority | Security engineering | Business owner, privacy and data specialists |
| Agent behavior, datasets, and evidence completeness | Technical owner | Agent development team | Domain reviewers, evaluation specialists |
| Production promotion within the approved envelope | Designated release authority | Release engineering | Business owner, operations, security by governance tier |
| Policy exception | Named policy authority | Exception sponsor | Control owner, affected data owner, operations |
| Emergency disable and containment | Incident commander | Authorized operations and security responders | Agent owner and business owner, promptly |
| Restart after an incident | Named recovery authority | Operations and technical owner | Incident commander, business owner, security |

Assign real people or staffed groups to these roles in the agent inventory.
Role names alone do not provide coverage.

- Separate the ability to **propose** an expansion of authority from the
  ability to **approve** it.
- Separate **emergency disable** from **restart** authorization.
- Where a small team combines roles, document the conflict and add independent
  review for consequential changes.

Treat this table as a starting point to ratify, not a replacement for the
organization's own decision process. The
[Agent Playbook](../agent-playbook/10-security-and-governance.md#ownership)
requires each agent to name its owners; this table explains how those owners
relate.

## Oversight: who needs to see what

Different groups ask different questions of the same agents. Give each a view
that answers its questions without exposing more than it needs.

| Audience | Questions the view answers | Access boundary |
| --- | --- | --- |
| Central security and risk | Which agents hold authority? Which controls are stale? Where are unknown capabilities, policy drift, critical failures, or expired exceptions? | Organization-wide metadata; sensitive content access controlled and audited. |
| Operations | Are the shared controls, runtimes, queues, revocation, and telemetry working? Which releases lack readiness? | Operational metadata with controlled diagnostic access. |
| Business function | Are outcomes useful? What was executed or escalated? What did it cost? Which approvals, exceptions, and incidents need attention? | Records scoped to the function, plus approved aggregate comparisons. |
| Agent development team | Which case, tool, policy decision, or integration caused a failure? Which release regressed? | Traces for owned agents with redacted diagnostic detail. |
| Independent reviewer | What evidence and authority justified promotion? Can it be reproduced? What changed after approval? | Immutable evidence and approval history, with content access on need. |

To make these views possible, every agent emits consistent metadata: agent
and release, run, business function, tenant, capability, policy revision,
governance tier, decision and approval references, and budget counters (see
[correlation](../agent-playbook/08-observability.md#correlation)). Identifiers
must not carry secrets, sensitive approval payloads, or raw user content.

- **Enforce access in the data layer**, not by hiding a filter in a dashboard.
- **Business-function attribution is for oversight and cost**, not a security
  principal. Tenant and data-owner restrictions still apply.
- **Route alerts by who can act.** Unauthorized actions, critical gate
  failures, unknown agents, stale policy, bypassed controls, and tenant
  mismatches go to central responders and the owner. Quality and cost
  regressions go to the business and technical owners.
- **Make telemetry loss visible.** Alert on gaps, and decide per governance
  tier whether losing required audit delivery blocks new consequential
  actions. Logs are evidence; they do not enforce authority.

## Adopt in stages, on evidence

Authorize each stage with exit evidence, not a calendar promise. Track
delivery dates separately, with named dependencies and owners. Do not onboard
high-consequence use cases to meet a platform deadline.

| Stage | Work to complete | Exit evidence |
| --- | --- | --- |
| Foundation | Ratify the agent contract, owners, risk scenarios, data handling, and baseline metrics. Inventory existing agents, owners, tools, side effects, and credentials. | Two reference agents validate; required fields and control gaps are visible. |
| Developer pilot | Build a read-only agent and an approval-gated action agent with the standard tooling. Improve validation messages and evaluation templates with real developers. | Teams can explain a failure, add evidence, and reproduce a release locally without platform help. |
| Control validation | Verify that isolation, call mediation, identity, telemetry, and revocation work in a dedicated environment. Add denial, bypass, startup, and partition tests. | Effective policy is reported; bypass attempts are blocked; agents refuse to start when a required control is absent; disable drills meet agreed objectives. |
| Controlled production | Release a bounded cohort with staffed support, approved evidence, dashboards, budgets, and rollback procedures. | Value and reliability meet pilot criteria; the inventory matches the agents actually running. |
| Scale and improve | Add durable workflows, higher-consequence capabilities, and delegated business views only after their controls are validated. | Evidence and approvals remain complete as adoption grows; the exception backlog and support cost stay manageable. |

The first production cohort should show whether the standard improves
developer lead time and operational clarity, not only whether the automation
runs.

### Bringing existing agents into conformance

Teams with agents already in use can adopt the playbook incrementally:

1. Inventory agents, owners, tools, side effects, and credentials.
2. Assign execution classes and complete scenario-based risk assessments.
3. Introduce typed inputs, outputs, and tool contracts.
4. Move state-changing agents onto a durable execution engine.
5. Add hard budgets and correlated telemetry.
6. Establish smoke, regression, safety, and trajectory evaluations.
7. Add human approval to consequential actions.
8. Complete the production-readiness checklist.

### Make the right path the easy path

Adoption depends on good defaults and helpful feedback:

- An explanation for every failed gate that links it to the capability, risk
  scenario, policy rule, and an example remedy.
- A preview of what a release will be allowed to do before it is submitted.
- How-to guides for common tasks, a migration checklist for existing agents,
  and a clear exception path for genuinely unsupported needs.
- Platform support that studies recurring friction and improves the standard,
  rather than leaving teams to accumulate private workarounds.

## Keep a decision register

Record each organizational decision the playbooks leave open: approved
integrations, identity approach, isolation model, orchestration criteria,
policy-distribution service levels, data handling, risk thresholds, and
release authorities. Each entry names its evidence, accountable owner,
effective date, review trigger, and replacement plan. Version the register so
teams can tell an approved standard from a proposed next step.
