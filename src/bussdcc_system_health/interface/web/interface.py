import threading

from werkzeug.serving import make_server

from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event

from .factory import create_app
from ...events import (
    WebInterfaceStarted,
    TemperatureUpdate,
    LoadAverageUpdate,
    MemoryUsageUpdate,
    CPUUsageUpdate,
    NetworkUsageUpdate,
    DiskUsageUpdate,
)


class WebInterface(Process):
    name = "web"

    def __init__(self, host: str, port: int) -> None:
        self._thread: threading.Thread | None = None
        self.host = host
        self.port = port

    def start(self, ctx: ContextProtocol) -> None:
        self.app = create_app(ctx)
        self.socketio = self.app.socketio
        self._thread = threading.Thread(
            target=self._run,
            name=self.name,
            daemon=True,
        )
        self._thread.start()
        ctx.emit(WebInterfaceStarted(host=self.host, port=self.port))

    def _run(self) -> None:
        self._server = make_server(
            host=self.host,
            port=self.port,
            app=self.app,
            threaded=True,
        )

        self._server.serve_forever()

    def stop(self, ctx: ContextProtocol) -> None:
        if hasattr(self, "_server"):
            self._server.shutdown()

        if self._thread:
            self._thread.join(timeout=5)

    def handle_event(self, ctx: ContextProtocol, evt: Event[object]) -> None:
        payload = evt.payload

        if isinstance(payload, TemperatureUpdate):
            self.socketio.emit("ui.system.temperature.updated", payload.to_dict())
        elif isinstance(payload, LoadAverageUpdate):
            self.socketio.emit("ui.system.load.updated", payload.to_dict())
        elif isinstance(payload, MemoryUsageUpdate):
            self.socketio.emit("ui.system.memory.usage.updated", payload.to_dict())
        elif isinstance(payload, CPUUsageUpdate):
            self.socketio.emit("ui.system.cpu.usage.updated", payload.to_dict())
        elif isinstance(payload, DiskUsageUpdate):
            self.socketio.emit("ui.system.disk.usage.updated", payload.to_dict())
        elif isinstance(payload, NetworkUsageUpdate):
            self.socketio.emit(
                "ui.system.network.usage.updated",
                {"timestamp": evt.time.timestamp(), **payload.to_dict()},
            )
