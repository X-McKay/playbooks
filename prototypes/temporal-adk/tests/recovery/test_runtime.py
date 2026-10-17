from bridge_probe.runtime import Runtime


async def test_real_demo_runs_through_five_cold_boundaries(tmp_path):
    runtime = Runtime(
        tmp_path, session="demo", manifest="demo-v1", key=b"x" * 32, message="Inspect"
    )
    position = runtime.tape.empty(runtime.workspace.capture())
    binding = {"session": "demo"}
    try:
        for cursor in range(6):
            response = await runtime.handle(
                runtime.authority.sign(
                    "advance",
                    {"binding": binding, "position": position.model_dump(), "pending": None},
                )
            )
            if cursor == 5:
                assert (
                    response["status"] == "done"
                    and response["result"]["final_text"] == "Report ready."
                )
                break
            result = await runtime.handle(
                runtime.authority.sign(
                    "execute",
                    {
                        "binding": binding,
                        "position": position.model_dump(),
                        "operation": response["operation"],
                        "attempt_id": f"attempt-{cursor}",
                    },
                )
            )
            from bridge_probe.artifacts import Receipt

            position = Receipt.model_validate(result["receipt"]).position
        assert len(runtime.effects) == 5
        assert (tmp_path / "workspace" / "report.md").read_text() == "Workspace inspected."
    finally:
        await runtime.dispatcher.close()
