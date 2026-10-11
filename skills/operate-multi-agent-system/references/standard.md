# Multi-Agent Operations Standard

This file condenses [Multi-Agent Systems Playbook chapter 8, Observability](https://github.com/X-McKay/playbooks/blob/main/multi-agent-playbook/08-observability.md), [Multi-Agent Systems Playbook chapter 9, Cost and capacity](https://github.com/X-McKay/playbooks/blob/main/multi-agent-playbook/09-cost-and-capacity.md), and [Multi-Agent Systems Playbook chapter 10, Security and governance](https://github.com/X-McKay/playbooks/blob/main/multi-agent-playbook/10-security-and-governance.md). The chapters are canonical: if they differ from this file, follow the chapters and update this file.

Correlate every event with system run, workflow, manifest, graph version, delegation, parent delegation, member, attempt, tenant, actor, policy decision, and budget ledger identifiers as applicable.

Measure outcome quality, end-to-end and per-edge latency, queue delay, model and tool calls, token and monetary cost, fan-out, depth, retries, disagreements, escalations, duplicates, partial effects, and dynamic admission results.

Capacity is multiplicative. Model worst-case parallelism, recursive depth, retry amplification, model/tool quotas, durable execution worker queues, and external dependency limits. Enforce hard system ceilings even if per-member limits remain.

Version and roll back System Specs, Agent Specs, prompts, models, policies, schemas, workflows, and registries independently. Preserve compatibility for in-flight durable runs or route them to versioned workers.
