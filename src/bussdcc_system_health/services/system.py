from typing import Optional, Mapping, Any
import time
import os
import socket
from pathlib import Path

import psutil

from bussdcc.context import ContextProtocol
from bussdcc.service import Service


class SystemService(Service):
    name = "system"
    interval = 5.0

    def __init__(self) -> None:
        self._prev_stat: Optional[dict[str, int]] = None
        self._prev_net: Optional[Mapping[str, Any]] = None
        self._prev_net_time: Optional[float] = None

    def start(self, ctx: ContextProtocol) -> None:
        hostname = socket.gethostname()
        model = self._read("/proc/device-tree/model")
        serial = self._cpuinfo_field("Serial")

        ctx.events.emit(
            "system.identity",
            hostname=hostname,
            model=model,
            serial=serial,
        )

    def tick(self, ctx: ContextProtocol) -> None:
        self._emit_memory_usage(ctx)
        self._emit_cpu_usage(ctx)
        self._emit_load_average(ctx)
        self._emit_disk_usage(ctx)
        self._emit_temperature(ctx)
        self._emit_network_usage(ctx)
        self._emit_throttling(ctx)

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
            cpu_c=temp_c,
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

    def _emit_throttling(self, ctx: ContextProtocol) -> None:
        flags = self._read_throttled_flags()
        if flags is None:
            return

        ctx.events.emit(
            "system.throttling.updated",
            **flags,
        )

    def _read(self, path: str) -> str | None:
        try:
            return Path(path).read_text().strip("\x00\n")
        except Exception:
            return None

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

    def _cpuinfo_field(self, key: str) -> str | None:
        try:
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith(key):
                    return line.split(":", 1)[1].strip()
        except Exception:
            pass
        return None

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

    def _read_throttled_flags(self) -> dict[str, bool | int] | None:
        path = Path("/sys/devices/platform/soc/soc:firmware/get_throttled")

        try:
            raw = path.read_text().strip()
            value = int(raw, 0)  # handles hex automatically
        except Exception:
            return None

        def bit(n: int) -> bool:
            return bool(value & (1 << n))

        return {
            # current state
            "undervoltage": bit(0),
            "freq_capped": bit(1),
            "throttled": bit(2),
            "soft_temp_limit": bit(3),
            # historical since boot
            "undervoltage_occurred": bit(16),
            "freq_capped_occurred": bit(17),
            "throttled_occurred": bit(18),
            "soft_temp_limit_occurred": bit(19),
            "raw": value,
        }
