# Independent development-skill validation

`validate_independent.py` is a **development-only** cross-check for the proposed library. It does not import, execute, or install any development-skill resource; it reads `SKILL.md` and JSON fixtures as data only.

The CI job creates an isolated virtual environment outside the checkout and installs only the exact development dependencies in `requirements-validation.txt`. `skills-ref` is fetched only from commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`; its source build backend and every resolved runtime dependency are explicitly pinned. The job uses finite pip retry and timeout settings.

For the exact eight proposed skill directories, the script reports each of these checks even if another skill fails:

1. The directory has precisely the six approved static resources; a missing or additional resource, including executable material, fails inventory validation.
2. `packet-template.json` and `evaluation-cases.json` are strict JSON (no duplicate keys or `NaN`/`Infinity`) and conform to their closed Draft 2020-12 schemas through `jsonschema.Draft202012Validator`.
3. Each fixture's `skill` value matches its directory name.
4. The pinned `skills-ref validate` CLI validates the `SKILL.md` format.

Run it after creating the isolated environment:

```bash
. /path/to/validation-venv/bin/activate
python tools/agent_skills/validate_independent.py \
  --root . \
  --skills-ref /path/to/validation-venv/bin/skills-ref
```

A JSON report contains all eight result records. The command exits nonzero for an invalid schema, malformed fixture, fixture/schema mismatch, inventory drift, or reference-format failure. A pass is static-format evidence only; it does not claim host behavior, permissions, authorization, model performance, or live effects.
