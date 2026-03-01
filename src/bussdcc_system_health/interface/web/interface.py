from typing import Any
from flask import render_template
from flask_socketio import SocketIO

from bussdcc.context import ContextProtocol
from bussdcc.event import Event
from bussdcc.message import Message

from bussdcc_framework.interface import web
from bussdcc_framework.interface.web.base import FlaskApp

from ... import message
from ...version import __version__ as app_version


class WebInterface(web.WebInterface):
    def __init__(self, host: str, port: int) -> None:
        super().__init__(__name__, host=host, port=port)

    def register_routes(self, app: FlaskApp, ctx: ContextProtocol) -> None:

        @app.context_processor
        def get_context() -> dict[str, Any]:
            cpu_usage = ctx.state.get("system.cpu.usage")
            memory_usage = ctx.state.get("system.memory.usage")
            disk_usage = ctx.state.get("system.disk.usage")
            load = ctx.state.get("system.load")
            network_usage = ctx.state.get("system.network.usage")
            network_history = ctx.state.get("system.network.history", {})
            system_temperature = ctx.state.get("system.temperature")

            return dict(
                app_version=app_version,
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                load=load,
                network_usage=network_usage,
                network_history=network_history,
                system_temperature=system_temperature,
            )

        @app.route("/")
        def home() -> str:
            return render_template("home.html")

    def register_socketio(self, socketio: SocketIO, ctx: ContextProtocol) -> None:
        pass

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        payload = evt.payload

        if isinstance(payload, message.TemperatureUpdate):
            self.socketio.emit("ui.system.temperature.updated", payload.to_dict())
        elif isinstance(payload, message.LoadAverageUpdate):
            self.socketio.emit("ui.system.load.updated", payload.to_dict())
        elif isinstance(payload, message.MemoryUsageUpdate):
            self.socketio.emit("ui.system.memory.usage.updated", payload.to_dict())
        elif isinstance(payload, message.CPUUsageUpdate):
            self.socketio.emit("ui.system.cpu.usage.updated", payload.to_dict())
        elif isinstance(payload, message.DiskUsageUpdate):
            self.socketio.emit("ui.system.disk.usage.updated", payload.to_dict())
        elif isinstance(payload, message.NetworkUsageUpdate):
            self.socketio.emit(
                "ui.system.network.usage.updated",
                {"timestamp": evt.time.timestamp(), **payload.to_dict()},
            )
