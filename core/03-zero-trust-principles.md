# 3. Zero-trust principles for agents

This guide is for the developers who will build the agent. It explains why
you should design your agent as an untrusted workload acting on someone's
behalf, and what that means in practice for its identity, its permissions,
and the evidence you collect. Chapters 5 to 12 and
[Advanced concepts](../advanced/README.md) turn these principles into
requirements; this guide explains the reasoning so the requirements make
sense when you meet them.

## Why agents are not trusted insiders

Your agent's presence on an internal network, a successful evaluation, or a
previously approved conversation does not give it continuing authority. Every
request needs an authenticated identity, a current authorization decision,
and an appropriate resource boundary.

Zero trust is a design direction, not a certification or a claim that failure
is impossible. It matters more for agents than for ordinary services, for
three reasons:

- **The decision-maker can be steered.** A model's choices can be influenced
  by any content it reads: documents, tool results, web pages, and messages
  from other agents. Instructions embedded in that content are data, not
  commands.
- **Capability is easy to over-grant.** A broad tool or a shared credential
  is convenient in a prototype and dangerous in production. Discovering a
  tool is not permission to use it.
- **Actions compound.** Individually reasonable permissions combine into
  harmful paths. Production read access plus the ability to post externally
  is an exfiltration route.

## Give the agent its own, narrow authority

**Every agent has its own identity.** Each release has a distinct, verifiable
workload identity bound to its version and contents. Never share credentials
between agents or borrow a developer's. Expect to show that the identity is
bound to the capability manifest and build, with no shared or personal
credentials (see
[identity and authorization](09-tools.md#identity-and-authorization)).

**Deny by default, least capability by construction.** Explicitly allowlist
skills, tools, data, network destinations, and credentials. Your starting
template should grant no arbitrary shell, broad egress, production
credentials, or open tool discovery. Every addition needs a declared purpose
and a reviewed rule. A capability diff, negative tests, and the effective
runtime policy are your evidence (see
[least capability](05-principles-and-scope.md#least-capability)
and [tools](09-tools.md)).

**Explicit authority.** Each capability names its action, resource scope,
tenant, data class, approval requirement, and budget. The model may propose
an action; an independent, deterministic control decides whether it runs.
Keep a versioned capability manifest and record a policy decision at every
consequential boundary (see
[deterministic control](05-principles-and-scope.md#deterministic-control-probabilistic-assistance)).

**Authority is granted per action and expires.** A consequential action needs
an exact approval bound to that action, its arguments, actor, tenant, and
policy version. Approvals are single-use and time-limited, and a model cannot
grant or infer one. Approval records carry the hash, scope, expiry, and
consumption (see
[human approval](../advanced/01-durable-execution.md#human-approval)).

## Check every call and assume compromise

**Mediate and verify every call.** Tool and model calls pass through a control
point that authenticates the caller, checks authorization, and records the
decision. Treat content from tools and other agents as untrusted. Decision
logs from a gateway or equivalent, and tests showing that unlisted tools and
destinations are refused, are the evidence (see
[untrusted content](09-tools.md#untrusted-content)).

**Defense across independent boundaries.** Application authorization, call
mediation, process isolation, runtime visibility, and destination
authorization each catch different failures. Do not trust any single layer
to hold alone. Show a control map plus bypass tests demonstrating the
intended coverage (see
[isolation](../advanced/03-security-and-governance.md#isolation) and
[threat model](../advanced/03-security-and-governance.md#threat-model)).

**Assume breach.** Design as if the agent is already compromised: isolate its
execution, limit what it can reach, observe what it does, and keep the blast
radius small. Isolation configuration, egress restrictions, and runtime
observation should all be in place.

**Revocable execution.** You can disable new work and tool access separately
from terminating running work. Control freshness is enforced and recovery is
tested. Drill results, revocation acknowledgements, and measured stop times
are the evidence (see
[kill switches](12-production-readiness.md#kill-switches)).

## Earn trust with evidence

**Evidence before trust.** Quality, safety, durability, isolation, and
operational readiness have distinct gates, and good average performance
cannot offset a failed critical control. Trust is earned per release, not
inherited. Tie dataset digests, test results, scenario coverage, policy
verification, and approvals to the release (see
[release gates](10-evaluation.md#release-gates) and
[production readiness](12-production-readiness.md)).

**Observation never grants permission.** Watching the agent run may propose
the access it seems to need, but you review each proposal against the
declared purpose and central invariants. Behavior seen in testing is not
authorization. Reviewed policy diffs should show authority contracting as
well as expanding (see
[change classes](../advanced/03-security-and-governance.md#change-classes)).

## Best practices

- **Review combinations, not rules in isolation.** Data flows, delegation,
  and identity propagation can combine privileges across tools or agents,
  and a generic code runner can bypass a narrow tool interface. The
  [Multi-agent systems](../multi-agent/05-delegation-and-interactions.md#authority-attenuation)
  requires authority to attenuate, never amplify, across delegation.
- **Fail closed at consequential boundaries.** When the authorization or
  policy service is unavailable or stale, block new consequential actions
  rather than falling back to weaker controls, and tell users why.
- **Make the effective policy visible.** Owners approve the policy that will
  actually be enforced, not only its templates. A readable diff shows how
  each release changes authority.
- **Do not start work without its controls.** An agent must not begin
  executing while a required control is missing, stale, or not yet applied.
- **Keep claims precise.** Say which controls are verified in which
  environment. A passing local check does not show that production
  isolation, mediation, or revocation works.

## Common pitfalls

- **Prototype credentials that never leave.** The agent still runs on a
  developer's token, so nobody knows what it actually needs.
- **Trusting what the agent read.** A document or tool result told the agent
  to do something, and it did.
- **Granting what testing observed.** The test run captured a mistake or an
  injected instruction, and it became policy.
- **One wall.** A single gateway or sandbox was assumed to stop everything,
  and nothing caught its failure.

## Before you move on

Ask these of your design. You are ready for the
[operating model](04-operating-model.md) when you can answer each one with
evidence specific to this release:

- [ ] What identity does the agent act under, and could another agent or a
  person use the same credential?
- [ ] What is the most harmful action it can take, and what independent
  control stops it?
- [ ] Which content does it read that someone else could have written?
- [ ] Which combination of its permissions creates a path no single
  permission reveals?
- [ ] If it were compromised now, what could it reach, and how quickly could
  we stop it?
