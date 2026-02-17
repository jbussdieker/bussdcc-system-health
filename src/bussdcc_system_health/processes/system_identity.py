from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event


class SystemIdentityProcess(Process):
    name = "system_identity"

    def on_event(self, ctx: ContextProtocol, evt: Event) -> None:
        if evt.name == "system.booted":
            ctx.state.set("system.version", evt.data["version"])

        elif evt.name == "system_health.booted":
            ctx.state.set("system_health.version", evt.data["version"])

        elif evt.name == "system.identity":
            ctx.state.set("system.identity", evt.data)
