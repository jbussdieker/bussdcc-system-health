from collections import deque

from bussdcc.process import Process
from bussdcc.context import ContextProtocol
from bussdcc.event import Event


class SystemStatsProcess(Process):
    name = "system_stats"

    HISTORY_SECONDS = 300

    def __init__(self) -> None:
        self._net_history: dict[str, deque[dict[str, float | int]]] = {}

    def on_event(self, ctx: ContextProtocol, evt: Event) -> None:
        if evt.name == "system.temperature.updated":
            ctx.state.set("system.temperature", evt.data)

        elif evt.name == "system.load.updated":
            ctx.state.set("system.load", evt.data)

        elif evt.name == "system.cpu.usage.updated":
            ctx.state.set("system.cpu.usage", evt.data)

        elif evt.name == "system.memory.usage.updated":
            ctx.state.set("system.memory.usage", evt.data)

        elif evt.name == "system.disk.usage.updated":
            ctx.state.set("system.disk.usage", evt.data)

        elif evt.name == "system.network.usage.updated":
            if not evt.time:
                return

            now = evt.time.timestamp()

            ctx.state.set("system.network.usage", evt.data)

            for iface in evt.data.get("interfaces", []):
                name = iface["interface"]

                history = self._net_history.setdefault(name, deque())

                history.append(
                    {
                        "t": now,
                        "rx_bps": iface["rx_bps"],
                        "tx_bps": iface["tx_bps"],
                    }
                )

                cutoff = now - self.HISTORY_SECONDS
                while history and history[0]["t"] < cutoff:
                    history.popleft()

            ctx.state.set(
                "system.network.history",
                {k: list(v) for k, v in self._net_history.items()},
            )
