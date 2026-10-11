# Foundations: before you build

- **Status:** Draft
- **Last updated:** 2026-10-11

The [Agent Playbook](../agent-playbook/README.md) and the
[Multi-Agent Systems Playbook](../multi-agent-playbook/README.md) define what a
conforming agent or system must do. These guides come first. They help an
organization decide whether an agent is the right answer, describe the problem
well enough to build and judge one, adopt a zero-trust posture from the start,
and give people clear decisions to own.

They are written for executive sponsors, product and business owners, platform
and security leads, and the engineers who will build the agent. They are
guidance rather than conformance requirements: the playbooks remain the
standard. Where a guide uses **MUST**, **SHOULD**, or **MAY**, the terms carry
the meaning defined in the Agent Playbook.

## Guides

1. [Strategy and use-case selection](01-strategy-and-use-cases.md): when an
   agent is worth building, how to state a value hypothesis, and how to measure
   value, reliability, safety, and adoption separately.
2. [Defining the problem](02-problem-definition.md): the brief, success
   criteria, constraints, data, risks, owners, dependencies, and the two
   readiness decisions every agent faces.
3. [Zero-trust principles for agents](03-zero-trust-principles.md): why an
   agent is treated as an untrusted workload acting on someone's behalf, and
   what that requires.
4. [Operating model](04-operating-model.md): ownership, decision rights,
   oversight views, and how adoption progresses on evidence.

## How they connect to the playbooks

| Foundation output | Used by |
| --- | --- |
| Use-case charter and value hypothesis | [Agent contract](../agent-playbook/03-agent-contract.md), [risk assessment](../agent-playbook/13-risk-assessment.md) |
| Problem brief and success criteria | [Evaluation standard](../agent-playbook/07-evaluation.md), [cost optimization](../agent-playbook/09-cost-optimization.md) |
| Readiness decisions | [Production readiness](../agent-playbook/11-production-readiness.md) |
| Zero-trust principles | [Principles](../agent-playbook/01-principles-and-scope.md), [tools](../agent-playbook/05-tools.md), [security and governance](../agent-playbook/10-security-and-governance.md) |
| Decision rights and oversight | [Security and governance](../agent-playbook/10-security-and-governance.md), [observability](../agent-playbook/08-observability.md) |
