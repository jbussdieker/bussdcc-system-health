from typing import Optional

from bussdcc.runtime import SignalRuntime

from ..version import __name__ as name, __version__ as version


class Runtime(SignalRuntime):
    def boot(self) -> None:
        super().boot()
        self.ctx.events.emit("app.booted", name=name, version=version)

    def shutdown(self, reason: Optional[str] = None) -> None:
        self.ctx.events.emit("app.shutting_down", version=version, reason=reason)
        super().shutdown(reason)
