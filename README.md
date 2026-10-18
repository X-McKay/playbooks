# Playbooks

This playbook is a guide, with best practices, for developing production-grade
AI agents. It is split into three sections:

- **[Core concepts](core/README.md)**: what every agent needs before it
  ships. Chapters 1 to 4 cover what to settle before you build: whether an
  agent is worth building, defining the problem, zero-trust principles, and
  who owns which decisions. Chapters 5 to 12 cover building the agent:
  principles, reference architecture, the agent contract, skills, tools,
  evaluation, observability, and production readiness.
- **[Advanced concepts](advanced/README.md)**: what you add as your agent
  takes on more: durable execution and human approval, cost optimization,
  security and governance, risk assessment, and implementation patterns.
- **[Multi-agent systems](multi-agent/README.md)**: what changes when several
  agents work together: how to choose a topology, give each agent a role,
  hand work from one agent to another, narrow permissions as work is passed
  along, share state, and set limits for the system as a whole. Every agent in
  the system still follows Core and Advanced concepts.

The guidance is technology-neutral. It explains what good looks like and why,
and does not prescribe SDKs, frameworks, products, or languages, so it stays
valid as tools change and applies to any stack.

The [`skills/`](skills/README.md) library condenses the guidance into fourteen
portable Agent Skills that help you design, assess, test, and review agents
while you work.

## Scope

Content belongs here when it would still be true on a different stack. See
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

| Content | Version | Status |
| --- | --- | --- |
| Core concepts | 0.5 | Draft |
| Advanced concepts | 0.4 | Draft |
| Multi-agent systems | 0.3 | Draft |

Feedback and contributions
are welcome through [issues](https://github.com/X-McKay/playbooks/issues) and
[pull requests](https://github.com/X-McKay/playbooks/pulls).
