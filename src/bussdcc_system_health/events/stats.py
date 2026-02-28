from typing import Optional, List
from dataclasses import dataclass

from bussdcc.events import EventSchema


@dataclass(slots=True)
class MemoryUsageUpdate(EventSchema):
    name = "system.memory.usage.updated"

    total: int
    used: int
    available: int
    percent: float


@dataclass(slots=True)
class DiskUsageUpdate(EventSchema):
    name = "system.disk.usage.updated"

    mountpoint: str
    total: int
    used: int
    free: int
    percent: float


@dataclass(slots=True)
class TemperatureUpdate(EventSchema):
    name = "system.temperature.updated"

    value: float


@dataclass(slots=True)
class LoadAverageUpdate(EventSchema):
    name = "system.load.updated"

    load_1m: float
    load_5m: float
    load_15m: float


@dataclass(slots=True)
class CPUUsageUpdate(EventSchema):
    name = "system.cpu.usage.updated"

    user: float
    system: float
    iowait: float
    idle: float


@dataclass(slots=True)
class InterfaceUsage:
    interface: str
    tx_bps: int
    rx_bps: int


@dataclass(slots=True)
class NetworkUsageUpdate(EventSchema):
    name = "system.network.usage.updated"

    interfaces: List[InterfaceUsage]
