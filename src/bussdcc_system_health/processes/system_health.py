from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event


class SystemHealthProcess(Process):
    name = "system_health"

    def on_event(self, ctx: ContextProtocol, evt: Event) -> None:
        if evt.name == "system.throttling.updated":
            ctx.state.set("system.throttling", evt.data)
