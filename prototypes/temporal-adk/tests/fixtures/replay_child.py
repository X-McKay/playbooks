import asyncio
import json
import sys
from bridge_probe.capture import capture_boundary, BridgeModel, BridgeTool
from tests.fixtures.cases import FixtureCase, build_agent


async def main():
    request = json.load(sys.stdin)
    case = FixtureCase(scenario=request.get('scenario', 'normal'))
    def factory(bridge):
        return build_agent(case, BridgeModel(bridge), lambda fn: BridgeTool(fn, bridge))
    try:
        result = await capture_boundary(factory, request.get('tape', []), request.get('expected_pending'))
    except Exception as exc:
        result = {'error': type(exc).__name__, 'message': str(exc)}
    result.update(effects=case.effects, trace=case.trace)
    print(json.dumps(result))

asyncio.run(main())
