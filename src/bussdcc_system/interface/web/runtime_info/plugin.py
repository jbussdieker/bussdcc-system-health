from typing import Any

from flask import Blueprint, render_template, redirect, url_for, request

from bussdcc import ContextProtocol
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin


class SystemRuntimeInfoPlugin(BaseWebPlugin):
    name = "system-runtime-info"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_system_runtime_info",
            __name__,
            url_prefix="/system/runtime/info",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> Any:
            runtime_info = ctx.state.get("runtime_info", {})

            return render_template(
                "bussdcc_system/runtime_info/index.html", runtime_info=runtime_info
            )

        app.register_blueprint(bp)


plugin: WebPlugin = SystemRuntimeInfoPlugin()
