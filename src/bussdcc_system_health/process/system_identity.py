from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event
from bussdcc.events import RuntimeBooted

from .. import events


class SystemIdentityProcess(Process):
    name = "system_identity"

    def handle_event(self, ctx: ContextProtocol, evt: Event[object]) -> None:
        payload = evt.payload

        if isinstance(payload, RuntimeBooted):
            ctx.state.set("runtime.version", payload.version)

        elif isinstance(payload, events.AppBooted):
            ctx.state.set("app.version", payload.version)

        elif isinstance(payload, events.SystemIdentityEvent):
            ctx.state.set("system.identity", payload)
