import click

from .runtime import Runtime
from .sinks import ConsoleSink, JsonlSink

from .processes import SystemIdentityProcess, SystemStatsProcess
from .interfaces import SystemWebInterface
from .services import SystemIdentityService, SystemStatsService


@click.group()
def main() -> None:
    """BussDCC System Health"""


@main.command()
@click.option("--interval", default=5.0)
@click.option("--record", is_flag=True, default=False)
@click.option("--record-interval", default=600.0)
@click.option("--record-path", default="data/history")
@click.option("--quiet", is_flag=True, default=False)
def run(
    interval: float, record: bool, record_interval: float, record_path: str, quiet: bool
) -> None:
    runtime = Runtime()

    if not quiet:
        runtime.add_sink(ConsoleSink())

    if record:
        runtime.add_sink(JsonlSink(root="data/history", interval=record_interval))

    runtime.register_process(SystemIdentityProcess())
    runtime.register_process(SystemStatsProcess())

    runtime.register_interface(SystemWebInterface())

    runtime.register_service(SystemIdentityService())

    system_stats = SystemStatsService()
    system_stats.interval = interval
    runtime.register_service(system_stats)

    runtime.run()
