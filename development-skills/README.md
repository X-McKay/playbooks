# Agent Development Skills — proposed 0.5 mapping

**Library version:** 0.1.0 — proposed, not production-admitted.

**Canonical source:** playbook 0.5.0-draft.2 at `151fca01fbc609c5550c563c902946db540c2f4c`.

Use this development-time library to turn a detailed problem description into a reviewable agent contract, implementation, tests, operating instructions, and release-candidate evidence. It does not run inside the resulting agent by default, grant permissions, deploy anything, or certify production readiness. The [canonical book](../README.md), [applicability rules](../applicability.md), and [requirement index](../requirement-index.md) retain normative ownership.

The [legacy library](../skills/README.md) remains the v0.4 compatibility baseline. Do not install both libraries under the same visible names: `review-agent-readiness` exists in both. This library's catalog has qualified identities, but native hosts usually discover short names; reject a collision before use rather than relying on search order.

## Start with a detailed problem

For a complete coding task, explicitly use [draft-agent-implementation](draft-agent-implementation/SKILL.md). It loads the narrowly scoped procedures at named development phases; links do not automatically invoke sibling skills. Install the full eight-package closure for that workflow. Individual lifecycle packages can be used independently.

Give the builder a problem description, representative inputs and expected outputs, measurable success criteria, constraints, owner, data and action boundaries, an approved isolated coding workspace, and a chosen implementation profile. Missing ownership or authority is a blocker, not permission to invent business policy. A missing profile blocks stack-specific implementation, but need not prevent an initial planning packet.

A suitable task instruction is:

```text
Use draft-agent-implementation to draft an agent from problem.md.
Use the explicitly supplied python-local implementation profile.
Write only within this approved disposable workspace.
Use local fixtures; no live data, production credentials, or external effects.
Maximum two repair cycles. Preserve every failed test result.
Implement, test end-to-end, clean up, run the complete suite again,
then package the release candidate and produce a readiness recommendation.
Do not deploy, change permission settings, or claim production certification.
```

The [Python profile](../implementation-profiles/python/README.md) is a separate, non-normative implementation aid. The library does not require that stack. Existing project conventions and approved profiles take precedence over speculative framework adoption.

## The explicit workflow

The workflow produces a connected set of artifacts rather than seven unrelated checklists:

1. Frame the problem, suitability, success criteria, initial scope, risk, and assumptions.
2. Specify typed behavior, finite capabilities and budgets, outcomes, and trust boundaries.
3. Freeze test claims and acceptance criteria; mark optional capability profiles as applicable or explicitly not applicable.
4. Implement a thin vertical slice in the approved workspace, then complete the necessary behavior and controls.
5. Run unit, contract, integration, end-to-end, and applicable adverse-path checks. Retain failure and inconclusive records; use bounded repair rather than retry-until-green.
6. Perform final cleanup. Re-run the complete declared suite after cleanup, even if the earlier run passed.
7. Package the frozen code, configuration without secrets, tests, operations documentation, and evidence. Review readiness without treating the recommendation as authorization.

A source, configuration, dependency, fixture, or evaluator change invalidates the affected prior evidence. Do not edit after final testing and still claim the old package passed. A denied capability, unavailable dependency, missing observation, exhausted budget, or unknown external outcome has an explicit bounded result.

The optional [workflow evidence helper](../tools/agent_skills/README.md) checks a local phase ledger and artifact hashes. It does not execute the builder, impose an OS sandbox, enforce live-service permissions, or make evidence truthful. The caller and runtime must supply those controls.

## Package catalog

- [plan-agent-use](plan-agent-use/SKILL.md) turns the problem into a bounded development proposal and measurable acceptance criteria.
- [specify-agent-contract](specify-agent-contract/SKILL.md) defines typed behavior, effective-capability expectations, limits, and outcomes before implementation.
- [design-trust-boundaries](design-trust-boundaries/SKILL.md) maps authority, untrusted content, protected operations, and conditional data-handling obligations.
- [build-agent-evidence](build-agent-evidence/SKILL.md) designs and interprets claim-fit tests, baselines, trial statuses, and evidence.
- [review-agent-readiness](review-agent-readiness/SKILL.md) assembles a frozen release packet and a bounded recommendation, never approval.
- [operate-agent-lifecycle](operate-agent-lifecycle/SKILL.md) prepares observable operations, stops, support, incidents, and retirement.
- [author-and-admit-agent-skills](author-and-admit-agent-skills/SKILL.md) inspects complete package identities and proposes admission with activation and adherence evidence.
- [draft-agent-implementation](draft-agent-implementation/SKILL.md) coordinates the explicit bounded development workflow above.

[catalog.json](catalog.json) is a local discovery/dependency contract, not an Agent Skills extension or admitted capability manifest. Each package has an owner map, packet contract, normal and counterexamples, draft packet template, and evaluation cases. Required resources are directly linked; the exported packages do not depend on downloading mutable canonical chapters during execution. A reviewer can follow immutable source links when connectivity and authorization permit.

