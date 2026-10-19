# Part 4 — Testing and Evaluation

**Status:** 0.5.0-draft.2 — draft  
**Purpose:** Turn product, safety, and control claims into cases, fixtures, evaluators, coverage records, and evidence you can base a decision on.  
**Audience:** Builders, evaluation designers, reviewers, security/privacy reviewers where triggered, and decision owners.  
**Applicability:** Use this Part whenever evidence supports a design, pilot, release, change, or operational-learning decision. Every production candidate uses the universal evidence core; capability, risk, claim, and exposure profiles are added only when their triggers are true.  
**Reader question:** How do we produce and read evidence that justifies a bounded decision, without pretending a convenient score proves everything?

[Playbook home](../../README.md) · [Section index](../README.md) · [Applicability](../../applicability.md) · [Glossary](../../glossary.md) · [Requirement index](../../requirement-index.md) · [Practical reference](reference/README.md)

## Why this Part exists

An agent can look helpful while using an unpermitted source, following an unsafe path, hiding a failed retry, or relying on evidence that does not support a claim. A narrow controlled case can be useful evidence without proving field reliability. This Part gives you a shared way to tell these apart.

Tests and evaluations overlap: a deterministic boundary assertion can feed an evaluation, and a variable agent can be tested. The Part separates **where** behavior is exercised, **what** claim is assessed, **how** evidence is judged, **why** a suite is run, and **when/where** it runs. It then ties these to records a reviewer can inspect.

The Part sets no universal trial count, pass rate, latency threshold, or reviewer role. Owners set domain-specific thresholds and acceptance criteria.

## Prerequisites and outputs

### Prerequisites

Before planning a decision-grade evaluation, have a bounded agent contract and intended outcomes, an initial risk/data/ownership record, the candidate configuration, and the relevant capability and trust-boundary information. If these are missing, start with [Part 1](../01-problem-definition-and-planning/README.md), [Part 2](../02-agent-basics/README.md), and [Part 3](../03-security-and-trust-boundaries/README.md).

### Outputs

A proportional Part 4 effort produces:

- a versioned coverage map from claims and material risks to cases, profiles, owners, stages, and evidence;
- identified cases, fixtures, trial policies, evaluators, observations, and run statuses;
- evidence that keeps source support, permission/currentness, state/effects, and evaluator judgments distinct;
- an independent holdout when a decision relies on independence from tuning; and
- a bounded `go`, `conditional_go`, or `no_go` **evaluation conclusion** with evidence limits. It is not deployment authorization.

## Reading and working routes

### Learning route

Read [4.1](01-foundations-terms-and-definitions.md) through [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) in order, then use the [practical reference](reference/README.md) to see the records connected in one fictional example.

### Builder route

Start with [4.5 Planning, Designing, and Running Tests and Evaluations](05-planning-designing-and-running-tests-and-evaluations.md) to make a case and fixture contract. Use [4.6](06-standards-required-coverage-and-execution-cadence.md) to select the universal core and only the profiles whose triggers are true. Use [4.2](02-test-levels-techniques-and-suite-purposes.md) to choose a probe, [4.3](03-evaluation-types-and-dimensions.md) to state the claim and observable invariants, [4.4](04-evaluators-metrics-rubrics-and-calibration.md) to select the judgment method, and the [templates](reference/README.md#reusable-files) to keep records consistent.

### Reviewer route

Start with the coverage map and [4.6](06-standards-required-coverage-and-execution-cadence.md): are the universal core, profile triggers, owners, stages, and `N/A` rationales explicit? Read [4.3](03-evaluation-types-and-dimensions.md) for the claim and relation/repeat evidence, [4.4](04-evaluators-metrics-rubrics-and-calibration.md) for evaluator fitness, and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) for statuses, retries, aggregation, gates, and the conclusion. The [troubleshooting guide](reference/troubleshooting.md) helps isolate common evidence failures without rewriting the decision rule after results are seen.

## Chapters

1. [**4.1 Foundations, Terms, and Definitions**](01-foundations-terms-and-definitions.md) — The vocabulary and five independent descriptors for Part 4 records.
2. [**4.2 Test Levels, Techniques, and Suite Purposes**](02-test-levels-techniques-and-suite-purposes.md) — Technical boundaries, probing techniques, and suite purposes, kept apart.
3. [**4.3 Evaluation Types and Dimensions**](03-evaluation-types-and-dimensions.md) — Outcome, trajectory, relation/reliability, grounding, robustness, safety, and resource claims.
4. [**4.4 Evaluators, Metrics, Rubrics, and Calibration**](04-evaluators-metrics-rubrics-and-calibration.md) — Matching a claim to an evaluator, evidence type, rubric, and calibration record.
5. [**4.5 Planning, Designing, and Running Tests and Evaluations**](05-planning-designing-and-running-tests-and-evaluations.md) — Cases, fixtures, holdouts, trial policies, execution records, and failure intake.
6. [**4.6 Standards, Required Coverage, and Execution Cadence**](06-standards-required-coverage-and-execution-cadence.md) — The universal evidence core, triggered profiles, and material-change cadence.
7. [**4.7 Analyzing Results, Comparing Versions, and Making Decisions**](07-analyzing-results-comparing-versions-and-making-decisions.md) — Reading valid evidence, retries, comparisons, metrics, gates, and evaluation conclusions.

## Practical reference

The [Practical Reference](reference/README.md) has a connected [fictional policy-assistant walkthrough](reference/policy-assistant-worked-example.md), [troubleshooting guidance](reference/troubleshooting.md), and reusable YAML structures for a coverage plan, case/fixture record, evaluator record, trial policy, and decision report. It owns no requirements and reports no executed benchmark.

## Requirement ownership

The [requirement index](../../requirement-index.md) locates the owner of each identifier. In this Part, 4.1 and the practical reference own no requirement IDs; each other chapter owns the groups in its own `## Requirements` section. Read [Applicability](../../applicability.md) before treating a requirement as triggered, complete, eligible for an exception, or a release gate.

Older filenames remain as brief [migration redirects](01-evaluation-strategy-cases-and-test-environments.md).
