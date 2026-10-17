"""Activity transport facade: heartbeat remote work and validate artifact receipts."""

import asyncio
from contextlib import suppress

from temporalio import activity
from temporalio.exceptions import ApplicationError

from .artifacts import Position, Receipt
from .records import canonical_bytes, verify_operation


class Activities:
    def __init__(self, lifecycle, transport, tape):
        self.lifecycle = lifecycle
        self.transport = transport
        self.tape = tape

    async def remote(self, action, payload):
        async def heartbeat():
            while True:
                activity.heartbeat()
                await asyncio.sleep(2)

        task = asyncio.create_task(heartbeat())
        try:
            return await self.transport.call(action, payload)
        except ValueError as exc:
            raise ApplicationError(str(exc), non_retryable=True) from exc
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    @activity.defn
    async def provision_session(self, start: dict) -> dict:
        activity.heartbeat()
        return await self.lifecycle.provision(start)

    @activity.defn
    async def advance_runner(self, command: dict) -> dict:
        result = await self.remote("advance", command)
        if result.get("status") == "operation":
            verify_operation(
                result["operation"],
                manifest=self.tape.manifest,
                index=command["position"]["cursor"],
            )
        elif result.get("status") != "done":
            raise ApplicationError("invalid advance response", non_retryable=True)
        if len(canonical_bytes(result)) > 262144:
            raise ApplicationError("response exceeds protocol limit", non_retryable=True)
        return result

    async def execute(self, command):
        result = await self.remote("execute", command)
        receipt = Receipt.model_validate(result)
        self.tape.load(receipt.position)
        previous = Position.model_validate(command["position"])
        op = verify_operation(
            command["operation"], manifest=self.tape.manifest, index=previous.cursor
        )
        entries = self.tape.load(receipt.position)
        if (
            receipt.previous != previous.head
            or entries[-1]["operation"] != op
            or receipt.position.cursor != previous.cursor + 1
        ):
            raise ApplicationError("invalid candidate chain", non_retryable=True)
        return receipt.model_dump()

    @activity.defn
    async def execute_model(self, command: dict) -> dict:
        return await self.execute(command)

    @activity.defn
    async def execute_tool(self, command: dict) -> dict:
        return await self.execute(command)

    @activity.defn
    async def close_session(self, command: dict) -> dict:
        activity.heartbeat()
        return await self.lifecycle.close(command)

    def registered(self):
        return [
            self.provision_session,
            self.advance_runner,
            self.execute_model,
            self.execute_tool,
            self.close_session,
        ]
