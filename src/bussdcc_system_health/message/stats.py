from typing import Optional, List
from dataclasses import dataclass

from bussdcc.message import Message


@dataclass(slots=True)
class MemoryUsageUpdate(Message):
    name = "system.memory.usage.updated"

    total: int
    used: int
    available: int
    percent: float


@dataclass(slots=True)
class DiskUsageUpdate(Message):
    name = "system.disk.usage.updated"

    mountpoint: str
    total: int
    used: int
    free: int
    percent: float


@dataclass(slots=True)
class TemperatureUpdate(Message):
    name = "system.temperature.updated"

    value: float


@dataclass(slots=True)
class LoadAverageUpdate(Message):
    name = "system.load.updated"

    load_1m: float
    load_5m: float
    load_15m: float


@dataclass(slots=True)
class CPUUsageUpdate(Message):
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
class NetworkUsageUpdate(Message):
    name = "system.network.usage.updated"

    interfaces: List[InterfaceUsage]
