# 5. Principles and scope

This chapter is for developers building an agent that will run in production.
It explains the ideas the rest of the playbook builds on, helps you pick the
execution class that fits your agent, and says what "conforming" means. Read
it first: most requirements in later chapters follow from the principles
here, and the execution class you choose decides which of them apply to you.

## What this playbook is for

The playbook helps you build agents that behave predictably, are safe to give
authority to, and can be operated by someone other than you. It aims for:

- a predictable architecture from one agent project to the next;
- explicit trust, authorization, and side-effect boundaries;
- durable recovery for long-running or state-changing work;
- reproducible behavior and release decisions;
- observable quality, safety, latency, and cost; and
- clear ownership throughout the agent's life.

## Where it applies

The standard applies to production agents regardless of the framework,
language, or model provider you use, and however the agent is exposed: APIs,
user interfaces, background jobs, schedules, or event-driven workflows.

If your agent is one member of a multi-agent system, it MUST still satisfy
the agent contract on its own. The composition is governed by the
[Multi-agent systems](../multi-agent/README.md) section.

The rest of the playbook assumes you have already settled the use case,
problem brief, and ownership. Chapters 1 to 4 of Core concepts cover those
decisions and the
[zero-trust principles](03-zero-trust-principles.md) that the
principles below put into practice.

## Core principles

Each principle is a design habit. Later chapters turn them into specific
requirements.

### Declarative intent, typed enforcement

Declare what the agent is in a declarative agent specification (the Agent
Spec): identity, instructions, model defaults, retry budgets, timeouts,
capabilities, and metadata. Enforce what happens at runtime with
schema-validated types for inputs, dependencies, outputs, policies, and tool
contracts. The spec is easy to review; the types make sure reality matches it.

### Least capability

Give the agent only the skills, tools, data, network access, and credentials
its purpose needs. Being able to discover a capability is not permission to
use it. Every extra capability is something an injected instruction or a model
mistake can reach.

### Deterministic control, probabilistic assistance

Use deterministic code for authorization, budget enforcement, approval,
routing constraints, validation, and business invariants. Use the model for
interpretation, synthesis, planning, and judgment inside those boundaries. If
a rule must always hold, do not ask the model to remember it.

### Durable side effects

Any agent that can modify external state MUST run on a durable execution
engine. Model requests and I/O execute as durable steps; deterministic
coordination executes in workflows. This is what lets a crashed run resume
without repeating or losing an action.

### Human control for consequential action

When a person must approve an action, the approval is bound to the exact
action, arguments, actor, tenant, and policy version. A model cannot grant or
infer approval.

### Evaluation before intuition

Accept behavioral changes on evidence: deterministic tests, offline evals,
trajectory checks, durability scenarios, and staged production observation.
A change that "looks better" in a few manual tries is not evidence.

### Quality-adjusted cost

Optimize cost per successful, compliant outcome. A cheaper run that lowers
task success or safety is not an optimization.

### Observable by design

You should be able to attribute every production run to a specific agent,
configuration, model, skill set, tool set, worker build, and evaluation
baseline. Without that, you cannot explain a failure or compare releases.

## Execution classes

The execution class describes how your agent's work runs. Pick the lowest
class that covers what the agent can do; the most consequential tool you
enable sets the floor.

### Ephemeral

For short-lived, low-risk, request-response work such as classification,
extraction, summarization, and read-only retrieval.

- Durable execution is optional.
- Tools MUST be read-only.
- The agent MUST NOT create externally visible side effects.
- A failure may require the caller to retry the run.

### Durable

For long-running work, recoverable processes, or any side effect.

- The run MUST execute inside a durable workflow.
- Model, tool, MCP, database, filesystem, and network I/O MUST execute in
  durable steps.
- Side-effecting durable steps MUST be idempotent or use stable idempotency
  keys.
- Retry, timeout, cancellation, and compensation behavior MUST be explicit.

### Human-governed

For consequential operations that need accountable human review.

- All durable requirements apply.
- The workflow MUST pause before consequential action.
- The approver MUST be authenticated outside model control.
- Approval MUST be recorded and bound to a canonical action hash.
- Materially changed arguments MUST require new approval.

Best practices:

- **Start lower than you think you need.** A read-only ephemeral release
  produces evaluation data and tool interfaces at little risk, and most of it
  carries over when you add actions.
- **Treat a class change as a new release decision.** Moving from ephemeral
  to durable, or adding a consequential tool, changes your risk assessment
  and evaluation plan, not just configuration.

## What conformance means

Your service conforms when:

- all production agents satisfy the [canonical contract](07-agent-contract.md);
- all exposed tools and skills satisfy their chapters
  ([tools](09-tools.md), [skills](08-skills.md));
- execution class and risk controls are enforced at startup and at runtime;
- required evaluation and production gates pass; and
- exceptions are documented, approved, and unexpired.

## Common pitfalls

- **Letting the prompt enforce policy.** An instruction such as "never refund
  more than the limit" is a hope, not a control. Put the limit in code.
- **Treating discovered tools as granted tools.** A tool that is reachable is
  not therefore allowed; allowlist explicitly.
- **Choosing ephemeral for an agent that writes.** If any enabled tool changes
  external state, the agent is at least durable.
- **Approving intent instead of an action.** "Yes, go ahead" with no bound
  arguments lets the agent change what it does after approval.

## Before you move on

- [ ] You can state the agent's purpose and the least capability it needs.
- [ ] You have chosen an execution class that covers its most consequential
  tool.
- [ ] Every rule that must always hold is enforced in deterministic code.
- [ ] You know which later chapters apply to your class.
