# Canonical owner map

This portable package maps to the current draft at commit
`151fca01fbc609c5550c563c902946db540c2f4c`. The linked chapters remain the
normative owners; this map only identifies where each output field belongs.

| Canonical chapter-relative path | Requirement groups | Package use | Immutable source |
| --- | --- | --- | --- |
| `development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md` | `OPS-01`, `OPS-02`, `OPS-03`, `OPS-04`, `OPS-05` | Stable run/request identity, operation attribution, terminal-outcome and termination separation, applicable runtime bounds, exhaustion, and operator stop treatment. | [5.1 requirements](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/05-release-operations-and-lifecycle/01-observability-budgets-and-operational-control.md#requirements) |
| `development-guide/05-release-operations-and-lifecycle/03-ownership-incidents-maintenance-and-retirement.md` | `LIFECYCLE-01`, `LIFECYCLE-02`, `LIFECYCLE-03`, `LIFECYCLE-04`, `LIFECYCLE-05`, `LIFECYCLE-06` | Support ownership, suspected-incident triage and recovery record, feedback disposition, maintenance review, and deprecation/retirement handoff. | [5.3 requirements](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/05-release-operations-and-lifecycle/03-ownership-incidents-maintenance-and-retirement.md#requirements) |

## Boundary notes

- Chapter 5.1 owns operating control, not a telemetry product, release decision,
  or proof that a result was correct.
- Chapter 5.3 owns accountable support and lifecycle decisions. A stop operator
  and recovery authority are distinct; neither is created by this package.
- Release authorization and material-change routing remain owned by the linked
  [5.2 chapter](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/05-release-operations-and-lifecycle/02-readiness-change-and-rollout.md).
- Data handling, retention, and audit constraints remain owned by the linked
  [3.3 chapter](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/03-security-and-trust-boundaries/03-data-privacy-handling-and-minimum-audit-evidence.md).
- Uncertain external effects and retry/reconciliation constraints remain owned
  by the linked [7.2 chapter](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/engineering-reference/07-durable-execution-and-human-governed-work/02-side-effects-idempotency-and-unknown-outcomes.md).

Use the chapter-relative paths and group IDs in the packet's applicability
entries. Do not treat this map or a filled packet as authorization, certification,
or evidence that a control operated.
