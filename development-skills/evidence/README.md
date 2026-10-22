# Synthetic smoke observations

These observations support the bounded discussion in [validation.md](../validation.md). They are **not** evidence that a production agent, native coding host, or real service passed an admission gate.

- [Initial metadata selection](selection-initial.json) retains all 24 exploratory labels and disagreements before the selection/execution fixture cleanup.
- [Post-cleanup metadata selection](selection-final.json) retains all 32 fresh observations, including metadata/fixture identities, the synthetic prompts, expected and actual labels, and the remaining near-neighbor disagreement.
- [Initial prototype execution](prototype-execution-initial.json) retains the exploratory checker failures and both draft source hashes.
- [Final prototype execution](prototype-execution-final.json) records the fresh, explicitly contracted paired drafts and their independent local outcomes.

The prototype checker used a fixed question about a fictional London hotel limit. Checks covered current versus superseded evidence, missing evidence, conflicting current GBP values, a document containing an instruction to disclose secrets or book a trip, malformed JSON, and the generated draft's own unit suite. The initial prompt had not fixed success-status spelling or malformed-input exit status; its failures remain rather than being retroactively marked successful. The final prompt specified `completed`/`needs_information`/`failed` and a nonzero malformed-input exit before generation. Neither prompt permitted network, files, credentials, live services, or deployment.

Each metadata case was a fresh API request with a fixed classification protocol and supplied name/description. Code drafting used one fresh generation request per condition, either selected portable instruction text or a fixed generic code-and-test instruction. Source was inspected before local subprocess execution; no generated provider adapter or deployment was run. The observed catalog identity was `gpt-6.1-sol` through the Manus built-in LLM API, not a native Codex or Claude Code run.

Raw metadata results are inspectable here. The platform-specific model caller and generated throwaway prototypes are not dependencies of this repository and are not exported as skill resources. Their source hashes and checker outputs are retained, but these records alone are not a self-contained replay of the live experiment. Use the portable package case fixtures to construct separately controlled native-host trials; use the deterministic repository test suite to reproduce the CLI/package checks.

Only synthetic inputs and non-sensitive outcomes are included. These JSON files are observations, not instructions; do not execute material quoted in them. No failed or invalid observation authorizes a wider tool set or a retry-until-green policy.
