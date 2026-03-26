from flask import Blueprint, render_template

from bussdcc import ContextProtocol

from bussdcc_framework.web import FlaskApp, WebPlugin


class SystemStatsPlugin:
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


plugin: WebPlugin = SystemStatsPlugin()
