from flask import Blueprint, render_template

from bussdcc_framework.interface.web import current_ctx

bp = Blueprint("system_stats", __name__, url_prefix="/system/stats")


@bp.route("/")
def index() -> str:
    ctx = current_ctx()

    cpu_history = ctx.state.get("system.cpu.history", {})
    cpu_temperature = ctx.state.get("system.cpu.temperature")
    cpu_usage = ctx.state.get("system.cpu.usage")
    disk_usage = ctx.state.get("system.disk.usage", {"used": 0, "total": 0})
    memory_usage = ctx.state.get("system.memory.usage", {"used": 0, "total": 0})
    network_usage = ctx.state.get("system.network.usage")
    network_history = ctx.state.get("system.network.history", {})
    system_load = ctx.state.get("system.load")

    return render_template(
        "system_stats/index.html",
        cpu_history=cpu_history,
        cpu_temperature=cpu_temperature,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        disk_usage=disk_usage,
        system_load=system_load,
        network_usage=network_usage,
        network_history=network_history,
    )
