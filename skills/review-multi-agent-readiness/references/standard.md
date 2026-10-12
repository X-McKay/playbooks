# Multi-Agent Readiness Standard

This file condenses [Multi-agent systems chapter 11, Production readiness](https://github.com/X-McKay/playbooks/blob/main/multi-agent/11-production-readiness.md). The chapter is canonical: if the two differ, follow the chapter and update this file.

## Required Evidence Domains

- Necessity and measured benefit over simpler baselines.
- Versioned System Spec and exact composition manifest.
- Conformant members and system risk assessment.
- Declared graph, typed interactions, narrowed authority, and data policy.
- Finite system and edge budgets with deterministic termination.
- Durable recovery and approval behavior where required.
- Layered evals, adversarial tests, hard gates, and approved baseline.
- Traceability, SLOs, alerts, capacity, privacy, incident response, and rollback.
- Change control for members, graph, policy, models, prompts, and registries.

Block release for prohibited use, critical residual risk, missing consequential approval, undeclared or over-privileged edges, absent system limits, non-replay-safe durable code, placeholder hard gates, missing manifest provenance, or no safe recovery from partial effects.

Conditional-go conditions must be bounded, owned, observable, time-limited, and incapable of masking a hard blocker.
