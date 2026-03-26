from typing import Iterable
from flask import Blueprint, render_template
from flask_socketio import SocketIO

from bussdcc import ContextProtocol, Message, Event
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin
from bussdcc_system import message


class SystemStatsPlugin(BaseWebPlugin):
    name = "system-stats"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_system_stats",
            __name__,
            url_prefix="/system/stats",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> str:
            cpu_history = ctx.state.get("system.cpu.history", {})
            cpu_temperature = ctx.state.get("system.cpu.temperature")
            cpu_usage = ctx.state.get("system.cpu.usage")
            disk_usage = ctx.state.get("system.disk.usage", {"used": 0, "total": 0})
            memory_usage = ctx.state.get("system.memory.usage", {"used": 0, "total": 0})
            network_usage = ctx.state.get("system.network.usage")
            network_history = ctx.state.get("system.network.history", {})
            system_load = ctx.state.get("system.load")

            return render_template(
                "bussdcc_system/stats/index.html",
                cpu_history=cpu_history,
                cpu_temperature=cpu_temperature,
                cpu_usage=cpu_usage,
                disk_usage=disk_usage,
                memory_usage=memory_usage,
                network_usage=network_usage,
                network_history=network_history,
                system_load=system_load,
            )

        app.register_blueprint(bp)

    def event_types(self) -> Iterable[type[Message]]:
        return (
            message.CPUTemperatureUpdate,
            message.LoadAverageUpdate,
            message.MemoryUsageUpdate,
            message.CPUUsageUpdate,
            message.DiskUsageUpdate,
            message.NetworkUsageUpdate,
        )

    def handle_event(
        self,
        app: FlaskApp,
        socketio: SocketIO,
        ctx: ContextProtocol,
        evt: Event[Message],
    ) -> None:
        payload = evt.payload

        if isinstance(payload, message.CPUTemperatureUpdate):
            socketio.emit("ui.system.cpu.temperature.updated", payload)
        elif isinstance(payload, message.LoadAverageUpdate):
            socketio.emit("ui.system.load.updated", payload)
        elif isinstance(payload, message.MemoryUsageUpdate):
            socketio.emit("ui.system.memory.usage.updated", payload)
        elif isinstance(payload, message.CPUUsageUpdate):
            socketio.emit(
                "ui.system.cpu.usage.updated",
                {"timestamp": evt.time.timestamp(), "data": payload},
            )
        elif isinstance(payload, message.DiskUsageUpdate):
            socketio.emit("ui.system.disk.usage.updated", payload)
        elif isinstance(payload, message.NetworkUsageUpdate):
            socketio.emit(
                "ui.system.network.usage.updated",
                {"timestamp": evt.time.timestamp(), "data": payload},
            )


plugin: WebPlugin = SystemStatsPlugin()
