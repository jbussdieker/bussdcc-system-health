import click

from bussdcc_framework.io import ConsoleSink, JsonlSink, JsonlSource
from bussdcc_framework import (
    Runtime,
    ReplayRuntime,
    process as framework_process,
    service as framework_service,
)

from . import process, service, interface

from .version import __version__

PLUGINS = ["bootstrap", "bootstrap-layout", "formtree", "socketio", "chartjs"]


def history_path(data_dir: str) -> str:
    return f"{data_dir}/history"


@click.group()
def main() -> None:
    """BussDCC System Health"""


@main.command()
@click.option("--stats-interval", default=5.0)
@click.option("--record", is_flag=True, default=False)
@click.option("--record-interval", default=600.0)
@click.option("--data-dir", default="data")
@click.option("--quiet", is_flag=True, default=False)
@click.option("--web", is_flag=True, default=False)
@click.option("--web-host", default="127.0.0.1")
@click.option("--web-port", default=8000)
def run(
    stats_interval: float,
    record: bool,
    record_interval: float,
    data_dir: str,
    quiet: bool,
    web: bool,
    web_host: str,
    web_port: int,
) -> None:
    runtime = Runtime()
    runtime.ctx.state.set("app.version", __version__)

    if not quiet:
        runtime.add_sink(ConsoleSink())

    if record:
        runtime.add_sink(
            JsonlSink(root=history_path(data_dir), interval=record_interval)
        )

    runtime.processes.register(framework_process.SystemIdentityProcess())
    runtime.processes.register(process.SystemStatsProcess())

    runtime.services.register(framework_service.SystemIdentityService())
    runtime.services.register(service.SystemStatsService(stats_interval))

    if web:
        runtime.interfaces.register(
            interface.WebInterface(
                __name__,
                host=web_host,
                port=web_port,
                template_folder="interface/web/templates",
                static_folder="interface/web/static",
                plugins=PLUGINS,
            )
        )

    runtime.run()


@main.command()
@click.option("--speed", "-s", default=5.0)
@click.option("--data-dir", "-d", default="data")
@click.option("--web", is_flag=True, default=False)
@click.option("--web-host", default="127.0.0.1")
@click.option("--web-port", default=8000)
def replay(
    speed: float, data_dir: str, web: bool, web_host: str, web_port: int
) -> None:
    source = JsonlSource(root=history_path(data_dir))

    runtime = ReplayRuntime(speed=speed)
    runtime.ctx.state.set("app.version", __version__)

    runtime.add_sink(ConsoleSink())

    runtime.processes.register(framework_process.SystemIdentityProcess())
    runtime.processes.register(process.SystemStatsProcess())

    if web:
        runtime.interfaces.register(
            interface.WebInterface(
                __name__,
                host=web_host,
                port=web_port,
                template_folder="interface/web/templates",
                static_folder="interface/web/static",
                plugins=PLUGINS,
            )
        )

    runtime.replay(source)
