# Durable Agent Execution Standard

## Boundary

Workflow code may coordinate deterministic state, schedule durable steps, wait on timers or external events, expose queries, and decide transitions from recorded inputs. Durable steps perform all model calls, agent runs, tool calls, database and network access, file I/O, randomness, and other nondeterministic operations.

## Durable Step Design

- Use coarse enough steps to avoid excessive history, but narrow enough for meaningful retry and observability.
- Pass versioned, bounded, schema-validated payloads.
- Set execution timeouts for bounded work and heartbeat timeouts for long-running work.
- Heartbeat useful progress and cancellation state.
- Return artifact references instead of large transcripts or binaries.
- Map provider failures into stable application failure types.

## Retry Matrix

| Failure | Default handling |
| --- | --- |
| Rate limit or transient network | Backoff and retry within budget |
| Provider timeout before side effect | Retry within budget |
| Invalid input or schema | Terminal; repair upstream |
| Authentication or permission | Terminal; alert owner |
| Policy denial | Terminal or explicit human path |
| Unknown write outcome | Reconcile by idempotency key before retry |
| Model quality failure | Constrained repair or fallback, then stop |

Set maximum attempts, elapsed retry time, and cost limits. Engine retries and provider or client-library retries must share one budget.

## Human Approval

Persist an approval request identifier, requested action, actor requirements, expiry, and immutable audit facts. Wait for a named external event. Validate the actor and event payload in a durable step or deterministic policy layer. Model approved, rejected, expired, and cancelled states explicitly.

## Evolution

- Keep workflow identifiers stable for business processes.
- Version payload schemas compatibly.
- Use the engine's versioning or patching mechanism for nondeterministic workflow changes.
- Run replay tests against representative production histories before deployment.
- Continue as a new run for unbounded loops or histories approaching operational limits.

## Required Tests

- Workflow transition unit tests.
- Time-skipping tests for timers and expiry.
- Durable-step retry and terminal failure tests.
- Duplicate-delivery and idempotency tests.
- Worker termination and resumption.
- Approval authorization and timeout.
- Replay tests for changed workflow code.
- Trace-context propagation.
