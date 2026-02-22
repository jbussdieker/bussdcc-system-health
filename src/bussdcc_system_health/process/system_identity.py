from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event


class SystemIdentityProcess(Process):
    name = "system_identity"

    def handle_event(self, ctx: ContextProtocol, evt: Event) -> None:
        if evt.name == "runtime.booted":
            ctx.state.set("runtime.version", evt.data["version"])

        elif evt.name == "app.booted":
            ctx.state.set("app.version", evt.data["version"])

        elif evt.name == "system.identity":
            ctx.state.set("system.identity", evt.data)
