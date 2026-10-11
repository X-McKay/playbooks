# Playbooks

This playbook is a guide, with best practices, for developing production-grade
AI agents. It is split into three sections:

- **Core concepts**: what every agent needs before it ships. Start with the
  [Foundations](foundations/README.md) guides on whether an agent is worth
  building, defining the problem, zero-trust principles, and who owns which
  decisions. Then work through [Agent Playbook Part 1](agent-playbook/README.md#part-1-core):
  principles, reference architecture, the agent contract, skills, tools,
  evaluation, observability, and production readiness.
- **Advanced concepts**: what you add as your agent takes on more.
  [Agent Playbook Part 2](agent-playbook/README.md#part-2-advanced-concepts)
  covers durable execution and human approval, cost optimization, security and
  governance, risk assessment, and implementation patterns.
- **Multi-agent systems**: what changes when several agents work together.
  The [Multi-Agent Systems Playbook](multi-agent-playbook/README.md) covers how
  to choose a topology, give each agent a role, hand work from one agent to
  another, narrow permissions as work is passed along, share state, and set
  limits for the system as a whole. Every agent in the system still follows the
  Core and Advanced guidance.

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
| Foundations | Unversioned | Draft |
| Agent Playbook | 0.4 | Draft |
| Multi-Agent Systems Playbook | 0.2 | Draft |

Feedback and contributions
are welcome through [issues](https://github.com/X-McKay/playbooks/issues) and
[pull requests](https://github.com/X-McKay/playbooks/pulls).
