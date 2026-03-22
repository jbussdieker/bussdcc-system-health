from flask import Blueprint

from bussdcc import ContextProtocol

from bussdcc_framework.web import FlaskApp, WebPlugin

from .blueprints.system_stats import bp


class SystemStatsPlugin:
    name = "system-stats"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        app.register_blueprint(bp)


plugin: WebPlugin = SystemStatsPlugin()
