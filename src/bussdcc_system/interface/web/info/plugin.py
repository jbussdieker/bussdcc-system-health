from typing import Any

from flask import Blueprint, render_template, redirect, url_for, request

from bussdcc import ContextProtocol
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin


class SystemInfoPlugin(BaseWebPlugin):
    name = "system-info"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_system_info",
            __name__,
            url_prefix="/system/info",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> Any:
            return render_template("bussdcc_system/info/index.html")

        app.register_blueprint(bp)


plugin: WebPlugin = SystemInfoPlugin()
