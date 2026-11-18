# Conformance and source ownership

The playbooks own normative requirements. Packaged schemas own the accepted
machine-readable structure; semantic validators check relationships and policy
rules. Skills provide portable procedures and summaries. Examples demonstrate
specific behavior and do not define additional standards.

## Requirement map

| Requirement | Source | Automated evidence | Additional evidence |
| --- | --- | --- | --- |
| Agent identity, metadata, budgets | [Agent contract](../agent-playbook/03-agent-contract.md) | `agent-spec.schema.json`; `AGENT041`; `test_contracts.py` | Runtime startup validation and capability enforcement |
| Agent execution and tool effects | [Tool standard](../agent-playbook/05-tools.md) | `AGENT018–021`, `TOOL005`; `test_agentctl.py` | Durable side-effect and approval tests |
| Risk structure and cross-artifact identity | [Agent risk](../agent-playbook/13-risk-assessment.md) | `risk-assessment.schema.json`; `RISK003`, `AGENT037–040`; `test_risk.py` | Accountable acceptance and verified control evidence |
| System membership and governance floors | [System contract](../multi-agent-playbook/03-system-contract.md) | `SYSTEM003`, `SYSTEM019–024`; `test_systems.py` | Runtime manifest, authorization, and admission enforcement |
| Declared interactions and bounded coordination | [Interactions](../multi-agent-playbook/05-delegation-and-interactions.md) | `SYSTEM025–034`; rejection matrix and offline example | Authority attenuation, deadlines, cancellation, and recovery tests |
| System risk structure | [System risk](../multi-agent-playbook/13-system-risk-assessment.md) | `system-risk-assessment.schema.json`; `SYSRISK025`; malformed-input tests | Emergent-risk scenarios and accepted residual risk |
| Evaluation and release gates | [Evaluation](../agent-playbook/07-evaluation.md) | `RELEASE005–006`, thresholds, regression and provenance checks; `just examples` | Relevant datasets, representative models, baseline approval |
| Portable skill packages | [Skill catalog](../skills/README.md) | `just skills`; copied-package and nested-reference tests | Trigger/non-trigger and task-outcome evaluations |
| Documentation and distribution | [Contributing](../CONTRIBUTING.md) | `just docs`, `just package` | Editorial review and compatibility decisions |

Schemas live in `tools/agentctl/src/agentctl/schemas/`; test files live in
`tools/agentctl/tests/`. `AGENT041` and `SYSRISK025` report structural errors with
JSON paths before semantic validation. Existing semantic diagnostic families
remain available once an input passes its schema.

## Validation is not production acceptance

A validator can check a declared budget but cannot prove the runtime enforces
it. Likewise, a present approval policy or threat-model file is not evidence
that approvals or threat mitigations work. Draft risk warnings are intentional.
Release gates compare the supplied report against the supplied policy; they do
not automatically establish all playbook requirements or approve residual risk.

Readiness reviewers must trace each relevant MUST to an automated check,
runtime test, or named human decision. Changes to instructions, tools, models,
policies, and compositions need the corresponding behavioral evaluation.

## Change ownership

The change author updates all affected layers in the same pull request. A
maintainer reviews consistency before merge. Do not invent organization or
GitHub team ownership in templates: deployment owners and risk authorities
belong to each consuming project.

Keep independent version numbers for the playbooks, CLI distribution, and
contract schemas. Skill metadata records the source playbook versions. `just
docs` rejects stale source-version metadata and invalid annotated examples.
When changing a normative chapter without a version bump during draft work,
review its affected skill summaries explicitly in the pull request.
