import threading

from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event

from .factory import create_app


class SystemWebInterface(Process):
    name = "system_web"

    def on_start(self, ctx: ContextProtocol) -> None:
        self.app = create_app(ctx)
        self.socketio = self.app.socketio
        self._thread = threading.Thread(
            target=self._run,
            name="flask",
            daemon=True,
        )
        self._thread.start()

    def _run(self) -> None:
        self.socketio.run(
            self.app,
            host="0.0.0.0",
            port=8086,
            allow_unsafe_werkzeug=True,
        )

    def on_event(self, ctx: ContextProtocol, evt: Event) -> None:
        if evt.name == "system.temperature.updated":
            self.socketio.emit("ui.system.temperature.updated", evt.data)
        elif evt.name == "system.load.updated":
            self.socketio.emit("ui.system.load.updated", evt.data)
        elif evt.name == "system.memory.usage.updated":
            self.socketio.emit("ui.system.memory.usage.updated", evt.data)
        elif evt.name == "system.cpu.usage.updated":
            self.socketio.emit("ui.system.cpu.usage.updated", evt.data)
        elif evt.name == "system.disk.usage.updated":
            self.socketio.emit("ui.system.disk.usage.updated", evt.data)
        elif evt.name == "system.network.usage.updated":
            self.socketio.emit(
                "ui.system.network.usage.updated",
                {"timestamp": evt.time.timestamp(), **evt.data},
            )
