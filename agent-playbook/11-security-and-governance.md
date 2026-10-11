# 11. Security and governance

This chapter is for developers whose agent will run with real credentials,
data, or users. It covers the controls you build, the evidence you hand your
reviewers, and what you do when something goes wrong.

Execution class determines how work runs. The governance tier determines how
rigorously the agent must be governed.

The basics every agent needs, whatever its tier, live in Core:
[identity, untrusted content, and secrets](05-tools.md#identity-and-authorization)
in the tools chapter, and
[ownership, kill switches, and incident response](08-production-readiness.md#ownership)
in production readiness. This chapter adds what higher tiers and riskier
capabilities require.

## Governance tiers

You find your governance tier by running the
[agent risk assessment](12-risk-assessment.md): identify harm scenarios across
eight dimensions, score inherent and residual risk, apply mandatory floors,
link controls to evidence, and record acceptance. The Agent Spec declares the
assessment's governance tier. The highest material scenario determines the
tier; dimensions and scenarios MUST NOT be averaged.

The tier tells you which controls to build and which evidence to prepare:

| Tier | Typical controls |
| --- | --- |
| Low | Owner, typed contract, smoke evals, budgets, telemetry, peer review |
| Medium | Risk assessment, regression/safety/trajectory evals, staged deployment, domain review |
| High | Threat model, security/privacy review, human governance, adversarial evals, audit, canary |
| Critical | Independent assessment, dual control where appropriate, continuous eval, kill switch, formal recertification |

Some uses remain prohibited even with added controls; the
[regulatory and prohibited-use screen](12-risk-assessment.md#regulatory-and-prohibited-use-screen)
catches them.

## Threat model

Medium-, high-, and critical-tier agents maintain a threat model. Keep it
current. It covers users, trust boundaries, providers, tools, MCP, skills,
retrieval, memory, durable execution, approval, telemetry, audit, deployment,
and dependencies.

At minimum, consider:

- goal hijacking and indirect prompt injection;
- tool misuse and excessive agency;
- identity or privilege abuse;
- cross-tenant access and sensitive-data disclosure;
- memory, skill, or prompt poisoning;
- MCP and dependency compromise;
- unexpected code execution;
- denial of wallet;
- approval forgery or replay;
- duplicate side effects; and
- telemetry or audit evasion.

For each material threat, identify preventive, detective, and recovery
controls. They feed scenarios and controls in your
risk assessment.

## MCP and supply chain

External capabilities require an owner, an immutable identity or
version, a trust classification, authentication, egress rules, a data
classification, an effect classification, dependency monitoring, and a
revocation process.

MCP servers MUST be allowlisted, authenticated, pinned where possible, and
monitored for unexpected tool-list changes. Server descriptions and results
are untrusted. Dynamic installation in production is prohibited.

Agent frameworks, SDKs, and runtime libraries evolve quickly, and pre-1.0
releases may change behavior without notice. Production projects SHOULD pin
versions, review release notes, and run full compatibility evals before
upgrades, treating each upgrade as a behavioral change.

## Isolation

Isolation limits damage when other controls fail. Production agents
SHOULD use outbound network allowlists, restricted filesystems, immutable
artifacts, resource limits, isolated temporary storage, and no ambient
credentials. Arbitrary code execution is a distinct high-risk tool and
requires a sandbox, quotas, and strong artifact controls.

## Change classes

Classify each change so you know what evidence it needs before merge:

| Change | Additional requirements |
| --- | --- |
| Non-behavioral | Unit/static checks and peer review |
| Behavioral | Agent version, offline evals, baseline comparison, staged rollout |
| Security-sensitive | Security review, adversarial evals, threat-model update |
| Replay-sensitive | Replay tests, code-versioning plan, compatible build retention |

A change may belong to more than one class; it then needs the evidence of
each.

## Deployment

Use a progression that fits the governance tier:

```text
local → integration → staging → shadow → canary → gradual rollout → full release
```

Shadow mode MUST disable side effects. Promote a canary only on operational
and behavioral health. Rollback plans MUST account for active workflow
histories: you may need to keep a build that can continue in-flight workflows
even after routing new work to an earlier build.

## Exceptions and review

If you cannot meet a requirement, record an exception rather than quietly
skipping it. An exception records the waived requirement, justification, risk,
compensating controls, approver, scope, expiry, and re-review date.

Suggested maximum review intervals are 12 months for low, 6 months for medium,
3 months for high, and 1 month for critical governance tiers, adjusted for
organizational and regulatory requirements.

## Decommissioning

Stop new starts, inventory active
workflows, complete, cancel, or migrate them, keep a compatible build
available as required, revoke access, remove tool and MCP registrations,
retain required audit and eval artifacts, delete data by policy, and mark the
capability manifest retired.

## Common pitfalls

- **Trusting the prompt to enforce policy.** Injected content will override
  it; enforce authorization at the tool.
- **Untested kill switches.** A switch that has never been exercised is a
  plan, not a control.
- **Silent exceptions.** A skipped requirement without an expiry becomes
  permanent.

## Before you move on

- [ ] The governance tier comes from a current risk assessment.
- [ ] Owners are named, and a threat model exists for medium tier and above.
- [ ] Authorization is enforced deterministically at tool execution.
- [ ] Kill switches and the incident runbook are tested.
- [ ] Every waived requirement has a recorded, unexpired exception.
