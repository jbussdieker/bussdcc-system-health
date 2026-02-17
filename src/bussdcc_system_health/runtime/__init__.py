from typing import Optional

from bussdcc import runtime

from .. import __version__


class Runtime(runtime.SignalRuntime):
    def boot(self) -> None:
        super().boot()
        self.ctx.events.emit("system_health.booted", version=__version__)

    def shutdown(self, reason: Optional[str] = None) -> None:
        self.ctx.events.emit(
            "system_health.shutting_down", version=__version__, reason=reason
        )
        super().shutdown(reason)
