# Part 4 — Testing and Evaluation

**Status:** 0.5.0-draft.2 — draft  
**Purpose:** Turn product, safety, and control claims into cases, fixtures, evaluators, coverage records, and decision-grade evidence.  
**Audience:** Builders, evaluation designers, reviewers (including security/privacy where triggered), and decision owners.  
**Applicability:** Whenever evidence supports a design, pilot, release, change, or operational-learning decision. Every production candidate uses the universal evidence core; capability, risk, claim, and exposure profiles apply only when triggered.  
**Reader question:** How do we produce and read evidence that justifies a bounded decision without letting a convenient score claim too much?

[Playbook home](../../README.md) · [Section index](../README.md) · [Applicability](../../applicability.md) · [Glossary](../../glossary.md) · [Requirement index](../../requirement-index.md) · [Practical reference](reference/README.md)

## Why this Part exists

An agent can look helpful while using an unpermitted source, following an unsafe path, hiding a failed retry, or relying on evidence that does not support its claim. A narrow controlled case is useful evidence but does not prove field reliability. This Part gives you a shared way to tell these apart.

Tests and evaluations overlap: a deterministic assertion can feed an evaluation, and a variable agent can be tested. The Part separates **where** behavior is exercised, **what** claim is assessed, **how** evidence is judged, **why** a suite runs, and **when/where** it runs, and ties each to an inspectable record.

It sets no universal trial count, pass rate, latency threshold, or reviewer role; owners set those per domain.

## Prerequisites and outputs

### Prerequisites

Have a bounded agent contract and intended outcomes, an initial risk/data/ownership record, the candidate configuration, and the relevant capability and trust-boundary information. If any are missing, start with [Part 1](../01-problem-definition-and-planning/README.md), [Part 2](../02-agent-basics/README.md), and [Part 3](../03-security-and-trust-boundaries/README.md).

### Outputs

A proportional effort produces:

- a versioned coverage map from claims and material risks to cases, profiles, owners, stages, and evidence;
- identified cases, fixtures, trial policies, evaluators, observations, and run statuses;
- evidence that keeps source support, permission/currentness, state/effects, and evaluator judgments distinct;
- an independent holdout when a decision relies on independence from tuning; and
- a bounded `go`, `conditional_go`, or `no_go` **evaluation conclusion** with evidence limits. It is not deployment authorization.

## Reading and working routes

### Learning route

Read [4.1](01-foundations-terms-and-definitions.md) to [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) in order, then see the records connected in the [practical reference](reference/README.md).

### Builder route

Start with [4.5](05-planning-designing-and-running-tests-and-evaluations.md) to write a case and fixture contract. Use [4.6](06-standards-required-coverage-and-execution-cadence.md) to select the universal core and triggered profiles, [4.2](02-test-levels-techniques-and-suite-purposes.md) to choose a probe, [4.3](03-evaluation-types-and-dimensions.md) to state the claim and observable invariants, [4.4](04-evaluators-metrics-rubrics-and-calibration.md) to choose the judgment method, and the [templates](reference/README.md#reusable-files) to keep records consistent.

### Reviewer route

Start with the coverage map and [4.6](06-standards-required-coverage-and-execution-cadence.md): are the universal core, profile triggers, owners, stages, and `N/A` rationales explicit? Then read [4.3](03-evaluation-types-and-dimensions.md) for the claim and relation/repeat evidence, [4.4](04-evaluators-metrics-rubrics-and-calibration.md) for evaluator fitness, and [4.7](07-analyzing-results-comparing-versions-and-making-decisions.md) for statuses, retries, aggregation, gates, and the conclusion. The [troubleshooting guide](reference/troubleshooting.md) isolates common evidence failures without rewriting the decision rule after results are seen.

## Chapters

1. [**4.1 Foundations, Terms, and Definitions**](01-foundations-terms-and-definitions.md) — Vocabulary and the five independent record descriptors.
2. [**4.2 Test Levels, Techniques, and Suite Purposes**](02-test-levels-techniques-and-suite-purposes.md) — Boundaries, probing techniques, and suite purposes, kept apart.
3. [**4.3 Evaluation Types and Dimensions**](03-evaluation-types-and-dimensions.md) — Outcome, trajectory, relation/reliability, grounding, robustness, safety, and resource claims.
4. [**4.4 Evaluators, Metrics, Rubrics, and Calibration**](04-evaluators-metrics-rubrics-and-calibration.md) — Matching a claim to an evaluator, evidence type, rubric, and calibration.
5. [**4.5 Planning, Designing, and Running Tests and Evaluations**](05-planning-designing-and-running-tests-and-evaluations.md) — Cases, fixtures, holdouts, trial policies, execution records, and failure intake.
6. [**4.6 Standards, Required Coverage, and Execution Cadence**](06-standards-required-coverage-and-execution-cadence.md) — The universal evidence core, triggered profiles, and material-change cadence.
7. [**4.7 Analyzing Results, Comparing Versions, and Making Decisions**](07-analyzing-results-comparing-versions-and-making-decisions.md) — Valid evidence, retries, comparisons, metrics, gates, and conclusions.

## Practical reference

The [practical reference](reference/README.md) has a [fictional policy-assistant walkthrough](reference/policy-assistant-worked-example.md), [troubleshooting](reference/troubleshooting.md), and YAML templates for a coverage plan, case/fixture, evaluator, trial policy, and decision report. It owns no requirements and reports no executed benchmark.

## Requirement ownership

The [requirement index](../../requirement-index.md) locates each identifier's owner. Here, 4.1 and the practical reference own none; each other chapter owns the groups in its `## Requirements` section. Read [Applicability](../../applicability.md) before treating a requirement as triggered, complete, excepted, or a release gate.
