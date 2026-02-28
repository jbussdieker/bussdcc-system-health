from collections import deque

from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event

from .. import events


class SystemStatsProcess(Process):
    name = "system_stats"

    HISTORY_SECONDS = 300

    def start(self, ctx: ContextProtocol) -> None:
        self._net_history: dict[str, deque[dict[str, float | int]]] = {}

    def handle_event(self, ctx: ContextProtocol, evt: Event[object]) -> None:
        payload = evt.payload

        if isinstance(payload, events.TemperatureUpdate):
            ctx.state.set("system.temperature", payload)

        if isinstance(payload, events.MemoryUsageUpdate):
            ctx.state.set("system.memory.usage", payload)

        elif isinstance(payload, events.DiskUsageUpdate):
            ctx.state.set("system.disk.usage", payload)

        elif isinstance(payload, events.LoadAverageUpdate):
            ctx.state.set("system.load", payload)

        elif isinstance(payload, events.CPUUsageUpdate):
            ctx.state.set("system.cpu.usage", payload)

        elif isinstance(payload, events.NetworkUsageUpdate):
            ctx.state.set("system.network.usage", payload)

            if not evt.time:
                return

            now = evt.time.timestamp()

            for iface in payload.interfaces:
                name = iface.interface

                history = self._net_history.setdefault(name, deque())

                history.append(
                    {
                        "t": now,
                        "rx_bps": iface.rx_bps,
                        "tx_bps": iface.tx_bps,
                    }
                )

                cutoff = now - self.HISTORY_SECONDS
                while history and history[0]["t"] < cutoff:
                    history.popleft()

            ctx.state.set(
                "system.network.history",
                {k: list(v) for k, v in self._net_history.items()},
            )
