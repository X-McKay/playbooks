# 4. Operating model

This guide is for the developers who will build the agent. You will not make
every decision about your agent yourself: someone else decides what is worth
automating, sets the minimum controls, and approves a release. This guide
tells you which decisions are yours, whose sign-off you need, what your agent
must report so others can oversee it, and how it moves from pilot to
production on evidence rather than on a calendar.

## Know who decides what

An agent crosses organizational lines: a business function decides what to
automate, security sets mandatory controls, operations runs the shared
runtime, and you build the bounded behavior and submit the evidence. Knowing
who holds each decision tells you whom to ask before release day.

| Decision | Who is accountable | What you do |
| --- | --- | --- |
| Use-case value and authorized purpose | Business owner | Build to the agreed purpose; raise it when the design needs more. |
| Contract standard and approved integrations | Platform owner | Use the approved integrations, or request a new one with its purpose. |
| Risk method and minimum controls | Risk or security authority | Complete the risk assessment and implement the controls it requires. |
| Agent behavior, datasets, and evidence completeness | Technical owner | Own this: build, test, and assemble the evidence. |
| Production promotion within the approved envelope | Designated release authority | Submit the release with its evidence; do not self-approve. |
| Policy exception | Named policy authority | Sponsor the request, with its scope, reason, and expiry. |
| Emergency disable and containment | Incident commander | Make sure disable works; expect to be informed promptly. |
| Restart after an incident | Named recovery authority | Help diagnose and fix; restart only when authorized. |

