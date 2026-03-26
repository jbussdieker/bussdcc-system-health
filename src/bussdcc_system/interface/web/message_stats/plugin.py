from typing import Any

from flask import Blueprint, render_template, redirect, url_for, request

from bussdcc import ContextProtocol
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin


class SystemMessageStatsPlugin(BaseWebPlugin):
    name = "system-message-stats"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_system_message_stats",
            __name__,
            url_prefix="/system/runtime/info",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> Any:
            message_stats = ctx.state.get("runtime_info", {})

            return render_template(
                "bussdcc_system/message_stats/index.html", message_stats=message_stats
            )

        app.register_blueprint(bp)


plugin: WebPlugin = SystemMessageStatsPlugin()
