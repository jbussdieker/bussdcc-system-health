from .runtime import Runtime
from .services import SystemService
from .sinks import ConsoleSink, JsonlSink
from .interfaces import SystemWebInterface
from .processes import SystemProcess


def main() -> None:
    runtime = Runtime()
    runtime.add_sink(ConsoleSink())
    runtime.add_sink(JsonlSink(root="data/history", interval=600.0))
    runtime.register_service(SystemService())
    runtime.register_process(SystemProcess())
    runtime.register_interface(SystemWebInterface())
    runtime.run()
