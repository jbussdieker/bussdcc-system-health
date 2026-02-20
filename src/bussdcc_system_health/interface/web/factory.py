from typing import Any

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap5  # type: ignore[import-untyped]

from bussdcc.context import ContextProtocol


class SystemHealthFlask(Flask):
    ctx: ContextProtocol
    socketio: SocketIO


def create_app(ctx: ContextProtocol) -> SystemHealthFlask:
    app = SystemHealthFlask(__name__)
    Bootstrap5(app)
    app.ctx = ctx
    app.socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

    @app.context_processor
    def get_context() -> dict[str, Any]:
        system_identity = ctx.state.get("system.identity")
        runtime_version = ctx.state.get("runtime.version")
        app_version = ctx.state.get("system_health.version")
        cpu_usage = ctx.state.get("system.cpu.usage")
        memory_usage = ctx.state.get("system.memory.usage")
        disk_usage = ctx.state.get("system.disk.usage")
        load = ctx.state.get("system.load")
        network_usage = ctx.state.get("system.network.usage")
        network_history = ctx.state.get("system.network.history", {})
        system_temperature = ctx.state.get("system.temperature")

        return dict(
            system_identity=system_identity,
            runtime_version=runtime_version,
            app_version=app_version,
            system_temperature=system_temperature,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            load=load,
            network_usage=network_usage,
            network_history=network_history,
        )

    @app.route("/")
    def home() -> str:
        return render_template("home.html")

    return app
