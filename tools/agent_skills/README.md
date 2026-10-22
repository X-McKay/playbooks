# Development skill validation tools

These are non-normative repository-development aids for the [proposed skill library](../../development-skills/README.md). They inspect files and record a bounded development workflow; they do not invoke a model, execute a skill, launch a coding host, deploy an agent, grant permissions, or provide an operating-system sandbox.

## Validate, inventory, and export

Run from the repository root with Python 3.11 or later. No third-party dependency, provider account, or network access is required for the deterministic tool or its test suite.

```bash
python3 tools/agent_skills/skillctl.py --help
python3 tools/agent_skills/skillctl.py validate --root .
python3 tools/agent_skills/skillctl.py inventory --root . --output /tmp/agent-skills-inventory.json
python3 tools/agent_skills/skillctl.py package --root . --output /tmp/agent-development-skills.zip --profile python-local
python3 tools/agent_skills/skillctl.py verify-package /tmp/agent-development-skills.zip
python3 -m unittest discover -s tests/agent_skills -v
```

Use fresh output paths whose parent directories already exist. The tool refuses to overwrite an existing inventory, initial workflow state, or ZIP unless the caller explicitly supplies `--force`; ordinary workflow advancement atomically updates its existing ledger. The export is deterministic for identical inputs: normalized names, fixed ZIP metadata, sorted entries, and full content hashes. The manifest binds all skill resources, the catalog, contracts, and the selected implementation profile. It deliberately excludes its own bytes to avoid a self-referential hash. Archive verification reads without extraction or execution. This is a content-integrity record, not a publisher signature or admission decision, and coherent replacement of both content and hashes is not detectable without a separately trusted identity.

Validation checks the library's constrained standard-frontmatter subset, required resources, internal reference containment, package identities, explicit dependencies, draft packet and case contracts, and declared owner IDs. It rejects duplicates, missing dependencies, cycles, unsafe links, and symlinks rather than silently following them. This validator intentionally does not implement all YAML or certify every package permitted by the Agent Skills specification. Run the independent `skills-ref` validator when format interoperability matters.

Archive verification requires both shared contracts and checks their constrained schema content. Each skill's inventory must exactly cover its archived resources, including allowed optional references/assets; unassigned or unsupported members fail. Every CLI JSON input rejects duplicate keys and non-standard `NaN`/infinity tokens rather than silently admitting them.

The separate [independent-validation CI job](INDEPENDENT-VALIDATION.md) installs pinned development validators in an isolated environment and repeats full JSON Schema and Agent Skills reference checks. These packages are not dependencies of `skillctl.py` or the standard-library test suite. Its six-resource source allowlist is deliberately fixed to this initial proposed library; adding approved resources requires updating that CI inventory alongside the library.

Context figures are byte/word measurements and heuristic estimates, not actual host instruction-token counts. Native host selection, loaded-resource tracing, tool availability, permission behavior, and task performance require separate trials.

## Check an evidence packet

```bash
python3 tools/agent_skills/skillctl.py check-packet /tmp/build/packet.json --workspace /tmp/build
```

A packet uses the [shared envelope](../../development-skills/contracts/packet.schema.json) and the selected skill's task-specific contract. An observed evidence artifact must be a normalized relative path within the approved workspace, with its actual SHA-256. Do not use absolute paths, traversal, symlinks, or files outside the workspace. Planned evidence is visibly unrun and cannot support `met` or a positive release recommendation.

A passing packet check confirms the recorded mechanical predicates and matching bytes. It does not prove that the artifact tells the truth, that all applicable requirements were enumerated, that a test measured its claimed property, or that an authorized owner approved the release. `decision.authorized` stays `false`; external approval is a separate record.

## Record the development sequence

```bash
python3 tools/agent_skills/skillctl.py workflow --help
python3 tools/agent_skills/skillctl.py workflow init --output /tmp/build/workflow.json --max-repairs 2
python3 tools/agent_skills/skillctl.py workflow advance /tmp/build/workflow.json --event plan --evidence /tmp/build/evidence/plan.receipt.json
```

The local sequence is initialized → planned → implemented → tested → cleaned → retested → packaged → review-ready. Each successful phase must name actual evidence; a test pass cannot skip cleanup or the complete post-cleanup re-test. Failed or blocked events remain visible. A bounded repair returns to implementation and invalidates subsequent phase eligibility, rather than pretending a prior pass applies to new code.

Create the approved workspace and evidence directory first. Forward event names are `plan`, `implement`, `test`, `cleanup`, `retest`, `package`, and `review_ready`; the exceptional events are `block`, `fail`, and bounded `repair`. A unique receipt JSON has `event`, `outcome`, `artifact`, and `sha256`, plus an optional absolute `workspace`. A forward or repair receipt uses `outcome: pass`; a block/fail receipt uses its matching outcome. `artifact` is an actual normalized workspace-relative file and `sha256` its full current digest. A package receipt hashes an actual ZIP, not a note saying one exists. Never reuse or mutate a receipt pathname for a later attempt.

Evidence files are observations supplied by the caller, not commands executed by the helper. The caller owns the frozen source/configuration/dependency/evaluator identity, complete suite execution, workspace isolation, timeout policy, and honesty of the supplied receipts. A historical first-test result may remain in the ledger after cleanup, but cannot establish readiness for the changed candidate. Final retest and packaging must bind the same current candidate.

The helper's source snapshot omits any path component named `.git`, `.skillctl`, `evidence`, `artifacts`, `output`, `outputs`, `build`, `dist`, `coverage`, `__pycache__`, `.pytest_cache`, or `.mypy_cache`. It also consistently omits the active state, incoming receipt, and every retained receipt file, including invalidated attempts. Retained receipts and observation artifacts are hash-checked separately, even when a receipt lives at the workspace root; omitting it from source identity does not permit tampering. This is not a universal candidate bill of materials: explicitly bind any behavior-affecting code, configuration, dependencies, fixtures, or evaluator files in excluded/generated locations through your implementation manifest and evidence. Concurrent writers and hostile filesystem replacement are outside this helper's security model.

Ignored directories are pruned before entry-level inspection, so ordinary hardlinked Git objects or unreferenced cache metadata do not block a candidate snapshot. This pruning applies only to source identity: included source and explicitly referenced receipts/artifacts still reject unsafe file types, symlinks, and hardlinks. Static package validation/export retains strict whole-package traversal without these source exclusions.

The ledger uses atomic writes and verifies retained evidence hashes. It is not a durable execution engine, concurrency coordinator, business-transaction record, or human-approval system. Do not use it to retry a consequential external operation. Stop and reconcile an unknown external outcome at the authoritative service.

## Test boundaries

The offline suite exercises valid-library checks, malformed packets, whole-resource hashing, archive round trips, unsafe paths and symlinks, duplicate names and dependency failures, workflow order, bounded repair, cleanup/retest gates, and tamper refusal. It does not contact a coding host or execute exported skill code.

For independent behavioral evidence, run the package cases in fresh sessions on the intended host/model, compare with a pinned baseline, retain failures and inconclusive attempts, and report the test denominator and environment. Never relabel a deterministic tooling test as a native-host autonomous-development trial.
