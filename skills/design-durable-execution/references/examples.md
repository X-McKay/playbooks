# Durable Agent Execution Examples

## Durable Research Request

A research agent gathers sources, pauses for analyst approval, then publishes a report. Use one workflow with durable steps for planning, model execution, source retrieval, report storage, and publication. Use an external event for approval. Store the report outside workflow history and pass its artifact identifier.

Language-neutral pseudocode:

```text
workflow ResearchWorkflow(request: ResearchRequest) -> ResearchResult
  draft = run_step(draft_report, DraftReportInput(request),
                   timeout = 5 minutes, retry = TRANSIENT_RETRY_POLICY)
  wait until approval event received            # durable wait; survives restarts
  if not approval.approved:
    return ResearchResult.rejected(draft.artifact_id)
  return run_step(publish_report,
                  PublishInput(artifact_id = draft.artifact_id,
                               idempotency_key = request.request_id),
                  timeout = 1 minute, retry = IDEMPOTENT_WRITE_RETRY_POLICY)
```

Treat this as a structural example; translate it into the durable execution engine and agent framework pinned by the repository.

## Unknown Write Outcome

If `publish_report` times out after the remote system may have committed:

1. Query the destination using the idempotency key.
2. Return the existing publication if found.
3. Attempt creation only if no result exists.
4. Record reconciliation in telemetry.

## Approval Edge Cases

- Ignore or reject an approval for a different request identifier.
- Reject approval from an actor without the required role.
- Resolve races among approval, cancellation, and expiry deterministically.
- Never place an access token in an external event payload or workflow history.

## When Not to Use Durable Execution

A stateless FAQ agent that makes one model call and one read-only lookup usually belongs in the `ephemeral` execution class. Adding a workflow would add operational overhead without a durable business requirement.
