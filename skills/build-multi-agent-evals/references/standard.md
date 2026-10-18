# Multi-Agent Evaluation Standard

This file condenses [Multi-agent systems chapter 7, Evaluation](https://github.com/X-McKay/playbooks/blob/main/multi-agent/07-evaluation.md). The chapter is canonical: if the two differ, follow the chapter and update this file.

Use a layered suite:

1. Member conformance and existing member risk gates.
2. Interaction contract, authorization, data-flow, and schema tests.
3. Coordination tests for routing, aggregation, budgets, and termination.
4. Durability tests for retries, duplicates, crashes, cancellation, and compensation.
5. Adversarial tests for injection propagation, collusion, false consensus, registry poisoning, and resource exhaustion.
6. End-to-end outcome, cost, latency, and human-impact tests.

Attribute each failure to where it first went wrong (routing, handoff, member, aggregation or review, termination) and reproduce recurring failures at the narrowest layer. Check handoffs by asserting that required facts and constraints reach the receiving member.

Keep system evals affordable: test interactions with recorded or simulated members, rerun member suites when a member changes, keep a small end-to-end smoke set per change, and run full outcome, adversarial, and ablation suites before release.

Critical risk scenarios are hard gates. Report distributions and tail behavior, not only means. Treat cost per successful outcome and worst-case amplification as first-class metrics.

Every report identifies a system subject and exact composition manifest. Baselines use the same dataset and evaluator version. Dynamic systems report admission decisions and selected members per run.
