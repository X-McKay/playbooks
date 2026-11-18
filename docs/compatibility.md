# Compatibility

## Version boundaries

| Component | Current version or range | Validation scope |
| --- | --- | --- |
| Agent Playbook | 0.3, draft | Normative prose and contract examples |
| Multi-Agent Systems Playbook | 0.1, draft | Composition requirements and templates |
| agentctl distribution | 0.4.0, with unreleased changes | Local and installed-wheel checks |
| Agent metadata contract | 1 | Packaged Agent Spec schema and semantic checks |
| System metadata contract | 1 | Packaged System Spec schema and semantic checks |
| Risk/eval report schema | 1 | Risk validation and release-policy checks |
| Python | >=3.12,<3.15 | CI matrix: 3.12, 3.13, 3.14 |
| PydanticAI offline examples | pydantic-ai-slim 2.70.0 | Typed output, TestModel, usage limits, fixed composition |
| Temporal | Chosen and pinned by each application | Illustrative guidance; no Temporal integration test in this repository |

Exact transitive Python dependencies are in `uv.lock`; Nix system tools are
pinned by `flake.lock`. The examples group is a development dependency and is
not part of the standalone CLI's runtime requirements.

## What the examples establish

The examples use PydanticAI's [testing interfaces](https://pydantic.dev/docs/ai/guides/testing/)
with provider requests disabled. They exercise typed construction, deterministic
authorization and coordination, bounded requests, evaluation report generation,
and release-policy acceptance/rejection. They do not establish real-model
quality, durable replay safety, or compatibility of every illustrative API in
the playbooks.

Applications must pin their own model SDKs, PydanticAI, Temporal SDK, worker,
and telemetry conventions, then run integration and replay tests. Record the
exact resolved versions with evaluation evidence.

## Upgrade procedure

1. Update the intended dependency constraint or source version.
2. Regenerate the relevant lockfile; do not hand-edit resolved hashes.
3. Review framework API changes against the affected examples and chapters.
4. Run `just check` and `just nix-check`; inspect the CI version matrix.
5. Update this table, affected skill source metadata, and the changelog.

The compatibility table lists the intended CI coverage; a new CI workflow must
run successfully on the hosting service before remote matrix results can be
claimed.
