# Playbooks

Guides, best practices, and education for designing, building, and operating
production AI agents and multi-agent systems.

The playbooks are technology-neutral. They explain what good looks like and
why: the contracts, controls, evidence, and decisions that make an agent safe
to run. They do not prescribe SDKs, frameworks, products, or languages, so the
guidance stays valid as tools change and applies to any stack.

For one opinionated implementation of these ideas, with a focus on zero-trust
agents, see [Zetra](https://github.com/X-McKay/zetra). Zetra is where SDK
adapters, tooling, reference code, and deployment evidence live.

## What's here

### Agent Playbook

The [Agent Playbook](agent-playbook/README.md) is a standard for production AI
agents. It covers:

- Agent specifications and typed contracts
- Skills and tools, and how to classify their effects
- Durable execution and human approval
- Evaluation, observability, and cost controls
- Security, governance, risk assessment, and production readiness

### Multi-Agent Systems Playbook

The [Multi-Agent Systems Playbook](multi-agent-playbook/README.md) extends the
Agent Playbook for governed compositions of multiple agents. It adds standards
for topology selection, membership, roles, typed delegation, authority
attenuation, dynamic composition, shared state, system-wide limits, and
composition manifests while retaining the Agent Playbook contract for every
participating agent.

### Agent Development Skills

The [`skills/`](skills/README.md) library turns both playbooks into fourteen
portable Agent Skills for Claude Code, Codex, and compatible runtimes. They
guide design, interactions, risk, durable execution, evals, production
operations, and readiness reviews without assuming a particular stack.

## Scope

Content belongs here when it would still be true on a different stack. Content
that only makes sense for a particular SDK, framework, product, or language
belongs in an implementation such as Zetra. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the test to apply and how to handle
examples.

## Development

The repository is Markdown only. A pinned [Nix](https://nixos.org/) flake
provides the lint and link-check tools.

```bash
nix develop
just check
```

## Status

The Agent Playbook is currently **v0.4 — draft**. Feedback and contributions
are welcome through [issues](https://github.com/X-McKay/playbooks/issues) and
[pull requests](https://github.com/X-McKay/playbooks/pulls).
