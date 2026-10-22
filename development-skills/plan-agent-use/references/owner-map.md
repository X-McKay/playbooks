# Canonical owner map

Use this map to locate the current canonical material while keeping this portable package independent of a surrounding checkout. It maps planning packet areas to their owners; it does not restate or replace the canonical requirements.

**Pinned source:** [`151fca01fbc609c5550c563c902946db540c2f4c`](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/requirement-index.md) (`0.5.0-draft.2`).

## Part 1 ownership

| Packet area | Requirement group IDs | Canonical chapter-relative path | Immutable owner link | Use in this package |
| --- | --- | --- | --- | --- |
| Problem brief | `PROBLEM-01`–`PROBLEM-04` | `development-guide/01-problem-definition-and-planning/01-defining-the-problem.md` | [1.1 Defining the Problem](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/01-problem-definition-and-planning/01-defining-the-problem.md#requirements) | Keep user work, current process, variations, dependencies, consumers, exclusions, and unverified assumptions distinguishable from a proposed solution. |
| Success record | `SUCCESS-01`–`SUCCESS-05` | `development-guide/01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md` | [1.2 Requirements, Success Criteria, and Measurable Targets](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/01-problem-definition-and-planning/02-requirements-success-criteria-and-measurable-targets.md#requirements) | Define outcomes, case behavior, separate dimensions, measures, targets, ownership, and evidence handoff before interpreting results. |
| Suitability record | `SUITABILITY-01`–`SUITABILITY-05` | `development-guide/01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md` | [1.3 Agent Suitability and Alternatives](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/01-problem-definition-and-planning/03-agent-suitability-and-alternatives.md#requirements) | Compare a shared task boundary with a simpler baseline and make fixed versus adaptive behavior explicit. |
| Initial scope record | `SCOPE-01`–`SCOPE-05` | `development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md` | [1.4 Initial Risk, Data, Ownership, and Delivery Plan](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/01-problem-definition-and-planning/04-initial-risk-data-ownership-and-delivery-plan.md#requirements) | Surface plausible harms, information, authority, ownership, delivery constraints, and the next applicable handoffs without deciding risk or approval. |

## Applicability dependency

Read [`applicability.md`](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/applicability.md) with the chapter owners. It explains how a trigger, `not_applicable`, unresolved applicable work, and a proposed governed exception differ. The packet is a mapping and planning aid, not proof that any requirement is met.

## Canonical planning templates

These immutable shapes informed the package output fields. They are illustrative planning aids, not observations or authorization.

| Packet artifact | Canonical template-relative path | Immutable template link |
| --- | --- | --- |
| Problem brief | `templates/1.1/problem-brief.yaml` | [problem-brief.yaml](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/templates/1.1/problem-brief.yaml) |
| Success record and metric definitions | `templates/1.2/success-criteria.yaml`; `templates/1.2/metric-specification.yaml` | [success-criteria.yaml](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/templates/1.2/success-criteria.yaml); [metric-specification.yaml](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/templates/1.2/metric-specification.yaml) |
| Suitability record | `templates/1.3/suitability-decision.yaml` | [suitability-decision.yaml](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/templates/1.3/suitability-decision.yaml) |
| Initial scope record | `templates/1.4/initial-scope-record.yaml` | [initial-scope-record.yaml](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/templates/1.4/initial-scope-record.yaml) |

## Boundary of this map

Part 1 plans the initial boundary. It hands detailed contract, trust-boundary, evidence, readiness, and operational work to separately loaded leaves. If a canonical owner is unavailable at the pinned revision, record the dependency gap; do not substitute legacy material or a mutable link.
