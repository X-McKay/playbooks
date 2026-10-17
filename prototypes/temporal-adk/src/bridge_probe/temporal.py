"""External Temporal owner. Agent modules and effect bodies never run here."""

from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

SAFE_RETRY = RetryPolicy(maximum_attempts=3)
ONCE = RetryPolicy(maximum_attempts=1)


@workflow.defn
class SessionWorkflow:
    def __init__(self):
        self.position = None
        self.pending = None
        self.resumed = False

    @workflow.query
    def progress(self) -> dict:
        return {"position": self.position, "pending": self.pending}

    @workflow.signal
    def resume(self):
        self.resumed = True

    async def call(self, name, arg, *, effect=False):
        return await workflow.execute_activity(
            name,
            arg,
            start_to_close_timeout=timedelta(seconds=45),
            schedule_to_close_timeout=timedelta(seconds=100),
            heartbeat_timeout=timedelta(seconds=10),
            retry_policy=ONCE if effect else SAFE_RETRY,
        )

    @workflow.run
    async def run(self, start: dict) -> dict:
        result = {"status": "FAILED", "cleanup": "REMEDIATION_REQUIRED"}
        binding = None
        try:
            binding = await self.call("provision_session", start)
            self.position = binding["position"]
            for _ in range(65):
                if start.get("pause_at") == self.position["cursor"] and not self.resumed:
                    await workflow.wait_condition(
                        lambda: self.resumed, timeout=timedelta(minutes=2)
                    )
                advanced = await self.call(
                    "advance_runner",
                    {"binding": binding, "position": self.position, "pending": self.pending},
                )
                if advanced["status"] == "done":
                    if self.pending is not None:
                        raise ApplicationError(
                            "finalized with pending operation", non_retryable=True
                        )
                    result = {
                        "status": "SUCCEEDED",
                        "result": advanced["result"],
                        "position": self.position,
                    }
                    break
                operation = advanced["operation"]
                if self.pending is not None and self.pending != operation:
                    raise ApplicationError("pending descriptor changed", non_retryable=True)
                if operation["index"] != self.position["cursor"] or operation["kind"] not in (
                    "model",
                    "tool",
                ):
                    raise ApplicationError("invalid operation sequence", non_retryable=True)
                self.pending = operation
                receipt = await self.call(
                    "execute_" + operation["kind"],
                    {
                        "binding": binding,
                        "position": self.position,
                        "operation": operation,
                        "attempt_id": operation["operation_id"] + ":attempt-1",
                    },
                    effect=True,
                )
                if (
                    receipt["previous"] != self.position["head"]
                    or receipt["operation_id"] != operation["operation_id"]
                    or receipt["request_digest"] != operation["request_digest"]
                    or receipt["position"]["cursor"] != self.position["cursor"] + 1
                ):
                    raise ApplicationError("invalid execution receipt", non_retryable=True)
                # This assignment is reconstructed only from an accepted Activity result.
                self.position = receipt["position"]
                self.pending = None
            else:
                raise ApplicationError("boundary budget exhausted", non_retryable=True)
        except ActivityError:
            # Execute Activities have no automatic retry. Missing completion is
            # uncertainty, not permission to repeat an effect on a new sandbox.
            result = {
                "status": "OUTCOME_UNKNOWN" if self.pending else "FAILED",
                "position": self.position,
                "pending": self.pending,
            }
        except (KeyError, TypeError, ValueError, ApplicationError, TimeoutError) as exc:
            result = {"status": "FAILED", "error": type(exc).__name__, "position": self.position}
        finally:
            try:
                closed = await self.call("close_session", {"start": start, "binding": binding})
                result["cleanup"] = closed["cleanup"]
            except ActivityError:
                result["cleanup"] = "REMEDIATION_REQUIRED"
        return result
