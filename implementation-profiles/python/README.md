# Python local coding profile

> **Status — proposed, non-normative implementation aid.** This profile is a
> Python **3.11+** local-development pattern for an approved coding task. It
> does not add, restate, or supersede the stack-neutral requirements in the
> playbook. It is not a deployment recipe, a runtime daemon, a permissions
> broker, or evidence that an implementation is safe, approved, or ready to
> release.

This profile gives a coding agent a small default shape so that the user receives
an **inspectable, runnable, and tested candidate for review**. The user or the
appropriate accountable reviewer still decides whether to accept the change,
grant access, run it on a target host, or authorize any effect. A passing local
suite is test evidence within its recorded scope; it is not self-certification.

## Applicability and prerequisites

Use this profile when a user has authorized a bounded **local Python coding
change** and wants a package-style command-line implementation. It is useful for
validators, formatters, converters, parsers, and other deterministic local
components. Prefer the standard library unless a declared third-party dependency
materially improves the task.

Do not use it as a substitute for an agent contract, authority decision, trust
boundary, evidence plan, readiness decision, production deployment, long-running
service, scheduler, or host sandbox. Tool/API access, network access, durable
state, consequential effects, and multi-agent behavior require their separately
applicable design and evidence work.

Before implementation, record or confirm:

1. **Approved workspace and boundaries.** Identify the isolated workspace,
   allowed input roots, allowed output roots, required files, file-size/depth
   limits, wall-clock deadline, and whether symlinks are forbidden. Stop with
   `needs_information` if the workspace, host, or boundary is unavailable.
2. **Candidate contract.** Define typed inputs, outputs, error/status values,
   effect class, user-visible CLI behavior, and an observable definition of
   done. Keep effects absent or use a reviewed fake/dry-run boundary until a
   separate authorization applies.
3. **Dependency decision.** State whether the standard library is sufficient.
   A third-party package is optional, not assumed: name its purpose, pin its
   resolved version in the project's reviewed lock material, record its source
   and hash support, and provide a missing-dependency stop. Never install or
   fetch a dependency merely because this profile mentions it.
4. **Test plan.** Define unit, contract, end-to-end, and security cases before
   relying on the candidate. Give every test its own temporary directory and
   unique fixture/output names; do not share mutable test fixtures between
   tests.

The runtime or host, **not this profile and not the Python process**, must
actually enforce workspace isolation, read/write mounts, network policy,
credential exposure, CPU/memory/process/output limits, and cancellation. Code
should validate its own boundary assumptions, but assertions in code do not turn
an unrestricted host into an isolated one.

## Candidate layout

Adapt names to the approved project; angle-bracket names below are placeholders,
not files to create in this repository. Keep importable modules free of runtime
work. A small single-process package can use this shape:

```text
<approved-workspace>/
├── pyproject.toml                         # package metadata and optional dependency policy
├── config.example.toml                    # non-secret, documented defaults only
├── .env.example                           # variable names only; never a real secret
├── src/
│   └── <package_name>/
│       ├── __init__.py                    # metadata/types only; no I/O or side effects
│       ├── __main__.py                    # `python -m <package_name>` entry point
│       ├── cli.py                         # argparse boundary and JSONL rendering
│       ├── contracts.py                   # typed input/output/error data structures
│       ├── service.py                     # business logic using injected ports
│       └── ports.py                       # Protocols for clock, files, transport, effects
└── tests/
    ├── unit/
    ├── contract/
    ├── e2e/
    └── security/
```

If the project needs a command name, expose it through a reviewed
`[project.scripts]` entry in `pyproject.toml` and retain `__main__.py` for an
ordinary `python -m` smoke path. This profile supplies **no scaffold, generated
code, daemon, or service runtime**. Create only files needed by the authorized
implementation.

## Design rules

### Keep import and composition safe

- Make imports side-effect-free. Do not read configuration, environment
  variables, standard input, the network, or the filesystem; spawn a process;
  configure logging; or perform effects at module import time.
- Use `if __name__ == "__main__":` only to invoke `main()` from `__main__.py`.
  Return an integer status from `main(argv: Sequence[str] | None = None)` and
  make the outer entry point translate it to process exit status.
