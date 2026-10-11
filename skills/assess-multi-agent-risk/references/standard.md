# Multi-Agent Risk Standard

This file condenses [Multi-Agent Systems Playbook chapter 13, System risk assessment](https://github.com/X-McKay/playbooks/blob/main/multi-agent-playbook/13-system-risk-assessment.md). The chapter is canonical: if the two differ, follow the chapter and update this file.

Start with member assessments, then add system-specific scenarios. Record affected parties, participating roles, interactions, causes, preconditions, consequences, inherent score, controls, evidence, residual score, treatment, owner, eval cases, indicators, alerts, and runbook.

The system governance tier is at least the maximum member tier and maximum inherent system-scenario tier, plus any mandatory floor. Critical residual risk or prohibited use requires no-go. Risk acceptance names an accountable role, conditions, expiry, and review cadence.

Dynamic systems additionally assess registry compromise, publisher trust, incompatible contracts, capability substitution, churn, manifest non-reproducibility, admission races, and emergency quarantine.

Monitor leading indicators such as denied edges, depth, fan-out, admission failures, disagreement, retries, duplicate effects, partial effects, cost amplification, and late results.
