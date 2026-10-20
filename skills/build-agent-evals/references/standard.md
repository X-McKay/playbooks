# Agent Evaluation Standard

This file condenses [Core chapter 10, Evaluation](https://github.com/X-McKay/playbooks/blob/main/core/10-evaluation.md). The chapter is canonical: if the two differ, follow the chapter and update this file.

## Start from Failures

Build the first cases from the problem brief and from people who do the task today. Run the agent, read every transcript, group failures into named modes, and write an evaluator for each mode that matters. Keep reading transcripts after scores are automated.

## Types of Evaluation

Classify each eval by purpose, scope, setup, and stage.

| Purpose | Question | Failure response |
| --- | --- | --- |
| Smoke | Does it run end to end? | Stop; something is broken |
| Capability | How well can it do this task? | Keep improving; not a blocker alone |
| Regression | Does it still do what it did? | Block, or accept explicitly |
| Safety and policy | Does it stay within its limits? | Block release |
| Adversarial | Does it resist misuse? | Block release; update threat model |
| Operational | Fast, cheap, reliable enough? | Block or tune |
| Comparison | Is B better than A? | Keep the baseline |
| Acceptance | Do real users get the job done? | Not ready for production |
| Online monitoring | Still working on real traffic? | Investigate; may roll back |

Scopes are component, outcome, trajectory, and conversation. Stages run from prototype through development, each change, pre-release, user testing, rollout (shadow, canary), production, and after incidents. Choose evals from what is changing: instructions need a regression comparison; tools need positive and negative tool evals; data sources need retrieval, groundedness, and injection cases; model changes need every suite with repeated runs. Keep each type's cases separate, and promote capability cases to regression once they pass reliably.

## Evaluation Layers

| Layer | Purpose | Typical evidence |
| --- | --- | --- |
| Contract | Types and invariants | Schema checks, exact assertions |
| Capability | Tool and skill behavior | Tool arguments, denied calls, trajectory |
| Task | End-user outcome | Domain metrics and rubric scores |
| Workflow | Durable behavior | Retry, approval, timer, replay scenarios |
| System | Production objectives | Quality, latency, reliability, cost |

## Dataset Taxonomy

Every material behavior should have cases for happy paths, boundaries, ambiguous inputs, missing evidence, adversarial content, permission denial, dependency failure, historical regressions, and high-risk operations. Workflow agents also need duplicate delivery, retry, timeout, cancellation, external-event race, and worker recovery cases.

Each case should include:

- stable ID and human-readable name;
- source and creation date;
- input and controlled dependencies;
- relevant risk and capability tags;
- expected structured fields or invariants;
- allowed variation;
- redaction and retention classification.

Have a second person review expected results, keep a held-out set for release decisions (retire or replace cases once their results inform tuning, and version the set), refresh the dataset when it saturates, and sanitize production cases into minimal reproductions.

Every material scenario in the agent risk assessment should map to one or more
case IDs, deterministic invariants where possible, and a release or monitoring
decision. Report uncovered scenario IDs explicitly; average quality must not
hide missing risk coverage.

## Grade Outcomes Where They Happen

Run cases against controlled, resettable fixtures and assert on the resulting state, including the number of side effects. Simulated tools return realistic errors and denials. Multi-turn tasks use a simulated user with a goal. Retrieval quality is measured separately from answer quality.

## Evaluator Selection

Use the least subjective evaluator that captures the claim. Deterministic evaluators should own schemas, exact values, forbidden actions, authorization, citations, and budget limits. Use model judges for relevance, tone, or completeness only with a documented rubric, representative calibration set, and periodic human review.

A judge rubric checks one criterion, uses pass/fail or a short described scale, asks for a reason before the score, and includes real passing and failing examples. Calibrate against human labels, study disagreements, and recalibrate when the rubric, judge model, or typical agent output changes. Run pairwise comparisons in both orders to control position bias.

## Stochastic Measurement

Run critical cases multiple times. Report attempt count, pass rate, distribution, variance, and confidence bounds when useful. Use all-attempts pass rates for critical behavior: with independent attempts, a 90% per-attempt success rate passes five of five only about 59% of the time. Report run count and per-attempt failure rate beside the all-attempts score. Five passes of five does not establish reliability (the 95% lower bound on per-attempt success is about 55%); for critical gates, prespecify the number of fresh runs from the tolerable failure rate and require zero failures (zero in n runs bounds the failure rate below about 3/n at 95% confidence). Keep sampling parameters fixed for comparisons. Store model, provider, prompt, tool, skill, policy, and dataset versions with results.

Compare baseline and candidate on identical cases and read the flipped cases. Size datasets so the allowed regression is larger than measurement noise. Treat model changes as releases: run the full suite on the new model with unchanged instructions first, retune afterwards, and roll out gradually.

## Checking the Evals

Each evaluator must fail on a known-bad result. Investigate sudden score jumps for broken fixtures or graders. Pair each safety metric with a usefulness metric so refusing everything does not score well. Label infrastructure failures separately from agent failures.

## Release Gates

Block release on any hard safety or authorization violation. For graded metrics, define baseline, minimum acceptable value, allowed regression, sample size, and owner. Compare quality and safety alongside p50/p95 latency, input/output tokens, tool calls, retries, and cost per successful task.

## Online Evaluation

Sample by risk and failure mode, not only uniformly. Redact before storage. Keep monitoring alerts separate from offline release gates until labels and evaluator reliability are understood. Promote reviewed failures into a versioned regression dataset.