- Put construction in a narrow **composition root** (normally CLI `main`). Pass
  explicit settings and `Protocol`-shaped ports to services through constructors
  or function parameters. Do not hide a clock, filesystem, transport, random
  source, environment, or effect client in a global singleton.
- Use `dataclasses`, `typing`, `pathlib`, `json`, `argparse`, `logging`,
  `subprocess`, `tempfile`, and `tomllib` where they fit. These Python 3.11
  standard-library tools are defaults, not a requirement to avoid a separately
  reviewed dependency.

### Treat input as data, not instructions

- Parse command arguments with `argparse`; parse JSON with `json.loads` and
  validate its full shape, types, required fields, allowed values, sizes, and
  nesting before it reaches service logic. Reject unknown or ambiguous fields
  where the contract is closed.
- Use typed data structures at the boundary and make success, validation,
  policy, dependency, and internal-error outcomes distinguishable. Do not infer
  a successful outcome from a fluent message or an exception-free path alone.
- Never form source code, SQL, shell text, file paths, URLs, or host commands by
  interpolating untrusted input. If a subprocess is genuinely required, pass a
  fixed executable and argument list with `shell=False`, a minimal allowlisted
  environment, an explicit `cwd`, captured bounded output, and a timeout.
- Resolve each requested path before use and prove it is under the designated
  approved root. Reject absolute paths when not explicitly allowed, `..`
  traversal, NULs, unexpected file types, and symlinks unless a documented,
  tested policy permits them. Re-check containment at the point of open/write to
  reduce time-of-check/time-of-use exposure.
- Make output paths deterministic or caller-selected only from a declared
  output allowlist. Refuse unexpected overwrites by default; use atomic writes
  where a partial output would be misleading.

### Give the CLI a stable, bounded interface

- Offer `--help`; validate command-line values before any effect; and use
  conventional nonzero exits for validation, missing dependency, policy, and
  internal failures. Do not print tracebacks, secrets, or raw private input by
  default.
- For automation, emit one UTF-8 JSON object per line on stdout (**JSONL**).
  Include at least `schema_version`, `event`, `status`, and a correlation/run
  identifier; add declared input/output artifact paths only when safe. Write
  human diagnostics and redacted logs to stderr, not mixed into JSONL stdout.
- Bound every read, parse, recursion/walk, output, subprocess, retry, and
  external wait with task-appropriate explicit limits. Fail visibly on a bound
  rather than retrying until green. Classify an effect whose outcome cannot be
  observed as unknown and stop for reconciliation; do not blindly repeat it.
- Keep normal CLI work foreground and finite. This profile does not create a
  resident process, worker, server, scheduler, or autonomous loop.

### Configure without exposing credentials

- Keep checked-in configuration non-secret (`config.example.toml` and
  `.env.example` document keys and safe example values only). Add actual local
  secret files to ignore rules in the consuming project; do not copy them to
  fixtures, logs, test snapshots, command history, or artifacts.
- Load configuration once at the composition root: documented non-secret file
  values first, then explicitly allowlisted environment-variable overrides.
  Validate configuration exactly as untrusted input. Read a needed secret only
  at the narrow client boundary; never echo it or treat its presence as
  authorization.
- If the requested host, interpreter, package, optional dependency, reviewed
  connector, or secret provisioning is unavailable, return `needs_information`
  or a typed missing-dependency result. Do not download an SDK, search for
  credentials, silently use an ambient token, or replace the requested
  capability with a broader one.

## Test and evidence minimum

Run tests in fresh temporary workspaces built from immutable input fixtures.
Retain the command, interpreter version, dependency/lock identity when present,
fixture identity, result, elapsed time, and redacted failures. A test suite is
not a permission grant and does not prove behavior outside its inputs or host.

