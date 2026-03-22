from typing import Optional, List
from dataclasses import dataclass, field

from bussdcc import Message


@dataclass(slots=True, frozen=True)
class MemoryUsageUpdate(Message):
    total: int
    used: int
    available: int
    percent: float


@dataclass(slots=True, frozen=True)
class DiskUsageUpdate(Message):
    mountpoint: str
    total: int
    used: int
    free: int
    percent: float


@dataclass(slots=True, frozen=True)
class CPUTemperatureUpdate(Message):
    value: float


@dataclass(slots=True, frozen=True)
class LoadAverageUpdate(Message):
    load_1m: float
    load_5m: float
    load_15m: float


@dataclass(slots=True, frozen=True)
class CPUUsageUpdate(Message):
    user: float
    system: float
    iowait: float
    idle: float


@dataclass(slots=True, frozen=True)
class InterfaceUsage:
    interface: str
    tx_bps: int
    rx_bps: int


@dataclass(slots=True, frozen=True)
class NetworkUsageUpdate(Message):
    interfaces: List[InterfaceUsage] = field(default_factory=list)
