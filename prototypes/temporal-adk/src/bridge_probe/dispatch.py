"""Volatile per-session execution deduplication, never durable progress authority."""

import asyncio
import json
from types import MappingProxyType

from .records import canonical_bytes, verify_operation


class OutcomeUnknown(RuntimeError):
    pass


def freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({k: freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(freeze(v) for v in value)
    return value


class Dispatcher:
    def __init__(self, registry, *, manifest):
        self.registry = MappingProxyType(dict(registry))
        self.manifest = manifest
        self.tasks = {}

    async def execute(self, operation, attempt_id):
        operation = verify_operation(operation, manifest=self.manifest)
        key = operation["operation_id"]
        identity = canonical_bytes(operation)
        if key in self.tasks:
            old_identity, old_attempt, task = self.tasks[key]
            if old_identity != identity or old_attempt != attempt_id:
                raise ValueError("conflicting execution delivery")
        else:
            if any(not item[2].done() for item in self.tasks.values()):
                raise ValueError("another operation is still executing")
            if len(self.tasks) >= 64:
                raise ValueError("session execution limit")
            executor = self.registry[operation["executor"]]

            async def run():
                try:
                    payload = operation["request"]
                    value = await executor(
                        freeze(payload.get("arguments", payload)),
                        freeze(payload.get("state", {})),
                        key,
                    )
                    return {"status": "succeeded", "value": json.loads(canonical_bytes(value))}
                except Exception as exc:
                    # A body exception cannot establish whether an effect occurred.
                    raise OutcomeUnknown(f"operation outcome unknown: {key}") from exc

            task = asyncio.create_task(run())
            self.tasks[key] = (identity, attempt_id, task)
        result = await asyncio.shield(task)
        return json.loads(canonical_bytes(result))

    async def close(self):
        tasks = [item[2] for item in self.tasks.values()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
