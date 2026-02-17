from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event


class SystemProcess(Process):
    name = "system"

    def on_event(self, ctx: ContextProtocol, evt: Event) -> None:
        if evt.name == "system.booted":
            ctx.state.set("system.version", evt.data["version"])

        elif evt.name == "system_health.booted":
            ctx.state.set("system_health.version", evt.data["version"])

        elif evt.name == "system.identity":
            ctx.state.set("system.identity", evt.data)

        elif evt.name == "system.temperature.updated":
            ctx.state.set("system.temperature", evt.data)

        elif evt.name == "system.load.updated":
            ctx.state.set("system.load", evt.data)

        elif evt.name == "system.cpu.usage.updated":
            ctx.state.set("system.cpu.usage", evt.data)

        elif evt.name == "system.memory.usage.updated":
            ctx.state.set("system.memory.usage", evt.data)

        elif evt.name == "system.disk.usage.updated":
            ctx.state.set("system.disk.usage", evt.data)

        elif evt.name == "system.network.usage.updated":
            ctx.state.set("system.network.usage", evt.data)

        elif evt.name == "system.throttling.updated":
            ctx.state.set("system.throttling", evt.data)
