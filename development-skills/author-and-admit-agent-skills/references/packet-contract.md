# Admission Proposal Packet Contract

Use this contract while filling `assets/packet-template.json`. It describes a **proposal packet**, not deployment configuration, an effective manifest, approval, or a grant of authority.

## Common Envelope

Keep these top-level fields exactly: `schema_version`, `skill`, `run_id`, `status`, `source_commit`, `inputs`, `outputs`, `assumptions`, `blockers`, `applicability`, `evidence`, and `decision`.

- `schema_version` is `1.0`; `skill` is `author-and-admit-agent-skills`; and `source_commit` is the pinned canonical source used by this library.
- `status` is one of `draft`, `needs_information`, `blocked`, or `candidate_evidenced`.
- `decision.recommendation` is one of `not_assessed`, `go`, `conditional_go`, or `no_go`; `decision.authorized` is always `false`. A recommendation is not permission, approval, admission, deployment, or an effective allowlist update.
- Keep assumptions and blockers explicit. Do not replace an unknown owner, source, license, dependency, resource identity, or host behavior with a plausible value.

## Candidate Identity Output

Record these fields in `outputs.candidate_identity_record` or an equivalently named structured output:

- candidate name and unique-resolution status;
- semantic version;
- accountable owner and owner-verification status;
- source, revision, and source-verification status;
- license or licensing status;
- resolved complete-package identity and identity method;
- complete material inventory location and identity scope;
- prior identity and change-review status when this is a changed candidate; and
- admission state `proposed-not-admitted` unless an external record is supplied for comparison.

The material inventory covers every regular package file. It identifies each file's path, digest, role, and behavior relevance. The resolved package identity must cover the whole material inventory; no entry-file-only digest may stand in for it. A changed behavior-relevant reference, output-shaping asset, or executable file requires a new candidate identity and renewed review/evaluation plan.

## Dependency and Resource Output

Record one dependency entry for each required procedure dependency: ID, purpose, expected identity, verification observation, status, and bounded unavailable/mismatch handling. Record every direct reference or resource with path, digest, purpose, direct load predicate, host loading observation or status, and staged cost result.

Measure and label cost separately for discovery metadata, activated instructions, and deferred resources. Preserve the host, method, available bytes/tokens, load count, and whether a resource was needed. A cost estimate is not a loading observation. A host without a reliable required-resource loading path is a blocker, not a reason to assume the reference entered context.

## Applicability and Evidence

Each applicability record has exactly `requirement_id`, `status`, `rationale`, and `evidence_ids`. Its status is `met`, `not_applicable`, `unmet`, or `exception_proposed`.

- A `met` entry needs at least one matching `observed` and `pass` evidence ID.
- A planned, failed, invalid, inconclusive, or not-run item cannot establish `met` and cannot support `go` or `conditional_go`.
- A `not_applicable` entry records the absent trigger and rationale; it is not a hidden waiver.
- An `exception_proposed` entry remains a proposal and identifies its governing path outside this skill.

An evidence item has `id`, `kind`, `status`, `artifact`, and `sha256`. `kind` is `planned` or `observed`; `status` is `pass`, `fail`, `invalid`, `inconclusive`, or `not_run`. An observed artifact is a normalized relative path confined to the approved workspace and its hash is lowercase 64-character hexadecimal. Planned evidence may leave `artifact` and `sha256` empty.

Plan evidence for format and metadata, complete-package inventory/identity, dependency resolution, stage-specific cost/loading, positive activation, negative non-selection, ambiguous selection, procedure adherence, and safety handling. Include a prior-version comparison for every behavior-relevant change. Fixtures are planning aids, not observations.

## Required Handoff Shape

The outputs name the package inventory, candidate identity record, proposed admission relation, dependency register, resource loading/cost plan, selection-evaluation plan, and external review handoff. Mark the candidate unapproved and preserve unresolved questions. If an unsafe, missing, mismatched, changed, or inaccessible required resource prevents completion, list it in `blockers` and use `blocked` or `needs_information` rather than making a favorable decision.
