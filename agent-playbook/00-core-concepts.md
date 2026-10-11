# 0. Core concepts

Start here if you are new to building agents. This chapter defines the
building blocks the rest of the playbook relies on, explains how they differ,
and shows when to use each one and where it lives in a repository. Later
chapters link back here instead of redefining these terms.

## The mental model

An agent is a loop. A **model** reads its **context** (instructions, the
conversation, and results so far), decides what to do next, and either
answers or asks to call a **tool**. The application runs the tool, adds the
result to the context, and the loop repeats until the agent produces its
output or hits a limit.

Everything else in this playbook shapes that loop:

- **Instructions** tell the model what it is for and what it must never do.
- **Tools** let it read or change things outside itself.
- **MCP servers** supply tools (and data) from a separate process or service.
- **Skills** give it know-how for a class of tasks, loaded only when relevant.
- **Deterministic code** does anything that must be exact, outside the model.
- **Workflows** make the loop durable, so it survives crashes and can wait for
  a human.
- **Evaluations** measure whether the loop behaves as intended.

## Definitions

### Model

The large language model that reads context and produces text or tool calls,
such as a Claude, GPT, or Gemini model. The model is stateless: it knows only
what is in the current context. Production agents select models through a
versioned model policy rather than hard-coding a model name (see
[Canonical agent contract](03-agent-contract.md#model-policy)).

### Agent

A model plus its instructions, tools, skills, typed inputs and outputs,
budgets, and limits, packaged as one versioned unit with an owner. In this
playbook an agent is defined declaratively by an **Agent Spec** and assembled
by a factory (see [Canonical agent contract](03-agent-contract.md)).

> Example: a `customer-support` agent that answers order questions using order
> and customer records, and proposes refunds for human approval.

### Instructions

Text included in every model request that sets the agent's purpose, rules,
and output expectations. Also called the system prompt. Instructions are
always loaded, so they cost tokens on every request and should stay short.

> Example: "Distinguish verified facts from assumptions. Never claim a refund
> was issued unless the refund tool confirms it."

Instructions guide the model; they do not enforce anything. A rule that must
always hold, such as "refunds above $500 need approval", belongs in code or
policy, not only in instructions.

### Context

Everything the model sees in one request: instructions, conversation history,
tool definitions, loaded skills, and tool results. The context window is
finite and every token costs money and latency, so what goes into context is a
design decision (see [Cost optimization](09-cost-optimization.md#context)).

### Tool

A typed function the model can ask the application to call. The model sees
the tool's name, description, and input schema; the application validates the
arguments, checks authorization, runs the code, and returns the result. Tools
are how an agent **acts or fetches data**.

> Example: `lookup_order(order_id) -> Order` reads an order;
> `issue_refund(order_id, amount) -> RefundResult` changes one.

Every tool is classified by its effect: `read`, `write_reversible`, or
`write_consequential` (see [Tool standard](05-tools.md)). The model only
requests a tool call; your code decides whether it runs.

### Toolset

A named group of related tools registered with an agent as one unit, such as
all tools for the CRM. Toolsets are the unit you allowlist, filter, prefix,
or wrap with approval rules.

### MCP server

A separate program that exposes tools, read-only data (resources), and prompt
templates over the [Model Context Protocol](https://modelcontextprotocol.io),
a standard interface any compatible client can use. Your agent is the **MCP
client**: it connects to the server and the server's tools appear to the model
like any other tools.

> Example: your company runs a CRM MCP server exposing `get_customer` and
> `list_tickets`. The support agent, Claude Code, and Codex can all use it
> without each re-implementing the CRM integration.

An MCP server is a **way to deliver tools**, not a different kind of
capability. Its tools still need effect classification, authorization, and an
allowlist. Because it is code you may not own, it is also a supply-chain
dependency (see [Security and governance](10-security-and-governance.md#mcp-and-supply-chain)).

### Skill

A folder containing a `SKILL.md` file of instructions, with optional
references, examples, and scripts, that teaches an agent **how to approach a
class of tasks**. Skills follow the open
[Agent Skills specification](https://agentskills.io/specification). The model
first sees only each skill's name and description, and loads the full
instructions when a task matches. This progressive loading keeps the context
small when many skills are available.

> Example: an `incident-triage` skill that lists the steps for investigating
> an outage, which diagnostic tools to use in what order, and what a finished
> report must contain.

A skill gives knowledge, not the ability to act. If a skill's procedure says
"check the error rate", a tool must exist to do it. Skills cannot grant
permissions or enforce policy (see [Skill standard](04-skills.md)).

There are two audiences for skills, using the same format:

- **Runtime skills** are loaded by the agent you are building, in production.
  They live in your application package.
- **Development skills** are loaded by the coding agent you build with, such
  as Codex or Claude Code. They teach it your standards, for example this
  repository's `design-agent-capabilities` skill.

### Project instructions (AGENTS.md)

A Markdown file at the repository root that coding agents read at the start
of every session: build commands, conventions, layout, and rules. It is the
always-on counterpart to development skills, which load on demand. Codex
reads `AGENTS.md`; Claude Code reads `CLAUDE.md`, which should contain the
single line `@AGENTS.md` so both tools share one file.

### Deterministic code

Ordinary application code: validation, calculations, policy checks, and
business rules. Anything that must give the same answer every time belongs
here, not in a prompt. A tool often wraps deterministic code so the model can
request it.

### Workflow and activity

A [Temporal](https://docs.temporal.io/) workflow is a durable, replayable
orchestration: it records every step, so it can resume after a crash, wait
days for a human approval, and avoid repeating side effects. An activity is a
single step that does I/O, such as a model call or a tool call. Agents that
change external state run their side effects as activities (see
[Temporal execution standard](06-temporal-execution.md)).

### Evaluation

A repeatable test of agent behavior against a dataset of cases, scored by
deterministic checks or model-based judges. Unlike unit tests, evaluations
measure probabilistic behavior: answer quality, whether the right tools were
called, safety, latency, and cost (see [Evaluation standard](07-evaluation.md)).

## Skill vs. tool vs. MCP server

|                             | Tool                                        | MCP server                                                 | Skill                                       |
| --------------------------- | ------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------- |
| **What it gives the agent** | An action or data lookup                    | A set of tools (plus resources and prompts) from elsewhere | Know-how: a procedure, rules, examples      |
| **What it is**              | A typed function in your code               | A separate process or service speaking MCP                 | A folder with `SKILL.md`                    |
| **Runs where**              | In your application, or a Temporal activity | In its own process, locally or over the network            | Nowhere; it is text loaded into context     |
| **In context**              | Name, description, schema on every request  | Same as tools, for each exposed tool                       | Name and description; body only when used   |
| **Can change the world**    | Yes, if it writes                           | Yes, if its tools write                                    | No; it can only describe what tools to call |
| **Who enforces safety**     | Your code: validation, auth, approval       | The server and your client-side filters and approval       | Nothing; skill text is guidance only        |
| **Reusable across**         | Agents in your codebase                     | Any MCP client, in any language                            | Any Agent Skills client                     |
| **Example**                 | `lookup_order`                              | Company CRM server                                         | `incident-triage`                           |

They are complementary, not alternatives. A typical capability uses all
three: an MCP server provides the CRM tools, your own tool wraps the refund
calculation, and a skill describes the refund procedure that uses both.

## When to use what

Ask these questions in order and stop at the first "yes":

1. **Must the result be exact and repeatable?** Use deterministic code. If the
   model needs to trigger it, wrap it in a tool.
2. **Is it a rule that applies to every run?** Put it in instructions, and
   enforce it in code or policy if a violation would cause harm.
3. **Does the agent need to read or change something outside itself?** Use a
   tool.
   - If a maintained MCP server already provides it, or the capability must be
     shared across many agents, clients, or languages, consume or build an
     **MCP server** and allowlist only the tools you need.
   - Otherwise write a **function tool** in your package. It is simpler to
     test, type, and run inside a Temporal activity.
4. **Does the agent need a procedure or domain knowledge for some tasks but
   not others?** Write a **runtime skill**.
5. **Does your coding agent need to know your conventions?** Put facts needed
   in every session in **AGENTS.md**; put task-specific procedures in a
   **development skill**.

### Common mistakes

- **A skill that should be a tool.** "Calculate the refund amount" in skill
  text means the model does arithmetic. Make it a tool backed by code.
- **A tool that should be a skill.** A `get_refund_policy` tool that returns
  a fixed block of text is a skill with extra steps.
- **Instructions as enforcement.** "Never refund more than $500" in a prompt
  is a request, not a control. Enforce the limit in the tool.
- **Connecting a whole MCP server.** Exposing every tool a server offers
  bloats context and widens the attack surface. Filter to an allowlist.
- **Everything in AGENTS.md.** Long, task-specific procedures there load into
  every session. Move them into development skills.
- **Mixing up skill audiences.** Runtime skills for your product do not go in
  `.agents/skills/`, and development skills do not ship in your package.

## Where things live

| What                         | Location                                        | Used by                   |
| ---------------------------- | ----------------------------------------------- | ------------------------- |
| Agent Spec                   | `src/<package>/agents/<agent>/agent.yaml`       | Your agent at startup     |
| Instructions                 | `src/<package>/agents/<agent>/instructions/`    | Your agent, every request |
| Agent-private tools          | `src/<package>/agents/<agent>/tools/`           | That agent                |
| Shared tools and toolsets    | `src/<package>/tools/<domain>/`                 | Several agents            |
| Agent-private runtime skills | `src/<package>/agents/<agent>/skills/`          | That agent                |
| Shared runtime skills        | `src/<package>/skills/`                         | Several agents            |
| MCP server connections       | Toolset definitions in `src/<package>/tools/`   | Your agent                |
| MCP servers you build        | Their own package or service                    | Any MCP client            |
| Project instructions         | `AGENTS.md`, plus `CLAUDE.md` importing it      | Codex and Claude Code     |
| Development skills           | `.agents/skills/`, linked from `.claude/skills` | Codex and Claude Code     |
| Workflows and activities     | `src/<package>/workflows/`, `activities/`       | Temporal workers          |
| Evaluations                  | `evals/`                                        | CI and release gates      |

The full layout is in [Reference architecture](02-reference-architecture.md).

## Worked example

A `customer-support` agent answers order questions and proposes refunds.

| Need                                              | Building block                                                                          |
| ------------------------------------------------- | --------------------------------------------------------------------------------------- |
| "Never promise a refund before approval"          | Instructions                                                                            |
| Refund eligibility and amount                     | Deterministic code, exposed as the `quote_refund` tool                                  |
| Read an order                                     | Function tool `lookup_order` (`read`)                                                   |
| Issue a refund                                    | Function tool `issue_refund` (`write_consequential`), human approval, Temporal activity |
| Customer profile and ticket history               | Company CRM MCP server, filtered to two read tools                                      |
| How to handle a refund dispute, step by step      | Runtime skill `refund-disputes`                                                         |
| Teach Codex or Claude Code to add tools correctly | Development skill `design-agent-capabilities`                                           |

The tools and MCP connection in PydanticAI:

```python
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPToolset

from acme.orders import Order, OrdersClient


@dataclass
class SupportDeps:
    orders: OrdersClient


# Connect to the CRM MCP server, exposing only the two read tools this agent needs.
crm = MCPToolset("https://crm.internal.example/mcp").filtered(
    lambda ctx, tool: tool.name in {"get_customer", "list_tickets"}
)

agent = Agent(
    model,  # resolved from the agent's model policy
    deps_type=SupportDeps,
    instructions="Answer order questions using verified records. Never promise a refund before approval.",
    toolsets=[crm],
)


@agent.tool
async def lookup_order(ctx: RunContext[SupportDeps], order_id: str) -> Order:
    """Return an order's status, items, and payment details."""
    return await ctx.deps.orders.get(order_id)
```

In production the agent is assembled from its Agent Spec by a factory rather
than constructed inline; see [Reference implementation](12-reference-implementation.md).

## Other terms

| Term               | Meaning                                                                               | Defined in                                                             |
| ------------------ | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Execution class    | How an agent runs: `ephemeral`, `durable`, or `human_governed`                        | [Principles and scope](01-principles-and-scope.md#execution-classes)   |
| Effect class       | What a tool does to external state: `read`, `write_reversible`, `write_consequential` | [Tool standard](05-tools.md#effect-classification)                     |
| Governance tier    | Assurance required by an agent's inherent risk                                        | [Agent risk assessment](13-risk-assessment.md)                         |
| Allowlist          | The explicit list of skills and tools an agent may use; everything else is denied     | [Skill standard](04-skills.md#selection)                               |
| Trajectory         | The sequence of model and tool calls an agent made during a run                       | [Evaluation standard](07-evaluation.md#trajectory-evaluation)          |
| LLM judge          | A model used to score another model's output against a rubric                         | [Evaluation standard](07-evaluation.md#llm-judges)                     |
| Idempotency        | Running an operation twice has the same effect as running it once                     | [Temporal execution standard](06-temporal-execution.md#idempotency)    |
| Human approval     | A recorded human decision required before a consequential action runs                 | [Temporal execution standard](06-temporal-execution.md#human-approval) |
| Multi-agent system | Several agents coordinated under one governed contract                                | [Multi-Agent Systems Playbook](../multi-agent-playbook/README.md)      |