The [Agent Playbook](../agent-playbook/10-security-and-governance.md#ownership)
requires each agent to name its owners. Treat this table as a starting point
your organization ratifies; it may already have its own decision process.

Best practices:

- **Name real people or staffed groups.** Role names alone do not provide
  coverage. Record them where your organization keeps its agent inventory.
- **Separate proposing from approving.** You can propose an expansion of
  your agent's authority; someone else approves it.
- **Separate emergency disable from restart.** The person who can stop the
  agent is not automatically the person who decides it is safe to restart.
- **Document combined roles.** On a small team you may be both technical and
  operating owner. Write the conflict down and get independent review for
  consequential changes.

## Feed the oversight views

Different people ask different questions of the same agents, and your
agent's telemetry is what answers them:

| Audience | Questions they ask | What they may see |
| --- | --- | --- |
| Security and risk | Which agents hold authority? Which controls are stale? Where are unknown capabilities, policy drift, critical failures, or expired exceptions? | Organization-wide metadata; sensitive content access controlled and audited. |
| Operations | Are the shared controls, runtimes, queues, revocation, and telemetry working? Which releases lack readiness? | Operational metadata with controlled diagnostic access. |
| Business function | Are outcomes useful? What was executed or escalated? What did it cost? Which approvals, exceptions, and incidents need attention? | Records scoped to the function, plus approved aggregate comparisons. |
| You, the development team | Which case, tool, policy decision, or integration caused a failure? Which release regressed? | Traces for owned agents with redacted diagnostic detail. |
| Independent reviewer | What evidence and authority justified promotion? Can it be reproduced? What changed after approval? | Immutable evidence and approval history, with content access on need. |

To make these views possible, every agent emits consistent metadata: agent
and release, run, business function, tenant, capability, policy revision,
governance tier, decision and approval references, and budget counters (see
[correlation](../agent-playbook/08-observability.md#correlation)). Identifiers
must not carry secrets, sensitive approval payloads, or raw user content.

Best practices:

- **Enforce access in the data layer**, not by hiding a filter in a
  dashboard.
- **Treat business-function attribution as a label, not a principal.** It is
  for oversight and cost; tenant and data-owner restrictions still apply.
- **Route alerts to whoever can act.** Unauthorized actions, critical gate
  failures, unknown agents, stale policy, bypassed controls, and tenant
  mismatches go to central responders and the owner. Quality and cost
  regressions go to the business and technical owners.
- **Make telemetry loss visible.** Alert on gaps, and decide per governance
  tier whether losing required audit delivery blocks new consequential
  actions. Logs are evidence; they do not enforce authority.

## Adopt in stages, on evidence

Each stage widens what your agent can do or who uses it, so each needs exit
evidence, not a calendar promise. Track delivery dates separately, with named
dependencies and owners, and do not onboard a high-consequence use case to
meet a deadline.

| Stage | Work to complete | Exit evidence |
| --- | --- | --- |
| Foundation | Ratify the agent contract, owners, risk scenarios, data handling, and baseline metrics. Inventory existing agents, owners, tools, side effects, and credentials. | Two reference agents validate; required fields and control gaps are visible. |
| Developer pilot | Build a read-only agent and an approval-gated action agent with the standard tooling. Feed back on validation messages and evaluation templates. | Teams can explain a failure, add evidence, and reproduce a release locally without platform help. |
| Control validation | Verify that isolation, call mediation, identity, telemetry, and revocation work in a dedicated environment. Add denial, bypass, startup, and partition tests. | Effective policy is reported; bypass attempts are blocked; agents refuse to start when a required control is absent; disable drills meet agreed objectives. |
| Controlled production | Release a bounded cohort with staffed support, approved evidence, dashboards, budgets, and rollback procedures. | Value and reliability meet pilot criteria; the inventory matches the agents actually running. |
| Scale and improve | Add durable workflows, higher-consequence capabilities, and delegated business views only after their controls are validated. | Evidence and approvals remain complete as adoption grows; the exception backlog and support cost stay manageable. |

The first production cohort should show whether the standard improves your
lead time and operational clarity, not only whether the automation runs.

### Bringing existing agents into conformance

If you already have an agent in use, adopt the playbook incrementally:

1. Inventory agents, owners, tools, side effects, and credentials.
2. Assign execution classes and complete scenario-based risk assessments.
3. Introduce typed inputs, outputs, and tool contracts.
4. Move state-changing agents onto a durable execution engine.
5. Add hard budgets and correlated telemetry.
6. Establish smoke, regression, safety, and trajectory evaluations.
7. Add human approval to consequential actions.
8. Complete the production-readiness checklist.

### What to expect from your platform

Good defaults make the right path the easy path. You should be able to get:

- an explanation for every failed gate that links it to the capability, risk
  scenario, policy rule, and an example remedy;
- a preview of what a release will be allowed to do before you submit it;
- how-to guides for common tasks, a migration checklist for existing agents,
  and a clear exception path for genuinely unsupported needs; and
- support that studies recurring friction and improves the standard.

If these are missing, say so rather than building a private workaround.

## Check the decision register

The playbooks leave some decisions to your organization: approved
integrations, identity approach, isolation model, orchestration criteria,
policy-distribution service levels, data handling, risk thresholds, and
release authorities. Your organization should record each in a versioned
decision register, with its evidence, accountable owner, effective date,
review trigger, and replacement plan. Check it before you design around an
assumption, and tell an approved standard apart from a proposed next step.

## Common pitfalls

- **Finding the approver at release time.** Nobody knew who could promote
  the agent, so the release waited.
- **Self-approved authority.** The developer who proposed broader access also
  approved it.
- **Inconsistent metadata.** The agent's telemetry lacked release, tenant, or
  policy revision, so nobody could see what it did or who it did it for.
- **Deadline-driven stages.** A use case moved to production because a date
  arrived, not because its exit evidence did.

## Before you move on

You are ready to start the
[Agent Playbook](../agent-playbook/README.md) when you can answer yes to each
of these:

- [ ] Every decision in the table has a named person or staffed group.
- [ ] We know who approves our release and any authority expansion, and it
  is not us.
- [ ] Our agent emits the correlation metadata the oversight views need,
  without secrets or raw content in identifiers.
- [ ] We know which adoption stage we are in and what evidence moves us on.
- [ ] We have checked the decision register for choices that affect our
  design.
