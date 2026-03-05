import click

from bussdcc_framework.runtime import Runtime, ReplayRuntime

from bussdcc_framework.io.console import ConsoleSink
from bussdcc_framework.io.jsonl import JsonlSink, JsonlSource

from bussdcc_framework import process as framework_process
from bussdcc_framework import service as framework_service

from . import process, interface, service


@click.group()
def main() -> None:
    """BussDCC System Health"""


@main.command()
@click.option("--stats-interval", default=5.0)
@click.option("--record", is_flag=True, default=False)
@click.option("--record-interval", default=600.0)
@click.option("--record-path", default="data/history")
@click.option("--quiet", is_flag=True, default=False)
@click.option("--web", is_flag=True, default=False)
@click.option("--web-host", default="127.0.0.1")
@click.option("--web-port", default=8086)
def run(
    stats_interval: float,
    record: bool,
    record_interval: float,
    record_path: str,
    quiet: bool,
    web: bool,
    web_host: str,
    web_port: int,
) -> None:
    runtime = Runtime()

    if not quiet:
        runtime.add_sink(ConsoleSink())

    if record:
        runtime.add_sink(JsonlSink(root=record_path, interval=record_interval))

    runtime.register_process(framework_process.SystemIdentityProcess())
    runtime.register_process(process.SystemStatsProcess())

    if web:
        runtime.register_interface(interface.WebInterface(web_host, web_port))

    runtime.register_service(framework_service.SystemIdentityService())
    runtime.register_service(service.SystemStatsService(stats_interval))

    runtime.run()


@main.command()
@click.option("--speed", "-s", default=5.0)
@click.option("--path", "-p", default="data/history")
@click.option("--web", is_flag=True, default=False)
@click.option("--web-host", default="127.0.0.1")
@click.option("--web-port", default=8086)
def replay(speed: float, path: str, web: bool, web_host: str, web_port: int) -> None:
    source = JsonlSource(path)

    runtime = ReplayRuntime(speed=speed)

    runtime.add_sink(ConsoleSink())

    runtime.register_process(framework_process.SystemIdentityProcess())
    runtime.register_process(process.SystemStatsProcess())

    if web:
        runtime.register_interface(interface.WebInterface(web_host, web_port))

    runtime.replay(source)
