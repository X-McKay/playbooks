# Durable Multi-Agent Coordination Examples

## Fan-Out/Gather

The workflow records three delegation records and reserves their budgets, then schedules three durable steps. Results are deduplicated by delegation ID. At the deadline, deterministic policy aggregates completed branches and either proceeds with a declared minimum evidence count or escalates.

## Consequential Action

An agent proposes a typed action. The workflow stores its hash and manifest, waits for a signed approval external event, revalidates policy, and schedules an idempotent effect step. The effect receipt is persisted before completion.

## Recursive Decomposition

Each child receives remaining depth and budget. Creation is denied at zero depth or insufficient reserve. Children cannot inherit credentials; they receive narrowed capability references.