| Layer | Minimum purpose and examples |
| --- | --- |
| **Unit** | Test pure services, data validation, error mapping, parsers, and injected fake ports. Cover boundary values and explicit stop statuses. |
| **Contract** | Test the public JSON input/output schema, JSONL event shape, CLI exit codes, `--help`, and the port/effect contract with fakes. Reject unknown fields and malformed UTF-8/JSON as the contract requires. |
| **End-to-end** | Invoke the package CLI in a fresh unique temporary workspace with representative fixtures. Assert declared artifacts, permissions where applicable, JSONL parseability, stdout/stderr separation, cleanup, and no write outside the output allowlist. |
| **Security** | Exercise prompt/command-injection-looking strings as data, traversal and symlink attempts, unexpected files, oversized/deep inputs, secret-like environment values, missing optional dependencies, timeout/cancellation paths, and mocked effect denial/unknown outcome. Assert fail-closed behavior and no secret in captured output. |

For an external or consequential action, run the end-to-end path against a fake
or approved sandbox and assert a typed proposal/receipt boundary. Do not convert
a test pass into an assertion that a real target was changed correctly. Record
invalid, inconclusive, timed-out, and failed trials rather than deleting them.
After a repair, run affected cases, clean their unique temporary output, then run
the complete relevant suite again before offering the candidate for review.

## Example review commands

These are **examples for an implementation inside the approved isolated
workspace**, not commands to run in this playbook repository, book chapters, or
legacy `skills/` tree. The caller must review the project paths, optional
dependencies, commands, and permissions before use.

```bash
# Confirm the declared interpreter and inspect the public CLI.
python3.11 --version
python3.11 -m <package_name> --help

# Use a fresh local environment only if the reviewed project needs one.
python3.11 -m venv .venv
. .venv/bin/activate
# Only when the project declares a reviewed, pinned, hash-verified lock input:
python -m pip install --require-hashes -r requirements-dev.lock

# Run the standard-library test layout with finite outer time limits supplied by the host.
python -m compileall -q src
python -m unittest discover -s tests/unit -t .
python -m unittest discover -s tests/contract -t .
python -m unittest discover -s tests/e2e -t .
python -m unittest discover -s tests/security -t .
```

If the project adopts another reviewed test runner, pin it as an optional
development dependency and give it equivalent unit, contract, end-to-end, and
security coverage. No command in this document authorizes installation,
execution, data access, a network request, a service start, or a target-side
effect.

## Host permissions, isolation, and handoff

Use the normal interactive permission review of the selected host. In **Codex**
and **Claude Code**, review each requested command, path, network/data access,
and effect under the host's ordinary policy; do **not** use
`--dangerously-skip-permissions`, `--yolo`, or any equivalent permission-bypass
flag. A coding agent must stop for review when the host requires consent or when
its available permissions are narrower than the approved contract.

The agent may modify only the user-approved isolated workspace. It must present
the user with a review-ready candidate: changed files, how to run it, test
commands and observed results, remaining failures/limits, dependency changes,
and any proposed (not performed) effects. It must not claim the candidate is
approved, secure, deployed, compliant, isolated, or production-ready solely
because it generated code or ran tests.

**Native-host status:** this profile is documentation and proposed metadata. It
is **untested on native hosts until actually run** in the declared host,
interpreter, dependency set, permission mode, and isolated workspace. Record
that host-specific run separately; do not infer it from format validation or a
run on another machine.

## Relationship to the playbook

This profile is intentionally outside the canonical, stack-neutral chapters and
preserves the legacy material unchanged. It operationalizes a narrow local coding
option while leaving authority, isolation enforcement, evaluation decisions, and
release decisions with their owners. Consult the current immutable draft for the
normative requirements and applicability decisions:

- [Agent contracts and configuration](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/02-agent-basics/02-agent-contracts-and-configuration.md)
- [Skills and reusable capabilities](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/02-agent-basics/05-skills-and-reusable-capabilities.md)
- [Test levels, techniques, and suite purposes](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/04-testing-and-evaluation/02-test-levels-techniques-and-suite-purposes.md)
- [Standards, required coverage, and execution cadence](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/04-testing-and-evaluation/06-standards-required-coverage-and-execution-cadence.md)
- [Results, comparisons, and decision limits](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/development-guide/04-testing-and-evaluation/07-analyzing-results-comparing-versions-and-making-decisions.md)
- [Applicability and normative language](https://github.com/X-McKay/playbooks/blob/151fca01fbc609c5550c563c902946db540c2f4c/applicability.md)
