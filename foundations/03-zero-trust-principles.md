# 3. Zero-trust principles for agents

An agent is an untrusted workload that acts on someone's behalf. It is never a
trusted insider. Its presence on an internal network, a successful evaluation,
or a previously approved conversation does not confer continuing authority.
Every request needs an authenticated identity, a current authorization
decision, and an appropriate resource boundary.

Zero trust is a design direction, not a certification or a claim that failure
is impossible. Agents make it more pressing than for ordinary services for
three reasons:

- **The decision-maker can be steered.** A model's choices can be influenced by
  any content it reads: documents, tool results, web pages, and messages from
  other agents. Instructions embedded in that content are data, not commands.
- **Capability is easy to over-grant.** A broad tool or a shared credential is
  convenient during a prototype and dangerous in production. Discovering a tool
  is not permission to use it.
- **Actions compound.** Individually reasonable permissions combine into
  harmful paths, such as production read access plus the ability to post
  externally, which together create an exfiltration route.

## Principles

| Principle | What it requires | Evidence to expect | Where the playbook applies it |
| --- | --- | --- | --- |
| Every agent has its own identity | Each agent release has a distinct, verifiable workload identity bound to its version and contents. Credentials are never shared between agents or borrowed from developers. | Identity bound to the capability manifest and build; no shared or personal credentials. | [Identity and authorization](../agent-playbook/10-security-and-governance.md#identity-and-authorization) |
| Deny by default, least capability by construction | Skills, tools, data, network destinations, and credentials are explicitly allowlisted. Default templates grant no arbitrary shell, broad egress, production credentials, or open tool discovery. Additions need a declared purpose and a reviewed rule. | Capability diff, negative tests, and the effective runtime policy. | [Least capability](../agent-playbook/01-principles-and-scope.md#least-capability), [tool standard](../agent-playbook/05-tools.md) |
| Explicit authority | Each capability names its action, resource scope, tenant, data class, approval requirement, and budget. The model may propose an action; an independent, deterministic control decides whether it executes. | Versioned capability manifest and a recorded policy decision at every consequential boundary. | [Deterministic control](../agent-playbook/01-principles-and-scope.md#deterministic-control-probabilistic-assistance) |
| Authority is granted per action and expires | Consequential actions need an exact, bound approval for that action, its arguments, actor, tenant, and policy version. Approvals are single-use and time-limited. A model cannot grant or infer approval. | Approval records with hash, scope, expiry, and consumption. | [Human approval](../agent-playbook/06-durable-execution.md#human-approval) |
| Mediate and verify every call | Tool and model calls pass through a control point that authenticates the caller, checks authorization, and records the decision. Content from tools and other agents is treated as untrusted. | Gateway or equivalent decision logs, and tests showing that unlisted tools and destinations are refused. | [Untrusted content](../agent-playbook/10-security-and-governance.md#untrusted-content) |
| Defense across independent boundaries | Application authorization, call mediation, process isolation, runtime visibility, and destination authorization each cover different failures. No single layer is trusted to hold alone. | A control map plus bypass tests showing the intended coverage. | [Isolation](../agent-playbook/10-security-and-governance.md#isolation), [threat model](../agent-playbook/10-security-and-governance.md#threat-model) |
| Assume breach | Design as if an agent is already compromised: isolate its execution, limit what it can reach, observe what it does, and keep blast radius small. | Isolation configuration, egress restrictions, and runtime observation in place. | [Isolation](../agent-playbook/10-security-and-governance.md#isolation) |
| Evidence before trust | Quality, safety, durability, isolation, and operational readiness have distinct gates. Good average performance cannot offset a failed critical control. Trust is earned per release, not inherited. | Dataset digests, test results, scenario coverage, policy verification, and approvals tied to the release. | [Release gates](../agent-playbook/07-evaluation.md#release-gates), [production readiness](../agent-playbook/11-production-readiness.md) |
| Observation never grants permission | Watching an agent run may propose the access it seems to need, but proposals are reviewed against declared purpose and central invariants. Behavior seen during testing is not authorization. | Reviewed policy diffs showing expansion and contraction of authority. | [Change classes](../agent-playbook/10-security-and-governance.md#change-classes) |
| Revocable execution | New work and tool access can be disabled separately from terminating running work. Control freshness is enforced, and recovery is tested. | Drill results, revocation acknowledgements, and measured stop times. | [Kill switches](../agent-playbook/10-security-and-governance.md#kill-switches) |

## Applying the principles

- **Review combinations, not rules in isolation.** Data flows, delegation, and
  identity propagation can combine privileges across tools or agents. A
  generic code runner can bypass a narrow tool interface. The
  [Multi-Agent Systems Playbook](../multi-agent-playbook/05-delegation-and-interactions.md#authority-attenuation)
  requires authority to attenuate, never amplify, across delegation.
- **Fail closed at consequential boundaries.** When the authorization or
  policy service is unavailable or stale, block new consequential actions
  rather than falling back to weaker controls, and tell users why.
- **Make the effective policy visible.** Owners approve the policy that will
  actually be enforced, not only its templates. A readable diff shows how a
  release changes authority.
- **Do not start work without its controls.** An agent must not begin
  executing while a required control is missing, stale, or not yet applied.
- **Keep claims precise.** State which controls are verified in which
  environment. A passing local check does not show that production isolation,
  mediation, or revocation works.

## Questions to ask of any agent design

1. What identity does this agent act under, and could another agent or a
   person use the same credential?
2. What is the most harmful action it can take, and what independent control
   stops it?
3. Which content does it read that someone else could have written?
4. Which combination of its permissions creates a path no single permission
   reveals?
5. If it were compromised now, what could it reach, and how quickly could we
   stop it?
6. What evidence, specific to this release, shows each answer above is true?