## Use with coding hosts

The portable packages follow the [Agent Skills specification](https://agentskills.io/specification). Their frontmatter has no commands, permission grants, hooks, or host-only dependency declarations. Copy the named package directories—not the catalog or contracts folders—into a skills location supported by your installed host. Inspect the package inventory before installing and reject already-visible duplicate names. Do not enable every package merely because a directory appeared.

For Codex, invoke the workflow explicitly in the approved project:

```text
Use $draft-agent-implementation with problem.md and the supplied python-local profile.
```

For Claude Code, invoke its named skill entry:

```text
/draft-agent-implementation
Use problem.md and the supplied python-local profile in this approved workspace.
```

Use normal host permission controls. Do not disable approvals or enable unrestricted execution to make a test pass. Filesystem reading and local coding tools must be separately available; a selected skill cannot make them available. The implementation profile and approved workspace must be explicitly provided to the host; they are not auto-discovered portable skill resources.

Consult the installed host's current documentation for placement and supported features: [Codex skills](https://developers.openai.com/codex/skills) and [Claude Code skills](https://code.claude.com/docs/en/skills). Placement, invocation, context retention, and permissions are host-specific. This release contains no claim that these particular packages have passed native-host activation or autonomous implementation trials.

## Deterministic validation and packaging

From the repository root, use the non-normative development tools:

```bash
python3 tools/agent_skills/skillctl.py validate --root .
python3 -m unittest discover -s tests/agent_skills -v
python3 tools/agent_skills/skillctl.py inventory --root . --output /tmp/agent-skills-inventory.json
python3 tools/agent_skills/skillctl.py package --root . --output /tmp/agent-development-skills.zip --profile python-local
python3 tools/agent_skills/skillctl.py verify-package /tmp/agent-development-skills.zip
```

Select a new output path; the tools refuse to overwrite existing output. Inventory binds all regular package resources, not just `SKILL.md`. The ZIP includes a manifest, the complete library, and the selected profile. Packaging does not install, execute, admit, or authorize the contents.

The local frontmatter validator deliberately supports a constrained YAML subset used by this library. Its checks are not full YAML validation or standard certification. Independently validate with the specification's reference validator when installed:

```bash
for skill in development-skills/*/SKILL.md; do
  skills-ref validate "$(dirname "$skill")"
done
```

Run the repository Markdown and offline link checks as well. See [tool documentation](../tools/agent_skills/README.md) for packet checks, workflow evidence, error behavior, and limitations.

## Evidence contracts and evaluation

[packet.schema.json](contracts/packet.schema.json) defines the common envelope; each skill adds a substantive task-specific output contract. `draft` means planning material. `candidate_evidenced` is restricted to the declared frozen candidate and assessed scope. `authorized` remains `false` in the packet because a recommendation cannot represent an external authorization.

An observed evidence record names a workspace-contained artifact and its full content hash. A `met` entry cites observed passing evidence; missing, failed, invalid, or inconclusive observations cannot become a positive readiness recommendation. A not-applicable entry requires an explicit trigger rationale. A proposed exception is not an approved waiver. A passing hash/schema check proves only the mechanical facts checked, not the truth of the artifact or complete requirement coverage.

The packet's `evidence` array is the current declared candidate evidence set. Retain earlier failed, invalid, and inconclusive attempts unchanged in the separate attempt ledger and reference that history through the outputs; do not relabel them or mix superseded observations into a current positive claim. An empty map, an all-not-applicable map, or an empty evidence set cannot support a positive recommendation.

[evaluation-cases.schema.json](contracts/evaluation-cases.schema.json) and package case files provide positive, negative near-neighbor, ambiguous, missing-dependency, safety, and held-out fixtures. These are test plans, not recorded live-agent results. A fitting skill with missing execution inputs is still `select`; use `clarify` when the requested skill or phase itself is unresolved. Assert the later needs-information/blocked behavior separately. Keep held-out prompts out of description optimization and report activation separately from execution quality.

For promotion, compare the candidate with no skill, a fixed generic plan/verify prompt, and an earlier immutable release when available. Use fresh workspaces and sessions, shared tool/fixture limits, and deterministic end-state assertions. Record the exact model, host, package, profile, fixture, and checker identities; all attempt statuses; resource use; and raw denominators. Use calibrated qualitative judges only for criteria that need them, never as the sole safety or authorization gate.

Native host discovery/activation, autonomous code-writing quality, alternate-model transfer, data-service isolation, and live deployment readiness remain separate evidence obligations. The repository tooling tests do not discharge them.

See [validation evidence and known gaps](validation.md) for the actual implementation checks and exploratory probes. Explicit invocation is recommended; the metadata-only smoke probe retained a near-neighbor selection disagreement and does not establish reliable native-host discovery.
