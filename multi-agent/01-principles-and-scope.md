# 1. Principles and scope

This guide is for developers composing several agents into one system. It
helps you decide whether you need more than one agent, and sets out the
principles later chapters build on. Each member already follows the
[single-agent guidance](../core/README.md); this covers what changes when
agents work together.

## What this playbook covers

This playbook applies when two or more model-driven agents work toward one
application outcome through delegation, handoff, review, voting, parallel
work, or shared coordination state. It applies however the agents are
deployed: one process or many services, the same or different models, and
in-process calls, a durable execution engine, queues, RPC, or another
transport.

A deterministic service, an ordinary tool call, or a fixed software module is
not an agent just because an agent invokes it.

## Do you need more than one agent?

Several agents cost more to build, test, and run than one, and fail in ways
a single agent cannot. You MUST document why a multi-agent design is
justified before adopting it. At least one of these benefits SHOULD be
material and backed by a testable hypothesis:

- capability or privilege isolation between specialists;
- context or sensitive-data segregation;
- independent review that measurably reduces important errors;
- parallel work that materially improves latency or coverage;
- distinct ownership, deployment, or operational lifecycles; or
- a durable business process with separately governed agent responsibilities.

You SHOULD NOT choose a multi-agent design only to create personas, divide a
prompt into roles, imitate an organization chart, or hide an oversized tool
catalog. Prefer a single conforming agent with skills and tools when it meets
the same outcome, safety, latency, and cost objectives with less complexity.

Your evaluation plan MUST include a baseline that can test the claimed
benefit. The baseline is normally the best reasonable single-agent or
deterministic implementation.

## Core principles

These principles extend the
[single-agent core principles](../core/05-principles-and-scope.md)
to the graph.

### Inherit, then extend

Every reachable member agent MUST independently satisfy the single-agent guidance.
The system contract adds composition requirements; it MUST NOT copy or
silently override member contracts.

### The graph is a governed capability

Membership, roles, and interaction edges are capabilities, just as tools are
for one agent (see
[least capability](../core/05-principles-and-scope.md#least-capability)).
Discovering an agent or endpoint is not permission to invoke it. Production
systems MUST use an explicit allowlisted graph.

### Authority only attenuates

An agent cannot grant authority it does not have. The effective authority for
an interaction is the intersection of system policy, the caller's delegable
scope, the callee's capability, the authenticated actor's scope, the tenant
context, and the current deterministic policy decision. Passing work along can
only narrow it ([chapter 5](05-delegation-and-interactions.md#authority-attenuation)).

### Typed boundaries, minimal context

Every interaction uses typed, bounded inputs and outputs. Pass the minimum
context and data the assigned objective needs. A transcript or shared memory
is not an implicit source of authorization or truth.

### Deterministic control, probabilistic collaboration

This is the single-agent
[deterministic control principle](../core/05-principles-and-scope.md#deterministic-control-probabilistic-assistance)
extended to coordination. Use deterministic code for admission, authorization,
routing constraints, budget allocation, state transitions, conflict policy,
approval, side effects, and termination. Models may propose plans, choose
among allowlisted routes, and synthesize evidence within those controls.

### One owner for system truth

The system MUST identify the deterministic authority for workflow state,
accepted evidence, conflict resolution, final status, and externally visible
effects. Agents may propose changes but MUST NOT mutate shared truth without
going through that authority.

### Bounded autonomy

Depth, fan-out, concurrency, rounds, agent runs, model requests, tool calls,
time, tokens, and spend all have explicit finite limits. Dynamic membership
and recursive delegation are opt-in. They need separate justification,
admission controls, runtime bounds, and evidence, but they are valid when a
static composition cannot meet the need efficiently.

### Durable composition

The single-agent rule that side effects run durably still holds for each
member. In addition, long-running coordination, and any path through the
system that can reach a side effect, executes through a durable execution
engine. Workflows own deterministic coordination; durable steps own agent
runs, model calls, tools, and other nondeterministic I/O.

### Evidence at both levels

Member evals prove individual behavior. System evals prove routing, handoffs,
aggregation, failure containment, termination, and end-to-end outcomes.
Neither substitutes for the other.

### Quality-adjusted system cost

Optimize total cost per successful, compliant system outcome. Count nested
agent runs, failed branches, retries, infrastructure, review, and recovery,
not only the coordinator's model usage.

## Terms you will need

- **Agent:** one independently contracted model-driven component.
- **System:** the versioned composition that coordinates member agents.
- **Role:** a system-specific responsibility assigned to a member.
- **Interaction:** one typed invocation or transfer across an allowed edge.
- **Delegation:** the caller assigns bounded work and later resumes control.
- **Handoff:** control transfers to another member without automatically
  returning to the caller.
- **Orchestrator:** deterministic code that owns system state and
  coordination.
- **Coordinator:** an agent allowed to propose or select bounded
  interactions.
- **Composition manifest:** the resolved, immutable bill of materials for a
  system release.

A model-driven coordinator is not the orchestrator and MUST NOT
become the sole authority for policy, approval, state integrity, or
termination.

## Execution class and governance tier for the system

Composition can raise the assurance a system needs; it never lowers it.

The system's effective execution class MUST be at least the highest class
required by every reachable interaction, tool, and side effect. It may be
higher than any member's default class, because coordination itself may be
long-running or stateful. (The classes themselves are defined in the Agent
Playbook's [execution classes](../core/05-principles-and-scope.md#execution-classes).)

The system governance tier MUST be at least the highest of: the tiers of its
reachable members, applicable legal or policy floors, capability floors, and
inherent system-level risk scenarios. A low member tier does not reduce a
higher system tier.

Residual risk affects the launch decision, not the minimum assurance required
by the system's inherent risk and mandatory floors.

## Common pitfalls

- **Roles without a reason.** The agents were personas splitting one prompt,
  and a single agent did as well for less.
- **A coordinator that is also the orchestrator.** A model ended up deciding
  approval, state, or termination because no deterministic code owned them.
- **Assuming member conformance is enough.** Each agent passed its own gates,
  but the system amplified authority or cost across the edges.

## Conformance

A system conforms when:

- The multi-agent admission test is documented.
- Every reachable member conforms to the single-agent guidance.
- The System Spec, composition manifest, and system risk assessment agree.
- Membership and interaction edges are explicitly allowlisted and validated.
- Required execution, authorization, data-flow, budget, and termination
  policies are enforced at startup and runtime.
- Member and system evaluation gates pass with reproducible provenance.
- Production readiness, residual-risk acceptance, and exceptions are
  complete, approved, and unexpired.

## Before you move on

- [ ] We wrote down which multi-agent benefit we expect and how a test could
  disprove it.
- [ ] We have a single-agent or deterministic baseline to compare against.
- [ ] Every member we plan to use already conforms to the single-agent guidance.
- [ ] We know the system's execution class and governance tier floor.
