from typing import Optional, Mapping, Any
import time
import os
from pathlib import Path

import psutil

from bussdcc.context import ContextProtocol
from bussdcc.service import Service


class SystemStatsService(Service):
    name = "system_stats"
    interval = 5.0

    def __init__(self, interval: float = 5.0) -> None:
        self._prev_stat: Optional[dict[str, int]] = None
        self._prev_net: Optional[Mapping[str, Any]] = None
        self._prev_net_time: Optional[float] = None
        self.interval = interval

    def tick(self, ctx: ContextProtocol) -> None:
        self._emit_memory_usage(ctx)
        self._emit_cpu_usage(ctx)
        self._emit_load_average(ctx)
        self._emit_disk_usage(ctx)
        self._emit_temperature(ctx)
        self._emit_network_usage(ctx)

    def _emit_memory_usage(self, ctx: ContextProtocol) -> None:
        mem = psutil.virtual_memory()
        ctx.events.emit(
            "system.memory.usage.updated",
            total=mem.total,
            used=mem.used,
            available=mem.available,
            percent=mem.percent,
        )

    def _emit_cpu_usage(self, ctx: ContextProtocol) -> None:
        stat = self._stat()
        if stat is None:
            return

        if self._prev_stat is None:
            self._prev_stat = stat
            return

        delta = {k: stat[k] - self._prev_stat[k] for k in stat}

        self._prev_stat = stat

        total = sum(delta.values())
        if total == 0:
            return

        ctx.events.emit(
            "system.cpu.usage.updated",
            user=round(delta["user"] / total * 100, 1),
            system=round(delta["system"] / total * 100, 1),
            iowait=round(delta["iowait"] / total * 100, 1),
            idle=round(delta["idle"] / total * 100, 1),
        )

    def _emit_load_average(self, ctx: ContextProtocol) -> None:
        load1, load5, load15 = os.getloadavg()
        cores = os.cpu_count() or 1

        ctx.events.emit(
            "system.load.updated",
            load_1m=round(load1 / cores, 1),
            load_5m=round(load5 / cores, 1),
            load_15m=round(load15 / cores, 1),
        )

    def _emit_disk_usage(self, ctx: ContextProtocol) -> None:
        try:
            disk = psutil.disk_usage("/")
        except Exception:
            return

        ctx.events.emit(
            "system.disk.usage.updated",
            mountpoint="/",
            total=disk.total,
            used=disk.used,
            free=disk.free,
            percent=disk.percent,
        )

    def _emit_temperature(self, ctx: ContextProtocol) -> None:
        temp_c = self._read_cpu_temperature()
        if temp_c is None:
            return

        ctx.events.emit(
            "system.temperature.updated",
            value=temp_c,
        )

    def _emit_network_usage(self, ctx: ContextProtocol) -> None:
        counters = psutil.net_io_counters(pernic=True)
        now = time.time()

        # First sample — establish baseline
        if self._prev_net is None or self._prev_net_time is None:
            self._prev_net = counters
            self._prev_net_time = now
            return

        dt = now - self._prev_net_time
        if dt <= 0:
            return

        interfaces = []

        for name, cur in counters.items():
            prev = self._prev_net.get(name)
            if prev is None:
                continue

            tx_rate = (cur.bytes_sent - prev.bytes_sent) / dt
            rx_rate = (cur.bytes_recv - prev.bytes_recv) / dt

            # Ignore inactive interfaces
            if tx_rate == 0 and rx_rate == 0:
                continue

            interfaces.append(
                {
                    "interface": name,
                    "tx_bps": int(tx_rate),
                    "rx_bps": int(rx_rate),
                }
            )

        self._prev_net = counters
        self._prev_net_time = now

        if not interfaces:
            return

        ctx.events.emit(
            "system.network.usage.updated",
            interfaces=interfaces,
        )

    def _stat(self) -> Optional[dict[str, int]]:
        try:
            with open("/proc/stat", "r") as f:
                line = f.readline()
        except Exception:
            return None

        parts = line.split()
        values = list(map(int, parts[1:]))

        return {
            "user": values[0],
            "nice": values[1],
            "system": values[2],
            "idle": values[3],
            "iowait": values[4],
            "irq": values[5],
            "softirq": values[6],
            "steal": values[7] if len(values) > 7 else 0,
        }

    def _read_cpu_temperature(self) -> float | None:
        # Most Linux SBCs expose CPU temp here
        base = Path("/sys/class/thermal")

        try:
            for zone in base.glob("thermal_zone*"):
                type_file = zone / "type"
                temp_file = zone / "temp"

                if not temp_file.exists():
                    continue

                # Prefer CPU-related zones when available
                zone_type = None
                try:
                    zone_type = type_file.read_text().strip().lower()
                except Exception:
                    pass

                if zone_type and "cpu" not in zone_type and "soc" not in zone_type:
                    continue

                raw = temp_file.read_text().strip()
                return round(int(raw) / 1000.0, 1)

        except Exception:
            pass

        return None
