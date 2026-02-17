from .runtime import Runtime
from .sinks import ConsoleSink, JsonlSink

from .processes import SystemIdentityProcess, SystemStatsProcess, SystemHealthProcess
from .interfaces import SystemWebInterface
from .services import SystemIdentityService, SystemStatsService, SystemHealthService


def main() -> None:
    runtime = Runtime()

    runtime.add_sink(ConsoleSink())
    runtime.add_sink(JsonlSink(root="data/history", interval=600.0))

    runtime.register_process(SystemIdentityProcess())
    runtime.register_process(SystemStatsProcess())
    runtime.register_process(SystemHealthProcess())

    runtime.register_interface(SystemWebInterface())

    runtime.register_service(SystemIdentityService())
    runtime.register_service(SystemStatsService())
    runtime.register_service(SystemHealthService())

    runtime.run()
