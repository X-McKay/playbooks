# Foundations: before you build

- **Status:** Draft
- **Last updated:** 2026-10-11

The [Agent Playbook](../agent-playbook/README.md) and the
[Multi-Agent Systems Playbook](../multi-agent-playbook/README.md) define what a
conforming agent or system must do. These guides come first. They help you
decide whether an agent is the right answer, describe the problem well enough
to build and judge one, adopt a zero-trust posture from the start, and know who
owns each decision.

They are written for the developers who build agents, though product owners,
platform teams, and security reviewers may also find them useful. They are
guidance rather than conformance requirements: the playbooks remain the
standard. Where a guide uses **MUST**, **SHOULD**, or **MAY**, the terms carry
the meaning defined in the Agent Playbook.

## Guides

1. [Strategy and use-case selection](01-strategy-and-use-cases.md): for
   developers deciding whether an agent is worth building, how much authority
   the first release gets, and how to measure success, cost, and safety
   separately.
2. [Defining the problem](02-problem-definition.md): how to write
   the brief, agree success criteria and limits, map data, risks, owners, and
   dependencies, and set the two readiness decisions every agent faces.
3. [Zero-trust principles for agents](03-zero-trust-principles.md): why you
   design your agent as an untrusted workload acting on someone's behalf, and
   what that means for its identity, permissions, and evidence.
4. [Operating model](04-operating-model.md): which decisions are yours, whose
   sign-off you need, what your agent must report for oversight, and how it
   moves through adoption stages on evidence.

## How they connect to the playbooks

| Foundation output | Used by |
| --- | --- |
| Use-case charter and value hypothesis | [Agent contract](../agent-playbook/03-agent-contract.md), [risk assessment](../agent-playbook/12-risk-assessment.md) |
| Problem brief and success criteria | [Evaluation standard](../agent-playbook/06-evaluation.md), [cost optimization](../agent-playbook/10-cost-optimization.md) |
| Readiness decisions | [Production readiness](../agent-playbook/08-production-readiness.md) |
| Zero-trust principles | [Principles](../agent-playbook/01-principles-and-scope.md), [tools](../agent-playbook/05-tools.md), [security and governance](../agent-playbook/11-security-and-governance.md) |
| Decision rights and oversight | [Security and governance](../agent-playbook/11-security-and-governance.md), [observability](../agent-playbook/07-observability.md) |
