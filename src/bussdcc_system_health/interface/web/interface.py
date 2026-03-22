from typing import Any

from flask import redirect, url_for
from flask_socketio import SocketIO

from bussdcc import ContextProtocol, Event, Message
from bussdcc_framework.web import FlaskApp, WebInterface as Base

from ... import message

from .blueprints.system_stats import bp as system_stats_bp


class WebInterface(Base):
    def register_routes(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        app.register_blueprint(system_stats_bp)

        @app.route("/")
        def index() -> Any:
            return redirect(url_for("system_stats.index"))

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        payload = evt.payload

        if isinstance(payload, message.CPUTemperatureUpdate):
            self.socketio.emit("ui.system.cpu.temperature.updated", payload)
        elif isinstance(payload, message.LoadAverageUpdate):
            self.socketio.emit("ui.system.load.updated", payload)
        elif isinstance(payload, message.MemoryUsageUpdate):
            self.socketio.emit("ui.system.memory.usage.updated", payload)
        elif isinstance(payload, message.CPUUsageUpdate):
            self.socketio.emit(
                "ui.system.cpu.usage.updated",
                {"timestamp": evt.time.timestamp(), "data": payload},
            )
        elif isinstance(payload, message.DiskUsageUpdate):
            self.socketio.emit("ui.system.disk.usage.updated", payload)
        elif isinstance(payload, message.NetworkUsageUpdate):
            self.socketio.emit(
                "ui.system.network.usage.updated",
                {"timestamp": evt.time.timestamp(), "data": payload},
            )
