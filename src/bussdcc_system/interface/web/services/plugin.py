from typing import Any

from flask import Blueprint, render_template, redirect, url_for, request

from bussdcc import ContextProtocol
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin


class SystemServicesPlugin(BaseWebPlugin):
    name = "system-services"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_system_services",
            __name__,
            url_prefix="/system/services",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> Any:
            supervisor = ctx.runtime.services
            services = supervisor.statuses()

            return render_template(
                "bussdcc_system/services/index.html", services=services
            )

        @bp.route("/stop/<service>")
        def stop(service: str) -> Any:
            supervisor = ctx.runtime.services
            supervisor.stop(service)

            return redirect(url_for("bussdcc_system_services.index"))

        @bp.route("/start/<service>")
        def start(service: str) -> Any:
            supervisor = ctx.runtime.services
            supervisor.start(service)

            return redirect(url_for("bussdcc_system_services.index"))

        app.register_blueprint(bp)


plugin: WebPlugin = SystemServicesPlugin()
