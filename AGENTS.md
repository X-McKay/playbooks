# Repository guidance

Keep normative requirements in the two playbooks, portable procedures in skills,
and executable enforcement in agentctl. Read CONTRIBUTING.md and
docs/conformance.md before changing contracts.

Preserve chapter paths and CLI commands unless a migration is part of the task.
Update affected skill summaries, schemas, templates, and examples together.
Do not treat a successful schema check or a draft risk assessment as production
approval. Keep offline examples free of provider calls.

Run `just check` for Python, docs, skills, examples, and wheel verification.
Run `just nix-check` for Nix source checks. Use the locked uv workspace; avoid
changing `.python-version` or dependency constraints merely to suit a local
installation. Keep the repository unlicensed unless the user explicitly changes
that decision.
